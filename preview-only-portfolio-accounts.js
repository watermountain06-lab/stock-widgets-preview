// preview 전용 Portfolio 탭 — 한국 계좌(키움, 2026-10-28 사용자 결정·dr 5라운드 설계). 라이브로 옮기지 않는다 — pipeline/site_ui/UI_DIFF.md 1절 portfolio.
//
// 키움은 원화를 직접 달러로 바꿔(환전) 미국 주식을 산다. 거래 내역 파일이 없어 손으로 기록한다.
//   계좌 장부(Firestore portfolio/trades 문서의 ledger 지도 — 묶음과 무관하게 한 번만 적는다): fx(환전 usd·krw), fxOut(역환전), income(배당·이자)
//   정정 = 취소 기록 + 새 기록(root = 정정 체인의 최초 id, replaces = 바로 앞 id)을 한 번에 쓴다. 반영일·몫 달·기록 시각은 root의 것
//   (income만 지급일을 따른다). 한 체인에 살아 있는 기록이 둘 이상이면 '정정 충돌'로 알린다.
//   시간: 기록 시각(카드 계좌 현금 칸) · 반영일(= root 기록 시각 다음 장 시작 — 엔진·실제 계좌·한도 몫) · 환전일(date, 보여 주기만)
//   환전 달러는 보통 입금과 같은 길로 엔진·실제 계좌·카드 한도에 한 번씩 들어간다(id 접두어 L:). 배당은 수익(외부 흐름 아님).
// 설계: pipeline/portfolio/STRATEGY_DESIGN.md '한국 계좌'.
import { depositTiming, twr, _internal } from './preview-only-portfolio-engine.js?v=13';

export const KW = 'kw', RH = 'rh';
export const acctOf = (x) => (x && x.account === KW ? KW : RH);   // 계좌 칸이 없는 옛 매매는 Robinhood
const etDate = (iso) => new Date(Date.parse(iso)).toLocaleDateString('en-CA', { timeZone: 'America/New_York' });
const cents = (v) => Math.round(v * 100) / 100;
const isMonth = (m) => /^\d{4}-(0[1-9]|1[0-2])$/.test(m || '');

// 장부 → 유효 사건 목록. 돌려주는 값: { events: [{id, root, kind, usd, krw, date, note, recordedAt(root), forMonth(root), day(반영일, fx·fxOut),
//   rec(root 기록일)}], conflicts: [root] }. 취소된 기록, 살아 있는 기록이 없는 체인은 빠진다.
export function ledgerActive(ledger) {
  const all = Object.entries(ledger || {});
  const cancelled = new Set(all.filter(([, x]) => x && x.cancels).map(([, x]) => x.cancels));
  const byId = new Map(all.filter(([, x]) => x && !x.cancels).map(([id, x]) => [id, x]));
  const groups = new Map();
  for (const [id, x] of byId) {
    const root = x.root && byId.has(x.root) ? x.root : x.root ? x.root : id;
    if (!groups.has(root)) groups.set(root, []);
    groups.get(root).push([id, x]);
  }
  const events = [], conflicts = [];
  for (const [root, list] of groups) {
    const r = byId.get(root) || list.map(([, x]) => x).sort((a, b) => ((a.recordedAt || '') < (b.recordedAt || '') ? -1 : 1))[0];
    const live = list.filter(([id]) => !cancelled.has(id)).sort(([, a], [, b]) => ((a.recordedAt || '') < (b.recordedAt || '') ? -1 : 1));
    if (!live.length || !r?.recordedAt) continue;
    if (live.length > 1) {   // 정정 충돌(dr): 계산에서 빼고, 살아 있는 기록을 모두 목록에 보여 하나를 취소하게 한다
      conflicts.push({ root, ids: live.map(([id, x]) => ({ id, kind: x.kind, usd: x.usd, krw: x.krw, date: x.date })) });
      continue;
    }
    const [id, x] = live[live.length - 1];
    if (!['fx', 'fxOut', 'income'].includes(x.kind) || !(x.usd > 0)) continue;
    const ev = { id, root, kind: x.kind, usd: cents(x.usd), krw: Math.round(Number(x.krw) || 0), date: x.date || etDate(r.recordedAt), note: x.note || '',
      recordedAt: r.recordedAt, rec: etDate(r.recordedAt) };
    if (x.kind !== 'income') {
      const tm = depositTiming(r.recordedAt);
      if (!tm.day) continue;
      ev.day = tm.day;
      ev.forMonth = isMonth(r.forMonth) && r.forMonth >= tm.day.slice(0, 7) ? r.forMonth : tm.day.slice(0, 7);   // fxOut도 저장된 몫 달(dr)
    }
    events.push(ev);
  }
  events.sort((a, b) => (a.recordedAt < b.recordedAt ? -1 : 1));
  return { events, conflicts };
}

// fx·fxOut을 입금 지도 모양으로(엔진·실제 계좌·카드 한도가 그대로 읽는다). 키에 L: 접두어, 기록 시각·몫 달은 root의 것
export function ledgerDeposits(events) {
  const out = {};
  for (const e of events) {
    if (e.kind === 'income') continue;
    out['L:' + e.root] = { amount: e.usd, ...(e.kind === 'fxOut' ? { kind: 'withdraw' } : {}), ...(e.forMonth > e.day.slice(0, 7) ? { forMonth: e.forMonth } : {}),
      recordedAt: e.recordedAt, account: KW };
  }
  return out;
}
export const incomeList = (events) => events.filter((e) => e.kind === 'income').map((e) => ({ date: e.date, amount: e.usd, account: KW }));

// 시작 스냅샷에 키움 시작 상태를 합친다(종목 수량 합, 현금 합) — 엔진·실제 계좌 합계 줄의 출발(설계 4절)
export function mergeStart(snapshot, kw0) {
  const holdings = { ...(snapshot.holdings || {}) };
  for (const h of kw0?.holdings || []) holdings[h.ticker] = Math.round(((Number(holdings[h.ticker]) || 0) + h.qty) * 1e6) / 1e6;
  return { ...snapshot, holdings, cash: cents((Number(snapshot.cash) || 0) + (kw0?.cash || 0)) };
}

// 매매 지도를 계좌로 거른다(취소 기록은 대상이 남는 쪽에 함께 둔다)
export function tradesOf(trades, account) {
  const all = Object.entries(trades || {});
  const keep = new Set(all.filter(([, x]) => !x.cancels && acctOf(x) === account).map(([id]) => id));
  return Object.fromEntries(all.filter(([id, x]) => (x.cancels ? keep.has(x.cancels) : keep.has(id))));
}

// 키움 보유·현금(달러). mode 'rec': 카드 표시(기록일 ≤ upTo인 환전, 거래일 ≤ upTo인 매매·배당), mode 'eff': 엔진 시작 상태(반영일·거래일 ≤ upTo).
// 평균 단가 = 남은 원가 ÷ 수량(매수 원가에 수수료 포함, 매도는 평균 단가로 원가를 줄임)
// splits: 일별 기록 [{splits:[{id,ticker,effectiveDate,ratio}]}] — 효력일이 매매 뒤·upTo 이하면 수량에 곱한다(실제 계좌 줄과 같게, dr)
export function kwState(events, trades, upTo, mode = 'eff', records) {
  let cash = 0;
  for (const e of events) {
    const d = e.kind === 'income' ? e.date : mode === 'rec' ? e.rec : e.day;
    if (!d || d > upTo) continue;
    cash += e.kind === 'fxOut' ? -e.usd : e.usd;
  }
  const pos = new Map();
  const list = Object.entries(tradesOf(trades, KW));
  const cancelled = new Set(list.filter(([, x]) => x.cancels).map(([, x]) => x.cancels));
  const live = list.filter(([id, x]) => !x.cancels && !cancelled.has(id) && x.date <= upTo).map(([, x]) => x)
    .sort((a, b) => (a.date !== b.date ? (a.date < b.date ? -1 : 1) : a.side !== b.side ? (a.side === 'buy' ? -1 : 1) : (a.recordedAt || '') < (b.recordedAt || '') ? -1 : 1));
  const seen = new Set(), splits = [];
  for (const r of records || []) for (const sp of r.splits || []) if (!seen.has(sp.id) && sp.ratio > 0 && sp.effectiveDate <= upTo) { seen.add(sp.id); splits.push(sp); }
  splits.sort((a, b) => (a.effectiveDate < b.effectiveDate ? -1 : 1));
  let si = 0;
  const applySplits = (before) => { while (si < splits.length && splits[si].effectiveDate <= before) { const sp = splits[si++], p = pos.get(sp.ticker); if (p && p.qty > 0) p.qty = Math.round(p.qty * sp.ratio * 1e6) / 1e6; } };
  for (const x of live) {
    applySplits(x.date);   // 분할 효력일이 매매일 이하면 매매 전에 적용(효력일 장 시작 전 — 실제 계좌 줄과 같은 순서)
    const p = pos.get(x.ticker) || { qty: 0, cost: 0 };
    const fee = Number(x.fee) || 0, amt = cents(x.qty * x.price);
    if (x.side === 'buy') { p.qty += x.qty; p.cost += amt + fee; cash -= amt + fee; }
    else { const q = Math.min(x.qty, p.qty), avg = p.qty ? p.cost / p.qty : 0; if (q > 0) { p.qty -= q; p.cost -= q * avg; cash += cents(q * x.price) - fee; } }
    pos.set(x.ticker, p);
  }
  applySplits(upTo);
  const holdings = [...pos].filter(([, p]) => p.qty > 1e-9).map(([t, p]) => ({ ticker: t, qty: Math.round(p.qty * 1e6) / 1e6, avgPrice: p.qty ? p.cost / p.qty : null, account: KW }))
    .sort((a, b) => (a.ticker < b.ticker ? -1 : 1));
  return { holdings, cash: cents(cash) };
}

// 환율: 평가일 d의 원/달러 = 그날 공개 기록 fx.USDKRW, 없으면 fx_history.json, 그날 값이 없으면 직전 값(5거래일까지). 그보다 오래 비면 null(미확정)
export function fxSeries(records, history) {
  const cal = _internal.makeCalendar();
  const raw = new Map();
  for (const [d, v] of Object.entries(history?.rates || {})) if (v > 0) raw.set(d, { v, src: 'hist' });
  for (const r of records || []) { const v = r.fx?.USDKRW; if (v > 0) raw.set(r.session, { v, src: 'rec', bar: r.fx.bar }); }   // 공개 기록 값 우선
  return (d) => {
    let i = cal.index(d);
    if (i < 0) return null;
    for (let k = 0; k <= 5 && i - k >= 0; k++) { const x = raw.get(cal.sessions[i - k]); if (x) return { rate: x.v, from: cal.sessions[i - k], bar: x.bar || null, carried: k > 0 }; }
    return null;
  };
}

// 원화 성과(설계 6절): 원화 TWR(평가 = 달러 평가 × 그날 환율, 흐름 = 달러 흐름 × 반영일 전날 환율 — 스프레드는 금액에만),
// 금액 = 지금 원화 가치 + 역환전 받은 원화 − 환전에 쓴 원화, 평균 환전 환율 = 쓴 원화 ÷ 환전 받은 달러(누적 매입 기준),
// 환율 수익률 = 오늘 환율 ÷ 평균 환전 환율 − 1(사용자 요청 2026-10-28 — 단순 지표, 여러 번 나눠 바꾸면 원화 TWR과 곱이 정확히 맞지는 않는다)
// valueNow: 카드와 같은 기록일 기준 키움 평가액(금액 칸 — 원금도 모든 기록을 쓰므로 같은 기준, dr). 원화 TWR은 반영일 기준 줄
// fxNow: 화면의 '오늘 환율'과 같은 값(환율 수익률·원화 금액이 같은 환율을 쓰게, dr)
export function krwPerformance(kwLine, events, fxAt, valueNow, fxNow) {
  const days = (kwLine?.days || []);
  const cal = _internal.makeCalendar();
  let prevV = 0, unknownFlow = false;
  const rows = days.map((x) => {
    const f = fxAt(x.date), pd = cal.sessions[cal.index(x.date) - 1], fp = pd ? fxAt(pd) : null;
    // 흐름 환율 = 전날 환율. 전날 환율이 없을 때 그날 환율로 대신하는 것은 자본이 없던 날(첫 유입)만 — 그 밖에는 그날을 미확정으로(dr)
    const fr = fp || (prevV > 0 ? null : f);
    const fl = x.flowUsd ? (fr ? x.flowUsd * fr.rate : NaN) : 0;
    if (!Number.isFinite(fl)) unknownFlow = true;   // 환율 모르는 날의 흐름 — 다음 날 평가액 증가가 수익으로 잡히지 않게 원화 TWR 전체를 미확정으로(dr)
    const row = { value: x.value == null || !f || !Number.isFinite(fl) ? null : x.value * f.rate, flow: Number.isFinite(fl) ? fl : 0 };
    if (x.value != null) prevV = x.value;
    return row;
  });
  const k0 = rows.findIndex((r) => r.value !== null);
  const t = k0 < 0 ? [] : twr(rows.slice(k0));
  const krwTwr = t.length && !unknownFlow ? t[t.length - 1] : null;
  const fx = events.filter((e) => e.kind === 'fx'), out = events.filter((e) => e.kind === 'fxOut');
  const krwIn = fx.reduce((a, e) => a + e.krw, 0), usdIn = fx.reduce((a, e) => a + e.usd, 0), krwOut = out.reduce((a, e) => a + e.krw, 0);
  const last = [...days].reverse().find((x) => x.value != null);
  const fNow = fxNow !== undefined ? fxNow : last ? fxAt(last.date) : null;   // null = 미확정(넘긴 값 그대로), 안 넘겼을 때만 줄의 마지막 날 환율(dr)
  const vNow = valueNow !== undefined ? (typeof valueNow === 'number' ? valueNow : null) : last ? last.value : null;   // null = 가격 없음 등으로 미확정(dr)
  const avgRate = usdIn > 0 && krwIn > 0 ? krwIn / usdIn : null;
  return {
    krwTwr, avgRate, krwIn, krwOut, usdIn: cents(usdIn),
    rate: fNow ? fNow.rate : null, rateDate: fNow ? fNow.from : null, rateCarried: !!fNow?.carried,
    valueKrw: vNow != null && fNow ? Math.round(vNow * fNow.rate) : null,
    pnlKrw: vNow != null && fNow && krwIn ? Math.round(vNow * fNow.rate + krwOut - krwIn) : null,
    fxReturn: avgRate && fNow ? fNow.rate / avgRate - 1 : null,
  };
}
