// preview 전용 Portfolio 탭 — 기록·관리 하위 탭(2026-10-21 사용자 선택: 디자인 시안 "기록 A · 한 줄 타임라인"). 라이브로 옮기지 않는다 — pipeline/site_ui/UI_DIFF.md 1절 portfolio.
//
// 실제 매매·입금·시작 스냅샷·올린 보유를 날짜순 한 목록으로 보여 주고(종류별로 거를 수 있음), 줄마다 고치기·지우기를 둔다.
// "＋ 기록 추가"는 매매·입금 입력을 연다. 묶음 끝내기는 맨 아래에 접어 둔다. 저장은 handlers(trade·editTrade·deleteTrade·deposit·editDeposit·deleteDeposit·close).
// 한눈에 파일(-home.js)이 이 파일을 부르므로, 거기 있는 계산(currentHoldings·checkTrade·etDate)은 인자 h로 받는다(같은 모듈을 두 번 읽지 않게).
// 순수 함수 timelineItems는 node 시험이 부른다(pipeline/portfolio/test_strategy_view.mjs).
import { el, msgLine, twoStep, usd, shares, startForm } from './preview-only-portfolio-strategy.js?v=27';
import { depositTiming } from './preview-only-portfolio-engine.js?v=14';

// ---- 순수 함수 ----

// 입금 하나의 상태 글(엔진과 같은 기준: 취소는 반영일 09:30 ET 전에 기록된 것만 효력)
export function depositState(id, d, cancelAt, now) {
  const t = depositTiming(d.recordedAt);
  const cAt = cancelAt.has(id) ? Date.parse(cancelAt.get(id)) : null;
  if (cAt != null && t.day && cAt < t.cancelBefore) return '취소됨';
  return (t.day ? t.day + (now < t.cancelBefore ? ' 반영 예정' : ' 반영') : '반영일 계산 불가') + (cAt != null ? '(취소가 반영 뒤라 무시됨)' : '');
}

// 기록 → 목록 줄(최신이 위). cur = currentHoldings 결과(매매 상태), bundle = 지금 묶음(없거나 끝났으면 입금·스냅샷 없음)
// 줄: { kind: 'trade'|'deposit'|'snap'|'upload', id, date, title, detail, amount, raw } + 매매·입출금에는 state(상태 글)·value(부호 붙은 현금 흐름)
export function timelineItems({ trades, cur, bundle, bundleNo, holdings, now, etDate }) {
  const out = [];
  const all = Object.entries(trades || {});
  const cancelled = new Set(all.filter(([, x]) => x.cancels).map(([, x]) => x.cancels));
  const skipped = new Set(cur.skipped.map((x) => x.id)), future = new Set(cur.future.map((x) => x.id));
  const clipped = new Map(cur.clipped.map((c) => [c.id, c.short]));
  for (const [id, x] of all) {
    if (x.cancels) continue;
    let state = '반영';
    if (cancelled.has(id)) state = '취소됨';   // 예전 취소 기록(덧붙이기만 시절)
    else if (skipped.has(id)) state = '기준일 전(반영 안 함)';
    else if (future.has(id)) state = '미래 날짜(그날부터 반영)';
    else if (clipped.has(id)) state = `보유 초과 — ${shares(x.qty - clipped.get(id))}주만 반영`;
    const amt = x.qty * x.price;
    out.push({ kind: 'trade', id, date: x.date, title: `${x.ticker} ${x.side === 'buy' ? '매수' : '매도'} ${shares(x.qty)}주`,
      detail: `${usd(x.price)} · ${state}`, amount: (x.side === 'buy' ? '−' : '+') + usd(amt), raw: x, state, value: x.side === 'buy' ? -amt : amt });
  }
  if (bundle && !bundle.closed) {
    const deps = Object.entries(bundle.deposits || {});
    const cancelAt = new Map();
    for (const [, d] of deps) if (d.cancels && d.recordedAt && (!cancelAt.has(d.cancels) || d.recordedAt < cancelAt.get(d.cancels))) cancelAt.set(d.cancels, d.recordedAt);
    for (const [id, d] of deps) {
      if (d.cancels) continue;
      const rec = d.recordedAt ? etDate(Date.parse(d.recordedAt)) : null;
      const out_ = d.kind === 'withdraw';   // 출금(2026-10-22) — 같은 입금 지도에 kind:'withdraw'로 둔다
      const dst = depositState(id, d, cancelAt, now);
      out.push({ kind: 'deposit', id, date: rec || '', title: `${out_ ? '출금' : '입금'} ${usd(d.amount)}`,
        detail: `${rec ? rec + ' 기록' : '기록 중'}` + (d.forMonth && !out_ ? ` · ${+d.forMonth.slice(5)}월 몫(미리)` : '') + ` · ${dst}`, amount: (out_ ? '−' : '+') + usd(d.amount), raw: d, state: dst, value: out_ ? -d.amount : d.amount });
    }
    const s = bundle.snapshot || {};
    if (s.date) {
      const hs = Object.entries(s.holdings || {}).sort();
      const list = hs.slice(0, 6).map(([t, q]) => `${t} ${shares(q)}`).join(' · ') + (hs.length > 6 ? ` 외 ${hs.length - 6}종목` : '');
      out.push({ kind: 'snap', id: 'snap', date: s.date, title: `시작 스냅샷 (묶음 ${bundleNo})`,
        detail: `${list || '종목 없음'} · 현금 ${usd(s.cash)}` + ((s.holdOnly || []).length ? ` · 그대로 두는 보유 ${s.holdOnly.join(', ')}` : ''), amount: '', raw: s });
    }
  }
  const asOf = holdings?.asOf || '';
  if (/^\d{4}-\d{2}-\d{2}/.test(asOf)) {
    const n = (holdings.rows || []).filter((r) => String(r.ticker || '').trim()).length;
    const cash = (holdings.rows || []).some((r) => !String(r.ticker || '').trim());
    out.push({ kind: 'upload', id: 'upload', date: asOf.slice(0, 10), title: '보유 올림', detail: `${asOf} · ${n}종목${cash ? ' + 현금' : ''}`, amount: '', raw: null });
  }
  const order = { trade: 0, deposit: 1, snap: 2, upload: 3 };
  return out.sort((a, b) => (a.date !== b.date ? (a.date < b.date ? 1 : -1) : order[a.kind] - order[b.kind]));
}

// 날짜별 묶음(2026-11-20 정리, 최신이 위 — items 순서를 그대로 따른다). 한 날짜의 매매·입출금은 한 카드(moves), 시작 스냅샷·올린 보유는 따로(base).
// 취소된 기록은 줄에는 남기되 건수·합계에서 뺀다. tradeNet·cashNet = 부호 붙은 합(산 돈은 −).
export function dayGroups(items) {
  const out = [];
  for (const it of items) {
    let g = out.at(-1);
    if (!g || g.date !== it.date) { g = { date: it.date, moves: [], base: [], buys: 0, sells: 0, deps: 0, outs: 0, tradeNet: 0, cashNet: 0 }; out.push(g); }
    if (it.kind === 'snap' || it.kind === 'upload') { g.base.push(it); continue; }
    g.moves.push(it);
    if (it.state === '취소됨') continue;
    if (it.kind === 'trade') { if (it.value < 0) g.buys++; else g.sells++; g.tradeNet += it.value; }
    else { if (it.value < 0) g.outs++; else g.deps++; g.cashNet += it.value; }
  }
  return out;
}

// 맨 위 요약 숫자. today = 미국 동부 날짜(YYYY-MM-DD). 마지막 매매·이번 달 산 돈은 취소된 기록을 빼고, 쌓인 기록 건수는 목록·보기 단추와 같게 취소된 줄도 센다.
// { last: { date, buys, sells } | null, monthBuy, monthBuys, total, trades, deposits, base, snap: 줄 | null }
export function recSummary(items, today) {
  const live = items.filter((x) => x.kind === 'trade' && x.state !== '취소됨');
  const lastDate = live.map((x) => x.date).sort().at(-1) || null;
  const on = live.filter((x) => x.date === lastDate);
  const mb = live.filter((x) => x.value < 0 && x.date.slice(0, 7) === today.slice(0, 7) && x.date <= today);   // 미래 날짜로 적은 매수는 아직 산 돈이 아니다
  return {
    last: lastDate ? { date: lastDate, buys: on.filter((x) => x.value < 0).length, sells: on.filter((x) => x.value > 0).length } : null,
    monthBuy: mb.reduce((a, x) => a - x.value, 0), monthBuys: mb.length,
    total: items.length, trades: items.filter((x) => x.kind === 'trade').length, deposits: items.filter((x) => x.kind === 'deposit').length,
    base: items.filter((x) => x.kind === 'snap' || x.kind === 'upload').length,
    snap: items.find((x) => x.kind === 'snap') || null,
  };
}

// '2026-11-09' → '11월 9일'(올해가 아니면 연도를 앞에). 날짜가 없으면 '날짜 없음'
export const kdate = (d, today) => (!/^\d{4}-\d{2}-\d{2}/.test(d || '') ? '날짜 없음' : (d.slice(0, 4) !== (today || '').slice(0, 4) ? `${d.slice(0, 4)}년 ` : '') + `${+d.slice(5, 7)}월 ${+d.slice(8, 10)}일`);

// ---- 그리기 ----

const FILTER = { all: ['전체', () => true], trade: ['매매', (x) => x.kind === 'trade'], deposit: ['입출금', (x) => x.kind === 'deposit'], base: ['시작·보유', (x) => x.kind === 'snap' || x.kind === 'upload'] };
const VIEW_KEY = 'pf-rec-view';
const view = (() => { try { return { filter: 'all', open: null, ...JSON.parse(sessionStorage.getItem(VIEW_KEY) || '{}') }; } catch (_) { return { filter: 'all', open: null }; } })();
const keep = () => { try { sessionStorage.setItem(VIEW_KEY, JSON.stringify(view)); } catch (_) { /* 기억 못 해도 화면은 그대로 */ } };
const btn = (text, cls) => { const b = el('button', cls || 'pf-btn pf-btn-quiet', text); b.type = 'button'; return b; };
const signed = (v) => (v < 0 ? '−' : '+') + usd(Math.abs(v));
// 폰에서는 큰 버튼을 기록 목록 아래에 둔다(2026-11-19 사용자 결정) — 폭이 경계를 넘으면 다시 그린다
const PHONE = typeof window !== 'undefined' && window.matchMedia ? window.matchMedia('(max-width:760px)') : null;
let place = null;   // 지금 그려진 화면의 큰 버튼·기록 목록 자리를 폭에 맞게 놓는다(다시 그리지 않고 옮기기만 — 쓰던 양식의 입력을 지우지 않는다)
PHONE?.addEventListener?.('change', () => place?.());

// mg = #pf-manage, h = { currentHoldings, checkTrade, etDate, acctName } (-home.js에서 넘긴다)
// 2026-11-20 정리(디자인 시안 Records): 위에 요약 숫자 네 칸, 큰 버튼(입금·출금, 보유 파일, 시작 스냅샷, 올린 보유 표, 메모), 그 아래
// "자산이 쌓인 기록"을 날짜별 카드로(매매·입출금은 칸, 시작 스냅샷·올린 보유는 따로), 맨 아래 계산 방식·고급 관리 접기.
// 파일 올리기·올린 보유 표·메모는 html의 #pf-static에 있는 요소를 옮겨 쓴다(preview-only-portfolio.js가 id로 채우고 이벤트를 단다).
let latest = null;
export function renderManage(mg, model, smodel, handlers, h) {
  latest = [mg, model, smodel, handlers, h];
  const draw = () => renderManage(...latest);   // 저장 뒤 늦게 부르는 닫기도 새로 받은 값으로 그린다
  // 옮겨 쓰는 고정 요소는 지우기 전에 잡아 둔다
  const upWrap = document.getElementById('pf-upwrap'), holdWrap = document.getElementById('pf-holdwrap'), memo = document.getElementById('pf-scenarios');
  // 파일을 고른 뒤 확인을 기다리는 중이면 올리기 칸을 열어 둔다(지우기 전에 본다 — 지운 뒤엔 문서에서 찾을 수 없다)
  const pendingUpload = !!upWrap && upWrap.querySelector('#pf-upload-confirm')?.hidden === false;
  mg.textContent = '';
  const b = smodel.bundle && !smodel.bundle.closed ? smodel.bundle : null;
  const lastRec = (smodel.records || []).at(-1)?.session || null;
  if (!b) { const s = el('section', 'pf-panel'); s.appendChild(startForm(smodel, handlers, lastRec)); mg.appendChild(s); }
  const now = model.now ?? Date.now(), today = h.etDate(now);
  const hold = model.main?.holdings || {};
  const cur = h.currentHoldings(hold.rows, hold.asOf, model.trades, today);
  const items = timelineItems({ trades: model.trades, cur, bundle: b, bundleNo: smodel.bundleNo, holdings: hold, now, etDate: h.etDate });
  const sum = recSummary(items, today);
  const nHold = (hold.rows || []).filter((r) => String(r.ticker || '').trim()).length;

  // 요약 숫자 네 칸
  const top = el('section', 'pf-panel pf-r2top');
  const stat = (k, big, sub) => { const d = el('div', 'pf-r2stat'); d.appendChild(el('span', 'pf-ac2k', k)); d.appendChild(el('strong', 'pf-ac2big', big)); d.appendChild(el('span', 'pf-s', sub)); top.appendChild(d); };
  stat('마지막 매매 기록', sum.last ? kdate(sum.last.date, today) : '—',
    sum.last ? [sum.last.buys && `매수 ${sum.last.buys}건`, sum.last.sells && `매도 ${sum.last.sells}건`].filter(Boolean).join(' · ') : '아직 없음');
  stat('이번 달 산 돈', usd(sum.monthBuy), sum.monthBuys ? `매수 ${sum.monthBuys}건` : '매수 없음');
  stat('쌓인 기록', `${sum.total}건`, [sum.trades && `매매 ${sum.trades}`, sum.deposits && `입출금 ${sum.deposits}`, sum.base && `시작·보유 ${sum.base}`].filter(Boolean).join(' · ') || '아직 없음');
  const s0 = b?.snapshot || {};
  stat('비교 시작', b && s0.date ? kdate(s0.date, today) : '—', b && s0.date ? `묶음 ${smodel.bundleNo} · ${Object.keys(s0.holdings || {}).length}종목 + 현금` : '아직 시작 전');

  // 큰 버튼: 누르면 바로 아래에 그 칸이 열린다
  const acts = el('section', 'pf-r2actwrap');
  const actGrid = el('div', 'pf-r2acts'); acts.appendChild(actGrid);
  const area = el('div', 'pf-panel pf-r2area'); area.id = 'pf-r2area'; area.hidden = true; acts.appendChild(area);
  if (pendingUpload) view.open = 'upload';
  const act = (key, verb, name, sub, body) => {
    const open = view.open === key;
    const b2 = btn(null, 'pf-r2act'); b2.setAttribute('aria-expanded', String(open)); b2.setAttribute('aria-controls', 'pf-r2area');
    b2.appendChild(el('span', 'pf-r2verb', verb)); b2.appendChild(el('strong', null, name)); b2.appendChild(el('span', 'pf-s', sub));
    b2.dataset.key = key;
    b2.addEventListener('click', () => { view.open = open ? null : key; keep(); draw(); latest[0].querySelector(`.pf-r2act[data-key="${key}"]`)?.focus?.(); });
    actGrid.appendChild(b2);
    if (open) { area.hidden = false; area.appendChild(el('h3', 'pf-r2h3', `${name} ${verb}`)); body(area); }
  };
  if (b) act('deposit', '추가', '입금·출금', '모든 전략에 같이 반영', (a) => {
    a.appendChild(el('p', 'pf-note', '기록한 뒤 처음 오는 장 시작부터 반영합니다. 출금은 현금에서만 뺍니다.'));
    depositForm(a, handlers);
  });
  act('upload', '올리기', '보유 파일', 'CSV · Excel · JSON', (a) => {
    a.appendChild(el('p', 'pf-note', 'JSON은 원칙·올린 보유·관심 종목을 통째로, CSV·Excel은 올린 보유만 바꿉니다(Robinhood 거래 내역 CSV는 보유·평균 단가·현금을 계산, 보유 표는 Ticker·Quantity·Avg Price 열과 현금 CASH 줄). 전략 비교와 실제 매매 기록은 바뀌지 않습니다.'));
    if (upWrap) a.appendChild(upWrap);
  });
  if (b) act('snap', '고치기', '시작 스냅샷', `${s0.date ? md(s0.date) : '—'} · ${Object.keys(s0.holdings || {}).length}종목 + 현금`, (a) => a.appendChild(startForm(smodel, handlers, lastRec, s0)));
  act('holdings', '보기', '올린 보유 표', hold.asOf ? `${hold.asOf} · ${nHold}종목` : '아직 없음', (a) => { if (holdWrap) a.appendChild(holdWrap); });
  if (memo && memo.childElementCount) act('memo', '보기', '모의 운용 메모', '손으로 적은 기록', (a) => a.appendChild(memo));
  if (area.hidden && view.open) { view.open = null; keep(); }   // 열어 둔 칸이 없어졌으면(묶음을 끝냄 등) 기억을 지운다

  // 자산이 쌓인 기록
  const recs = el('section', 'pf-r2recs');
  const head = el('div', 'pf-r2head'); head.appendChild(el('h2', 'pf-h2q', '자산이 쌓인 기록'));
  const keys = Object.keys(FILTER).filter((k) => k === 'all' || items.some(FILTER[k][1]));
  if (!keys.includes(view.filter)) view.filter = 'all';
  const filters = el('div', 'pf-seg pf-segbox'); filters.setAttribute('role', 'group'); filters.setAttribute('aria-label', '보기');
  for (const k of keys) {
    const f = btn(`${FILTER[k][0]} ${items.filter(FILTER[k][1]).length}`, 'pf-segbtn'); f.setAttribute('aria-pressed', String(view.filter === k));
    f.addEventListener('click', () => { view.filter = k; keep(); draw(); });
    filters.appendChild(f);
  }
  head.appendChild(filters); recs.appendChild(head);
  const msg = msgLine();
  const list = el('div', 'pf-r2list');
  const shown = items.filter(FILTER[view.filter][1]);
  if (!shown.length) { const e = el('section', 'pf-panel'); e.appendChild(el('p', 'pf-empty', '아직 기록이 없습니다. 매매는 위 "＋ 매매 기록"으로 적습니다.')); list.appendChild(e); }
  // ⋯ → 그 줄에 할 수 있는 일, 고치기를 누르면 그 자리에서 양식
  const fill = (it, box) => {
    const row = el('div', 'pf-acts pf-edacts');
    if (it.kind === 'trade') {
      const fix = btn('고치기'); fix.addEventListener('click', () => { box.textContent = ''; tradeEdit(box, it.id, it.raw, handlers, h); });
      const del = btn('지우기'); twoStep(del, msg, `${it.title} 기록을 지웁니다. 맞으면 지우기를 한 번 더 누르세요.`, () => handlers.deleteTrade(it.id));
      row.appendChild(fix); row.appendChild(del);
    } else if (it.kind === 'deposit') {
      const fix = btn('고치기'); fix.addEventListener('click', () => { box.textContent = ''; depositEdit(box, it.id, it.raw, handlers); });
      const del = btn('지우기'); twoStep(del, msg, `이 ${it.raw.kind === 'withdraw' ? '출금' : '입금'}을 지웁니다(처음부터 다시 계산). 맞으면 지우기를 한 번 더 누르세요.`, () => handlers.deleteDeposit(it.id));
      row.appendChild(fix); row.appendChild(del);
    } else if (it.kind === 'snap') {
      const fix = btn('고치기'); fix.addEventListener('click', () => { box.textContent = ''; box.appendChild(startForm(smodel, handlers, lastRec, it.raw)); });
      row.appendChild(fix);
    } else {
      const go = btn('다시 올리기'); go.addEventListener('click', () => { view.open = 'upload'; keep(); draw(); document.getElementById('pf-r2area')?.scrollIntoView?.({ block: 'nearest' }); });
      row.appendChild(go);
    }
    box.appendChild(row);
  };
  const moreBtn = (it, edit) => {
    const more = btn('⋯', 'pf-more pf-r2more'); more.setAttribute('aria-label', `${it.title} ${it.kind === 'snap' ? '고치기' : it.kind === 'upload' ? '다시 올리기' : '고치기·지우기'}`); more.setAttribute('aria-expanded', 'false');
    more.addEventListener('click', () => {
      const was = !edit.hidden;
      list.querySelectorAll('.pf-edit').forEach((e) => { e.hidden = true; e.textContent = ''; });
      list.querySelectorAll('.pf-more').forEach((m) => m.setAttribute('aria-expanded', 'false'));
      if (was) return;
      edit.hidden = false; more.setAttribute('aria-expanded', 'true'); fill(it, edit);
    });
    return more;
  };
  const stateCls = (st) => (st === '취소됨' ? 'pf-r2off' : st === '반영' || /^\d{4}-\d\d-\d\d 반영$/.test(st) ? 'pf-r2ok' : 'pf-r2wait');
  let baseGrid = null;
  for (const g of dayGroups(shown)) {
    if (g.moves.length) {
      baseGrid = null;
      const card = el('section', 'pf-panel pf-r2day');
      const dh = el('div', 'pf-r2dayhead');
      dh.appendChild(el('strong', 'pf-r2date', kdate(g.date, today)));
      const accts = [...new Set(g.moves.filter((x) => x.kind === 'trade').map((x) => h.acctName?.(x.raw)).filter(Boolean))];
      const cancelled = g.moves.filter((x) => x.state === '취소됨').length;
      dh.appendChild(el('span', 'pf-r2daysub', [g.buys && `매수 ${g.buys}건`, g.sells && `매도 ${g.sells}건`, g.deps && `입금 ${g.deps}건`, g.outs && `출금 ${g.outs}건`, cancelled && `취소 ${cancelled}건`,
        accts.length && accts.map((a) => a.replace(' 계좌', '')).join('·') + ' 계좌'].filter(Boolean).join(' · ')));
      const hasT = g.buys + g.sells > 0, hasD = g.deps + g.outs > 0;
      if (hasT || hasD) {
        const tot = el('strong', 'pf-r2date pf-r2tot');
        if (hasT && hasD) tot.appendChild(el('small', null, '매매 '));
        tot.appendChild(document.createTextNode(signed(hasT ? g.tradeNet : g.cashNet)));
        dh.appendChild(tot);
      }
      card.appendChild(dh);
      const tiles = el('div', 'pf-r2tiles');
      for (const it of g.moves) {
        const tile = el('div', 'pf-r2tile' + (it.state === '취소됨' ? ' pf-r2dead' : ''));
        const main = el('div', 'pf-r2tmain');
        const x = it.raw;
        if (it.kind === 'trade') {
          const nm = el('strong', 'pf-r2tk', x.ticker); nm.appendChild(el('small', x.side === 'buy' ? 'pf-r2side' : 'pf-r2side pf-r2sell', x.side === 'buy' ? '매수' : '매도')); main.appendChild(nm);
          main.appendChild(el('span', 'pf-s', `${shares(x.qty)}주 × ${usd(x.price)}`));
        } else {
          main.appendChild(el('strong', 'pf-r2tk', x.kind === 'withdraw' ? '출금' : '입금'));
          if (x.forMonth && x.kind !== 'withdraw') main.appendChild(el('span', 'pf-s', `${+x.forMonth.slice(5)}월 몫(미리)`));
        }
        const amt = el('span', 'pf-r2amt', usd(Math.abs(it.value)));
        amt.appendChild(el('small', stateCls(it.state), '· ' + it.state.replace(/^\d{4}-(\d\d)-(\d\d)/, '$1/$2')));
        main.appendChild(amt);
        tile.appendChild(main);
        const edit = el('div', 'pf-edit pf-r2edit'); edit.hidden = true;
        tile.appendChild(moreBtn(it, edit));
        tiles.appendChild(tile); tiles.appendChild(edit);
      }
      card.appendChild(tiles);
      list.appendChild(card);
    }
    for (const it of g.base) {
      if (!baseGrid) { baseGrid = el('div', 'pf-r2base'); list.appendChild(baseGrid); }
      const card = el('section', 'pf-panel pf-r2basecard');
      const row = el('div', 'pf-r2baserow');
      const main = el('div', 'pf-r2tmain');
      main.appendChild(el('span', 'pf-r2verb', `${kdate(it.date, today)} · ${it.kind === 'snap' ? '비교 시작' : '보유 파일'}`));
      main.appendChild(el('strong', 'pf-r2tk', it.title));
      main.appendChild(el('span', 'pf-s', it.detail));
      row.appendChild(main);
      const edit = el('div', 'pf-edit pf-r2edit'); edit.hidden = true;
      row.appendChild(moreBtn(it, edit));
      card.appendChild(row); card.appendChild(edit);
      baseGrid.appendChild(card);
    }
  }
  recs.appendChild(list);
  recs.appendChild(msg);

  // 맨 아래: 계산 방식, 되돌릴 수 없는 작업
  const foot = el('div', 'pf-r2foot');
  const info = el('section', 'pf-panel pf-r2info');
  info.appendChild(el('strong', null, '기록이 성과의 기준이 됩니다'));
  info.appendChild(el('p', 'pf-sub', '입금은 수익과 따로 셉니다. 모든 전략은 같은 시작 스냅샷에서 출발합니다.'));
  const how = el('details', 'pf-minifold'); how.appendChild(el('summary', null, '계산 방식'));
  how.appendChild(el('p', 'pf-note', '매매·입출금 기록은 언제든 고치거나 지울 수 있습니다. 올린 보유의 기준일과 그 전 날짜의 매매는 이미 올린 보유에 들어 있다고 보고 반영하지 않습니다. 입금은 기록한 뒤 처음 오는 장 시작(동부 09:30)부터 반영합니다. 입금·스냅샷을 고치면 모든 전략을 처음부터 다시 계산합니다.'));
  info.appendChild(how);
  foot.appendChild(info);
  if (b) {
    const dz = el('section', 'pf-r2danger');
    dz.appendChild(el('span', 'pf-r2dk', '되돌릴 수 없는 작업'));
    const adv = el('details', 'pf-minifold pf-danger'); adv.appendChild(el('summary', null, `고급 관리 · 처음부터 다시 하기 (묶음 ${smodel.bundleNo})`));
    adv.appendChild(el('p', 'pf-note', '이 묶음을 "정정으로 종료"로 남기고 계산에서 뺀 뒤, 새 시작 스냅샷으로 다시 시작합니다.' + (smodel.closedCount ? ` 끝낸 묶음 ${smodel.closedCount}개.` : '')));
    const end = btn('이 묶음 끝내기'); const em = msgLine();
    adv.appendChild(end); adv.appendChild(em);
    twoStep(end, em, '이 묶음을 끝냅니다. 맞으면 한 번 더 누르세요.', () => handlers.close());
    dz.appendChild(adv);
    foot.appendChild(dz);
  }

  mg.appendChild(top); mg.appendChild(acts); mg.appendChild(recs); mg.appendChild(foot);
  place = () => {
    if (!acts.isConnected) return;
    const f = document.activeElement;
    if (PHONE?.matches) mg.insertBefore(acts, foot); else mg.insertBefore(acts, recs);
    if (f && f !== document.activeElement && mg.contains(f)) f.focus?.();
  };
  place();
  // 닫힌 칸에 들어가지 않은 고정 요소는 숨긴 보관 칸으로 돌려 둔다(id로 계속 찾을 수 있게)
  const holder = document.getElementById('pf-static');
  for (const x of [upWrap, holdWrap, memo]) if (x && !x.isConnected && holder) holder.appendChild(x);
}

const md = (d) => (d ? d.slice(5).replace('-', '/') : '');
// 입금·출금 추가(데이터 관리 칸). 출금은 모든 전략에서 현금에서만 뺀다(현금이 모자라면 뺄 수 있는 만큼 — 2026-10-22 사용자 결정)
function depositForm(box, handlers) {
  const f = el('div', 'pf-form pf-tradeform');
  const kl = el('label', 'pf-field'); kl.appendChild(el('span', null, '종류'));
  const kind = el('select');
  for (const [v, t] of [['deposit', '입금(넣은 돈)'], ['withdraw', '출금(뺀 돈)']]) { const o = el('option', null, t); o.value = v; kind.appendChild(o); }
  kl.appendChild(kind); f.appendChild(kl);
  const l = el('label', 'pf-field'); l.appendChild(el('span', null, '금액(USD)'));
  const amt = el('input'); amt.type = 'number'; amt.min = '0.01'; amt.step = '0.01'; l.appendChild(amt); f.appendChild(l);
  const save = btn('기록', 'pf-btn'); const msg = msgLine();
  f.appendChild(save); f.appendChild(msg);
  twoStep(save, msg, '이 금액을 기록합니다. 맞으면 한 번 더 누르세요.', async () => {
    const v = Number(amt.value);
    if (!(v > 0) || Math.round(v * 100) / 100 !== v || v > 1e7) throw new Error('0보다 큰 금액을 센트 단위까지 넣으세요.');
    await handlers.deposit(v, kind.value);
  }, f);
  box.appendChild(f);
}

function tradeEdit(box, id, x, handlers, h) {
  box.appendChild(el('p', 'pf-note', `${x.date} ${x.ticker} 기록 고치기`));
  const f = el('div', 'pf-form pf-tradeform');
  const field = (lab, input) => { const l = el('label', 'pf-field'); l.appendChild(el('span', null, lab)); l.appendChild(input); f.appendChild(l); return input; };
  const d = field('날짜(체결일, 미국 동부)', el('input')); d.type = 'date'; d.value = x.date;
  const sd = field('매매', el('select'));
  for (const [v, t] of [['buy', '매수'], ['sell', '매도']]) { const o = el('option', null, t); o.value = v; sd.appendChild(o); }
  sd.value = x.side;
  const tk = field('종목(티커)', el('input')); tk.value = x.ticker; tk.className = 'pf-ticker';
  const q = field('수량', el('input')); q.type = 'number'; q.step = 'any'; q.value = String(x.qty);
  const pr = field('체결가(USD)', el('input')); pr.type = 'number'; pr.step = '0.0001'; pr.value = String(x.price);
  const save = btn('저장', 'pf-btn');
  const close = btn('닫기'); close.addEventListener('click', () => { box.hidden = true; box.textContent = ''; });
  const em = msgLine();
  f.appendChild(save); f.appendChild(close); f.appendChild(em);
  box.appendChild(f);
  twoStep(save, em, '이대로 고칩니다. 맞으면 한 번 더 누르세요.', async () => {
    const y = { date: d.value, ticker: tk.value.trim().toUpperCase(), side: sd.value, qty: Number(q.value), price: Number(pr.value) };
    const bad = h.checkTrade(y, h.etDate(Date.now()));
    if (bad) throw new Error(bad);
    await handlers.editTrade(id, y);
  }, f);
}

function depositEdit(box, id, d, handlers) {
  box.appendChild(el('span', 'pf-note', `${d.recordedAt ? d.recordedAt.slice(0, 10) : ''} ${d.kind === 'withdraw' ? '출금' : '입금'} 금액 고치기`));
  const a = el('input'); a.type = 'number'; a.min = '0.01'; a.step = '0.01'; a.value = String(d.amount); a.setAttribute('aria-label', '새 금액(USD)');
  const save = btn('저장', 'pf-btn');
  const close = btn('닫기'); close.addEventListener('click', () => { box.hidden = true; box.textContent = ''; });
  const em = msgLine();
  box.appendChild(a); box.appendChild(save); box.appendChild(close); box.appendChild(em);
  twoStep(save, em, '이 금액으로 고칩니다(처음부터 다시 계산). 맞으면 한 번 더 누르세요.', async () => {
    const v = Number(a.value);
    if (!(v > 0) || Math.round(v * 100) / 100 !== v || v > 1e7) throw new Error('0보다 큰 금액을 센트 단위까지 넣으세요.');
    await handlers.editDeposit(id, v);
  }, box);
}
