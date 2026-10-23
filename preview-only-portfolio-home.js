// preview 전용 Portfolio 탭 — "한눈에" 하위 탭(2026-10-20, 시안 A2 사용자 선택). 라이브로 옮기지 않는다 — pipeline/site_ui/UI_DIFF.md 1절 portfolio.
//
// 내 자산(올린 보유 + 그 뒤 기록한 실제 매매), 실제 매매 기록 칸, 이번 달 할 일, 이번 달 운용(점검일 결정과 회차 진행),
// 전략 비교 도넛(전략마다 지금 들고 있는 종목·현금 비중, 가운데 수익률)을 그린다. 계산은 엔진 결과(replay)를 받아 쓰고,
// 저장은 preview-only-portfolio.js가 넘겨 준 handlers로 한다. 순수 함수(currentHoldings·monthView)는 node 시험이 부른다
// (pipeline/portfolio/test_strategy_view.mjs). 실제 매매 기록은 모의 전략 계산에는 넣지 않고, 전략 비교의 "내 실제 계좌" 줄만 쓴다(preview-only-portfolio-actual.js).
import { el, twoStep, msgLine, usd, pct, pp, shares, label, summarize } from './preview-only-portfolio-strategy.js?v=18';
import { renderStrategy } from './preview-only-portfolio-rank.js?v=7';
import { renderManage } from './preview-only-portfolio-records.js?v=6';
import { ENGINE_VERSION, BUY_PRINCIPLE, _internal, depositTiming, twr as engineTwr } from './preview-only-portfolio-engine.js?v=3';
import { effectiveDeposits } from './preview-only-portfolio-actual.js?v=8';

// 미국 동부 날짜(YYYY-MM-DD). 매매 기록 칸의 기본값·미래 날짜 검사와 '이번 달' 판단에 쓴다.
export const etDate = (ms) => new Intl.DateTimeFormat('en-CA', { timeZone: 'America/New_York', year: 'numeric', month: '2-digit', day: '2-digit' }).format(new Date(ms));
const usd0 = (v) => (v == null ? '—' : '$' + Math.round(v).toLocaleString('en-US'));
const md = (d) => (d ? d.slice(5).replace('-', '/') : '');
const TIER_CLS = { '초저평가': 'pf-t-low', '저평가': 'pf-t-low', '적정~저평가': 'pf-t-low', '적정': 'pf-t-mid', '고평가~적정': 'pf-t-mid', '고평가': 'pf-t-high', '초고평가': 'pf-t-vhigh' };

// ---- 순수 함수 ----

// 올린 보유(holdings.rows, 기준일 asOf) + 기준일 뒤에 기록한 실제 매매 → 지금 보유
// rows: [{ticker, qty, avgPrice, currency}] — 티커가 빈 줄은 현금(수량 1 × avgPrice = 금액, 2026-10-19 vault 형식)
// trades: {id: {date, ticker, side, qty, price, recordedAt} | {cancels, recordedAt}}
// upTo(YYYY-MM-DD)를 주면 그날 뒤 날짜의 매매는 반영하지 않는다(future). 같은 날은 매수를 먼저, 그다음 기록 순서.
// 올린 보유에 현금 줄이 없으면 현금을 모르는 것으로 보고 매매로 현금을 바꾸지 않는다(hasCash=false).
// 보유보다 많이 판 기록은 가진 만큼만 반영하고 clipped(반영 못 한 주 수)를 남긴다.
export function currentHoldings(rows, asOf, trades, upTo) {
  const base = (asOf || '').slice(0, 10);
  const pos = new Map();
  let cash = 0, hasCash = false;
  for (const r of rows || []) {
    if (r.currency && String(r.currency).toUpperCase() !== 'USD') continue;
    const t = String(r.ticker || '').trim().toUpperCase();
    const q = Number(r.qty) || 0, a = Number(r.avgPrice) || 0;
    if (!t) { cash += q * a; hasCash = true; continue; }
    const p = pos.get(t) || { qty: 0, cost: 0, name: r.name || '' };
    p.qty += q; p.cost += q * a; pos.set(t, p);
  }
  const all = Object.entries(trades || {});
  const cancelled = new Set(all.filter(([, x]) => x.cancels).map(([, x]) => x.cancels));
  const list = all.filter(([id, x]) => !x.cancels && !cancelled.has(id))
    .map(([id, x]) => ({ id, ...x }))
    .sort((x, y) => (x.date !== y.date ? (x.date < y.date ? -1 : 1) : x.side !== y.side ? (x.side === 'buy' ? -1 : 1)
      : (x.recordedAt || '') < (y.recordedAt || '') ? -1 : 1));
  const applied = [], skipped = [], future = [], clipped = [];
  for (const x of list) {
    if (base && x.date <= base) { skipped.push(x); continue; }   // 기준일과 그 전 매매는 올린 보유에 이미 들어 있다
    if (upTo && x.date > upTo) { future.push(x); continue; }
    const p = pos.get(x.ticker) || { qty: 0, cost: 0, name: '' };
    if (x.side === 'buy') { p.qty += x.qty; p.cost += x.qty * x.price; if (hasCash) cash -= x.qty * x.price; }
    else {
      const q = Math.min(x.qty, p.qty), avg = p.qty ? p.cost / p.qty : 0;
      p.qty -= q; p.cost -= q * avg; if (hasCash) cash += q * x.price;
      if (x.qty - q > 1e-9) clipped.push({ id: x.id, ticker: x.ticker, short: x.qty - q });
    }
    pos.set(x.ticker, p);
    applied.push(x);
  }
  const holdings = [...pos.entries()].filter(([, p]) => p.qty > 1e-9)
    .map(([t, p]) => ({ ticker: t, name: p.name, qty: p.qty, avgPrice: p.qty ? p.cost / p.qty : null })).sort((a, b) => (a.ticker < b.ticker ? -1 : 1));
  return { holdings, cash: Math.round(cash * 100) / 100, hasCash, applied, skipped, future, clipped, base };
}

// 손실 한도(새 원칙 4, 2026-10-22 사용자 결정 — 예전 원칙 9 '알림만'에서 바뀜): 한 종목이 평균 단가보다 limit(20%) 넘게 떨어지면 매도 검토를 시작한다.
// 팔지·얼마나는 사용자가 판단한다 — 엔진 계산·자동 매도는 없다.
// holdings: currentHoldings().holdings, close(t): 최근 종가 또는 null. 평균 단가나 가격이 없는 종목은 건너뛴다. 하락이 큰 순.
export const LOSS_LIMIT = 0.2;
// 카드가 없어도 20% 하락 매도 검토를 보는 지수 ETF(원칙 1·6, 사용자 결정 2026-10-22). 카드 없는 개별 종목은 원칙 6으로 뺀다
export const INDEX_ETFS = ['SPY', 'IVV', 'VOO', 'SPLG', 'VTI', 'QQQ', 'QQQM', 'RSP', 'DIA', 'IWM'];
// 20% 하락 매도 검토 대상인가(원칙 4·6): 기록이 있고, 카드가 있으면 holdReason 통과, 카드가 없으면 지수 ETF일 때만
export function lossReviewable(ticker, rec, today) {
  if (!rec) return false;
  const card = rec.cards?.[ticker];
  return card ? !holdReason(card, rec, today) : INDEX_ETFS.includes(ticker) && holdReason(undefined, rec, today) !== 'recordStale';
}
const dropText = (d) => (d * 100).toFixed(1).replace('-', '−') + '%';
export function lossAlerts(holdings, close, limit = LOSS_LIMIT) {
  const out = [];
  for (const x of holdings || []) {
    const c = close(x.ticker);
    if (c == null || !(x.avgPrice > 0)) continue;
    const drop = c / x.avgPrice - 1;
    // "20% 넘게"(원칙 4) — 정확히 20%는 아님, 실수 오차로 경계를 넓히지 않게
    if (drop < -limit - 1e-9) out.push({ ticker: x.ticker, drop, avgPrice: x.avgPrice, close: c });
  }
  return out.sort((a, b) => a.drop - b.drop || (a.ticker < b.ticker ? -1 : 1));
}

// 다음 할 일 카드에 쓸 시나리오(숨은 원칙 시나리오, 없으면 B나 처음 만든 시나리오)와 그달 계획
// today(미국 동부 날짜)를 주면 '이번 달'은 그 달이다(없으면 lastSession의 달).
export function monthView(result, lastSession, today) {
  if (!result) return null;
  // 원칙 시나리오(attachActual이 떼어 둔 result.plan)가 있으면 그것, 없으면 예전처럼 B나 처음 만든 시나리오
  const pick = (result.plan && result.plan.started ? result.plan : null) || result.scenarios.find((s) => s.strategy === 'B' && s.started) || result.scenarios.find((s) => s.id !== 'A' && s.id !== 'REAL' && s.started);
  if (!pick) return null;
  const plan = pick.months[pick.months.length - 1] || null;
  if (!plan) return { scenario: pick, plan: null };
  const trades = pick.trades.filter((t) => t.date >= plan.decisionDate);
  const skips = pick.skips.filter((x) => x.date && x.date >= plan.decisionDate);
  const steps = [{ label: '결정', date: plan.decisionDate, state: 'done' }, ...plan.rounds.map((r, i) => {
    const sk = skips.some((x) => x.date === r.date && x.action !== 'carried'), tr = trades.some((t) => t.date === r.date);
    return { label: i + 1 + '회차', date: r.date,
      state: r.dropped ? 'dropped' : r.date > lastSession ? 'todo' : sk && tr ? 'partial' : sk ? 'skip'
        : skips.some((x) => x.date === r.date) ? 'carry' : 'done' };
  })];
  const spent = trades.filter((t) => t.side === 'buy').reduce((a, t) => a + t.amount, 0);
  const next = plan.rounds.find((r) => !r.dropped && r.date > lastSession) || null;
  // 마지막 결정이 지난달이면(이번 달 점검일 결정이 아직 없음) stale — 화면은 '지난달 계획 · 이번 달 결정 대기'로 보여 준다
  const nowMonth = (today || lastSession || '').slice(0, 7);
  const stale = !!nowMonth && plan.decisionDate.slice(0, 7) !== nowMonth;
  return { scenario: pick, plan, steps, spent, next, stale, alerts: (plan.fires || []).filter((f) => f.observed && !f.skip) };
}

// 실제 매매 입력 검사(기록·고치기 공통). 틀리면 사람이 읽을 문구, 맞으면 null.
export function checkTrade(x, today) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(x.date || '')) return '날짜를 고르세요.';
  if (x.date > today) return '미래 날짜는 기록할 수 없습니다(체결한 날, 미국 동부 기준).';
  if (!/^[A-Z][A-Z0-9.-]{0,9}$/.test(x.ticker || '')) return '티커를 넣으세요.';
  if (x.side !== 'buy' && x.side !== 'sell') return '매수·매도를 고르세요.';
  if (!(x.qty > 0) || Math.round(x.qty * 1e6) / 1e6 !== x.qty) return '수량은 0보다 크고 소수 6자리까지입니다.';
  if (!(x.price > 0)) return '체결가를 넣으세요.';
  if (x.qty > 1e7 || x.price > 1e7) return '수량·체결가는 1천만 이하만 기록합니다.';
  return null;
}

// 내 자산 현금에 더할 입금: 모든 묶음의 입금(키 '묶음:id', 끝낸 묶음 포함) 가운데 반영일이 기준일 뒤·오늘까지인 것.
// 입금 기록 하나 = 실제 입금 하나로 센다(반영일·금액만으로는 다시 적은 것인지 알 수 없다 — dr r3). 취소는 묶음 안에서만 찾는다.
export function depositsSince(all, base, today) {
  const byBundle = new Map();
  for (const [k, v] of Object.entries(all || {})) { const b = k.split(':')[0]; if (!byBundle.has(b)) byBundle.set(b, {}); byBundle.get(b)[k] = v; }
  const out = [];
  for (const deps of byBundle.values()) for (const p of effectiveDeposits(deps)) if (p.day > base && p.day <= today) out.push(p);
  return out.sort((x, y) => (x.day < y.day ? -1 : 1));
}

// 원칙 3 매수 금액(2026-10-22 사용자 결정, dr r1 반영 — 예전 초안 '원칙 10'): 그달 넣은 돈(+지난달 판 돈)만 쓰고, 카드가 보여 준 살 후보 중 내가 고른 종목에 나눠 산다.
// 나누는 방법은 균등·시총 비중(시가총액 비례)·판정 가중(등급 무게 초저평가 4 : 저평가 3 : 적정~저평가 2 : 적정 1) 가운데 고른다(기본값 없음).
// 놓친 회차(사용자 결정 10-22 Q2): 이번 회차 금액 = (그 종목 달 몫 − 이번 달 그 종목에 산 돈) ÷ 남은 회차 수(이번 회차 포함).
// 모든 종목의 남은 몫 합은 남은 돈(쓸 돈 − 이번 달 산 돈 전부)을 넘지 않게 비례로 줄인다. 계산은 끝까지 센트 정수(내림 — 남는 센트는 쓰지 않는다).
// budget·spent·bought 값은 달러. 고른 것 가운데 무게가 없는 종목(시총 없음·무게 밖 판정)이 있으면 그 방법은 null.
// 돌려주는 값(모두 방법별): by(달 몫)·rest(남은 몫)·round(이번 회차 금액, 남은 회차 0이면 null) {티커: 달러}, missed(지난 회차 계획보다 덜 산 종목), capped(남은 돈에 맞춰 줄임).
export const BUY_METHODS = [['equal', '균등'], ['cap', '시총 비중'], ['tier', '판정 가중']];
export const TIER_WEIGHT = { '초저평가': 4, '저평가': 3, '적정~저평가': 2, '적정': 1 };
const toC = (v) => Math.max(0, Math.round((v || 0) * 100));
// a × b ÷ c 내림을 정확히(정수만, BigInt — 실수 비율로 하면 3/11 같은 무게에서 1센트가 빠진다, dr r2)
const mulDiv = (a, b, c) => Number((BigInt(a) * BigInt(b)) / BigInt(c));
export function buyPlan({ cands, picked, budget, spent = 0, bought = {}, tiers = {}, caps = {}, rounds = 4, roundsLeft = rounds }) {
  const sel = cands.filter((t) => picked.includes(t));
  const cents = toC(budget), left = Math.max(0, cents - toC(spent)), passed = Math.max(0, rounds - roundsLeft);
  const plan = (w) => {
    const wt = Object.fromEntries(sel.map((t) => [t, Math.round(w(t))]));   // 시총은 달러 정수로(1e13대까지 안전 정수)
    if (!sel.length || sel.some((t) => !(wt[t] > 0) || !Number.isSafeInteger(wt[t]))) return null;
    const tot = sel.reduce((a, t) => a + wt[t], 0);
    const share = Object.fromEntries(sel.map((t) => [t, mulDiv(cents, wt[t], tot)]));
    let rest = Object.fromEntries(sel.map((t) => [t, Math.max(0, share[t] - toC(bought[t]))]));
    const sum = sel.reduce((a, t) => a + rest[t], 0);
    const capped = sum > left;   // 남은 돈에 맞춰 비례로 줄였다
    if (capped) rest = Object.fromEntries(sel.map((t) => [t, mulDiv(rest[t], left, sum)]));
    const round = roundsLeft > 0 ? Object.fromEntries(sel.map((t) => [t, Math.floor(rest[t] / roundsLeft)])) : null;
    // 놓친 몫: 지난 회차까지 계획(달 몫 × 지난 회차 ÷ 회차 수)보다 그 종목에 덜 샀다
    const missed = round && passed > 0 ? sel.filter((t) => toC(bought[t]) < mulDiv(share[t], passed, rounds)) : [];
    return { share, rest, round, missed, capped };
  };
  const out = { sel, by: {}, round: {}, rest: {}, missed: {}, capped: {} };
  const usdOf = (o) => (o ? Object.fromEntries(Object.entries(o).map(([t, c]) => [t, c / 100])) : null);
  for (const [k, w] of [['equal', () => 1], ['cap', (t) => caps[t]], ['tier', (t) => TIER_WEIGHT[tiers[t]]]]) {
    const r = plan(w);
    out.by[k] = usdOf(r?.share); out.round[k] = usdOf(r?.round); out.rest[k] = usdOf(r?.rest); out.missed[k] = r ? r.missed : []; out.capped[k] = !!r?.capped;
  }
  return out;
}

// 그달 넣은 돈: 모든 묶음의 입금(키 '묶음:id') 가운데 반영일(엔진과 같은 기준 — 기록 시각 다음 장 시작)이 그달인 것(dr r1 — 점검일
// 직전 주말 입금이 그달 몫이 되게). 취소는 묶음 안에서만 찾는다. 반영일이 다음 달 이후면 later로 따로 준다.
export function monthDeposits(all, month) {
  const byBundle = new Map();
  for (const [k, v] of Object.entries(all || {})) { const b = k.split(':')[0]; if (!byBundle.has(b)) byBundle.set(b, {}); byBundle.get(b)[k] = v; }
  const now = [], later = [];
  for (const deps of byBundle.values()) for (const p of effectiveDeposits(deps)) {
    const m = p.day.slice(0, 7);
    if (m === month) now.push(p); else if (m > month) later.push(p);
  }
  const by = (x, y) => (x.day < y.day ? -1 : 1);
  return { now: now.sort(by), later: later.sort(by) };
}

// 이번 달 실제 매수(취소 빼고, 그달 1일부터 오늘까지 — dr r1: 점검일 전 매수도 그달 돈을 쓴 것) — 종목별 {qty, amount}
export function monthBuys(trades, month, today) {
  const real = Object.entries(trades || {});
  const cancelled = new Set(real.filter(([, x]) => x.cancels).map(([, x]) => x.cancels));
  const out = new Map();
  for (const [id, x] of real) {
    if (x.cancels || cancelled.has(id) || x.side !== 'buy' || x.date.slice(0, 7) !== month || x.date > today) continue;
    const o = out.get(x.ticker) || { qty: 0, amount: 0 }; o.qty += x.qty; o.amount = Math.round(o.amount * 100 + Math.round(x.qty * x.price * 100)) / 100; out.set(x.ticker, o);   // 거래마다 센트(매도와 같은 단위)
  }
  return out;
}

// 그달 실제 매도 대금(취소 빼고, 그달 1일~오늘). 원칙 4: 판 돈은 다음 달 점검일에 그달 돈에 더한다.
export function monthSells(trades, month, today) {
  const real = Object.entries(trades || {});
  const cancelled = new Set(real.filter(([, x]) => x.cancels).map(([, x]) => x.cancels));
  let sum = 0;
  for (const [id, x] of real) {
    if (x.cancels || cancelled.has(id) || x.side !== 'sell' || x.date.slice(0, 7) !== month || x.date > today) continue;
    sum += Math.round(x.qty * x.price * 100);   // 거래마다 센트로 반올림해 더한다(엔진·실제 계좌 대금과 같은 단위)
  }
  return sum / 100;
}
// 원칙 6 보류 이유(엔진 blocked와 같은 판단 — 카드 없음·판정 없음·가격 묵음·판정 날짜 5거래일 넘게 묵음). rec = 일별 기록. 통과하면 null.
// today를 주면 기록 자체가 오늘보다 5거래일 넘게 묵었는지도 본다(파이프라인이 여러 날 실패한 경우 — dr r2. 엔진은 그날 기록이 없으면 안 산다)
let CAL = null;
const cal = () => (CAL ??= _internal.makeCalendar());
const RECORD_STALE = 5;   // 엔진 STALE_SESSIONS와 같은 값
const nextMonthOf = (m) => cal().sessions.find((d) => d.slice(0, 7) > m)?.slice(0, 7) || null;   // m 다음 달(달력에 있는 달)
export function recordGap(rec, today) { return rec ? cal().sessions.filter((d) => d > rec.session && d <= today).length : Infinity; }
export function holdReason(card, rec, today) {
  if (!rec) return 'noRecord';
  if (today && recordGap(rec, today) > RECORD_STALE) return 'recordStale';
  const why = _internal.blocked(card, rec, cal());
  if (why) return why;
  // 판정 날짜도 오늘까지 센다 — 기록 묵음·판정 묵음이 각각 5거래일 이하여도 합쳐 넘으면 묵은 판정이다(dr r3)
  if (today && recordGap({ session: card.verdictAsOf }, today) > RECORD_STALE) return 'stale';
  return null;
}
const HOLD_TEXT = { noRecord: '완전한 기록 없음', recordStale: '마지막 기록 묵음', noCard: '카드 없음', noVerdict: '판정 없음', stale: '가격·판정 묵음' };
export const prevMonth = (m) => { const [y, n] = m.split('-').map(Number); return n === 1 ? `${y - 1}-12` : `${y}-${String(n - 1).padStart(2, '0')}`; };

// 첫 달 시연(사용자 결정 2026-10-22): 일별 기록이 이번 달에 시작해 그달 정기 점검이 없을 때, 그달 첫 거래일에 점검한 것처럼
// 카드를 보여 준다 — 후보는 그달 첫 일별 기록(firstRec)의 판정(원칙 1·6), 회차는 첫 거래일부터 매주 4회. 보여 주기만 하고(기록 버튼 없음)
// 실제 투자는 다음 달 점검부터. monthView와 같은 모양({plan, steps, next, stale, alerts, demo})을 돌려준다.
export function demoMonth(firstRec, month, lastSession) {
  if (!firstRec || firstRec.session.slice(0, 7) !== month) return null;
  const S = cal().sessions;
  const d0 = S.find((d) => d.slice(0, 7) === month);
  if (!d0) return null;
  const plus = (d, n) => new Date(Date.parse(d + 'T12:00:00Z') + n * 864e5).toISOString().slice(0, 10);
  const rounds = [0, 1, 2, 3].map((k) => ({ date: S.find((d) => d >= plus(d0, 7 * k)), dropped: false })).filter((r) => r.date);
  const candidates = Object.keys(firstRec.cards || {}).sort().filter((t) => !holdReason(firstRec.cards[t], firstRec) && BUY_PRINCIPLE.includes(firstRec.cards[t].tier));
  const plan = { decisionDate: d0, record: firstRec.session, rounds, candidates, fires: [] };
  const steps = [{ label: '결정', date: d0, state: 'done' }, ...rounds.map((r, i) => ({ label: i + 1 + '회차', date: r.date, state: r.date > lastSession ? 'todo' : 'done' }))];
  return { plan, steps, next: rounds.find((r) => r.date > lastSession) || null, stale: false, alerts: [], demo: true };
}

// 시작 전 실제 계좌 흐름을 이어 붙인 수익률(사용자 결정 2026-10-22 A안): pre = {from, base, end, endHoldings, endCash, days:[{d, v, f}], spy:{base, end}}
// (볼트 portfolio_site.json의 preStart — Robinhood CSV와 종가로 만든 base(9/30) 장 마감~end(시작 스냅샷일) 일별 평가액·입출금 f).
// 시작 스냅샷과 같은 날·같은 보유일 때만 잇는다: 전체 = (1 + 시작 전 TWR) × (1 + 실제 계좌 TWR) − 1, SPY도 base 종가부터 같은 방식.
// 맞지 않으면 {why}. 입출금은 수익에서 빼고 배당·이자는 평가액에 든다(현금).
export function chainPreStart(pre, real, snapshot, startValue) {
  if (!pre || !real) return null;
  if (!real.started || real.twr == null) return { why: '실제 계좌가 아직 출발 전' };
  if (pre.end !== real.started || !snapshot || snapshot.date !== pre.end) return { why: `시작 전 기록의 끝(${pre.end})과 시작 스냅샷(${snapshot?.date || '없음'})이 다름` };
  const num = (x) => (typeof x === 'number' && Number.isFinite(x) ? x : NaN);   // 빈 값·글자를 0으로 보지 않는다(dr)
  const a = pre.endHoldings || {}, b = snapshot.holdings || {};
  const same = Object.keys({ ...a, ...b }).every((t) => Math.abs(num(a[t]) - num(b[t])) < 1e-6)
    && Math.abs(num(pre.endCash) - num(snapshot.cash)) < 0.01;
  if (!same) return { why: '시작 전 기록의 마지막 보유·현금이 시작 스냅샷과 다름' };
  const days = pre.days || [];
  if (days.length < 2 || days[0].d !== pre.base || days[days.length - 1].d !== pre.end) return { why: '시작 전 기록의 날짜가 맞지 않음' };
  // 이어 붙이는 날의 평가액이 실제 계좌 출발 평가액과 같아야 한다(가격 출처·반올림이 다르면 이음새에 틈 — dr)
  const vEnd = days[days.length - 1].v;
  if (!(Math.abs(vEnd - num(startValue)) <= Math.max(1, vEnd * 1e-4))) return { why: '시작 전 기록의 마지막 평가액이 출발 평가액과 다름' };
  // 입출금 시점은 사이트 실제 계좌와 같은 규칙(엔진 twr — 그날 입출금은 장 시작 전에 들어온 것으로 본다, dr)
  const t = engineTwr(days.map((x) => ({ value: x.v, flow: x.f })));
  const preTwr = t[t.length - 1];
  if (!Number.isFinite(preTwr)) return { why: '시작 전 수익률을 계산하지 못함' };
  const total = (1 + preTwr) * (1 + real.twr) - 1;
  // SPY: 시작 전은 종가 비율, 실제 계좌 구간은 엔진 SPY 기준선(마이크로주로 종가 비율을 따라감)을 역산
  const spyReal = real.vs?.SPY != null ? real.twr - real.vs.SPY / 100 : null;
  const spyPre = pre.spy?.base > 0 && pre.spy?.end > 0 ? pre.spy.end / pre.spy.base - 1 : null;
  const vsSPY = spyReal == null || spyPre == null ? null : (total - ((1 + spyPre) * (1 + spyReal) - 1)) * 100;
  return { from: pre.from, preTwr, twr: total, vsSPY };
}

// 수익률을 아는 마지막 날 기준 요약(마지막 기록이 불완전해 그날 평가가 비면 그 전날 값 — 예: 10/21 pipelineFull false)
export function summarizeKnown(s) {
  const m = summarize(s);
  if (m.twr != null || !s.started) return m;
  const k = [...(s.days || [])].reverse().find((d) => d.date >= s.started && d.twr != null);
  return k ? { ...m, twr: k.twr, vs: k.vs || null, asOf: k.date } : m;
}

// ---- 그리기 ----
// model = { main(올린 데이터), trades(실제 매매 지도), result|null, bundle|null, byId, records, now }
// handlers = { trade({date, ticker, side, qty, price}), editTrade(id, …), deleteTrade(id), deposit(amount), pick(month, [티커]), goto(tab) }
export function renderHome(root, model, handlers) {
  root.textContent = '';
  const recs = model.records || [];
  const last = recs[recs.length - 1] || null;
  // 가격·판정은 마지막 '완전한' 기록에서 읽는다(파이프라인 실패 날은 엔진도 값을 쓰지 않는다)
  const lastFull = [...recs].reverse().find((r) => r.pipelineFull) || null;
  const close = (t) => { const c = lastFull && (lastFull.cards?.[t]?.close ?? lastFull.prices?.[t]); return typeof c === 'number' ? c : null; };
  // 내 자산·보유 금액은 가장 최근 종가(불완전한 날 기록이라도 그 종목 종가가 있으면 — 사용자 결정 2026-10-22, 급락이 바로 보이게).
  // 매수·매도 검토 같은 판단은 위의 close(마지막 완전한 기록, 원칙 6)를 그대로 쓴다
  const priceDays = new Set();
  const closeNow = (t) => {
    for (let k = recs.length - 1; k >= 0; k--) {
      const c = recs[k].cards?.[t]?.close ?? recs[k].prices?.[t];
      if (typeof c === 'number' && !recs[k].cards?.[t]?.priceStale) { priceDays.add(recs[k].session); return c; }
    }
    return null;
  };
  const tierOf = (t) => (lastFull && lastFull.cards?.[t] ? lastFull.cards[t].tier : null);
  const h = model.main?.holdings || {};
  const now = model.now ?? Date.now(), today = etDate(now);
  const cur = currentHoldings(h.rows, h.asOf, model.trades, today);
  // 전략 비교에 기록한 입금(실제로 계좌에 넣은 돈)도 올린 보유 기준일 뒤·오늘까지 반영일이면 현금에 더한다(dr r1 — 실제 계좌 줄과 같은 돈).
  // 끝낸 묶음의 입금도 실제 돈이므로 모든 묶음을 본다(dr r2, model.allDeposits — 없으면 지금 묶음)
  const depIn = cur.hasCash ? depositsSince(model.allDeposits || Object.fromEntries(Object.entries(model.bundle?.deposits || {})
    .map(([k, v]) => ['b0:' + k, v.cancels ? { ...v, cancels: 'b0:' + v.cancels } : v])), cur.base || '', today) : [];
  if (depIn.length) cur.cash = Math.round((cur.cash + depIn.reduce((a, p) => a + p.amount, 0)) * 100) / 100;
  let mv = monthView(model.result, last ? last.session : '', today);
  // 첫 달 시연: 전략 비교가 출발했고 이번 달 점검 결정이 아직 없으며 일별 기록이 이번 달에 시작했으면(사용자 결정 10-22)
  if (mv && !mv.plan && model.bundle && !model.bundle.closed) mv = demoMonth(recs.find((r) => r.pipelineFull) || null, today.slice(0, 7), last ? last.session : '') || mv;
  // 20% 하락 매도 검토(원칙 4). 원칙 6에 걸리면 뺀다 — 카드 없는 종목은 지수 ETF만 본다(사용자 결정 10-22)
  const recStale = !!lastFull && recordGap(lastFull, today) > RECORD_STALE;   // 기록 자체가 묵었으면 사지도 팔지도 않는다(원칙 6)
  const losses = recStale ? [] : lossAlerts(cur.holdings, close).filter((l) => lossReviewable(l.ticker, lastFull, today));
  const lossOf = new Map(losses.map((l) => [l.ticker, l]));

  // 2026-10-21 최종 시안(Claude 안 + ChatGPT 안): 자산 요약 띠 → 왼쪽(다음 할 일·보유 자산) | 오른쪽(이번 달 운용·전략과 나란히).
  // 경고 문구는 페이지 맨 아래 한 번(html), 매매 기록 양식은 탭 줄의 "＋ 매매 기록"이 여는 창(어느 탭에서나).
  // 색은 종목에 고정: 7자리를 내 보유 평가액 큰 순으로 먼저 채우고, 남는 자리를 전략 보유 합산 큰 순으로 채운다
  let total = cur.cash, missing = [];
  for (const x of cur.holdings) { const c = closeNow(x.ticker); if (c == null) missing.push(x.ticker); else total += x.qty * c; }
  const myVal = new Map(cur.holdings.map((x) => { const c = closeNow(x.ticker); return [x.ticker, c == null ? 0 : x.qty * c]; }));
  const simW = new Map();
  for (const sc of model.result?.scenarios || []) if (sc.started) for (const t of Object.keys(sc.holdings)) { const c = close(t); simW.set(t, (simW.get(t) || 0) + (c == null ? 0 : sc.holdings[t] * c)); }
  const byVal = (m) => [...m.entries()].filter(([, v]) => v > 0).sort((a, b) => b[1] - a[1]).map(([t]) => t);   // 가격 없는 종목은 색 자리를 받지 않는다
  const named = [...new Set([...byVal(myVal), ...byVal(simW)])].slice(0, SLOTS).sort();
  const color = (t) => (t === '현금' ? 'var(--pf-cash)' : named.includes(t) ? `var(--pf-k${named.indexOf(t) + 1})` : 'var(--pf-other)');
  const has = cur.holdings.length || cur.hasCash;
  const real = model.result?.scenarios?.find((s) => s.id === 'REAL');
  // 띠는 수익률을 아는 마지막 날 기준(마지막 기록이 불완전해 그날 평가가 비면 그 전날 — 예: 10/21 pipelineFull false)
  const rs = real ? summarizeKnown(real) : null;

  // 매매 기록 창: 탭 줄의 "＋ 매매 기록"(html #pf-trade-open)과 아래 "후보로 매수 기록"이 연다
  const dlg = tradeDialog(model, handlers, recs, mv, today);
  const openBtn = document.getElementById('pf-trade-open');
  if (openBtn) openBtn.onclick = () => dlg.open();

  // 1) 자산 요약 띠
  const band = el('section', 'pf-panel pf-band');
  const cell = (k, v, sub, cls) => { const d = el('div', 'pf-bandcell'); d.appendChild(el('div', 'pf-k', k)); d.appendChild(el('div', 'pf-v' + (cls ? ' ' + cls : ''), v)); if (sub) d.appendChild(el('div', 'pf-s', sub)); band.appendChild(d); };
  cell('내 자산', has ? usd0(total) : '—', !has ? '기록·관리 탭에서 보유를 올리세요'
    : (cur.hasCash ? `주식 ${usd0(total - cur.cash)} · 현금 ${usd0(cur.cash)}` : '현금 모름(올린 보유에 현금 줄 없음)') + (missing.length ? ` · 가격 없음 ${missing.join(', ')}` : '')
      + (priceDays.size ? ` · ${[...priceDays].sort().map(md).join('·')} 종가` : ''));
  // 시작 전 실제 계좌 흐름(preStart)이 맞으면 그날부터 이어 붙인다(A안) — 전략 비교는 그대로 시작 스냅샷부터
  const pre = chainPreStart(model.main?.preStart, rs, model.bundle?.snapshot, real?.startValue);
  const ok = pre && !pre.why;
  cell('시작 뒤 수익률', ok ? pct(pre.twr) : rs?.twr != null ? pct(rs.twr) : '—',
    ok ? `${md(pre.from)}부터 · 내 실제 계좌(${md(rs.started)}까지는 Robinhood 기록)` : rs?.started ? `${md(rs.started)}부터 · 내 실제 계좌` + (pre?.why ? ` · ${md(model.main.preStart.from)} 기록 못 이음: ${pre.why}` : '') : '전략 비교를 시작하면 보입니다', 'pf-v-accent');
  cell('SPY 대비', ok ? (pre.vsSPY != null ? pp(pre.vsSPY) : '—') : rs?.vs?.SPY != null ? pp(rs.vs.SPY) : '—', rs?.asOf ? (ok ? `${md(pre.from)}부터 · ` : '') + `${md(rs.asOf)} 종가 기준` : lastFull ? `${md(lastFull.session)} 종가 기준` : '');
  root.appendChild(band);

  const grid = el('div', 'pf-homegrid');
  const left = el('div', 'pf-homecol pf-homemain'), right = el('div', 'pf-homecol pf-homeside');

  // 2) 이번 달, 다음 할 일
  const next = el('section', 'pf-panel pf-next');
  const na = nextAction(mv);
  const nh = el('div', 'pf-nexthead');
  const nt = el('div', 'pf-nextmain');
  const live = !!(mv?.plan && !mv.stale);   // 이번 달 계획이 있으면 아래에 돈·나누는 방법·후보 칸(buyBox)
  const eye = el('div', 'pf-eyerow'); eye.appendChild(el('div', 'pf-eyebrow2', '이번 달, 다음 할 일'));
  if (live && na.total) eye.appendChild(el('span', 'pf-badge', mv.demo ? `시연 · 실제 투자는 다음 달 점검부터` : `${na.total}회 중 ${na.done}회 진행`));
  nt.appendChild(eye);
  nt.appendChild(el('h2', 'pf-nexttitle', na ? na.title : !model.bundle || model.bundle.closed ? '전략 비교를 시작하세요' : '원칙 계산 출발 대기'));
  if (!live || !mv.next) nt.appendChild(el('p', 'pf-sub', na ? na.sub : !model.bundle || model.bundle.closed
    ? '기록·관리 탭에서 시작 스냅샷을 정하면 매달 점검일 결정과 회차 진행이 여기에 보입니다.'
    : '시작 스냅샷의 종목에 모두 그날 가격이 있어야 출발합니다(전략 비교 탭의 출발 대기 이유를 보세요).'));
  nh.appendChild(nt);
  const cands = mv?.plan && !mv.stale ? mv.plan.candidates : [];
  const buyBtn = el('button', 'pf-btn', '매매 기록'); buyBtn.type = 'button';
  buyBtn.addEventListener('click', () => dlg.open(cands[0]));
  if (!cands.length && !mv?.demo) nh.appendChild(buyBtn);   // 후보가 있으면 아래 줄마다 "기록" 버튼, 시연 달은 매매 기록 버튼 없음
  next.appendChild(nh);
  if (na && na.total) {
    const seg = el('div', 'pf-segs'); seg.setAttribute('role', 'img'); seg.setAttribute('aria-label', `${na.total}회 중 ${na.done}회 진행`);
    const nowAt = mv.steps.slice(1).findIndex((s) => s.state === 'todo');   // 다음 회차는 테두리만
    mv.steps.slice(1).forEach((s, i) => seg.appendChild(el('span', 'pf-seg-' + (i === nowAt && live ? 'now' : s.state))));
    next.appendChild(seg);
  }
  const buySlot = el('div', 'pf-buyslot'); next.appendChild(buySlot);
  for (const l of losses) {
    const w = el('div', 'pf-lossline');
    w.appendChild(el('strong', null, '매도 검토(20% 하락)'));
    w.appendChild(el('span', null, ` ${l.ticker} 평균 단가 대비 ${dropText(l.drop)} · 매도 검토를 시작합니다(원칙 4). 팔지·얼마나는 판정과 함께 직접 판단하세요.`));
    next.appendChild(w);
  }
  // 매도 검토(원칙 기준, 알림만 — 예전 '이번 달 운용' 칸에서 옮김)와 판정 방식이 바뀐 달 안내
  if (recStale) next.appendChild(el('p', 'pf-warn', `⚠ 마지막 완전한 기록이 ${md(lastFull.session)}로 ${recordGap(lastFull, today)}거래일 지났습니다. 새 기록이 올 때까지 사지도 팔지도 않습니다(원칙 6).`));
  if (live && mv.plan.ruleChanged) next.appendChild(el('p', 'pf-note', '판정 방식이 바뀐 달입니다. 전략 비교의 모의 계산은 이번 달 매매하지 않습니다(바뀐 판정으로 매도가 생기지 않게).'));
  // 판정 매도 검토도 지금 데이터가 원칙 6을 통과한 종목만(기록 묵음·종목별 묵음 — dr r3·r4). 목록과 건수가 같은 배열을 쓴다
  const sellAlerts = live && !recStale ? mv.alerts.filter((f) => !holdReason(lastFull?.cards?.[f.ticker], lastFull, today)) : [];
  for (const f of sellAlerts) {
    const w = el('div', 'pf-sellline');
    w.appendChild(el('strong', null, '매도 검토'));
    w.appendChild(el('span', null, ` ${f.ticker} ${f.observed} · ` + '팔지·얼마나는 직접 판단(원칙 4)'));
    next.appendChild(w);
  }
  // 넣은 돈(원칙 3): 모든 묶음의 입금 가운데 반영일이 이번 달(미국 동부)인 것 — 엔진·기록·관리 탭과 같은 반영일·취소 기준(dr r1)
  const month = today.slice(0, 7);
  const depMap = model.allDeposits || Object.fromEntries(Object.entries(model.bundle?.deposits || {})
    .map(([k, v]) => ['b0:' + k, v.cancels ? { ...v, cancels: 'b0:' + v.cancels } : v]));
  const deps = monthDeposits(depMap, month);
  const canDeposit = !!(model.bundle && !model.bundle.closed);   // 입금은 지금 묶음 문서에 쓴다
  const stats = el('div', 'pf-nextstats');
  const stat = (k, v) => { const s = el('span', null, k + ' '); s.appendChild(el('strong', null, v)); stats.appendChild(s); };
  // 매도 검토 = 판정(고평가·초고평가) 알림 + 20% 하락(원칙 4), 종목 기준
  const sellN = new Set([...sellAlerts.map((f) => f.ticker), ...losses.map((l) => l.ticker)]).size;
  if (live || sellN) stat('매도 검토', sellN ? sellN + '종목' : '없음');
  if (!live && !canDeposit) stat('이번 달 넣은 돈', deps.now.length ? usd0(deps.now.reduce((a, d) => a + d.amount, 0)) : '없음');
  stat('마지막 기록', last ? md(last.session) : '없음');
  next.appendChild(stats);
  // 계획이 있으면 돈·나누는 방법·후보(첫 달은 시연), 계획이 없으면 돈 칸 + 점검 미리 보기(사용자 결정 10-22 Q1·B안)
  if (live || canDeposit) {
    const rec = live ? recs.find((r) => r.session === mv.plan.record) : null;
    const planTier = (t) => rec?.cards?.[t]?.tier ?? null;   // 무게는 점검일 판정으로 고정(dr r1)
    // 지금 살 단계인가(원칙 1·6): 마지막 완전한 기록에서 판정이 살 단계·유효하고 가격이 묵지 않음 — 엔진 회차 재확인의 화면용 근사
    const nowHold = (t) => holdReason(lastFull?.cards?.[t], lastFull, today);   // 원칙 6 — 엔진 회차 재확인과 같은 판단 + 기록 자체의 묵음
    const nowBuyable = (t) => !nowHold(t) && BUY_PRINCIPLE.includes(lastFull.cards[t].tier);
    // 점검일 전 미리 보기(B안): 결정 대기면 이번 달, 아니면 다음 점검일(오늘 뒤 첫 '그달 첫 거래일')의 달을 목표로 한다
    // 목표 달과 점검일을 함께 정한다(dr): 이번 달 점검일이 아직 안 왔으면 이번 달, 지났는데 결정이 없으면(지연·결정 대기) 이번 달을 기다리고,
    // 이번 달 점검일이 전략 비교 시작 전이었으면(첫 달) 다음 달 점검일
    const S = cal().sessions, nextCheckAfter = (m) => S.find((d) => d.slice(0, 7) > m) || null;
    const thisCheck = S.find((d) => d.slice(0, 7) === month) || null;
    const startDay = model.bundle?.snapshot?.date || '';
    const firstMonth = !!thisCheck && thisCheck < today && startDay >= thisCheck && !mv?.plan;
    const waiting = !live && !!thisCheck && thisCheck <= today && !firstMonth;   // 이번 달 점검 결정 대기(지난달 계획 stale 또는 첫 결정 지연)
    const checkDay = live ? null : firstMonth ? nextCheckAfter(month) : thisCheck;
    const target = firstMonth && checkDay ? checkDay.slice(0, 7) : month;
    const preview = !live && !!lastFull && !recStale;
    buySlot.appendChild(buyBox({ model: { ...model, lastCards: lastFull?.cards }, handlers, mv: live ? mv : null, dlg, close, tierOf, planTier, hasRec: !!rec, nowBuyable, nowHold,
      waiting, preview, checkDay, month: target, today, deps: target === month ? deps : monthDeposits(depMap, target) }));
  } else buySlot.remove();
  left.appendChild(next);

  // 3) 보유 자산(비중 막대 + 접는 목록)
  const hold = el('section', 'pf-panel pf-side');
  const hh = el('h2', 'pf-h2s', '보유 자산 '); hh.appendChild(el('small', null, `${cur.holdings.length}종목`)); hold.appendChild(hh);
  const mine = new Map();
  for (const x of cur.holdings) { const v = myVal.get(x.ticker); if (!v) continue; const k = named.includes(x.ticker) ? x.ticker : '기타'; mine.set(k, (mine.get(k) || 0) + v); }
  // 조각 순서: 평가액 큰 순, 기타·현금은 끝
  const myParts = [...mine.entries()].filter(([t, v]) => v > 0 && t !== '기타').sort((a, b) => b[1] - a[1]);
  if (mine.get('기타') > 0) myParts.push(['기타', mine.get('기타')]);
  if (cur.hasCash && cur.cash > 0) myParts.push(['현금', cur.cash]);
  const myTot = myParts.reduce((a, [, v]) => a + v, 0);
  const share = (v, tot) => { const p = (v / tot) * 100; return p > 0 && p < 1 ? '<1%' : Math.round(p) + '%'; };
  if (myTot > 0) {
    const bar = el('div', 'pf-mix'); bar.setAttribute('role', 'img');
    bar.setAttribute('aria-label', '보유 비중: ' + myParts.map(([t, v]) => `${t} ${share(v, myTot)}`).join(', '));
    const leg = el('ul', 'pf-legend pf-mixleg');
    for (const [t, v] of myParts) {
      const p = share(v, myTot);
      const seg = el('i'); seg.style.flexGrow = String(v); seg.style.background = color(t === '기타' ? '__other' : t);
      seg.title = `${t} ${p} · ${usd0(v)}`; bar.appendChild(seg);
      const li = el('li'); const sw = el('i'); sw.style.background = seg.style.background; li.appendChild(sw); li.appendChild(el('span', null, `${t} ${p}`)); leg.appendChild(li);
    }
    hold.appendChild(bar); hold.appendChild(leg);
  } else if (!has) hold.appendChild(el('p', 'pf-note', '아직 올린 보유가 없습니다. 기록·관리 탭의 "보유 파일 올리기"로 올리세요.'));
  const fold = el('details', 'pf-holdfold');
  try { fold.open = sessionStorage.getItem('pf-holds-open') === '1'; } catch (_) { /* 기억 못 해도 접힌 채로 */ }
  fold.addEventListener('toggle', () => { try { sessionStorage.setItem('pf-holds-open', fold.open ? '1' : '0'); } catch (_) { /* 무시 */ } });
  fold.appendChild(el('summary', null, `보유 종목 ${cur.holdings.length}개 보기`));
  // 펼친 목록은 평가액 큰 순(가격 없는 종목은 끝), 10종목 넘으면 나머지는 한 번 더 접는다(사용자 결정 10-20)
  const list = el('div', 'pf-holds');
  const sorted = cur.holdings.slice().sort((a, b) => (myVal.get(b.ticker) || 0) - (myVal.get(a.ticker) || 0) || (a.ticker < b.ticker ? -1 : 1));
  let more = null;
  sorted.forEach((x, i) => {
    if (i === HOLD_SHOWN) {
      more = el('details', 'pf-holdfold pf-holdmore');
      more.appendChild(el('summary', null, `나머지 ${sorted.length - HOLD_SHOWN}종목 더 보기`));
      list.appendChild(more);
    }
    const c = closeNow(x.ticker), tier = tierOf(x.ticker);
    const row = el('div', 'pf-hold');
    const nm = el('div');
    const dot = el('i', 'pf-dot'); dot.style.background = color(x.ticker); nm.appendChild(dot);
    nm.appendChild(el('strong', null, x.ticker));
    nm.appendChild(el('small', null, [x.name, shares(x.qty) + '주', x.avgPrice ? '평균 ' + usd(x.avgPrice) : ''].filter(Boolean).join(' · ')));
    const loss = lossOf.get(x.ticker);
    if (loss) { const w = el('span', 'pf-loss', `⚠ 평균 대비 ${dropText(loss.drop)}`); w.title = `원칙 4 매도 검토(20% 하락): 평균 ${usd(loss.avgPrice)} → 종가 ${usd(loss.close)}`; nm.appendChild(w); }
    row.appendChild(nm);
    row.appendChild(el('span', 'pf-chip ' + (TIER_CLS[tier] || 'pf-t-none'), tier || '카드 없음'));
    row.appendChild(el('b', null, c == null ? '가격 없음' : usd0(x.qty * c)));
    (more || list).appendChild(row);
  });
  fold.appendChild(list);
  if (cur.holdings.length) hold.appendChild(fold);
  if (cur.hasCash && cur.cash < 0) hold.appendChild(el('p', 'pf-warn', `⚠ 현금이 ${usd0(cur.cash)}입니다. 빠진 입금이나 잘못 적은 매수가 없는지 확인하세요(막대는 현금을 빼고 그립니다).`));
  if (cur.clipped.length) hold.appendChild(el('p', 'pf-warn', `⚠ 보유보다 많이 판 기록 ${cur.clipped.length}건(${cur.clipped.map((c) => c.ticker + ' ' + shares(c.short) + '주').join(', ')})은 가진 만큼만 반영했습니다. 올린 보유나 빠진 매수 기록을 확인하세요.`));
  if (h.asOf) hold.appendChild(el('p', 'pf-note', `올린 보유 ${h.asOf} + 그 뒤 기록한 매매 ${cur.applied.length}건` + (depIn.length ? ` + 입금 ${depIn.length}건(오늘 반영분 포함)` : '')
    + (cur.future.length ? ` (미래 날짜 ${cur.future.length}건은 그날부터)` : '')));
  right.appendChild(hold);   // 보유 자산은 오른쪽 단(사용자 결정 10-22): 왼쪽은 할 일, 오른쪽은 현황

  // 4) 전략과 나란히(내 실제 계좌·1위·A). 예전 '이번 달 운용' 칸은 다음 할 일 카드와 겹쳐 뺐다(사용자 결정 10-22)
  right.appendChild(miniRank(model, handlers));
  grid.appendChild(left); grid.appendChild(right);
  root.appendChild(grid);
}

const kday = (d) => (d ? `${+d.slice(5, 7)}월 ${+d.slice(8, 10)}일` : '');
// 다음 할 일 카드의 제목·설명과 회차 진행(순수 함수, 시험이 부른다). mv = monthView 결과
export function nextAction(mv) {
  if (!mv) return null;
  if (!mv.plan) return { title: '첫 점검일을 기다리는 중', sub: '매달 1일(휴장이면 다음 거래일)에 살 후보를 정하고 나눠 삽니다.', done: 0, total: 0 };
  const rounds = mv.plan.rounds, total = rounds.length;
  const done = mv.steps.slice(1).filter((s) => s.state !== 'todo').length;
  const cands = mv.plan.candidates.length ? mv.plan.candidates.join(' · ') : '없음';
  if (mv.stale) return { title: '이번 달 결정 대기', sub: '점검일 정보가 오면 살 후보를 정합니다. 회차 막대는 지난달 계획입니다.', done, total };
  if (mv.next) return { title: `${kday(mv.next.date)}, ${rounds.indexOf(mv.next) + 1}번째 나눠 사기`, sub: `살 후보 ${cands} · ${total}회 중 ${done}회 진행`, done, total };
  return { title: '이번 달 회차 끝', sub: `살 후보 ${cands} · 다음 점검은 다음 달 1일(휴장이면 다음 거래일)`, done, total };
}

// 나누는 방법: 원칙으로 정하기 전이라 이 탭에서만 기억한다(sessionStorage). 저장소가 막혀도 메모리 값으로 동작한다(dr r1)
let buyMethod;
let pickSaving = false;
let demoPicks = [];   // 시연 달 체크(저장하지 않음, 이 탭에서만)   // 체크 저장 중이면 다시 그린 목록·방법 버튼도 잠근다(dr r2)
try { buyMethod = sessionStorage.getItem('pf-buy-method'); } catch (_) { /* 정하지 않음 */ }
if (!BUY_METHODS.some(([k]) => k === buyMethod)) buyMethod = null;

// 다음 할 일 카드 안의 "무엇을·얼마나"(2026-10-22 사용자 결정, 디자인 캔버스 최종안, dr r1 반영): 돈(쓸 돈 = 넣은 돈 + 지난달 판 돈, − 이번 달 산 돈 = 남은 돈, 더 넣을 돈),
// 나누는 방법(기본값 없음), 원칙 1·6을 통과한 살 후보(체크). 넣은 돈 = 반영일이 이번 달인 입금 기록(내 자산 현금·전략 비교에도 들어간다).
// 방법을 고르면 체크한 종목마다 이번 회차 금액(buyPlan — 남은 몫 ÷ 남은 회차)과 기록 버튼이 나온다.
// mv가 null이면(첫 점검일 전·이번 달 결정 대기) 돈 칸과 점검 미리 보기(previewSection)가 보인다(사용자 결정 10-22 Q1·B안).
function buyBox(args) {
  const { model, handlers, mv, dlg, close, tierOf, planTier, hasRec, nowBuyable, nowHold, today, deps } = args;
  const box = el('div', 'pf-buy');
  const month = args.month || today.slice(0, 7);   // 미리 보기면 다음 점검 달(그달 쓸 돈·체크)
  const ahead = month !== today.slice(0, 7);
  // 쓸 돈 = 반영일이 그달인 입금 + 그 전달에 판 돈(원칙 3·4). 그달에 판 돈은 다음 달 몫
  const soldPrev = monthSells(model.trades, prevMonth(month), today), soldNow = monthSells(model.trades, month, today);
  const deposited = Math.round(deps.now.reduce((a, d) => a + d.amount, 0) * 100) / 100;   // 그달 입금 − 그달 출금(음수일 수 있음)
  const budget = Math.max(0, Math.round((deposited + soldPrev) * 100) / 100);   // 쓸 돈 = 입금 − 출금 + 지난달 판 돈, 0 아래로 안 감(사용자 결정, dr)
  const bought = monthBuys(model.trades, month, today);
  const spent = Math.round([...bought.values()].reduce((a, b) => a + b.amount, 0) * 100) / 100;
  const leftUsd = Math.round((budget - spent) * 100) / 100;

  // 1) 돈: 쓸 돈 − 이번 달 산 돈 = 남은 돈(계획 전에는 쓸 돈만), 아래에 더 넣을 돈
  const money = el('div', 'pf-receipt');
  const cells = el('div', 'pf-receiptrow' + (mv ? '' : ' pf-receiptone'));
  const cell = (k, v, sub, cls) => { const d = el('div', 'pf-receiptcell' + (cls ? ' ' + cls : '')); d.appendChild(el('span', 'pf-k', k)); d.appendChild(el('strong', null, v)); d.appendChild(el('span', 'pf-s', sub)); cells.appendChild(d); };
  const laterSum = deps.later.reduce((a, d) => a + d.amount, 0);
  const later = (deps.later.length ? ` · 다음 달 이후 ${laterSum < 0 ? '출금 ' + usd0(-laterSum) : '몫 ' + usd0(laterSum)}(${deps.later.map((d) => md(d.day)).join('·')} 반영)` : '')
    + (soldNow > 0 ? ` · 이번 달 판 돈 ${usd0(soldNow)}은 다음 달 몫` : '');
  const parts = deps.now.map((d) => `${md(d.day)} ${d.amount < 0 ? '출금 ' + usd0(-d.amount) : usd0(d.amount)}` + (d.day > today ? ' 반영 예정' : ''));
  if (soldPrev > 0) parts.push(`${ahead ? '이번 달' : '지난달'} 판 돈 ${usd0(soldPrev)}`);
  cell(ahead ? `${+month.slice(5)}월 쓸 돈` : '쓸 돈', usd(budget), (parts.length ? parts.join(' · ') : `반영일(기록 다음 장 시작)이 ${ahead ? +month.slice(5) + '월' : '이번 달'}인 입금`) + later);
  if (mv) {
    cell('− 이번 달 산 돈', usd(spent), bought.size ? [...bought.keys()].join(' · ') : '아직 없음');
    cell('= 남은 돈', usd(Math.max(0, leftUsd)), leftUsd < 0 ? `쓸 돈보다 ${usd(-leftUsd)} 더 샀습니다` : '이 돈만 씁니다(원칙 3)', 'pf-receiptleft');
  }
  money.appendChild(cells);
  const f = el('div', 'pf-receiptadd');
  const lab = el('label'); lab.appendChild(el('span', null, budget > 0 ? '더 넣을 돈' : '넣을 돈'));
  const amt = el('input'); amt.type = 'number'; amt.min = '0.01'; amt.step = '0.01'; amt.placeholder = '$ 금액';
  lab.appendChild(amt); f.appendChild(lab);
  const save = el('button', 'pf-btn pf-btn-dark', '입금 기록'); save.type = 'button';
  const msg = msgLine();
  f.appendChild(save); money.appendChild(f); money.appendChild(msg);
  twoStep(save, msg, '이 금액을 입금으로 기록합니다. 맞으면 한 번 더 누르세요.', async () => {
    const v = Number(amt.value);
    if (!(v > 0) || Math.round(v * 100) / 100 !== v || v > 1e7) throw new Error('0보다 큰 금액을 센트 단위까지 넣으세요.');
    await handlers.deposit(v);
  }, f);
  box.appendChild(money);
  // 지금 기록하면 어느 달 몫인지(반영일 = 기록 다음 장 시작, 엔진과 같은 기준) — 시연 달·미리 보기에서 다음 달 돈을 넣으려는 경우를 위해(dr)
  const nowDay = depositTiming(new Date(model.now ?? Date.now()).toISOString()).day;
  const useMonth = mv?.demo ? nextMonthOf(month) : month;   // 시연 달이면 실제로 쓰는 것은 다음 달
  if (nowDay && (mv?.demo || ahead || nowDay.slice(0, 7) !== month)) {
    money.appendChild(el('p', 'pf-note pf-depnote', `지금 기록하면 반영일 ${md(nowDay)} → ${+nowDay.slice(5, 7)}월 몫입니다.`
      + (useMonth && nowDay.slice(0, 7) < useMonth ? ` ${+useMonth.slice(5)}월에 쓰려면 반영일이 ${+useMonth.slice(5)}월이어야 합니다(그달 첫 거래일 전날 장 마감 뒤 기록).` : '')));
  }
  if (!mv) {
    box.appendChild(el('p', 'pf-note', args.waiting ? `이번 달 점검(${md(args.checkDay)}) 결정이 오면 이 돈으로 살 후보를 확정합니다.` : `${md(args.checkDay)} 점검일에 이 돈으로 살 후보를 확정합니다. 주말에 넣어도 반영일이 ${+month.slice(5)}월이면 ${+month.slice(5)}월 몫입니다.`));
    if (args.preview) previewSection(args, box, month, budget);
    return box;
  }
  const { plan } = mv;
  if (!plan.candidates.length) { box.appendChild(el('p', 'pf-note', '이번 달 원칙 1·6을 통과한 살 후보가 없습니다.')); freshSection(args, box, plan, bought); return box; }

  // 2) 나누는 방법(기본값 없음 — 다시 누르면 끈다)
  const method = buyMethod;
  const active = plan.rounds.filter((r) => !r.dropped);   // 다음 점검일 뒤로 밀린 회차는 빼고 센다
  const rounds = active.length || 1;
  const roundsLeft = mv.next ? active.filter((r) => r.date >= mv.next.date).length : 0;
  const nextIdx = mv.next ? plan.rounds.indexOf(mv.next) + 1 : 0;   // 밀린(dropped) 회차는 늘 끝쪽이라 번호와 남은 회차가 어긋나지 않는다
  const mh = el('div', 'pf-buysechead');
  mh.appendChild(el('span', 'pf-buylabel', '나누는 방법'));
  const tiers = Object.fromEntries(plan.candidates.map((t) => [t, planTier(t)]));
  const picked = ((mv.demo ? demoPicks : model.picks?.[month]) || []).filter((t) => plan.candidates.includes(t));
  const bp = method ? buyPlan({ cands: plan.candidates, picked, budget, spent, bought: Object.fromEntries([...bought].map(([t, b]) => [t, b.amount])),
    tiers, caps: model.caps || {}, rounds, roundsLeft }) : null;
  mh.appendChild(el('span', 'pf-note', !method ? '아직 원칙으로 정하지 않음' : !mv.next ? '이번 달 회차 끝'
    : `(종목 달 몫 − 그 종목에 산 돈) ÷ 남은 회차 ${roundsLeft}회` + (bp?.capped[method] ? ' · 남은 돈에 맞춰 비례로 줄임' : '')
      + (method === 'cap' ? ' · 시총은 오늘 기준' : method === 'tier' ? ' · 무게는 점검일 판정 4:3:2:1' : '')));
  box.appendChild(mh);
  const seg = el('div', 'pf-buyseg'); seg.setAttribute('role', 'group'); seg.setAttribute('aria-label', '나누는 방법');
  for (const [k, t] of BUY_METHODS) {
    const btn = el('button', null, t); btn.type = 'button'; btn.setAttribute('aria-pressed', String(k === method)); btn.disabled = pickSaving;
    btn.addEventListener('click', () => {
      buyMethod = k === method ? null : k;
      try { if (buyMethod) sessionStorage.setItem('pf-buy-method', buyMethod); else sessionStorage.removeItem('pf-buy-method'); } catch (_) { /* 메모리 값으로 */ }
      const typed = amt.value; const nb = buyBox(args); box.replaceWith(nb);
      const ni = nb.querySelector('.pf-receiptadd input'); if (ni) ni.value = typed;   // 적던 입금액은 그대로
    });
    seg.appendChild(btn);
  }
  box.appendChild(seg);

  // 3) 내 기준대로 살 후보
  const lh = el('div', 'pf-buysechead');
  lh.appendChild(el('span', 'pf-buylabel', `내 기준대로 살 후보 ${plan.candidates.length}`));
  lh.appendChild(el('span', 'pf-note', mv.demo ? `시연 · ${md(plan.decisionDate)} 점검으로 보고 ${md(plan.record)} 첫 기록 판정 · 체크는 저장하지 않음` : `원칙 1·6 통과 · ${md(plan.decisionDate)} 점검 · 체크한 종목만 삽니다`));
  box.appendChild(lh);
  const list = el('div', 'pf-buylist');
  const pickMsg = msgLine();
  for (const t of plan.candidates) {
    const on = picked.includes(t);
    const row = el('label', 'pf-buyrow' + (on ? ' pf-on' : ''));
    const cb = el('input'); cb.type = 'checkbox'; cb.checked = on; cb.value = t; cb.disabled = pickSaving;
    // 저장하는 동안 목록 전체를 잠그고, 보낼 목록은 지금 화면의 체크 상태로 만든다(dr r1 — 연달아 누르면 앞 체크가 지워지던 문제)
    cb.addEventListener('change', async () => {
      const boxes = [...list.querySelectorAll('input[type=checkbox]')];
      const nx = boxes.filter((c) => c.checked).map((c) => c.value);
      if (mv.demo) { demoPicks = nx; box.replaceWith(buyBox(args)); return; }   // 시연 달 체크는 저장하지 않고 화면에서만(dr)
      const segBtns = [...seg.querySelectorAll('button')];
      pickSaving = true; [...boxes, ...segBtns].forEach((c) => { c.disabled = true; });
      pickMsg.textContent = '저장 중…';
      try { await handlers.pick?.(month, nx); pickMsg.textContent = ''; picked.splice(0, picked.length, ...nx); } catch (e) {
        boxes.forEach((c) => { c.checked = picked.includes(c.value); });
        pickMsg.textContent = e.message || '저장하지 못했습니다.';
      } finally {
        // 저장 중에 페이지가 다시 그려지면(실제 페이지는 저장 뒤 다시 불러와 그린 다음에야 끝난다) 잠긴 새 목록이 화면에 있다 —
        // 옛 요소와 지금 화면의 요소를 모두 푼다(dr r3)
        pickSaving = false;
        [...boxes, ...segBtns, ...document.querySelectorAll('.pf-buylist input[type=checkbox], .pf-buyseg button')].forEach((c) => { c.disabled = false; });
      }
    });
    row.appendChild(cb);
    const nm = el('span', 'pf-buyname');
    nm.appendChild(el('strong', null, t));
    nm.appendChild(el('span', 'pf-chip ' + (TIER_CLS[tiers[t]] || 'pf-t-none'), tiers[t] || '판정 없음'));
    const now = tierOf(t);
    if (now && now !== tiers[t]) nm.appendChild(el('span', 'pf-note', `지금 ${now}`));
    const b = bought.get(t);
    if (b) nm.appendChild(el('span', 'pf-note', `이번 달 ${usd0(b.amount)}(${shares(b.qty)}주) 삼`));
    row.appendChild(nm);
    const act = el('span', 'pf-buyact');
    const note = (x) => act.appendChild(el('span', 'pf-note', x));
    const c = close(t);
    if (!on) note('고르지 않음');
    else if (!mv.next) note('이번 달 회차 끝');
    else if (!nowBuyable(t)) note(nowHold(t) ? `${HOLD_TEXT[nowHold(t)] || '데이터 문제'} — 보류(원칙 6)` : '살 단계 벗어남 — 이번 회차 건너뜀(원칙 2)');
    else if (!bp) note('방법을 고르면 금액');
    else if (!(budget > 0)) note('쓸 돈 없음');
    else if (!bp.by[method]) note(method === 'cap' ? '시총 없는 종목이 있음' : !hasRec ? '점검일 기록이 없어 판정 가중을 못 씀' : '무게 밖 판정이 있음(초저평가~적정만)');
    else {
      const r = bp.round[method][t];
      if (!(r > 0)) note(bp.rest[method][t] > 0 ? '회차 몫 1센트 미만' : leftUsd <= 0 || bp.capped[method] ? '남은 돈 없음' : '달 몫을 다 샀음');
      else if (c == null) note(`${usd(r)} · 가격 없음`);
      else if (Math.floor((r / c) * 1e4) <= 0) note(`${usd(r)} · 0.0001주 미만`);
      else {
        const amtBox = el('span', 'pf-buyamt');
        amtBox.appendChild(el('strong', null, usd(r)));
        amtBox.appendChild(el('span', 'pf-s', `${nextIdx}회차 · 달 몫 ${usd0(bp.by[method][t])}` + (bp.missed[method].includes(t) ? ' · 놓친 몫 포함' : '')));
        act.appendChild(amtBox);
        if (!mv.demo) {   // 시연 달은 보여 주기만
          const go = el('button', 'pf-btn pf-btn-quiet', '기록'); go.type = 'button';
          go.title = '이 금액으로 매수 기록 창을 엽니다(예상 수량은 최근 종가로 계산, 체결 뒤 실제 값으로 고치세요)';
          go.addEventListener('click', (e) => { e.preventDefault(); dlg.open(t, { qty: Math.floor((r / c) * 1e4) / 1e4, price: c }); });
          act.appendChild(go);
        }
      }
    }
    row.appendChild(act);
    list.appendChild(row);
  }
  box.appendChild(list);
  box.appendChild(pickMsg);

  freshSection(args, box, plan, bought);
  return box;
}

// 점검일 전 미리 보기(사용자 결정 2026-10-22 B안): 첫 점검일 전·이번 달 결정 대기 때 지금 판정 기준 후보(원칙 1·6)를 체크 칸과 함께 보여 준다.
// 확정은 점검일에 한다. 체크는 그 점검 달(month) 몫으로 저장하고, 금액은 그달 쓸 돈을 4회로 나눈 회당 금액(회차 일정은 점검일에 생긴다)
function previewSection(args, box, month, budget) {
  const { model, handlers, tierOf, nowBuyable } = args;
  const cands = Object.keys(model.lastCards || {}).sort().filter((t) => nowBuyable(t));
  const ph = el('div', 'pf-buysechead');
  ph.appendChild(el('span', 'pf-buylabel', `${args.checkDay ? md(args.checkDay) + ' 점검 ' : ''}미리 보기 · 지금 판정 기준 후보 ${cands.length}`));
  ph.appendChild(el('span', 'pf-note', `원칙 1·6 통과 · 점검일에 확정 · 체크는 ${+month.slice(5)}월 몫으로 저장`));
  box.appendChild(ph);
  if (!cands.length) { box.appendChild(el('p', 'pf-note', '지금 판정으로는 살 단계인 종목이 없습니다.')); return; }
  const method = buyMethod;
  const seg = el('div', 'pf-buyseg'); seg.setAttribute('role', 'group'); seg.setAttribute('aria-label', '나누는 방법');
  for (const [k, t] of BUY_METHODS) {
    const btn = el('button', null, t); btn.type = 'button'; btn.setAttribute('aria-pressed', String(k === method)); btn.disabled = pickSaving;
    btn.addEventListener('click', () => {
      buyMethod = k === method ? null : k;
      try { if (buyMethod) sessionStorage.setItem('pf-buy-method', buyMethod); else sessionStorage.removeItem('pf-buy-method'); } catch (_) { /* 메모리 값으로 */ }
      const typed = box.querySelector('.pf-receiptadd input')?.value || ''; const nb = buyBox(args); box.replaceWith(nb);
      const ni = nb.querySelector('.pf-receiptadd input'); if (ni) ni.value = typed;
    });
    seg.appendChild(btn);
  }
  box.appendChild(seg);
  const picked = (model.picks?.[month] || []).filter((t) => cands.includes(t));
  const tiers = Object.fromEntries(cands.map((t) => [t, tierOf(t)]));
  const bp = method ? buyPlan({ cands, picked, budget, tiers, caps: model.caps || {}, rounds: 4, roundsLeft: 4 }) : null;
  const list = el('div', 'pf-buylist');
  const pickMsg = msgLine();
  for (const t of cands) {
    const on = picked.includes(t);
    const row = el('label', 'pf-buyrow' + (on ? ' pf-on' : ''));
    const cb = el('input'); cb.type = 'checkbox'; cb.checked = on; cb.value = t; cb.disabled = pickSaving;
    cb.addEventListener('change', async () => {
      const boxes = [...list.querySelectorAll('input[type=checkbox]')], segBtns = [...seg.querySelectorAll('button')];
      const nx = boxes.filter((c) => c.checked).map((c) => c.value);
      pickSaving = true; [...boxes, ...segBtns].forEach((c) => { c.disabled = true; });
      pickMsg.textContent = '저장 중…';
      try { await handlers.pick?.(month, nx); pickMsg.textContent = ''; picked.splice(0, picked.length, ...nx); } catch (e) {
        boxes.forEach((c) => { c.checked = picked.includes(c.value); });
        pickMsg.textContent = e.message || '저장하지 못했습니다.';
      } finally {
        pickSaving = false;
        [...boxes, ...segBtns, ...document.querySelectorAll('.pf-buylist input[type=checkbox], .pf-buyseg button')].forEach((c) => { c.disabled = false; });
      }
    });
    row.appendChild(cb);
    const nm = el('span', 'pf-buyname'); nm.appendChild(el('strong', null, t));
    nm.appendChild(el('span', 'pf-chip ' + (TIER_CLS[tiers[t]] || 'pf-t-none'), tiers[t]));
    row.appendChild(nm);
    const act = el('span', 'pf-buyact');
    const note = (x) => act.appendChild(el('span', 'pf-note', x));
    if (!on) note('고르지 않음');
    else if (!bp) note('방법을 고르면 금액');
    else if (!(budget > 0)) note(`${+month.slice(5)}월 쓸 돈 없음`);
    else if (!bp.by[method]) note(method === 'cap' ? '시총 없는 종목이 있음' : '무게 밖 판정이 있음(초저평가~적정만)');
    else {
      const amtBox = el('span', 'pf-buyamt');
      amtBox.appendChild(el('strong', null, usd(bp.round[method][t])));
      amtBox.appendChild(el('span', 'pf-s', `회당(4회) · 달 몫 ${usd0(bp.by[method][t])}`));
      act.appendChild(amtBox);
    }
    row.appendChild(act);
    list.appendChild(row);
  }
  box.appendChild(list);
  box.appendChild(pickMsg);
}

// 주간 확인(원칙 2·6): 점검일 뒤 살 단계에 든 종목 — 보여 주기만, 살지는 사용자가 판단(사면 그달 남은 돈에서). 회차가 남았을 때만
function freshSection({ model, mv, dlg, tierOf, nowBuyable }, box, plan, bought) {
  const fresh = Object.keys(model.lastCards || {}).sort().filter((t) => !plan.candidates.includes(t) && nowBuyable(t));
  if (!fresh.length || !mv.next) return;
  const fh = el('div', 'pf-buysechead');
  fh.appendChild(el('span', 'pf-buylabel', `주간 확인 · 점검일 뒤 살 단계에 든 종목 ${fresh.length}`));
  fh.appendChild(el('span', 'pf-note', '살지는 직접 판단 · 사면 그달 남은 돈에서(원칙 2·6)'));
  box.appendChild(fh);
  const fl = el('div', 'pf-buylist');
  for (const t of fresh) {
    const row = el('div', 'pf-buyrow pf-freshrow');
    row.appendChild(el('span'));
    const nm = el('span', 'pf-buyname'); nm.appendChild(el('strong', null, t));
    nm.appendChild(el('span', 'pf-chip ' + (TIER_CLS[tierOf(t)] || 'pf-t-none'), tierOf(t)));
    const b = bought.get(t);
    if (b) nm.appendChild(el('span', 'pf-note', `이번 달 ${usd0(b.amount)}(${shares(b.qty)}주) 삼`));
    row.appendChild(nm);
    const act = el('span', 'pf-buyact');
    if (!mv.demo) { const go = el('button', 'pf-btn pf-btn-quiet', '기록'); go.type = 'button'; go.addEventListener('click', () => dlg.open(t)); act.appendChild(go); }
    row.appendChild(act);
    fl.appendChild(row);
  }
  box.appendChild(fl);
}

// 매매 기록 창(<dialog>). 한 페이지에 하나만 두고 그릴 때마다 내용을 바꾼다. open(ticker)는 그 종목·매수로 채워 연다
function tradeDialog(model, handlers, recs, mv, today) {
  let dlg = document.getElementById('pf-tradedlg');
  if (!dlg) { dlg = el('dialog', 'pf-dialog'); dlg.id = 'pf-tradedlg'; dlg.setAttribute('aria-labelledby', 'pf-tradedlg-h'); document.body.appendChild(dlg); }
  dlg.textContent = '';
  const box = tradeForm(model, handlers, recs, mv, today, () => dlg.close());
  const x = el('button', 'pf-btn pf-btn-quiet pf-dlgclose', '닫기'); x.type = 'button'; x.addEventListener('click', () => dlg.close());
  box.insertBefore(x, box.firstChild);
  dlg.appendChild(box);
  return { open: (ticker, pre) => { box.fill?.(ticker, pre); if (!dlg.open) dlg.showModal?.(); } };
}

function tradeForm(model, handlers, recs, mv, today, done) {
  const box = el('div', 'pf-tradebox');
  const hd = el('h2', 'pf-h2', '실제 매매 기록'); hd.id = 'pf-tradedlg-h'; box.appendChild(hd);
  box.appendChild(el('p', 'pf-note', '실제로 사고판 것을 적으면 내 자산과 전략 비교의 "내 실제 계좌" 줄에 들어갑니다. 잘못 적었으면 기록·관리 탭에서 고치거나 지웁니다.'));
  const f = el('div', 'pf-form pf-tradeform');
  const field = (lab, input) => { const l = el('label', 'pf-field'); l.appendChild(el('span', null, lab)); l.appendChild(input); f.appendChild(l); return input; };
  const date = field('날짜(체결일, 미국 동부)', el('input')); date.type = 'date';
  date.value = today; date.max = today;
  const side = field('매매', el('select'));
  for (const [v, t] of [['buy', '매수'], ['sell', '매도']]) { const o = el('option', null, t); o.value = v; side.appendChild(o); }
  const tick = field('종목(티커)', el('input')); tick.setAttribute('list', 'pf-tickers'); tick.className = 'pf-ticker'; tick.autocomplete = 'off';
  const dl = el('datalist'); dl.id = 'pf-tickers';
  const last = recs[recs.length - 1];
  const cands = mv?.plan && !mv.stale ? mv.plan.candidates : [];
  const names = [...new Set([...cands, ...Object.keys(last?.cards || {}).sort()])];
  for (const t of names) { const o = el('option'); o.value = t; if (cands.includes(t)) o.label = '이번 달 살 후보'; dl.appendChild(o); }
  f.appendChild(dl);
  if (cands.length) {
    const quick = el('div', 'pf-row');
    quick.appendChild(el('span', 'pf-note', '이번 달 살 후보:'));
    for (const t of cands) { const b = el('button', 'pf-btn pf-btn-quiet', t); b.type = 'button'; b.addEventListener('click', () => { tick.value = t; side.value = 'buy'; }); quick.appendChild(b); }
    f.appendChild(quick);
  }
  const qty = field('수량(주, 소수 가능)', el('input')); qty.type = 'number'; qty.min = '0'; qty.step = 'any';
  const price = field('체결가(USD)', el('input')); price.type = 'number'; price.min = '0'; price.step = '0.0001';
  const btn = el('button', 'pf-btn', '기록'); btn.type = 'button';
  const msg = msgLine();
  f.appendChild(btn); f.appendChild(msg);
  twoStep(btn, msg, '이대로 기록합니다. 맞으면 한 번 더 누르세요.', async () => {
    const x = { date: date.value, ticker: tick.value.trim().toUpperCase(), side: side.value, qty: Number(qty.value), price: Number(price.value) };
    const bad = checkTrade(x, etDate(Date.now()));
    if (bad) throw new Error(bad);
    await handlers.trade(x);
    done?.();
  }, f);
  box.appendChild(f);
  box.fill = (t, pre) => { if (t) { tick.value = t; side.value = 'buy'; } if (pre) { qty.value = String(pre.qty); price.value = String(pre.price); } };
  return box;
}

// 전략과 나란히: 내 실제 계좌, 만든 전략 위 두 개(없으면 SPY) — 누르면 전략 비교 탭으로. A는 숨긴다(사용자 결정 2026-10-22)
function miniRank(model, handlers) {
  const sec = el('section', 'pf-panel pf-side');
  const head = el('div', 'pf-sidehead'); head.appendChild(el('h2', 'pf-h2s', '전략과 나란히'));
  const go = el('button', 'pf-linkbtn', '전체'); go.type = 'button'; go.addEventListener('click', () => handlers.goto('strategy')); head.appendChild(go);
  sec.appendChild(head);
  const sc = (model.result?.scenarios || []).map((s) => ({ s, m: summarizeKnown(s) })).filter(({ m }) => m.twr != null);
  if (!sc.length) { sec.appendChild(el('p', 'pf-note', '전략 비교가 출발하면 내 실제 계좌와 다른 전략의 수익률이 여기에 보입니다.')); return sec; }
  // A(그대로 보유)는 계산의 기준선이라 화면에 보이지 않는다(사용자 결정 2026-10-22). 내 실제 계좌 + 만든 전략 가운데 위 두 개, 만든 전략이 없으면 SPY
  const real = sc.find(({ s }) => s.id === 'REAL');
  const mine = sc.filter(({ s }) => s.id !== 'REAL' && s.id !== 'A').sort((a, b) => b.m.twr - a.m.twr).slice(0, 2);
  const rows = [real, ...mine.map((r, i) => (i === 0 && mine.length > 1 ? { ...r, top: true } : r))].filter(Boolean);
  if (!mine.length && real?.m.vs?.SPY != null) rows.push({ s: { id: 'SPY' }, m: { twr: real.m.twr - real.m.vs.SPY / 100 }, name: 'SPY(같은 날 시작)' });
  const max = Math.max(...rows.map(({ m }) => Math.abs(m.twr)), 0.0001);
  for (const r of rows) {
    const d = el('div', 'pf-minirow' + (r.s.id === 'REAL' ? ' pf-mine' : ''));
    d.appendChild(el('span', null, (r.name || label(r.s, model.byId)) + (r.top ? ' (1위)' : '')));
    d.appendChild(el('strong', null, pct(r.m.twr)));
    const b = el('i'); const f = el('b'); f.style.width = Math.round((Math.abs(r.m.twr) / max) * 100) + '%'; b.appendChild(f); d.appendChild(b);
    sec.appendChild(d);
  }
  return sec;
}

const HOLD_SHOWN = 10;   // 펼친 보유 목록에 바로 보이는 종목 수
const SLOTS = 7;   // 종목 색 7개(검증된 팔레트) + 현금 회색. 8번째 종목부터는 '기타'로 묶는다

// 세 하위 탭(한눈에·전략 비교·기록·관리)을 한 번에 그린다. preview-only-portfolio.js와 화면 시험 페이지가 같이 쓴다.
// model = renderHome과 같음, smodel = { bundle, bundleNo, closedCount, records, recordsError, calcError, holdingsRows }
export function renderTabs(roots, model, smodel, handlers) {
  renderHome(roots.home, model, handlers);
  const st = roots.strategy, { result } = model, recs = smodel.records || [];
  st.textContent = '';
  const lastRec = recs.length ? recs[recs.length - 1].session : null;
  if (smodel.recordsError) st.appendChild(el('p', 'pf-warn', '일별 기록을 불러오지 못했습니다. 새로고침해 보세요.'));
  else if (smodel.calcError) st.appendChild(el('p', 'pf-warn', '계산하지 못했습니다: ' + smodel.calcError));
  else if (!result && !(smodel.bundle && !smodel.bundle.closed)) st.appendChild(el('p', 'pf-note', '전략 비교를 시작하면(기록·관리 탭의 시작 스냅샷) 여기에 비교 표·그래프·매매 기록이 보입니다.'));
  // 순위·편집기·내 전략 카드·접은 표(2026-10-21 디자인 시안 선택 — -rank.js). 모형 설명은 순위 제목 옆 "?"에서 펼친다
  const info = result ? `큰 사건 예외를 뺀 정기 운용 모형 · 엔진 ${ENGINE_VERSION} · 마지막 기록 ${lastRec} · 빠진 날 ${result.missingSessions.length}일` : '';
  // A(그대로 보유)는 화면에서 숨긴다 — 계산(다른 전략 출발점·SPY 기준선)에는 그대로 쓰므로 baseA로 넘긴다(사용자 결정 2026-10-22)
  const shown = result ? { ...result, scenarios: result.scenarios.filter((s) => s.id !== 'A'), baseA: result.scenarios.find((s) => s.id === 'A') || null } : null;
  renderStrategy(st, smodel.recordsError || smodel.calcError ? { ...model, result: null } : { ...model, result: shown }, { ...smodel, info }, handlers);
  // 시작 폼 미리 채우기: 내 자산과 같은 계산으로 마지막 기록일까지(그 뒤 매매는 빼고)
  const hh = model.main?.holdings || {};
  const pc = currentHoldings(hh.rows, hh.asOf, model.trades, lastRec || etDate(model.now ?? Date.now()));
  smodel = { ...smodel, prefill: { asOf: hh.asOf || null, upTo: lastRec, holdings: pc.holdings, cash: pc.hasCash ? pc.cash : null, clipped: pc.clipped } };
  // 기록·관리: 모든 기록 한 줄 타임라인(2026-10-21 디자인 시안 선택 — -records.js)
  renderManage(roots.manage, model, smodel, handlers, { currentHoldings, checkTrade, etDate });
}
