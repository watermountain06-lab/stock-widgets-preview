// Tests for preview-only-portfolio-strategy.js 순수 함수(2026-10-20). Run: node --test pipeline/portfolio/test_strategy_view.mjs
// 화면 그리기는 브라우저에서 확인한다. 여기서는 Firestore 묶음 → 엔진 입력 변환, 비교 표 요약, 시나리오 입력 검사만 본다.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { toEngineInput, summarize, checkScenario, waitText, MAX_SCENARIOS } from '../../preview-only-portfolio-strategy.js';

const bundle = {
  snapshot: { date: '2026-10-16', holdings: { AAA: 10 }, cash: 5, holdOnly: ['AAA'], createdAt: '2026-10-16T22:00:00Z' },
  deposits: {
    d1: { amount: 100, recordedAt: '2026-11-07T15:00:00Z' },
    c1: { cancels: 'd1', recordedAt: '2026-11-08T15:00:00Z' },
  },
  scenarios: {
    s2: { name: '둘', strategy: 'C', params: { splitWeeks: 2, cashReserve: 0 }, createdAt: '2026-11-02T15:00:00Z', engineVersion: 'v' },
    s1: { name: '하나', strategy: 'B', params: { sellFraction: 0, splitWeeks: 4, cashReserve: 0 }, createdAt: '2026-10-16T22:00:00Z', engineVersion: 'v' },
  },
  lastKey: 's2',
};

test('toEngineInput: 스냅샷·holdOnly·입금(취소 포함)·시나리오(만든 순서)', () => {
  const x = toEngineInput(bundle, ['R']);
  assert.deepEqual(x.records, ['R']);
  assert.deepEqual(x.snapshot, { date: '2026-10-16', holdings: { AAA: 10 }, cash: 5 });
  assert.deepEqual(x.settings, { holdOnly: ['AAA'] });
  assert.deepEqual(x.deposits, [
    { id: 'd1', amount: 100, recordedAt: '2026-11-07T15:00:00Z' },
    { id: 'c1', cancels: 'd1', recordedAt: '2026-11-08T15:00:00Z' },
  ]);
  assert.deepEqual(x.scenarios.map((s) => [s.id, s.strategy]), [['s1', 'B'], ['s2', 'C']]);
  // 언제 만들었든 시작일 장 마감 뒤로 맞춰 A와 같이 출발한다(사용자 결정 10-20)
  assert.deepEqual(x.scenarios.map((s) => s.createdAt), ['2026-10-16T23:00:00Z', '2026-10-16T23:00:00Z']);
  assert.equal('lastKey' in x, false);
});

test('summarize: 마지막 날 값, 미확정이면 마지막 확정값, 건너뜀은 넘긴 회차 제외', () => {
  const s = {
    id: 'B', started: '2026-10-16', cash: 50,
    days: [
      { date: '2026-10-15', value: null },
      { date: '2026-10-16', value: 1000, deposits: 0, pnl: 0, twr: 0, vs: { SPY: 0 } },
      { date: '2026-10-19', value: 1100, deposits: 0, pnl: 100, twr: 0.1, vs: { SPY: 2 } },
      { date: '2026-10-20', value: null, deposits: 100, pnl: null, twr: null, vs: { SPY: null }, pause: 6 },
    ],
    trades: [{ ticker: 'AAA' }, { ticker: 'AAA' }, { ticker: 'BBB' }],
    skips: [{ action: 'carried' }, { action: 'erased' }, { action: 'dropped' }],
  };
  const m = summarize(s);
  assert.equal(m.value, null);
  assert.deepEqual(m.lastKnown, { date: '2026-10-19', value: 1100 });
  assert.equal(m.deposits, 100);
  assert.equal(m.trades, 3);
  assert.deepEqual(m.tradesByTicker, { AAA: 2, BBB: 1 });
  assert.equal(m.skipped, 2);
  assert.equal(m.elapsed, 2);
  assert.equal(m.pause, 6);
  assert.equal(m.cashShare, null);
  const ok = summarize({ ...s, days: s.days.slice(0, 3) });
  assert.equal(ok.cashShare, 50 / 1100);
  assert.equal(ok.lastKnown, null);
  assert.equal(summarize({ id: 'x', started: null, days: [{ date: 'd', value: null }], cash: 0, waiting: 'notYet' }).waiting, 'notYet');
});

test('checkScenario: 개수·이름·전략·사용자 정의 판정', () => {
  const ok = { name: '시험', strategy: 'C', params: {} };
  assert.equal(checkScenario(ok, 0), null);
  assert.match(checkScenario(ok, MAX_SCENARIOS), /20개/);
  assert.match(checkScenario({ ...ok, name: '  ' }, 0), /이름/);
  assert.match(checkScenario({ ...ok, name: 'x'.repeat(41) }, 0), /40자/);
  assert.match(checkScenario({ ...ok, strategy: 'A' }, 0), /전략/);
  assert.match(checkScenario({ ...ok, strategy: 'B' }, 0), /전략/);
  assert.match(checkScenario({ name: 'c', strategy: 'custom', params: { buyTiers: [] } }, 0), /판정/);
});

// ---- 한눈에(preview-only-portfolio-home.js) ----
import { currentHoldings, monthView } from '../../preview-only-portfolio-home.js';

test('currentHoldings: 올린 보유 + 기준일 뒤 매매(매수는 평균 단가·현금, 매도는 현금), 취소·기준일 전은 빼고, 현금 줄은 수량×단가', () => {
  const rows = [
    { ticker: 'AAA', qty: 10, avgPrice: 100, currency: 'USD', name: 'A' },
    { ticker: 'aaa', qty: 10, avgPrice: 120, currency: 'USD' },          // 다른 계좌 같은 종목 → 합침
    { ticker: '', qty: 1, avgPrice: 1000, currency: 'USD' },             // 현금
    { ticker: 'KRW1', qty: 5, avgPrice: 1, currency: 'KRW' },            // 미국 달러가 아니면 뺌
  ];
  const trades = {
    t1: { date: '2026-10-14', ticker: 'AAA', side: 'buy', qty: 5, price: 90, recordedAt: '2026-10-14T20:00:00Z' },   // 기준일 당일 → 이미 들어 있음
    t2: { date: '2026-10-20', ticker: 'BBB', side: 'buy', qty: 2, price: 50, recordedAt: '2026-10-20T20:00:00Z' },
    t3: { date: '2026-10-21', ticker: 'AAA', side: 'buy', qty: 5, price: 140, recordedAt: '2026-10-21T20:00:00Z' },
    t4: { date: '2026-10-22', ticker: 'AAA', side: 'sell', qty: 10, price: 150, recordedAt: '2026-10-22T20:00:00Z' },
    t5: { date: '2026-10-22', ticker: 'BBB', side: 'buy', qty: 100, price: 1, recordedAt: '2026-10-22T21:00:00Z' },
    x5: { cancels: 't5', recordedAt: '2026-10-22T22:00:00Z' },
  };
  const c = currentHoldings(rows, '2026-10-14 기준', trades);
  assert.deepEqual(c.skipped.map((x) => x.id), ['t1']);
  assert.deepEqual(c.applied.map((x) => x.id), ['t2', 't3', 't4']);
  const aaa = c.holdings.find((h) => h.ticker === 'AAA');
  assert.equal(aaa.qty, 15);
  assert.equal(Math.round(aaa.avgPrice * 1e6) / 1e6, 116);          // 20주 평균 110 → 5주@140 매수로 116, 팔아도 평균 단가는 그대로
  assert.equal(c.holdings.find((h) => h.ticker === 'BBB').qty, 2);
  assert.equal(c.cash, 1000 - 100 - 700 + 1500);
  assert.equal(c.holdings.some((h) => h.ticker === 'KRW1'), false);
});

test('monthView: 내 원칙(B) 우선, 회차 상태(완료·건너뜀·넘김·예정·버림), 다음 회차, 모의 매수 합계', () => {
  const mk = (id, strategy, extra = {}) => ({ id, strategy, started: '2026-10-16', trades: [], skips: [], months: [], ...extra });
  const plan = { decisionDate: '2026-12-01', candidates: ['BBB'], budget: 500,
    rounds: [{ date: '2026-12-01' }, { date: '2026-12-08' }, { date: '2026-12-15' }, { date: '2026-12-22' }, { date: '2027-01-04', dropped: true }],
    fires: [{ ticker: 'AAA', observed: '고평가', warnOnly: true }, { ticker: 'DDD', observed: null, skip: 'stale' }] };
  const B = mk('s1', 'B', { months: [plan],
    trades: [{ date: '2026-12-01', side: 'buy', amount: 100 }, { date: '2026-11-20', side: 'buy', amount: 999 }],
    skips: [{ date: '2026-12-08', action: 'carried' }, { date: '2026-12-15', action: 'erased' }] });
  const r = { scenarios: [mk('A', 'A'), mk('s0', 'C'), B] };
  const m = monthView(r, '2026-12-16');
  assert.equal(m.scenario.id, 's1');
  assert.deepEqual(m.steps.map((s) => s.state), ['done', 'done', 'carry', 'skip', 'todo', 'dropped']);
  assert.equal(m.next.date, '2026-12-22');
  // 2026-11-17: 회차는 그 주 금요일까지 — 12/15(화) 회차는 12/16 기록이 있어도 12/18(금)까지 이번 회차, 토요일부터 다음 회차
  assert.equal(monthView(r, '2026-12-16', '2026-12-17').next.date, '2026-12-15');
  assert.equal(monthView(r, '2026-12-16', '2026-12-18').next.date, '2026-12-15');
  assert.equal(monthView(r, '2026-12-18', '2026-12-19').next.date, '2026-12-22');
  assert.equal(monthView(r, '2026-12-29', '2026-12-28').next, null);
  assert.equal(m.spent, 100);
  assert.deepEqual(m.alerts.map((f) => f.ticker), ['AAA']);
  assert.equal(monthView({ scenarios: [mk('A', 'A')] }, '2026-12-16'), null);
  assert.equal(monthView({ scenarios: [mk('A', 'A'), mk('s0', 'C')] }, '2026-12-16').plan, null);
});

test('currentHoldings: 초과 매도는 가진 만큼만(clipped), 같은 날은 매수 먼저, 현금 줄 없으면 현금 미반영, upTo 뒤는 future', () => {
  const rows = [{ ticker: 'AAA', qty: 1, avgPrice: 100 }, { ticker: '', qty: 1, avgPrice: 50 }];
  const trades = {
    s1: { date: '2026-10-20', ticker: 'BBB', side: 'sell', qty: 2, price: 10, recordedAt: '2026-10-20T15:00:00Z' },   // 같은 날 매수보다 먼저 적음
    b1: { date: '2026-10-20', ticker: 'BBB', side: 'buy', qty: 2, price: 8, recordedAt: '2026-10-20T16:00:00Z' },
    s2: { date: '2026-10-21', ticker: 'AAA', side: 'sell', qty: 3, price: 120, recordedAt: '2026-10-21T15:00:00Z' },  // 1주뿐
    f1: { date: '2026-10-30', ticker: 'AAA', side: 'buy', qty: 1, price: 1, recordedAt: '2026-10-21T16:00:00Z' },
  };
  const c = currentHoldings(rows, '2026-10-16', trades, '2026-10-21');
  assert.deepEqual(c.holdings, []);
  assert.equal(c.cash, 50 - 16 + 20 + 120);
  assert.deepEqual(c.clipped, [{ id: 's2', ticker: 'AAA', short: 2 }]);
  assert.deepEqual(c.future.map((x) => x.id), ['f1']);
  assert.equal(c.hasCash, true);
  const nc = currentHoldings([{ ticker: 'AAA', qty: 1, avgPrice: 100 }], '2026-10-16', { b1: trades.b1 });
  assert.equal(nc.hasCash, false);
  assert.equal(nc.cash, 0);
  assert.equal(nc.holdings.find((h) => h.ticker === 'BBB').qty, 2);
});

test('monthView: 일부 건너뜀, 회차 당일은 끝난 것, 매도는 예산 사용에서 뺌, 건너뛴 발동은 알림 아님, 지난달 계획은 stale', () => {
  const plan = { decisionDate: '2026-12-01', candidates: ['BBB'], budget: 500,
    rounds: [{ date: '2026-12-01' }, { date: '2026-12-08' }],
    fires: [{ ticker: 'AAA', observed: '고평가' }, { ticker: 'CCC', observed: '초고평가', skip: 'noPrice' }] };
  const B = { id: 's1', strategy: 'B', started: '2026-10-16', months: [plan],
    trades: [{ date: '2026-12-01', side: 'buy', amount: 100 }, { date: '2026-12-01', side: 'sell', amount: 70 }, { date: '2026-12-08', side: 'buy', amount: 50 }],
    skips: [{ date: '2026-12-01', action: 'erased' }] };
  const m = monthView({ scenarios: [{ id: 'A', strategy: 'A', started: '2026-10-16' }, B] }, '2026-12-08');
  assert.deepEqual(m.steps.map((s) => s.state), ['done', 'partial', 'done']);
  assert.equal(m.next, null);
  assert.equal(m.spent, 150);
  assert.deepEqual(m.alerts.map((f) => f.ticker), ['AAA']);
  assert.equal(m.stale, false);
  assert.equal(monthView({ scenarios: [B] }, '2027-01-04').stale, true);
  // 기록은 아직 지난달(10-30)인데 오늘(동부)은 다음 달 — 지난달 계획을 이번 달로 보이지 않는다
  assert.equal(monthView({ scenarios: [B] }, '2026-12-30', '2027-01-02').stale, true);
  assert.equal(monthView({ scenarios: [B] }, '2026-12-30', '2026-12-31').stale, false);
});

import { etDate } from '../../preview-only-portfolio-home.js';
test('etDate: 미국 동부 날짜(UTC 자정 넘어도 동부 저녁이면 그날)', () => {
  assert.equal(etDate(Date.parse('2026-10-21T01:00:00Z')), '2026-10-20');
  assert.equal(etDate(Date.parse('2026-10-21T05:00:00Z')), '2026-10-21');
});

test('waitText: 엔진 대기 사유, 출발 평가 미확정의 마지막 사유(가격 없음 안내), 사유 없으면 아직 시작 전', () => {
  assert.equal(waitText({ started: '2026-10-19' }), null);
  assert.equal(waitText({ started: null, waiting: 'notYet' }), '아직 시작 전');
  const s = { started: null, days: [{ date: '2026-10-19', value: null, why: ['notStarted', 'noPrice:APPL'] }] };
  assert.equal(waitText(s), '출발 대기 — 가격 없음 APPL(카드 목록 밖 종목이거나 티커 오타일 수 있음)');
  assert.equal(waitText({ started: null, days: [{ date: 'd', value: null, why: ['notStarted', 'pipelineFailed'] }] }), '출발 대기 — 그날 기록 없음·실패');
  assert.equal(waitText({ started: null, days: [] }), '아직 시작 전');
  assert.equal(summarize({ ...s, cash: 0 }).waitText, waitText(s));
});

import { checkTrade } from '../../preview-only-portfolio-home.js';
test('checkTrade: 기록·고치기 공통 검사', () => {
  const ok = { date: '2026-10-20', ticker: 'AAPL', side: 'buy', qty: 1.5, price: 100 };
  assert.equal(checkTrade(ok, '2026-10-20'), null);
  assert.match(checkTrade({ ...ok, date: '2026-10-21' }, '2026-10-20'), /미래/);
  assert.match(checkTrade({ ...ok, date: '' }, '2026-10-20'), /날짜/);
  assert.match(checkTrade({ ...ok, ticker: 'aapl' }, '2026-10-20'), /티커/);
  assert.match(checkTrade({ ...ok, side: 'hold' }, '2026-10-20'), /매수/);
  assert.match(checkTrade({ ...ok, qty: 0.0000001 }, '2026-10-20'), /소수 6자리/);
  assert.match(checkTrade({ ...ok, price: 0 }, '2026-10-20'), /체결가/);
  assert.match(checkTrade({ ...ok, qty: 2e7 }, '2026-10-20'), /1천만/);
});

import { depositsSince } from '../../preview-only-portfolio-home.js';
test('depositsSince: 기준일 뒤·오늘까지, 반영 전 취소 빼고, 끝낸 묶음 포함, 같은 날·같은 금액도 기록마다 한 건', () => {
  const all = {
    'b1:d1': { amount: 500, recordedAt: '2026-10-19T20:00:00Z' },   // 10-20 반영(끝낸 묶음)
    'b1:d2': { amount: 100, recordedAt: '2026-10-19T20:05:00Z' },
    'b1:c2': { cancels: 'b1:d2', recordedAt: '2026-10-19T21:00:00Z' },   // 반영 전 취소
    'b2:e1': { amount: 500, recordedAt: '2026-10-19T22:00:00Z' },   // 다른 묶음의 같은 날·같은 금액 — 따로 센다
    'b2:e2': { amount: 500, recordedAt: '2026-10-20T20:00:00Z' },   // 10-21 반영
    'b2:e4': { amount: 500, recordedAt: '2026-10-20T20:30:00Z' },   // 같은 묶음 같은 날·같은 금액 — 따로 센다
    'b2:e3': { amount: 70, recordedAt: '2026-10-14T20:00:00Z' },    // 기준일(10-16) 전 반영
  };
  assert.deepEqual(depositsSince(all, '2026-10-16', '2026-10-21').map((p) => [p.day, p.amount]),
    [['2026-10-20', 500], ['2026-10-20', 500], ['2026-10-21', 500], ['2026-10-21', 500]]);
  assert.equal(depositsSince(all, '2026-10-16', '2026-10-20').length, 4);   // 계좌 현금은 기록한 날부터(10-25 사용자 결정) — 10-20 기록분도 10-20에 든다
  assert.equal(depositsSince(all, '2026-10-16', '2026-10-19').length, 2);   // 기록 전 날에는 아직
});

import { paramsText } from '../../preview-only-portfolio-strategy.js';
test('paramsText: 전략 설정 한 줄 요약', () => {
  assert.equal(paramsText({ strategy: 'C', params: { splitWeeks: 4, cashReserve: 0 } }), '살 판정 초저평가·저평가 · 매도 안 팖 · 4회 · 유보 0%');
  assert.equal(paramsText({ strategy: 'D', params: { splitWeeks: 2, cashReserve: 0.1 } }), '살 판정 원칙 1(초저평가·저평가·적정~저평가) · 매도 고평가면 전부 · 2회 · 유보 10%');
  assert.equal(paramsText({ strategy: 'custom', params: { buyTiers: ['저평가', '적정'], sellFraction: 0.5, splitWeeks: 1, cashReserve: 0 } }), '살 판정 저평가·적정 · 매도 고평가면 50% · 1회 · 유보 0%');
  assert.equal(paramsText({ strategy: 'B', params: { sellFraction: 0 } }), '살 판정 원칙 1(초저평가·저평가·적정~저평가) · 매도 원칙 4(고평가 나눠 전부·초고평가 한 번에) · 4회 · 유보 0%');
});

import { lossAlerts } from '../../preview-only-portfolio-home.js';

test('lossAlerts: 평균 단가보다 20% 넘게 내린 종목만(원칙 4), 하락 큰 순, 평균·가격 없으면 건너뜀', () => {
  const px = { AAA: 7.999, BBB: 7.5, CCC: 8.01, DDD: 1, EEE: null, FFF: 80 };
  const h = [
    { ticker: 'AAA', qty: 1, avgPrice: 10 },     // −20.01% → 알림
    { ticker: 'BBB', qty: 1, avgPrice: 10 },     // −25%
    { ticker: 'CCC', qty: 1, avgPrice: 10 },     // −19.9% → 아님
    { ticker: 'DDD', qty: 1, avgPrice: null },   // 평균 없음
    { ticker: 'EEE', qty: 1, avgPrice: 10 },     // 가격 없음
    { ticker: 'FFF', qty: 1, avgPrice: 100 },    // 정확히 −20% → 아님("넘게")
  ];
  const r = lossAlerts(h, (t) => px[t] ?? null);
  assert.deepEqual(r.map((x) => x.ticker), ['BBB', 'AAA']);
  assert.ok(Math.abs(r[0].drop + 0.25) < 1e-12);
  assert.deepEqual(lossAlerts(h, (t) => px[t] ?? null, 0.3), []);
});

import { draftOf, shapeOf, sentenceOf, rankRows, spyLine } from '../../preview-only-portfolio-rank.js';

test('편집기: 저장된 전략 ↔ 편집기 값, 저평가만·갈아타기는 값을 안 바꾸면 그대로', () => {
  assert.deepEqual(draftOf(null), { kind: 'verdict', tiers: ['초저평가', '저평가', '적정~저평가'], sell: 0, rounds: 4, reserve: 0, mode: 'split', etfShare: 100, etfs: ['SPY', 'QQQ', 'RSP'] });
  const C = { strategy: 'C', params: { splitWeeks: 2, cashReserve: 0.1 } };
  assert.deepEqual(draftOf(C), { kind: 'verdict', tiers: ['초저평가', '저평가'], sell: 0, rounds: 2, reserve: 10, mode: 'split', etfShare: 100, etfs: ['SPY', 'QQQ', 'RSP'] });
  assert.deepEqual(shapeOf('C', draftOf(C)), { strategy: 'C', params: { splitWeeks: 2, cashReserve: 0.1 } });
  assert.equal(shapeOf('C', { ...draftOf(C), sell: 25 }).strategy, 'custom');
  const D = { strategy: 'D', params: { splitWeeks: 4, cashReserve: 0 } };
  assert.equal(draftOf(D).sell, 100);
  assert.equal(shapeOf('D', draftOf(D)).strategy, 'D');
  // 새 전략·사용자 정의는 사용자 정의로, 살 판정은 판정 순서대로
  assert.deepEqual(shapeOf(null, { kind: 'verdict', tiers: ['적정', '초저평가'], sell: 50, rounds: 1, reserve: 20 }),
    { strategy: 'custom', params: { buyTiers: ['초저평가', '적정'], sellFraction: 0.5, splitWeeks: 1, cashReserve: 0.2 } });
  const cu = { strategy: 'custom', params: { buyTiers: ['저평가'], sellFraction: 0.33, splitWeeks: 3, cashReserve: 0 } };
  assert.deepEqual(draftOf(cu), { kind: 'verdict', tiers: ['저평가'], sell: 33, rounds: 3, reserve: 0, mode: 'split', etfShare: 100, etfs: ['SPY', 'QQQ', 'RSP'] });
  // 순위 1주씩(10-25): 저평가만·갈아타기에서 골라도 직접 만든 전략으로, 저장 값에 buyMode, 되읽으면 mode
  const r1 = shapeOf('C', { ...draftOf(C), mode: 'rank1' });
  assert.deepEqual(r1, { strategy: 'custom', params: { buyTiers: ['초저평가', '저평가'], sellFraction: 0, splitWeeks: 2, cashReserve: 0.1, buyMode: 'rank1' } });
  assert.equal(draftOf(r1).mode, 'rank1');
  assert.match(sentenceOf(null, { ...draftOf(null), mode: 'rank1' }), /1주씩/);
  for (const m of ['cap', 'tier']) { const x = shapeOf(null, { ...draftOf(null), mode: m }); assert.equal(x.params.buyMode, m); assert.equal(draftOf(x).mode, m); }
  assert.equal(shapeOf(null, draftOf(null)).params.buyMode, undefined);   // 균등은 칸을 두지 않는다
  assert.match(sentenceOf(null, { ...draftOf(null), mode: 'cap' }), /시가총액 비례/);
  assert.match(sentenceOf('C', draftOf(C)), /팔지 않습니다/);
  assert.match(sentenceOf(null, draftOf(null)), /매주 회차일에 판정을 보고, 고평가면 전부/);   // 원칙 전략(비율 0%)은 원칙 4 매도(2026-10-28)
  assert.match(sentenceOf(null, { ...draftOf(null), tiers: ['저평가'] }), /알림만/);              // 직접 고른 판정 + 비율 0%는 알림만
  assert.match(sentenceOf(null, draftOf(null)), /알림만/);
  assert.match(sentenceOf(null, { tiers: ['고평가'], sell: 0, rounds: 4, reserve: 0 }), /원칙과 다름/);
  assert.match(sentenceOf(null, { tiers: ['저평가'], sell: 25, rounds: 1, reserve: 10 }), /한 번에.*25%.*10%/);
  // ETF 섞기(E): 비율·고른 ETF를 엔진 순서(SPY·RSP·QQQ)로 저장하고, 되읽으면 같은 값
  const e = { ...draftOf(null), kind: 'etf', etfShare: 50, etfs: ['QQQ', 'SPY'] };
  assert.deepEqual(shapeOf('custom', e), { strategy: 'E', params: { etfShare: 0.5, etfs: ['SPY', 'QQQ'] } });
  assert.deepEqual(draftOf(shapeOf(null, e)), { ...e, etfs: ['SPY', 'QQQ'] });
  assert.match(sentenceOf(null, e), /보유 종목\(고른 ETF는 빼고\)의 50%를 팔아 SPY·QQQ에/);
  assert.match(sentenceOf(null, { ...e, etfShare: 100 }), /빼고\)을 모두/);
  assert.match(sentenceOf(null, { ...e, etfs: [] }), /하나 이상/);
  assert.equal(draftOf({ strategy: 'E' }).etfShare, 100);
  assert.equal(checkScenario({ name: 'x', strategy: 'E', params: { etfShare: 1, etfs: [] } }, 0), '살 ETF를 하나 이상 고르세요.');
  assert.equal(checkScenario({ name: 'x', strategy: 'E', params: { etfShare: 1 } }, 0), null);   // 안 적으면 엔진처럼 세 개 다
  assert.match(checkScenario({ name: 'x', strategy: 'E', params: { etfs: ['GLD'] } }, 0), /가운데서/);
  assert.match(checkScenario({ name: 'x', strategy: 'E', params: { etfs: ['SPY', 'SPY'] } }, 0), /가운데서/);
  assert.match(checkScenario({ name: 'x', strategy: 'E', params: { etfShare: 1.5 } }, 0), /0~100%/);
  // 소수 비율도 열었다 저장하면 그대로(dr r1): 0.333333 → 33.3333% → 0.333333
  const odd = { strategy: 'E', params: { etfShare: 0.333333, etfs: ['SPY'] } };
  assert.equal(draftOf(odd).etfShare, 33.3333);
  assert.deepEqual(shapeOf('E', draftOf(odd)), { strategy: 'E', params: { etfShare: 0.333333, etfs: ['SPY'] } });
  const oddC = { strategy: 'custom', params: { buyTiers: ['저평가'], sellFraction: 0.123457, splitWeeks: 2, cashReserve: 0.015 } };
  assert.deepEqual(shapeOf('custom', draftOf(oddC)), oddC);
  // 기본 ETF 목록은 draft마다 새 배열
  draftOf(null).etfs.push('X'); assert.deepEqual(draftOf(null).etfs, ['SPY', 'QQQ', 'RSP']);
  assert.equal(checkScenario({ name: 'x', strategy: 'E', params: { etfShare: 1, etfs: ['SPY'] } }, 0), null);
  assert.equal(paramsText({ strategy: 'E', params: { etfShare: 0.25, etfs: ['SPY', 'QQQ'] } }), '보유 종목의 25%를 ETF로 · SPY·QQQ · 현금 그대로 · 그 뒤 매매 없음');
  assert.match(paramsText({ strategy: 'E', params: { etfs: ['SPY', 'RSP', 'QQQ'] } }), /SPY·QQQ·RSP/);   // 편집기와 같은 순서
});

test('순위: 수익률·SPY 대비 순, 값 없는 줄은 맨 뒤, 그래프와 같은 색 번호', () => {
  const sc = (id, twr, spy, value) => ({ id, strategy: id === 'A' ? 'A' : 'custom', started: twr == null ? null : '2026-10-16',
    days: twr == null ? [] : [{ date: '2026-10-16', value, deposits: 0, pnl: 0, twr, vs: { SPY: spy } }], trades: [], skips: [], cash: 0,
    baselines: id === 'A' ? { SPY: [{ date: '2026-10-16', twr: 0.02 }, { date: '2026-10-17', twr: null }] } : undefined });
  const result = { scenarios: [sc('REAL', 0.05, 3, 90), sc('A', 0.07, 5, 100), sc('s1', null), sc('s2', 0.09, 7, 80)] };
  const byId = { s1: { name: '하나' }, s2: { name: '둘' } };
  assert.deepEqual(rankRows(result, byId, 'twr').map((r) => r.id), ['REAL', 's2', 'A', 's1']);
  assert.deepEqual(rankRows(result, byId, 'value').map((r) => r.id), ['REAL', 'A', 's2', 's1']);
  const r = rankRows(result, byId, 'spy');
  assert.equal(r[0].id, 'REAL'); assert.equal(r[1].name, '둘'); assert.equal(r[1].slot, 4); assert.equal(r.at(-1).twr, null);
  assert.equal(r.find((x) => x.id === 'REAL').auto, true);
  assert.equal(spyLine(result), 0.02);
});

import { timelineItems } from '../../preview-only-portfolio-records.js';

test('기록 목록: 매매·입금·스냅샷·올린 보유를 최신순으로, 취소된 입금 표시', () => {
  const trades = { t1: { date: '2026-10-19', ticker: 'BBB', side: 'buy', qty: 3, price: 54.1 }, t2: { date: '2026-10-10', ticker: 'AAA', side: 'sell', qty: 1, price: 10 } };
  const cur = { skipped: [{ id: 't2' }], future: [], clipped: [] };
  const bundle = { snapshot: { date: '2026-10-16', holdings: { AAA: 10 }, cash: 5 },
    deposits: { d1: { amount: 100, recordedAt: '2026-11-07T15:00:00Z' }, c1: { cancels: 'd1', recordedAt: '2026-11-07T16:00:00Z' } } };
  const items = timelineItems({ trades, cur, bundle, bundleNo: 1, holdings: { asOf: '2026-10-16 기준', rows: [{ ticker: 'AAA' }, { ticker: '' }] },
    now: Date.parse('2026-12-01T00:00:00Z'), etDate });
  assert.deepEqual(items.map((x) => x.kind + ':' + x.date), ['deposit:2026-11-07', 'trade:2026-10-19', 'snap:2026-10-16', 'upload:2026-10-16', 'trade:2026-10-10']);
  assert.match(items[0].detail, /취소됨/);
  assert.match(items[1].amount, /^−\$162\.30$/);
  assert.match(items.at(-1).detail, /기준일 전/);
  assert.match(items[3].detail, /1종목 \+ 현금/);
  // 끝낸 묶음이면 입금·스냅샷은 목록에 없다
  assert.deepEqual(timelineItems({ trades: {}, cur: { skipped: [], future: [], clipped: [] }, bundle: { ...bundle, closed: {} }, holdings: {}, now: 0, etDate }), []);
});

import { nextAction } from '../../preview-only-portfolio-home.js';

test('다음 할 일: 다음 회차·결정 대기·회차 끝·첫 점검 대기', () => {
  assert.equal(nextAction(null), null);
  assert.match(nextAction({ plan: null }).title, /첫 점검일/);
  const rounds = [{ date: '2026-12-01' }, { date: '2026-12-08' }, { date: '2026-12-15' }, { date: '2026-12-22' }];
  const plan = { rounds, candidates: ['BBB', 'EEE'] };
  const steps = [{ state: 'done' }, { state: 'done' }, { state: 'skip' }, { state: 'todo' }, { state: 'todo' }];
  const a = nextAction({ plan, steps, next: rounds[2], stale: false });
  assert.equal(a.title, '12월 15일 주, 3번째 나눠 사기');
  assert.equal(a.sub, '구매 후보 BBB · EEE · 4회 중 2회 진행');
  assert.deepEqual([a.done, a.total], [2, 4]);
  assert.equal(nextAction({ plan, steps, next: null, stale: true }).title, '이번 달 결정 대기');
  assert.match(nextAction({ plan: { rounds, candidates: [] }, steps, next: null, stale: false }).sub, /구매 후보 없음 · 다음 점검/);
});

import { buyPlan, monthDeposits, monthBuys } from '../../preview-only-portfolio-home.js';
import { tierWeights } from '../../preview-only-portfolio-engine.js';
const W_OLD = tierWeights('2026-10');

test('원칙 3 매수 금액: 체크한 종목만, 균등·시총 비중·판정 가중, 센트 내림', () => {
  const tiers = { BBB: '저평가', CCC: '적정~저평가', EEE: '적정' };
  const p = buyPlan({ cands: ['BBB', 'CCC', 'EEE'], picked: ['BBB', 'EEE'], budget: 400, tiers, caps: { BBB: 3e12, EEE: 1e12 }, rounds: 4, weights: W_OLD });
  assert.deepEqual(p.sel, ['BBB', 'EEE']);
  assert.deepEqual(p.by.equal, { BBB: 200, EEE: 200 });
  assert.deepEqual(p.by.cap, { BBB: 300, EEE: 100 });   // 큰 시총도 1센트 틀리지 않게
  assert.deepEqual(p.by.tier, { BBB: 300, EEE: 100 });   // 옛 판: 저평가 3 : 적정 1
  // 새 판(11월 계획부터, 기본값): 저평가 2 : 적정~저평가 1, 적정은 무게 없음 → 판정 가중 계산 안 함
  assert.deepEqual(buyPlan({ cands: ['BBB', 'CCC'], picked: ['BBB', 'CCC'], budget: 300, tiers }).by.tier, { BBB: 200, CCC: 100 });
  assert.equal(buyPlan({ cands: ['BBB', 'EEE'], picked: ['BBB', 'EEE'], budget: 300, tiers }).by.tier, null);
  assert.deepEqual(p.round.equal, { BBB: 50, EEE: 50 });
  // 내림: 200/3 = 66.666… → 66.66, 회차 66.66/4 = 16.665 → 16.66
  const q = buyPlan({ cands: ['A', 'B', 'C'], picked: ['A', 'B', 'C'], budget: 200, rounds: 4 });
  assert.deepEqual(q.by.equal, { A: 66.66, B: 66.66, C: 66.66 });
  assert.deepEqual(q.round.equal, { A: 16.66, B: 16.66, C: 16.66 });
  // 회차 금액은 회차 안에서 고정(2026-11-09): 1회차 놓치고 2회차에 $1000을 3회로 → $333.33, 그 회차에 다 사도 금액은 그대로, 더 살 돈(todo)만 0
  const f0 = buyPlan({ cands: ['A'], picked: ['A'], budget: 1000, rounds: 4, roundsLeft: 3 });
  assert.equal(f0.round.equal.A, 333.33);
  const f1 = buyPlan({ cands: ['A'], picked: ['A'], budget: 1000, spent: 333.33, bought: { A: 333.33 }, boughtNow: { A: 333.33 }, rounds: 4, roundsLeft: 3 });
  assert.equal(f1.round.equal.A, 333.33);
  assert.equal(f1.todo.equal.A, 0);
  assert.equal(f1.rest.equal.A, 666.67);
  const f2 = buyPlan({ cands: ['A'], picked: ['A'], budget: 1000, spent: 100, bought: { A: 100 }, boughtNow: { A: 100 }, rounds: 4, roundsLeft: 3 });
  assert.equal(f2.round.equal.A, 333.33);
  assert.equal(f2.todo.equal.A, 233.33);
  // 달러 실수 오차로 1센트 빠지지 않게(1.16 × 100 = 115.999…)
  assert.equal(buyPlan({ cands: ['A'], picked: ['A'], budget: 1.16, rounds: 4 }).round.equal.A, 0.29);
  // 무게가 없는 종목이 하나라도 있으면 그 방법은 계산하지 않는다
  assert.equal(buyPlan({ cands: ['BBB', 'CCC'], picked: ['BBB', 'CCC'], budget: 100, tiers, caps: { BBB: 1 } }).by.cap, null);
  assert.equal(buyPlan({ cands: ['X'], picked: ['X'], budget: 100, tiers: { X: '고평가' } }).by.tier, null);
  assert.equal(buyPlan({ cands: ['BBB'], picked: [], budget: 100 }).by.equal, null);
  assert.deepEqual(buyPlan({ cands: ['BBB'], picked: ['BBB'], budget: 0 }).round.equal, { BBB: 0 });

  // 정확한 정수 내림(dr r2): 무게 1·1·2·3·4(합 11)에 $0.55 → 저평가 3/11 = 15센트(실수 비율이면 14)
  const T5 = { A: '적정', B: '적정', C: '적정~저평가', D: '저평가', E: '초저평가' };
  assert.equal(buyPlan({ cands: ['A', 'B', 'C', 'D', 'E'], picked: ['A', 'B', 'C', 'D', 'E'], budget: 0.55, tiers: T5, weights: W_OLD }).by.tier.D, 0.15);
  // 나누어떨어지지 않는 큰 시총: 각 몫이 정확한 내림값이고 합은 넣은 돈 이하
  const caps = { A: 2345678901234, B: 1234567890123 };
  const c = buyPlan({ cands: ['A', 'B'], picked: ['A', 'B'], budget: 1234.57, caps }).by.cap;
  const tot = BigInt(caps.A + caps.B);
  assert.equal(c.A, Number((123457n * BigInt(caps.A)) / tot) / 100);
  assert.equal(c.B, Number((123457n * BigInt(caps.B)) / tot) / 100);
  assert.ok(Math.round((c.A + c.B) * 100) <= 123457);
});

test('원칙 3 놓친 회차: 남은 몫 ÷ 남은 회차, 남은 돈을 넘지 않음, 회차 끝이면 없음', () => {
  // 달 몫 200씩, BBB는 이미 50 삼, 남은 회차 2 → BBB (200−50)/2 = 75(놓친 몫 포함), EEE 200/2 = 100
  const p = buyPlan({ cands: ['BBB', 'EEE'], picked: ['BBB', 'EEE'], budget: 400, spent: 50, bought: { BBB: 50 }, rounds: 4, roundsLeft: 2 });
  assert.deepEqual(p.round.equal, { BBB: 75, EEE: 100 });
  assert.deepEqual(p.missed.equal, ['BBB', 'EEE']);
  // 후보 아닌 종목에 300을 써서 남은 돈이 100뿐이면 남은 몫(200+200)을 100에 맞춰 줄인다
  const q = buyPlan({ cands: ['BBB', 'EEE'], picked: ['BBB', 'EEE'], budget: 400, spent: 300, bought: { ZZZ: 300 }, rounds: 4, roundsLeft: 4 });
  assert.deepEqual(q.rest.equal, { BBB: 50, EEE: 50 });
  assert.deepEqual(q.round.equal, { BBB: 12.5, EEE: 12.5 });
  assert.deepEqual(q.missed.equal, []);
  assert.equal(q.capped.equal, true);
  // 홀수 금액 비례 축소: 남은 몫 합·회차 금액 × 남은 회차 합이 남은 돈을 넘지 않는다
  const o = buyPlan({ cands: ['A', 'B', 'C'], picked: ['A', 'B', 'C'], budget: 100.01, spent: 33.37, bought: { A: 3.33, Z: 30.04 }, rounds: 4, roundsLeft: 3 });
  const restC = Object.values(o.rest.equal).reduce((a, v) => a + Math.round(v * 100), 0);
  const roundC = Object.values(o.round.equal).reduce((a, v) => a + Math.round(v * 100) * 3, 0);
  assert.ok(o.capped.equal && restC <= 6664 && roundC <= restC);
  // 계획대로 1회차를 샀으면 놓친 몫이 아니다
  const n = buyPlan({ cands: ['BBB'], picked: ['BBB'], budget: 200, spent: 50, bought: { BBB: 50 }, rounds: 4, roundsLeft: 3 });
  assert.deepEqual([n.round.equal.BBB, n.missed.equal, n.capped.equal], [50, [], false]);
  // 넣은 돈보다 많이 샀으면 0, 회차가 끝났으면 회차 금액 없음
  assert.deepEqual(buyPlan({ cands: ['A'], picked: ['A'], budget: 100, spent: 150, bought: { A: 150 }, roundsLeft: 1 }).round.equal, { A: 0 });
  assert.equal(buyPlan({ cands: ['A'], picked: ['A'], budget: 100, roundsLeft: 0 }).round.equal, null);
});

test('원칙 3 넣은 돈·산 돈: 반영일 기준 달, 묶음 전부, 취소, 그달 1일~오늘 매수', () => {
  const all = {
    'b1:d1': { amount: 100, recordedAt: '2026-10-31T16:00:00Z' },   // 토요일 → 반영일 11-02
    'b1:d2': { amount: 50, recordedAt: '2026-10-15T15:00:00Z' },
    'b2:d1': { amount: 30, recordedAt: '2026-11-03T15:00:00Z' },
    'b2:d2': { amount: 70, recordedAt: '2026-11-04T15:00:00Z' },
    'b2:c1': { cancels: 'b2:d2', recordedAt: '2026-11-04T15:05:00Z' },
  };
  const oct = monthDeposits(all, '2026-10'), nov = monthDeposits(all, '2026-11');
  assert.deepEqual(oct.now.map((d) => d.amount), [50]);
  assert.deepEqual(oct.later.map((d) => [d.day, d.amount]), [['2026-11-02', 100], ['2026-11-04', 30]]);
  assert.deepEqual(nov.now.map((d) => [d.day, d.amount]), [['2026-11-02', 100], ['2026-11-04', 30]]);
  const trades = {
    t1: { date: '2026-11-02', ticker: 'A', side: 'buy', qty: 2, price: 10 },
    t2: { date: '2026-11-05', ticker: 'A', side: 'buy', qty: 1, price: 10 },
    t3: { date: '2026-11-03', ticker: 'B', side: 'sell', qty: 1, price: 10 },
    t4: { date: '2026-10-30', ticker: 'A', side: 'buy', qty: 1, price: 10 },
    t5: { date: '2026-11-03', ticker: 'B', side: 'buy', qty: 1, price: 20 },
    x5: { cancels: 't5' },
  };
  assert.deepEqual([...monthBuys(trades, '2026-11', '2026-11-04')], [['A', { qty: 2, amount: 20 }]]);
});

import { monthSells, prevMonth } from '../../preview-only-portfolio-home.js';

test('원칙 4 판 돈: 그달 매도 대금(취소 빼고 1일~오늘), 지난달 계산', () => {
  const trades = {
    s1: { date: '2026-11-03', ticker: 'A', side: 'sell', qty: 2, price: 10.5 },
    s2: { date: '2026-11-20', ticker: 'B', side: 'sell', qty: 1, price: 30 },
    s3: { date: '2026-11-05', ticker: 'C', side: 'sell', qty: 1, price: 99 },
    x3: { cancels: 's3' },
    b1: { date: '2026-11-04', ticker: 'A', side: 'buy', qty: 1, price: 10 },
    s4: { date: '2026-10-30', ticker: 'A', side: 'sell', qty: 1, price: 7 },
  };
  assert.equal(monthSells(trades, '2026-11', '2026-11-10'), 21);
  assert.equal(monthSells(trades, '2026-11', '2026-11-30'), 51);
  assert.equal(monthSells(trades, '2026-10', '2026-11-30'), 7);
  assert.equal(prevMonth('2026-11'), '2026-10');
  assert.equal(prevMonth('2027-01'), '2026-12');
});

import { holdReason } from '../../preview-only-portfolio-home.js';

test('원칙 6 보류 이유: 엔진과 같은 판단(tierStatus는 보지 않음), 기록 없음·기록 묵음', () => {
  const rec = { session: '2026-10-21' };
  assert.equal(holdReason({ tier: '저평가', tierStatus: 'normalized', verdictAsOf: '2026-10-21' }, rec), null);   // 실제 기록의 55종목이 normalized
  assert.equal(holdReason(undefined, rec), 'noCard');
  assert.equal(holdReason({ tier: null, verdictAsOf: '2026-10-21' }, rec), 'noVerdict');
  assert.equal(holdReason({ tier: '저평가', priceStale: true, verdictAsOf: '2026-10-21' }, rec), 'stale');
  assert.equal(holdReason({ tier: '저평가', verdictAsOf: '2026-10-01' }, rec), 'stale');   // 판정 날짜가 5거래일 넘게 묵음
  assert.equal(holdReason({ tier: '저평가', verdictAsOf: '2026-10-21' }, null), 'noRecord');
  // 기록 자체가 오늘보다 5거래일 넘게 묵었으면(파이프라인 여러 날 실패) 보류, 주말은 거래일이 아니라 세지 않는다
  const ok = { tier: '저평가', verdictAsOf: '2026-10-21' };
  assert.equal(holdReason(ok, rec, '2026-10-25'), null);          // 토·일 뒤 일요일: 10-22·23 두 거래일
  assert.equal(holdReason(ok, rec, '2026-10-28'), null);          // 22·23·26·27·28 = 5거래일
  assert.equal(holdReason(ok, rec, '2026-10-29'), 'recordStale'); // 6거래일
  // 판정 날짜는 오늘까지 센다: 판정 10-14·기록 10-21(5거래일)·오늘 10-28(5거래일) → 판정은 10거래일 묵음
  assert.equal(holdReason({ tier: '저평가', verdictAsOf: '2026-10-14' }, rec, '2026-10-28'), 'stale');
  assert.equal(holdReason({ tier: '저평가', verdictAsOf: '2026-10-21' }, rec, '2026-10-28'), null);
});

test('원칙 3 산 돈: 매수도 거래마다 센트로 반올림해 더한다', () => {
  const t = { a: { date: '2026-11-02', ticker: 'A', side: 'buy', qty: 0.0014, price: 10 }, b: { date: '2026-11-03', ticker: 'A', side: 'buy', qty: 0.0014, price: 10 } };
  assert.equal(monthBuys(t, '2026-11', '2026-11-30').get('A').amount, 0.02);   // 거래당 $0.014 → 1센트씩
});

import { lossReviewable } from '../../preview-only-portfolio-home.js';

test('원칙 4·6 20% 매도 검토 대상: 카드 있으면 원칙 6 통과, 카드 없으면 지수 ETF만', () => {
  const rec = { session: '2026-10-21', cards: { AAA: { tier: '고평가', verdictAsOf: '2026-10-21' }, BBB: { tier: '저평가', priceStale: true, verdictAsOf: '2026-10-21' } } };
  assert.equal(lossReviewable('AAA', rec, '2026-10-22'), true);
  assert.equal(lossReviewable('BBB', rec, '2026-10-22'), false);   // 가격 묵음
  assert.equal(lossReviewable('ZZZ', rec, '2026-10-22'), false);   // 카드 없는 개별 종목
  assert.equal(lossReviewable('SPY', rec, '2026-10-22'), true);    // 지수 ETF는 카드 없어도
  assert.equal(lossReviewable('SPY', rec, '2026-10-29'), false);   // 기록이 묵으면 ETF도 보류
  assert.equal(lossReviewable('SPY', null, '2026-10-22'), false);
});

import { chainPreStart } from '../../preview-only-portfolio-home.js';

test('시작 전 실제 계좌 흐름 잇기(A안): 같은 날·보유·출발 평가액일 때만, 입출금은 사이트와 같은 규칙(장 시작 전)', () => {
  const pre = { from: '2026-10-01', base: '2026-09-30', end: '2026-10-20', endHoldings: { AAA: 2 }, endCash: 50,
    days: [{ d: '2026-09-30', v: 1000, f: 0 }, { d: '2026-10-08', v: 1600, f: 500 }, { d: '2026-10-20', v: 1200, f: 0 }],
    spy: { base: 100, end: 105 } };
  const snap = { date: '2026-10-20', holdings: { AAA: 2 }, cash: 50 };
  const real = { started: '2026-10-20', twr: 0.1, vs: { SPY: 2 } };   // SPY 실제 구간 0.08
  const r = chainPreStart(pre, real, snap, 1200);
  // 시작 전: 1600/(1000+500) × 1200/1600 = 0.8 → −0.2. 전체 0.8 × 1.1 − 1 = −0.12. SPY 1.05 × 1.08 − 1 = 0.134 → −25.4%p
  assert.ok(Math.abs(r.preTwr - -0.2) < 1e-12);
  assert.ok(Math.abs(r.twr - -0.12) < 1e-12);
  assert.ok(Math.abs(r.vsSPY - -25.4) < 1e-9);
  assert.match(chainPreStart(pre, real, snap, 1210).why, /평가액/);          // 보유·현금이 같아도 평가액이 다르면 잇지 않음
  assert.match(chainPreStart(pre, real, snap, undefined).why, /평가액/);
  assert.match(chainPreStart(pre, real, { ...snap, cash: 51 }, 1200).why, /보유·현금/);
  assert.match(chainPreStart(pre, real, { ...snap, holdings: { AAA: 2, BBB: 1 } }, 1200).why, /보유·현금/);
  assert.match(chainPreStart({ ...pre, endCash: undefined }, real, { ...snap, cash: 0 }, 1200).why, /보유·현금/);   // 빈 값을 0으로 보지 않음
  assert.match(chainPreStart(pre, { ...real, started: '2026-10-21' }, snap, 1200).why, /시작 스냅샷/);
  assert.match(chainPreStart(pre, { started: null, twr: null }, snap, 1200).why, /출발 전/);
  assert.equal(chainPreStart(null, real, snap, 1200), null);
  assert.equal(chainPreStart(pre, { ...real, vs: null }, snap, 1200).vsSPY, null);
});

import { summarizeKnown } from '../../preview-only-portfolio-home.js';

test('마지막 날 평가가 비면 수익률을 아는 마지막 날 기준(summarizeKnown)', () => {
  const s = { started: '2026-10-20', days: [{ date: '2026-10-20', value: 100, twr: 0, vs: { SPY: 0 } }, { date: '2026-10-21', value: null, twr: null }], trades: [], skips: [], cash: 0 };
  const m = summarizeKnown(s);
  assert.deepEqual([m.twr, m.vs, m.asOf], [0, { SPY: 0 }, '2026-10-20']);
  const ok = { ...s, days: [s.days[0], { date: '2026-10-21', value: 110, twr: 0.1, vs: { SPY: 1 } }] };
  assert.equal(summarizeKnown(ok).twr, 0.1);
});

test('출금(2026-10-22): 그달 넣은 돈에서 빠지고(음수 흐름), 입출금 목록에 출금으로 보인다', () => {
  const all = {
    'b1:d1': { amount: 500, recordedAt: '2026-11-03T15:00:00Z' },
    'b1:w1': { amount: 200, kind: 'withdraw', recordedAt: '2026-11-05T15:00:00Z' },
  };
  const m = monthDeposits(all, '2026-11');
  assert.deepEqual(m.now.map((d) => d.amount), [500, -200]);
  const items = timelineItems({ trades: {}, cur: { skipped: [], future: [], clipped: [] }, bundle: { snapshot: {}, deposits: { d1: all['b1:d1'], w1: all['b1:w1'] } },
    bundleNo: 1, holdings: {}, now: Date.parse('2026-11-10T00:00:00Z'), etDate });
  const w = items.find((x) => x.id === 'w1');
  assert.match(w.title, /^출금 /);
  assert.match(w.amount, /^−/);
});

import { roundStrip, monthBuyList } from '../../preview-only-portfolio-home.js';

test('4회 띠: 지난 회차는 산 돈(없으면 놓침), 이번 회차·남은 회차는 계획, 첫 회차 전 매수는 회차 외', () => {
  const dates = ['2026-11-02', '2026-11-09', '2026-11-16', '2026-11-23'];
  const buys = [{ date: '2026-11-01', amount: 10 }, { date: '2026-11-03', amount: 100 }, { date: '2026-11-16', amount: 5 }];
  const r = roundStrip(dates, '2026-11-16', buys, 75);
  assert.deepEqual(r.rounds.map((x) => [x.state, x.amount]), [['done', 100], ['missed', 0], ['now', 75], ['plan', 75]]);
  assert.equal(r.rounds[2].done, 5);
  assert.equal(r.outside, 10);
  assert.deepEqual(roundStrip(dates, null, buys, null).rounds.map((x) => x.state), ['done', 'missed', 'done', 'missed']);   // 회차 끝
  const trades = { a: { date: '2026-11-03', side: 'buy', qty: 0.0014, price: 10 }, b: { date: '2026-11-04', side: 'sell', qty: 1, price: 5 }, c: { date: '2026-11-05', side: 'buy', qty: 1, price: 2 }, x: { cancels: 'c' } };
  assert.deepEqual(monthBuyList(trades, '2026-11', '2026-11-30'), [{ date: '2026-11-03', amount: 0.01 }]);
});

test('4회 띠: 한도를 주면 지난 회차는 그때 고정 몫과 다 못 쓴 돈(남은 돈)을 보인다', () => {
  const dates = ['2026-11-02', '2026-11-09', '2026-11-16', '2026-11-23'];
  const r = roundStrip(dates, '2026-11-16', [{ date: '2026-11-10', amount: 332.95 }], 333.5, 999.98).rounds;
  assert.equal(r[0].state, 'missed');
  assert.deepEqual([r[1].state, r[1].share, r[1].left], ['done', 333.32, 0.37]);
  const over = roundStrip(dates, '2026-11-16', [{ date: '2026-11-03', amount: 300 }], 0, 999.98).rounds[0];
  assert.deepEqual([over.share, over.left], [249.99, 0]);
  const big = roundStrip(dates, '2026-11-16', [{ date: '2026-11-03', amount: 400 }], 0, 999.98).rounds[0];
  assert.equal(big.left, 0);   // 몫보다 많이 사면 0
});

import { carryIn } from '../../preview-only-portfolio-home.js';

test('잔금(원칙 3): 4회가 끝나고 못 쓴 돈은 다음 달 한도에 더한다, 시작 달은 0, 음수는 0', () => {
  const net = { '2026-10': 0, '2026-11': 500, '2026-12': 400 }, sold = { '2026-11': 101 }, spent = { '2026-10': 76, '2026-11': 300, '2026-12': 650 };
  const f = { net: (m) => net[m] || 0, sold: (m) => sold[m] || 0, spent: (m) => spent[m] || 0 };
  assert.equal(carryIn('2026-10', '2026-10', f), 0);
  assert.equal(carryIn('2026-11', '2026-10', f), 0);                // 10월 한도 0인데 76 삼 → 넘어갈 돈 없음
  assert.equal(carryIn('2026-12', '2026-10', f), 200);              // 11월 500 − 300
  assert.equal(carryIn('2027-01', '2026-10', f), 51);               // 12월 400 + 11월 판 돈 101 + 잔금 200 = 701 − 650
  assert.equal(carryIn('2026-12', null, f), 0);
});

test('잔금: 시작 달은 회차가 없어 다음 달로 안 넘긴다, 출금이 잔금을 먹고 0 아래는 안 넘어간다', () => {
  const net = { '2026-10': 300, '2026-11': 500, '2026-12': 400, '2027-01': -300, '2027-02': -20 }, sold = { '2026-11': 101 }, spent = { '2026-11': 300, '2026-12': 650 };
  const f = { net: (m) => net[m] || 0, sold: (m) => sold[m] || 0, spent: (m) => spent[m] || 0 };
  assert.equal(carryIn('2026-11', '2026-10', f), 0);                // 10월(시작 달) 300은 원칙 5 현금
  assert.equal(carryIn('2027-02', '2026-10', f), 0);                // 1월: 51 − 300 → 한도 0
  assert.equal(carryIn('2027-03', '2026-10', f), 0);                // 빚은 안 넘어감 → 2월 한도 0
  const g = { ...f, net: (m) => (m === '2027-01' ? -20 : net[m] || 0) };
  assert.equal(carryIn('2027-02', '2026-10', g), 31);               // 51 − 20
});

test('미리 넣은 돈(forMonth): 다음 달 몫이면 그 달 한도, 앞당기기는 반영일 달, 출금(역환전)도 저장된 몫 달(2026-10-28 dr)', () => {
  const all = {
    'b1:d1': { amount: 500, forMonth: '2026-11', recordedAt: '2026-10-26T15:00:00Z' },   // 10-26 반영, 11월 몫
    'b1:d2': { amount: 50, forMonth: '2026-09', recordedAt: '2026-10-26T15:05:00Z' },    // 앞당기기 → 10월
    'b1:w1': { amount: 30, kind: 'withdraw', account: 'kw', forMonth: '2026-11', recordedAt: '2026-10-26T15:10:00Z' },   // 역환전 몫 11월 → 11월에서 뺀다
    'b1:w2': { amount: 7, kind: 'withdraw', forMonth: '2026-11', recordedAt: '2026-10-26T15:20:00Z' },   // Robinhood 출금은 몫 달을 쓰지 않음 → 10월
  };
  assert.deepEqual(monthDeposits(all, '2026-11').now.map((p) => p.amount).sort((a, b) => a - b), [-30, 500]);
  assert.deepEqual(monthDeposits(all, '2026-10').now.map((p) => p.amount).sort((a, b) => a - b), [-7, 50]);
  assert.deepEqual(monthDeposits(all, '2026-10').later.map((p) => p.amount).sort((a, b) => a - b), [-30, 500]);
});

test('입금 즉시 반영: 기준일까지 기록한 입금은 올린 현금에 든 것으로 보고, 반영 전 취소는 현금에서도 빠진다', () => {
  const all = {
    'b1:d1': { amount: 100, recordedAt: '2026-10-23T21:00:00Z' },   // 10-23 기록, 10-26 반영 — 기준일 10-23에 이미 포함
    'b1:d2': { amount: 200, recordedAt: '2026-10-24T15:00:00Z' },   // 10-24 기록(토)
    'b1:d3': { amount: 50, recordedAt: '2026-10-24T16:00:00Z' },
    'b1:c3': { cancels: 'b1:d3', recordedAt: '2026-10-25T16:00:00Z' },   // 반영(10-26) 전 취소
  };
  assert.deepEqual(depositsSince(all, '2026-10-23', '2026-10-25').map((p) => p.amount), [200]);
  assert.deepEqual(depositsSince(all, '2026-10-23', '2026-10-23').map((p) => p.amount), []);
});

test('미리 넣은 돈: 연 넘김(12월에 1월 몫), 없는 달·같은 달 몫은 무시', () => {
  const all = {
    'b1:d1': { amount: 300, forMonth: '2027-01', recordedAt: '2026-12-10T15:00:00Z' },
    'b1:d2': { amount: 40, forMonth: '2026-13', recordedAt: '2026-12-10T15:05:00Z' },
    'b1:d3': { amount: 60, forMonth: '2026-12', recordedAt: '2026-12-10T15:10:00Z' },
  };
  assert.deepEqual(monthDeposits(all, '2027-01').now.map((p) => p.amount), [300]);
  assert.deepEqual(monthDeposits(all, '2026-12').now.map((p) => [p.amount, !!p.forMonth]).sort(), [[40, false], [60, false]]);
});

import { byCap } from '../../preview-only-portfolio-home.js';
test('후보 줄 순서: 시총 큰 순, 시총 모르면 맨 뒤 티커순', () => {
  assert.deepEqual(byCap(['AAA', 'BBB', 'CCC', 'DDD'], { BBB: 5e11, DDD: 2e12, AAA: 1e9 }), ['DDD', 'BBB', 'AAA', 'CCC']);
});

import { historyPrefix, withPrefix } from '../../preview-only-portfolio-home.js';
import { _internal as _eng, openUtcMs as _open } from '../../preview-only-portfolio-engine.js';
test('10/01부터 공통 과거: Robinhood 기록 × 끝낸 비교의 실제 계좌(새 출발일까지), SPY도 같은 구간, 각 줄 앞에 곱함', () => {
  const cal = _eng.makeCalendar();
  const days = cal.sessions.filter((d) => d >= '2026-10-16' && d <= '2026-10-23');
  const px = { '2026-10-16': 100, '2026-10-19': 104, '2026-10-20': 106, '2026-10-21': 110, '2026-10-22': 111, '2026-10-23': 112 };
  const spy = { '2026-10-16': 500, '2026-10-19': 505, '2026-10-20': 507, '2026-10-21': 510, '2026-10-22': 511, '2026-10-23': 512 };
  const recs = days.map((d, i) => ({ session: d, generatedAt: new Date(_open(cal.sessions[cal.index(d) + 1]) + 90 * 60e3).toISOString(), ruleVersion: 'v2-verdict', pipelineFull: true,
    cards: { AAA: { tier: '적정', tierStatus: 'valid', close: px[d], verdictAsOf: d, priceStale: false } }, prices: { SPY: spy[d] }, splits: [], missing: [], prevSession: i ? days[i - 1] : null, prevPublishedAt: null }));
  const pre = { from: '2026-10-01', base: '2026-09-30', end: '2026-10-16', endHoldings: { AAA: 10 }, endCash: 0,
    days: [{ d: '2026-09-30', v: 900, f: 0 }, { d: '2026-10-16', v: 1000, f: 0 }], spy: { base: 480, end: 500 } };
  const past = [{ snapshot: { date: '2026-10-16', holdings: { AAA: 10 }, cash: 0 }, deposits: {} }];
  const h = historyPrefix(pre, past, { date: '2026-10-21' }, '2026-10-21', 1100, { records: recs, trades: {} });
  assert.ok(Math.abs(h.twr - ((1000 / 900) * 1.1 - 1)) < 1e-9, String(h.twr));
  assert.ok(Math.abs(h.spy - ((500 / 480) * (510 / 500) - 1)) < 1e-9);
  assert.equal(h.n, 1);
  const w = withPrefix(0.1, 5, h);   // 새 비교: 10%, SPY 5%
  assert.ok(Math.abs(w.twr - ((1 + h.twr) * 1.1 - 1)) < 1e-9);
  assert.ok(Math.abs(w.vsSPY - (w.twr - ((1 + h.spy) * 1.05 - 1)) * 100) < 1e-9);
  // 끝낸 비교가 없으면 Robinhood 기록만(지금 시작 스냅샷이 그 끝과 같아야)
  const h0 = historyPrefix(pre, [], { date: '2026-10-16', holdings: { AAA: 10 }, cash: 0 }, '2026-10-16', 1000, { records: recs, trades: {} });
  assert.ok(Math.abs(h0.twr - (1000 / 900 - 1)) < 1e-9);
  // 끝낸 비교의 그날 평가가 없으면 이유
  assert.match(historyPrefix(pre, past, { date: '2026-10-26' }, '2026-10-26', 1, { records: recs, trades: {} }).why, /평가가 없음/);
});

import { weeklySells, monthRounds } from '../../preview-only-portfolio-home.js';
test('매주 판정 매도(카드, 2026-10-28): 고평가는 남은 회차에 나눠, 초고평가는 전부, 같은 회차에 판 것은 빼고, 계좌 따로', () => {
  assert.deepEqual(monthRounds('2026-11'), ['2026-11-02', '2026-11-09', '2026-11-16', '2026-11-23']);
  const card = (tier, d = '2026-11-06') => ({ tier, tierStatus: 'valid', verdictAsOf: d, priceStale: false, close: 10 });
  const rec = { session: '2026-11-06', ruleVersion: 'r', cards: { DDD: card('고평가'), EEE: card('초고평가'), AAA: card('적정'), FFF: card('고평가') } };
  const recAt = (d) => ({ session: d, ruleVersion: 'r', cards: { DDD: card('고평가', d) } });   // 원칙 6에 안 걸리게 그날 기록
  const rounds = monthRounds('2026-11');
  const base = { rec, today: '2026-11-07', rounds, lastSession: '2026-11-06' };
  const r = weeklySells({ ...base, holdings: [{ ticker: 'DDD', qty: 9, account: 'rh' }, { ticker: 'DDD', qty: 2.5, account: 'kw' }, { ticker: 'EEE', qty: 4, account: 'rh' }, { ticker: 'AAA', qty: 5, account: 'rh' }], trades: {} });
  assert.deepEqual(r.map((x) => [x.ticker, x.account, x.shares, x.remaining, x.round]), [
    ['DDD', 'kw', 0.833334, 3, '2026-11-09'], ['DDD', 'rh', 3, 3, '2026-11-09'], ['EEE', 'rh', 4, 3, '2026-11-09']]);   // 적정(AAA)은 보유(고평가부터 판다)
  // 회차 당일 3주를 팔아 기록하면(기록은 아직 전날) 그 회차 몫은 0, 다음 회차는 남은 6주 ÷ 2회
  const sold = { t1: { date: '2026-11-09', ticker: 'DDD', side: 'sell', qty: 3, price: 10 } };
  const a = weeklySells({ ...base, today: '2026-11-09', holdings: [{ ticker: 'DDD', qty: 6, account: 'rh' }], trades: sold });
  assert.equal(a[0].shares, 0);
  // 10주 가운데 1주만 팔았으면 그 회차 몫은 ⌈10 ÷ 3⌉ − 1 = 3주 남음(지금 보유 9주로 다시 나누면 ⌈9/3⌉ − 1 = 2로 줄어든다)
  assert.equal(weeklySells({ ...base, today: '2026-11-09', holdings: [{ ticker: 'DDD', qty: 9, account: 'rh' }], trades: { t1: { ...sold.t1, qty: 1 } } })[0].shares, 3);
  const b = weeklySells({ ...base, today: '2026-11-10', lastSession: '2026-11-09', rec: recAt('2026-11-09'), holdings: [{ ticker: 'DDD', qty: 6, account: 'rh' }], trades: sold });
  assert.deepEqual([b[0].shares, b[0].remaining, b[0].round], [3, 2, '2026-11-16']);
  // 놓친 회차: 11/09에 안 팔았으면 11/16 회차는 9주 ÷ 2회 = 5주(정수 올림), 마지막 회차는 전부
  assert.equal(weeklySells({ ...base, today: '2026-11-10', lastSession: '2026-11-09', rec: recAt('2026-11-09'), holdings: [{ ticker: 'DDD', qty: 9, account: 'rh' }], trades: {} })[0].shares, 5);
  // 적은 보유: 1주 ÷ 4회 → 첫 회차에 1주(0주로 '이미 팔았음'처럼 보이지 않게, dr r1)
  assert.equal(weeklySells({ ...base, today: '2026-11-01', lastSession: '2026-10-30', holdings: [{ ticker: 'DDD', qty: 1, account: 'rh' }], trades: {} })[0].shares, 1);
  // 소수와 정수가 섞여도 마지막 회차는 지금 보유 전부(9.5주), 그대로 두는 보유는 빠진다(dr r1)
  assert.equal(weeklySells({ ...base, today: '2026-11-23', lastSession: '2026-11-20', rec: recAt('2026-11-20'), holdings: [{ ticker: 'DDD', qty: 9.5, account: 'rh' }], trades: { t9: { date: '2026-11-23', ticker: 'DDD', side: 'sell', qty: 0.5, price: 10 } } })[0].shares, 9.5);
  assert.deepEqual(weeklySells({ ...base, holdOnly: ['DDD'], holdings: [{ ticker: 'DDD', qty: 9, account: 'rh' }], trades: {} }), []);
  assert.equal(weeklySells({ ...base, today: '2026-11-20', lastSession: '2026-11-19', rec: recAt('2026-11-19'), holdings: [{ ticker: 'DDD', qty: 5, account: 'rh' }], trades: {} })[0].shares, 5);
  // 회차가 끝난 뒤(11/23 뒤)는 수량 없이 '다음 점검일'
  const end = weeklySells({ ...base, today: '2026-11-27', lastSession: '2026-11-25', rec: recAt('2026-11-25'), holdings: [{ ticker: 'DDD', qty: 5, account: 'rh' }], trades: {} });
  assert.deepEqual([end[0].shares, end[0].round], [null, null]);
  // 고평가~적정은 팔지 않는다(2026-11-03 되돌림)
  assert.deepEqual(weeklySells({ ...base, rec: { ...rec, cards: { DDD: card('고평가~적정') } }, holdings: [{ ticker: 'DDD', qty: 9, account: 'rh' }], trades: {} }), []);
  // 원칙 6(묵은 판정)이면 빠진다
  assert.deepEqual(weeklySells({ ...base, rec: { ...rec, cards: { DDD: { ...card('고평가'), priceStale: true } } }, holdings: [{ ticker: 'DDD', qty: 9, account: 'rh' }], trades: {} }), []);
});

import { staleHoldings, sellRounds } from '../../preview-only-portfolio-home.js';
test('알림 칸(2026-10-29): 10월에도 다음 달 첫 회차부터 팔 양, 판정이 묵은 보유는 확인 필요(카드 없는 종목·그대로 두는 보유 제외)', () => {
  assert.deepEqual(sellRounds('2026-10', '2026-10-28'), ['2026-11-02', '2026-11-09', '2026-11-16', '2026-11-23']);   // 10월 회차는 다 지남
  assert.deepEqual(sellRounds('2026-11', '2026-11-06'), ['2026-11-02', '2026-11-09', '2026-11-16', '2026-11-23']);
  assert.equal(sellRounds('2026-11', '2026-11-25')[0], '2026-12-01');                                                // 11월 회차가 끝난 주는 12월
  const card = (o) => ({ tier: '적정', tierStatus: 'valid', verdictAsOf: '2026-10-27', priceStale: false, close: 10, ...o });
  const rec = { session: '2026-10-28', ruleVersion: 'r', cards: { AAA: card({ priceStale: true }), BBB: card({ tier: null }), CCC: card({}), OLD: card({ verdictAsOf: '2026-10-01' }) } };
  const hold = [['AAA', 'rh'], ['BBB', 'kw'], ['CCC', 'rh'], ['OLD', 'rh'], ['ZZZ', 'rh']].map(([ticker, account]) => ({ ticker, account, qty: 3 }));
  assert.deepEqual(staleHoldings({ holdings: hold, rec, today: '2026-10-29' }).map((x) => [x.ticker, x.account, x.why]),
    [['AAA', 'rh', 'stale'], ['BBB', 'kw', 'noVerdict'], ['OLD', 'rh', 'stale']]);   // 카드 없는 ZZZ·정상 CCC는 빠짐
  assert.deepEqual(staleHoldings({ holdings: hold, rec, today: '2026-10-29', holdOnly: ['AAA', 'BBB', 'OLD'] }), []);
  // 기록 자체가 묵었으면 줄마다 띄우지 않는다(칸 위 경고 한 줄)
  assert.deepEqual(staleHoldings({ holdings: hold, rec, today: '2026-11-20' }), []);
});

import { ledgerMonth } from '../../preview-only-portfolio-home.js';
test('환전 몫 달(2026-11-03): 반영일 달에 남은 회차가 있으면 그 달, 없으면 다음 달 — 계획이 없는 달도 원칙 2 회차로', () => {
  assert.equal(ledgerMonth('2026-10-29', null, null), '2026-11');   // 10월 회차(10/01~10/22)가 다 지남 → 11월 몫(예전엔 10월)
  assert.equal(ledgerMonth('2026-11-02', '2026-10', []), '2026-11');  // 월말 주말 기록 → 11/02 반영, 11월 첫 회차 당일 → 11월
  assert.equal(ledgerMonth('2026-11-03', '2026-10', []), '2026-11');  // 11월 결정이 밀려도 11월 회차가 남았으면 11월
  const rounds = ['2026-11-02', '2026-11-09', '2026-11-16', '2026-11-23'].map((date) => ({ date, dropped: false }));
  assert.equal(ledgerMonth('2026-11-20', '2026-11', rounds), '2026-11');
  assert.equal(ledgerMonth('2026-11-24', '2026-11', rounds), '2026-12');   // 4회 끝난 뒤 → 다음 달
  // 다음 점검일 뒤로 밀린 회차(dropped)는 남은 회차로 치지 않는다(dr): 남은 것이 모두 밀렸으면 다음 달, 하나라도 남으면 그 달, 회차 당일은 포함
  const dr = rounds.map((r, i) => ({ ...r, dropped: i >= 2 }));
  assert.equal(ledgerMonth('2026-11-10', '2026-11', dr), '2026-12');
  assert.equal(ledgerMonth('2026-11-09', '2026-11', dr), '2026-11');
  assert.equal(ledgerMonth('2026-11-09', '2026-11', []), '2026-12');            // 계획은 있는데 회차가 없으면 다음 달
  assert.equal(ledgerMonth('2026-11-20', '2026-12', null), '2026-11');          // 계획 달이 반영일보다 뒤면 반영일 달의 원칙 2 회차로
  assert.equal(ledgerMonth('2026-11-24', '2026-12', null), '2026-12');
  assert.equal(ledgerMonth('2026-11-24', '2026-10', []), '2026-11');           // 11월 결정이 4회차 날짜 뒤로 밀려도 결정 대기 달이면 11월(입금 칸과 같게)
  assert.equal(ledgerMonth('2027-12-29', null, null), '2028-01');              // 달력 끝에서도 다음 달
});

import { cashLeft } from '../../preview-only-portfolio-home.js';
test('현금 10% 목표(카드, 2026-11-03): 남은 한도 = 현금 − 총자산 10% − 이번 달 판 돈 − 다음 달 몫, 모자라면 0', () => {
  assert.deepEqual(cashLeft({ cash: 3000, total: 11000 }), { target: 1100, left: 1900, short: 0, unknown: false });
  assert.deepEqual(cashLeft({ cash: 3000, total: 11000, soldNow: 500, laterIn: 400 }), { target: 1100, left: 1000, short: 0, unknown: false });
  assert.equal(cashLeft({ cash: 3000, total: 11000, laterOut: 300 }).left, 1600);                    // 출금 예정은 미리 뺀다
  assert.deepEqual(cashLeft({ cash: 1014.1, total: 11755.37 }), { target: 1175.54, left: 0, short: 161.44, unknown: false });   // 새 돈이 먼저 현금을 채운다
  // 가격 없는 보유가 있거나 현금·총자산을 모르면 한도를 막는다(예전 식으로 돌아가지 않음)
  assert.deepEqual(cashLeft({ cash: 3000, total: 11000, missing: 1 }), { target: null, left: 0, short: 0, unknown: true });
  assert.equal(cashLeft({ cash: null, total: 11000 }).unknown, true);
  assert.equal(cashLeft({ cash: NaN, total: 11000 }).unknown, true);
  assert.equal(cashLeft({ cash: 3000, total: Infinity }).unknown, true);
  assert.equal(cashLeft({ cash: 3000, total: 11000, laterOut: -300 }).left, 1600);   // 음수로 넘겨도 한도를 줄인다
});

// 매도 탭의 이번 달 판 기록(2026-11-03): 취소·다른 달·미래·매수는 빼고, 받은 돈은 수수료를 뺀 센트 셈, 계좌는 acctOf
import { monthSellList } from '../../preview-only-portfolio-home.js';
test('monthSellList: 이번 달 취소 안 된 매도만, 수수료 뺀 받은 돈', () => {
  const trades = {
    a: { date: '2026-11-09', ticker: 'BBB', side: 'sell', qty: 2, price: 10.005 },
    b: { date: '2026-11-09', ticker: 'AAA', side: 'sell', qty: 1, price: 50, account: 'kw', fee: 0.5 },
    c: { date: '2026-11-10', ticker: 'CCC', side: 'sell', qty: 1, price: 5 },
    d: { cancels: 'c' },
    e: { date: '2026-10-30', ticker: 'DDD', side: 'sell', qty: 1, price: 5 },
    f: { date: '2026-11-12', ticker: 'EEE', side: 'sell', qty: 1, price: 5 },
    g: { date: '2026-11-09', ticker: 'FFF', side: 'buy', qty: 1, price: 5 },
  };
  assert.deepEqual(monthSellList(trades, '2026-11', '2026-11-11'), [
    { date: '2026-11-09', ticker: 'AAA', account: 'kw', qty: 1, amount: 49.5 },
    { date: '2026-11-09', ticker: 'BBB', account: 'rh', qty: 2, amount: 20.01 },
  ]);
  assert.deepEqual(monthSellList(undefined, '2026-11', '2026-11-11'), []);
});

// 최소 주문 $10(사용자 결정 2026-11-18, 키움, dr 3라운드 합의) — 가짜 티커만
import { MIN_ORDER, roundTotals, skipTxt } from '../../preview-only-portfolio-home.js';
const M = { minOrder: MIN_ORDER };
// 한 종목을 회차마다 보인 금액대로 산다고 보고 4회를 돈다(새 회차마다 boughtNow 비움)
const walk = (budget, method = 'equal') => {
  let spent = 0; const out = [];
  for (let k = 0; k < 4; k++) {
    const p = buyPlan({ cands: ['AAA'], picked: ['AAA'], budget, spent, bought: { AAA: spent }, rounds: 4, roundsLeft: 4 - k, caps: { AAA: 1e12 }, tiers: { AAA: '저평가' }, ...M });
    out.push({ todo: p.todo[method].AAA, skip: p.skip[method].AAA || null, sched: p.sched[method].AAA });
    spent = Math.round((spent + p.todo[method].AAA) * 100) / 100;
  }
  return out;
};

test('최소 주문: 달 몫 $25는 1·2회 다음 회차로, 3·4회 $12.50', () => {
  const w = walk(25);
  assert.equal(MIN_ORDER, 10);
  assert.deepEqual(w.map((x) => x.skip), [{ kind: 'next', amt: 6.25 }, { kind: 'next', amt: 8.33 }, null, null]);
  assert.deepEqual(w.map((x) => x.todo), [0, 0, 12.5, 12.5]);
  assert.deepEqual(w[0].sched, [0, 0, 12.5, 12.5]);
  for (const m of ['cap', 'tier']) assert.deepEqual(walk(25, m).map((x) => x.todo), [0, 0, 12.5, 12.5], m);   // 세 방법 모두 같은 규칙
});

test('최소 주문: 달 몫 $8은 네 회 모두 다음 달로(금액 = 남은 몫)', () => {
  const w = walk(8);
  assert.deepEqual(w.map((x) => x.skip), Array(4).fill({ kind: 'month', amt: 8 }));
  assert.deepEqual(w.map((x) => x.todo), [0, 0, 0, 0]);
  assert.deepEqual(w[0].sched, [0, 0, 0, 0]);
});

test('최소 주문 경계: todo 1000센트는 사고 999센트는 건너뜀', () => {
  assert.deepEqual(walk(40).map((x) => x.todo), [10, 10, 10, 10]);
  const p = buyPlan({ cands: ['AAA'], picked: ['AAA'], budget: 39.96, rounds: 4, ...M });
  assert.equal(p.todo.equal.AAA, 0); assert.deepEqual(p.skip.equal.AAA, { kind: 'next', amt: 9.99 });
});

test('최소 주문: 이번 회차에 이미 산 종목은 남은 돈이 작아도 건너뜀으로 안 잡는다', () => {
  // 회차 몫 $30 중 $25 삼 → todo $5, skip 없음 / 0.0001주 내림으로 몇 센트 남음 → skip 없음
  const a = buyPlan({ cands: ['AAA'], picked: ['AAA'], budget: 120, spent: 25, bought: { AAA: 25 }, boughtNow: { AAA: 25 }, rounds: 4, ...M });
  assert.equal(a.todo.equal.AAA, 5); assert.deepEqual(a.skip.equal, {});
  assert.deepEqual(a.sched.equal.AAA, [30, 31.66, 31.67, 31.67]);   // 남은 $5는 뒤 회차로(rem = rest 95)
  const b = buyPlan({ cands: ['AAA'], picked: ['AAA'], budget: 120, spent: 29.97, bought: { AAA: 29.97 }, boughtNow: { AAA: 29.97 }, rounds: 4, ...M });
  assert.equal(b.todo.equal.AAA, 0.03); assert.deepEqual(b.skip.equal, {});
});

test('최소 주문: 회차 계획(sched)은 이번 회차를 두 번 세지 않는다', () => {
  const now = buyPlan({ cands: ['AAA'], picked: ['AAA'], budget: 100, spent: 25, bought: { AAA: 25 }, boughtNow: { AAA: 25 }, rounds: 4, ...M });
  assert.deepEqual(now.sched.equal.AAA, [25, 25, 25, 25]);
  const r2 = buyPlan({ cands: ['AAA'], picked: ['AAA'], budget: 100, spent: 25, bought: { AAA: 25 }, rounds: 4, roundsLeft: 3, ...M });
  assert.deepEqual(r2.sched.equal.AAA, [25, 25, 25]);
});

test('최소 주문: 이번 주 합(roundTotals)은 고른 종목만, 건너뛴 종목은 0, 이미 산 종목은 회차 몫 그대로', () => {
  // AAA 달 몫 $100(이번 회차 $25 다 삼), BBB 달 몫 $25(1회 건너뜀), CCC는 지금 못 사는 종목이라 ok에서 빠짐
  const p = buyPlan({ cands: ['AAA', 'BBB', 'CCC'], picked: ['AAA', 'BBB', 'CCC'], budget: 150, spent: 25, bought: { AAA: 25 }, boughtNow: { AAA: 25 }, rounds: 4,
    caps: { AAA: 4, BBB: 1, CCC: 1 }, ...M });
  assert.deepEqual(p.by.cap, { AAA: 100, BBB: 25, CCC: 25 });
  assert.deepEqual(p.todo.cap, { AAA: 0, BBB: 0, CCC: 0 });
  assert.deepEqual(roundTotals(p.sched.cap, ['AAA', 'BBB']), [25, 25, 37.5, 37.5]);   // 이번 주 $25(산 것 포함), 예정 칸은 회차별
  assert.deepEqual(roundTotals(p.sched.cap, ['AAA', 'BBB', 'CCC']), [25, 25, 50, 50]);
  assert.equal(roundTotals(null, ['AAA']), null);
});

test('최소 주문: 비례 축소·밀린 회차·회차 끝·무게 없음·다 샀음', () => {
  // 남은 돈 $8에 맞춰 줄어 각 $4 → 다음 달로
  const c = buyPlan({ cands: ['AAA', 'BBB'], picked: ['AAA', 'BBB'], budget: 80, spent: 72, rounds: 4, ...M });
  assert.ok(c.capped.equal); assert.deepEqual(c.skip.equal, { AAA: { kind: 'month', amt: 4 }, BBB: { kind: 'month', amt: 4 } });
  const r3 = buyPlan({ cands: ['AAA'], picked: ['AAA'], budget: 8, rounds: 3, roundsLeft: 1, ...M });
  assert.deepEqual(r3.skip.equal.AAA, { kind: 'month', amt: 8 }); assert.deepEqual(r3.sched.equal.AAA, [0]);
  const end = buyPlan({ cands: ['AAA'], picked: ['AAA'], budget: 8, rounds: 4, roundsLeft: 0, ...M });
  assert.equal(end.skip.equal, null); assert.equal(end.sched.equal, null);
  const nw = buyPlan({ cands: ['AAA'], picked: ['AAA'], budget: 8, rounds: 4, tiers: { AAA: '적정' }, ...M });
  assert.equal(nw.skip.tier, null); assert.equal(nw.sched.tier, null);
  const all = buyPlan({ cands: ['AAA'], picked: ['AAA'], budget: 40, spent: 40, bought: { AAA: 40 }, rounds: 4, roundsLeft: 2, ...M });
  assert.equal(all.todo.equal.AAA, 0); assert.deepEqual(all.skip.equal, {});
});

test('최소 주문 기본값 0이면 예전과 같다', () => {
  const p = buyPlan({ cands: ['AAA'], picked: ['AAA'], budget: 25, rounds: 4 });
  assert.equal(p.todo.equal.AAA, 6.25); assert.deepEqual(p.skip.equal, {});
  assert.deepEqual(p.sched.equal.AAA, [6.25, 6.25, 6.25, 6.25]);
  assert.equal(skipTxt({ kind: 'next', amt: 6.25 }), '$6.25 · $10 미만, 다음 회차로');
  assert.equal(skipTxt({ kind: 'month', amt: 8 }), '$8.00 · $10 미만, 다음 달로');
});

// 보유 비중 줄(2026-11-19 시안): 종목 | 업종 전환 — 가짜 티커만
import { mixRows } from '../../preview-only-portfolio-home.js';
test('보유 비중 줄: 종목 보기는 받은 조각 그대로, 업종 보기는 분류 안 됨 → 업종 → ETF·현금 순, 두 보기 합은 같다', () => {
  const parts = [{ name: 'ZZ1', value: 600, color: 'c1' }, { name: 'SPY', value: 300, color: 'c2' }, { name: '현금', value: 100, color: 'c3' }];
  const items = [{ ticker: 'ZZ1', value: 600 }, { ticker: 'SPY', value: 300 }];
  const tk = mixRows('ticker', parts, items, 100, 1000);
  assert.deepEqual(tk.map((r) => [r.name, r.pct, r.color]), [['ZZ1', '60%', 'c1'], ['SPY', '30%', 'c2'], ['현금', '10%', 'c3']]);
  const sc = mixRows('sector', parts, items, 100, 1000);
  assert.deepEqual(sc.map((r) => [r.name, r.pct, r.cls]), [['분류 안 됨', '60%', 'pf-mxwarn'], ['지수 ETF · 속 안 셈', '30%', 'pf-mxrest pf-mxsep'], ['현금', '10%', 'pf-mxrest']]);
  assert.equal(sc[0].sub, 'ZZ1 60%');
  const sum = (rows) => Math.round(rows.filter((r) => !r.cls.includes('pf-mxsub')).reduce((a, r) => a + r.share, 0) * 1e9) / 1e9;
  assert.equal(sum(tk), 1); assert.equal(sum(sc), 1);
  assert.deepEqual(mixRows('ticker', [{ name: 'ZZ1', value: 5, color: 'c' }], [], 0, 0).map((r) => r.pct), ['—']);   // 총액 0
  // 기술은 하위 줄이 따라온다(하위 합 = 상위)
  const tech = mixRows('sector', [], [{ ticker: 'NVDA', value: 70 }, { ticker: 'MSFT', value: 30 }], 0, 100);
  assert.deepEqual(tech.map((r) => [r.name, r.pct, r.cls]), [['기술', '100%', ''], ['반도체', '70%', 'pf-mxsub'], ['소프트웨어·서비스', '30%', 'pf-mxsub']]);
});

// 업종 먼저 나누기(사용자 결정 2026-11-19, dr v8 합의) — 가짜 티커만, 묶음은 시험이 직접 넘긴다
const SEMI = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6'], NET = ['I1', 'I2', 'I3'], SOLO = ['A', 'B', 'C', 'D', 'E'];
const ALL14 = [...SEMI, ...NET, ...SOLO];
const g14 = (t) => (SEMI.includes(t) ? 'semi' : NET.includes(t) ? 'net' : 'solo:' + t);
const BOUGHT5 = { S1: 61.1, S2: 61.1, A: 61.1, B: 61.1, C: 61.1 };
const exA = (extra) => buyPlan({ cands: ALL14, picked: ALL14, order: ALL14, groupOf: g14, budget: 1000, spent: 305.5, bought: BOUGHT5, rounds: 4, roundsLeft: 2, minOrder: 10, ...extra });
const pickT = (o, ts) => ts.map((t) => o[t]);

test('업종 먼저: groupOf가 없으면 예전과 같고 groups는 null', () => {
  const a = buyPlan({ cands: ['AAA', 'BBB'], picked: ['AAA', 'BBB'], budget: 300, spent: 50, bought: { AAA: 50 }, rounds: 4, roundsLeft: 3, minOrder: 10 });
  assert.deepEqual(a.by.equal, { AAA: 150, BBB: 150 }); assert.equal(a.groups.equal, null);
  assert.deepEqual(a.why.equal, { AAA: null, BBB: null });
});

test('업종 먼저: 묶음마다 똑같이 → 묶음 안은 방법의 무게로, 체크가 바뀌면 묶음 수도 바뀐다', () => {
  const g = (t) => ({ X1: 'x', X2: 'x', X3: 'x', Y1: 'y', Y2: 'y', Z1: 'z' })[t];
  const c = ['X1', 'X2', 'X3', 'Y1', 'Y2', 'Z1'];
  const p = buyPlan({ cands: c, picked: c, groupOf: g, budget: 600, rounds: 4, caps: { X1: 3, X2: 1, X3: 1, Y1: 1, Y2: 3, Z1: 9 } });
  assert.deepEqual(p.by.equal, { X1: 66.66, X2: 66.66, X3: 66.66, Y1: 100, Y2: 100, Z1: 200 });
  assert.deepEqual(p.by.cap, { X1: 120, X2: 40, X3: 40, Y1: 50, Y2: 150, Z1: 200 });   // 묶음 사이 똑같이, 안은 시총 비례
  assert.deepEqual(p.groups.equal.map((x) => [x.key, x.tickers.join(''), x.cap, x.bought, x.left]), [['x', 'X1X2X3', 200, 0, 200], ['y', 'Y1Y2', 200, 0, 200], ['z', 'Z1', 200, 0, 200]]);
  assert.equal(p.by.tier, null); assert.equal(p.groups.tier, null);   // 판정 무게가 없으면 그 방법은 null
  const q = buyPlan({ cands: c, picked: ['X1', 'X2', 'X3', 'Y1', 'Y2'], groupOf: g, budget: 600, rounds: 4 });   // 마지막 묶음의 체크를 빼면 G 3 → 2
  assert.deepEqual(q.by.equal, { X1: 100, X2: 100, X3: 100, Y1: 150, Y2: 150 });
  // solo: 키가 다르면 다른 묶음, 같으면 한 묶음
  const s1 = buyPlan({ cands: ['P', 'Q'], picked: ['P', 'Q'], groupOf: (t) => 'solo:' + t, budget: 100, rounds: 1 });
  const s2 = buyPlan({ cands: ['P', 'Q'], picked: ['P', 'Q'], groupOf: () => 'solo:X', budget: 100, rounds: 1 });
  assert.deepEqual(s1.groups.equal.map((x) => x.cap), [50, 50]); assert.deepEqual(s2.groups.equal.map((x) => x.cap), [100]);
});

test('업종 먼저 예 A: 업종 한도가 걸리면 순위 높은 쪽부터 각자 $10 이상이 되게 고르게', () => {
  const a = exA({ boughtNow: {} });   // (가) 지난 회차에 산 경우
  assert.deepEqual(pickT(a.by.equal, ['S1', 'I1', 'A']), [23.8, 47.61, 142.85]);
  assert.deepEqual(pickT(a.rest.equal, ['S1', 'S2', 'S3', 'S4', 'S5', 'S6']), [0, 0, 10.32, 10.32, 0, 0]);
  assert.deepEqual(pickT(a.round.equal, ['S3', 'S4', 'S5', 'I1', 'A', 'D']), [5.16, 5.16, 0, 23.8, 40.87, 71.42]);
  assert.deepEqual(pickT(a.todo.equal, ['S3', 'S4', 'S5', 'I1', 'A', 'D']), [0, 0, 0, 23.8, 40.87, 71.42]);
  assert.deepEqual(a.skip.equal, { S3: { kind: 'next', amt: 5.16 }, S4: { kind: 'next', amt: 5.16 } });
  assert.deepEqual(pickT(a.why.equal, ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'I1', 'A', 'D']), ['done', 'done', 'group', 'group', 'group', 'group', null, null, null]);
  assert.equal(a.capped.equal, false);
  assert.deepEqual(a.groups.equal.slice(0, 2).map((x) => [x.key, x.cap, x.bought, x.left]), [['semi', 142.85, 122.2, 20.65], ['net', 142.85, 0, 142.85]]);
  // (다) 다음 회차(마지막): 둘 다 사고, S3를 산 뒤에도 S4는 그대로
  const c1 = exA({ boughtNow: {}, roundsLeft: 1 });
  assert.deepEqual(pickT(c1.todo.equal, ['S3', 'S4', 'S5']), [10.32, 10.32, 0]);
  const c2 = exA({ roundsLeft: 1, spent: 315.82, bought: { ...BOUGHT5, S3: 10.32 }, boughtNow: { S3: 10.32 } });
  assert.deepEqual(pickT(c2.rest.equal, ['S3', 'S4', 'S5']), [0, 10.32, 0]);
  assert.deepEqual(pickT(c2.todo.equal, ['S3', 'S4', 'S5']), [0, 10.32, 0]);
});

test('업종 먼저 예 A (나): 이번 회차에 넘겨 산 경우는 뒤 순위부터 깎고, 그 뒤 사도 다른 종목은 그대로', () => {
  const b = exA({ boughtNow: BOUGHT5 });
  assert.deepEqual(pickT(b.round.equal, ['S1', 'S3', 'S4', 'S5', 'S6', 'A']), [11.9, 11.9, 11.9, 11.9, 11.9, 71.42]);   // 회차 시작 값(고정)
  assert.deepEqual(pickT(b.rest.equal, ['S1', 'S3', 'S4', 'S5', 'S6']), [0, 20.65, 0, 0, 0]);
  assert.deepEqual(pickT(b.todo.equal, ['S3', 'S4', 'A']), [11.9, 0, 10.32]);
  assert.deepEqual(pickT(b.why.equal, ['S1', 'S3', 'S4', 'S6']), ['done', 'group', 'group', 'group']);
  const b2 = exA({ spent: 317.4, bought: { ...BOUGHT5, S3: 11.9 }, boughtNow: { ...BOUGHT5, S3: 11.9 } });
  assert.deepEqual(pickT(b2.rest.equal, ['S3', 'S4', 'S5', 'S6']), [8.75, 0, 0, 0]);
});

test('업종 먼저 예 B: 체크 안 한 같은 업종 매수도 한도에, 다른 묶음 매수는 제외, 업종 한도 → 전체 한도 순서', () => {
  const g = (t) => ({ A: 'g1', B: 'g1', U: 'g1', C: 'g2', X: 'g3' })[t];
  const base = { cands: ['A', 'B', 'C', 'U'], picked: ['A', 'B', 'C'], groupOf: g, budget: 100, spent: 70, bought: { A: 30, U: 10, X: 30 }, rounds: 1 };
  const p = buyPlan({ ...base, boughtNow: {} });
  assert.deepEqual(p.by.equal, { A: 25, B: 25, C: 50 });
  assert.deepEqual(p.groups.equal.map((x) => [x.key, x.bought, x.left]), [['g1', 40, 10], ['g2', 0, 50]]);
  assert.deepEqual(p.rest.equal, { A: 0, B: 5, C: 25 });   // 순서를 뒤집으면 B 10, C 20
  assert.deepEqual(p.why.equal, { A: 'done', B: 'group', C: 'left' });
  const v = buyPlan({ ...base, boughtNow: { U: 10 } });   // 이번 회차의 체크 안 한 매수를 되돌린 회차 시작 값
  assert.deepEqual(v.round.equal, { A: 0, B: 11.42, C: 28.57 });   // 안 되돌리면 6.66 / 33.33
  assert.deepEqual(v.todo.equal, { A: 0, B: 5, C: 25 });  // 제 달 몫을 다 산 종목은 업종 한도에 걸려도 'done'이 먼저: 이번 회차에 A를 제 몫 25만큼 삼, 체크 안 한 U는 지난 회차에 40
  const d = buyPlan({ cands: ['A', 'B', 'C', 'U'], picked: ['A', 'B', 'C'], groupOf: g, budget: 100, spent: 65, bought: { A: 25, U: 40 }, boughtNow: { A: 25 }, rounds: 1 });
  assert.deepEqual(d.round.equal, { A: 5, B: 5, C: 50 });   // 회차 시작 한도 10을 A·B가 나눔(합 60 = 회차 시작 때 남은 돈)
  assert.deepEqual(d.why.equal, { A: 'done', B: 'group', C: 'left' });
});

test('업종 먼저 예 C·D: 순위 순, 값을 키우지 않음, 작은 값이 업종을 막지 않음, 남은 한도는 다음 순위에', () => {
  const g = (t) => (t === 'Z' ? 'h' : 'g');
  const c = { cands: ['C1', 'C2', 'C3', 'Z', 'U'], picked: ['C1', 'C2', 'C3', 'Z'], groupOf: g, budget: 120, spent: 35, bought: { U: 35 }, rounds: 1 };
  assert.deepEqual(buyPlan({ ...c, order: ['C1', 'C2', 'C3', 'Z'], minOrder: 10 }).rest.equal, { C1: 12.5, C2: 12.5, C3: 0, Z: 60 });
  assert.deepEqual(buyPlan({ ...c, order: ['C3', 'C2', 'C1', 'Z'], minOrder: 10 }).rest.equal, { C1: 0, C2: 12.5, C3: 12.5, Z: 60 });
  assert.deepEqual(buyPlan({ ...c, order: ['C3', 'C3', 'Z'], minOrder: 10 }).rest.equal, { C1: 12.5, C2: 0, C3: 12.5, Z: 60 });   // order에 없는 종목은 맨 뒤, 중복은 처음 것만
  assert.deepEqual(buyPlan({ ...c, minOrder: 0 }).rest.equal, { C1: 8.33, C2: 8.33, C3: 8.33, Z: 60 });   // 최소 주문이 없으면 단순 비례
  assert.deepEqual(buyPlan({ ...c, spent: 55, bought: { U: 55 }, minOrder: 10 }).rest.equal, { C1: 0, C2: 0, C3: 0, Z: 60 });   // 한도 $5
  // D1: 값 12·12·12, 한도 25.01 → 12·12·0 (비례 식이면 12.50으로 커진다)
  const d1 = buyPlan({ cands: ['P', 'Q', 'R', 'Z', 'U'], picked: ['P', 'Q', 'R', 'Z'], groupOf: g, budget: 200, spent: 74.99, bought: { P: 21.33, Q: 21.33, R: 21.33, U: 11 }, rounds: 1, minOrder: 10 });
  assert.deepEqual(d1.rest.equal, { P: 12, Q: 12, R: 0, Z: 100 });
  assert.deepEqual(d1.why.equal, { P: null, Q: null, R: 'group', Z: null });
  // D2: 1위 값 3, 2위 값 40, 한도 20 → 0 / 20
  const d2 = buyPlan({ cands: ['P', 'Q', 'Z', 'U'], picked: ['P', 'Q', 'Z'], groupOf: g, caps: { P: 43, Q: 57, Z: 1 }, budget: 200, spent: 80, bought: { P: 40, Q: 17, U: 23 }, rounds: 1, minOrder: 10 });
  assert.deepEqual(d2.by.cap, { P: 43, Q: 57, Z: 100 });
  assert.deepEqual(d2.rest.cap, { P: 0, Q: 20, Z: 100 }); assert.equal(d2.capped.cap, false);
  // D3: 값 12·12·30, 한도 40 → 12·12·16
  const d3 = buyPlan({ cands: ['P', 'Q', 'R', 'Z', 'U'], picked: ['P', 'Q', 'R', 'Z'], groupOf: g, caps: { P: 12, Q: 12, R: 30, Z: 1 }, budget: 108, spent: 14, bought: { U: 14 }, rounds: 1, minOrder: 10 });
  assert.deepEqual(d3.rest.cap, { P: 12, Q: 12, R: 16, Z: 54 });
  assert.deepEqual(d3.why.cap, { P: null, Q: null, R: 'group', Z: null });
});

test('업종 먼저 예 E: 회차 안에서 사도 다음 종목 몫은 그대로(무게가 달라도, 체크 안 한 매수 뒤에도)', () => {
  const g = (t) => (t === 'Z' ? 'h' : 'g');
  const e = { cands: ['P', 'Q', 'R', 'Z', 'U'], picked: ['P', 'Q', 'R', 'Z'], groupOf: g, caps: { P: 1, Q: 5, R: 5, Z: 1 }, budget: 440, rounds: 1, minOrder: 10 };
  const sub = (o) => pickT(o, ['P', 'Q', 'R']);
  const e1 = buyPlan({ ...e, spent: 150, bought: { U: 150 }, boughtNow: {} });
  assert.deepEqual(sub(e1.by.cap), [20, 100, 100]); assert.deepEqual(sub(e1.todo.cap), [11.66, 58.33, 0]);
  const e2 = buyPlan({ ...e, spent: 161.66, bought: { U: 150, P: 11.66 }, boughtNow: { P: 11.66 } });
  assert.deepEqual(sub(e2.todo.cap), [0, 58.33, 0]);   // 다시 고르면 Q 29.17, R 29.17이 된다
  const e3 = buyPlan({ ...e, spent: 180, bought: { U: 180 }, boughtNow: { U: 30 } });   // 체크 안 한 같은 업종을 이번 회차에 삼
  assert.deepEqual(sub(e3.round.cap), [11.66, 58.33, 0]); assert.deepEqual(sub(e3.rest.cap), [20, 20, 0]); assert.deepEqual(sub(e3.todo.cap), [11.66, 20, 0]);
  const e4a = buyPlan({ ...e, spent: 150, bought: { U: 150 }, boughtNow: { U: 150 } });   // 이번 회차에 U를 먼저 삼
  assert.deepEqual(sub(e4a.round.cap), [20, 100, 100]); assert.deepEqual(sub(e4a.todo.cap), [11.66, 58.33, 0]);
  const e4b = buyPlan({ ...e, spent: 161.66, bought: { U: 150, P: 11.66 }, boughtNow: { U: 150, P: 11.66 } });   // 이어서 P를 삼
  assert.deepEqual(sub(e4b.todo.cap), [0, 58.33, 0]);
});

// ---- 업종 탭(sectorTabs·buyGroup·groupLabel, 2026-11-19) — 가짜 티커, groupOf는 시험이 직접 넘긴다 ----
import { sectorTabs, buyGroup, groupLabel } from '../../preview-only-portfolio-home.js';
{
  const gOf = (t) => ({ S1: 'semi', S2: 'semi', S3: 'semi', N1: 'net', F1: 'fin', H1: 'semi', H2: 'ind' }[t] || `solo:${t}`);
  const shown = ['N1', 'S1', 'S2', 'F1', 'S3', 'Q'];
  test('업종 탭: 묶음 순서는 보이는 후보에서 처음 나온 순, 숨김뿐인 묶음은 맨 뒤', () => {
    const r = sectorTabs({ shown, picked: ['S1', 'N1', 'H1', 'H2'], ok: [], groupOf: gOf, plan: null });
    assert.deepEqual(r.map((g) => g.key), ['net', 'semi', 'fin', 'solo:Q', 'ind']);
    assert.deepEqual(r.find((g) => g.key === 'semi'), { key: 'semi', shownN: 3, pickedN: 1, hiddenN: 1, cap: null, amount: null });
    assert.deepEqual(r.find((g) => g.key === 'ind'), { key: 'ind', shownN: 0, pickedN: 0, hiddenN: 1, cap: null, amount: null });
    assert.deepEqual(r.find((g) => g.key === 'fin'), { key: 'fin', shownN: 1, pickedN: 0, hiddenN: 0, cap: null, amount: null });
  });
  test('업종 탭: 금액은 ok 종목의 todo만 센트로 더하고, 합은 전체 todo 합과 같다', () => {
    const plan = { todo: { S1: 10.1, S2: 20.2, S3: 5.05, N1: 0.1, Q: 7.07, H1: 99 }, groups: [{ key: 'semi', cap: 33.33 }, { key: 'net', cap: 33.33 }, { key: 'solo:Q', cap: 33.33 }] };
    const ok = ['S1', 'S2', 'N1', 'Q'];   // S3는 체크했지만 지금 못 삼, H1은 숨겨진 체크
    const r = sectorTabs({ shown, picked: ['S1', 'S2', 'S3', 'N1', 'Q', 'H1'], ok, groupOf: gOf, plan });
    const by = Object.fromEntries(r.map((g) => [g.key, g]));
    assert.equal(by.semi.amount, 30.3);   // 10.1 + 20.2 — 0.1+0.2식 소수 오차 없이
    assert.equal(by.net.amount, 0.1);
    assert.equal(by['solo:Q'].amount, 7.07);
    assert.equal(by.fin.amount, 0);   // 체크 없는 묶음은 0
    assert.equal(by.fin.cap, null);   // 계획에 없는 묶음의 업종 몫은 null
    assert.equal(by.semi.cap, 33.33);
    assert.equal(by.semi.hiddenN, 1);
    const sum = r.reduce((a, g) => a + Math.round(g.amount * 100), 0);
    assert.equal(sum, ok.reduce((a, t) => a + Math.round(plan.todo[t] * 100), 0));
  });
  test('업종 탭: 계획이 없으면 금액·업종 몫은 null이고 개수는 그대로', () => {
    const a = sectorTabs({ shown, picked: ['S1'], ok: ['S1'], groupOf: gOf, plan: null });
    const b = sectorTabs({ shown, picked: ['S1'], ok: ['S1'], groupOf: gOf, plan: { todo: { S1: 5 }, groups: null } });
    assert.ok(a.every((g) => g.amount === null && g.cap === null));
    assert.deepEqual(a.map((g) => [g.key, g.shownN, g.pickedN, g.hiddenN]), b.map((g) => [g.key, g.shownN, g.pickedN, g.hiddenN]));
    assert.equal(b.find((g) => g.key === 'semi').amount, 5);
    assert.ok(b.every((g) => g.cap === null));
  });
  test('묶음 키와 이름: 기술은 아래 갈래로, 분류 안 된 종목은 각자', () => {
    assert.equal(buyGroup('NVDA'), 'semi');
    assert.equal(buyGroup('JPM'), 'fin');
    assert.equal(buyGroup('SPY'), 'idx');
    assert.equal(buyGroup('ZZZZ'), 'solo:ZZZZ');
    assert.equal(groupLabel('semi'), '반도체');
    assert.equal(groupLabel('fin'), '금융');
    assert.equal(groupLabel('idx'), '지수 ETF');
    assert.equal(groupLabel('solo:ZZZZ'), '분류 안 됨 · ZZZZ');
  });
}
