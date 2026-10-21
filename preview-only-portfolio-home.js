// preview 전용 Portfolio 탭 — "한눈에" 하위 탭(2026-10-20, 시안 A2 사용자 선택). 라이브로 옮기지 않는다 — pipeline/site_ui/UI_DIFF.md 1절 portfolio.
//
// 내 자산(올린 보유 + 그 뒤 기록한 실제 매매), 실제 매매 기록 칸, 이번 달 할 일, 이번 달 운용(점검일 결정과 회차 진행),
// 전략 비교 도넛(전략마다 지금 들고 있는 종목·현금 비중, 가운데 수익률)을 그린다. 계산은 엔진 결과(replay)를 받아 쓰고,
// 저장은 preview-only-portfolio.js가 넘겨 준 handlers로 한다. 순수 함수(currentHoldings·monthView)는 node 시험이 부른다
// (pipeline/portfolio/test_strategy_view.mjs). 실제 매매 기록은 모의 전략 계산에는 넣지 않고, 전략 비교의 "내 실제 계좌" 줄만 쓴다(preview-only-portfolio-actual.js).
import { el, table, twoStep, msgLine, usd, pct, pp, shares, label, STRATEGY, REASON, FIXED_NOTICE, compareSection, chartSection, detailSection,
  depositSection, scenarioForm, bundleSection, startForm, waitText } from './preview-only-portfolio-strategy.js?v=12';
import { ENGINE_VERSION, depositTiming } from './preview-only-portfolio-engine.js?v=1';
import { effectiveDeposits } from './preview-only-portfolio-actual.js?v=6';

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

  // 1) 내 자산 | 실제 매매 기록
  const top = el('section', 'pf-panel pf-grid2');
  const left = el('div');
  left.appendChild(el('div', 'pf-eyebrow', 'MY ASSETS'));
  left.appendChild(el('h2', 'pf-h2', '내 자산'));
  let total = cur.cash, missing = [];
  for (const x of cur.holdings) { const c = close(x.ticker); if (c == null) missing.push(x.ticker); else total += x.qty * c; }
  const hero = el('div', 'pf-hero');
  const heroL = el('div');
  heroL.appendChild(el('div', 'pf-big', cur.holdings.length || cur.hasCash ? usd(total) : '—'));
  const sub = el('p', 'pf-sub');
  sub.textContent = cur.holdings.length || cur.hasCash
    ? (cur.hasCash ? `현금 ${usd0(cur.cash)}` : '현금 모름(올린 보유에 현금 줄 없음, 합계에서 뺌)') + ` · ${cur.holdings.length}종목`
      + (lastFull ? ` · ${md(lastFull.session)} 종가 기준` : '') + (missing.length ? ` · 가격 없음 ${missing.join(', ')}(합계는 가격 있는 것만)` : '')
    : '아직 올린 보유가 없습니다. 기록·관리 탭에서 데이터를 올리세요.';
  heroL.appendChild(sub);
  hero.appendChild(heroL);
  // 색은 종목에 고정(아래 전략 도넛과 같은 색): 7자리를 내 보유 평가액 큰 순으로 먼저 채우고, 남는 자리를 전략 보유 합산 큰 순으로 채운다
  const myVal = new Map(cur.holdings.map((x) => { const c = close(x.ticker); return [x.ticker, c == null ? 0 : x.qty * c]; }));
  const simW = new Map();
  for (const sc of model.result?.scenarios || []) if (sc.started) for (const t of Object.keys(sc.holdings)) { const c = close(t); simW.set(t, (simW.get(t) || 0) + (c == null ? 0 : sc.holdings[t] * c)); }
  const byVal = (m) => [...m.entries()].filter(([, v]) => v > 0).sort((a, b) => b[1] - a[1]).map(([t]) => t);   // 가격 없는 종목은 색 자리를 받지 않는다
  const named = [...new Set([...byVal(myVal), ...byVal(simW)])].slice(0, SLOTS).sort();
  const hasOther = new Set([...myVal.keys(), ...simW.keys()]).size > SLOTS;
  const color = (t) => (t === '현금' ? 'var(--pf-cash)' : named.includes(t) ? `var(--pf-k${named.indexOf(t) + 1})` : 'var(--pf-other)');
  const mine = new Map();
  for (const x of cur.holdings) { const v = myVal.get(x.ticker); if (!v) continue; const k = named.includes(x.ticker) ? x.ticker : '기타'; mine.set(k, (mine.get(k) || 0) + v); }
  // 조각 순서: 평가액 큰 순, 기타·현금은 끝
  const myParts = [...mine.entries()].filter(([t, v]) => v > 0 && t !== '기타').sort((a, b) => b[1] - a[1]);
  if (mine.get('기타') > 0) myParts.push(['기타', mine.get('기타')]);
  if (cur.hasCash && cur.cash > 0) myParts.push(['현금', cur.cash]);
  const myTot = myParts.reduce((a, [, v]) => a + v, 0);
  const share = (v, tot) => { const p = (v / tot) * 100; return p > 0 && p < 1 ? '<1%' : Math.round(p) + '%'; };
  left.appendChild(hero);
  if (myTot > 0) {
    // 비중 막대 한 줄 + 범례 한 줄(종목 목록은 아래에서 접고 편다)
    const bar = el('div', 'pf-mix'); bar.setAttribute('role', 'img');
    bar.setAttribute('aria-label', '보유 비중: ' + myParts.map(([t, v]) => `${t} ${share(v, myTot)}`).join(', '));
    const leg = el('ul', 'pf-legend pf-mixleg');
    for (const [t, v] of myParts) {
      const p = share(v, myTot);
      const seg = el('i'); seg.style.flexGrow = String(v); seg.style.background = color(t === '기타' ? '__other' : t);
      seg.title = `${t} ${p} · ${usd0(v)}`; bar.appendChild(seg);
      const li = el('li'); const sw = el('i'); sw.style.background = seg.style.background; li.appendChild(sw); li.appendChild(el('span', null, `${t} ${p}`)); leg.appendChild(li);
    }
    left.appendChild(bar); left.appendChild(leg);
  }
  const fold = el('details', 'pf-holdfold');
  try { fold.open = sessionStorage.getItem('pf-holds-open') === '1'; } catch (_) { /* 기억 못 해도 접힌 채로 */ }
  fold.addEventListener('toggle', () => { try { sessionStorage.setItem('pf-holds-open', fold.open ? '1' : '0'); } catch (_) { /* 무시 */ } });
  fold.appendChild(el('summary', null, `보유 종목 보기 (${cur.holdings.length})`));
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
    row.appendChild(nm);
    row.appendChild(el('span', 'pf-chip ' + (TIER_CLS[tier] || 'pf-t-none'), tier || '카드 없음'));
    row.appendChild(el('b', null, c == null ? '가격 없음' : usd0(x.qty * c)));
    (more || list).appendChild(row);
  });
  fold.appendChild(list);
  if (cur.holdings.length) left.appendChild(fold);
  if (cur.hasCash && cur.cash < 0) left.appendChild(el('p', 'pf-warn', `⚠ 현금이 ${usd0(cur.cash)}입니다. 빠진 입금이나 잘못 적은 매수가 없는지 확인하세요(막대는 현금을 빼고 그립니다).`));
  if (cur.clipped.length) left.appendChild(el('p', 'pf-warn', `⚠ 보유보다 많이 판 기록 ${cur.clipped.length}건(${cur.clipped.map((c) => c.ticker + ' ' + shares(c.short) + '주').join(', ')})은 가진 만큼만 반영했습니다. 올린 보유나 빠진 매수 기록을 확인하세요.`));
  if (h.asOf) left.appendChild(el('p', 'pf-note', `올린 보유 ${h.asOf} + 그 뒤 기록한 매매 ${cur.applied.length}건` + (depIn.length ? ` + 입금 ${depIn.length}건(오늘 반영분 포함)` : '')
    + (cur.future.length ? ` (미래 날짜 ${cur.future.length}건은 그날부터)` : '')));
  top.appendChild(left);
  top.appendChild(tradeForm(model, handlers, recs, mv, today));
  root.appendChild(top);

  // 2) 이번 달 할 일(가로 한 줄)
  const tsec = el('section', 'pf-panel pf-todosec');
  const head = el('div', 'pf-todohead');
  const ht = el('div'); ht.appendChild(el('div', 'pf-eyebrow', 'THIS MONTH')); ht.appendChild(el('h2', 'pf-h2', '이번 달 할 일'));
  head.appendChild(ht);
  const right = el('div', 'pf-todos');
  const todo = (a, b) => { const d = el('div', 'pf-todo'); d.appendChild(el('span', null, a)); d.appendChild(el('b', null, b)); right.appendChild(d); };
  todo('다음 회차', !mv ? '시나리오 없음' : mv.stale ? '이번 달 결정 대기' : mv.next ? md(mv.next.date) : '다음 달 1일 점검');
  todo('매도 검토 알림', mv && mv.plan && !mv.stale ? `${mv.alerts.length}건${mv.alerts.length ? ' ⚠' : ''}` : '—');
  // 이번 달(미국 동부) 기록한 입금 중 효력 있는 취소(반영일 09:30 ET 전)를 뺀 것 — 엔진·기록·관리 탭과 같은 기준
  const month = today.slice(0, 7);
  const allDeps = Object.entries(model.bundle?.deposits || {});
  const gone = new Set(allDeps.filter(([, c]) => c.cancels).filter(([, c]) => {
    const dep = model.bundle.deposits[c.cancels]; if (!dep || dep.cancels) return false;
    const t = depositTiming(dep.recordedAt); return t.day && Date.parse(c.recordedAt) < t.cancelBefore;
  }).map(([, c]) => c.cancels));
  const deps = allDeps.filter(([id, d]) => !d.cancels && !gone.has(id) && d.recordedAt && etDate(Date.parse(d.recordedAt)).slice(0, 7) === month).map(([, d]) => d);
  todo('이번 달 입금', deps.length ? usd0(deps.reduce((a, d) => a + d.amount, 0)) + ' 기록' : '아직 없음');
  todo('마지막 기록', last ? md(last.session) : '없음');
  const go = el('button', 'pf-btn pf-btn-quiet', '＋ 입금 기록'); go.type = 'button';
  go.addEventListener('click', () => handlers.goto('manage'));
  head.appendChild(go);
  tsec.appendChild(head);
  tsec.appendChild(right);
  root.appendChild(tsec);

  // 3) 이번 달 운용
  root.appendChild(monthPanel(mv, model, lastFull, handlers));
  // 4) 전략 비교 도넛
  root.appendChild(donutPanel(model, lastFull, close, handlers, color, named, hasOther));
  root.appendChild(el('p', 'pf-notice', '모의 운용입니다. 판정은 수익 예측이 검증된 신호가 아닙니다. 카드 목록은 직접 고른 종목이라 결과를 일반화할 수 없습니다. 배당·세금·환율·큰 사건 예외 제외.'));
}

function tradeForm(model, handlers, recs, mv, today) {
  const box = el('div', 'pf-tradebox');
  box.appendChild(el('div', 'pf-eyebrow', 'MY TRADES'));
  box.appendChild(el('h2', 'pf-h2', '실제 매매 기록'));
  box.appendChild(el('p', 'pf-note', '실제로 사고판 것을 적으면 내 자산의 보유 수량·평균 단가·현금에 바로 반영되고, 전략 비교의 "내 실제 계좌" 줄에도 들어갑니다(시작일 뒤 날짜, 그날 일별 기록이 나온 뒤부터). 잘못 적었으면 기록·관리 탭에서 고치거나 지웁니다.'));
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
  }, f);
  box.appendChild(f);
  return box;
}

function monthPanel(mv, model, last, handlers) {
  const sec = el('section', 'pf-panel');
  if (!mv || !mv.plan) {
    sec.appendChild(el('div', 'pf-eyebrow', 'THIS MONTH'));
    sec.appendChild(el('h2', 'pf-h2', '이번 달 운용'));
    sec.appendChild(el('p', 'pf-note', !model.bundle || model.bundle.closed
      ? '전략 비교를 시작하면(기록·관리 탭의 시작 스냅샷) 매달 점검일 결정과 회차 진행이 여기에 보입니다.'
      : !mv ? '원칙 계산이 아직 출발하지 못했습니다. 시작 스냅샷의 종목에 모두 그날 가격이 있어야 출발합니다(전략 비교 탭의 출발 대기 이유를 보세요).'
        : '첫 점검일(매달 1일, 휴장이면 다음 거래일)을 기다리는 중입니다.'));
    if (!model.bundle || model.bundle.closed || !mv) {
      const b = el('button', 'pf-btn pf-btn-quiet', '기록·관리로'); b.type = 'button'; b.addEventListener('click', () => handlers.goto('manage')); sec.appendChild(b);
    }
    return sec;
  }
  const { plan, scenario } = mv;
  sec.appendChild(el('div', 'pf-eyebrow', `${md(plan.decisionDate)} 점검일 결정 · ${label(scenario, model.byId)}`));
  const h = el('h2', 'pf-h2', mv.stale ? '지난달 계획 ' : '이번 달 운용 ');
  h.appendChild(el('small', null, `매달 1일 정하고 ${plan.rounds.length}번에 나눠 삽니다` + (scenario.id === '__plan' ? ' · 원칙 기준(유보 0%, 매도는 알림만)' : '')));
  sec.appendChild(h);
  const steps = el('ol', 'pf-steps');
  for (const s of mv.steps) {
    const li = el('li', 'pf-step pf-step-' + s.state);
    li.appendChild(el('i', null, { done: '✓', partial: '!', skip: '!', carry: '→', dropped: '–', todo: '' }[s.state]));
    li.appendChild(el('span', null, s.label));
    li.appendChild(el('small', null, md(s.date) + ({ partial: ' 일부 건너뜀', skip: ' 건너뜀', carry: ' 다음으로', dropped: ' 버림' }[s.state] || '')));
    steps.appendChild(li);
  }
  sec.appendChild(steps);
  if (mv.stale) sec.appendChild(el('p', 'pf-warn', '이번 달 점검일 결정이 아직 없습니다(정보 없음이면 다음 거래일로 미룸). 아래는 지난달 계획입니다.'));
  if (plan.ruleChanged) sec.appendChild(el('p', 'pf-note', '이번 달은 판정 방식이 바뀌어 매매하지 않습니다(바뀐 판정으로 매도가 생기지 않게).'));
  sec.appendChild(el('h3', 'pf-h3', `살 후보 ${plan.candidates.length}종목`));
  const cards = el('div', 'pf-cands');
  const real = Object.values(model.trades || {});
  const cancelled = new Set(real.filter((x) => x.cancels).map((x) => x.cancels));
  const realBuys = Object.entries(model.trades || {}).filter(([id, x]) => !x.cancels && !cancelled.has(id) && x.side === 'buy' && x.date >= plan.decisionDate && x.date.slice(0, 7) === plan.decisionDate.slice(0, 7)).map(([, x]) => x);
  for (const t of plan.candidates) {
    const c = el('div', 'pf-cand');
    const head = el('div'); head.appendChild(el('b', null, t + ' '));
    const tier = last?.cards?.[t]?.tier; head.appendChild(el('span', 'pf-chip ' + (TIER_CLS[tier] || 'pf-t-none'), tier || '—'));
    c.appendChild(head);
    const sim = scenario.trades.filter((x) => x.ticker === t && x.side === 'buy' && x.date >= plan.decisionDate).reduce((a, x) => a + x.amount, 0);
    c.appendChild(el('div', 'pf-note', `원칙 기준 ${usd0(sim)} 매수`));
    const mine = realBuys.filter((x) => x.ticker === t);
    const q = mine.reduce((a, x) => a + x.qty, 0);
    c.appendChild(el('div', 'pf-cand-real', mine.length ? `실제로 ${shares(q)}주 삼` : '실제 매수 기록 없음'));
    cards.appendChild(c);
  }
  if (!plan.candidates.length) cards.appendChild(el('p', 'pf-note', '이번 달 살 후보가 없습니다(조건에 맞는 판정 없음).'));
  sec.appendChild(cards);
  if (plan.budget > 0) {
    sec.appendChild(el('div', 'pf-note', '이번 달 예산 사용(원칙 기준 모의)'));
    const bar = el('div', 'pf-bar'), fill = el('span'); fill.style.width = Math.min(100, (mv.spent / plan.budget) * 100) + '%'; bar.appendChild(fill);
    sec.appendChild(bar);
    sec.appendChild(el('p', 'pf-note', `${usd0(mv.spent)} / ${usd0(plan.budget)}`));
  }
  const al = el('div', 'pf-alerts');
  for (const f of mv.alerts) al.appendChild(el('p', null, `⚠ ${f.ticker} ${f.observed} — 매도 검토` + (f.warnOnly ? '(원칙 2 비율 미정이라 알림만)' : ` · ${shares(f.shares)}주 나눠 매도`)));
  if (!mv.alerts.length) al.appendChild(el('p', 'pf-note', '매도 검토 알림 없음'));
  sec.appendChild(al);
  return sec;
}

const HOLD_SHOWN = 10;   // 펼친 보유 목록에 바로 보이는 종목 수
const SLOTS = 7;   // 종목 색 7개(검증된 팔레트) + 현금 회색. 8번째 종목부터는 '기타'로 묶는다
function donutPanel(model, last, close, handlers, color, named, hasOther) {
  const sec = el('section', 'pf-panel');
  sec.appendChild(el('div', 'pf-eyebrow', 'STRATEGY CHECK'));
  const r = model.result;
  const A = r?.scenarios?.find((s) => s.id === 'A');
  const h = el('h2', 'pf-h2', '전략 비교 ');
  if (A?.started) h.appendChild(el('small', null, `${md(A.started)} 시작 · ${A.days.filter((d) => d.date >= A.started).length - 1}거래일`));
  sec.appendChild(h);
  if (!r) {
    sec.appendChild(el('p', 'pf-note', '전략 비교를 시작하면 전략마다 지금 들고 있는 종목과 수익률이 여기에 보입니다.'));
    return sec;
  }
  sec.appendChild(el('p', 'pf-note', '모든 전략이 시작일의 같은 보유로 출발합니다(카드의 출발일). 도넛은 각 전략이 지금 들고 있는 종목과 현금의 비중, 가운데 숫자는 자기 출발일 뒤 수익률(TWR)이라 출발일이 다르면 기간도 다릅니다.'));
  const started = r.scenarios.filter((s) => s.started);
  const val = (s, t) => { const c = close(t); return c == null ? null : s.holdings[t] * c; };
  const held = new Set(started.flatMap((s) => Object.keys(s.holdings)));
  const leg = el('ul', 'pf-legend');
  for (const t of [...named.filter((x) => held.has(x)), ...(hasOther ? ['기타'] : []), '현금']) {
    const li = el('li'); const i = el('i'); i.style.background = color(t === '기타' ? '__other' : t); li.appendChild(i); li.appendChild(el('span', null, t)); leg.appendChild(li);
  }
  sec.appendChild(leg);
  const grid = el('div', 'pf-scards');
  const tip = el('div', 'pf-tip'); tip.hidden = true;
  for (const s of r.scenarios) {
    const card = el('div', 'pf-sc');
    card.appendChild(el('div', 'pf-sc-name', label(s, model.byId)));
    card.appendChild(el('div', 'pf-sc-kind', (s.id === 'A' ? '입금만 비중대로 적립' : STRATEGY[s.strategy] || '') + (s.started ? ` · ${md(s.started)} 출발` : '')));
    if (!s.started) {
      card.appendChild(el('p', 'pf-note', waitText(s)));
      for (const w of s.warnings || []) card.appendChild(el('p', 'pf-warn', '⚠ ' + w));
      grid.appendChild(card); continue;
    }
    const groups = new Map();
    let unknown = false;
    for (const t of Object.keys(s.holdings)) {
      const v = val(s, t); if (v == null) { unknown = true; continue; }
      const k = named.includes(t) ? t : '기타'; groups.set(k, (groups.get(k) || 0) + v);
    }
    // 조각 순서는 내 자산 막대와 같게: 평가액 큰 순, 기타·현금은 끝
    const parts = [...groups.entries()].filter(([t, v]) => v > 0 && t !== '기타').sort((a, b) => b[1] - a[1]);
    if (groups.get('기타') > 0) parts.push(['기타', groups.get('기타')]);
    if (s.cash > 0) parts.push(['현금', s.cash]);
    const tot = parts.reduce((a, [, v]) => a + v, 0);
    const last1 = [...s.days].reverse().find((d) => d.date >= s.started) || {};
    // 엔진이 마지막 날 평가를 못 했으면(분할 확인·가격 없음 등) 비중도 확정값처럼 보이지 않게 가운데를 '미확정'으로
    const unvalued = s.halted || last1.value == null;
    card.appendChild(donut(parts, tot, color, s.halted ? { v: '평가 불가', l: '수익률' } : last1.value == null ? { v: '미확정', l: '마지막 날 평가 없음' }
      : { v: pct(last1.twr), l: '수익률', cls: last1.twr == null ? '' : last1.twr >= 0 ? 'pf-up' : 'pf-down' }, tip));
    const top3 = parts.slice().sort((a, b) => b[1] - a[1]).slice(0, 3).map(([t, v]) => `${t} ${Math.round((v / tot) * 100)}%`).join(' · ');
    card.appendChild(el('div', 'pf-note pf-sc-top', top3 + (unknown ? ' · 가격 없는 종목 뺌' : '') + (unvalued ? ' · 참고용(평가 미확정)' : '')));
    const rows = el('div', 'pf-sc-rows');
    const row = (a, b) => { const d = el('div'); d.appendChild(el('span', null, a)); d.appendChild(el('b', null, b)); rows.appendChild(d); };
    row('평가액', last1.value == null ? '미확정' : usd0(last1.value));
    row('SPY 대비', pp(last1.vs ? last1.vs.SPY : null));
    row('체결 · 건너뜀', `${s.trades.length} · ${s.skips.filter((x) => x.action !== 'carried').length}`);
    card.appendChild(rows);
    if (s.halted) card.appendChild(el('p', 'pf-warn', `${s.halted.since}부터 평가 불가(${REASON[s.halted.reason] || s.halted.reason})`));
    for (const w of s.warnings || []) card.appendChild(el('p', 'pf-warn', '⚠ ' + w));   // 내 실제 계좌: 보유 초과 매도·음수 현금
    grid.appendChild(card);
  }
  sec.appendChild(grid);
  sec.appendChild(tip);
  const more = el('button', 'pf-btn pf-btn-quiet', '그래프·매매 기록 보기'); more.type = 'button';
  more.addEventListener('click', () => handlers.goto('strategy'));
  sec.appendChild(more);
  return sec;
}

const SVG = 'http://www.w3.org/2000/svg';
function donut(parts, tot, color, center, tip) {
  const svg = document.createElementNS(SVG, 'svg');
  svg.setAttribute('viewBox', '0 0 150 150'); svg.setAttribute('class', 'pf-donut');
  svg.setAttribute('role', 'img');
  svg.setAttribute('aria-label', '보유 구성: ' + parts.map(([t, v]) => `${t} ${Math.round((v / tot) * 100)}%`).join(', '));
  const P = (r, a) => [75 + r * Math.sin(a), 75 - r * Math.cos(a)];
  let a = 0;
  for (const [t, v] of parts) {
    const a0 = a, a1 = parts.length === 1 ? a + Math.PI * 2 - 1e-4 : a + (v / tot) * Math.PI * 2; a = a1;
    const big = a1 - a0 > Math.PI ? 1 : 0, [x0, y0] = P(72, a0), [x1, y1] = P(72, a1), [x2, y2] = P(46, a1), [x3, y3] = P(46, a0);
    const path = document.createElementNS(SVG, 'path');
    path.setAttribute('d', `M${x0} ${y0}A72 72 0 ${big} 1 ${x1} ${y1}L${x2} ${y2}A46 46 0 ${big} 0 ${x3} ${y3}Z`);
    path.setAttribute('fill', color(t === '기타' ? '__other' : t));
    const text = `${t} ${Math.round((v / tot) * 100)}% · ${usd0(v)}`;
    path.addEventListener('pointermove', (e) => {
      tip.textContent = text; tip.hidden = false;
      const box = tip.parentElement.getBoundingClientRect();
      tip.style.left = Math.max(0, Math.min(e.clientX - box.left + 12, box.width - tip.offsetWidth - 4)) + 'px'; tip.style.top = e.clientY - box.top + 12 + 'px';
    });
    path.addEventListener('pointerleave', () => { tip.hidden = true; });
    svg.appendChild(path);
  }
  const t1 = document.createElementNS(SVG, 'text');
  t1.setAttribute('x', 75); t1.setAttribute('y', 78); t1.setAttribute('text-anchor', 'middle');
  t1.setAttribute('class', 'pf-donut-v ' + (center.cls || ''));
  t1.textContent = center.v;
  const t2 = document.createElementNS(SVG, 'text');
  t2.setAttribute('x', 75); t2.setAttribute('y', 96); t2.setAttribute('text-anchor', 'middle'); t2.setAttribute('class', 'pf-donut-l');
  t2.textContent = center.l;
  svg.appendChild(t1); svg.appendChild(t2);
  return svg;
}

// 기록·관리 탭의 실제 매매 기록 목록(취소 포함)
export function tradeList(model, handlers) {
  const sec = el('div', 'pf-st-block');
  sec.appendChild(el('h3', null, '실제 매매 기록'));
  const h = model.main?.holdings || {};
  const cur = currentHoldings(h.rows, h.asOf, model.trades, etDate(model.now ?? Date.now()));
  const all = Object.entries(model.trades || {});
  const cancelled = new Set(all.filter(([, x]) => x.cancels).map(([, x]) => x.cancels));
  const skipped = new Set(cur.skipped.map((x) => x.id)), future = new Set(cur.future.map((x) => x.id));
  const clipped = new Map(cur.clipped.map((c) => [c.id, c.short]));
  const msg = msgLine();
  const edit = el('div', 'pf-edit'); edit.hidden = true;
  const openEdit = (id, x) => {
    edit.textContent = ''; edit.hidden = false;
    edit.appendChild(el('p', 'pf-note', `${x.date} ${x.ticker} 기록 고치기`));
    const f = el('div', 'pf-form pf-tradeform');
    const field = (lab, input) => { const l = el('label', 'pf-field'); l.appendChild(el('span', null, lab)); l.appendChild(input); f.appendChild(l); return input; };
    const d = field('날짜(체결일, 미국 동부)', el('input')); d.type = 'date'; d.value = x.date;
    const sd = field('매매', el('select'));
    for (const [v, t] of [['buy', '매수'], ['sell', '매도']]) { const o = el('option', null, t); o.value = v; sd.appendChild(o); }
    sd.value = x.side;
    const tk = field('종목(티커)', el('input')); tk.value = x.ticker; tk.className = 'pf-ticker';
    const q = field('수량', el('input')); q.type = 'number'; q.step = 'any'; q.value = String(x.qty);
    const pr = field('체결가(USD)', el('input')); pr.type = 'number'; pr.step = '0.0001'; pr.value = String(x.price);
    const save = el('button', 'pf-btn', '저장'); save.type = 'button';
    const close = el('button', 'pf-btn pf-btn-quiet', '닫기'); close.type = 'button'; close.addEventListener('click', () => { edit.hidden = true; });
    const em = msgLine();
    f.appendChild(save); f.appendChild(close); f.appendChild(em);
    edit.appendChild(f);
    twoStep(save, em, '이대로 고칩니다. 맞으면 한 번 더 누르세요.', async () => {
      const y = { date: d.value, ticker: tk.value.trim().toUpperCase(), side: sd.value, qty: Number(q.value), price: Number(pr.value) };
      const bad = checkTrade(y, etDate(Date.now()));
      if (bad) throw new Error(bad);
      await handlers.editTrade(id, y);
    }, f);
  };
  const rows = all.filter(([, x]) => !x.cancels).sort(([, a], [, b]) => (a.date < b.date ? 1 : -1)).map(([id, x]) => {
    let state = '반영';
    if (cancelled.has(id)) state = '취소됨';   // 예전 취소 기록(덧붙이기만 시절)
    else if (skipped.has(id)) state = '기준일 전(반영 안 함)';
    else if (future.has(id)) state = '미래 날짜(그날부터 반영)';
    else if (clipped.has(id)) state = `보유 초과 — ${shares(x.qty - clipped.get(id))}주만 반영`;
    const acts = el('div', 'pf-acts');
    const fix = el('button', 'pf-btn pf-btn-quiet', '고치기'); fix.type = 'button'; fix.addEventListener('click', () => openEdit(id, x));
    const del = el('button', 'pf-btn pf-btn-quiet', '지우기'); del.type = 'button';
    twoStep(del, msg, '이 기록을 지웁니다. 맞으면 지우기를 한 번 더 누르세요.', () => handlers.deleteTrade(id));
    acts.appendChild(fix); acts.appendChild(del);
    return [x.date, x.ticker, x.side === 'buy' ? '매수' : '매도', shares(x.qty), usd(x.price), usd(x.qty * x.price), state, acts];
  });
  sec.appendChild(table(['날짜', '종목', '매매', '수량', '체결가', '금액', '상태', ''], rows, [3, 4, 5], true));
  sec.appendChild(msg);
  sec.appendChild(edit);
  sec.appendChild(el('p', 'pf-note', '기록은 언제든 고치거나 지울 수 있습니다. 올린 보유의 기준일과 그 전 날짜의 매매는 이미 올린 보유에 들어 있다고 보고 반영하지 않습니다.'));
  return sec;
}

// 세 하위 탭(한눈에·전략 비교·기록·관리)을 한 번에 그린다. preview-only-portfolio.js와 화면 시험 페이지가 같이 쓴다.
// model = renderHome과 같음, smodel = { bundle, bundleNo, closedCount, records, recordsError, calcError, holdingsRows }
export function renderTabs(roots, model, smodel, handlers) {
  renderHome(roots.home, model, handlers);
  const st = roots.strategy, { result } = model, recs = smodel.records || [];
  st.textContent = '';
  st.appendChild(el('p', 'pf-note pf-fixed', FIXED_NOTICE));
  const lastRec = recs.length ? recs[recs.length - 1].session : null;
  if (smodel.recordsError) st.appendChild(el('p', 'pf-warn', '일별 기록을 불러오지 못했습니다. 새로고침해 보세요.'));
  else if (smodel.calcError) st.appendChild(el('p', 'pf-warn', '계산하지 못했습니다: ' + smodel.calcError));
  else if (!result) st.appendChild(el('p', 'pf-note', '전략 비교를 시작하면(기록·관리 탭의 시작 스냅샷) 여기에 비교 표·그래프·매매 기록이 보입니다.'));
  else {
    st.appendChild(el('p', 'pf-note', `큰 사건 예외를 뺀 정기 운용 모형 · 엔진 ${ENGINE_VERSION} · 마지막 기록 ${lastRec} · 빠진 날 ${result.missingSessions.length}일`));
    st.appendChild(compareSection(result, model.byId));
    st.appendChild(chartSection(result, model.byId));
    st.appendChild(detailSection(result, model.byId));
  }
  // 시작 폼 미리 채우기: 내 자산과 같은 계산으로 마지막 기록일까지(그 뒤 매매는 빼고)
  const hh = model.main?.holdings || {};
  const pc = currentHoldings(hh.rows, hh.asOf, model.trades, lastRec || etDate(model.now ?? Date.now()));
  smodel = { ...smodel, prefill: { asOf: hh.asOf || null, upTo: lastRec, holdings: pc.holdings, cash: pc.hasCash ? pc.cash : null, clipped: pc.clipped } };
  const mg = roots.manage;
  mg.textContent = '';
  mg.appendChild(tradeList(model, handlers));
  const b = smodel.bundle;
  if (!b || b.closed) mg.appendChild(startForm(smodel, handlers, lastRec));
  else {
    mg.appendChild(depositSection(b, handlers, model.now ?? Date.now()));
    mg.appendChild(scenarioForm(b, handlers));
    mg.appendChild(bundleSection(b, smodel, handlers));
  }
}
