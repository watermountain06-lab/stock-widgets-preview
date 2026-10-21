// preview 전용 Portfolio 탭 — "한눈에" 하위 탭(2026-10-20, 시안 A2 사용자 선택). 라이브로 옮기지 않는다 — pipeline/site_ui/UI_DIFF.md 1절 portfolio.
//
// 내 자산(올린 보유 + 그 뒤 기록한 실제 매매), 실제 매매 기록 칸, 이번 달 할 일, 이번 달 운용(점검일 결정과 회차 진행),
// 전략 비교 도넛(전략마다 지금 들고 있는 종목·현금 비중, 가운데 수익률)을 그린다. 계산은 엔진 결과(replay)를 받아 쓰고,
// 저장은 preview-only-portfolio.js가 넘겨 준 handlers로 한다. 순수 함수(currentHoldings·monthView)는 node 시험이 부른다
// (pipeline/portfolio/test_strategy_view.mjs). 실제 매매 기록은 모의 전략 계산에는 넣지 않고, 전략 비교의 "내 실제 계좌" 줄만 쓴다(preview-only-portfolio-actual.js).
import { el, twoStep, msgLine, usd, pct, pp, shares, label, summarize } from './preview-only-portfolio-strategy.js?v=15';
import { renderStrategy } from './preview-only-portfolio-rank.js?v=4';
import { renderManage } from './preview-only-portfolio-records.js?v=3';
import { ENGINE_VERSION, depositTiming } from './preview-only-portfolio-engine.js?v=2';
import { effectiveDeposits } from './preview-only-portfolio-actual.js?v=7';

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

// 손실 한도(원칙 9, 2026-10-21 사용자 결정): 한 종목이 평균 단가보다 limit(20%) 이상 떨어지면 알림만 띄운다 — 엔진 계산·자동 매도는 없다.
// holdings: currentHoldings().holdings, close(t): 최근 종가 또는 null. 평균 단가나 가격이 없는 종목은 건너뛴다. 하락이 큰 순.
export const LOSS_LIMIT = 0.2;
const dropText = (d) => (d * 100).toFixed(1).replace('-', '−') + '%';
export function lossAlerts(holdings, close, limit = LOSS_LIMIT) {
  const out = [];
  for (const x of holdings || []) {
    const c = close(x.ticker);
    if (c == null || !(x.avgPrice > 0)) continue;
    const drop = c / x.avgPrice - 1;
    if (drop <= -limit + 1e-9) out.push({ ticker: x.ticker, drop, avgPrice: x.avgPrice, close: c });
  }
  return out.sort((a, b) => a.drop - b.drop || (a.ticker < b.ticker ? -1 : 1));
}

// 이번 달 운용에 보여 줄 시나리오(내 원칙 B가 있으면 그것, 없으면 처음 만든 시나리오)와 그달 계획
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

// ---- 그리기 ----
// model = { main(올린 데이터), trades(실제 매매 지도), result|null, bundle|null, byId, records, now }
// handlers = { trade({date, ticker, side, qty, price}), editTrade(id, …), deleteTrade(id), goto(tab) }
export function renderHome(root, model, handlers) {
  root.textContent = '';
  const recs = model.records || [];
  const last = recs[recs.length - 1] || null;
  // 가격·판정은 마지막 '완전한' 기록에서 읽는다(파이프라인 실패 날은 엔진도 값을 쓰지 않는다)
  const lastFull = [...recs].reverse().find((r) => r.pipelineFull) || null;
  const close = (t) => { const c = lastFull && (lastFull.cards?.[t]?.close ?? lastFull.prices?.[t]); return typeof c === 'number' ? c : null; };
  const tierOf = (t) => (lastFull && lastFull.cards?.[t] ? lastFull.cards[t].tier : null);
  const h = model.main?.holdings || {};
  const now = model.now ?? Date.now(), today = etDate(now);
  const cur = currentHoldings(h.rows, h.asOf, model.trades, today);
  // 전략 비교에 기록한 입금(실제로 계좌에 넣은 돈)도 올린 보유 기준일 뒤·오늘까지 반영일이면 현금에 더한다(dr r1 — 실제 계좌 줄과 같은 돈).
  // 끝낸 묶음의 입금도 실제 돈이므로 모든 묶음을 본다(dr r2, model.allDeposits — 없으면 지금 묶음)
  const depIn = cur.hasCash ? depositsSince(model.allDeposits || Object.fromEntries(Object.entries(model.bundle?.deposits || {})
    .map(([k, v]) => ['b0:' + k, v.cancels ? { ...v, cancels: 'b0:' + v.cancels } : v])), cur.base || '', today) : [];
  if (depIn.length) cur.cash = Math.round((cur.cash + depIn.reduce((a, p) => a + p.amount, 0)) * 100) / 100;
  const mv = monthView(model.result, last ? last.session : '', today);
  const losses = lossAlerts(cur.holdings, close);
  const lossOf = new Map(losses.map((l) => [l.ticker, l]));

  // 2026-10-21 최종 시안(Claude 안 + ChatGPT 안): 자산 요약 띠 → 왼쪽(다음 할 일·보유 자산) | 오른쪽(이번 달 운용·전략과 나란히).
  // 경고 문구는 페이지 맨 아래 한 번(html), 매매 기록 양식은 탭 줄의 "＋ 매매 기록"이 여는 창(어느 탭에서나).
  // 색은 종목에 고정: 7자리를 내 보유 평가액 큰 순으로 먼저 채우고, 남는 자리를 전략 보유 합산 큰 순으로 채운다
  let total = cur.cash, missing = [];
  for (const x of cur.holdings) { const c = close(x.ticker); if (c == null) missing.push(x.ticker); else total += x.qty * c; }
  const myVal = new Map(cur.holdings.map((x) => { const c = close(x.ticker); return [x.ticker, c == null ? 0 : x.qty * c]; }));
  const simW = new Map();
  for (const sc of model.result?.scenarios || []) if (sc.started) for (const t of Object.keys(sc.holdings)) { const c = close(t); simW.set(t, (simW.get(t) || 0) + (c == null ? 0 : sc.holdings[t] * c)); }
  const byVal = (m) => [...m.entries()].filter(([, v]) => v > 0).sort((a, b) => b[1] - a[1]).map(([t]) => t);   // 가격 없는 종목은 색 자리를 받지 않는다
  const named = [...new Set([...byVal(myVal), ...byVal(simW)])].slice(0, SLOTS).sort();
  const color = (t) => (t === '현금' ? 'var(--pf-cash)' : named.includes(t) ? `var(--pf-k${named.indexOf(t) + 1})` : 'var(--pf-other)');
  const has = cur.holdings.length || cur.hasCash;
  const real = model.result?.scenarios?.find((s) => s.id === 'REAL');
  const rs = real ? summarize(real) : null;

  // 매매 기록 창: 탭 줄의 "＋ 매매 기록"(html #pf-trade-open)과 아래 "후보로 매수 기록"이 연다
  const dlg = tradeDialog(model, handlers, recs, mv, today);
  const openBtn = document.getElementById('pf-trade-open');
  if (openBtn) openBtn.onclick = () => dlg.open();

  // 1) 자산 요약 띠
  const band = el('section', 'pf-panel pf-band');
  const cell = (k, v, sub, cls) => { const d = el('div', 'pf-bandcell'); d.appendChild(el('div', 'pf-k', k)); d.appendChild(el('div', 'pf-v' + (cls ? ' ' + cls : ''), v)); if (sub) d.appendChild(el('div', 'pf-s', sub)); band.appendChild(d); };
  cell('내 자산', has ? usd0(total) : '—', !has ? '기록·관리 탭에서 보유를 올리세요'
    : (cur.hasCash ? `주식 ${usd0(total - cur.cash)} · 현금 ${usd0(cur.cash)}` : '현금 모름(올린 보유에 현금 줄 없음)') + (missing.length ? ` · 가격 없음 ${missing.join(', ')}` : ''));
  cell('시작 뒤 수익률', rs?.twr != null ? pct(rs.twr) : '—', rs?.started ? `${md(rs.started)}부터 · 내 실제 계좌` : '전략 비교를 시작하면 보입니다', 'pf-v-accent');
  cell('SPY 대비', rs?.vs?.SPY != null ? pp(rs.vs.SPY) : '—', lastFull ? `${md(lastFull.session)} 종가 기준` : '');
  root.appendChild(band);

  const grid = el('div', 'pf-homegrid');
  const left = el('div', 'pf-homecol pf-homemain'), right = el('div', 'pf-homecol pf-homeside');

  // 2) 이번 달, 다음 할 일
  const next = el('section', 'pf-panel pf-next');
  const na = nextAction(mv);
  const nh = el('div', 'pf-nexthead');
  const nt = el('div');
  nt.appendChild(el('div', 'pf-eyebrow2', '이번 달, 다음 할 일'));
  nt.appendChild(el('h2', 'pf-nexttitle', na ? na.title : !model.bundle || model.bundle.closed ? '전략 비교를 시작하세요' : '원칙 계산 출발 대기'));
  nt.appendChild(el('p', 'pf-sub', na ? na.sub : !model.bundle || model.bundle.closed
    ? '기록·관리 탭에서 시작 스냅샷을 정하면 매달 점검일 결정과 회차 진행이 여기에 보입니다.'
    : '시작 스냅샷의 종목에 모두 그날 가격이 있어야 출발합니다(전략 비교 탭의 출발 대기 이유를 보세요).'));
  nh.appendChild(nt);
  const cands = mv?.plan && !mv.stale ? mv.plan.candidates : [];
  const buyBtn = el('button', 'pf-btn', cands.length ? '후보로 매수 기록' : '매매 기록'); buyBtn.type = 'button';
  buyBtn.addEventListener('click', () => dlg.open(cands[0]));
  nh.appendChild(buyBtn);
  next.appendChild(nh);
  if (na && na.total) {
    const seg = el('div', 'pf-segs'); seg.setAttribute('role', 'img'); seg.setAttribute('aria-label', `${na.total}회 중 ${na.done}회 진행`);
    for (const s of mv.steps.slice(1)) seg.appendChild(el('span', 'pf-seg-' + s.state));
    next.appendChild(seg);
  }
  for (const l of losses) {
    const w = el('div', 'pf-lossline');
    w.appendChild(el('strong', null, '손실 알림'));
    w.appendChild(el('span', null, ` ${l.ticker} 평균 단가 대비 ${dropText(l.drop)} · 자동으로 팔지 않습니다(원칙 9). 판정과 함께 직접 판단하세요.`));
    next.appendChild(w);
  }
  // 이번 달(미국 동부) 기록한 입금 중 효력 있는 취소(반영일 09:30 ET 전)를 뺀 것 — 엔진·기록·관리 탭과 같은 기준
  const month = today.slice(0, 7);
  const allDeps = Object.entries(model.bundle?.deposits || {});
  const gone = new Set(allDeps.filter(([, c]) => c.cancels).filter(([, c]) => {
    const dep = model.bundle.deposits[c.cancels]; if (!dep || dep.cancels) return false;
    const t = depositTiming(dep.recordedAt); return t.day && Date.parse(c.recordedAt) < t.cancelBefore;
  }).map(([, c]) => c.cancels));
  const deps = allDeps.filter(([id, d]) => !d.cancels && !gone.has(id) && d.recordedAt && etDate(Date.parse(d.recordedAt)).slice(0, 7) === month).map(([, d]) => d);
  const stats = el('div', 'pf-nextstats');
  const stat = (k, v) => { const s = el('span', null, k + ' '); s.appendChild(el('strong', null, v)); stats.appendChild(s); };
  stat('매도 검토', mv && mv.plan && !mv.stale ? mv.alerts.length + '건' : '—');
  stat('이번 달 입금', deps.length ? usd0(deps.reduce((a, d) => a + d.amount, 0)) : '없음');
  stat('마지막 기록', last ? md(last.session) : '없음');
  next.appendChild(stats);
  left.appendChild(next);

  // 3) 보유 자산(비중 막대 + 접는 목록)
  const hold = el('section', 'pf-panel');
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
  fold.appendChild(el('summary', null, `보유 종목 ${cur.holdings.length}개 보기 · 판정·평균 단가·평가액`));
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
    const c = close(x.ticker), tier = tierOf(x.ticker);
    const row = el('div', 'pf-hold');
    const nm = el('div');
    const dot = el('i', 'pf-dot'); dot.style.background = color(x.ticker); nm.appendChild(dot);
    nm.appendChild(el('strong', null, x.ticker));
    nm.appendChild(el('small', null, [x.name, shares(x.qty) + '주', x.avgPrice ? '평균 ' + usd(x.avgPrice) : ''].filter(Boolean).join(' · ')));
    const loss = lossOf.get(x.ticker);
    if (loss) { const w = el('span', 'pf-loss', `⚠ 평균 대비 ${dropText(loss.drop)}`); w.title = `원칙 9 손실 한도: 평균 ${usd(loss.avgPrice)} → 종가 ${usd(loss.close)}`; nm.appendChild(w); }
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
  left.appendChild(hold);

  // 4) 이번 달 운용(오른쪽, 짧게)
  right.appendChild(planPanel(mv, model, lastFull));
  // 5) 전략과 나란히(내 실제 계좌·1위·A)
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

// 매매 기록 창(<dialog>). 한 페이지에 하나만 두고 그릴 때마다 내용을 바꾼다. open(ticker)는 그 종목·매수로 채워 연다
function tradeDialog(model, handlers, recs, mv, today) {
  let dlg = document.getElementById('pf-tradedlg');
  if (!dlg) { dlg = el('dialog', 'pf-dialog'); dlg.id = 'pf-tradedlg'; dlg.setAttribute('aria-labelledby', 'pf-tradedlg-h'); document.body.appendChild(dlg); }
  dlg.textContent = '';
  const box = tradeForm(model, handlers, recs, mv, today, () => dlg.close());
  const x = el('button', 'pf-btn pf-btn-quiet pf-dlgclose', '닫기'); x.type = 'button'; x.addEventListener('click', () => dlg.close());
  box.insertBefore(x, box.firstChild);
  dlg.appendChild(box);
  return { open: (ticker) => { box.fill?.(ticker); if (!dlg.open) dlg.showModal?.(); } };
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
  box.fill = (t) => { if (t) { tick.value = t; side.value = 'buy'; } };
  return box;
}

// 이번 달 운용(오른쪽 칸): 점검일 결정, 살 후보(실제로 산 수량), 매도 검토, 예산 사용
function planPanel(mv, model, last) {
  const sec = el('section', 'pf-panel pf-side');
  const head = el('div', 'pf-sidehead'); head.appendChild(el('h2', 'pf-h2s', '이번 달 운용'));
  sec.appendChild(head);
  if (!mv || !mv.plan) { sec.appendChild(el('p', 'pf-note', '첫 점검일(매달 1일, 휴장이면 다음 거래일)에 원칙 기준 살 후보와 매도 검토가 여기에 보입니다.')); return sec; }
  const { plan } = mv;
  head.appendChild(el('span', 'pf-badge', `${md(plan.decisionDate)} 점검` + (mv.stale ? ' · 지난달' : '')));
  if (plan.ruleChanged) sec.appendChild(el('p', 'pf-note', '이번 달은 판정 방식이 바뀌어 매매하지 않습니다(바뀐 판정으로 매도가 생기지 않게).'));
  const row = (k) => { const d = el('div', 'pf-siderow'); d.appendChild(el('div', 'pf-k', k)); sec.appendChild(d); return d; };
  const cr = row(`살 후보 ${plan.candidates.length}종목`);
  const chips = el('div', 'pf-candchips');
  const real = Object.entries(model.trades || {});
  const cancelled = new Set(real.filter(([, x]) => x.cancels).map(([, x]) => x.cancels));
  const realBuys = real.filter(([id, x]) => !x.cancels && !cancelled.has(id) && x.side === 'buy' && x.date >= plan.decisionDate && x.date.slice(0, 7) === plan.decisionDate.slice(0, 7)).map(([, x]) => x);
  for (const t of plan.candidates) {
    const tier = last?.cards?.[t]?.tier;
    const q = realBuys.filter((x) => x.ticker === t).reduce((a, x) => a + x.qty, 0);
    const c = el('span', 'pf-candchip', t); c.title = (tier || '판정 없음') + (q ? ` · 실제로 ${shares(q)}주 삼` : ' · 실제 매수 기록 없음');
    if (q) c.appendChild(el('small', null, ` ${shares(q)}주`));
    chips.appendChild(c);
  }
  if (!plan.candidates.length) chips.appendChild(el('span', 'pf-note', '조건에 맞는 판정 없음'));
  cr.appendChild(chips);
  const ar = row('매도 검토');
  if (!mv.alerts.length) ar.appendChild(el('span', 'pf-note', '없음'));
  for (const f of mv.alerts) ar.appendChild(el('div', 'pf-sideval', `${f.ticker} ${f.observed} · ` + (f.warnOnly ? '비율은 아직 정하지 않음(알림만)' : `${shares(f.shares)}주 나눠 매도`)));
  if (plan.budget > 0) {
    const br = row('원칙 기준 예산 사용(모의)');
    const bar = el('div', 'pf-bar'), fill = el('span'); fill.style.width = Math.min(100, (mv.spent / plan.budget) * 100) + '%'; bar.appendChild(fill);
    br.appendChild(bar); br.appendChild(el('span', 'pf-note', `${usd0(mv.spent)} / ${usd0(plan.budget)}`));
  }
  return sec;
}

// 전략과 나란히: 내 실제 계좌, 1위(실제 계좌 제외), A — 누르면 전략 비교 탭으로
function miniRank(model, handlers) {
  const sec = el('section', 'pf-panel pf-side');
  const head = el('div', 'pf-sidehead'); head.appendChild(el('h2', 'pf-h2s', '전략과 나란히'));
  const go = el('button', 'pf-linkbtn', '전체'); go.type = 'button'; go.addEventListener('click', () => handlers.goto('strategy')); head.appendChild(go);
  sec.appendChild(head);
  const sc = (model.result?.scenarios || []).map((s) => ({ s, m: summarize(s) })).filter(({ m }) => m.twr != null);
  if (!sc.length) { sec.appendChild(el('p', 'pf-note', '전략 비교가 출발하면 내 실제 계좌와 다른 전략의 수익률이 여기에 보입니다.')); return sec; }
  const real = sc.find(({ s }) => s.id === 'REAL'), A = sc.find(({ s }) => s.id === 'A');
  const top = sc.filter(({ s }) => s.id !== 'REAL').sort((a, b) => b.m.twr - a.m.twr)[0];
  const rows = [real, top && top !== A ? { ...top, top: true } : null, A].filter(Boolean);
  const max = Math.max(...rows.map(({ m }) => Math.abs(m.twr)), 0.0001);
  for (const r of rows) {
    const d = el('div', 'pf-minirow' + (r.s.id === 'REAL' ? ' pf-mine' : ''));
    d.appendChild(el('span', null, label(r.s, model.byId) + (r.top ? ' (1위)' : '')));
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
  renderStrategy(st, smodel.recordsError || smodel.calcError ? { ...model, result: null } : model, { ...smodel, info }, handlers);
  // 시작 폼 미리 채우기: 내 자산과 같은 계산으로 마지막 기록일까지(그 뒤 매매는 빼고)
  const hh = model.main?.holdings || {};
  const pc = currentHoldings(hh.rows, hh.asOf, model.trades, lastRec || etDate(model.now ?? Date.now()));
  smodel = { ...smodel, prefill: { asOf: hh.asOf || null, upTo: lastRec, holdings: pc.holdings, cash: pc.hasCash ? pc.cash : null, clipped: pc.clipped } };
  // 기록·관리: 모든 기록 한 줄 타임라인(2026-10-21 디자인 시안 선택 — -records.js)
  renderManage(roots.manage, model, smodel, handlers, { currentHoldings, checkTrade, etDate });
}
