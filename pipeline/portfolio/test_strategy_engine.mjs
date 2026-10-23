// Tests for preview-only-portfolio-engine.js (2026-10-19). Run: node --test pipeline/portfolio/test_strategy_engine.mjs
// 가짜 티커(AAA~DDD)와 고정 ETF만 쓴다. 기록 X는 다음 거래일 장 시작 90분 뒤에 만들어지고 10분 뒤 공개된다고 둔다
// (v2 cards가 다음 날 동부 오전에 끝나는 실제 일정과 같은 모양 — 그래서 D의 결정에는 보통 D−2 기록이 쓰인다).
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { replay, twr, openUtcMs, depositTiming, isTradingDay, ENGINE_VERSION, _internal } from '../../preview-only-portfolio-engine.js';

const cal = _internal.makeCalendar();
const next = (d) => cal.sessions[cal.index(d) + 1];
const between = (a, b) => cal.sessions.slice(cal.index(a), cal.index(b) + 1);
const DEF_CLOSE = { AAA: 100, BBB: 50, CCC: 20, DDD: 10, SPY: 500, RSP: 200, QQQ: 400 };
const DEF_TIER = { AAA: '적정', BBB: '저평가', CCC: '고평가~적정', DDD: '고평가' };
const CARDS = ['AAA', 'BBB', 'CCC', 'DDD'];

// opts: end, omit[sessions], failed[sessions], tier(t,d), close(t,d), rule(d), asOf(t,d), drop(t,d)(카드에서 뺌),
//       splits{session: [split]}, nullPub[sessions](그 기록의 공개 시각을 모름)
function world(opts = {}) {
  const days = between('2026-10-16', opts.end || '2026-12-31').filter((d) => !(opts.omit || []).includes(d));
  const recs = [];
  for (const d of days) {
    const cards = {}, prices = {};
    for (const t of CARDS) {
      if (opts.asPrice?.(t, d)) { prices[t] = opts.close?.(t, d) ?? DEF_CLOSE[t]; continue; }
      if (opts.drop?.(t, d)) continue;
      const tier = opts.tier?.(t, d);
      const c = opts.close?.(t, d);
      cards[t] = {
        tier: tier === undefined ? DEF_TIER[t] : tier, tierStatus: 'valid',
        close: c === undefined ? DEF_CLOSE[t] : c, verdictAsOf: opts.asOf?.(t, d) ?? d, priceStale: false,
      };
    }
    for (const t of ['SPY', 'RSP', 'QQQ']) {
      const c = opts.close?.(t, d);
      if (c !== null) prices[t] = c === undefined ? DEF_CLOSE[t] : c;
    }
    const gen = new Date(openUtcMs(next(d)) + (opts.genLagMin ?? 90) * 60e3);   // 다음 거래일 장 시작 90분 뒤
    recs.push({
      session: d, generatedAt: gen.toISOString(), ruleVersion: opts.rule?.(d) ?? 'v2-verdict', scoreVersion: 'v2',
      pipelineFull: !(opts.failed || []).includes(d), cards, prices, splits: opts.splits?.[d] || [], missing: [],
    });
  }
  recs.forEach((r, i) => {
    const p = recs[i - 1];
    r.prevSession = p ? p.session : null;
    r.prevPublishedAt = p && !(opts.nullPub || []).includes(p.session)
      ? new Date(Date.parse(p.generatedAt) + 10 * 60e3).toISOString() : null;
  });
  return recs;
}
const SNAP = { date: '2026-10-16', holdings: { AAA: 10, DDD: 100 }, cash: 1000 };   // 평가 3000달러
const run = (o = {}) => replay({
  records: o.records || world(o.world), snapshot: o.snapshot || SNAP, deposits: o.deposits || [],
  settings: o.settings || {}, scenarios: o.scenarios || [],
});
const S = (strategy, params, extra = {}) => ({ id: extra.id || strategy, name: 'x', strategy, params, createdAt: extra.createdAt || '2026-10-16T22:00:00Z', engineVersion: ENGINE_VERSION });
const pick = (res, id) => res.scenarios.find((s) => s.id === id);
const day = (s, d) => s.days.find((x) => x.date === d);
const trades = (s, f = {}) => s.trades.filter((t) => Object.entries(f).every(([k, v]) => t[k] === v));
const nov = (xs) => xs.filter((t) => t.date < '2026-12-01');
const near = (a, b, eps = 1e-6) => assert.ok(Math.abs(a - b) <= eps, `${a} != ${b}`);

// ---------------- 달력·시각 ----------------
test('calendar: 휴장일·점검일·장 시작 시각(서머타임)', () => {
  assert.equal(cal.isSession('2026-11-26'), false);                 // 추수감사절
  assert.equal(cal.checkDay('2026-11-15'), '2026-11-02');           // 11-01 일요일
  assert.equal(cal.checkDay('2027-01-20'), '2027-01-04');           // 01-01 휴장, 주말
  assert.equal(new Date(openUtcMs('2026-10-19')).toISOString(), '2026-10-19T13:30:00.000Z');
  assert.equal(new Date(openUtcMs('2026-11-02')).toISOString(), '2026-11-02T14:30:00.000Z');
  assert.throws(() => cal.index('2028-01-03'), /휴장일이 없다/);
});

// ---------------- 정보 마감 ----------------
test('info cutoff: 장 시작 전에 공개된 최신 기록, 2거래일 이내', () => {
  const mk = _internal.makeMarket(world(), cal);
  assert.equal(mk.infoFor('2026-11-02').rec.session, '2026-10-29');   // 10-30 기록은 11-02 장 중에 공개
  assert.equal(mk.infoFor('2026-11-02').provisional, false);
  // 기록이 장 시작 전에 공개되면 직전 거래일 것을 쓴다
  const fast = _internal.makeMarket(world({ genLagMin: -600 }), cal);
  assert.equal(fast.infoFor('2026-11-02').rec.session, '2026-10-30');
  // 2거래일 넘게 오래되면 정보 없음
  const gap = _internal.makeMarket(world({ omit: ['2026-10-28', '2026-10-29'] }), cal);
  assert.equal(gap.infoFor('2026-11-02'), null);
  // 파이프라인 실패 기록은 정보로 쓰지 않는다(10-28은 3거래일 전이라 정보 없음, 11-03에는 10-30을 쓴다)
  const bad = _internal.makeMarket(world({ failed: ['2026-10-29'] }), cal);
  assert.equal(bad.infoFor('2026-11-02'), null);
  assert.equal(bad.infoFor('2026-11-03').rec.session, '2026-10-30');
  // 다음 기록이 있는데 공개 시각을 모르면 공개 전으로 본다
  const np = _internal.makeMarket(world({ nullPub: ['2026-10-29'] }), cal);
  assert.equal(np.infoFor('2026-11-02'), null);
  assert.equal(np.infoFor('2026-11-03').rec.session, '2026-10-30');
  // 마지막 기록은 공개 시각이 미정 — generatedAt이 장 시작 전이면 잠정으로 쓴다
  const tail = _internal.makeMarket(world({ end: '2026-10-30', genLagMin: -600 }), cal);
  assert.deepEqual([tail.infoFor('2026-11-02').rec.session, tail.infoFor('2026-11-02').provisional], ['2026-10-30', true]);
  const tail2 = _internal.makeMarket(world({ end: '2026-10-30' }), cal);
  assert.equal(tail2.infoFor('2026-11-02').rec.session, '2026-10-29');
});

// ---------------- 점검일·회차 일정·금액/수량 ----------------
test('schedule: 점검일 당일 종가부터 매주 같은 요일, 휴장이면 다음 거래일, 매수는 금액·매도는 수량', () => {
  const res = run({ world: { end: '2027-01-29' }, scenarios: [S('D')] });
  const d = pick(res, 'D');
  const m11 = d.months[0];
  assert.equal(m11.decisionDate, '2026-11-02');
  assert.equal(m11.record, '2026-10-29');
  assert.deepEqual(m11.rounds.map((r) => r.date), ['2026-11-02', '2026-11-09', '2026-11-16', '2026-11-23']);
  assert.deepEqual(m11.candidates, ['AAA', 'BBB']);
  // 매도: 100주 × 100% ÷ 4
  assert.deepEqual(trades(d, { ticker: 'DDD', side: 'sell' }).map((t) => [t.date, t.shares]),
    [['2026-11-02', 25], ['2026-11-09', 25], ['2026-11-16', 25], ['2026-11-23', 25]]);
  // 매수: 1000달러 ÷ 2후보 ÷ 4회 = 125달러, 수량 = 금액 ÷ 종가
  const a1 = trades(d, { ticker: 'AAA', date: '2026-11-02' })[0];
  assert.equal(a1.amount, 125); near(a1.shares, 1.25);
  // 1월: 01-04(월), 01-11, MLK(01-18) → 01-19, 01-25
  const jan = d.months.find((m) => m.checkDate === '2027-01-04');
  assert.deepEqual(jan.rounds.map((r) => r.date), ['2027-01-04', '2027-01-11', '2027-01-19', '2027-01-25']);
});

test('schedule: 정보 없음으로 결정이 밀리면 결정일 요일을 쓰고, 다음 점검일 뒤 회차는 버린다', () => {
  const omit = between('2026-10-28', '2026-11-20');
  const res = run({ world: { omit }, scenarios: [S('B')] });
  const b = pick(res, 'B');
  const m11 = b.months[0];
  assert.equal(m11.decisionDate, '2026-11-25');   // 11-23 기록이 11-24에 공개 → 11-25 결정
  assert.deepEqual(m11.rounds.map((r) => [r.date, r.dropped]),
    [['2026-11-25', false], ['2026-12-02', true], ['2026-12-09', true], ['2026-12-16', true]]);
  assert.ok(b.events.some((e) => e.kind === 'decisionDeferred' && e.date === '2026-11-02'));
  const dropped = b.skips.filter((x) => x.reason === 'pastNextCheck' && x.ticker === 'AAA');
  assert.equal(dropped.length, 3);
  assert.equal(trades(b, { ticker: 'AAA' }).filter((t) => t.date < '2026-12-01').length, 1);
});

test('schedule: 다음 점검일 당일에 떨어지는 회차도 버린다', () => {
  const b = pick(run({ world: { omit: between('2026-10-28', '2026-11-05') }, scenarios: [S('B')] }), 'B');
  assert.equal(b.months[0].decisionDate, '2026-11-10');
  assert.deepEqual(b.months[0].rounds.map((r) => [r.date, r.dropped]),
    [['2026-11-10', false], ['2026-11-17', false], ['2026-11-24', false], ['2026-12-01', true]]);
  assert.equal(b.months[1].checkDate, '2026-12-01');
});

test('schedule: 지난달 결정이 다음 점검일까지 못 나면 버린다', () => {
  const omit = between('2026-10-28', '2026-12-01');
  const res = run({ world: { omit }, scenarios: [S('B')] });
  const b = pick(res, 'B');
  assert.ok(b.events.some((e) => e.kind === 'decisionDropped' && e.checkDate === '2026-11-02'));
  assert.equal(b.months[0].checkDate, '2026-12-01');
});

// ---------------- 회차 재확인 ----------------
test('recheck: 조건을 벗어난 회차는 지우고(넘기지 않음) 현금으로 둔다', () => {
  const res = run({ world: { tier: (t, d) => (t === 'AAA' && d === '2026-11-05' ? '고평가' : undefined) }, scenarios: [S('B')] });
  const b = pick(res, 'B');
  assert.deepEqual(nov(trades(b, { ticker: 'AAA', side: 'buy' })).map((t) => [t.date, t.amount]),
    [['2026-11-02', 125], ['2026-11-16', 125], ['2026-11-23', 125]]);
  assert.deepEqual(b.skips.map((x) => [x.date, x.ticker, x.reason, x.action]), [['2026-11-09', 'AAA', 'tierOut', 'erased']]);
  near(day(b, '2026-11-30').value, 3000, 0.02);       // 가격이 그대로라 평가액은 그대로(현금 + 산 주식)
  assert.equal(b.months[1].budget, 125);            // 지운 125달러는 현금으로 남아 12월 예산이 된다
});

test('recheck: 정보 없음(정보로 쓸 기록이 없거나 실패) 회차는 다음 회차로 넘긴다', () => {
  for (const w of [{ omit: ['2026-11-04', '2026-11-05'] }, { failed: ['2026-11-05'] }]) {
    const b = pick(run({ world: w, scenarios: [S('B')] }), 'B');
    assert.deepEqual(nov(trades(b, { ticker: 'AAA', side: 'buy' })).map((t) => [t.date, t.amount]),
      [['2026-11-02', 125], ['2026-11-16', 250], ['2026-11-23', 125]], JSON.stringify(w));
    assert.ok(b.skips.some((x) => x.date === '2026-11-09' && x.reason === 'noInfo' && x.action === 'carried'));
  }
});

test('recheck: 체결일 그날 기록이 없거나 실패면 넘기고, 마지막 회차면 버린다', () => {
  for (const w of [{ omit: ['2026-11-09', '2026-11-23'] }, { failed: ['2026-11-09', '2026-11-23'] }]) {
    const b = pick(run({ world: w, scenarios: [S('B')] }), 'B');
    assert.deepEqual(nov(trades(b, { ticker: 'AAA', side: 'buy' })).map((t) => [t.date, t.amount]),
      [['2026-11-02', 125], ['2026-11-16', 250]], JSON.stringify(w));
    assert.deepEqual(b.skips.filter((x) => x.ticker === 'AAA').map((x) => [x.date, x.reason, x.action]),
      [['2026-11-09', 'pipelineFailed', 'carried'], ['2026-11-23', 'pipelineFailed', 'dropped']]);
    assert.equal(day(b, '2026-11-09')?.value ?? null, null);      // 실패 기록의 종가로 평가하지 않는다
  }
});

test('recheck: 종목 하나의 체결일 가격이 없으면 그 회차를 지운다(사용자 결정 10-20)', () => {
  const b = pick(run({ world: { close: (t, d) => (t === 'AAA' && (d === '2026-11-09' || d === '2026-11-23') ? null : undefined) }, scenarios: [S('B')] }), 'B');
  assert.deepEqual(nov(trades(b, { ticker: 'AAA', side: 'buy' })).map((t) => [t.date, t.amount]),
    [['2026-11-02', 125], ['2026-11-16', 125]]);
  assert.deepEqual(b.skips.filter((x) => x.ticker === 'AAA').map((x) => [x.date, x.reason, x.action]),
    [['2026-11-09', 'noPrice', 'erased'], ['2026-11-23', 'noPrice', 'erased']]);
  assert.equal(trades(b, { ticker: 'BBB', date: '2026-11-09' }).length, 1);   // 다른 종목은 그대로
  assert.deepEqual(b.months[0].summary.find((x) => x.ticker === 'AAA'), { ticker: 'AAA', side: 'buy', roundsDone: 2, notUsed: 250, scheduled: 0 });
});

test('recheck: 원칙 6 — 카드 없음·판정 없음·묵음은 결정에서 빼고 회차는 지운다', () => {
  const res = run({
    world: {
      drop: (t, d) => t === 'BBB' && d === '2026-10-29',
      asOf: (t, d) => (t === 'DDD' && d === '2026-10-29' ? '2026-10-16' : undefined),   // 9거래일 묵음
      tier: (t, d) => (t === 'AAA' && d === '2026-11-12' ? null : undefined),
    },
    scenarios: [S('D')],
  });
  const d = pick(res, 'D');
  const m11 = d.months[0];
  assert.deepEqual(m11.candidates, ['AAA']);
  assert.deepEqual(m11.fires, [{ ticker: 'DDD', observed: null, skip: 'stale' }]);
  assert.equal(nov(trades(d, { side: 'sell' })).length, 0);
  assert.ok(d.skips.some((x) => x.date === '2026-11-16' && x.ticker === 'AAA' && x.reason === 'noVerdict' && x.action === 'erased'));
});

// ---------------- 매도 발동 상태표 ----------------
test('lastStage: 발동 표(재진입 포함)', () => {
  const byMonth = { '2026-10': '고평가', '2026-11': '고평가', '2026-12': '초고평가', '2027-01': '고평가',
    '2027-02': '초고평가', '2027-03': '적정', '2027-04': '고평가', '2027-05': '고평가' };
  const res = run({
    world: { end: '2027-06-04', tier: (t, d) => (t === 'DDD' ? byMonth[d.slice(0, 7)] ?? '고평가' : undefined) },
    scenarios: [S('custom', { buyTiers: ['적정'], sellFraction: 0.5 })],
  });
  const c = pick(res, 'custom');
  const fires = c.months.flatMap((m) => m.fires.map((f) => [m.checkDate.slice(0, 7), f.prev, f.observed]));
  assert.deepEqual(fires, [
    ['2026-11', 'none', '고평가'], ['2027-01', '고평가', '초고평가'], ['2027-03', '고평가', '초고평가'], ['2027-05', 'out', '고평가'],
  ]);
  // 발동마다 그 점검일의 남은 수량 × 50%
  const sold = (m) => trades(c, { ticker: 'DDD', side: 'sell' }).filter((t) => t.date.startsWith(m)).reduce((a, t) => a + t.shares, 0);
  // 3월 발동은 2월 기록(초고평가)으로 했지만 3월 기록은 적정이라 2~4회차는 재확인에서 지운다(발동은 다시 계획하지 않음)
  near(sold('2026-11'), 50); near(sold('2027-01'), 25); near(sold('2027-03'), 3.125); near(sold('2027-05'), 10.9375);
  assert.equal(c.skips.filter((x) => x.ticker === 'DDD' && x.date.startsWith('2027-03') && x.reason === 'tierOut').length, 3);
  assert.equal(c.lastStage.DDD, '고평가');
});

test('lastStage: B(비율 0%)는 알림만, C는 관측하지 않는다', () => {
  const res = run({ scenarios: [S('B'), S('C')] });
  assert.deepEqual(pick(res, 'B').months[0].fires.map((f) => [f.ticker, f.warnOnly]), [['DDD', true]]);
  assert.equal(trades(pick(res, 'B'), { side: 'sell' }).length, 0);
  assert.deepEqual(pick(res, 'C').months[0].fires, []);
  assert.deepEqual(pick(res, 'C').months[0].candidates, ['BBB']);
});

test('ruleVersion: 점검일에 바뀌면 발동·매매 없이 관측만, 주중에 바뀌면 그 회차를 지운다', () => {
  const res = run({ world: { end: '2027-01-29', rule: (d) => (d >= '2026-11-12' ? 'v3' : 'v2') }, scenarios: [S('D')] });
  const d = pick(res, 'D');
  const m11 = d.months[0], dec = d.months[1], jan = d.months[2];
  assert.ok(d.skips.some((x) => x.date === '2026-11-16' && x.reason === 'ruleVersion' && x.action === 'erased'));
  assert.equal(dec.ruleChanged, true);
  assert.deepEqual(dec.legs, []);
  assert.deepEqual(dec.fires.map((f) => [f.ticker, f.skip]), [['AAA', 'ruleVersion'], ['BBB', 'ruleVersion'], ['DDD', 'ruleVersion']]);
  assert.equal(d.lastStage.DDD, '고평가');
  assert.equal(jan.ruleChanged, false);
  assert.ok(jan.legs.length > 0);
  assert.equal(m11.ruleChanged, false);
});

// ---------------- 매도 대금·현금 유보 ----------------
test('proceeds: 매도 대금은 그달 후보에 똑같이 나눠 다음 회차부터 더하고, 같은 날 매수에는 쓰지 않는다', () => {
  const res = run({ snapshot: { ...SNAP, cash: 0 }, scenarios: [S('D')] });
  const d = pick(res, 'D');
  assert.equal(trades(d, { side: 'buy', date: '2026-11-02' }).length, 0);    // 예산 0, 대금은 다음 회차부터
  // 1회차 대금 250 → 후보 2 → 125씩 → 남은 3회차: 41.66, 41.66, 41.68
  // 2회차 대금 250 → 125씩 → 남은 2회차: 62.5, 62.5
  // 3회차 대금 250 → 125씩 → 남은 1회차: 125. 4회차 대금은 남은 회차가 없어 현금으로
  const aaa = nov(trades(d, { ticker: 'AAA', side: 'buy' })).map((t) => [t.date, t.amount]);
  assert.deepEqual(aaa, [['2026-11-09', 41.66], ['2026-11-16', 104.16], ['2026-11-23', 229.18]]);
  assert.ok(d.events.some((e) => e.kind === 'proceedsToCash' && e.date === '2026-11-23'));
});

test('cashReserve: 매수 한도 = max(0, 현금 − 당일 매도 대금 − 유보액), 넘치면 비례로 줄인다', () => {
  const b = pick(run({ scenarios: [S('B', { cashReserve: 0.2 })] }), 'B');
  // 11-02: 현금 1000, 평가 3000 → 유보 600 → 한도 400 ≥ 250
  assert.equal(trades(b, { date: '2026-11-02', side: 'buy' }).reduce((a, t) => a + t.amount, 0), 250);
  // 11-09: 현금 750 → 한도 150 < 250 → 각 75
  assert.deepEqual(trades(b, { date: '2026-11-09', side: 'buy' }).map((t) => t.amount), [75, 75]);
  assert.ok(b.skips.some((x) => x.date === '2026-11-09' && x.reason === 'cashLimit' && x.amount === 50));
  // 같은 날 매도 대금은 한도에 넣지 않는다
  const c = pick(run({
    snapshot: { date: '2026-10-16', holdings: { DDD: 100 }, cash: 100 },
    scenarios: [S('custom', { buyTiers: ['적정'], sellFraction: 1, splitWeeks: 1, cashReserve: 0.5 })],
  }), 'custom');
  assert.equal(trades(c, { side: 'sell', date: '2026-11-02' })[0].amount, 1000);
  assert.equal(nov(trades(c, { side: 'buy' })).length, 0);      // 한도 = 1100 − 1000 − 550 < 0
  assert.equal(pick(run({ scenarios: [S('B')] }), 'B').notes.includes('noPrinciple7'), true);
  assert.equal(b.notes.includes('noPrinciple7'), false);
});

test('cashReserve: 그날 평가가 미확정이면 매수 회차를 지운다(매도는 진행)', () => {
  const d = pick(run({ world: { close: (t, x) => (t === 'AAA' && x === '2026-11-09' ? null : undefined) }, scenarios: [S('D', { cashReserve: 0.1 })] }), 'D');
  assert.deepEqual(trades(d, { date: '2026-11-09' }).map((t) => [t.ticker, t.side, t.shares]), [['DDD', 'sell', 25]]);
  assert.deepEqual(d.skips.filter((x) => x.date === '2026-11-09').map((x) => [x.ticker, x.reason, x.action]),
    [['AAA', 'noPrice', 'erased'], ['BBB', 'reserveUnknown', 'erased']]);
});

// ---------------- 입금 ----------------
test('deposits: 반영일은 기록 시각 뒤 첫 09:30 ET, A·기준선은 반영일 종가에 사고 B는 다음 점검일에 쓴다', () => {
  const deposits = [
    { id: 'd1', amount: 1000, recordedAt: '2026-11-07T15:00:00Z' },   // 토 → 11-09
    { id: 'd2', amount: 300, recordedAt: '2026-11-16T14:29:00Z' },    // 월 09:29 EST → 11-16
    { id: 'd3', amount: 200, recordedAt: '2026-11-16T14:31:00Z' },    // 월 09:31 EST → 11-17
  ];
  const res = run({ deposits, scenarios: [S('B')] });
  const a = pick(res, 'A'), b = pick(res, 'B');
  // A 비중: AAA 1000, DDD 1000 → 반반
  assert.deepEqual(trades(a).map((t) => [t.date, t.ticker, t.amount]), [
    ['2026-11-09', 'AAA', 500], ['2026-11-09', 'DDD', 500], ['2026-11-16', 'AAA', 150], ['2026-11-16', 'DDD', 150],
    ['2026-11-17', 'AAA', 100], ['2026-11-17', 'DDD', 100]]);
  assert.equal(day(a, '2026-11-17').deposits, 1500);
  assert.equal(day(b, '2026-11-17').deposits, 1500);
  assert.equal(nov(trades(b)).length, 8);
  assert.equal(b.months[1].budget, 1500);                    // 11월에 1000을 다 쓰고, 12월 예산은 입금 1500
  near(pick(res, 'A').baselines.SPY.find((x) => x.date === '2026-11-09').value, 4000, 0.01);
});

test('deposits: 기준선은 입금을 반영일 종가에 한 번에 산다', () => {
  const res = run({ world: { close: (t, d) => (t === 'SPY' && d >= '2026-11-10' ? 550 : undefined) },
    deposits: [{ id: 'd1', amount: 1000, recordedAt: '2026-11-07T15:00:00Z' }] });
  const spy = pick(res, 'A').baselines.SPY;
  near(spy.find((x) => x.date === '2026-11-10').value, (6 + 2) * 550, 0.01);   // 출발 3000/500 = 6주 + 입금 1000/500 = 2주
  near(spy.at(-1).twr, 0.1);
});

test('deposits: 출발이 미뤄진 사이의 입금도 A는 출발일 종가에 출발 비중대로 산다', () => {
  const res = run({ world: { close: (t, d) => (t === 'AAA' && d <= '2026-10-19' ? null : undefined) },
    deposits: [{ id: 'd', amount: 1000, recordedAt: '2026-10-17T15:00:00Z' }] });
  const a = pick(res, 'A');
  assert.equal(a.started, '2026-10-20');
  assert.equal(a.startValue, 4000);
  assert.deepEqual(trades(a).map((t) => [t.date, t.ticker, t.amount]), [['2026-10-20', 'AAA', 500], ['2026-10-20', 'DDD', 500]]);
  assert.equal(a.baselines.SPY[0].value, 4000);
  assert.equal(day(a, '2026-10-20').deposits, 0);
});

test('A는 원칙 6을 보지 않는다: 판정 없는 종목도 입금으로 산다, 카드에서 빠진 보유는 prices로 계속 평가', () => {
  const res = run({
    world: { tier: (t) => (t === 'AAA' ? null : undefined), asPrice: (t, d) => t === 'DDD' && d >= '2026-10-26' },
    deposits: [{ id: 'd', amount: 100, recordedAt: '2026-11-07T15:00:00Z' }], scenarios: [S('B')],
  });
  const a = pick(res, 'A'), b = pick(res, 'B');
  assert.deepEqual(trades(a).map((t) => t.ticker), ['AAA', 'DDD']);
  near(day(b, '2026-11-30').value, 3100, 0.02);           // DDD는 카드에서 빠져도 prices로 평가(입금 100 포함)
  assert.deepEqual(b.months[0].candidates, ['BBB']);
  assert.deepEqual(b.months[0].fires.map((f) => [f.ticker, f.skip]), [['AAA', 'noVerdict'], ['DDD', 'noCard']]);
});

test('deposits: 반영일 전 취소는 없애고, 늦은 취소는 무시한다', () => {
  const res = run({
    deposits: [
      { id: 'd1', amount: 1000, recordedAt: '2026-11-07T15:00:00Z' },
      { id: 'c1', cancels: 'd1', recordedAt: '2026-11-08T15:00:00Z' },
      { id: 'd2', amount: 500, recordedAt: '2026-11-10T15:00:00Z' },   // 11-11 반영
      { id: 'c2', cancels: 'd2', recordedAt: '2026-11-11T16:00:00Z' },
    ],
  });
  assert.equal(day(pick(res, 'A'), '2026-11-30').deposits, 500);
  assert.deepEqual(res.warnings, [{ kind: 'cancelIgnored', id: 'c2' }]);
});

// ---------------- 분할 ----------------
const sp = (t, eff, ratio) => ({ id: `${t}:${eff}`, ticker: t, effectiveDate: eff, ratio });

test('split: 기준선 ETF 분할도 적용한다', () => {
  const res = run({ world: { close: (t, d) => (t === 'SPY' && d >= '2026-11-10' ? 250 : undefined), splits: { '2026-11-10': [sp('SPY', '2026-11-10', 2)] } } });
  const spy = pick(res, 'A').baselines.SPY;
  near(spy.find((x) => x.date === '2026-11-10').value, 3000, 0.01);
  near(spy.at(-1).twr, 0);
});

test('split: 같은 id는 한 번만 적용한다', () => {
  const res = run({ world: { close: (t, d) => (t === 'DDD' && d >= '2026-11-10' ? 5 : undefined),
    splits: { '2026-11-10': [sp('DDD', '2026-11-10', 2)], '2026-11-11': [sp('DDD', '2026-11-10', 2)] } } });
  const a = pick(res, 'A');
  assert.equal(a.holdings.DDD, 200);
  assert.equal(a.halted, null);
  assert.equal(a.splitLog.length, 1);
});

test('split: 틀린 수량으로 평가한 날이 없으면 늦은 분할도 멈추지 않는다', () => {
  // 표시가 풀리는 날 분할이 실린다
  const release = pick(run({ world: { close: (t, d) => (t === 'AAA' && d >= '2026-11-10' ? 50 : undefined),
    splits: { '2026-11-17': [sp('AAA', '2026-11-10', 2)] } } }), 'A');
  assert.equal(release.halted, null);
  near(day(release, '2026-11-17').value, 3000, 0.01);
  // 효력일 기록이 없고 다음 기록에 실린다
  const gap = pick(run({ world: { omit: ['2026-11-10'], close: (t, d) => (t === 'AAA' && d >= '2026-11-10' ? 50 : undefined),
    splits: { '2026-11-11': [sp('AAA', '2026-11-10', 2)] } } }), 'A');
  assert.equal(gap.halted, null);
  near(day(gap, '2026-11-11').value, 3000, 0.01);
});

test('split 지연: 다른 급변으로 다시 켜진 표시가 지난 분할 지연을 숨기지 않는다', () => {
  const a = pick(run({ world: { close: (t, d) => (t === 'AAA' ? (d >= '2026-11-10' ? 25 : d >= '2026-11-02' ? 50 : undefined) : undefined),
    splits: { '2026-11-12': [sp('AAA', '2026-11-02', 2)] } } }), 'A');
  assert.equal(a.halted?.since, '2026-11-02');
});

test('split: 효력일 기록에 오면 장 시작 전 수량 × ratio, 남은 매도 예정 수량도 × ratio', () => {
  const res = run({
    world: { close: (t, d) => (t === 'DDD' && d >= '2026-11-10' ? 5 : undefined), splits: { '2026-11-10': [sp('DDD', '2026-11-10', 2)] } },
    scenarios: [S('D')],
  });
  const a = pick(res, 'A'), d = pick(res, 'D');
  assert.equal(a.holdings.DDD, 200);
  near(day(a, '2026-11-10').value, 3000, 0.01);
  assert.deepEqual(trades(d, { ticker: 'DDD', side: 'sell' }).map((t) => [t.date, t.shares]),
    [['2026-11-02', 25], ['2026-11-09', 25], ['2026-11-16', 50], ['2026-11-23', 50]]);
});

test('split: 시작일이나 그 전에 효력이 난 분할은 늦게 와도 브로커 수량을 바꾸지 않는다', () => {
  const res = run({ world: { splits: { '2026-10-20': [sp('DDD', '2026-10-16', 2)] } } });
  const a = pick(res, 'A');
  assert.equal(a.holdings.DDD, 100);
  assert.deepEqual(a.splitLog, [{ id: 'DDD:2026-10-16', date: '2026-10-20', action: 'ignored' }]);
});

test('split 안전망: 0.6배 이하로 뛰고 분할 기록이 없으면 확인 필요(이어짐), 5거래일 뒤 풀린다', () => {
  const res = run({ world: { close: (t, d) => (t === 'AAA' && d >= '2026-11-10' ? 50 : undefined) } });
  const a = pick(res, 'A');
  for (const d of between('2026-11-10', '2026-11-16')) {
    assert.equal(day(a, d).value, null, d);
    assert.deepEqual(day(a, d).why, ['splitCheck:AAA']);
  }
  near(day(a, '2026-11-17').value, 2500, 0.01);   // 풀린 뒤에는 새 가격으로
});

test('split 안전망: 표시 중에 늦은 분할이 오면 적용하고 이어서 계산한다', () => {
  const res = run({ world: {
    close: (t, d) => (t === 'AAA' && d >= '2026-11-10' ? 50 : undefined),
    splits: { '2026-11-12': [sp('AAA', '2026-11-10', 2)] } } });
  const a = pick(res, 'A');
  assert.equal(day(a, '2026-11-11').value, null);
  near(day(a, '2026-11-12').value, 3000, 0.01);
  assert.equal(a.halted, null);
});

test('split 지연: 표시가 풀린 뒤나 안전망이 못 잡는 비율(3:2)로 늦게 오면 효력일부터 평가 불가', () => {
  const late = run({ world: {
    close: (t, d) => (t === 'AAA' && d >= '2026-11-10' ? 50 : undefined),
    splits: { '2026-11-18': [sp('AAA', '2026-11-10', 2)] } } });
  assert.deepEqual(pick(late, 'A').halted, { reason: 'splitDelay', since: '2026-11-10', ticker: 'AAA' });
  assert.equal(day(pick(late, 'A'), '2026-11-09').value !== null, true);
  assert.equal(day(pick(late, 'A'), '2026-11-30').value, null);
  const r32 = run({ world: {
    close: (t, d) => (t === 'AAA' && d >= '2026-11-10' ? 100 / 1.5 : undefined),
    splits: { '2026-11-12': [sp('AAA', '2026-11-10', 1.5)] } } });
  assert.equal(pick(r32, 'A').halted.since, '2026-11-10');
  // 보유하지 않은 종목의 늦은 분할은 멈추지 않는다
  const other = run({ world: { splits: { '2026-11-12': [sp('BBB', '2026-11-10', 2)] } } });
  assert.equal(pick(other, 'A').halted, null);
  // A가 나중에 멈춰도 그 전에 출발할 파생 시나리오는 출발하고, 멈춘 효력일 전까지는 평가한다
  const d = pick(run({ world: {
    close: (t, x) => (t === 'AAA' && x >= '2026-11-10' ? 50 : undefined),
    splits: { '2026-11-18': [sp('AAA', '2026-11-10', 2)] } },
  scenarios: [S('B', undefined, { id: 'mid', createdAt: '2026-11-03T20:00:00Z' })] }), 'mid');
  assert.equal(d.started, '2026-11-03');
  assert.ok(day(d, '2026-11-09').value !== null);
  assert.equal(d.halted?.since, '2026-11-10');
});

test('split: 파생 시나리오는 A의 판단을 따른다(이중 적용 없음, 시작 전 효력 분할은 무시)', () => {
  const res = run({
    world: {
      close: (t, d) => (t === 'DDD' && d >= '2026-11-04' ? 5 : undefined),
      splits: { '2026-11-06': [sp('DDD', '2026-11-04', 2)], '2026-11-20': [sp('AAA', '2026-10-15', 2)] },
    },
    scenarios: [S('B', undefined, { id: 'late', createdAt: '2026-11-04T20:00:00Z' })],   // S = 11-05, S 전 거래일 11-04는 확인 필요
  });
  const a = pick(res, 'A'), l = pick(res, 'late');
  assert.equal(l.started, '2026-11-06');                  // A가 11-04·11-05 미확정 → 확정일로 미룸
  assert.equal(l.holdings.DDD, 200);                      // A가 적용한 분할 한 번만
  assert.equal(a.holdings.DDD, 200);
  assert.equal(a.holdings.AAA, 10);                       // 시작 전 효력 분할은 둘 다 무시
  assert.deepEqual(l.splitLog.map((x) => x.action), ['ignored']);
});

// ---------------- 가격 없는 날·TWR ----------------
test('twr: 일별 연결, 입금은 장 시작 전, 미확정 구간은 잇되 입금이 끼면 그 뒤 미확정', () => {
  assert.deepEqual(twr([{ value: 100 }, { value: 110, flow: 0 }, { value: null, flow: 0 }, { value: 121, flow: 0 }]), [0, 0.10000000000000009, null, 0.2100000000000002]);
  near(twr([{ value: 100 }, { value: 160, flow: 50 }])[1], 160 / 150 - 1);
  assert.deepEqual(twr([{ value: 100 }, { value: null, flow: 50 }, { value: 160, flow: 0 }, { value: 170, flow: 0 }]), [0, null, null, null]);
  assert.deepEqual(twr([{ value: 100 }, { value: null, flow: 0 }, { value: 160, flow: 50 }]), [0, null, null]);
});

test('price gap: 보유 종목 가격이 없으면 평가 미확정, 5거래일 넘으면 중단 표시, 돌아오면 이어서', () => {
  const gap = between('2026-11-10', '2026-11-18');   // 7거래일
  const res = run({ world: { close: (t, d) => (t === 'AAA' && gap.includes(d) ? null : undefined) },
    deposits: [{ id: 'd', amount: 100, recordedAt: '2026-11-11T15:00:00Z' }] });
  const a = pick(res, 'A');
  assert.equal(day(a, '2026-11-10').value, null);
  assert.equal(day(a, '2026-11-16').pause, undefined);
  assert.equal(day(a, '2026-11-17').pause, 6);
  assert.ok(day(a, '2026-11-19').value !== null);
  assert.equal(day(a, '2026-11-19').twr, null);            // 구간에 입금이 끼었다
  assert.equal(day(a, '2026-11-30').twr, null);
  assert.equal(day(a, '2026-11-19').deposits, 100);
  const noDep = pick(run({ world: { close: (t, d) => (t === 'AAA' && gap.includes(d) ? null : undefined) } }), 'A');
  near(day(noDep, '2026-11-19').twr, 0);
  assert.deepEqual(day(noDep, '2026-11-19').vs, { SPY: 0, RSP: 0, QQQ: 0 });
});

test('start: 시작일 평가가 미확정이면 다음 확정일로 출발을 미룬다', () => {
  const res = run({ world: { close: (t, d) => (t === 'AAA' && d === '2026-10-16' ? null : undefined) }, scenarios: [S('B')] });
  assert.equal(pick(res, 'A').started, '2026-10-19');
  assert.equal(pick(res, 'B').started, '2026-10-19');
  assert.equal(pick(res, 'A').baselines.SPY[0].date, '2026-10-19');
});

// ---------------- 전략과 기준선 ----------------
test('strategies: A는 매도 없음·원칙 6 무시, 기준선은 출발 평가액을 전부 넣는다', () => {
  const res = run({ world: { close: (t, d) => (t === 'SPY' && d >= '2026-11-02' ? 550 : undefined) }, scenarios: [S('B'), S('C'), S('D')] });
  const a = pick(res, 'A');
  assert.equal(a.trades.length, 0);
  assert.deepEqual(a.holdings, { AAA: 10, DDD: 100 });
  const spy = a.baselines.SPY;
  assert.equal(spy[0].value, 3000);
  near(spy.at(-1).twr, 0.1);
  near(day(a, '2026-12-31').vs.SPY, -10);
  assert.equal(day(a, '2026-12-31').vs.RSP, 0);
  assert.deepEqual(res.scenarios.map((s) => s.id), ['A', 'B', 'C', 'D']);
});

test('holdOnly: B·C·D는 사지도 팔지도 않고, A는 입금으로 비중대로 산다', () => {
  const res = run({ settings: { holdOnly: ['DDD', 'AAA'] }, scenarios: [S('D')],
    deposits: [{ id: 'd', amount: 100, recordedAt: '2026-11-07T15:00:00Z' }] });
  const d = pick(res, 'D');
  assert.equal(trades(d, { ticker: 'DDD' }).length, 0);
  assert.deepEqual(d.months[0].candidates, ['BBB']);
  assert.deepEqual(trades(pick(res, 'A')).map((t) => t.ticker), ['AAA', 'DDD']);
});

test('derived: 만든 다음 거래일 S부터, S 전 거래일 장 마감 뒤 A에서 출발하고 S가 점검일이면 그날 결정하지 않는다', () => {
  const res = run({
    world: { end: '2027-01-29' },
    deposits: [{ id: 'd', amount: 600, recordedAt: '2026-11-07T15:00:00Z' }],
    scenarios: [S('B', undefined, { id: 'mid', createdAt: '2026-11-10T20:00:00Z' }), S('B', undefined, { id: 'eve', createdAt: '2026-11-30T20:00:00Z' })],
  });
  const a = pick(res, 'A'), mid = pick(res, 'mid'), eve = pick(res, 'eve');
  assert.equal(mid.started, '2026-11-10');
  assert.equal(mid.startValue, day(a, '2026-11-10').value);
  assert.ok(mid.trades.every((t) => t.date >= '2026-12-01'));
  assert.equal(mid.baselines.SPY[0].date, '2026-11-10');
  assert.equal(mid.months[0].checkDate, '2026-12-01');
  assert.equal(day(mid, '2026-11-30').deposits, 0);         // 출발 뒤 입금만 센다
  assert.equal(eve.started, '2026-11-30');
  assert.equal(eve.months[0].checkDate, '2027-01-04');      // S = 12-01 점검일이라 그날은 결정하지 않는다
  // 출발이 S 뒤로 미뤄져도 금지일은 S 하나 — 회복 다음 날이 점검일이면 그날 결정한다
  const late = pick(run({ world: { close: (t, d) => (t === 'AAA' && d >= '2026-11-04' && d <= '2026-11-27' ? null : undefined) },
    scenarios: [S('B', undefined, { id: 'late', createdAt: '2026-11-04T20:00:00Z' })] }), 'late');
  assert.equal(late.started, '2026-11-30');
  assert.equal(late.months[0].decisionDate, '2026-12-01');
  // 시작 스냅샷 경로에서도 S가 점검일이면 그날 결정하지 않는다
  const snap = pick(run({ snapshot: { ...SNAP, date: '2026-10-30' }, scenarios: [S('B', undefined, { id: 'snap', createdAt: '2026-10-30T22:00:00Z' })] }), 'snap');
  assert.equal(snap.months[0].checkDate, '2026-12-01');
  // 스냅샷 날보다 먼저 만든 시나리오(S가 첫 활동일보다 이르다)는 첫 활동일에 결정할 수 있다
  const early = pick(run({ snapshot: { ...SNAP, date: '2026-10-30' }, scenarios: [S('B', undefined, { id: 'early', createdAt: '2026-10-29T22:00:00Z' })] }), 'early');
  assert.equal(early.months[0].decisionDate, '2026-11-02');
  // 마지막 기록 날 저녁에 만든 시나리오는 그날 A 상태에서 바로 출발한다(S 전 거래일 상태를 이미 안다)
  const today = pick(run({ world: { end: '2026-11-06' }, scenarios: [S('B', undefined, { id: 't', createdAt: '2026-11-06T22:00:00Z' })] }), 't');
  assert.equal(today.started, '2026-11-06');
  const notYet = run({ scenarios: [S('B', undefined, { id: 'f', createdAt: '2027-01-05T20:00:00Z' })] });
  assert.equal(pick(notYet, 'f').waiting, 'notYet');
});

test('lastStage: 다 판 뒤 적정으로 내려가 다시 산 종목이 고평가가 되면 재발동', () => {
  const res = run({ world: { end: '2027-01-29', tier: (t, d) => (t === 'DDD' ? (d >= '2026-12-30' ? '고평가' : d >= '2026-11-27' ? '적정' : '고평가') : undefined) },
    scenarios: [S('D')] });
  const d = pick(res, 'D');
  assert.ok(trades(d, { ticker: 'DDD', side: 'buy' }).some((t) => t.date.startsWith('2026-12')));
  const jan = d.months.find((m) => m.checkDate === '2027-01-04');
  assert.deepEqual(jan.fires.map((f) => [f.ticker, f.prev, f.observed]), [['DDD', 'none', '고평가']]);   // 새로 보유하면 '없음'부터
});

test('lastStage: 고평가에서 새로 산 종목도 다음 점검일에 발동한다(사용자 정의)', () => {
  const c = pick(run({ snapshot: { date: '2026-10-16', holdings: {}, cash: 1000 },
    scenarios: [S('custom', { buyTiers: ['고평가'], sellFraction: 1 })] }), 'custom');
  assert.ok(trades(c, { ticker: 'DDD', side: 'buy' }).length > 0);
  assert.deepEqual(c.months[1].fires.map((f) => [f.ticker, f.prev, f.observed]), [['DDD', 'none', '고평가']]);
});

test('원칙 6 경계: 판정이 정확히 5거래일 묵으면 쓰고 6거래일이면 묵음', () => {
  const asOf = (n) => (t, d) => (t === 'BBB' && d === '2026-10-29' ? cal.sessions[cal.index(d) - n] : undefined);
  assert.deepEqual(pick(run({ world: { asOf: asOf(5) }, scenarios: [S('C')] }), 'C').months[0].candidates, ['BBB']);
  assert.deepEqual(pick(run({ world: { asOf: asOf(6) }, scenarios: [S('C')] }), 'C').months[0].candidates, []);
});

test('안전망 경계: 정확히 0.6배는 확인 필요, 0.61배는 정상', () => {
  const at = (x) => pick(run({ world: { close: (t, d) => (t === 'AAA' && d >= '2026-11-10' ? 100 * x : undefined) } }), 'A');
  assert.equal(day(at(0.6), '2026-11-10').value, null);
  near(day(at(0.61), '2026-11-10').value, 2610, 0.01);
});

test('사유 우선순위: 판정 이탈과 그날 기록 실패가 겹치면 지운다', () => {
  const b = pick(run({ world: { failed: ['2026-11-09'], tier: (t, d) => (t === 'AAA' && d === '2026-11-05' ? '고평가' : undefined) }, scenarios: [S('B')] }), 'B');
  assert.deepEqual(b.skips.filter((x) => x.date === '2026-11-09').map((x) => [x.ticker, x.reason, x.action]),
    [['AAA', 'tierOut', 'erased'], ['BBB', 'pipelineFailed', 'carried']]);
});

test('A 입금 배분은 정수 센트로(실수 비중 오차로 센트를 잃지 않는다)', () => {
  const a = pick(run({ world: { close: (t) => (t === 'AAA' || t === 'BBB' ? 1 : undefined) }, snapshot: { date: '2026-10-16', holdings: { AAA: 29, BBB: 21 }, cash: 0 },
    deposits: [{ id: 'd', amount: 1, recordedAt: '2026-11-07T15:00:00Z' }] }), 'A');
  assert.deepEqual(trades(a).map((t) => [t.ticker, t.amount]), [['AAA', 0.58], ['BBB', 0.42]]);
  assert.equal(a.cash, 0);
});

test('후보 수로 나눈 잔돈은 월 기록의 unallocated로 남는다', () => {
  const c = pick(run({ world: { close: (t) => (['AAA', 'BBB', 'CCC'].includes(t) ? 1 : undefined), tier: (t) => (t === 'DDD' ? undefined : '적정') },
    snapshot: { date: '2026-10-16', holdings: {}, cash: 1 }, scenarios: [S('custom', { buyTiers: ['적정'], splitWeeks: 1 })] }), 'custom');
  const m = c.months[0];
  assert.equal(m.unallocated, 0.01);
  assert.equal(m.summary.reduce((a, x) => a + x.notUsed, 0), 0);
  assert.deepEqual(nov(trades(c)).map((t) => t.amount), [0.33, 0.33, 0.33]);
});

test('지원하지 않는 기업 사건(events)이 오면 보유 시나리오는 사건일부터 멈춘다', () => {
  const recs = world();
  recs.find((r) => r.session === '2026-11-12').events = [{ ticker: 'AAA', kind: 'spinoff', date: '2026-11-10' }];
  const res = run({ records: recs, scenarios: [S('C')] });
  assert.deepEqual(pick(res, 'A').halted, { reason: 'corporateEvent', since: '2026-11-10', ticker: 'AAA' });
  assert.equal(day(pick(res, 'A'), '2026-11-10').value, null);
  assert.ok(day(pick(res, 'A'), '2026-11-09').value !== null);
});

test('기업 사건: 사건일 전날 보유했으면 그날 전량 팔았어도 멈추고, 아무도 보유 안 한 사건으로는 멈추지 않는다', () => {
  const r1 = world({ end: '2026-11-04' });
  r1.find((r) => r.session === '2026-11-04').events = [{ ticker: 'DDD', kind: 'spinoff', date: '2026-11-02' }];
  const d = pick(run({ records: r1, snapshot: { date: '2026-10-16', holdings: { DDD: 100 }, cash: 0 }, scenarios: [S('D', { splitWeeks: 1 })] }), 'D');
  assert.equal(trades(d, { side: 'sell' })[0].date, '2026-11-02');
  assert.equal(d.halted?.since, '2026-11-02');
  const r2 = world();
  r2.find((r) => r.session === '2026-11-05').events = [{ ticker: 'AAA', kind: 'spinoff', date: '2026-10-20' }];
  const c = pick(run({ records: r2, snapshot: { date: '2026-10-16', holdings: {}, cash: 1000 }, scenarios: [S('custom', { buyTiers: ['적정'] })] }), 'custom');
  assert.ok(trades(c, { ticker: 'AAA' }).length > 0);
  assert.equal(c.halted, null);
});

test('늦은 분할 두 건: 멈춘 날은 더 이른 효력일로 당긴다', () => {
  const a = pick(run({ world: {
    close: (t, d) => (t === 'AAA' && d >= '2026-11-10' ? 100 / 1.5 : t === 'DDD' && d >= '2026-11-02' ? 10 / 1.5 : undefined),
    splits: { '2026-11-18': [sp('AAA', '2026-11-10', 1.5)], '2026-11-20': [sp('DDD', '2026-11-02', 1.5)] } } }), 'A');
  assert.equal(a.halted.since, '2026-11-02');
  assert.equal(day(a, '2026-11-05').value, null);
});

test('늦은 분할: 출발 전 미확정 날의 보유는 세지 않는다(출발이 도착 뒤면 멈추지 않음)', () => {
  const a = pick(run({ world: {
    close: (t, d) => (t === 'AAA' && d <= '2026-10-27' ? null : t === 'DDD' && d >= '2026-10-19' ? 10 / 1.5 : undefined),
    splits: { '2026-10-23': [sp('DDD', '2026-10-19', 1.5)] } } }), 'A');
  assert.equal(a.halted, null);
  assert.equal(a.started, '2026-10-28');
  near(a.startValue, 3000, 0.01);
});

test('기준선도 늦은 분할 두 건이면 더 이른 효력일부터 평가 불가', () => {
  const a = pick(run({ world: {
    close: (t, d) => (t === 'SPY' ? (d >= '2026-11-10' ? 500 / 2.25 : d >= '2026-11-02' ? 500 / 1.5 : undefined) : undefined),
    splits: { '2026-11-18': [sp('SPY', '2026-11-10', 1.5)], '2026-11-20': [sp('SPY', '2026-11-02', 1.5)] } } }), 'A');
  const spy = a.baselines.SPY;
  assert.deepEqual(a.baselineHalts.SPY, { reason: 'splitDelay', since: '2026-11-02' });
  assert.deepEqual(JSON.parse(JSON.stringify(a)).baselineHalts.SPY.since, '2026-11-02');   // JSON으로도 남는다
  assert.equal(spy.find((x) => x.date === '2026-11-05').value, null);
  assert.ok(spy.find((x) => x.date === '2026-10-30').value !== null);
});

test('출발일 전에 효력이 난 늦은 분할로 멈추면 출발하지 않은 것으로 보고한다', () => {
  const a = pick(run({ world: {
    close: (t, d) => (t === 'AAA' && d <= '2026-10-20' ? null : t === 'DDD' && d >= '2026-10-19' ? 10 / 1.5 : undefined),
    splits: { '2026-10-26': [sp('DDD', '2026-10-19', 1.5)] } } }), 'A');
  assert.deepEqual([a.started, a.startValue, a.waiting], [null, null, 'splitDelay']);
  assert.deepEqual(a.baselines, {});
});

test('비례 축소도 정수로 내림한다(부동소수점 오차로 센트를 잃지 않는다)', () => {
  const b = pick(run({ world: { close: (t) => (t === 'AAA' || t === 'BBB' ? 1 : undefined) }, snapshot: { date: '2026-10-16', holdings: {}, cash: 1 },
    scenarios: [S('B', { splitWeeks: 1, cashReserve: 0.42 })] }), 'B');
  assert.deepEqual(trades(b, { date: '2026-11-02' }).map((t) => t.amount), [0.29, 0.29]);
});

test('유보율·매도 비율은 정수 백만분율로 곱한다(0.29 × 100센트 = 29센트)', () => {
  const b = pick(run({ world: { close: (t) => (t === 'AAA' || t === 'BBB' ? 1 : undefined) }, snapshot: { date: '2026-10-16', holdings: {}, cash: 1 },
    scenarios: [S('B', { splitWeeks: 1, cashReserve: 0.29 })] }), 'B');
  assert.deepEqual(trades(b, { date: '2026-11-02' }).map((t) => t.amount), [0.35, 0.35]);
  const c = pick(run({ snapshot: { date: '2026-10-16', holdings: { DDD: 100 }, cash: 0 }, scenarios: [S('custom', { buyTiers: ['적정'], sellFraction: 0.29, splitWeeks: 1 })] }), 'custom');
  assert.equal(trades(c, { side: 'sell' })[0].shares, 29);   // 실수 곱이면 28.999999
});

test('분할 뒤 남은 매도 회차도 반올림 잔량을 마지막 회차에 더한다(역분할)', () => {
  const d = pick(run({ snapshot: { date: '2026-10-16', holdings: { DDD: 1 }, cash: 0 },
    world: { close: (t, x) => (t === 'DDD' ? (x >= '2026-11-03' ? 30000 : 10000) : undefined), splits: { '2026-11-03': [sp('DDD', '2026-11-03', 1 / 3)] } },
    scenarios: [S('D')] }), 'D');
  assert.deepEqual(nov(trades(d, { ticker: 'DDD', side: 'sell' })).map((t) => t.shares), [0.25, 0.083333, 0.083333, 0.083334]);
  assert.equal(d.holdings.DDD, undefined);
});

test('기준선도 그 ETF의 지원하지 않는 기업 사건이면 사건일부터 멈춘다', () => {
  const recs = world();
  recs.find((r) => r.session === '2026-11-12').events = [{ ticker: 'SPY', kind: 'spinoff', date: '2026-11-10' }];
  const spy = pick(run({ records: recs }), 'A').baselines.SPY;
  assert.deepEqual(pick(run({ records: recs }), 'A').baselineHalts.SPY, { reason: 'corporateEvent', since: '2026-11-10' });
  assert.equal(spy.find((x) => x.date === '2026-11-10').value, null);
  assert.ok(spy.find((x) => x.date === '2026-11-09').value !== null);
  assert.ok(pick(run({ records: recs }), 'A').baselines.RSP.at(-1).value !== null);
});

test('늦은 분할: 효력일에 전량 매도했으면(분할 전 수량으로 체결) 효력일부터 멈춘다', () => {
  const d = pick(run({ snapshot: { date: '2026-10-16', holdings: { DDD: 100 }, cash: 0 },
    world: { end: '2026-11-04', close: (t, x) => (t === 'DDD' && x >= '2026-11-02' ? 10 / 1.5 : undefined), splits: { '2026-11-04': [sp('DDD', '2026-11-02', 1.5)] } },
    scenarios: [S('D', { splitWeeks: 1 })] }), 'D');
  assert.equal(trades(d, { side: 'sell' })[0].shares, 100);
  assert.equal(d.halted?.since, '2026-11-02');
  assert.equal(day(d, '2026-11-04').value, null);
});

test('늦은 분할: 효력일 뒤에 처음 산 종목에는 곱하지 않고 멈추지도 않는다', () => {
  const res = run({ world: { end: '2026-12-31',
    close: (t, x) => (t === 'BBB' && x >= '2026-11-10' ? 25 : undefined), splits: { '2026-12-10': [sp('BBB', '2026-11-10', 2)] },
    tier: (t, x) => (t === 'BBB' ? (x >= '2026-11-25' ? '저평가' : '적정') : undefined) },   // C는 12월에야 BBB를 처음 산다
  scenarios: [S('C'), S('C', undefined, { id: 'mid', createdAt: '2026-11-19T20:00:00Z' })] });
  const c = pick(res, 'C'), mid = pick(res, 'mid');
  const bought = trades(c, { ticker: 'BBB', side: 'buy' }).reduce((a, t) => a + t.shares, 0);
  assert.ok(bought > 0 && trades(c, { ticker: 'BBB' }).every((t) => t.date >= '2026-12-01'));
  near(c.holdings.BBB, bought);
  assert.equal(c.halted, null);
  assert.deepEqual(c.splitLog.find((x) => x.id === 'BBB:2026-11-10'), { id: 'BBB:2026-11-10', date: '2026-12-10', action: 'ignored', why: 'notHeldAtEffective' });
  assert.equal(mid.started, '2026-11-19');
  assert.equal(mid.halted, null);
});

test('늦은 분할: 그 사이 다른 분할이 있어도 효력일 전날 보유 여부로 판단한다', () => {
  // A: 11-02 효력 1.25배가 늦게 오는데 11-03 입금 매수와 11-10 정상 역분할이 끼었다 → 효력일에 보유했고 매매가 있었으니 멈춘다
  const a = pick(run({ snapshot: { date: '2026-10-16', holdings: { AAA: 10 }, cash: 0 },
    world: { end: '2026-11-12', close: (t, d) => (t === 'AAA' ? (d >= '2026-11-10' ? 160 : d >= '2026-11-02' ? 80 : undefined) : undefined),
      splits: { '2026-11-10': [sp('AAA', '2026-11-10', 0.5)], '2026-11-12': [sp('AAA', '2026-11-02', 1.25)] } },
    deposits: [{ id: 'd', amount: 1000, recordedAt: '2026-11-02T22:00:00Z' }] }), 'A');
  assert.equal(a.halted?.since, '2026-11-02');
  // C: 12월에 처음 산 BBB에 12-09 정상 분할이 끼고 11-10 효력 늦은 분할이 온다 → 효력일엔 0주였으니 무시
  const c = pick(run({ world: { end: '2026-12-10',
    close: (t, d) => (t === 'BBB' ? (d >= '2026-12-09' ? 20 : d >= '2026-11-10' ? 40 : undefined) : undefined),
    tier: (t, d) => (t === 'BBB' ? (d >= '2026-11-25' ? '저평가' : '적정') : undefined),
    splits: { '2026-12-09': [sp('BBB', '2026-12-09', 2)], '2026-12-10': [sp('BBB', '2026-11-10', 1.25)] } }, scenarios: [S('C')] }), 'C');
  const bought = trades(c, { ticker: 'BBB', side: 'buy' }).reduce((x, t) => x + t.shares, 0);
  near(c.holdings.BBB, bought * 2);
  assert.equal(c.halted, null);
});

test('늦은 분할: 효력일 뒤에 사서 판 종목도 무시한다(매도가 있어도)', () => {
  const c = pick(run({ snapshot: { date: '2026-10-16', holdings: {}, cash: 1000 }, world: { end: '2026-12-10',
    tier: (t, d) => (t === 'AAA' && d >= '2026-11-25' ? '고평가' : undefined), splits: { '2026-12-10': [sp('AAA', '2026-10-20', 1.5)] } },
  scenarios: [S('custom', { buyTiers: ['적정'], sellFraction: 0.5 })] }), 'custom');
  assert.ok(trades(c, { ticker: 'AAA', side: 'sell' }).length > 0);
  assert.equal(c.halted, null);
  const net = c.trades.filter((t) => t.ticker === 'AAA').reduce((x, t) => x + (t.side === 'buy' ? t.shares : -t.shares), 0);
  near(c.holdings.AAA, net);
});

test('늦은 분할: 그 사이 평가가 모두 미확정이었으면 멈추지 않는다', () => {
  const a = pick(run({ world: {
    close: (t, d) => (t === 'AAA' && d >= '2026-11-10' ? 100 / 1.5 : t === 'DDD' && d >= '2026-11-10' && d <= '2026-11-17' ? null : undefined),
    splits: { '2026-11-18': [sp('AAA', '2026-11-10', 1.5)] } } }), 'A');
  assert.equal(a.halted, null);
  near(day(a, '2026-11-18').value, 3000, 0.01);
});

test('파생은 A가 이미 본 분할 id를 물려받는다(같은 id가 다시 실려도 한 번만)', () => {
  const l = pick(run({ world: {
    close: (t, d) => (t === 'DDD' && d >= '2026-11-04' ? 5 : undefined),
    splits: { '2026-11-04': [sp('DDD', '2026-11-04', 2)], '2026-11-20': [sp('DDD', '2026-11-04', 2)] } },
  scenarios: [S('B', undefined, { id: 'late', createdAt: '2026-11-10T20:00:00Z' })] }), 'late');
  assert.equal(l.holdings.DDD, 200);
  assert.deepEqual(l.splitLog, []);
});

test('출발 전에 지나간 점검일은 사건(decisionDropped, notStarted)으로 남긴다', () => {
  const b = pick(run({ world: { close: (t, d) => (t === 'AAA' && d <= '2026-11-03' ? null : undefined) }, scenarios: [S('B')] }), 'B');
  assert.equal(b.started, '2026-11-04');
  assert.ok(b.events.some((e) => e.kind === 'decisionDropped' && e.checkDate === '2026-11-02' && e.reason === 'notStarted'));
  // 출발일이 점검일이어도 그날은 결정하지 않고 사건을 남긴다
  const s2 = pick(run({ world: { close: (t, d) => (t === 'AAA' && d <= '2026-10-30' ? null : undefined) }, scenarios: [S('B')] }), 'B');
  assert.equal(s2.started, '2026-11-02');
  assert.ok(s2.events.some((e) => e.checkDate === '2026-11-02' && e.reason === 'notStarted'));
  // 파생이 A를 기다리는 동안 지나간 점검일도 남긴다
  const late = pick(run({ world: { end: '2026-11-06', close: (t, d) => (t === 'AAA' && d >= '2026-10-22' && d <= '2026-11-03' ? null : undefined) },
    scenarios: [S('B', undefined, { id: 'late', createdAt: '2026-10-22T20:00:00Z' })] }), 'late');
  assert.equal(late.started, '2026-11-04');
  assert.deepEqual(late.events.filter((e) => e.kind === 'decisionDropped'), [{ date: '2026-11-02', kind: 'decisionDropped', checkDate: '2026-11-02', reason: 'notStarted' }]);
});

test('입력 방어: 소수 6자리 넘는 비율, 효력일이 기록보다 뒤인 분할·사건은 거부, 시작일 전 사건은 무시', () => {
  assert.throws(() => run({ scenarios: [S('custom', { buyTiers: ['적정'], sellFraction: 0.1234567 })] }), /소수 6자리/);
  assert.throws(() => run({ world: { splits: { '2026-11-10': [sp('AAA', '2026-11-12', 2)] } } }), /효력일이 기록 날짜보다 뒤/);
  const recs = world();
  recs.find((r) => r.session === '2026-11-05').events = [{ ticker: 'AAA', kind: 'spinoff', date: '2026-10-15' }, { ticker: 'SPY', kind: 'spinoff', date: '2026-10-15' }];
  const a = pick(run({ records: recs }), 'A');
  assert.equal(a.halted, null);
  assert.deepEqual(a.baselineHalts, {});
});

test('멈추면 그달 남은 회차는 예정이 아니라 쓰지 않은 몫으로 닫는다', () => {
  const b = pick(run({ world: { close: (t, d) => (t === 'AAA' && d >= '2026-11-10' ? 100 / 1.5 : undefined),
    splits: { '2026-11-12': [sp('AAA', '2026-11-10', 1.5)] } }, scenarios: [S('B')] }), 'B');
  assert.equal(b.months[0].closed, 'halted');
  assert.deepEqual(b.months[0].summary.map((x) => [x.ticker, x.notUsed, x.scheduled]), [['AAA', 250, 0], ['BBB', 250, 0]]);
});

test('매수 수량 내림으로 남는 금액은 현금으로 남는다', () => {
  const c = pick(run({ world: { close: (t) => (t === 'AAA' ? 600000 : undefined) }, snapshot: { date: '2026-10-16', holdings: {}, cash: 1 },
    scenarios: [S('custom', { buyTiers: ['적정'], splitWeeks: 1 })] }), 'custom');
  const t = trades(c, { ticker: 'AAA' })[0];
  assert.deepEqual([t.shares, t.amount], [0.000001, 0.6]);
  near(day(c, '2026-11-02').value, 1, 1e-9);
});

test('달력 마지막 해 12월도 재생한다', () => {
  const b = pick(run({ world: { end: '2027-12-10' }, scenarios: [S('B')] }), 'B');
  const dec = b.months.find((m) => m.checkDate === '2027-12-01');
  assert.deepEqual(dec.rounds.map((r) => [r.date, r.dropped]), [['2027-12-01', false], ['2027-12-08', false], ['2027-12-15', false], ['2027-12-22', false]]);
});

test('engine version과 표시', () => {
  const res = run({ scenarios: [{ ...S('custom', { buyTiers: ['고평가'], sellFraction: 0 }), engineVersion: 'old' }, S('B')] });
  assert.equal(pick(res, 'custom').engineMismatch, true);
  assert.deepEqual(pick(res, 'custom').notes, ['offPrinciple']);
  assert.deepEqual(pick(res, 'B').notes, ['provisionalPrinciple', 'noPrinciple7']);
  assert.throws(() => run({ scenarios: [S('C', { sellFraction: 0.5 })] }), /바꿀 수 없는 값/);
  assert.throws(() => run({ scenarios: [S('custom', { buyTiers: ['적정'], splitWeeks: 5 })] }), /splitWeeks/);
  assert.throws(() => run({ scenarios: [S('B', { cashReserve: NaN })] }), /cashReserve/);
  assert.throws(() => run({ scenarios: [S('B', { sellFraction: NaN })] }), /sellFraction/);
});

test('결정적: 기록·시나리오·보유 순서를 섞어도 결과가 같다', () => {
  const recs = world({ tier: (t, d) => (t === 'AAA' && d === '2026-11-05' ? '고평가' : undefined) });
  const scen = [S('B'), S('D'), S('custom', { buyTiers: ['적정', '저평가'], sellFraction: 0.3, splitWeeks: 3, cashReserve: 0.1 })];
  const deposits = [{ id: 'd', amount: 777.77, recordedAt: '2026-11-07T15:00:00Z' }];
  const one = replay({ records: recs, snapshot: SNAP, deposits, scenarios: scen });
  const two = replay({ records: [...recs].reverse(), snapshot: { ...SNAP, holdings: { DDD: 100, AAA: 10 } }, deposits, scenarios: [...scen].reverse() });
  const key = (r) => JSON.stringify(r.scenarios.slice().sort((x, y) => (x.id < y.id ? -1 : 1)));
  assert.equal(key(one), key(two));
});

test('오류 문구에 개인 값을 넣지 않는다', () => {
  try { run({ snapshot: { ...SNAP, holdings: { AAA: -12345.678 } } }); assert.fail('no throw'); } catch (e) {
    assert.ok(!String(e.message).includes('12345') && !String(e.message).includes('AAA'), e.message);
  }
});

test('화면용 도우미: 입금 반영일·취소 마감, 거래일 여부', () => {
  assert.deepEqual(depositTiming('2026-11-07T15:00:00Z'), { day: '2026-11-09', cancelBefore: Date.parse('2026-11-09T14:30:00Z') });
  assert.equal(depositTiming('2026-11-16T14:31:00Z').day, '2026-11-17');
  assert.equal(depositTiming('bad').day, null);
  assert.equal(isTradingDay('2026-11-26'), false);
  assert.equal(isTradingDay('2026-11-27'), true);
  assert.equal(isTradingDay('2030-01-02'), false);
});

// ---- 내 실제 계좌 줄(preview-only-portfolio-actual.js, 2026-10-21) ----
import { actualAccount, attachActual } from '../../preview-only-portfolio-actual.js';
import { toEngineInput } from '../../preview-only-portfolio-strategy.js';
import { monthView } from '../../preview-only-portfolio-home.js';

test('실제 계좌: 스냅샷 출발, 매매(휴장일은 다음 거래일·같은 날 매수 먼저), 입금·늦은 취소, 분할, 가격 없음, TWR·SPY 대비', () => {
  const recs = world({ end: '2026-10-30', close: (t, d) => (t === 'AAA' && d >= '2026-10-23' ? 110 : t === 'BBB' && d >= '2026-10-28' ? 25 : undefined),
    splits: { '2026-10-28': [{ id: 'BBB-2026-10-28', ticker: 'BBB', effectiveDate: '2026-10-28', ratio: 2 }],
      '2026-10-20': [{ id: 'AAA-2026-10-16', ticker: 'AAA', effectiveDate: '2026-10-16', ratio: 3 }] } });   // 시작일 효력 분할은 스냅샷에 이미 있음 → 무시
  const deposits = {
    d1: { amount: 500, recordedAt: '2026-10-21T20:00:00Z' },            // 10-22 반영
    d2: { amount: 300, recordedAt: '2026-10-26T20:00:00Z' },            // 10-27 반영, 취소는 반영 뒤라 무시
    c2: { cancels: 'd2', recordedAt: '2026-10-27T15:00:00Z' },
    d3: { amount: 999, recordedAt: '2026-10-21T20:30:00Z' }, c3: { cancels: 'd3', recordedAt: '2026-10-21T21:00:00Z' },   // 반영 전 취소
  };
  const tr = {
    t0: { date: '2026-10-16', ticker: 'AAA', side: 'buy', qty: 99, price: 1, recordedAt: '2026-10-16T20:00:00Z' },      // 시작일 당일 → 스냅샷에 이미 있음
    t1: { date: '2026-10-25', ticker: 'BBB', side: 'sell', qty: 4, price: 50, recordedAt: '2026-10-25T19:00:00Z' },     // 일요일 → 10-26, 먼저 적었어도 매수 뒤
    t2: { date: '2026-10-25', ticker: 'BBB', side: 'buy', qty: 4, price: 50, recordedAt: '2026-10-25T20:00:00Z' },
    t3: { date: '2026-10-26', ticker: 'BBB', side: 'buy', qty: 2, price: 50, recordedAt: '2026-10-26T20:00:00Z' },
    t4: { date: '2026-10-27', ticker: 'ZZZ', side: 'buy', qty: 1, price: 10, recordedAt: '2026-10-27T20:00:00Z' },      // 가격 없는 종목
    x4: { cancels: 't4', recordedAt: '2026-10-27T21:00:00Z' },
  };
  const A = replay({ records: recs, snapshot: SNAP, deposits: toEngineInput({ snapshot: SNAP, deposits }, recs).deposits }).scenarios[0];
  const r = actualAccount({ records: recs, snapshot: SNAP, deposits, trades: tr, baselines: A.baselines, baseStart: A.started, baseStartValue: A.startValue });
  assert.equal(r.started, '2026-10-16');
  assert.equal(day(r, '2026-10-16').value, 3000);
  assert.equal(day(r, '2026-10-22').value, 3500);
  assert.equal(day(r, '2026-10-23').value, 3600);                       // AAA 110
  assert.deepEqual(r.trades.map((t) => [t.date, t.ticker, t.side]), [['2026-10-26', 'BBB', 'buy'], ['2026-10-26', 'BBB', 'sell'], ['2026-10-26', 'BBB', 'buy']]);
  assert.equal(day(r, '2026-10-27').value, 3600 - 100 + 100 + 300);     // 2주 100달러 매수, 늦은 취소는 무시되어 300 반영
  assert.equal(r.holdings.BBB, 4);                                       // 10-28 분할 2배
  assert.equal(day(r, '2026-10-28').value, 1100 + 1000 + 4 * 25 + 1000 + 500 - 100 + 300);
  assert.equal(day(r, '2026-10-27').deposits, 800);
  assert.equal(day(r, '2026-10-16').twr, 0);
  near(day(r, '2026-10-23').twr, 3600 / 3500 - 1);
  near(day(r, '2026-10-23').vs.SPY, (day(r, '2026-10-23').twr - 0) * 100);   // SPY는 그대로라 기준선 TWR 0
  // SPY가 움직이면 같은 날짜의 기준선 TWR을 뺀다
  const recs2 = world({ end: '2026-10-23', close: (t, d) => (t === 'SPY' && d >= '2026-10-22' ? 550 : undefined) });
  const A2 = replay({ records: recs2, snapshot: SNAP }).scenarios[0];
  const r4 = actualAccount({ records: recs2, snapshot: SNAP, deposits: {}, trades: {}, baselines: A2.baselines, baseStart: A2.started, baseStartValue: A2.startValue });
  near(day(r4, '2026-10-22').vs.SPY, (0 - 0.1) * 100);
  near(day(r4, '2026-10-19').vs.SPY, 0);
  // 출발일이 같아도 출발 평가액이 다르면 A의 기준선을 쓰지 않는다(dr r2)
  const r5 = actualAccount({ records: recs2, snapshot: SNAP, deposits: {}, trades: {}, baselines: A2.baselines, baseStart: A2.started, baseStartValue: A2.startValue + 1 });
  assert.equal(day(r5, '2026-10-22').vs.SPY, null);
  assert.match(r5.warnings[0], /출발 평가액/);
  const r6 = actualAccount({ records: recs2, snapshot: SNAP, deposits: {}, trades: {}, baselines: A2.baselines, baseStart: '2026-10-19', baseStartValue: A2.startValue });
  assert.equal(day(r6, '2026-10-22').vs.SPY, null);
  assert.match(r6.warnings[0], /출발일/);
  // 가격 없는 종목을 사면 그날부터 미확정
  const r2 = actualAccount({ records: recs, snapshot: SNAP, deposits: {}, trades: { t4: tr.t4 }, baselines: A.baselines, baseStart: A.started, baseStartValue: A.startValue });
  assert.equal(day(r2, '2026-10-27').value, null);
  assert.deepEqual(day(r2, '2026-10-27').why, ['noPrice:ZZZ']);
  assert.equal(day(r2, '2026-10-26').value, 3100);                     // 입금 없음: 3000 + AAA 상승 100
  // 보유보다 많이 판 기록은 가진 만큼만(현금도 그만큼만)
  const r3 = actualAccount({ records: recs, snapshot: SNAP, deposits: {}, trades: { s: { date: '2026-10-21', ticker: 'DDD', side: 'sell', qty: 150, price: 10, recordedAt: 'x' } }, baselines: A.baselines, baseStart: A.started, baseStartValue: A.startValue });
  assert.equal(r3.holdings.DDD, undefined);
  assert.equal(r3.cash, 2000);
  assert.equal(r3.warnings.length, 1);
  assert.deepEqual(r3.trades.map((t) => [t.shares, t.amount, t.requested]), [[100, 1000, 150]]);   // 반영된 수량·대금으로 기록
});

test('실제 계좌: 분할은 기록이 늦어도 효력일에 선적용(기록 전 급변 날은 안전망으로 미확정), 대금은 체결마다 센트, 음수 현금 경고', () => {
  // AAA 10주 보유. 10-20 효력 2:1 분할 기록이 10-23에야 실린다. 10-21에 분할 뒤 가격(50)으로 10주를 더 샀고, 10-22에 20주를 팔았다.
  // 분할은 효력일(10-20) 장 시작 전에 적용한다 — 증권사처럼 그 뒤 매매는 분할 뒤 수량이다.
  const recs = world({ end: '2026-10-27', close: (t, d) => (t === 'AAA' && d >= '2026-10-20' ? 50 : undefined),
    splits: { '2026-10-23': [{ id: 'AAA-2026-10-20', ticker: 'AAA', effectiveDate: '2026-10-20', ratio: 2 }],
      '2026-10-26': [{ id: 'AAA-2026-10-20', ticker: 'AAA', effectiveDate: '2026-10-20', ratio: 2 }] } });   // 같은 분할이 두 기록에 실려도 한 번
  const tr = { b: { date: '2026-10-21', ticker: 'AAA', side: 'buy', qty: 10, price: 50, recordedAt: 'x' },
    s: { date: '2026-10-22', ticker: 'AAA', side: 'sell', qty: 20, price: 50, recordedAt: 'y' } };
  const r = actualAccount({ records: recs, snapshot: SNAP, deposits: {}, trades: tr, baselines: {}, baseStart: null });
  assert.equal(r.holdings.AAA, 10);                                   // 10 × 2 + 10 − 20
  assert.deepEqual(r.warnings.filter((w) => /보유/.test(w)), []);   // 보유 초과 경고 없음
  assert.equal(r.cash, 1000 - 500 + 1000);
  assert.equal(day(r, '2026-10-26').value, 10 * 50 + 1000 + 1500);
  // 기록이 오기 전 가격 급변 날은 엔진의 분할 안전망이 미확정으로 둔다
  assert.equal(day(r, '2026-10-21').value, null);
  // 소수 주식 대금은 체결마다 센트로(0.001주 × $6 = $0.006 → $0.01씩)
  const r2 = actualAccount({ records: recs, snapshot: { date: '2026-10-16', holdings: {}, cash: 1 }, deposits: {},
    trades: { a: { date: '2026-10-19', ticker: 'BBB', side: 'buy', qty: 0.001, price: 6, recordedAt: '1' }, b: { date: '2026-10-19', ticker: 'BBB', side: 'buy', qty: 0.001, price: 6, recordedAt: '2' } },
    baselines: {}, baseStart: null });
  assert.equal(r2.cash, 0.98);
  assert.deepEqual(r2.trades.map((t) => t.amount), [0.01, 0.01]);
  // 현금이 음수가 되면 경고
  const r3 = actualAccount({ records: recs, snapshot: { date: '2026-10-16', holdings: {}, cash: 10 }, deposits: {},
    trades: { a: { date: '2026-10-19', ticker: 'BBB', side: 'buy', qty: 1, price: 50, recordedAt: '1' } }, baselines: {}, baseStart: null });
  assert.equal(r3.cash, -40);
  assert.ok(r3.warnings.some((w) => /음수/.test(w)));
});

test('attachActual: 숨은 원칙 시나리오는 result.plan으로, 실제 계좌는 맨 앞(그다음 A)', () => {
  const recs = world({ end: '2026-11-10' });
  const bundle = { snapshot: { ...SNAP, holdOnly: [], createdAt: '2026-10-16T22:00:00Z' }, deposits: {}, scenarios: { s1: { name: '저평가만', strategy: 'C', params: { splitWeeks: 4, cashReserve: 0 }, createdAt: '2026-10-20T15:00:00Z', engineVersion: ENGINE_VERSION } } };
  const res = attachActual(replay(toEngineInput(bundle, recs, { plan: true })), { records: recs, bundle, trades: {} });
  assert.deepEqual(res.scenarios.map((s) => s.id), ['REAL', 'A', 's1']);
  assert.equal(res.plan.id, '__plan');
  assert.equal(res.plan.started, '2026-10-16');
  assert.equal(res.plan.months.length > 0, true);
  // 매매·입금이 없으면 실제 계좌 = A(그대로 보유)
  assert.deepEqual(res.scenarios[1].days.map((x) => x.value), res.scenarios[0].days.map((x) => x.value));
  // 소수 주식이 반 센트 경계에 걸려도 매매·입금이 없으면 A와 같은 값·같은 출발 평가액(기준선 대비 유지)
  const snapF = { date: '2026-10-16', holdings: { DDD: 1.0005 }, cash: 0 };
  const bF = { snapshot: { ...snapF, holdOnly: [], createdAt: '2026-10-16T22:00:00Z' }, deposits: {}, scenarios: {} };
  const resF = attachActual(replay(toEngineInput(bF, recs, { plan: true })), { records: recs, bundle: bF, trades: {} });
  assert.equal(resF.scenarios[1].startValue, resF.scenarios[0].startValue);
  assert.deepEqual(resF.scenarios[0].warnings, []);   // 실제 계좌(맨 앞)
  // 여러 종목을 스냅샷 순서와 다르게 넣어도 엔진(티커순)과 같은 합(0.1+0.1+4.3 ≠ 4.3+0.1+0.1)
  const recsG = world({ end: '2026-10-20', close: (t) => (t === 'AAA' || t === 'BBB' ? 1 : t === 'CCC' ? 43 : undefined) });
  const snapG = { date: '2026-10-16', holdings: { CCC: 0.001, BBB: 0.001, AAA: 0.001 }, cash: 1000 };
  const bG = { snapshot: { ...snapG, holdOnly: [], createdAt: '2026-10-16T22:00:00Z' }, deposits: {}, scenarios: {} };
  const resG = attachActual(replay(toEngineInput(bG, recsG, { plan: true })), { records: recsG, bundle: bG, trades: {} });
  assert.equal(resG.scenarios[1].startValue, resG.scenarios[0].startValue);
  assert.deepEqual(resG.scenarios[0].warnings, []);
  // 예전 B가 남아 있어도 이번 달 운용은 숨은 원칙을 쓴다
  const withB = { ...bundle, scenarios: { ...bundle.scenarios, b0: { name: '옛 원칙', strategy: 'B', params: { sellFraction: 0, splitWeeks: 2, cashReserve: 0.1 }, createdAt: '2026-10-17T15:00:00Z', engineVersion: ENGINE_VERSION } } };
  const resB = attachActual(replay(toEngineInput(withB, recs, { plan: true })), { records: recs, bundle: withB, trades: {} });
  assert.equal(monthView(resB, '2026-11-10').scenario.id, '__plan');
  // 원칙 시나리오가 없으면 이번 달 운용은 실제 계좌가 아니라 다른 모의 시나리오를 쓴다
  assert.equal(monthView({ ...res, plan: null }, '2026-11-10').scenario.id, 's1');
});

test('E(ETF 섞기): 출발일 종가에 주식을 팔아 고른 ETF에 똑같이 나누고, 현금은 그대로, 그 뒤 매매 없음', () => {
  const r = run({ scenarios: [S('E', { etfShare: 1, etfs: ['SPY', 'RSP', 'QQQ'] })] });
  const e = pick(r, 'E');
  assert.equal(e.started, '2026-10-16');
  assert.deepEqual(trades(e, { side: 'sell' }).map((t) => [t.ticker, t.shares, t.kind]), [['AAA', 10, 'etf'], ['DDD', 100, 'etf']]);
  const buys = trades(e, { side: 'buy' });
  assert.deepEqual(buys.map((t) => [t.date, t.ticker, t.kind]), [['2026-10-16', 'QQQ', 'etf'], ['2026-10-16', 'RSP', 'etf'], ['2026-10-16', 'SPY', 'etf']]);
  for (const b of buys) assert.ok(b.amount <= 666.66 + 1e-9 && b.amount > 666.6, String(b.amount));
  assert.deepEqual(Object.keys(e.holdings), ['QQQ', 'RSP', 'SPY']);
  // 센트까지 정확히: 대금 200,000센트 ÷ 3 = 66,666센트씩(남는 2센트는 현금), 종가가 1센트 단위라 대금 = 배정액
  assert.deepEqual(buys.map((b) => b.amount), [666.66, 666.66, 666.66]);
  assert.equal(e.cash, 1000.02);
  assert.equal(e.startValue, 3000);
  assert.equal(day(e, '2026-10-16').value, 3000);
  assert.equal(e.trades.length, 5);   // 그 뒤로는 사고팔지 않는다
});

test('E: 일부만 바꾸면 남은 주식은 그대로 들고, 이미 가진 고른 ETF는 팔지 않는다', () => {
  const snap = { date: '2026-10-16', holdings: { AAA: 10, DDD: 100, SPY: 1 }, cash: 0 };
  const e = pick(run({ snapshot: snap, scenarios: [S('E', { etfShare: 0.5, etfs: ['SPY'] })] }), 'E');
  assert.deepEqual(e.holdings, { AAA: 5, DDD: 50, SPY: 3 });
  assert.equal(trades(e, { side: 'sell', ticker: 'SPY' }).length, 0);
  // 기본값은 100%·세 ETF
  const d = pick(run({ scenarios: [S('E', {})] }), 'E');
  assert.deepEqual(Object.keys(d.holdings), ['QQQ', 'RSP', 'SPY']);
});

test('E: 입금은 출발 때 현금 비중만큼 현금으로 두고 나머지를 비중대로 산다', () => {
  const e = pick(run({ scenarios: [S('E', { etfShare: 1, etfs: ['SPY', 'RSP', 'QQQ'] })], deposits: [{ id: 'd1', amount: 300, recordedAt: '2026-11-02T15:00:00Z' }] }), 'E');
  const dep = trades(e, { kind: 'deposit' });
  assert.deepEqual(dep.map((t) => t.date), ['2026-11-03', '2026-11-03', '2026-11-03']);
  const spent = dep.reduce((a, t) => a + t.amount, 0);
  assert.ok(spent > 199.9 && spent <= 200, String(spent));   // 300 × (1 − 1000/3000)
});

test('E: 현금 없이 SPY 하나로 다 바꾸면 SPY 기준선과 같이 움직인다', () => {
  const close = (t, d) => (t === 'SPY' ? 500 * (1 + cal.index(d) / 1000) : t === 'AAA' ? 100 * (1 - cal.index(d) / 2000) : undefined);
  const snap = { date: '2026-10-16', holdings: { AAA: 30 }, cash: 0 };
  const e = pick(run({ world: { close }, snapshot: snap, scenarios: [S('E', { etfShare: 1, etfs: ['SPY'] })] }), 'E');
  const last = e.days.at(-1);
  assert.ok(Math.abs(last.vs.SPY) < 0.01, String(last.vs.SPY));
});

test('E: 출발일에 ETF 가격이 없으면 그 몫은 현금으로 두었다가 가격이 돌아온 날 산다, 잘못된 값은 거부', () => {
  const close = (t, d) => (t === 'QQQ' && d <= '2026-11-04' ? null : undefined);
  const dep = [{ id: 'd1', amount: 300, recordedAt: '2026-11-02T15:00:00Z' }];   // 11-03 반영 — QQQ는 아직 가격 없음
  const e = pick(run({ world: { close }, deposits: dep, scenarios: [S('E', { etfShare: 1, etfs: ['SPY', 'QQQ'] })] }), 'E');
  // 바꾼 몫: 200,000센트 ÷ 2 = 1,000달러씩. 입금 300 중 1/3은 현금, 200은 비중(SPY 1,000·QQQ 1,000 → 반반)
  assert.deepEqual(trades(e, { side: 'buy' }).map((t) => [t.date, t.ticker, t.kind, t.amount]),
    [['2026-10-16', 'SPY', 'etf', 1000], ['2026-11-03', 'SPY', 'deposit', 100], ['2026-11-05', 'QQQ', 'etf', 1000], ['2026-11-05', 'QQQ', 'deposit', 100]]);
  assert.equal(e.cash, 1100);
  // 가격이 끝까지 안 돌아오면 그 몫은 현금으로 남는다
  const never = pick(run({ world: { close: (t) => (t === 'QQQ' ? null : undefined) }, scenarios: [S('E', { etfShare: 1, etfs: ['SPY', 'QQQ'] })] }), 'E');
  assert.deepEqual(Object.keys(never.holdings), ['SPY']);
  assert.equal(never.cash, 2000);
  assert.throws(() => run({ scenarios: [S('E', { etfs: ['GLD'] })] }), /etfs/);
  assert.throws(() => run({ scenarios: [S('E', { etfs: [] })] }), /etfs/);
  assert.throws(() => run({ scenarios: [S('E', { etfShare: 1.2 })] }), /etfShare/);
  assert.throws(() => run({ scenarios: [S('E', { splitWeeks: 2 })] }), /바꿀 수 없는/);
});

test('E: 출발이 미뤄진 사이의 입금은 현금 비율 계산에서 빼고, 입금처럼 현금 몫만 남긴 채 산다', () => {
  // AAA 가격이 10-16에 없어 출발이 10-19로 밀리고, 그 사이(10-19 장 시작 전) 입금 300이 들어온다
  const close = (t, d) => (t === 'AAA' && d === '2026-10-16' ? null : undefined);
  const dep = [{ id: 'd1', amount: 300, recordedAt: '2026-10-16T21:00:00Z' }];
  const e = pick(run({ world: { close }, deposits: dep, scenarios: [S('E', { etfShare: 1, etfs: ['SPY', 'RSP', 'QQQ'] })] }), 'E');
  assert.equal(e.started, '2026-10-19');
  assert.equal(e.startValue, 3300);
  // 현금 비율 = (1,300 − 300) ÷ (3,300 − 300) = 1/3 → 입금 300 중 100은 현금, 200을 세 ETF에(66.66씩)
  assert.deepEqual(trades(e, { kind: 'deposit' }).map((t) => t.amount), [66.66, 66.66, 66.66]);
  assert.deepEqual(trades(e, { kind: 'etf', side: 'buy' }).map((t) => t.amount), [666.66, 666.66, 666.66]);
  near(e.cash, 1100.04, 1e-9);
});

test('E: 나중에 만들면 만든 날의 A 상태(입금으로 산 수량 포함)에서 출발해 그날 바꾼다', () => {
  const dep = [{ id: 'd1', amount: 300, recordedAt: '2026-11-02T15:00:00Z' }];
  const r = run({ deposits: dep, scenarios: [S('E', { etfShare: 1, etfs: ['SPY'] }, { createdAt: '2026-11-10T15:00:00Z' })] });
  const a = pick(r, 'A'), e = pick(r, 'E');
  assert.equal(e.started, '2026-11-10');   // S = 11-11, S 전 거래일 장 마감 뒤 A에서
  const sells = trades(e, { side: 'sell' });
  assert.ok(sells.every((t) => t.date === '2026-11-10' && t.kind === 'etf'));
  // A가 입금으로 더 산 수량까지 판다
  const aShares = (t) => a.trades.filter((x) => x.ticker === t).reduce((s2, x) => s2 + x.shares, 0);
  assert.equal(sells.find((t) => t.ticker === 'AAA').shares, 10 + aShares('AAA'));
  assert.deepEqual(Object.keys(e.holdings), ['SPY']);
  assert.equal(trades(e, { kind: 'deposit' }).length, 0);   // 기다리는 동안의 입금은 A가 이미 샀다(현금 몫 없이 물려받음)
});

// 출금(2026-10-22 사용자 결정): 모든 전략이 현금에서만 뺀다. 모자라면 뺄 수 있는 만큼만 빼고 withdrawShort 사건을 남긴다
const W = (id, amount, recordedAt) => ({ id, amount, kind: 'withdraw', recordedAt });
test('withdraw: 현금에서만 빼고 종목은 팔지 않는다, 흐름은 음수라 수익률은 그대로', () => {
  const res = run({ deposits: [W('w1', 300, '2026-11-07T15:00:00Z')] });   // 토 → 11-09
  const a = pick(res, 'A');
  assert.equal(trades(a).filter((t) => t.side === 'sell').length, 0);
  near(day(a, '2026-11-09').value, 2700, 0.01);
  near(day(a, '2026-11-09').deposits, -300, 0.01);
  near(day(a, '2026-11-09').twr, 0);
  assert.equal(a.events.filter((e) => e.kind === 'withdrawShort').length, 0);
});

test('withdraw: 현금보다 많이 빼면 있는 만큼만, 못 뺀 돈은 사건으로', () => {
  const res = run({ deposits: [W('w1', 1500, '2026-11-07T15:00:00Z')] });
  const a = pick(res, 'A');
  near(day(a, '2026-11-09').value, 2000, 0.01);
  near(day(a, '2026-11-09').deposits, -1000, 0.01);
  assert.deepEqual(a.events.filter((e) => e.kind === 'withdrawShort').map((e) => [e.date, e.amount]), [['2026-11-09', 500]]);
  // 기준선(SPY 6주, 현금 0)은 뺄 현금이 없어 그대로
  near(a.baselines.SPY.find((x) => x.date === '2026-11-09').value, 3000, 0.01);
});

test('withdraw: 아직 사지 못한 입금 몫은 남은 현금을 넘지 않게 줄인다', () => {
  const res = run({ snapshot: { ...SNAP, cash: 0 },
    deposits: [{ id: 'd1', amount: 1000, recordedAt: '2026-11-07T15:00:00Z' }, W('w1', 600, '2026-11-07T15:01:00Z')] });
  const a = pick(res, 'A');
  assert.deepEqual(trades(a).map((t) => [t.date, t.ticker, t.amount]), [['2026-11-09', 'AAA', 200], ['2026-11-09', 'DDD', 200]]);
  near(day(a, '2026-11-09').deposits, 400, 0.01);
});

test('withdraw: 점검일 뒤 출금이면 남은 회차는 현금을 넘겨 사지 않는다', () => {
  const res = run({ scenarios: [S('B')], deposits: [W('w1', 900, '2026-11-02T22:00:00Z')] });   // 11-03 반영
  const b = pick(res, 'B');
  const after = trades(b).filter((t) => t.side === 'buy' && t.date >= '2026-11-03' && t.date < '2026-12-01');
  assert.equal(after.length, 0);
  assert.ok(b.events.some((e) => e.kind === 'withdrawShort' && e.date === '2026-11-03'));
  for (const x of b.days) if (x.value != null) assert.ok(x.value >= 0);
});

test('withdraw: 같은 반영일 입출금은 기록 시각 순서 — 입력 배열 순서와 상관없다', () => {
  const dep = { id: 'd1', amount: 1000, recordedAt: '2026-11-07T15:00:00Z' }, wd = W('w1', 1000, '2026-11-07T15:01:00Z');
  const a = pick(run({ snapshot: { ...SNAP, cash: 0 }, deposits: [wd, dep] }), 'A');
  const b = pick(run({ snapshot: { ...SNAP, cash: 0 }, deposits: [dep, wd] }), 'A');
  assert.deepEqual(a.days.map((x) => x.value), b.days.map((x) => x.value));
  near(day(a, '2026-11-09').deposits, 0, 0.01);                     // 입금 뒤 출금이라 다 뺐다
  assert.equal(a.events.filter((e) => e.kind === 'withdrawShort').length, 0);
});

test('withdraw: 두 예약(A 입금 몫·E ETF 몫)을 합쳐 같은 비율로 줄인다', () => {
  // E 출발일(10-16) SPY 가격이 없으면 ETF 몫이 예약으로 남는다. 그 사이 입금·출금
  const res = run({ world: { close: (t, d) => (t === 'SPY' && d <= '2026-11-09' ? null : undefined) },
    scenarios: [S('E', { etfShare: 1, etfs: ['SPY'] })],
    deposits: [W('w1', 2000, '2026-11-07T15:00:00Z')] });
  const e = pick(res, 'E');
  const buys = trades(e).filter((t) => t.kind === 'etf');
  // 출발 때 종목 2000을 팔아 SPY 예약 2000 + 현금 1000. 11-09 출금 2000 → 현금 1000, 예약은 1000으로 줄어 그 돈으로 SPY를 산다
  assert.ok(buys.every((t) => t.amount <= 1000 + 1e-9));
  for (const x of e.days) if (x.value != null) assert.ok(x.value >= -1e-9);
});
