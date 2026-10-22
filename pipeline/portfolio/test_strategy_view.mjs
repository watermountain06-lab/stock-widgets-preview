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
  assert.equal(depositsSince(all, '2026-10-16', '2026-10-20').length, 2);   // 오늘 뒤 반영은 아직
});

import { paramsText } from '../../preview-only-portfolio-strategy.js';
test('paramsText: 전략 설정 한 줄 요약', () => {
  assert.equal(paramsText({ strategy: 'C', params: { splitWeeks: 4, cashReserve: 0 } }), '살 판정 초저평가·저평가 · 매도 안 팖 · 4회 · 유보 0%');
  assert.equal(paramsText({ strategy: 'D', params: { splitWeeks: 2, cashReserve: 0.1 } }), '살 판정 초저평가~적정 · 매도 고평가면 전부 · 2회 · 유보 10%');
  assert.equal(paramsText({ strategy: 'custom', params: { buyTiers: ['저평가', '적정'], sellFraction: 0.5, splitWeeks: 1, cashReserve: 0 } }), '살 판정 저평가·적정 · 매도 고평가면 50% · 1회 · 유보 0%');
  assert.equal(paramsText({ strategy: 'B', params: { sellFraction: 0 } }), '살 판정 초저평가~적정 · 매도 알림만 · 4회 · 유보 0%');
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
  assert.deepEqual(draftOf(null), { kind: 'verdict', tiers: ['초저평가', '저평가', '적정~저평가', '적정'], sell: 0, rounds: 4, reserve: 0, etfShare: 100, etfs: ['SPY', 'QQQ', 'RSP'] });
  const C = { strategy: 'C', params: { splitWeeks: 2, cashReserve: 0.1 } };
  assert.deepEqual(draftOf(C), { kind: 'verdict', tiers: ['초저평가', '저평가'], sell: 0, rounds: 2, reserve: 10, etfShare: 100, etfs: ['SPY', 'QQQ', 'RSP'] });
  assert.deepEqual(shapeOf('C', draftOf(C)), { strategy: 'C', params: { splitWeeks: 2, cashReserve: 0.1 } });
  assert.equal(shapeOf('C', { ...draftOf(C), sell: 25 }).strategy, 'custom');
  const D = { strategy: 'D', params: { splitWeeks: 4, cashReserve: 0 } };
  assert.equal(draftOf(D).sell, 100);
  assert.equal(shapeOf('D', draftOf(D)).strategy, 'D');
  // 새 전략·사용자 정의는 사용자 정의로, 살 판정은 판정 순서대로
  assert.deepEqual(shapeOf(null, { kind: 'verdict', tiers: ['적정', '초저평가'], sell: 50, rounds: 1, reserve: 20 }),
    { strategy: 'custom', params: { buyTiers: ['초저평가', '적정'], sellFraction: 0.5, splitWeeks: 1, cashReserve: 0.2 } });
  const cu = { strategy: 'custom', params: { buyTiers: ['저평가'], sellFraction: 0.33, splitWeeks: 3, cashReserve: 0 } };
  assert.deepEqual(draftOf(cu), { kind: 'verdict', tiers: ['저평가'], sell: 33, rounds: 3, reserve: 0, etfShare: 100, etfs: ['SPY', 'QQQ', 'RSP'] });
  assert.match(sentenceOf('C', draftOf(C)), /팔지 않습니다/);
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
  assert.deepEqual(rankRows(result, byId, 'twr').map((r) => r.id), ['s2', 'A', 'REAL', 's1']);
  assert.deepEqual(rankRows(result, byId, 'value').map((r) => r.id), ['A', 'REAL', 's2', 's1']);
  const r = rankRows(result, byId, 'spy');
  assert.equal(r[0].name, '둘'); assert.equal(r[0].slot, 4); assert.equal(r.at(-1).twr, null);
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
  assert.equal(a.title, '12월 15일, 3번째 나눠 사기');
  assert.equal(a.sub, '살 후보 BBB · EEE · 4회 중 2회 진행');
  assert.deepEqual([a.done, a.total], [2, 4]);
  assert.equal(nextAction({ plan, steps, next: null, stale: true }).title, '이번 달 결정 대기');
  assert.match(nextAction({ plan: { rounds, candidates: [] }, steps, next: null, stale: false }).sub, /살 후보 없음 · 다음 점검/);
});

import { buyPlan, monthDeposits, monthBuys } from '../../preview-only-portfolio-home.js';

test('원칙 3 매수 금액: 체크한 종목만, 균등·시총 비중·판정 가중, 센트 내림', () => {
  const tiers = { BBB: '저평가', CCC: '적정~저평가', EEE: '적정' };
  const p = buyPlan({ cands: ['BBB', 'CCC', 'EEE'], picked: ['BBB', 'EEE'], budget: 400, tiers, caps: { BBB: 3e12, EEE: 1e12 }, rounds: 4 });
  assert.deepEqual(p.sel, ['BBB', 'EEE']);
  assert.deepEqual(p.by.equal, { BBB: 200, EEE: 200 });
  assert.deepEqual(p.by.cap, { BBB: 300, EEE: 100 });   // 큰 시총도 1센트 틀리지 않게
  assert.deepEqual(p.by.tier, { BBB: 300, EEE: 100 });   // 저평가 3 : 적정 1
  assert.deepEqual(p.round.equal, { BBB: 50, EEE: 50 });
  // 내림: 200/3 = 66.666… → 66.66, 회차 66.66/4 = 16.665 → 16.66
  const q = buyPlan({ cands: ['A', 'B', 'C'], picked: ['A', 'B', 'C'], budget: 200, rounds: 4 });
  assert.deepEqual(q.by.equal, { A: 66.66, B: 66.66, C: 66.66 });
  assert.deepEqual(q.round.equal, { A: 16.66, B: 16.66, C: 16.66 });
  // 달러 실수 오차로 1센트 빠지지 않게(1.16 × 100 = 115.999…)
  assert.equal(buyPlan({ cands: ['A'], picked: ['A'], budget: 1.16, rounds: 4 }).round.equal.A, 0.29);
  // 무게가 없는 종목이 하나라도 있으면 그 방법은 계산하지 않는다
  assert.equal(buyPlan({ cands: ['BBB', 'CCC'], picked: ['BBB', 'CCC'], budget: 100, tiers, caps: { BBB: 1 } }).by.cap, null);
  assert.equal(buyPlan({ cands: ['X'], picked: ['X'], budget: 100, tiers: { X: '고평가' } }).by.tier, null);
  assert.equal(buyPlan({ cands: ['BBB'], picked: [], budget: 100 }).by.equal, null);
  assert.deepEqual(buyPlan({ cands: ['BBB'], picked: ['BBB'], budget: 0 }).round.equal, { BBB: 0 });

  // 정확한 정수 내림(dr r2): 무게 1·1·2·3·4(합 11)에 $0.55 → 저평가 3/11 = 15센트(실수 비율이면 14)
  const T5 = { A: '적정', B: '적정', C: '적정~저평가', D: '저평가', E: '초저평가' };
  assert.equal(buyPlan({ cands: ['A', 'B', 'C', 'D', 'E'], picked: ['A', 'B', 'C', 'D', 'E'], budget: 0.55, tiers: T5 }).by.tier.D, 0.15);
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
