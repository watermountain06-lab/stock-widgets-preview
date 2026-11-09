// preview 전용 Portfolio 탭 — "한눈에" 하위 탭(2026-10-20, 시안 A2 사용자 선택). 라이브로 옮기지 않는다 — pipeline/site_ui/UI_DIFF.md 1절 portfolio.
//
// 내 자산(올린 보유 + 그 뒤 기록한 실제 매매), 실제 매매 기록 칸, 이번 달 할 일, 이번 달 운용(점검일 결정과 회차 진행),
// 전략 비교 도넛(전략마다 지금 들고 있는 종목·현금 비중, 가운데 수익률)을 그린다. 계산은 엔진 결과(replay)를 받아 쓰고,
// 저장은 preview-only-portfolio.js가 넘겨 준 handlers로 한다. 순수 함수(currentHoldings·monthView)는 node 시험이 부른다
// (pipeline/portfolio/test_strategy_view.mjs). 실제 매매 기록은 모의 전략 계산에는 넣지 않고, 전략 비교의 "내 실제 계좌" 줄만 쓴다(preview-only-portfolio-actual.js).
import { el, twoStep, msgLine, usd, pct, pp, shares, label, summarize } from './preview-only-portfolio-strategy.js?v=27';
import { renderStrategy } from './preview-only-portfolio-rank.js?v=20';
import { renderManage } from './preview-only-portfolio-records.js?v=16';
import { ENGINE_VERSION, principleFor, tierWeights, PRINCIPLE_FROM, CASH_FROM, cashTarget, PRINCIPLE_SELL, PICK_FROM, PICK_FROM_ROUND, PICK_MAX, pickTop, _internal, depositTiming, twr as engineTwr } from './preview-only-portfolio-engine.js?v=13';
import { effectiveDeposits, actualAccount } from './preview-only-portfolio-actual.js?v=18';
import { ledgerActive, ledgerDeposits, incomeList, kwState, tradesOf, acctOf, RH, KW, fxSeries, krwPerformance } from './preview-only-portfolio-accounts.js?v=7';
import { renderAccounts } from './preview-only-portfolio-acctview.js?v=7';

// 미국 동부 날짜(YYYY-MM-DD). 매매 기록 칸의 기본값·미래 날짜 검사와 '이번 달' 판단에 쓴다.
export const etDate = (ms) => new Intl.DateTimeFormat('en-CA', { timeZone: 'America/New_York', year: 'numeric', month: '2-digit', day: '2-digit' }).format(new Date(ms));
const shareTxt = (r, c) => { const n = c > 0 && r > 0 ? Math.floor((r / c) * 100 + 1e-9) / 100 : 0; return n > 0 ? `약 ${n.toLocaleString('en-US', { maximumFractionDigits: 2 })}주 · ` : c > 0 && r > 0 ? '0.01주 미만 · ' : ''; };   // 보여 주기만(계산은 돈으로)
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

// 매주 판정 매도(원칙 4, 2026-10-28 사용자 결정 — 11월 계획부터): 실제 보유(계좌별)를 마지막 완전한 기록의 판정으로 보고
// 고평가면 전부를 그달 남은 회차(다음 회차 포함)에 나눠, 초고평가면 남은 것 전부를 이번 회차에 판다. 고평가~적정 이하로 내려오면 줄이 사라진다(멈춤).
// 놓친 회차는 남은 보유를 남은 회차로 다시 나눈다. 같은 회차에 이미 판 것은 그 회차 몫에서 뺀다(dr — 기록 뒤 몫이 다시 커지지 않게).
// 수량 단위: 보유·판 것이 모두 정수 주면 정수로 올림, 아니면 소수 6자리 올림(dr r1 — 내림이면 적은 보유가 앞 회차에 0주가 된다), 몫이 남은 보유를
// 넘지 않게. 마지막 회차·초고평가는 지금 보유 전부(dr r1). 계좌가 다르면 따로 계산한다. 전략 비교에서 '그대로 두는 보유'(holdOnly)는 빼고(엔진과 같게, dr r1)
// holdings: [{ticker, qty, account}], rounds: 그달 회차 날짜(오름차순), lastSession: 판정을 본 기록 날짜(마지막 완전한 기록), trades: 실제 매매 지도
export function weeklySells({ holdings, rec, today, rounds, lastSession, trades, holdOnly = [] }) {
  if (!rec) return [];
  const nextDate = (rounds || []).find((d) => d > (lastSession || '')) || null;
  const real = Object.entries(trades || {});
  const cancelled = new Set(real.filter(([, x]) => x.cancels).map(([, x]) => x.cancels));
  const out = [];
  for (const h of holdings || []) {
    if (!(h.qty > 1e-9) || holdOnly.includes(h.ticker)) continue;
    const card = rec.cards?.[h.ticker];
    if (!card || holdReason(card, rec, today)) continue;
    if (!PRINCIPLE_SELL.includes(card.tier)) continue;   // 고평가부터 판다(원칙 4, 2026-11-03 되돌림 — 고평가~적정은 보유)
    const base = { ticker: h.ticker, account: h.account, tier: card.tier, round: nextDate };
    if (!nextDate) { out.push({ ...base, shares: null, remaining: 0 }); continue; }   // 이번 달 회차 끝 — 다음 점검일에 다시
    const soldSince = real.filter(([id, x]) => !x.cancels && !cancelled.has(id) && x.side === 'sell' && x.ticker === h.ticker
      && acctOf(x) === h.account && x.date >= nextDate && x.date <= today).reduce((a, [, x]) => a + x.qty, 0);
    const remaining = rounds.filter((d) => d >= nextDate).length;
    const start = h.qty + soldSince;
    const all = card.tier === '초고평가' || remaining <= 1;
    const isInt = (v) => Math.abs(v - Math.round(v)) < 1e-9;
    const whole = isInt(h.qty) && isInt(soldSince);
    const up = (v) => (whole ? Math.ceil(v - 1e-9) : Math.ceil(v * 1e6 - 1e-6) / 1e6);
    const left = all ? h.qty : Math.max(0, Math.min(h.qty, up(start / remaining) - soldSince));
    out.push({ ...base, shares: Math.round(left * 1e6) / 1e6, remaining, sold: soldSince, all });
  }
  return out.sort((a, b) => (a.ticker < b.ticker ? -1 : a.ticker > b.ticker ? 1 : a.account < b.account ? -1 : 1));
}
// 판정이 묵은 보유(원칙 6, 사용자 결정 2026-10-29): 카드는 있는데 판정이 없거나 가격·판정 날짜가 묵어 판정으로 사고팔 수 없는 보유.
// 알림 칸에 '확인 필요'로 보여 준다. 카드가 없는 종목은 넣지 않는다(사용자 결정). 기록 자체가 묵었으면(recordStale) 칸 위 경고 한 줄로 충분해 뺀다
export function staleHoldings({ holdings, rec, today, holdOnly = [] }) {
  if (!rec) return [];
  const out = [];
  for (const h of holdings || []) {
    if (!(h.qty > 1e-9) || holdOnly.includes(h.ticker) || !rec.cards?.[h.ticker]) continue;
    const why = holdReason(rec.cards[h.ticker], rec, today);
    if (why && why !== 'recordStale' && why !== 'noCard') out.push({ ticker: h.ticker, account: h.account, why });
  }
  return out.sort((a, b) => (a.ticker < b.ticker ? -1 : a.ticker > b.ticker ? 1 : a.account < b.account ? -1 : 1));
}
// 매도 안내에 쓸 회차: 마지막 완전한 기록 뒤 회차가 이번 달에 남았으면 이번 달, 아니면 다음 달 회차(10월에도 11/02부터 미리 보여 줌, 2026-10-29)
export function sellRounds(month, ref) {
  const nm = (m) => { const [y, mo] = m.split('-').map(Number); return mo === 12 ? `${y + 1}-01` : `${y}-${String(mo + 1).padStart(2, '0')}`; };
  const cur = monthRounds(month);
  return cur.some((d) => d > ref) ? cur : monthRounds(nm(month));
}
// 환전 기록의 몫 달(2026-11-03 고침 — 입금 칸과 같은 규칙): 반영일 달에 남은 회차가 있으면 그 달, 없으면 다음 달.
// 그 달 계획(planM)이 있으면 계획의 회차(밀린 회차 제외)로, 아직 없으면(점검 전·첫 달 시연) 원칙 2 회차 날짜로 본다.
// 예전에는 계획이 없으면 무조건 반영일 달 몫이라, 10/27 환전(10/29 반영)이 회차가 이미 끝난 10월 몫이 되어 11월 한도에서 빠졌다
// 계획이 지난달 것이면(이번 달 점검 결정 대기) 입금 칸처럼 그 달 몫 — 결정이 늦어져 원칙 2 회차 날짜가 다 지나도 결정 뒤 회차에서 쓴다(dr Fable)
// 현금 10% 목표(원칙 3·5, 2026-11-03): 목표 = 총자산의 10%(센트 반올림, 엔진 cashTarget과 같은 셈), 남은 한도 = max(0, 현금 − 목표 − 이번 달 판 돈 − 다음 달 몫 미리 넣은 돈)
// 현금·총자산을 모르거나 가격 없는 보유가 있으면(missing > 0) 목표를 몰라 한도를 막는다(dr — 엔진의 '평가액 모름 → 그달 안 삼'과 같게). laterOut = 아직 안 나간 출금 예정
export function cashLeft({ cash, total, soldNow = 0, laterIn = 0, laterOut = 0, missing = 0 }) {
  if (!Number.isFinite(cash) || !Number.isFinite(total) || missing > 0) return { target: null, left: 0, short: 0, unknown: true };
  const c = (v) => Math.round((v || 0) * 100);
  const target = cashTarget(c(total));
  const left = Math.max(0, c(cash) - target - c(soldNow) - c(laterIn) - Math.abs(c(laterOut)));   // 출금 예정은 부호와 상관없이 뺀다(dr)
  return { target: target / 100, left: left / 100, short: Math.max(0, target - c(cash)) / 100, unknown: false };
}
export function ledgerMonth(dEff, planM, planRounds) {
  const m = dEff.slice(0, 7);
  if (planM && planM < m) return m;
  const left = planM === m ? (planRounds || []).some((r) => !r.dropped && r.date >= dEff) : monthRounds(m).some((d) => d >= dEff);
  const [y, n] = m.split('-').map(Number);
  return left ? m : nextMonthOf(m) || (n === 12 ? `${y + 1}-01` : `${y}-${String(n + 1).padStart(2, '0')}`);   // 달력 끝이어도 다음 달(dr Codex)
}
// 그달 회차 날짜(원칙 2): 첫 거래일부터 매주 같은 요일, 휴장이면 다음 거래일, 4회
export function monthRounds(month) {
  const S = cal().sessions;
  const d0 = S.find((d) => d.slice(0, 7) === month);
  if (!d0) return [];
  const plus = (d, n) => new Date(Date.parse(d + 'T12:00:00Z') + n * 864e5).toISOString().slice(0, 10);
  return [0, 1, 2, 3].map((k) => S.find((d) => d >= plus(d0, 7 * k))).filter(Boolean);
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
  // 계좌 현금 칸은 기록한 날부터 더한다(2026-10-25 사용자 결정 "바로 더하기") — 전략 비교는 반영일 그대로
  // 올린 보유 기준일도 기록일로 비교한다 — 기준일까지 기록한 입금은 올린 현금에 이미 들어 있다고 본다(dr)
  for (const deps of byBundle.values()) for (const p of effectiveDeposits(deps)) { const d0 = p.rec || p.day; if (d0 > base && d0 <= today) out.push(p); }
  return out.sort((x, y) => (x.day < y.day ? -1 : 1));
}

// 원칙 3 매수 금액(2026-10-22 사용자 결정, dr r1 반영 — 예전 초안 '원칙 10'): 그달 넣은 돈(+지난달 판 돈)만 쓰고, 카드가 보여 준 구매 후보 중 내가 고른 종목에 나눠 산다.
// 나누는 방법은 균등·시총 비중(시가총액 비례)·판정 가중(등급 무게 — 엔진 tierWeights: 옛 판 4:3:2:1, 11월 계획부터 3:2:1) 가운데 고른다(기본값 없음).
// 놓친 회차(사용자 결정 10-22 Q2): 이번 회차 금액 = (그 종목 달 몫 − 이번 달 그 종목에 산 돈) ÷ 남은 회차 수(이번 회차 포함).
// 모든 종목의 남은 몫 합은 남은 돈(쓸 돈 − 이번 달 산 돈 전부)을 넘지 않게 비례로 줄인다. 계산은 끝까지 센트 정수(내림 — 남는 센트는 쓰지 않는다).
// budget·spent·bought 값은 달러. 고른 것 가운데 무게가 없는 종목(시총 없음·무게 밖 판정)이 있으면 그 방법은 null.
// 돌려주는 값(모두 방법별): by(달 몫)·rest(남은 몫)·round(이번 회차 금액, 남은 회차 0이면 null) {티커: 달러}, missed(지난 회차 계획보다 덜 산 종목), capped(남은 돈에 맞춰 줄임).
export const BUY_METHODS = [['equal', '균등'], ['cap', '시총 비중'], ['tier', '판정 가중']];
// 후보 줄 순서(사용자 요청 2026-10-25): 시가총액 큰 순, 시총을 모르는 종목은 맨 뒤 티커순 — 보여 주는 순서만, 계산과 무관
export const byCap = (list, caps = {}) => [...list].sort((a, b) => (caps[b] || 0) - (caps[a] || 0) || (a < b ? -1 : 1));
const toC = (v) => Math.max(0, Math.round((v || 0) * 100));
// a × b ÷ c 내림을 정확히(정수만, BigInt — 실수 비율로 하면 3/11 같은 무게에서 1센트가 빠진다, dr r2)
const mulDiv = (a, b, c) => Number((BigInt(a) * BigInt(b)) / BigInt(c));
export function buyPlan({ cands, picked, budget, spent = 0, bought = {}, boughtNow = {}, tiers = {}, caps = {}, rounds = 4, roundsLeft = rounds, weights = tierWeights('9999-12') }) {
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
    // 회차 금액은 회차가 시작될 때 고정(사용자 결정 2026-11-09): 이번 회차에 산 돈(boughtNow)을 빼기 전 남은 몫 ÷ 남은 회차.
    // 예전에는 산 뒤 남은 몫을 다시 나눠 같은 회차 금액이 줄었다($333.5 사고 나면 $667÷3 = $222.3). todo = 이번 회차에 더 살 돈
    const nowC = Object.fromEntries(Object.entries(boughtNow).map(([t, v]) => [t, toC(v)])), nowAll = Object.values(nowC).reduce((a, b) => a + b, 0);
    const left0 = Math.min(cents, left + nowAll);
    let rest0 = Object.fromEntries(sel.map((t) => [t, Math.max(0, share[t] - toC(bought[t]) + (nowC[t] || 0))]));
    const sum0 = sel.reduce((a, t) => a + rest0[t], 0);
    if (sum0 > left0) rest0 = Object.fromEntries(sel.map((t) => [t, mulDiv(rest0[t], left0, sum0)]));
    const round = roundsLeft > 0 ? Object.fromEntries(sel.map((t) => [t, Math.floor(rest0[t] / roundsLeft)])) : null;
    const todo = round ? Object.fromEntries(sel.map((t) => [t, Math.min(rest[t], Math.max(0, round[t] - (nowC[t] || 0)))])) : null;
    // 놓친 몫: 지난 회차까지 계획(달 몫 × 지난 회차 ÷ 회차 수)보다 그 종목에 덜 샀다
    const missed = round && passed > 0 ? sel.filter((t) => toC(bought[t]) < mulDiv(share[t], passed, rounds)) : [];
    return { share, rest, round, todo, missed, capped };
  };
  const out = { sel, by: {}, round: {}, todo: {}, rest: {}, missed: {}, capped: {} };
  const usdOf = (o) => (o ? Object.fromEntries(Object.entries(o).map(([t, c]) => [t, c / 100])) : null);
  for (const [k, w] of [['equal', () => 1], ['cap', (t) => caps[t]], ['tier', (t) => weights[tiers[t]]]]) {
    const r = plan(w);
    out.by[k] = usdOf(r?.share); out.round[k] = usdOf(r?.round); out.todo[k] = usdOf(r?.todo); out.rest[k] = usdOf(r?.rest); out.missed[k] = r ? r.missed : []; out.capped[k] = !!r?.capped;
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
    // 미리 넣은 돈(forMonth가 반영일 달보다 뒤)은 그 달 몫 — 앞당기는 것은 받지 않는다(2026-10-25 사용자 결정)
    const m = p.forMonth || p.day.slice(0, 7);   // forMonth는 effectiveDeposits가 '반영일 달보다 뒤'인 것만 남긴다
    if (m === month) now.push(p); else if (m > month) later.push(p);
  }
  const by = (x, y) => (x.day < y.day ? -1 : 1);
  return { now: now.sort(by), later: later.sort(by) };
}

// 이번 달 실제 매수(취소 빼고, 그달 1일부터 오늘까지 — dr r1: 점검일 전 매수도 그달 돈을 쓴 것) — 종목별 {qty, amount}
export function monthBuys(trades, month, today, from = '') {   // from: 그 날짜부터의 매수만(이번 회차에 산 돈, 2026-11-09)
  const real = Object.entries(trades || {});
  const cancelled = new Set(real.filter(([, x]) => x.cancels).map(([, x]) => x.cancels));
  const out = new Map();
  for (const [id, x] of real) {
    if (x.cancels || cancelled.has(id) || x.side !== 'buy' || x.date.slice(0, 7) !== month || x.date > today || x.date < from) continue;
    const o = out.get(x.ticker) || { qty: 0, amount: 0 }; o.qty += x.qty; o.amount = Math.round(o.amount * 100 + Math.round(x.qty * x.price * 100) + Math.round((Number(x.fee) || 0) * 100)) / 100; out.set(x.ticker, o);   // 거래마다 센트(매도와 같은 단위), 수수료 포함(산 돈 = 대금 + fee, 2026-10-28)
  }
  return out;
}

// 그달 실제 매도 대금(취소 빼고, 그달 1일~오늘). 원칙 4: 판 돈은 다음 달 점검일에 그달 돈에 더한다.
// income: [{date, amount}] 배당·이자 — 매도 대금처럼 다음 달 한도로(한국 계좌 설계 3절)
export function monthSells(trades, month, today, income) {
  const real = Object.entries(trades || {});
  const cancelled = new Set(real.filter(([, x]) => x.cancels).map(([, x]) => x.cancels));
  let sum = 0;
  for (const [id, x] of real) {
    if (x.cancels || cancelled.has(id) || x.side !== 'sell' || x.date.slice(0, 7) !== month || x.date > today) continue;
    sum += Math.round(x.qty * x.price * 100) - Math.round((Number(x.fee) || 0) * 100);   // 거래마다 센트, 수수료를 뺀 실제 받은 돈
  }
  for (const p of income || []) if (p.date.slice(0, 7) === month && p.date <= today) sum += Math.round(p.amount * 100);
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
  const candidates = Object.keys(firstRec.cards || {}).sort().filter((t) => !holdReason(firstRec.cards[t], firstRec) && principleFor(month).includes(firstRec.cards[t].tier));
  const plan = { decisionDate: d0, record: firstRec.session, rounds, candidates, fires: [] };
  const steps = [{ label: '결정', date: d0, state: 'done' }, ...rounds.map((r, i) => ({ label: i + 1 + '회차', date: r.date, state: r.date > lastSession ? 'todo' : 'done' }))];
  const next = rounds.find((r) => r.date > lastSession) || null;
  if (!next) return null;   // 시연 회차가 다 지나면 시연을 끝내고 다음 점검 미리 보기로(사용자 결정 2026-10-23)
  return { plan, steps, next, stale: false, alerts: [], demo: true };
}

// 살 종목 상한의 실제 계좌 예외(원칙 3, 2026-11-04 사용자 결정): 엔진은 12월 계획부터 5개만 고르지만, 실제 계좌 화면은 11월 2회차부터
// 쓴다. 11월 계획이면 2회차 전 마지막 완전한 기록으로 한 번 골라 그달 고정한다. 그 기록이 아직 없으면(2회차 전) 마지막 기록으로 미리 보기.
// 엔진이 이미 고른 달(12월 이후)·시연 달·지난달 계획은 그대로 둔다. 순수 함수 — 시험이 부른다
export function pickMonth(mv, recs, today) {
  const p = mv?.plan;
  if (!p || mv.demo || mv.stale || p.passed != null) return mv;
  const m = (p.checkDate || p.decisionDate).slice(0, 7);
  if (m >= PICK_FROM || m !== PICK_FROM_ROUND.slice(0, 7)) return mv;
  const full = recs.filter((r) => r.pipelineFull);
  const before = full.filter((r) => r.session < PICK_FROM_ROUND);
  const rec = today >= PICK_FROM_ROUND ? before[before.length - 1] : full[full.length - 1];
  if (!rec) return mv;
  const candidates = pickTop(p.candidates, rec).sort();
  return { ...mv, plan: { ...p, candidates, passed: p.candidates.length, passedList: p.candidates, pickRecord: rec.session, pickProvisional: today < PICK_FROM_ROUND } };
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

// 10/01부터의 공통 과거(사용자 결정 2026-10-25 — 전략 비교를 새로 시작해도 모든 줄을 10/01부터): pre(볼트 preStart, 9/30~첫 시작일
// Robinhood 기록) × 끝낸 묶음마다 그 실제 계좌(그 묶음 시작 스냅샷 + 매매·입금 기록, 다음 묶음 시작일까지 — 마지막은 endDate까지).
// endDate = 지금 비교가 출발한 날(평가가 처음 확정된 날). 끝낸 묶음이 없으면 pre만(지금 시작 스냅샷이 pre 끝과 같아야 함).
// 돌려주는 값: {from, twr, spy}(공통 과거의 수익률·같은 구간 SPY) 또는 {why}. 시작하자마자 끝낸 묶음(다음 시작일과 같거나 뒤)은 거치지 않는다.
export function historyPrefix(pre, past, curSnapshot, endDate, curStartValue, { records, trades }) {
  if (!pre || !endDate) return null;
  past = (past || []).filter((b, k) => { const nx = (past[k + 1]?.snapshot || curSnapshot)?.date; return b.snapshot?.date && nx && b.snapshot.date < nx; });
  const spyOn = (d) => { const r = (records || []).find((x) => x.session === d); const v = r?.prices?.SPY ?? r?.cards?.SPY?.close; return typeof v === 'number' && v > 0 ? v : null; };
  let g = 1, gs = 1, first = { snapshot: curSnapshot, startValue: curStartValue, started: endDate };
  for (let k = 0; k < past.length; k++) {
    const b = past[k], end = k + 1 < past.length ? past[k + 1].snapshot.date : endDate;
    let r;
    try { r = actualAccount({ records, snapshot: b.snapshot, deposits: b.deposits || {}, trades }); } catch (e) { return { why: '끝낸 비교 계산 실패' }; }
    const day = (r.days || []).find((x) => x.date === end);
    if (!r.started || !day || day.twr == null) return { why: `끝낸 비교의 ${end} 평가가 없음` };
    const s0 = spyOn(r.started), s1 = spyOn(end);
    g *= 1 + day.twr;
    gs = gs != null && s0 && s1 ? gs * (s1 / s0) : null;
    if (k === 0) first = { snapshot: b.snapshot, startValue: r.startValue, started: r.started };
  }
  const c = chainPreStart(pre, { started: first.started, twr: g - 1, vs: gs == null ? null : { SPY: (g - gs) * 100 } }, first.snapshot, first.startValue);
  if (!c || c.why) return c;
  return { from: pre.from, twr: c.twr, spy: c.vsSPY == null ? null : c.twr - c.vsSPY / 100, n: past.length };
}
// 공통 과거를 앞에 곱한다: (1 + 과거) × (1 + 그 뒤) − 1. SPY 대비도 같은 방식(RSP·QQQ 대비는 과거 자료가 없어 비운다)
export function withPrefix(twr, vsSPY, h) {
  if (twr == null || !h || h.why) return { twr, vsSPY };
  const t = (1 + h.twr) * (1 + twr) - 1;
  const spy = h.spy == null || vsSPY == null ? null : (1 + h.spy) * (1 + (twr - vsSPY / 100)) - 1;
  return { twr: t, vsSPY: spy == null ? null : (t - spy) * 100 };
}

// 수익률을 아는 마지막 날 기준 요약(마지막 기록이 불완전해 그날 평가가 비면 그 전날 값 — 예: 10/21 pipelineFull false)
export function summarizeKnown(s) {
  const m = summarize(s);
  if (m.twr != null || !s.started) return m;
  const k = [...(s.days || [])].reverse().find((d) => d.date >= s.started && d.twr != null);
  return k ? { ...m, twr: k.twr, vs: k.vs || null, asOf: k.date } : m;
}

// 잔금(원칙 3, 사용자 결정 2026-10-23): 4회가 끝나고 쓰지 못한 돈은 다음 달 쓸 돈에 더한다.
// 그달 매수 한도 B(m) = max(0, 그달 입금 − 출금 + 지난달 판 돈 + 잔금(m)), 잔금(m) = max(0, B(m−1) − 산 돈(m−1)).
// 잔금은 회차가 있던 달에서만 생긴다: 첫 실제 점검 달은 시작 달(전략 비교 시작 스냅샷의 달) 다음 달이라, 시작 달 다음 달까지는 잔금 0(dr).
// 점검일이 그달 첫 거래일이고 회차는 7일 간격 4번이라 한 달 안에 끝난다. net(m)·sold(m)·spent(m)는 달 → 달러 함수
export function carryIn(month, startMonth, { net, sold, spent }) {
  const memo = new Map();
  const prev = (m) => { const [y, n] = m.split('-').map(Number); return n === 1 ? `${y - 1}-12` : `${y}-${String(n - 1).padStart(2, '0')}`; };
  const cents = (v) => Math.round(v * 100);
  const carry = (m) => {
    const p = prev(m);
    if (!startMonth || p <= startMonth) return 0;
    if (memo.has(m)) return memo.get(m);
    const B = Math.max(0, cents(net(p)) + cents(sold(prev(p))) + carry(p));
    const c = Math.max(0, B - cents(spent(p)));
    memo.set(m, c);
    return c;
  };
  return carry(month) / 100;
}

// 회차 띠(사용자 결정 2026-10-23 최적안): 회차 날짜들(dates, 오름차순)과 다음 회차(next — 없으면 회차 끝),
// 그달 실제 매수 목록 buys [{date, amount}], 이번·남은 회차 하나당 계획 금액(planEach, 달러|null)으로
// 회차마다 {date, state: 'done'|'missed'|'now'|'plan', amount}과 첫 회차 전 매수(outside)를 낸다.
// 회차 k의 매수 = [dates[k], dates[k+1]) 안의 매수(마지막 회차는 그달 끝까지).
export function roundStrip(dates, next, buys, planEach) {
  const sum = (a, b) => Math.round(buys.filter((x) => x.date >= a && (!b || x.date < b)).reduce((t, x) => t + x.amount, 0) * 100) / 100;
  const outside = dates.length ? Math.round(buys.filter((x) => x.date < dates[0]).reduce((t, x) => t + x.amount, 0) * 100) / 100 : 0;
  const out = dates.map((d, k) => {
    const got = sum(d, dates[k + 1]);
    if (next && d > next) return { date: d, state: 'plan', amount: planEach };
    if (next && d === next) return { date: d, state: 'now', amount: planEach, done: got };
    return { date: d, state: got > 0 ? 'done' : 'missed', amount: got };
  });
  return { rounds: out, outside };
}
// 그달 1일~오늘 실제 매수 목록 [{date, amount}](취소 빼고, 거래마다 센트)
export function monthBuyList(trades, month, today) {
  const real = Object.entries(trades || {});
  const cancelled = new Set(real.filter(([, x]) => x.cancels).map(([, x]) => x.cancels));
  return real.filter(([id, x]) => !x.cancels && !cancelled.has(id) && x.side === 'buy' && x.date.slice(0, 7) === month && x.date <= today)
    .map(([, x]) => ({ date: x.date, amount: Math.round(x.qty * x.price * 100) / 100 })).sort((a, b) => (a.date < b.date ? -1 : 1));
}
// 이번 달 판 기록(매도 탭, 2026-11-03): 취소 안 된 매도, 받은 돈 = 수량 × 체결가 − 수수료(monthSells와 같은 센트 셈, 배당은 뺌)
export function monthSellList(trades, month, today) {
  const real = Object.entries(trades || {});
  const cancelled = new Set(real.filter(([, x]) => x.cancels).map(([, x]) => x.cancels));
  return real.filter(([id, x]) => !x.cancels && !cancelled.has(id) && x.side === 'sell' && x.date.slice(0, 7) === month && x.date <= today)
    .map(([, x]) => ({ date: x.date, ticker: x.ticker, account: acctOf(x), qty: x.qty,
      amount: (Math.round(x.qty * x.price * 100) - Math.round((Number(x.fee) || 0) * 100)) / 100 }))
    .sort((a, b) => (a.date < b.date ? -1 : a.date > b.date ? 1 : a.ticker < b.ticker ? -1 : 1));
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
  CARDS = { ...(lastFull?.cards || {}), ...(last?.cards || {}) };   // 카드 링크는 카드가 있는 종목만(tickName)
  const h = model.main?.holdings || {};
  const now = model.now ?? Date.now(), today = etDate(now);
  // 한국 계좌(2026-10-28): 올린 보유표와 그 뒤 매매는 Robinhood만, 키움은 장부·키움 매매로(카드 표시라 기록일 기준)
  const { events: lev } = ledgerActive(model.ledger);
  const inc = incomeList(lev);
  const cur = currentHoldings(h.rows, h.asOf, tradesOf(model.trades, RH), today);
  // 전략 비교에 기록한 입금(실제로 계좌에 넣은 돈)도 올린 보유 기준일 뒤·오늘까지 반영일이면 현금에 더한다(dr r1 — 실제 계좌 줄과 같은 돈).
  // 끝낸 묶음의 입금도 실제 돈이므로 모든 묶음을 본다(dr r2, model.allDeposits — 없으면 지금 묶음)
  const depIn = cur.hasCash ? depositsSince(model.allDeposits || Object.fromEntries(Object.entries(model.bundle?.deposits || {})
    .map(([k, v]) => ['b0:' + k, v.cancels ? { ...v, cancels: 'b0:' + v.cancels } : v])), cur.base || '', today) : [];
  if (depIn.length) cur.cash = Math.round((cur.cash + depIn.reduce((a, p) => a + p.amount, 0)) * 100) / 100;
  const kw = kwState(lev, model.trades, today, 'rec', recs);
  const rhHold = cur.holdings;
  cur.cashBy = { rh: cur.cash, kw: kw.cash };
  cur.kwUsed = lev.length > 0 || kw.holdings.length > 0;
  if (cur.kwUsed) {
    cur.cash = Math.round((cur.cash + kw.cash) * 100) / 100;
    const m = new Map(rhHold.map((x) => [x.ticker, { ...x }]));
    for (const x of kw.holdings) {
      const o = m.get(x.ticker);
      if (!o) m.set(x.ticker, { ...x });
      else { const q = o.qty + x.qty; o.avgPrice = o.avgPrice != null && x.avgPrice != null ? (o.qty * o.avgPrice + x.qty * x.avgPrice) / q : null; o.qty = q; }   // 합산 단가는 참고(원칙 4는 계좌별)
    }
    cur.holdings = [...m.values()].sort((a, b) => (a.ticker < b.ticker ? -1 : 1));
  }
  let mv = monthView(model.result, last ? last.session : '', today);
  // 첫 달 시연: 전략 비교가 출발했고 이번 달 점검 결정이 아직 없으며 일별 기록이 이번 달에 시작했으면(사용자 결정 10-22)
  if (mv && !mv.plan && model.bundle && !model.bundle.closed) mv = demoMonth(recs.find((r) => r.pipelineFull) || null, today.slice(0, 7), last ? last.session : '') || mv;
  mv = pickMonth(mv, recs, today);
  // 20% 하락 매도 검토(원칙 4). 원칙 6에 걸리면 뺀다 — 카드 없는 종목은 지수 ETF만 본다(사용자 결정 10-22)
  const recStale = !!lastFull && recordGap(lastFull, today) > RECORD_STALE;   // 기록 자체가 묵었으면 사지도 팔지도 않는다(원칙 6)
  // 원칙 4 매도 검토는 계좌별(사용자 결정 2026-10-28 — 매도는 계좌 단위)
  const losses = recStale ? [] : [...lossAlerts(rhHold, close), ...lossAlerts(kw.holdings, close).map((l) => ({ ...l, account: KW }))].filter((l) => lossReviewable(l.ticker, lastFull, today));
  const lossOf = new Map(losses.map((l) => [l.ticker, l]));   // 합산 보유표 행 표시용(어느 계좌인지는 알림 줄에)

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
    : (cur.hasCash ? `주식 ${usd0(total - cur.cash)} · 현금 ${usd0(cur.cash)}` + (cur.kwUsed ? ' · 키움 포함' : '') : '현금 모름(올린 보유에 현금 줄 없음)') + (missing.length ? ` · 가격 없음 ${missing.join(', ')}` : '')
      + (priceDays.size ? ` · ${[...priceDays].sort().map(md).join('·')} 종가` : ''));
  // 시작 전 실제 계좌 흐름(preStart)이 맞으면 그날부터 이어 붙인다(A안) — 전략 비교는 그대로 시작 스냅샷부터
  // 10/01부터의 공통 과거(끝낸 비교를 거침, 10-25)를 지금 비교의 실제 계좌 수익률 앞에 곱한다
  const hist = rs?.started ? historyPrefix(model.main?.preStart, model.pastBundles, model.bundle?.snapshot, rs.started, real?.startValue, { records: model.records, trades: model.trades }) : null;
  const pre = !model.main?.preStart ? null : !rs?.started || rs.twr == null ? { why: '실제 계좌가 아직 출발 전' } : hist?.why ? hist
    : hist ? (() => { const w = withPrefix(rs.twr, rs.vs?.SPY ?? null, hist); return { from: hist.from, twr: w.twr, vsSPY: w.vsSPY }; })() : null;   // SPY 대비도 10/01부터(10-25 이음에서 빠졌던 것)
  const ok = pre && !pre.why;
  cell('시작 뒤 수익률', ok ? pct(pre.twr) : rs?.twr != null ? pct(rs.twr) : '—',
    ok ? `${md(pre.from)}부터 · 내 실제 계좌` + (hist.n ? `(끝낸 비교 ${hist.n}개를 거쳐 이음)` : `(${md(rs.started)}까지는 Robinhood 기록)`) : rs?.started ? `${md(rs.started)}부터 · 내 실제 계좌` + (pre?.why ? ` · ${md(model.main.preStart.from)} 기록 못 이음: ${pre.why}` : '') : '전략 비교를 시작하면 보입니다', 'pf-v-accent');
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
  if (live && mv.demo) eye.appendChild(el('span', 'pf-badge', '시연 · 실제 투자는 다음 달 점검부터'));
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
  // 매수 | 매도 탭(사용자 결정 2026-11-03): 처음엔 늘 매수, 기록 뒤 다시 그려도 이 페이지에서 고른 탭은 유지. 팔기 줄은 알림 칸에서 매도 탭으로 옮김
  const tabs = el('div', 'pf-segbox pf-dotabs'); tabs.setAttribute('role', 'tablist'); tabs.setAttribute('aria-label', '다음 할 일');
  const buyPane = el('div', 'pf-dopane'), sellPane = el('div', 'pf-dopane');
  next.appendChild(tabs); next.appendChild(buyPane); next.appendChild(sellPane);
  // 회차 진행은 돈 칸 아래 4회 띠(실제 매매 기록)가 보여 준다 — 모의 계산 기준 진행 막대는 뺐다(사용자 결정 2026-10-23, 둘이 달라 보임)
  const buySlot = el('div', 'pf-buyslot'); buyPane.appendChild(buySlot);
  // 알림 칸(사용자 결정 2026-10-28): 매도 안내·20% 하락 검토·기록 묵음 경고를 '다음 할 일'에서 옮겨 보유 자산 위 칸에 모은다. 없으면 '알림 없음 · 다음 판정 확인'
  // 알림 칸(2026-10-29 사용자 결정 B안): 한 줄 목록 — 배지(팔기·검토·확인) · 종목(계좌 · 이유) · 숫자, 팔기는 아래 작은 설명 한 줄
  const alerts = el('section', 'pf-panel pf-side pf-alerts');
  const ahead = el('div', 'pf-alerthead');
  const ah = el('h2', 'pf-h2s', '알림 '); ahead.appendChild(ah); alerts.appendChild(ahead);
  // 기록 묵음·판정 방식이 바뀐 달 안내는 목록 위 한 줄
  if (recStale) alerts.appendChild(el('p', 'pf-warn', `⚠ 마지막 완전한 기록이 ${md(lastFull.session)}로 ${recordGap(lastFull, today)}거래일 지났습니다. 새 기록이 올 때까지 사지도 팔지도 않습니다(원칙 6).`));
  if (live && mv.plan.ruleChanged) alerts.appendChild(el('p', 'pf-note', '판정 방식이 바뀐 달입니다. 전략 비교의 모의 계산은 이번 달 매매하지 않습니다(바뀐 판정으로 매도가 생기지 않게).'));
  // 원칙 4 개정(2026-10-28): 실제 보유를 매주 회차 기준으로 보고 이번 회차에 팔 양을 보여 준다. 10월에도 11/02 첫 회차부터 팔 양을 미리 보여 준다(2026-10-29)
  const weekly = today.slice(0, 7) >= PRINCIPLE_FROM;
  const allHold = [...rhHold.map((x) => ({ ...x, account: RH })), ...kw.holdings.map((x) => ({ ...x, account: KW }))];
  const holdOnly0 = model.bundle?.snapshot?.holdOnly || [];
  const sRounds = sellRounds(today.slice(0, 7), lastFull ? lastFull.session : today);
  const wSells = !recStale ? weeklySells({ holdings: allHold, rec: lastFull, today, rounds: sRounds,
    lastSession: lastFull ? lastFull.session : '', trades: model.trades, holdOnly: holdOnly0 }) : [];
  const staleH = !recStale ? staleHoldings({ holdings: allHold, rec: lastFull, today, holdOnly: holdOnly0 }) : [];
  const qty = (v) => (Math.abs(v - Math.round(v)) < 1e-9 ? String(Math.round(v)) : String(+v.toFixed(6)));
  const acct = (a) => (a === KW ? '키움' : cur.kwUsed ? 'RH' : '');
  const alist = el('div', 'pf-alertlist');
  const arow = (kind, badge, ticker, sub, val, valCls, detail) => {
    const r = el('div', 'pf-alertrow');
    r.appendChild(el('span', 'pf-abadge pf-ab-' + kind, badge));
    const nm = el('span', 'pf-aname'); nm.appendChild(tickName(ticker)); nm.appendChild(el('small', null, ' ' + sub)); r.appendChild(nm);
    r.appendChild(el('strong', 'pf-aval' + (valCls ? ' ' + valCls : ''), val));
    alist.appendChild(r);
    if (detail) alist.appendChild(el('p', 'pf-adetail', detail));
  };
  const sellList = el('div', 'pf-selllist');
  let sellNow = 0;
  for (const w0 of wSells) {
    const sub = [acct(w0.account), w0.tier].filter(Boolean).join(' · ');
    const val = !w0.round ? '다음 달' : w0.shares > 0 ? qty(w0.shares) + '주' : '팔았음';
    const detail = (!w0.round ? '이번 달 회차가 끝나 다음 점검일 첫 회차부터'
      : w0.shares <= 0 ? `${md(w0.round)} 회차 몫은 이미 팔았음`
      : w0.tier === '초고평가' ? `${md(w0.round)} 회차에 남은 것 전부`
      : w0.all ? `${md(w0.round)} 마지막 회차라 전부`
      : `${md(w0.round)} 회차 · 전부 팔 때까지 남은 ${w0.remaining}회에 나눠서`) + (!weekly && w0.round ? ' · 11월부터' : '');
    const r = el('div', 'pf-sellrow');
    const nm = el('span', 'pf-aname'); nm.appendChild(tickName(w0.ticker)); nm.appendChild(el('small', null, ' ' + sub)); r.appendChild(nm);
    r.appendChild(el('strong', 'pf-aval pf-aval-sell', val));
    const can = weekly && !!w0.round && w0.shares > 0;
    if (can) {
      sellNow++;
      const go = el('button', 'pf-btn pf-btn-quiet', '매도 기록'); go.type = 'button';
      go.addEventListener('click', () => dlg.open(w0.ticker, { side: 'sell', account: w0.account, qty: w0.shares }));
      r.appendChild(go);
    } else r.appendChild(el('span'));
    sellList.appendChild(r);
    sellList.appendChild(el('p', 'pf-adetail', detail));
  }
  for (const l of losses) arow('review', '검토', l.ticker, [acct(l.account), '20% 하락'].filter(Boolean).join(' · '), dropText(l.drop), 'pf-aval-down', null);
  for (const s0 of staleH) arow('check', '확인', s0.ticker, [acct(s0.account), HOLD_TEXT[s0.why] || '데이터 문제'].filter(Boolean).join(' · '), '보류', 'pf-aval-muted', null);
  if (alist.children.length) {
    alerts.appendChild(alist);
    const kinds = [losses.length && '검토는 직접 판단', staleH.length && '확인은 카드 갱신 전까지 사고팔지 않음'].filter(Boolean);
    alerts.appendChild(el('p', 'pf-afoot', kinds.join(' · ')));
  }
  // 예전 점검일 알림(모의 계산의 발동)은 실제 보유 기준 안내(wSells)로 바꿈(2026-10-29)
  // 넣은 돈(원칙 3): 모든 묶음의 입금 가운데 반영일이 이번 달(미국 동부)인 것 — 엔진·기록·관리 탭과 같은 반영일·취소 기준(dr r1)
  const month = today.slice(0, 7);
  const depMap0 = model.allDeposits || Object.fromEntries(Object.entries(model.bundle?.deposits || {})
    .map(([k, v]) => ['b0:' + k, v.cancels ? { ...v, cancels: 'b0:' + v.cancels } : v]));
  // 환전·역환전도 같은 입금 지도로(한도 몫은 저장된 forMonth — 한국 계좌 설계 2절)
  const depMap = { ...depMap0, ...ledgerDeposits(lev) };
  // 잔금 시작 달 = 첫 묶음 달과 가장 이른 몫 달 중 이른 쪽(설계 4절 — 새 묶음을 시작해도 잔금이 끊기지 않게)
  const firstMonth = [...(model.pastBundles || []).map((b) => b.snapshot?.date), model.bundle?.snapshot?.date].filter(Boolean).map((d) => d.slice(0, 7)).sort()[0] || null;
  // 통합 입금 지도 전체(Robinhood 입금 포함)에서 가장 이른 몫 달(dr)
  const earliestFor = Object.values(depMap).filter((d) => d && !d.cancels && d.recordedAt).map((d) => d.forMonth || (depositTiming(d.recordedAt).day || '').slice(0, 7)).filter(Boolean).sort()[0] || null;   // 몫 달이 없으면 반영일 달(한도 계산과 같게)
  const startMonth0 = [firstMonth, earliestFor].filter(Boolean).sort()[0] || null;
  const deps = monthDeposits(depMap, month);
  const canDeposit = !!(model.bundle && !model.bundle.closed);   // 입금은 지금 묶음 문서에 쓴다
  const stats = el('div', 'pf-nextstats');
  const stat = (k, v) => { const s = el('span', null, k + ' '); s.appendChild(el('strong', null, v)); stats.appendChild(s); };
  // 매도 검토 = 판정(고평가·초고평가) 알림 + 20% 하락(원칙 4), 종목 기준 — 알림 칸 제목에 센다
  const sellN = new Set([...losses.map((l) => l.ticker), ...staleH.map((f) => f.ticker)]).size;   // 팔기는 매도 탭에서 센다(2026-11-03)
  if (sellN) ah.appendChild(el('small', null, String(sellN)));
  // 머리 오른쪽: 다음 회차(판정 확인) 날짜. 알림이 없으면 초록 한 줄(B안 공통)
  const nextCheck = sRounds.find((d) => d > (lastFull ? lastFull.session : today)) || null;
  if (nextCheck) ahead.appendChild(el('span', 'pf-anext', `다음 회차 ${md(nextCheck)}`));
  if (!alist.children.length && !recStale) {
    const ok = el('div', 'pf-alertok');
    ok.innerHTML = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12l4 4 10-10"></path></svg>';
    const t = el('div'); t.appendChild(el('strong', null, '지금 할 검토·확인 없음')); if (nextCheck) t.appendChild(el('small', null, `다음 판정 확인 ${md(nextCheck)}`)); ok.appendChild(t);
    alerts.appendChild(ok);
  }
  if (sellNow) alerts.appendChild(el('p', 'pf-afoot', `팔기 ${sellNow}건은 '이번 달, 다음 할 일'의 매도 탭에`));
  // 매도 탭 내용: 이번 회차에 팔 것(줄마다 매도 기록) → 이번 달 판 기록과 판 돈(다음 달 매수로, 원칙 3)
  sellPane.appendChild(el('h3', 'pf-doh', nextCheck ? `${md(nextCheck)} 회차에 팔 것` : '이번 회차에 팔 것'));
  if (recStale) sellPane.appendChild(el('p', 'pf-note', '기록이 묵어 이번에는 팔지 않습니다(원칙 6). 새 기록이 오면 다시 계산합니다.'));
  else if (sellList.children.length) { sellPane.appendChild(sellList); sellPane.appendChild(el('p', 'pf-afoot', '고평가는 남은 회차에 나눠 팔고, 초고평가는 한 번에 · 고평가~적정 이하로 내려오면 멈춤')); }
  else sellPane.appendChild(el('p', 'pf-note', '지금 팔 종목이 없습니다. 보유 종목의 판정이 고평가 이상이 되면 여기에 나옵니다.'));
  const soldList = monthSellList(model.trades, today.slice(0, 7), today);
  sellPane.appendChild(el('h3', 'pf-doh', '이번 달 판 것'));
  if (soldList.length) {
    const sd = el('div', 'pf-soldlist');
    for (const x of soldList) {
      const r = el('div', 'pf-soldrow');
      r.appendChild(el('span', null, md(x.date)));
      const nm = el('span', 'pf-aname'); nm.appendChild(tickName(x.ticker)); nm.appendChild(el('small', null, ' ' + [acct(x.account), qty(x.qty) + '주'].filter(Boolean).join(' · '))); r.appendChild(nm);
      r.appendChild(el('strong', 'pf-aval', usd(x.amount)));
      sd.appendChild(r);
    }
    sellPane.appendChild(sd);
    const sum = Math.round(soldList.reduce((a, x) => a + x.amount * 100, 0)) / 100;
    sellPane.appendChild(el('p', 'pf-afoot', `판 돈 ${usd(sum)} · 다음 달 매수에 씀(원칙 3)`));
  } else sellPane.appendChild(el('p', 'pf-note', '아직 없음 · 판 돈은 다음 달 매수에 씁니다(원칙 3)'));
  const panes = { buy: buyPane, sell: sellPane };
  const tabBtns = {};
  const pick = (k) => { doTab = k; for (const [t, b] of Object.entries(tabBtns)) { b.setAttribute('aria-selected', String(t === k)); b.tabIndex = t === k ? 0 : -1; panes[t].hidden = t !== k; } };
  for (const [k, t] of [['buy', '매수'], ['sell', '매도']]) {
    const b = el('button', 'pf-segbtn', t); b.type = 'button'; b.setAttribute('role', 'tab'); b.id = 'pf-dotab-' + k;
    panes[k].setAttribute('role', 'tabpanel'); panes[k].setAttribute('aria-labelledby', b.id);
    b.addEventListener('click', () => pick(k));
    b.addEventListener('keydown', (e) => { if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') { const o = k === 'buy' ? 'sell' : 'buy'; pick(o); tabBtns[o].focus(); e.preventDefault(); } });
    tabBtns[k] = b; tabs.appendChild(b);
  }
  pick(doTab);
  if (!live && !canDeposit) stat('이번 달 넣은 돈', deps.now.length ? usd0(deps.now.reduce((a, d) => a + d.amount, 0)) : '없음');
  stat('마지막 기록', last ? md(last.session) : '없음');
  next.appendChild(stats);
  // 계획이 있으면 돈·나누는 방법·후보(첫 달은 시연), 계획이 없으면 돈 칸 + 점검 미리 보기(사용자 결정 10-22 Q1·B안)
  if (live || canDeposit) {
    const rec = live ? recs.find((r) => r.session === mv.plan.record) : null;
    const planTier = (t) => rec?.cards?.[t]?.tier ?? null;   // 무게는 점검일 판정으로 고정(dr r1)
    // 지금 살 단계인가(원칙 1·6): 마지막 완전한 기록에서 판정이 살 단계·유효하고 가격이 묵지 않음 — 엔진 회차 재확인의 화면용 근사
    const nowHold = (t) => holdReason(lastFull?.cards?.[t], lastFull, today);   // 원칙 6 — 엔진 회차 재확인과 같은 판단 + 기록 자체의 묵음
    // 원칙 1은 그 계획의 달(진행 중이면 점검일의 달, 미리 보기면 목표 달)의 판으로 — 11월부터 적정 제외(2026-10-28)
    const nowBuyable = (t) => !nowHold(t) && principleFor(live ? (mv.plan.checkDate || mv.plan.decisionDate).slice(0, 7) : target).includes(lastFull.cards[t].tier);
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
      waiting, preview, checkDay, month: target, today, cash: cur.hasCash ? cur.cash : null, cashBy: cur.kwUsed ? cur.cashBy : null,
      // 총자산(두 계좌 주식 + 현금, 현금 10% 목표용) — 가격 없는 종목은 빼고 개수를 알린다
      total: cur.hasCash ? Math.round(([...myVal.values()].reduce((a, v) => a + v, 0) + cur.cash) * 100) / 100 : null, totalMissing: cur.holdings.filter((x) => closeNow(x.ticker) == null).length, income: inc, depMap, startMonth: startMonth0, deps: target === month ? deps : monthDeposits(depMap, target) }));
  } else buySlot.remove();
  if (!buyPane.children.length) buyPane.appendChild(el('p', 'pf-note', '이번 달 살 계획이 아직 없습니다.'));
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
    nm.appendChild(tickName(x.ticker));
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
  right.appendChild(alerts);   // 알림 칸은 보유 자산 위(사용자 결정 2026-10-28)
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
  if (!mv.plan) return { title: '첫 점검일을 기다리는 중', sub: '매달 1일(휴장이면 다음 거래일)에 구매 후보를 정하고 나눠 삽니다.', done: 0, total: 0 };
  const rounds = mv.plan.rounds, total = rounds.length;
  const done = mv.steps.slice(1).filter((s) => s.state !== 'todo').length;
  const cands = mv.plan.candidates.length ? mv.plan.candidates.join(' · ') : '없음';
  if (mv.stale) return { title: '이번 달 결정 대기', sub: '점검일 정보가 오면 구매 후보를 정합니다. 회차 막대는 지난달 계획입니다.', done, total };
  if (mv.next) return { title: `${kday(mv.next.date)}, ${rounds.indexOf(mv.next) + 1}번째 나눠 사기`, sub: `구매 후보 ${cands} · ${total}회 중 ${done}회 진행`, done, total };
  return { title: '이번 달 회차 끝', sub: `구매 후보 ${cands} · 다음 점검은 다음 달 1일(휴장이면 다음 거래일)`, done, total };
}

// 나누는 방법: 원칙으로 정하기 전이라 이 탭에서만 기억한다(sessionStorage). 저장소가 막혀도 메모리 값으로 동작한다(dr r1)
let buyMethod;
let pickSaving = false;   // 체크 저장 중이면 다시 그린 목록·방법 버튼도 잠근다(dr r2)
// 종목 이름 → 그 종목 카드(사용자 결정 2026-11-03). 카드가 있는 종목만 링크, 새 탭으로 열어 이 화면(로그인)은 그대로 둔다
let CARDS = {};
function tickName(t) {
  if (!CARDS[t]) return el('strong', null, t);
  const a = el('a', 'pf-tlink', t); a.href = `${t.replace(/[^A-Za-z0-9]/g, '').toUpperCase()}_full_widget.html`;
  a.target = '_blank'; a.rel = 'noopener'; a.title = `${t} 카드 열기(새 탭)`;
  return a;
}
let doTab = 'buy';   // 다음 할 일 탭(매수|매도) — 페이지를 열 때마다 매수, 다시 그릴 때는 유지(sessionStorage 안 씀, 사용자 결정 '항상 매수')
let demoPicks = [];   // 시연 달 체크(저장하지 않음, 이 탭에서만)
try { buyMethod = sessionStorage.getItem('pf-buy-method'); } catch (_) { /* 정하지 않음 */ }
if (!BUY_METHODS.some(([k]) => k === buyMethod)) buyMethod = null;

// 다음 할 일 카드 안의 "무엇을·얼마나"(2026-10-22 사용자 결정, 디자인 캔버스 최종안, dr r1 반영): 돈(쓸 돈 = 넣은 돈 + 지난달 판 돈, − 이번 달 산 돈 = 남은 돈, 더 넣을 돈),
// 나누는 방법(기본값 없음), 원칙 1·6을 통과한 구매 후보(체크). 넣은 돈 = 반영일이 이번 달인 입금 기록(내 자산 현금·전략 비교에도 들어간다).
// 방법을 고르면 체크한 종목마다 이번 회차 금액(buyPlan — 남은 몫 ÷ 남은 회차)과 기록 버튼이 나온다.
// mv가 null이면(첫 점검일 전·이번 달 결정 대기) 돈 칸과 점검 미리 보기(previewSection)가 보인다(사용자 결정 10-22 Q1·B안).
function buyBox(args) {
  const { model, handlers, mv, dlg, close, tierOf, planTier, hasRec, nowBuyable, nowHold, today, deps } = args;
  const box = el('div', 'pf-buy');
  const month = args.month || today.slice(0, 7);   // 미리 보기면 다음 점검 달(그달 쓸 돈·체크)
  const ahead = month !== today.slice(0, 7);
  // 쓸 돈 = 반영일이 그달인 입금 + 그 전달에 판 돈(원칙 3·4). 그달에 판 돈은 다음 달 몫
  const soldPrev = monthSells(model.trades, prevMonth(month), today, args.income), soldNow = monthSells(model.trades, month, today, args.income);
  const deposited = Math.round(deps.now.reduce((a, d) => a + d.amount, 0) * 100) / 100;   // 그달 입금 − 그달 출금(음수일 수 있음)
  // 지난달 잔금(원칙 3): 4회가 끝나고 쓰지 못한 돈은 다음 달 쓸 돈에 더한다
  const netOf = (m) => monthDeposits(args.depMap || {}, m).now.reduce((a, d) => a + d.amount, 0);
  const spentOf = (m) => [...monthBuys(model.trades, m, today).values()].reduce((a, b) => a + b.amount, 0);
  const bought = monthBuys(model.trades, month, today);
  const spent = Math.round([...bought.values()].reduce((a, b) => a + b.amount, 0) * 100) / 100;
  // 현금 10%(원칙 3·5, 2026-11-03 사용자 결정): 11월부터 남은 한도 = 지금 현금(두 계좌) − 총자산의 10% − 이번 달 판 돈 − 다음 달 이후 몫으로 미리 넣은 돈.
  // 현금이 10%보다 많으면 넘는 만큼 사고, 적으면 새 돈이 먼저 현금을 채운다. 잔금은 현금으로 남아 다음 달 계산에 저절로 들어간다
  const laterIn0 = Math.round(deps.later.filter((d) => d.amount > 0 && (d.rec || d.day) <= today).reduce((a, d) => a + d.amount, 0) * 100) / 100;
  const laterOut0 = -Math.round([...deps.now, ...deps.later].filter((d) => d.amount < 0 && d.day > today).reduce((a, d) => a + d.amount, 0) * 100) / 100;   // 아직 안 나간 출금 예정(dr)
  const ct = month >= CASH_FROM ? cashLeft({ cash: args.cash, total: args.total, soldNow, laterIn: laterIn0, laterOut: laterOut0, missing: args.totalMissing || 0 }) : null;
  const carry = ct ? 0 : carryIn(month, args.startMonth, { net: netOf, sold: (m) => monthSells(model.trades, m, today, args.income), spent: spentOf });
  const budget = ct ? Math.round((spent + ct.left) * 100) / 100
    : Math.max(0, Math.round((deposited + soldPrev + carry) * 100) / 100);   // (10월까지) 쓸 돈 = 입금 − 출금 + 지난달 판 돈 + 잔금, 0 아래로 안 감
  const leftUsd = Math.round((budget - spent) * 100) / 100;

  // 1) 돈 세 칸(사용자 결정 2026-10-23 dr 최적안): 이번 달 입금 · 이번 주 매수(체크·방법에 따라 바뀜) · 계좌 현금, 그 아래 4회 띠.
  //    칸은 계획을 계산한 뒤 채운다(fillCells). 이번 달 매수 한도 B = max(0, 입금 − 출금 + 지난달 판 돈), 남은 한도 R = max(0, B − 산 돈)
  const money = el('div', 'pf-receipt');
  const cells = el('div', 'pf-receiptrow');
  money.appendChild(cells);
  const f = el('div', 'pf-receiptadd');
  const lab = el('label'); lab.appendChild(el('span', null, budget > 0 ? '더 넣을 돈' : '넣을 돈'));
  const amt = el('input'); amt.type = 'number'; amt.min = '0.01'; amt.step = '0.01'; amt.placeholder = '$ 금액';
  lab.appendChild(amt); f.appendChild(lab);
  // 몫은 자동(2026-10-25 사용자 결정 — 고르는 칸은 뺐다): 이번 달 회차가 남았으면 이번 달 몫(남은 회차에 나눠 삼),
  // 회차가 없거나 끝났으면(점검 전 미리 보기·시연 달·4회 끝) 다음 회차가 있는 달 몫
  const nowDay = depositTiming(new Date(model.now ?? Date.now()).toISOString()).day;
  // 남은 회차는 입금 반영일 기준으로 본다(마지막 기록 기준 mv.next는 기록이 늦으면 끝난 회차를 남은 것으로 본다 — cr). 저장할 때 다시 계산한다
  const liveDates = mv && !ahead && !mv.demo && mv.plan ? (mv.plan.rounds || []).filter((r) => !r.dropped).map((r) => r.date) : null;
  const autoFor = (dEff) => (ahead ? month : mv?.demo ? nextMonthOf(month) : !liveDates || !dEff ? null
    : liveDates.some((d) => d >= dEff) ? null : nextMonthOf(month));
  const autoMonth = autoFor(nowDay);
  const save = el('button', 'pf-btn pf-btn-dark', '입금 기록'); save.type = 'button';
  const msg = msgLine();
  f.appendChild(save); money.appendChild(f); money.appendChild(msg);
  twoStep(save, msg, '이 금액을 입금으로 기록합니다. 맞으면 한 번 더 누르세요.', async () => {
    const v = Number(amt.value);
    if (!(v > 0) || Math.round(v * 100) / 100 !== v || v > 1e7) throw new Error('0보다 큰 금액을 센트 단위까지 넣으세요.');
    const d1 = depositTiming(new Date().toISOString()).day;   // 저장 시각 기준으로 다시 본다 — 화면을 열어 둔 사이 달이 바뀌면 다음 달 표시가 뜻을 잃는다(dr)
    const am = autoFor(d1 || nowDay);
    await handlers.deposit(v, 'deposit', am && am > (d1 || nowDay || '').slice(0, 7) ? am : null);
  }, f);
  if (autoMonth) save.addEventListener('click', () => { if (save.dataset.armed) msg.textContent = `${+autoMonth.slice(5)}월 몫 입금으로 기록합니다. 맞으면 한 번 더 누르세요.`; });   // 어느 달 몫인지 확인 단계에 보인다(dr)
  box.appendChild(money);
  // 몫 안내(짧게)
  money.appendChild(el('p', 'pf-note pf-depnote', autoMonth ? `지금 넣는 돈은 ${+autoMonth.slice(5)}월 몫` : '지금 넣는 돈은 남은 회차에 나눠 삼'));
  const D = Math.round(deps.now.filter((d) => d.amount > 0).reduce((a, d) => a + d.amount, 0) * 100) / 100;
  const X = Math.round(-deps.now.filter((d) => d.amount < 0).reduce((a, d) => a + d.amount, 0) * 100) / 100;
  const R = Math.max(0, leftUsd), C = typeof args.cash === 'number' ? args.cash : null, over = Math.max(0, -leftUsd);
  // 계좌 현금에 이미 더한 다음 달 이후 몫 입금 — 이번 달 '쓸 수 있음'에서 뺀다(원칙 5, dr)
  const laterIn = Math.round(deps.later.filter((d) => d.amount > 0 && (d.rec || d.day) <= today).reduce((a, d) => a + d.amount, 0) * 100) / 100;
  const mLabel = ahead ? `${+month.slice(5)}월` : '이번 달';
  const strip = el('div', 'pf-strip');
  const fillCells = ({ week, weekLabel, weekNote, future, dates, next, preview, pending }) => {
    const cell = (k, v, sub, cls) => { const d = el('div', 'pf-receiptcell' + (cls ? ' ' + cls : '')); d.appendChild(el('span', 'pf-k', k)); d.appendChild(el('strong', null, v)); d.appendChild(el('span', 'pf-s', sub)); cells.appendChild(d); return d; };
    const laterSum = deps.later.reduce((a, d) => a + d.amount, 0);
    const p1 = deps.now.filter((d) => d.amount > 0).map((d) => (d.forMonth ? `${md(d.rec)} ${usd(d.amount)} 미리` : `${md(d.day)} ${usd(d.amount)}` + (d.day > today ? ' 예정' : '')));
    if (!p1.length) p1.push('입금 없음');
    if (X > 0) p1.push(`출금 −${usd(X)}`);
    if (!ct && soldPrev > 0) p1.push(`판 돈 +${usd(soldPrev)}`);
    if (carry > 0) p1.push(`잔금 +${usd(carry)}`);
    if (deps.later.length) p1.push(`다음 달 ${laterSum < 0 ? '출금 ' + usd0(-laterSum) : usd0(laterSum)}`);
    if (soldNow > 0) p1.push(`판 돈 ${usd0(soldNow)} 다음 달로`);
    p1.push(`한도 ${usd(budget)}`);
    cell(`${mLabel} 입금` + (ahead ? '(예상)' : ''), usd(D), p1.join(' · '));
    // 매수 완료 A와 앞으로 P는 늘 보이고(P를 모르면 —), 상태 안내는 앞에 붙인다(dr)
    cell(weekLabel, week == null ? '—' : usd(week), (weekNote ? weekNote + ' · ' : '') + `산 돈 ${usd(spent)} · 남음 ${future == null ? '—' : usd(future)}`);
    const ended = !preview && dates && dates.length && !next;
    const c3 = cell('계좌 현금' + (ahead ? ` (${md(today)} 기준)` : ''), C == null ? '—' : usd(C),
      over > 0 ? `한도 초과 ${usd(over)}(원칙 5)`
        : C == null ? '현금 모름'
        : ct ? (ct.unknown ? '한도 확인 불가 — 오른쪽 현금 목표 칸' : `쓸 수 있음 ${usd(R)} · 총자산의 10%는 현금으로(원칙 5)` + (laterIn > 0 ? ` · 다음 달 몫 ${usd0(laterIn)} 제외` : '') + (laterOut0 > 0 ? ` · 출금 예정 ${usd0(laterOut0)} 제외` : ''))
        : ahead ? (budget > 0 ? `${mLabel}엔 한도 ${usd(budget)}만 씀 · 나머지는 안 쓰는 돈(원칙 5)` : '안 쓰는 돈(원칙 5)')   // 미래 입금을 지금 현금에서 빼지 않는다(dr)
        : ended ? `${usd(R)} 다음 달로 · 나머지는 안 쓰는 돈(원칙 5)`
        : `쓸 수 있음 ${usd(Math.min(R, Math.max(0, C - laterIn)))}` + (laterIn > 0 ? ` · 다음 달 몫 ${usd0(laterIn)} 제외` : '') + ' · 나머지는 안 쓰는 돈(원칙 5)', 'pf-receiptleft');
    if (over > 0) c3.classList.add('pf-over');
    if (args.cashBy) c3.appendChild(el('span', 'pf-s', `미국 ${usd(args.cashBy.rh)} · 한국 ${usd(args.cashBy.kw)}`));   // 계좌별 현금(한국 계좌, 2026-10-28) — 한도는 하나지만 산 계좌에 돈이 있어야 한다
    // 잔금 칸: 지난달에서 넘어온 돈, 회차가 끝났으면 이번 달 남은 돈이 다음 달로 간다
    if (ct && ct.unknown) cell('현금 목표(10%)', '—', args.totalMissing ? `가격 없는 보유 ${args.totalMissing}종목이 있어 총자산을 몰라 이번 달 한도를 막음(원칙 6)` : '현금·총자산을 몰라 한도를 막음 — 보유 파일·현금을 확인하세요');
    else if (ct) cell('현금 목표(10%)', usd(ct.target), `총자산 ${usd0(args.total)}의 10% · 지금 현금 ${usd(C)}` + (ct.short > 0 ? ` · ${usd(ct.short)} 모자람` : ''));
    else cell(ended ? '다음 달로 넘길 잔금' : ahead ? `${mLabel}로 넘어올 잔금(예상)` : '지난달 잔금', usd(ended ? R : carry),
      ended ? '다음 달 한도에 더함(원칙 3)' : carry > 0 ? '한도에 포함' + (ahead ? ' · 이번 달 매매로 바뀜' : '') : '4회 뒤 남은 돈은 다음 달로(원칙 3)');
    // 4회 띠
    strip.textContent = '';
    if (!dates || !dates.length) return;
    // 방법·종목을 고르기 전에는 남은 한도 ÷ 남은 회차를 '약'으로 보인다(사용자 요청 2026-10-25)
    const nLeft = preview ? dates.length : next ? dates.filter((d) => d >= next).length : 0;
    const est = pending && week == null && nLeft && R > 0 ? Math.floor((R * 100) / nLeft) / 100 : null;   // 고르기 전일 때만 — 고른 종목을 지금 못 사거나 후보가 없으면 띄우지 않는다(cr)
    const each = week ?? est;
    const rs = roundStrip(dates, preview ? null : next, monthBuyList(model.trades, month, today), each);
    if (preview) rs.rounds = rs.rounds.map((r, i) => (r.amount > 0 ? r : { ...r, state: i === 0 ? 'first' : 'plan', amount: each }));   // 점검 전: 모두 예정(첫 회차만 표시)
    strip.appendChild(el('div', 'pf-k', `${mLabel} ${dates.length}회 매수`));
    const row = el('div', 'pf-striprow');
    const TXT = { done: '샀음', missed: next ? '놓침 → 남은 회차에' : '놓침', now: '이번 주', plan: preview ? '예정(예상)' : '예정', first: '1회차(예상)' };
    rs.rounds.forEach((r, i) => {
      const c = el('div', 'pf-stripcell pf-strip-' + r.state);
      c.appendChild(el('span', 'pf-s', `${i + 1}회 · ${md(r.date)}`));
      c.appendChild(el('strong', null, r.state === 'missed' ? '$0' : r.amount == null ? '—' : (est != null && (r.state === 'plan' || r.state === 'now' || r.state === 'first') ? '약 ' : '') + usd(r.amount)));
      if (r.state === 'first') c.classList.add('pf-strip-now');
      c.appendChild(el('span', 'pf-s', TXT[r.state] + (r.state === 'now' && r.done > 0 ? ` · 오늘까지 ${usd(r.done)} 삼` : '')));
      row.appendChild(c);
    });
    strip.appendChild(row);
    if (rs.outside > 0) strip.appendChild(el('p', 'pf-note', `회차 외 매수 ${usd(rs.outside)}(첫 회차 전)`));
    if (est != null) strip.appendChild(el('p', 'pf-note', '남은 한도 ÷ 남은 회차 · 방법·종목을 고르면 종목별로 나뉨'));
  };
  money.after(strip);

  if (!mv) {
    box.appendChild(el('p', 'pf-note', args.waiting ? `이번 달 점검(${md(args.checkDay)}) 결정이 오면 이 돈으로 구매 후보를 확정합니다.` : `${md(args.checkDay)} 점검일에 이 돈으로 구매 후보를 확정합니다.`));
    const pv = args.preview ? previewSection(args, box, month, budget) : null;
    // 점검 전: 회차는 점검일부터 매주 4회(예정), 이번 주 칸은 1회차 금액(예상)
    const S0 = cal().sessions, plus = (d, n) => new Date(Date.parse(d + 'T12:00:00Z') + n * 864e5).toISOString().slice(0, 10);
    const pdates = args.checkDay ? [0, 1, 2, 3].map((k) => S0.find((d) => d >= plus(args.checkDay, 7 * k))).filter(Boolean) : [];
    fillCells({ week: pv?.week ?? null, weekLabel: `${pdates[0] ? md(pdates[0]) + ' ' : ''}1회차 매수(예상)`, weekNote: pv ? pv.note : '점검 뒤 확정', future: pv ? pv.future : null, dates: pdates, next: pdates[0] || null, pending: !!pv && pv.note === '종목·방법을 고르세요', preview: true });
    return box;
  }
  const { plan } = mv;
  const nowBought = mv.next && !mv.demo ? Object.fromEntries([...monthBuys(model.trades, month, today, mv.next.date)].map(([t, b]) => [t, b.amount])) : {};   // 이번 회차에 산 돈(회차 금액 고정용)
  // 주간 확인에서 ↑로 올린 종목(사용자 결정 2026-11-09): 그달만 구매 후보 뒤에 더한다. 상한(원칙 3)은 막지 않고 체크가 넘으면 알린다(원칙 7)
  const promoted = (mv.demo ? [] : model.promoted?.[month] || []).filter((t) => !plan.candidates.includes(t));
  const cands = [...plan.candidates, ...promoted];
  if (!cands.length) { const act0 = plan.rounds.filter((r) => !r.dropped); fillCells({ week: null, weekLabel: '이번 주 매수', weekNote: '후보 없음', future: null, dates: act0.map((r) => r.date), next: mv.next ? mv.next.date : null }); box.appendChild(el('p', 'pf-note', '이번 달 원칙 1·6을 통과한 구매 후보가 없습니다.')); freshSection(args, box, plan, bought); return box; }

  // 2) 나누는 방법(기본값 없음 — 다시 누르면 끈다)
  const method = buyMethod;
  const active = plan.rounds.filter((r) => !r.dropped);   // 다음 점검일 뒤로 밀린 회차는 빼고 센다
  const rounds = active.length || 1;
  const roundsLeft = mv.next ? active.filter((r) => r.date >= mv.next.date).length : 0;
  const nextIdx = mv.next ? plan.rounds.indexOf(mv.next) + 1 : 0;   // 밀린(dropped) 회차는 늘 끝쪽이라 번호와 남은 회차가 어긋나지 않는다
  const mh = el('div', 'pf-buysechead');
  mh.appendChild(el('span', 'pf-buylabel', '나누는 방법'));
  const tiers = Object.fromEntries(cands.map((t) => [t, promoted.includes(t) ? tierOf(t) : planTier(t)]));   // 올린 종목은 점검일 판정이 없어 지금 판정
  const wMonth = (plan.checkDate || plan.decisionDate || month).slice(0, 7), weights = tierWeights(wMonth);
  const wText = Object.values(weights).join(':');
  const picked = ((mv.demo ? demoPicks : model.picks?.[month]) || []).filter((t) => cands.includes(t));
  const bp = method ? buyPlan({ cands, picked, budget, spent, bought: Object.fromEntries([...bought].map(([t, b]) => [t, b.amount])), boughtNow: nowBought,
    tiers, caps: model.caps || {}, rounds, roundsLeft, weights }) : null;
  // 체크 안 한 줄에도 '체크하면' 금액을 흐리게(사용자 결정 2026-10-25): 아무것도 안 골랐으면 전부 체크한 것으로, 골랐으면 그 종목을 더한 것으로 계산
  const hintPlans = new Map();
  const hint = (t, c) => {
    if (!method || !mv.next || !(budget > 0)) return null;
    const hp = picked.length ? [...picked, t] : cands, key = picked.length ? t : '*';
    if (!hintPlans.has(key)) hintPlans.set(key, buyPlan({ cands, picked: hp, budget, spent, bought: Object.fromEntries([...bought].map(([x, b]) => [x, b.amount])), boughtNow: nowBought, tiers, caps: model.caps || {}, rounds, roundsLeft, weights }));
    const r = hintPlans.get(key)?.todo[method]?.[t];
    return r > 0 ? `체크하면 ${shareTxt(r, c)}${usd(r)}` : null;
  };
  mh.appendChild(el('span', 'pf-note', !method ? '아직 원칙으로 정하지 않음' : !mv.next ? '이번 달 회차 끝'
    : `(종목 달 몫 − 지난 회차까지 산 돈) ÷ 남은 회차 ${roundsLeft}회 · 회차 안에서는 고정` + (bp?.capped[method] ? ' · 남은 돈에 맞춰 비례로 줄임' : '')
      + (method === 'cap' ? ' · 시총은 오늘 기준' : method === 'tier' ? ` · 무게는 점검일 판정 ${wText}` : '')));
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

  // 3) 내 기준대로 구매 후보
  // 점검일 뒤 판정이 바뀌어 지금 살 단계가 아닌 후보(예: 적정)는 숨긴다(사용자 결정 2026-11-03). 판정이 돌아오면 다시 보이고,
  // 이번 달 이미 산 종목과 회차가 끝난 달은 그대로 둔다. 숨긴 종목의 체크는 저장할 때 지우지 않는다
  const shownCands = [...byCap(plan.candidates, model.caps || {}), ...promoted].filter((t) => !mv.next || nowBuyable(t) || bought.has(t));
  const hiddenN = cands.length - shownCands.length;
  const hiddenPicked = picked.filter((t) => !shownCands.includes(t));
  const lh = el('div', 'pf-buysechead');
  const hidTxt = hiddenN ? ` · 지금 살 단계 아닌 ${hiddenN}개 숨김` : '';
  if (plan.passed != null && !mv.demo) {
    // 원칙 3 상한(2026-11-04): 제목에 고른 수와 200위 안 수, 기준·기록 날짜는 꼬리표로(사용자 결정 2026-11-05 — 긴 설명 줄 대신).
    // 2026-11-09: 통과 수(18)를 200위 안 수로 오해해 '5 / 18' 대신 '5 · 200위 안 N'으로 — 200위 안 수는 고른 그 기록으로 센다
    const pRec = (model.records || []).find((r) => r.session === (plan.pickRecord || plan.record));
    const inRange = pRec && plan.passedList ? pickTop(plan.passedList, pRec, { max: Infinity }).length : null;
    lh.appendChild(el('span', 'pf-buylabel', `구매 후보 ${shownCands.length}` + (inRange != null ? ` · 200위 안 ${inRange}` : '') + (promoted.length ? ` · 올림 ${promoted.length}` : '') + hidTxt));
    const tags = el('span', 'pf-buytags');
    tags.title = `원칙 1·6 통과 ${plan.passed}개 → 시총 200위 안 ${inRange ?? '?'}개 → 판정이 싼 순서·카드 점수 순으로 최대 5개(원칙 3) · 체크한 종목만 삽니다`;
    tags.appendChild(el('span', 'pf-badge', '200위 안 · 판정→점수'));
    tags.appendChild(el('span', 'pf-badge', `${md(plan.pickRecord || plan.record)} 기록${plan.pickProvisional ? ' · 미리 보기' : ''}`));
    lh.appendChild(tags);
  } else {
    lh.appendChild(el('span', 'pf-buylabel', `내 기준대로 구매 후보 ${shownCands.length}` + hidTxt));
    lh.appendChild(el('span', 'pf-note', mv.demo ? `시연 · ${md(plan.decisionDate)} 점검으로 보고 ${md(plan.record)} 첫 기록 판정 · 체크는 저장하지 않음`
      : `원칙 1·6 통과 · ${md(plan.decisionDate)} 점검 · 체크한 종목만 삽니다`));
  }
  box.appendChild(lh);
  const list = el('div', 'pf-buylist');
  const pickMsg = msgLine();
  for (const t of shownCands) {
    const on = picked.includes(t);
    const row = el('label', 'pf-buyrow' + (on ? ' pf-on' : ''));
    const cb = el('input'); cb.type = 'checkbox'; cb.checked = on; cb.value = t; cb.disabled = pickSaving;
    // 저장하는 동안 목록 전체를 잠그고, 보낼 목록은 지금 화면의 체크 상태로 만든다(dr r1 — 연달아 누르면 앞 체크가 지워지던 문제)
    cb.addEventListener('change', async () => {
      const boxes = [...list.querySelectorAll('input[type=checkbox]')];
      const nx = [...hiddenPicked, ...boxes.filter((c) => c.checked).map((c) => c.value)];
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
    nm.appendChild(tickName(t));
    nm.appendChild(el('span', 'pf-chip ' + (TIER_CLS[tiers[t]] || 'pf-t-none'), tiers[t] || '판정 없음'));
    const now = tierOf(t);
    if (now && now !== tiers[t]) nm.appendChild(el('span', 'pf-note', `지금 ${now}`));
    if (promoted.includes(t)) nm.appendChild(el('span', 'pf-badge', '올림'));
    const b = bought.get(t);
    if (b) nm.appendChild(el('span', 'pf-note', `이번 달 ${usd0(b.amount)}(${shares(b.qty)}주) 삼`));
    row.appendChild(nm);
    const act = el('span', 'pf-buyact');
    if (promoted.includes(t)) act.appendChild(moveBtn('↓', `${t} 주간 확인으로 내리기`, promoted.filter((x) => x !== t), args, month, pickMsg));
    const note = (x) => act.appendChild(el('span', 'pf-note', x));
    const c = close(t);
    if (!on) note(hint(t, c) || '고르지 않음');
    else if (!mv.next) note('이번 달 회차 끝');
    else if (!nowBuyable(t)) note(nowHold(t) ? `${HOLD_TEXT[nowHold(t)] || '데이터 문제'} — 보류(원칙 6)` : '살 단계 벗어남 — 이번 회차 건너뜀(원칙 2)');
    else if (!bp) note('방법을 고르면 금액');
    else if (!(budget > 0)) note('쓸 돈 없음');
    else if (!bp.by[method]) note(method === 'cap' ? '시총 없는 종목이 있음' : !hasRec ? '점검일 기록이 없어 판정 가중을 못 씀' : '무게 밖 판정이 있음(초저평가~적정만)');
    else {
      const r = bp.todo[method][t], fix = bp.round[method][t], got = nowBought[t] || 0;
      if (!(r > 0) && got > 0 && fix > 0) note(`${nextIdx}회차 몫 ${usd(fix)} 샀음`);
      else if (!(r > 0)) note(bp.rest[method][t] > 0 ? '회차 몫 1센트 미만' : leftUsd <= 0 || bp.capped[method] ? '남은 돈 없음' : '달 몫을 다 샀음');
      else if (c == null) note(`${usd(r)} · 가격 없음`);
      else if (Math.floor((r / c) * 1e4) <= 0) note(`${usd(r)} · 0.0001주 미만`);
      else {
        const amtBox = el('span', 'pf-buyamt');
        amtBox.appendChild(el('strong', null, shareTxt(r, c) + usd(r)));
        amtBox.appendChild(el('span', 'pf-s', `${nextIdx}회차` + (got > 0 ? ` 몫 ${usd(fix)} 중 ${usd(got)} 삼` : '') + ` · 달 몫 ${usd0(bp.by[method][t])}` + (bp.missed[method].includes(t) ? ' · 놓친 몫 포함' : '')));
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
  if (plan.passed != null && !mv.demo && picked.length > PICK_MAX) box.appendChild(el('p', 'pf-warn', `체크 ${picked.length}개 — 원칙 3 상한 ${PICK_MAX}개 넘음 · 이유를 기록하세요(원칙 7)`));
  // 칸 2: 체크한 종목 가운데 이번 회차에 살 수 있는 종목의 회차 금액 합(체크·방법을 바꾸면 바로 바뀜), 앞으로 = 남은 몫 합
  const ok = bp && bp.round[method] && mv.next ? picked.filter((t) => nowBuyable(t)) : [];
  const week = ok.length ? Math.round(ok.reduce((a, t) => a + (bp.round[method][t] || 0), 0) * 100) / 100 : null;
  const future = bp && bp.rest[method] ? Math.round(picked.reduce((a, t) => a + (bp.rest[method][t] || 0), 0) * 100) / 100 : null;
  fillCells({ week, pending: !!mv.next && (!method || !picked.length), weekLabel: mv.next ? `이번 주 매수(${nextIdx}/${rounds}회)` : '이번 주 매수',
    weekNote: !mv.next ? '회차 끝' : !method || !picked.length ? '종목·방법을 고르세요'
      : bp && !bp.by[method] ? (method === 'cap' ? '시총 없는 종목이 있음' : '무게 밖 판정이 있음') : null,
    future, dates: active.map((r) => r.date), next: mv.next ? mv.next.date : null });
  freshSection(args, box, plan, bought);
  return box;
}

// 점검일 전 미리 보기(사용자 결정 2026-10-22 B안): 첫 점검일 전·이번 달 결정 대기 때 지금 판정 기준 후보(원칙 1·6)를 체크 칸과 함께 보여 준다.
// 확정은 점검일에 한다. 체크는 그 점검 달(month) 몫으로 저장하고, 금액은 그달 쓸 돈을 4회로 나눈 회당 금액(회차 일정은 점검일에 생긴다)
function previewSection(args, box, month, budget) {
  const { model, handlers, tierOf, nowBuyable, close } = args;
  const cands = Object.keys(model.lastCards || {}).sort().filter((t) => nowBuyable(t));
  const ph = el('div', 'pf-buysechead');
  ph.appendChild(el('span', 'pf-buylabel', `${args.checkDay ? md(args.checkDay) + ' 점검 ' : ''}미리 보기 · 지금 판정 기준 후보 ${cands.length}`));
  ph.appendChild(el('span', 'pf-note', `원칙 1·6 통과 · 점검일에 확정 · 체크는 ${+month.slice(5)}월 몫으로 저장`));
  box.appendChild(ph);
  if (!cands.length) { box.appendChild(el('p', 'pf-note', '지금 판정으로는 살 단계인 종목이 없습니다.')); return { week: null, note: '후보 없음', month: 0 }; }
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
  const bought = monthBuys(model.trades, month, args.today);   // 같은 달 결정 대기 중 이미 산 돈은 다시 나누지 않는다(dr)
  const spent = Math.round([...bought.values()].reduce((a, b) => a + b.amount, 0) * 100) / 100;
  const bp = method ? buyPlan({ cands, picked, budget, spent, bought: Object.fromEntries([...bought].map(([t, b]) => [t, b.amount])), tiers, caps: model.caps || {}, rounds: 4, roundsLeft: 4 }) : null;
  const hintPlans = new Map();   // 체크 안 한 줄의 '체크하면' 금액(라이브 카드와 같은 규칙)
  const hint = (t, c) => {
    if (!method || !(budget > 0)) return null;
    const hp = picked.length ? [...picked, t] : cands, key = picked.length ? t : '*';
    if (!hintPlans.has(key)) hintPlans.set(key, buyPlan({ cands, picked: hp, budget, spent, bought: Object.fromEntries([...bought].map(([x, b]) => [x, b.amount])), tiers, caps: model.caps || {}, rounds: 4, roundsLeft: 4 }));
    const r = hintPlans.get(key)?.todo[method]?.[t];
    return r > 0 ? `체크하면 ${shareTxt(r, c)}${usd(r)}` : null;
  };
  const list = el('div', 'pf-buylist');
  const pickMsg = msgLine();
  for (const t of byCap(cands, model.caps || {})) {
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
    const nm = el('span', 'pf-buyname'); nm.appendChild(tickName(t));
    nm.appendChild(el('span', 'pf-chip ' + (TIER_CLS[tiers[t]] || 'pf-t-none'), tiers[t]));
    row.appendChild(nm);
    const act = el('span', 'pf-buyact');
    const note = (x) => act.appendChild(el('span', 'pf-note', x));
    if (!on) note(hint(t, close(t)) || '고르지 않음');
    else if (!bp) note('방법을 고르면 금액');
    else if (!(budget > 0)) note(`${+month.slice(5)}월 쓸 돈 없음`);
    else if (!bp.by[method]) note(method === 'cap' ? '시총 없는 종목이 있음' : '무게 밖 판정이 있음(초저평가~적정만)');
    else {
      const amtBox = el('span', 'pf-buyamt');
      const r = bp.round[method][t], c = close(t);
      amtBox.appendChild(el('strong', null, shareTxt(r, c) + usd(r)));
      amtBox.appendChild(el('span', 'pf-s', `회당(4회)` + (c ? '' : ' · 가격 없음') + ` · 달 몫 ${usd0(bp.by[method][t])}`));
      act.appendChild(amtBox);
    }
    row.appendChild(act);
    list.appendChild(row);
  }
  box.appendChild(list);
  box.appendChild(pickMsg);
  const wk = bp && bp.round[method] ? Math.round(picked.reduce((a, t) => a + (bp.round[method][t] || 0), 0) * 100) / 100 : null;
  const fu = bp && bp.rest[method] ? Math.round(picked.reduce((a, t) => a + (bp.rest[method][t] || 0), 0) * 100) / 100 : null;
  return { week: picked.length ? wk : null, future: fu, note: !method || !picked.length ? '종목·방법을 고르세요' : !(budget > 0) ? `${+month.slice(5)}월 입금이 아직 없음` : null };
}

// 주간 확인 ↔ 구매 후보 옮기기 버튼(2026-11-09). list = 저장할 그달 올린 종목 전체. 저장 중에는 같은 버튼들을 잠근다
function moveBtn(sym, label, list, args, month, msg) {
  const b = el('button', 'pf-btn pf-btn-quiet pf-movebtn', sym); b.type = 'button'; b.title = label; b.setAttribute('aria-label', label);
  b.disabled = pickSaving;
  b.addEventListener('click', async (e) => {
    e.preventDefault(); e.stopPropagation();
    const all = [...document.querySelectorAll('.pf-movebtn')];
    pickSaving = true; all.forEach((x) => { x.disabled = true; });
    try { await args.handlers.promote?.(month, list); } catch (err) {
      if (msg) msg.textContent = err.message || '저장하지 못했습니다.';
    } finally {
      pickSaving = false;
      document.querySelectorAll('.pf-movebtn').forEach((x) => { x.disabled = false; });
    }
  });
  return b;
}

// 주간 확인(원칙 2·6): 점검일 뒤 살 단계에 든 종목 — 보여 주기만, 살지는 사용자가 판단(사면 그달 남은 돈에서). 회차가 남았을 때만
function freshSection(args, box, plan, bought) {
  const { model, mv, dlg, tierOf, nowBuyable } = args;
  // 원칙 3 상한에서 밀린 점검일 후보(passedList)는 새로 든 종목이 아니라 빼고 센다(2026-11-05)
  const month = args.month || args.today.slice(0, 7);
  const promoted = (mv.demo ? [] : model.promoted?.[month] || []);
  const known = [...(plan.passedList || plan.candidates), ...promoted];
  const all = Object.keys(model.lastCards || {}).sort().filter((t) => !known.includes(t) && nowBuyable(t));
  if (!all.length || !mv.next) return;
  // 순서(사용자 결정 2026-11-09): 구매 후보와 같은 기준 — 200위 안을 위에, 밖을 아래에, 각각 판정이 싼 순서 → 카드 점수 순.
  // 순위는 마지막 기록의 시총, 시총을 모르는 종목은 맨 뒤 티커순
  const lastRec = { cards: model.lastCards };
  const inRange = pickTop(all, lastRec, { max: Infinity });
  const outRange = pickTop(all, lastRec, { max: Infinity, rankMax: Infinity }).filter((t) => !inRange.includes(t));
  const fresh = [...inRange, ...outRange, ...all.filter((t) => !inRange.includes(t) && !outRange.includes(t))];
  const fh = el('div', 'pf-buysechead');
  fh.appendChild(el('span', 'pf-buylabel', `주간 확인 · 점검일 뒤 살 단계에 든 종목 ${fresh.length}` + (inRange.length ? ` · 200위 안 ${inRange.length}` : '')));
  fh.appendChild(el('span', 'pf-note', '살지는 직접 판단 · 사면 그달 남은 돈에서(원칙 2·6)'));
  box.appendChild(fh);
  const fl = el('div', 'pf-buylist');
  for (const t of fresh) {
    if (t === fresh[inRange.length] && inRange.length) fl.appendChild(el('div', 'pf-note pf-freshcut', '시총 200위 밖'));
    const row = el('div', 'pf-buyrow pf-freshrow');
    // ↑ 그달 구매 후보로 올리기(사용자 결정 2026-11-09) — 올리면 구매 후보 목록 끝에 체크칸과 함께 나온다
    row.appendChild(mv.demo ? el('span') : moveBtn('↑', `${t} 구매 후보로 올리기`, [...promoted, t], args, month, null));
    const nm = el('span', 'pf-buyname'); nm.appendChild(tickName(t));
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
  for (const t of names) { const o = el('option'); o.value = t; if (cands.includes(t)) o.label = '이번 달 구매 후보'; dl.appendChild(o); }
  f.appendChild(dl);
  if (cands.length) {
    const quick = el('div', 'pf-row');
    quick.appendChild(el('span', 'pf-note', '이번 달 구매 후보:'));
    for (const t of cands) { const b = el('button', 'pf-btn pf-btn-quiet', t); b.type = 'button'; b.addEventListener('click', () => { tick.value = t; side.value = 'buy'; }); quick.appendChild(b); }
    f.appendChild(quick);
  }
  // 계좌(2026-10-28 한국 계좌): Robinhood | 키움. 키움은 수수료(달러)를 함께 적는다
  const acct = field('계좌', el('select'));
  for (const [v, t] of [['rh', 'Robinhood'], ['kw', '키움']]) { const o = el('option', null, t); o.value = v; acct.appendChild(o); }
  const qty = field('수량(주, 소수 가능)', el('input')); qty.type = 'number'; qty.min = '0'; qty.step = 'any';
  const price = field('체결가(USD)', el('input')); price.type = 'number'; price.min = '0'; price.step = '0.0001';
  const fee = field('수수료(USD, 키움만)', el('input')); fee.type = 'number'; fee.min = '0'; fee.step = '0.01';
  const feeLab = fee.closest('label'); const syncFee = () => { feeLab.hidden = acct.value !== 'kw'; if (acct.value !== 'kw') fee.value = ''; };
  acct.addEventListener('change', syncFee); syncFee();   // Robinhood는 수수료 0(카드 보유 계산과 맞게, dr)
  const btn = el('button', 'pf-btn', '기록'); btn.type = 'button';
  const msg = msgLine();
  f.appendChild(btn); f.appendChild(msg);
  twoStep(btn, msg, '이대로 기록합니다. 맞으면 한 번 더 누르세요.', async () => {
    const x = { date: date.value, ticker: tick.value.trim().toUpperCase(), side: side.value, qty: Number(qty.value), price: Number(price.value),
      ...(acct.value === 'kw' ? { account: 'kw' } : {}), ...(Number(fee.value) > 0 ? { fee: Math.round(Number(fee.value) * 100) / 100 } : {}) };
    if (fee.value && !(Number(fee.value) >= 0)) throw new Error('수수료는 0 이상 숫자로 넣으세요.');
    const bad = checkTrade(x, etDate(Date.now()));
    if (bad) throw new Error(bad);
    await handlers.trade(x);
    done?.();
  }, f);
  box.appendChild(f);
  // pre = { qty, price, side, account } — 매도 탭은 매도·계좌·수량만 채우고 체결가는 비운다(2026-11-03)
  box.fill = (t, pre) => {
    if (t) { tick.value = t; side.value = pre?.side || 'buy'; }
    if (pre?.account) { acct.value = pre.account; syncFee(); }
    if (pre?.qty != null) qty.value = String(pre.qty);
    price.value = pre?.price != null ? String(pre.price) : '';
  };
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
// 내 계좌 탭(2026-10-28 C안)의 숫자: 계좌별 평가액·현금·보유(기록일 기준, 한눈에 탭과 같은 계산), 수익률(달러 — 실제 계좌 계좌별 줄,
// Robinhood·합계는 10/01부터의 공통 과거를 곱함), 키움 원화 성과·환율 수익률, 오늘 환율
export function accountsState(model) {
  const recs = model.records || [];
  const now = model.now ?? Date.now(), today = etDate(now);
  const closeNow = (t) => { for (let k = recs.length - 1; k >= 0; k--) { const c = recs[k].cards?.[t]?.close ?? recs[k].prices?.[t]; if (typeof c === 'number' && !recs[k].cards?.[t]?.priceStale) return c; } return null; };
  const { events, conflicts } = ledgerActive(model.ledger);
  const h = model.main?.holdings || {};
  const rh = currentHoldings(h.rows, h.asOf, tradesOf(model.trades, RH), today);
  const depIn = rh.hasCash ? depositsSince(model.allDeposits || Object.fromEntries(Object.entries(model.bundle?.deposits || {})
    .map(([k, v]) => ['b0:' + k, v.cancels ? { ...v, cancels: 'b0:' + v.cancels } : v])), rh.base || '', today) : [];   // 한눈에 탭과 같은 폴백(dr)
  if (depIn.length) rh.cash = Math.round((rh.cash + depIn.reduce((a, p) => a + p.amount, 0)) * 100) / 100;
  const kw = kwState(events, model.trades, today, 'rec', recs);
  const rows = (list) => list.map((x) => { const c = closeNow(x.ticker); return { ticker: x.ticker, qty: x.qty, value: c == null ? null : x.qty * c, vsAvg: c != null && x.avgPrice ? c / x.avgPrice - 1 : null }; })
    .sort((a, b) => (b.value || 0) - (a.value || 0));
  // 가격 없는 종목이 있으면 평가액은 '확인된 부분합'이고 missing에 남긴다(0달러로 합치지 않음을 화면에 알림, dr)
  const val = (r, cash) => r.reduce((a, x) => a + (x.value || 0), 0) + (cash || 0);
  const miss = (r) => r.filter((x) => x.value == null).map((x) => x.ticker);
  const rhRows = rows(rh.holdings), kwRows = rows(kw.holdings);
  const fxAt = fxSeries(recs, model.fxHistory);
  const lastS = recs.length ? recs[recs.length - 1].session : null;
  const fxNow = lastS ? fxAt(lastS) : null;
  const acc = model.result?.accounts || null;
  const real = model.result?.scenarios?.find((s) => s.id === 'REAL');
  const rs = real ? summarizeKnown(real) : null;
  const hist = rs?.started ? historyPrefix(model.main?.preStart, model.pastBundles, model.bundle?.snapshot, rs.started, real?.startValue, { records: recs, trades: model.trades }) : null;
  const pre = (t) => (t == null ? null : hist && !hist.why ? withPrefix(t, null, hist).twr : t);
  // Robinhood 줄은 Robinhood 줄의 출발로 따로 잇는다(키움 시작 상태가 있으면 합계 출발과 달라지므로, dr)
  const rhLine = acc?.rh;
  const histRh = rhLine?.started ? historyPrefix(model.main?.preStart, model.pastBundles, model.bundle?.snapshot, rhLine.started, rhLine.startValue, { records: recs, trades: tradesOf(model.trades, RH) }) : null;
  const rhPre = (t) => (t == null ? null : histRh && !histRh.why ? withPrefix(t, null, histRh).twr : t);
  const rhS = acc?.rh ? summarizeKnown(acc.rh) : null, kwS = acc?.kw ? summarizeKnown(acc.kw) : null;
  const kwValue = val(kwRows, kw.cash);
  const krw = acc?.kw ? krwPerformance(acc.kw, events, fxAt, miss(kwRows).length ? null : kwValue, fxNow) : null;
  return {
    today, fx: fxNow, hasCash: rh.hasCash, from: hist && !hist.why ? hist.from : rs?.started || null,
    total: { value: val(rhRows, rh.cash) + val(kwRows, kw.cash), twr: pre(rs?.twr ?? null) },
    rh: { value: val(rhRows, rh.cash), cash: rh.cash, rows: rhRows, missing: miss(rhRows), twr: rhPre(rhS?.twr ?? null) },
    kw: { value: val(kwRows, kw.cash), cash: kw.cash, rows: kwRows, missing: miss(kwRows), twr: kwS?.twr ?? null, started: (acc?.kw?.days || []).find((x) => (x.value || 0) > 0 || (x.flowUsd || 0) > 0)?.date || null, krw, used: events.length > 0 || kw.holdings.length > 0 },   // started: 첫 돈이 들어온 날(시작 스냅샷 날의 0원은 출발로 보지 않음)
    events, conflicts,
    autoMonth: (dEff) => {   // 환전 기록의 몫 달(카드의 몫 자동 규칙과 같음): 반영일 달에 남은 회차가 있으면 그 달, 없으면 다음 달
      const mv = monthView(model.result, lastS || '', today);
      const planM = mv?.plan && !mv.demo ? mv.plan.decisionDate?.slice(0, 7) : null;
      return ledgerMonth(dEff, planM, mv?.plan?.rounds);
    },
  };
}

export function renderTabs(roots, model, smodel, handlers) {
  renderHome(roots.home, model, handlers);
  if (roots.accounts) renderAccounts(roots.accounts, accountsState(model), handlers);
  const st = roots.strategy, { result } = model, recs = smodel.records || [];
  st.textContent = '';
  const lastRec = recs.length ? recs[recs.length - 1].session : null;
  if (smodel.recordsError) st.appendChild(el('p', 'pf-warn', '일별 기록을 불러오지 못했습니다. 새로고침해 보세요.'));
  else if (smodel.calcError) st.appendChild(el('p', 'pf-warn', '계산하지 못했습니다: ' + smodel.calcError));
  else if (!result && !(smodel.bundle && !smodel.bundle.closed)) st.appendChild(el('p', 'pf-note', '전략 비교를 시작하면(기록·관리 탭의 시작 스냅샷) 여기에 비교 표·그래프·매매 기록이 보입니다.'));
  // 순위·편집기·내 전략 카드·접은 표(2026-10-21 디자인 시안 선택 — -rank.js). 모형 설명은 순위 제목 옆 "?"에서 펼친다
  const infoBase = (r) => r ? `큰 사건 예외를 뺀 정기 운용 모형 · 엔진 ${ENGINE_VERSION} · 마지막 기록 ${lastRec} · 빠진 날 ${r.missingSessions.length}일` : '';
  // A(그대로 보유)는 화면에서 숨긴다 — 계산(다른 전략 출발점·SPY 기준선)에는 그대로 쓰므로 baseA로 넘긴다(사용자 결정 2026-10-22)
  let shown = result ? { ...result, scenarios: result.scenarios.filter((s) => s.id !== 'A'), baseA: result.scenarios.find((s) => s.id === 'A') || null } : null;
  // 모든 줄을 10/01부터(사용자 결정 2026-10-25): 출발일까지의 공통 과거(내 실제 계좌)를 각 줄의 날마다 수익률·SPY 대비와 SPY 점선 앞에 곱한다
  const A0 = shown?.baseA, hist = A0?.started ? historyPrefix(model.main?.preStart, model.pastBundles, smodel.bundle?.snapshot, A0.started, A0.startValue, { records: recs, trades: model.trades }) : null;
  let histNote = '', since = '';
  if (shown && hist && !hist.why) {
    const fix = (s) => ({ ...s, twrSince: summarize(s).twr, days: (s.days || []).map((d) => { if (d.twr == null) return d; const w = withPrefix(d.twr, d.vs?.SPY ?? null, hist); return { ...d, twr: w.twr, vs: d.vs ? { SPY: w.vsSPY } : d.vs }; }),
      baselines: s.baselines ? { ...s.baselines, SPY: (s.baselines.SPY || []).map((p) => (p.twr == null || hist.spy == null ? p : { ...p, twr: (1 + hist.spy) * (1 + p.twr) - 1 })) } : s.baselines });
    shown = { ...shown, scenarios: shown.scenarios.map(fix), baseA: fix(shown.baseA) };
    histNote = ` · ${md(hist.from)}부터 이어 봄(${md(A0.started)}까지는 모든 줄이 내 실제 계좌)`;
    since = `수익률은 ${md(hist.from)}부터 — ${md(A0.started)}까지는 모든 줄이 내 실제 계좌 기록이고, 차이는 그 뒤에만 생깁니다.`;
  } else if (hist?.why) { histNote = ` · ${md(model.main.preStart.from)} 기록 못 이음: ${hist.why}`; since = `${md(model.main.preStart.from)}부터 이어 보지 못함: ${hist.why}.`; }
  else if (shown && model.main?.preStart && !A0?.started) since = `${md(model.main.preStart.from)}부터 이어 보기는 비교가 출발하면(시작 뒤 첫 완전한 기록) 붙습니다.`;
  renderStrategy(st, smodel.recordsError || smodel.calcError ? { ...model, result: null } : { ...model, result: shown }, { ...smodel, info: infoBase(result) + histNote, since, from: hist && !hist.why ? hist.from : A0?.started || null, startDay: A0?.started || null }, handlers);
  // 시작 폼 미리 채우기: 내 자산과 같은 계산으로 마지막 기록일까지(그 뒤 매매는 빼고)
  const hh = model.main?.holdings || {};
  const pc = currentHoldings(hh.rows, hh.asOf, model.trades, lastRec || etDate(model.now ?? Date.now()));
  smodel = { ...smodel, prefill: { asOf: hh.asOf || null, upTo: lastRec, holdings: pc.holdings, cash: pc.hasCash ? pc.cash : null, clipped: pc.clipped } };
  // 기록·관리: 모든 기록 한 줄 타임라인(2026-10-21 디자인 시안 선택 — -records.js)
  renderManage(roots.manage, model, smodel, handlers, { currentHoldings, checkTrade, etDate });
}
