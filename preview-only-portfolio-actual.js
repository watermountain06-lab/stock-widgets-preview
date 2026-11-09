// preview 전용 Portfolio 탭 — 전략 비교의 "내 실제 계좌" 줄(2026-10-21 사용자 결정). 라이브로 옮기지 않는다 — pipeline/site_ui/UI_DIFF.md 1절 portfolio.
//
// 사용자가 원칙을 직접 계좌에 반영하므로 모의 "내 원칙"(B) 대신 실제 계좌를 비교 줄로 둔다. 계산:
//   출발 = 시작 스냅샷(다른 전략과 같음) · 매매 = 한눈에 탭 "실제 매매 기록"(시작일 뒤 날짜, 실제 체결가, 휴장일이면 다음 거래일)
//   · 입금 = 전략 비교 입금(엔진과 같은 반영일·취소 기준) · 분할 = 모든 일별 기록의 분할(id로 한 번, 효력일이 시작일 뒤)을 먼저
//     모아 효력일 장 시작 전에 적용한다. 실제 계좌는 결정을 내리지 않으므로 늦게 도착한 기록을 앞당겨 써도 된다 — 증권사도
//     효력일부터 분할 뒤 수량으로 매매하므로 그 뒤 매매 기록과 단위가 맞는다(dr r1 Fable 제안). 기록이 오기 전 가격 급변 날은
//     엔진의 분할 안전망이 미확정으로 둔다
//   · 매매 대금은 체결마다 센트로 맞춘다(증권사와 같음). 보유보다 많이 판 기록은 가진 만큼만 반영하고 그 수량으로 기록한다
//   · 평가 = 일별 기록 종가(엔진과 같은 사용 가능 판정) · TWR·기준선 대비 = 엔진 twr과 A의 기준선(같은 출발).
// 결과는 엔진 시나리오와 같은 모양이라 비교 표·그래프·도넛·매매 기록이 그대로 그린다. 배당·세금은 다른 전략처럼 뺀다.
// 이번 달 운용(구매 후보·매도 검토)은 화면에 보이지 않는 원칙 시나리오 '__plan'(B, 매도 0%)이 계산한다(attachActual).
import { twr, depositTiming, BASELINES, _internal } from './preview-only-portfolio-engine.js?v=13';
import { ledgerActive, ledgerDeposits, incomeList, kwState, mergeStart } from './preview-only-portfolio-accounts.js?v=7';

export const REAL_ID = 'REAL';
export const PLAN_ID = '__plan';

const effectiveDeposits = (deposits) => {
  const all = Object.entries(deposits || {});
  const cancelAt = new Map();
  for (const [, d] of all) if (d.cancels && d.recordedAt) {
    const t = Date.parse(d.recordedAt);
    if (!cancelAt.has(d.cancels) || t < cancelAt.get(d.cancels)) cancelAt.set(d.cancels, t);
  }
  const out = [];
  for (const [id, d] of all) {
    if (d.cancels || !(d.amount > 0) || !d.recordedAt) continue;
    const tm = depositTiming(d.recordedAt);
    if (!tm.day) continue;
    if (cancelAt.has(id) && cancelAt.get(id) < tm.cancelBefore) continue;
    // rec: 기록한 날(뉴욕), forMonth: 미리 넣은 돈의 몫 달(2026-10-25 사용자 결정 — 카드 한도만 쓰고, 엔진·실제 계좌는 반영일 그대로)
    const rec = new Date(Date.parse(d.recordedAt)).toLocaleDateString('en-CA', { timeZone: 'America/New_York' });
    // forMonth는 있는 달이고 반영일 달보다 뒤일 때만 남긴다 — 계산·표시가 같은 값을 쓴다(dr)
    const pre = (d.kind !== 'withdraw' || d.account === 'kw') && /^\d{4}-(0[1-9]|1[0-2])$/.test(d.forMonth || '') && d.forMonth > tm.day.slice(0, 7);   // 출금(역환전)도 저장된 몫 달(2026-10-28 dr) — Robinhood 출금은 forMonth를 저장하지 않아 그대로
    out.push({ day: tm.day, rec, amount: d.kind === 'withdraw' ? -d.amount : d.amount, ...(pre ? { forMonth: d.forMonth } : {}) });   // 출금은 음수(2026-10-22)
  }
  return out;
};

// records: 일별 기록, snapshot: {date, holdings, cash}, deposits·trades: Firestore 지도, baselines: A의 기준선(같은 출발일일 때만 대비를 낸다)
export { effectiveDeposits };
// baseStart·baseStartValue: A의 출발일·출발 평가액 — 둘 다 같을 때만 A의 기준선으로 대비를 낸다(dr r2: 출발 평가액이 다르면 기준선도 다르다)
// account: 'rh'|'kw'를 주면 그 계좌 매매만(계좌 칸 없는 옛 매매는 rh), income: [{date, amount}] 배당·이자(그날 장 시작 전 현금, 외부 흐름 아님 — 2026-10-28 한국 계좌),
// 매매 수수료(fee, 달러)는 매수 대금에 더하고 매도 대금에서 뺀다
// kwStart: 합계 줄일 때 시작 보유 중 키움 몫 {티커: 수량} — 매도는 계좌별 보유까지만 체결한다(한 계좌에 없는 주식을 다른 계좌 보유로 팔지 않게, dr)
export function actualAccount({ records, snapshot, deposits, trades, baselines, baseStart, baseStartValue, account, income, kwStart }) {
  const cal = _internal.makeCalendar(), mk = _internal.makeMarket(records, cal);
  const i0 = cal.index(snapshot.date), i1 = cal.index(mk.lastSession);
  const shares = new Map(Object.entries(snapshot.holdings || {}).map(([t, q]) => [t, Number(q)]));
  const kwHave = new Map(Object.entries(kwStart || {}).map(([t, q]) => [t, Number(q)]));   // 합계 줄에서 키움 몫(나머지는 Robinhood 몫)
  let cash = Number(snapshot.cash) || 0;
  const deps = effectiveDeposits(deposits);
  const all = Object.entries(trades || {});
  const cancelled = new Set(all.filter(([, x]) => x.cancels).map(([, x]) => x.cancels));
  const list = all.filter(([id, x]) => !x.cancels && !cancelled.has(id) && x.date > snapshot.date && (!account || (x.account === 'kw' ? 'kw' : 'rh') === account))
    .map(([id, x]) => ({ id, ...x, day: cal.onOrAfter(x.date) }))
    .sort((a, b) => (a.date !== b.date ? (a.date < b.date ? -1 : 1) : a.side !== b.side ? (a.side === 'buy' ? -1 : 1) : (a.recordedAt || '') < (b.recordedAt || '') ? -1 : 1));
  const warnings = [], done = [];
  const raw = [];
  const splits = new Map();   // 효력 거래일 → [분할]
  const seen = new Set();
  for (const r of records) for (const sp of r.splits || []) {
    if (seen.has(sp.id) || !(sp.effectiveDate > snapshot.date) || !(sp.ratio > 0)) continue;
    seen.add(sp.id);
    const e = cal.onOrAfter(sp.effectiveDate);
    splits.set(e, [...(splits.get(e) || []), sp]);
  }
  const cents = (v) => Math.round(v * 100) / 100;
  const micro = (v) => Math.round(v * 1e6) / 1e6;   // 수량은 바뀔 때마다 마이크로주로 맞춘다(평가와 보여 주는 수량이 같게)
  for (let i = i0; i >= 0 && i <= i1; i++) {
    const d = cal.sessions[i];
    let flow = 0;
    if (i > i0) {
      for (const p of deps) if (p.day === d) { cash = cents(cash + p.amount); flow += p.amount; }
      for (const p of income || []) if (p.date > snapshot.date && cal.onOrAfter(p.date) === d) cash = cents(cash + p.amount);   // 배당·이자: 수익(흐름 아님)
      for (const sp of splits.get(d) || []) {
        if (shares.get(sp.ticker) > 0) shares.set(sp.ticker, micro(shares.get(sp.ticker) * sp.ratio));
        if (kwHave.get(sp.ticker) > 0) kwHave.set(sp.ticker, micro(kwHave.get(sp.ticker) * sp.ratio));
      }
      for (const x of list) {
        if (x.day !== d) continue;
        const have = shares.get(x.ticker) || 0;
        const isKw = x.account === 'kw', kwQ = kwHave.get(x.ticker) || 0;
        const acctHave = account ? have : isKw ? kwQ : Math.max(0, have - kwQ);   // 합계 줄은 그 계좌 몫까지만 판다
        let q = x.qty;
        if (x.side === 'buy') { shares.set(x.ticker, micro(have + q)); if (!account && isKw) kwHave.set(x.ticker, micro(kwQ + q)); }
        else {
          q = Math.min(x.qty, acctHave);
          if (!account && isKw) kwHave.set(x.ticker, micro(kwQ - q));
          if (x.qty - q > 1e-9) warnings.push(`${x.date} ${x.ticker} 보유(${Math.round(have * 1e6) / 1e6}주)보다 많이 판 기록(${x.qty}주) — 가진 만큼만 반영`);
          shares.set(x.ticker, micro(have - q));
        }
        if (!(q > 0)) continue;
        const amt = cents(q * x.price), fee = Number(x.fee) > 0 ? cents(Number(x.fee)) : 0;
        cash = cents(cash + (x.side === 'buy' ? -(amt + fee) : amt - fee));
        done.push({ date: d, ticker: x.ticker, side: x.side, shares: q, price: x.price, amount: amt, ...(fee ? { fee } : {}), ...(x.account === 'kw' ? { account: 'kw' } : {}), ...(q !== x.qty ? { requested: x.qty } : {}) });
      }
    }
    let v = null;
    const why = [];
    if (!mk.dayOk(d)) why.push(mk.by.has(d) ? 'pipelineFailed' : 'noRecord');
    else {
      // 엔진과 같은 계산 경로: 마이크로주 정수 × 종가를 모아 센트로 한 번 반올림(dr r3 — 반 센트 경계에서 A와 1센트 어긋나지 않게)
      let sum = 0;
      for (const [t, q] of [...shares].sort()) {   // 엔진과 같은 순서(티커순)로 더해야 부동소수 합이 같다(dr r4)
        if (!(q > 1e-9)) continue;
        if (!mk.usable(t, d)) { why.push((mk.flagged(t, d) ? 'splitCheck:' : 'noPrice:') + t); continue; }
        sum += (Math.round(q * 1e6) * mk.close(t, d)) / 1e4;
      }
      v = why.length ? null : (Math.round(cash * 100) + Math.round(sum)) / 100;
    }
    raw.push({ date: d, value: v, flow, why });
  }
  if (cash < 0) warnings.push(`현금이 ${cash}달러로 음수입니다 — 빠진 입금이나 잘못 적은 매수가 없는지 확인하세요`);
  // 출발: 평가가 처음 확정되는 날(그 전 입금은 출발 평가액에 든다 — 엔진과 같다)
  const j0 = raw.findIndex((x) => x.value !== null);
  const started = j0 < 0 ? null : raw[j0].date, startValue = j0 < 0 ? null : raw[j0].value;
  const tail = j0 < 0 ? [] : raw.slice(j0);
  const t = twr(tail);
  const sameStart = started && started === baseStart && baseStartValue != null && Math.abs(startValue - baseStartValue) < 0.005;
  if (started && !sameStart) warnings.push(started === baseStart ? `출발 평가액이 A와 달라 기준선 대비가 없습니다` : `출발일(${started})이 A와 달라 기준선 대비가 없습니다`);
  let cum = 0;
  const days = raw.map((x, k) => {
    const j = j0 < 0 ? -1 : k - j0;
    if (j > 0) cum += x.flow;
    const row = { date: x.date, value: x.value, deposits: cum, flowUsd: x.flow, pnl: x.value === null || j < 0 ? null : Math.round((x.value - startValue - cum) * 100) / 100,
      twr: j < 0 ? null : t[j], provisional: false, why: x.why.length ? (j < 0 ? ['notStarted', ...x.why] : x.why) : [] };
    if (j >= 0) row.vs = Object.fromEntries(BASELINES.map((e) => {
      const b = sameStart ? (baselines?.[e] || []).find((p) => p.date === x.date)?.twr : null;
      return [e, row.twr === null || b == null ? null : (row.twr - b) * 100];
    }));
    return row;
  });
  return {
    id: REAL_ID, strategy: REAL_ID, name: '내 실제 계좌', started, startValue, days, cumDeposits: cum,
    holdings: Object.fromEntries([...shares].filter(([, q]) => q > 1e-9).map(([k, q]) => [k, Math.round(q * 1e6) / 1e6])),
    cash: Math.round(cash * 100) / 100, trades: done, skips: [], months: [], events: [], notes: [], warnings,
    baselines: sameStart ? baselines : {}, baselineHalts: {}, halted: null,
  };
}

// 엔진 결과에서 숨은 원칙 시나리오를 떼어 result.plan으로 두고, 실제 계좌 줄을 맨 앞에(그다음 A, 만든 시나리오 — 사용자 요청 10-21) 둔다
// ledger(계좌 장부, 2026-10-28)가 있으면: 실제 계좌 줄 = Robinhood + 키움 합계(시작 = rh 스냅샷 + 키움의 반영일 ≤ 시작일 상태, 흐름 = rh 입금 ∪ 환전),
// result.accounts = { rh, kw }(계좌별 줄 — 내 계좌 탭), 장부 사건·정정 충돌
export function attachActual(result, { records, bundle, trades, ledger }) {
  if (!result) return result;
  const plan = result.scenarios.find((s) => s.id === PLAN_ID) || null;
  const rest = result.scenarios.filter((s) => s.id !== PLAN_ID);
  const A = rest[0];
  // 실제 계좌 계산이 실패해도 다른 전략은 그대로 보이게 한다
  let real;
  const { events, conflicts } = ledgerActive(ledger);
  // 시작일까지 반영된 장부 사건은 시작 상태(kw0)에 있으므로 흐름에서 뺀다(엔진과 같게 명시적으로, dr)
  const L = ledgerDeposits(events.filter((e) => e.kind === 'income' || e.day > bundle.snapshot.date)), income = incomeList(events);
  const kw0 = kwState(events, trades, bundle.snapshot.date, 'eff', records);
  const fail = (e, name) => ({ id: REAL_ID, strategy: REAL_ID, name, started: null, days: [], trades: [], skips: [], months: [], holdings: {}, cash: 0, warnings: ['계산하지 못했습니다: ' + e.message] });
  try { real = actualAccount({ records, snapshot: mergeStart(bundle.snapshot, kw0), deposits: { ...(bundle.deposits || {}), ...L }, trades, income, kwStart: Object.fromEntries(kw0.holdings.map((h) => [h.ticker, h.qty])), baselines: A?.baselines, baseStart: A?.started, baseStartValue: A?.startValue }); }
  catch (e) { real = fail(e, '내 실제 계좌'); }
  let rh, kw;
  try { rh = actualAccount({ records, snapshot: bundle.snapshot, deposits: bundle.deposits, trades, account: 'rh' }); } catch (e) { rh = fail(e, 'Robinhood'); }
  try { kw = actualAccount({ records, snapshot: mergeStart({ date: bundle.snapshot.date, holdings: {}, cash: 0 }, kw0), deposits: L, trades, account: 'kw', income }); } catch (e) { kw = fail(e, '키움'); }
  return { ...result, plan, scenarios: [real, A, ...rest.slice(1)], accounts: { rh, kw, events, conflicts } };
}
