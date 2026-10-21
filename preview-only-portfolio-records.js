// preview 전용 Portfolio 탭 — 기록·관리 하위 탭(2026-10-21 사용자 선택: 디자인 시안 "기록 A · 한 줄 타임라인"). 라이브로 옮기지 않는다 — pipeline/site_ui/UI_DIFF.md 1절 portfolio.
//
// 실제 매매·입금·시작 스냅샷·올린 보유를 날짜순 한 목록으로 보여 주고(종류별로 거를 수 있음), 줄마다 고치기·지우기를 둔다.
// "＋ 기록 추가"는 매매·입금 입력을 연다. 묶음 끝내기는 맨 아래에 접어 둔다. 저장은 handlers(trade·editTrade·deleteTrade·deposit·editDeposit·deleteDeposit·close).
// 한눈에 파일(-home.js)이 이 파일을 부르므로, 거기 있는 계산(currentHoldings·checkTrade·etDate)은 인자 h로 받는다(같은 모듈을 두 번 읽지 않게).
// 순수 함수 timelineItems는 node 시험이 부른다(pipeline/portfolio/test_strategy_view.mjs).
import { el, msgLine, twoStep, usd, shares, startForm } from './preview-only-portfolio-strategy.js?v=15';
import { depositTiming } from './preview-only-portfolio-engine.js?v=2';

// ---- 순수 함수 ----

// 입금 하나의 상태 글(엔진과 같은 기준: 취소는 반영일 09:30 ET 전에 기록된 것만 효력)
export function depositState(id, d, cancelAt, now) {
  const t = depositTiming(d.recordedAt);
  const cAt = cancelAt.has(id) ? Date.parse(cancelAt.get(id)) : null;
  if (cAt != null && t.day && cAt < t.cancelBefore) return '취소됨';
  return (t.day ? t.day + (now < t.cancelBefore ? ' 반영 예정' : ' 반영') : '반영일 계산 불가') + (cAt != null ? '(취소가 반영 뒤라 무시됨)' : '');
}

// 기록 → 목록 줄(최신이 위). cur = currentHoldings 결과(매매 상태), bundle = 지금 묶음(없거나 끝났으면 입금·스냅샷 없음)
// 줄: { kind: 'trade'|'deposit'|'snap'|'upload', id, date, title, detail, amount, raw }
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
      detail: `${usd(x.price)} · ${state}`, amount: (x.side === 'buy' ? '−' : '+') + usd(amt), raw: x });
  }
  if (bundle && !bundle.closed) {
    const deps = Object.entries(bundle.deposits || {});
    const cancelAt = new Map();
    for (const [, d] of deps) if (d.cancels && d.recordedAt && (!cancelAt.has(d.cancels) || d.recordedAt < cancelAt.get(d.cancels))) cancelAt.set(d.cancels, d.recordedAt);
    for (const [id, d] of deps) {
      if (d.cancels) continue;
      const rec = d.recordedAt ? etDate(Date.parse(d.recordedAt)) : null;
      out.push({ kind: 'deposit', id, date: rec || '', title: `입금 ${usd(d.amount)}`,
        detail: `${rec ? rec + ' 기록' : '기록 중'} · ${depositState(id, d, cancelAt, now)}`, amount: '+' + usd(d.amount), raw: d });
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

// ---- 그리기 ----

const KIND = { trade: '매매', deposit: '입금', snap: '시작 스냅샷', upload: '올린 보유' };
const ICON = { trade: '↗', deposit: '+', snap: '≡', upload: '≡' };
const FILTER = { all: ['전체', () => true], trade: ['매매', (x) => x.kind === 'trade'], deposit: ['입금', (x) => x.kind === 'deposit'], base: ['시작·보유', (x) => x.kind === 'snap' || x.kind === 'upload'] };
const VIEW_KEY = 'pf-rec-view';
const view = (() => { try { return { filter: 'all', open: null, ...JSON.parse(sessionStorage.getItem(VIEW_KEY) || '{}') }; } catch (_) { return { filter: 'all', open: null }; } })();
const keep = () => { try { sessionStorage.setItem(VIEW_KEY, JSON.stringify(view)); } catch (_) { /* 기억 못 해도 화면은 그대로 */ } };
const btn = (text, cls) => { const b = el('button', cls || 'pf-btn pf-btn-quiet', text); b.type = 'button'; return b; };

// mg = #pf-manage, h = { currentHoldings, checkTrade, etDate } (-home.js에서 넘긴다)
// 2026-10-21 최종 시안: 왼쪽 "자산이 쌓인 기록"(줄마다 ⋯ 하나), 오른쪽 "데이터 관리" 목록(입금 추가·보유 파일 올리기·시작 스냅샷 고치기·
// 올린 보유 표·모의 운용 메모)과 계산 방식·고급 관리 접기. 파일 올리기·올린 보유 표·메모는 html의 #pf-static에 있는 요소를 옮겨 쓴다
// (preview-only-portfolio.js가 id로 채우고 이벤트를 단다).
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
  const grid = el('div', 'pf-recgrid');

  // 왼쪽: 자산이 쌓인 기록
  const sec = el('section', 'pf-panel pf-recs');
  const t = el('div'); t.appendChild(el('h2', 'pf-h2q', '자산이 쌓인 기록')); t.appendChild(el('p', 'pf-sub', '매매·입금·시작 설정을 한곳에서. 새 매매는 위 "＋ 매매 기록"으로 적습니다.'));
  sec.appendChild(t);
  const keys = Object.keys(FILTER).filter((k) => k === 'all' || items.some(FILTER[k][1]));
  if (!keys.includes(view.filter)) view.filter = 'all';
  const filters = el('div', 'pf-seg pf-segbox'); filters.setAttribute('role', 'group'); filters.setAttribute('aria-label', '보기');
  for (const k of keys) {
    const f = btn(`${FILTER[k][0]} ${items.filter(FILTER[k][1]).length}`, 'pf-segbtn'); f.setAttribute('aria-pressed', String(view.filter === k));
    f.addEventListener('click', () => { view.filter = k; keep(); draw(); });
    filters.appendChild(f);
  }
  sec.appendChild(filters);
  const msg = msgLine();
  const list = el('div', 'pf-reclist');
  const shown = items.filter(FILTER[view.filter][1]);
  if (!shown.length) list.appendChild(el('p', 'pf-empty', '아직 기록이 없습니다. 위 "＋ 매매 기록"이나 오른쪽 "입금 추가"로 적습니다.'));
  for (const it of shown) {
    const row = el('div', 'pf-recrow');
    row.appendChild(el('span', 'pf-recdate', it.date || '—'));
    const ic = el('span', 'pf-recicon pf-rb-' + it.kind, ICON[it.kind]); ic.setAttribute('aria-hidden', 'true'); row.appendChild(ic);
    const txt = el('span', 'pf-rectext'); txt.appendChild(el('strong', null, it.title)); txt.appendChild(el('small', null, (it.kind === 'trade' ? '매매 · ' : '') + it.detail)); row.appendChild(txt);   // 아이콘은 꾸밈이라 종류는 제목·설명 글로 읽힌다
    row.appendChild(el('strong', 'pf-recamt', it.amount));
    const more = btn('⋯', 'pf-more'); more.setAttribute('aria-label', `${it.title} 고치기·지우기`); more.setAttribute('aria-expanded', 'false');
    row.appendChild(more);
    const edit = el('div', 'pf-edit'); edit.hidden = true;
    // ⋯ → 그 줄에 할 수 있는 일, 고치기를 누르면 그 자리에서 양식
    const fill = (box) => {
      const acts = el('div', 'pf-acts pf-edacts');
      if (it.kind === 'trade') {
        const fix = btn('고치기'); fix.addEventListener('click', () => { box.textContent = ''; tradeEdit(box, it.id, it.raw, handlers, h); });
        const del = btn('지우기'); twoStep(del, msg, `${it.title} 기록을 지웁니다. 맞으면 지우기를 한 번 더 누르세요.`, () => handlers.deleteTrade(it.id));
        acts.appendChild(fix); acts.appendChild(del);
      } else if (it.kind === 'deposit') {
        const fix = btn('고치기'); fix.addEventListener('click', () => { box.textContent = ''; depositEdit(box, it.id, it.raw, handlers); });
        const del = btn('지우기'); twoStep(del, msg, '이 입금을 지웁니다(처음부터 다시 계산). 맞으면 지우기를 한 번 더 누르세요.', () => handlers.deleteDeposit(it.id));
        acts.appendChild(fix); acts.appendChild(del);
      } else if (it.kind === 'snap') {
        const fix = btn('고치기'); fix.addEventListener('click', () => { box.textContent = ''; box.appendChild(startForm(smodel, handlers, lastRec, it.raw)); });
        acts.appendChild(fix);
      } else {
        const go = btn('다시 올리기'); go.addEventListener('click', () => { view.open = 'upload'; keep(); draw(); document.getElementById('pf-upwrap')?.scrollIntoView?.({ block: 'nearest' }); });
        acts.appendChild(go);
      }
      box.appendChild(acts);
    };
    more.addEventListener('click', () => {
      const was = !edit.hidden;
      list.querySelectorAll('.pf-edit').forEach((e) => { e.hidden = true; e.textContent = ''; });
      list.querySelectorAll('.pf-more').forEach((m) => m.setAttribute('aria-expanded', 'false'));
      if (was) return;
      edit.hidden = false; more.setAttribute('aria-expanded', 'true'); fill(edit);
    });
    list.appendChild(row);
    list.appendChild(edit);
  }
  sec.appendChild(list);
  sec.appendChild(msg);
  grid.appendChild(sec);

  // 오른쪽: 데이터 관리
  const side = el('div', 'pf-homecol pf-recside');
  const dm = el('section', 'pf-panel pf-side');
  dm.appendChild(el('div', 'pf-eyebrow2', '데이터 관리'));
  dm.appendChild(el('h2', 'pf-h2s', '내 기록의 출발점'));
  const item = (key, title, sub, mark, body) => {
    const b2 = btn(null, 'pf-dmrow'); b2.setAttribute('aria-expanded', String(view.open === key));
    const tt = el('span', 'pf-dmtext'); tt.appendChild(el('strong', null, title)); if (sub) tt.appendChild(el('small', null, sub)); b2.appendChild(tt);
    const mk = el('span', 'pf-dmmark' + (mark === '+' ? ' pf-dmplus' : ''), mark); mk.setAttribute('aria-hidden', 'true'); b2.appendChild(mk);
    const area = el('div', 'pf-dmarea'); area.hidden = view.open !== key;
    if (body) body(area);
    b2.addEventListener('click', () => { view.open = view.open === key ? null : key; keep(); draw(); });
    dm.appendChild(b2); dm.appendChild(area);
  };
  if (b) item('deposit', '입금 추가', '반영일 장 시작부터 모든 전략에 같이', '+', (a) => depositForm(a, handlers));
  if (pendingUpload) view.open = 'upload';
  item('upload', '보유 파일 올리기', 'CSV · Excel · JSON, 올리기 전 확인', '↗', (a) => {
    a.appendChild(el('p', 'pf-note', 'JSON은 원칙·올린 보유·관심 종목을 통째로, CSV·Excel은 올린 보유만 바꿉니다(Robinhood 거래 내역 CSV는 보유·평균 단가·현금을 계산, 보유 표는 Ticker·Quantity·Avg Price 열과 현금 CASH 줄). 전략 비교와 실제 매매 기록은 바뀌지 않습니다.'));
    if (upWrap) a.appendChild(upWrap);
  });
  if (b) {
    const s = b.snapshot || {};
    item('snap', '시작 스냅샷 고치기', `${s.date ? md(s.date) + ' 장 마감' : '—'} · ${Object.keys(s.holdings || {}).length}종목 + 현금`, '→', (a) => a.appendChild(startForm(smodel, handlers, lastRec, s)));
  }
  const n = (hold.rows || []).filter((r) => String(r.ticker || '').trim()).length;
  item('holdings', '올린 보유 표', hold.asOf ? `${hold.asOf} · ${n}종목` : '아직 없음', '+', (a) => { if (holdWrap) a.appendChild(holdWrap); });
  if (memo && memo.childElementCount) item('memo', '모의 운용 메모', '올린 데이터의 손으로 적은 기록', '+', (a) => a.appendChild(memo));
  side.appendChild(dm);
  const info = el('section', 'pf-panel pf-side');
  info.appendChild(el('strong', null, '기록이 성과의 기준이 됩니다'));
  info.appendChild(el('p', 'pf-sub', '입금은 수익과 따로 셉니다. 모든 전략은 같은 시작 스냅샷에서 출발합니다.'));
  const how = el('details', 'pf-minifold'); how.appendChild(el('summary', null, '계산 방식'));
  how.appendChild(el('p', 'pf-note', '기록은 언제든 고치거나 지울 수 있습니다. 올린 보유의 기준일과 그 전 날짜의 매매는 이미 올린 보유에 들어 있다고 보고 반영하지 않습니다. 입금은 기록한 뒤 처음 오는 장 시작(동부 09:30)부터 반영합니다. 입금·스냅샷을 고치면 모든 전략을 처음부터 다시 계산합니다.'));
  info.appendChild(how);
  if (b) {
    const adv = el('details', 'pf-minifold pf-danger'); adv.appendChild(el('summary', null, `고급 관리 · 처음부터 다시 하기 (묶음 ${smodel.bundleNo})`));
    adv.appendChild(el('p', 'pf-note', '이 묶음을 "정정으로 종료"로 남기고 계산에서 뺀 뒤, 새 시작 스냅샷으로 다시 시작합니다.' + (smodel.closedCount ? ` 끝낸 묶음 ${smodel.closedCount}개.` : '')));
    const end = btn('이 묶음 끝내기'); const em = msgLine();
    adv.appendChild(end); adv.appendChild(em);
    twoStep(end, em, '이 묶음을 끝냅니다. 맞으면 한 번 더 누르세요.', () => handlers.close());
    info.appendChild(adv);
  }
  side.appendChild(info);
  grid.appendChild(side);
  mg.appendChild(grid);
  // 닫힌 칸에 들어가지 않은 고정 요소는 숨긴 보관 칸으로 돌려 둔다(id로 계속 찾을 수 있게)
  const holder = document.getElementById('pf-static');
  for (const x of [upWrap, holdWrap, memo]) if (x && !x.isConnected && holder) holder.appendChild(x);
}

const md = (d) => (d ? d.slice(5).replace('-', '/') : '');
// 입금 추가(데이터 관리 칸)
function depositForm(box, handlers) {
  const f = el('div', 'pf-form pf-tradeform');
  const l = el('label', 'pf-field'); l.appendChild(el('span', null, '입금액(USD)'));
  const amt = el('input'); amt.type = 'number'; amt.min = '0.01'; amt.step = '0.01'; l.appendChild(amt); f.appendChild(l);
  const save = btn('기록', 'pf-btn'); const msg = msgLine();
  f.appendChild(save); f.appendChild(msg);
  twoStep(save, msg, '이 금액을 기록합니다. 맞으면 한 번 더 누르세요.', async () => {
    const v = Number(amt.value);
    if (!(v > 0) || Math.round(v * 100) / 100 !== v || v > 1e7) throw new Error('0보다 큰 금액을 센트 단위까지 넣으세요.');
    await handlers.deposit(v);
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
  box.appendChild(el('span', 'pf-note', `${d.recordedAt ? d.recordedAt.slice(0, 10) : ''} 입금 금액 고치기`));
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
