// Tests for preview-only-portfolio-accounts.js — 한국 계좌(키움, 2026-10-28). 설계(STRATEGY_DESIGN.md '한국 계좌') 9절 숫자 사례를 시험으로.
// Run: node --test pipeline/portfolio/test_accounts.mjs
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { ledgerActive, ledgerDeposits, incomeList, kwState, mergeStart, fxSeries, krwPerformance, tradesOf } from '../../preview-only-portfolio-accounts.js';
import { actualAccount } from '../../preview-only-portfolio-actual.js';
import { monthBuys, monthSells } from '../../preview-only-portfolio-home.js';
import { openUtcMs, _internal } from '../../preview-only-portfolio-engine.js';

const cal = _internal.makeCalendar();
const near = (a, b, eps = 1e-9) => assert.ok(Math.abs(a - b) <= eps, `${a} != ${b}`);
// 기록 시각: 그날 장 마감 뒤(반영일 = 다음 장)
const after = (d) => new Date(openUtcMs(d) + 8 * 3600e3).toISOString();

function recs(from, to, px, fx) {
  const days = cal.sessions.filter((d) => d >= from && d <= to);
  return days.map((d, i) => ({ session: d, generatedAt: new Date(openUtcMs(cal.sessions[cal.index(d) + 1]) + 90 * 60e3).toISOString(), ruleVersion: 'v2-verdict', pipelineFull: true,
    cards: { AAA: { tier: '적정', tierStatus: 'valid', close: px(d), verdictAsOf: d, priceStale: false } }, prices: { SPY: 500 }, splits: [], missing: [],
    prevSession: i ? days[i - 1] : null, prevPublishedAt: null, ...(fx && fx(d) ? { fx: { USDKRW: fx(d) } } : {}) }));
}

test('장부: 정정 체인은 root의 기록 시각·반영일·몫 달을 물려받고 마지막 유효본을 쓴다(사례 4), 충돌은 알린다', () => {
  const L = {
    A: { kind: 'fx', usd: 100, krw: 135000, date: '2026-10-29', recordedAt: after('2026-10-29'), forMonth: '2026-10' },
    x1: { cancels: 'A', recordedAt: after('2026-11-05') },
    B: { kind: 'fx', usd: 120, krw: 160000, date: '2026-10-29', root: 'A', replaces: 'A', recordedAt: after('2026-11-05') },
    x2: { cancels: 'B', recordedAt: after('2026-11-10') },
    C: { kind: 'fx', usd: 110, krw: 148000, date: '2026-10-29', root: 'A', replaces: 'B', recordedAt: after('2026-11-10') },
  };
  const { events, conflicts } = ledgerActive(L);
  assert.equal(events.length, 1); assert.equal(conflicts.length, 0);
  assert.equal(events[0].id, 'C'); assert.equal(events[0].usd, 110);
  assert.equal(events[0].day, '2026-10-30'); assert.equal(events[0].forMonth, '2026-10'); assert.equal(events[0].rec, '2026-10-29');
  const dep = ledgerDeposits(events);
  assert.deepEqual(Object.keys(dep), ['L:A']); assert.equal(dep['L:A'].amount, 110); assert.equal(dep['L:A'].recordedAt, L.A.recordedAt);
  // 두 기기에서 A를 따로 고쳐 둘 다 살아 있으면 충돌
  const L2 = { A: L.A, x1: L.x1, B: L.B, D: { ...L.B, usd: 130, recordedAt: after('2026-11-06') } };
  const c2 = ledgerActive(L2);
  assert.deepEqual(c2.conflicts.map((c) => c.root), ['A']); assert.deepEqual(c2.conflicts[0].ids.map((x) => x.id).sort(), ['B', 'D']);
  assert.equal(c2.events.length, 0);   // 충돌 체인은 계산에서 뺀다(dr)
  // 단독 취소면 그 체인은 없다
  assert.equal(ledgerActive({ A: L.A, x1: L.x1 }).events.length, 0);
});

test('키움 상태: 수수료는 매수 원가에 더하고 매도 대금에서 뺀다, 부분 매도 뒤 평균 단가(설계 8절 예), 역환전·배당', () => {
  const ev = ledgerActive({ f: { kind: 'fx', usd: 2000, krw: 2700000, recordedAt: after('2026-10-29') },
    o: { kind: 'fxOut', usd: 100, krw: 133000, recordedAt: after('2026-11-02') }, i: { kind: 'income', usd: 5, date: '2026-11-03', recordedAt: after('2026-11-03') } }).events;
  const T = {
    t1: { date: '2026-10-30', ticker: 'AAA', side: 'buy', qty: 10, price: 100, fee: 0, account: 'kw' },
    t2: { date: '2026-11-02', ticker: 'AAA', side: 'sell', qty: 5, price: 110, fee: 1, account: 'kw' },
    t3: { date: '2026-11-03', ticker: 'AAA', side: 'buy', qty: 5, price: 120, fee: 0, account: 'kw' },
    r1: { date: '2026-11-03', ticker: 'BBB', side: 'buy', qty: 1, price: 50 },   // Robinhood — 키움에 안 섞임
  };
  const s = kwState(ev, T, '2026-11-04', 'rec');
  assert.equal(s.holdings.length, 1); near(s.holdings[0].qty, 10); near(s.holdings[0].avgPrice, 110);   // 원가 500 + 600 = 1,100
  near(s.cash, 2000 - 1000 + (550 - 1) - 100 + 5 - 600);
  assert.deepEqual(Object.keys(tradesOf(T, 'rh')), ['r1']);
  // 사례 6: 경계 날 — 10/23 반영 환전 200, 10/23 매수 150 → 시작 상태 현금 50 + 주식
  const e6 = ledgerActive({ f: { kind: 'fx', usd: 200, krw: 270000, recordedAt: after('2026-10-22') } }).events;
  const s6 = kwState(e6, { b: { date: '2026-10-23', ticker: 'AAA', side: 'buy', qty: 1.5, price: 100, account: 'kw' } }, '2026-10-23', 'eff');
  near(s6.cash, 50); near(s6.holdings[0].qty, 1.5);
  const m = mergeStart({ date: '2026-10-23', holdings: { AAA: 2 }, cash: 10 }, s6);
  near(m.holdings.AAA, 3.5); near(m.cash, 60);
});

test('한도: 산 돈 = 대금 + 수수료, 판 돈 = 대금 − 수수료, 배당은 판 돈 칸(사례 3)', () => {
  const T = { b: { date: '2026-11-03', ticker: 'AAA', side: 'buy', qty: 1, price: 99, fee: 1, account: 'kw' }, s: { date: '2026-11-10', ticker: 'AAA', side: 'sell', qty: 0.5, price: 100, fee: 1, account: 'kw' } };
  near(monthBuys(T, '2026-11', '2026-11-30').get('AAA').amount, 100);
  near(monthSells(T, '2026-11', '2026-11-30'), 49);
  near(monthSells(T, '2026-11', '2026-11-30', [{ date: '2026-11-12', amount: 3 }]), 52);
});

test('키움 달러 수익률: 첫 유입 당일(사례 2), 전액 역환전은 손실이 아니다(사례 1)', () => {
  // 10/30 반영 +1,000, 그날 AAA 10주 @100 매수, 종가 101 → +1.0%
  const px = (d) => (d <= '2026-10-29' ? 100 : d === '2026-10-30' ? 101 : d === '2026-11-02' ? 101 : 102);
  const R = recs('2026-10-23', '2026-11-04', px);
  const ev = ledgerActive({ f: { kind: 'fx', usd: 1000, krw: 1350000, recordedAt: after('2026-10-29') } }).events;
  const T = { t: { date: '2026-10-30', ticker: 'AAA', side: 'buy', qty: 10, price: 100, account: 'kw' } };
  const kwLine = actualAccount({ records: R, snapshot: { date: '2026-10-23', holdings: {}, cash: 0 }, deposits: ledgerDeposits(ev), trades: T, account: 'kw' });
  const d30 = kwLine.days.find((x) => x.date === '2026-10-30');
  near(d30.twr, 0.01);
  // 사례 1: 전날 1,000 현금, 그날 전액 역환전 −1,000 → 그날 건너뜀, 다음 날 +500 유입, 종가 510 → +2%
  const ev1 = ledgerActive({ f: { kind: 'fx', usd: 1000, krw: 1350000, recordedAt: after('2026-10-28') }, o: { kind: 'fxOut', usd: 1000, krw: 1300000, recordedAt: after('2026-10-29') },
    g: { kind: 'fx', usd: 500, krw: 650000, recordedAt: after('2026-10-30') } }).events;
  const T1 = { t: { date: '2026-11-02', ticker: 'AAA', side: 'buy', qty: 5, price: 100, account: 'kw' } };
  const px1 = (d) => (d < '2026-11-02' ? 100 : 102);
  const l1 = actualAccount({ records: recs('2026-10-23', '2026-11-03', px1), snapshot: { date: '2026-10-23', holdings: {}, cash: 0 }, deposits: ledgerDeposits(ev1), trades: T1, account: 'kw' });
  const tw = (d) => l1.days.find((x) => x.date === d).twr;
  near(tw('2026-10-30'), 0);   // 10/30 반영 역환전: 분모 0 → 건너뜀(손실 아님)
  near(tw('2026-11-02'), 0.02);   // 11/2 반영 +500, 5주 @100 → 종가 102 ×5 = 510 → +2%
});

test('원화 성과: 흐름은 반영일 전날 환율 — 첫 유입 0%(사례 9), 전액 역환전 분모 0(사례 10), 환율 수익률', () => {
  const fx = (d) => (d <= '2026-10-29' ? 1300 : 1310);
  const R = recs('2026-10-23', '2026-11-03', () => 100, fx);
  const fxAt = fxSeries(R, null);
  const ev = ledgerActive({ f: { kind: 'fx', usd: 1000, krw: 1350000, recordedAt: after('2026-10-28') } }).events;   // 반영 10/29(전날 10/28 환율 1300)
  const line = actualAccount({ records: R, snapshot: { date: '2026-10-23', holdings: {}, cash: 0 }, deposits: ledgerDeposits(ev), trades: {}, account: 'kw' });
  const k = krwPerformance(line, ev, fxAt);
  near(k.avgRate, 1350); near(k.rate, 1310);
  near(k.fxReturn, 1310 / 1350 - 1);
  near(k.pnlKrw, 1000 * 1310 - 1350000);
  near(k.krwTwr, 1310 / 1300 - 1, 1e-9);   // 10/29 0%(1,300,000 ÷ 1,300,000), 10/30 환율 1310 → +0.769%
  // 사례 10: 10/29 반영 전액 역환전 — 원화 흐름 = −1,000 × 전날(10/28) 1,300 → 분모 0
  const ev2 = ledgerActive({ f: { kind: 'fx', usd: 1000, krw: 1350000, recordedAt: after('2026-10-26') }, o: { kind: 'fxOut', usd: 1000, krw: 1290000, recordedAt: after('2026-10-28') } }).events;
  const line2 = actualAccount({ records: R, snapshot: { date: '2026-10-23', holdings: {}, cash: 0 }, deposits: ledgerDeposits(ev2), trades: {}, account: 'kw' });
  const k2 = krwPerformance(line2, ev2, fxAt);
  near(k2.krwTwr, 0);
  near(k2.pnlKrw, 1290000 - 1350000);
});

test('환율: 공개 기록 값이 fx_history보다 먼저, 빈 날은 직전 값(5거래일까지), 그 뒤 미확정(사례 7)', () => {
  const R = recs('2026-10-23', '2026-11-10', () => 100, (d) => (d === '2026-10-23' ? 1320 : null));
  const fxAt = fxSeries(R, { rates: { '2026-10-23': 1999, '2026-10-26': 1330 } });
  assert.equal(fxAt('2026-10-23').rate, 1320);
  assert.equal(fxAt('2026-10-26').rate, 1330);
  const c = fxAt('2026-10-28'); assert.equal(c.rate, 1330); assert.equal(c.carried, true);
  assert.equal(fxAt('2026-11-02').rate, 1330);   // 5거래일째
  assert.equal(fxAt('2026-11-03'), null);       // 6거래일째 → 미확정
  assert.deepEqual(incomeList([{ kind: 'income', usd: 3, date: '2026-11-01' }]), [{ date: '2026-11-01', amount: 3, account: 'kw' }]);
});

test('원화 흐름은 반영일 "전날" 환율로 — 환율이 바뀐 날 유입하면 그날 환율 변동이 수익률에 든다', () => {
  const fx = (d) => (d <= '2026-10-29' ? 1300 : 1310);
  const R = recs('2026-10-23', '2026-11-03', () => 100, fx);
  const ev = ledgerActive({ f: { kind: 'fx', usd: 1000, krw: 1300000, recordedAt: after('2026-10-29') } }).events;   // 반영 10/30, 전날 10/29 1300
  const line = actualAccount({ records: R, snapshot: { date: '2026-10-23', holdings: {}, cash: 0 }, deposits: ledgerDeposits(ev), trades: {}, account: 'kw' });
  near(krwPerformance(line, ev, fxSeries(R, null)).krwTwr, 1310 / 1300 - 1, 1e-9);   // 그날 환율로 하면 0%가 된다
});

test('수수료: 키움 상태 현금과 실제 계좌 현금 모두 매수에 더하고 매도에서 뺀다', () => {
  const ev = ledgerActive({ f: { kind: 'fx', usd: 1000, krw: 1300000, recordedAt: after('2026-10-26') } }).events;
  const T = { b: { date: '2026-10-28', ticker: 'AAA', side: 'buy', qty: 2, price: 100, fee: 1.5, account: 'kw' }, s: { date: '2026-10-29', ticker: 'AAA', side: 'sell', qty: 1, price: 100, fee: 0.5, account: 'kw' } };
  near(kwState(ev, T, '2026-10-30', 'eff').cash, 1000 - 201.5 + 99.5);
  near(kwState(ev, T, '2026-10-30', 'eff').holdings[0].avgPrice, 100.75);
  const line = actualAccount({ records: recs('2026-10-23', '2026-10-30', () => 100), snapshot: { date: '2026-10-23', holdings: {}, cash: 0 }, deposits: ledgerDeposits(ev), trades: T, account: 'kw' });
  near(line.cash, 1000 - 201.5 + 99.5);
});

test('dr 수정: 키움 보유에 분할 반영, 원화 금액은 기록일 기준 평가액으로(오늘 기록한 환전이 손실로 보이지 않게)', () => {
  const R = [{ session: '2026-10-30', splits: [{ id: 's1', ticker: 'AAA', effectiveDate: '2026-10-30', ratio: 2 }] }];
  const ev = ledgerActive({ f: { kind: 'fx', usd: 200, krw: 270000, recordedAt: after('2026-10-27') } }).events;
  const s = kwState(ev, { b: { date: '2026-10-29', ticker: 'AAA', side: 'buy', qty: 1, price: 100, account: 'kw' } }, '2026-10-30', 'eff', R);
  near(s.holdings[0].qty, 2); near(s.holdings[0].avgPrice, 50);
  // 오늘(10/30 장 뒤) 환전 1,000 기록 — 반영일은 다음 장이라 줄에는 없지만, 기록일 기준 평가액(2,000)을 넘기면 원금과 맞는다
  const fx = () => 1300;
  const R2 = recs('2026-10-23', '2026-10-30', () => 100, fx);
  const ev2 = ledgerActive({ a: { kind: 'fx', usd: 1000, krw: 1300000, recordedAt: after('2026-10-26') }, b: { kind: 'fx', usd: 1000, krw: 1300000, recordedAt: after('2026-10-30') } }).events;
  const line = actualAccount({ records: R2, snapshot: { date: '2026-10-23', holdings: {}, cash: 0 }, deposits: ledgerDeposits(ev2), trades: {}, account: 'kw' });
  near(krwPerformance(line, ev2, fxSeries(R2, null), 2000).pnlKrw, 0);
  near(krwPerformance(line, ev2, fxSeries(R2, null)).pnlKrw, -1300000);   // 줄 값만 쓰면 생기던 허위 손실
});

test('dr r2: 합계 줄은 계좌별 보유까지만 판다 — 키움에만 있는 주식을 Robinhood 매도로 팔지 않는다', () => {
  const R = recs('2026-10-23', '2026-10-30', () => 100);
  const ev = ledgerActive({ f: { kind: 'fx', usd: 1000, krw: 1300000, recordedAt: after('2026-10-23') } }).events;
  const T = { k: { date: '2026-10-27', ticker: 'AAA', side: 'buy', qty: 10, price: 100, account: 'kw' }, r: { date: '2026-10-28', ticker: 'AAA', side: 'sell', qty: 5, price: 100 } };
  const real = actualAccount({ records: R, snapshot: { date: '2026-10-23', holdings: {}, cash: 0 }, deposits: ledgerDeposits(ev), trades: T, kwStart: {} });
  near(real.holdings.AAA, 10); near(real.cash, 0);   // Robinhood 매도 5주는 체결되지 않음(Robinhood 보유 0)
  assert.ok(real.warnings.some((w) => w.includes('많이 판')));
});

test('dr r3: 미확정(null)으로 넘긴 평가액·환율은 과거 값으로 대신하지 않는다', () => {
  const R = recs('2026-10-23', '2026-10-30', () => 100, () => 1300);
  const ev = ledgerActive({ a: { kind: 'fx', usd: 1000, krw: 1300000, recordedAt: after('2026-10-26') } }).events;
  const line = actualAccount({ records: R, snapshot: { date: '2026-10-23', holdings: {}, cash: 0 }, deposits: ledgerDeposits(ev), trades: {}, account: 'kw' });
  const k = krwPerformance(line, ev, fxSeries(R, null), null, null);
  assert.equal(k.pnlKrw, null); assert.equal(k.valueKrw, null); assert.equal(k.fxReturn, null);
  near(krwPerformance(line, ev, fxSeries(R, null)).pnlKrw, 0);   // 안 넘기면 줄 값(1,000 × 1,300)
});
