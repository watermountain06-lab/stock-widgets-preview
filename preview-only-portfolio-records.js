// preview 전용 Portfolio 탭 — 기록·관리 하위 탭(2026-10-21 사용자 선택: 디자인 시안 "기록 A · 한 줄 타임라인"). 라이브로 옮기지 않는다 — pipeline/site_ui/UI_DIFF.md 1절 portfolio.
//
// 실제 매매·입금·시작 스냅샷·올린 보유를 날짜순 한 목록으로 보여 주고(종류별로 거를 수 있음), 줄마다 고치기·지우기를 둔다.
// "＋ 기록 추가"는 매매·입금 입력을 연다. 묶음 끝내기는 맨 아래에 접어 둔다. 저장은 handlers(trade·editTrade·deleteTrade·deposit·editDeposit·deleteDeposit·close).
// 한눈에 파일(-home.js)이 이 파일을 부르므로, 거기 있는 계산(currentHoldings·checkTrade·etDate)은 인자 h로 받는다(같은 모듈을 두 번 읽지 않게).
// 순수 함수 timelineItems는 node 시험이 부른다(pipeline/portfolio/test_strategy_view.mjs).
import { el, msgLine, twoStep, usd, shares, startForm } from './preview-only-portfolio-strategy.js?v=14';
import { depositTiming } from './preview-only-portfolio-engine.js?v=1';

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
    out.push({ kind: 'upload', id: 'upload', date: asOf.slice(0, 10), title: '올린 보유', detail: `${asOf} · ${n}종목${cash ? ' + 현금' : ''}`, amount: '', raw: null });
  }
  const order = { trade: 0, deposit: 1, snap: 2, upload: 3 };
  return out.sort((a, b) => (a.date !== b.date ? (a.date < b.date ? 1 : -1) : order[a.kind] - order[b.kind]));
}

// ---- 그리기 ----

const KIND = { trade: '매매', deposit: '입금', snap: '스냅샷', upload: '올린 보유' };
const VIEW_KEY = 'pf-rec-view';
const view = (() => { try { return { filter: 'all', form: false, kind: 'trade', ...JSON.parse(sessionStorage.getItem(VIEW_KEY) || '{}') }; } catch (_) { return { filter: 'all', form: false, kind: 'trade' }; } })();
const keep = () => { try { sessionStorage.setItem(VIEW_KEY, JSON.stringify(view)); } catch (_) { /* 기억 못 해도 화면은 그대로 */ } };
const btn = (text, cls) => { const b = el('button', cls || 'pf-btn pf-btn-quiet', text); b.type = 'button'; return b; };

// mg = #pf-manage, h = { currentHoldings, checkTrade, etDate } (-home.js에서 넘긴다)
let latest = null;
export function renderManage(mg, model, smodel, handlers, h) {
  latest = [mg, model, smodel, handlers, h];
  const draw = () => renderManage(...latest);   // 저장 뒤 늦게 부르는 닫기도 새로 받은 값으로 그린다
  mg.textContent = '';
  const b = smodel.bundle && !smodel.bundle.closed ? smodel.bundle : null;
  const lastRec = (smodel.records || []).at(-1)?.session || null;
  if (!b) mg.appendChild(startForm(smodel, handlers, lastRec));
  const now = model.now ?? Date.now(), today = h.etDate(now);
  const hold = model.main?.holdings || {};
  const cur = h.currentHoldings(hold.rows, hold.asOf, model.trades, today);
  const items = timelineItems({ trades: model.trades, cur, bundle: b, bundleNo: smodel.bundleNo, holdings: hold, now, etDate: h.etDate });

  const sec = el('div', 'pf-st-block pf-recs');
  const head = el('div', 'pf-rankhead');
  head.appendChild(el('h3', null, '모든 기록'));
  const add = btn(view.form ? '닫기' : '＋ 기록 추가', 'pf-btn');
  add.addEventListener('click', () => { view.form = !view.form; keep(); draw(); });
  head.appendChild(add);
  sec.appendChild(head);
  if (view.form) sec.appendChild(addForm(b, handlers, h, today, draw));

  const count = (k) => items.filter((x) => k === 'all' || x.kind === k).length;
  const kinds = ['all', 'trade', 'deposit', 'snap'].filter((k) => k === 'all' || count(k));
  if (!kinds.includes(view.filter)) view.filter = 'all';
  const filters = el('div', 'pf-seg'); filters.setAttribute('role', 'group'); filters.setAttribute('aria-label', '보기');
  for (const k of kinds) {
    const f = btn(`${k === 'all' ? '전체' : KIND[k]} ${count(k)}`, 'pf-pill'); f.setAttribute('aria-pressed', String(view.filter === k));
    f.addEventListener('click', () => { view.filter = k; keep(); draw(); });
    filters.appendChild(f);
  }
  sec.appendChild(filters);

  const msg = msgLine();
  const list = el('div', 'pf-reclist');
  const shown = items.filter((x) => view.filter === 'all' || x.kind === view.filter);
  if (!shown.length) list.appendChild(el('p', 'pf-empty', '아직 기록이 없습니다. ＋ 기록 추가로 실제 매매나 입금을 적습니다.'));
  for (const it of shown) {
    const row = el('div', 'pf-recrow');
    row.appendChild(el('span', 'pf-recdate', it.date || '—'));
    row.appendChild(el('span', 'pf-recbadge pf-rb-' + it.kind, KIND[it.kind]));
    const txt = el('span', 'pf-rectext'); txt.appendChild(el('strong', null, it.title)); txt.appendChild(el('small', null, it.detail)); row.appendChild(txt);
    row.appendChild(el('strong', 'pf-recamt', it.amount));
    const acts = el('span', 'pf-acts');
    const edit = el('div', 'pf-edit'); edit.hidden = true;
    const open = (fill) => { const was = !edit.hidden; list.querySelectorAll('.pf-edit').forEach((e) => { e.hidden = true; e.textContent = ''; }); if (was) return; edit.hidden = false; fill(edit); };
    if (it.kind === 'trade') {
      const fix = btn('고치기'); fix.addEventListener('click', () => open((box) => tradeEdit(box, it.id, it.raw, handlers, h)));
      const del = btn('지우기'); twoStep(del, msg, `${it.title} 기록을 지웁니다. 맞으면 지우기를 한 번 더 누르세요.`, () => handlers.deleteTrade(it.id));
      acts.appendChild(fix); acts.appendChild(del);
    } else if (it.kind === 'deposit') {
      const fix = btn('고치기'); fix.addEventListener('click', () => open((box) => depositEdit(box, it.id, it.raw, handlers)));
      const del = btn('지우기'); twoStep(del, msg, '이 입금을 지웁니다(처음부터 다시 계산). 맞으면 지우기를 한 번 더 누르세요.', () => handlers.deleteDeposit(it.id));
      acts.appendChild(fix); acts.appendChild(del);
    } else if (it.kind === 'snap') {
      const fix = btn('고치기'); fix.addEventListener('click', () => open((box) => box.appendChild(startForm(smodel, handlers, lastRec, it.raw))));
      acts.appendChild(fix);
    } else {
      const go = btn('다시 올리기'); go.addEventListener('click', () => document.getElementById('pf-upload')?.closest('section')?.scrollIntoView?.({ block: 'start' }));
      acts.appendChild(go);
    }
    row.appendChild(acts);
    list.appendChild(row);
    list.appendChild(edit);
  }
  sec.appendChild(list);
  sec.appendChild(msg);
  sec.appendChild(el('p', 'pf-note', '기록은 언제든 고치거나 지울 수 있습니다. 올린 보유의 기준일과 그 전 날짜의 매매는 이미 올린 보유에 들어 있다고 보고 반영하지 않습니다. 입금·스냅샷을 고치면 모든 전략을 처음부터 다시 계산합니다.'));
  mg.appendChild(sec);

  if (b) {
    const fold = el('details', 'pf-st-block pf-stfold');
    fold.appendChild(el('summary', null, `처음부터 다시 하기 (묶음 ${smodel.bundleNo} 끝내기)`));
    fold.appendChild(el('p', 'pf-note', '이 묶음을 "정정으로 종료"로 남기고 계산에서 뺀 뒤, 새 시작 스냅샷으로 다시 시작합니다.' + (smodel.closedCount ? ` 끝낸 묶음 ${smodel.closedCount}개.` : '')));
    const end = btn('이 묶음 끝내기'); const em = msgLine();
    fold.appendChild(end); fold.appendChild(em);
    twoStep(end, em, '이 묶음을 끝냅니다. 맞으면 한 번 더 누르세요.', () => handlers.close());
    mg.appendChild(fold);
  }
}

// ＋ 기록 추가: 매매 또는 입금(입금은 전략 비교를 시작한 뒤에만)
function addForm(b, handlers, h, today, draw) {
  const box = el('div', 'pf-edit pf-addform');
  const seg = el('div', 'pf-seg pf-segbox'); seg.setAttribute('role', 'group'); seg.setAttribute('aria-label', '기록 종류');
  for (const [k, t] of [['trade', '실제 매매'], ['deposit', '입금']]) {
    const s = btn(t, 'pf-segbtn'); s.setAttribute('aria-pressed', String(view.kind === k));
    s.addEventListener('click', () => { view.kind = k; keep(); draw(); });
    seg.appendChild(s);
  }
  box.appendChild(seg);
  const f = el('div', 'pf-form pf-tradeform');
  const field = (lab, input) => { const l = el('label', 'pf-field'); l.appendChild(el('span', null, lab)); l.appendChild(input); f.appendChild(l); return input; };
  const msg = msgLine();
  if (view.kind === 'deposit') {
    if (!b) { box.appendChild(el('p', 'pf-note', '입금은 전략 비교를 시작한 뒤(위 시작 스냅샷) 기록합니다.')); return box; }
    box.appendChild(el('p', 'pf-note', '실제로 넣은 금액을 적습니다. 기록한 뒤 처음 오는 장 시작(동부 09:30)부터 모든 전략과 기준선에 같이 들어갑니다.'));
    const amt = field('입금액(USD)', el('input')); amt.type = 'number'; amt.min = '0.01'; amt.step = '0.01';
    const save = btn('기록', 'pf-btn'); f.appendChild(save); f.appendChild(msg);
    twoStep(save, msg, '이 금액을 기록합니다. 맞으면 한 번 더 누르세요.', async () => {
      const v = Number(amt.value);
      if (!(v > 0) || Math.round(v * 100) / 100 !== v || v > 1e7) throw new Error('0보다 큰 금액을 센트 단위까지 넣으세요.');
      await handlers.deposit(v);
    }, f);
  } else {
    box.appendChild(el('p', 'pf-note', '실제로 사고판 것을 적습니다. 내 자산과 전략 비교의 "내 실제 계좌" 줄에 들어갑니다.'));
    const date = field('날짜(체결일, 미국 동부)', el('input')); date.type = 'date'; date.value = today; date.max = today;
    const side = field('매매', el('select'));
    for (const [v, t] of [['buy', '매수'], ['sell', '매도']]) { const o = el('option', null, t); o.value = v; side.appendChild(o); }
    const tick = field('종목(티커)', el('input')); tick.className = 'pf-ticker'; tick.autocomplete = 'off'; tick.setAttribute('list', 'pf-tickers');
    const qty = field('수량(주, 소수 가능)', el('input')); qty.type = 'number'; qty.min = '0'; qty.step = 'any';
    const price = field('체결가(USD)', el('input')); price.type = 'number'; price.min = '0'; price.step = '0.0001';
    const save = btn('기록', 'pf-btn'); f.appendChild(save); f.appendChild(msg);
    twoStep(save, msg, '이대로 기록합니다. 맞으면 한 번 더 누르세요.', async () => {
      const x = { date: date.value, ticker: tick.value.trim().toUpperCase(), side: side.value, qty: Number(qty.value), price: Number(price.value) };
      const bad = h.checkTrade(x, h.etDate(Date.now()));
      if (bad) throw new Error(bad);
      await handlers.trade(x);
    }, f);
  }
  box.appendChild(f);
  return box;
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
