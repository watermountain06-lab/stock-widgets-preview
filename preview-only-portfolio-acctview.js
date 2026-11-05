// preview 전용 Portfolio 탭 — "내 계좌" 하위 탭(2026-10-28 사용자 결정 C안: 위는 합계·비중 막대, 아래는 미국·한국 칸 나란히,
// 한국 칸은 단순하게 — 주식 수익률·환율 수익률 두 칸과 평균/오늘 환율·원화로 보면 한 상자, 환전 기록은 버튼 안). 라이브로 옮기지 않는다.
// 숫자는 home.js accountsState가 만든다(한눈에 탭과 같은 계산). 장부 쓰기는 handlers.ledgerAdd·ledgerCancel·ledgerCorrect.
import { el, usd, pct, twoStep, msgLine } from './preview-only-portfolio-strategy.js?v=27';
import { depositTiming } from './preview-only-portfolio-engine.js?v=12';

const won = (v) => (v == null ? '—' : '₩' + Math.round(v).toLocaleString('en-US'));
const rate = (v) => (v == null ? '—' : '₩' + v.toLocaleString('en-US', { minimumFractionDigits: 1, maximumFractionDigits: 1 }));
const md = (d) => (d ? `${+d.slice(5, 7)}/${d.slice(8, 10)}` : '');
const KIND = { fx: '환전', fxOut: '역환전', income: '배당·이자' };
let showFx = false;   // 환전 기록 펼침(다시 그려도 유지)

export function renderAccounts(root, a, handlers) {
  root.textContent = '';
  // 1) 합계·비중
  const top = el('section', 'pf-panel pf-acctop');
  const row = el('div', 'pf-acctrow');
  const left = el('div');
  left.appendChild(el('div', 'pf-eyebrow2', '두 계좌 합계'));
  const big = el('div', 'pf-acctbig', usd(a.total.value));
  if (a.fx) big.appendChild(el('small', null, ' ' + won(a.total.value * a.fx.rate)));
  left.appendChild(big);
  left.appendChild(el('div', 'pf-s', a.fx ? `환율 ${rate(a.fx.rate)}(${md(a.fx.bar || a.fx.from)} 봉${a.fx.carried ? ', 직전 값' : ''})` : '환율 없음'));
  row.appendChild(left);
  const r = el('div', 'pf-acctret');
  r.appendChild(el('div', 'pf-s', `합계 수익률${a.from ? ' · ' + md(a.from) + '부터' : ''}`));
  r.appendChild(el('strong', a.total.twr == null ? null : a.total.twr >= 0 ? 'pf-up' : 'pf-down', a.total.twr == null ? '—' : pct(a.total.twr)));
  row.appendChild(r);
  top.appendChild(row);
  const tot = a.rh.value + a.kw.value;
  if (tot > 0 && a.kw.used) {
    const bar = el('div', 'pf-acctbar'); bar.setAttribute('role', 'img');
    const p = Math.round((a.rh.value / tot) * 100);
    bar.setAttribute('aria-label', `미국 ${p}%, 한국 ${100 - p}%`);
    const b1 = el('span', 'pf-acc-us'); b1.style.width = p + '%'; const b2 = el('span', 'pf-acc-kr'); b2.style.width = 100 - p + '%';
    bar.appendChild(b1); bar.appendChild(b2); top.appendChild(bar);
    const lg = el('div', 'pf-acclegend');
    lg.appendChild(el('span', 'pf-lg-us', `미국 · Robinhood ${p}%`)); lg.appendChild(el('span', 'pf-lg-kr', `한국 · 키움 ${100 - p}%`));
    top.appendChild(lg);
  }
  if (a.conflicts.length) top.appendChild(el('p', 'pf-warn', `⚠ 정정 충돌 ${a.conflicts.length}건 — 같은 환전 기록을 두 번 고쳐 계산에서 뺐습니다. 한국 칸의 환전 기록에서 틀린 쪽을 취소하세요.`));
  root.appendChild(top);

  // 2) 두 계좌 칸
  const grid = el('div', 'pf-accgrid');
  grid.appendChild(card('미국 · Robinhood', 'pf-acc-us', a.rh, [
    stat('주식 수익률', a.rh.twr == null ? '—' : pct(a.rh.twr), a.rh.twr),
    stat('보유 종목', `${a.rh.rows.length}개`),
  ], null, a.hasCash ? `주식 ${usd(a.rh.value - a.rh.cash)} · 현금 ${usd(a.rh.cash)}` : '현금 모름(올린 보유에 현금 줄 없음)'));
  const k = a.kw.krw;
  const box = el('div', 'pf-accbox');
  const line = (l, v, cls) => { const d = el('div', 'pf-accline'); d.appendChild(el('span', null, l)); d.appendChild(el('strong', cls || null, v)); box.appendChild(d); };
  line('내가 바꾼 평균 환율', rate(k?.avgRate ?? null));
  line(`오늘 환율${a.fx ? '(' + md(a.fx.bar || a.fx.from) + ' 봉)' : ''}`, rate(a.fx?.rate ?? null));
  const krwTxt = k?.krwTwr == null && k?.pnlKrw == null ? '—' : [k.krwTwr == null ? null : pct(k.krwTwr), k.pnlKrw == null ? null : (k.pnlKrw >= 0 ? '+' : '−') + won(Math.abs(k.pnlKrw)).slice(0)].filter(Boolean).join(' · ');
  line('원화로 보면', krwTxt, k?.pnlKrw == null ? null : k.pnlKrw >= 0 ? 'pf-up' : 'pf-down');
  const kwSub = (a.fx ? won(a.kw.value * a.fx.rate) + ' · ' : '') + `주식 ${usd(a.kw.value - a.kw.cash)} · 달러 현금 ${usd(a.kw.cash)}`;
  const kc = card('한국 · 키움', 'pf-acc-kr', a.kw, [
    stat('주식 수익률', a.kw.twr == null ? '—' : pct(a.kw.twr), a.kw.twr, a.kw.started ? md(a.kw.started) + '부터' : null),
    stat('환율 수익률', k?.fxReturn == null ? '—' : pct(k.fxReturn), k?.fxReturn, null, 'pf-accstat-fx'),
  ], box, kwSub);
  kc.appendChild(fxSection(a, handlers));
  grid.appendChild(kc);
  root.appendChild(grid);
  root.appendChild(el('p', 'pf-note', '환율 수익률 = 오늘 환율 ÷ 내가 바꾼 평균 환율 − 1(매일 환율로 다시 계산, 평균 환율에는 환전 수수료가 들어 있음). 원화로 보면 = 키움 평가액을 그날 환율로 바꾼 원화 수익률과, 지금 원화 가치 + 역환전 받은 원화 − 환전에 쓴 원화. 환율은 Yahoo 원/달러 일봉(평가일 전날까지 완성된 봉).'));
}

function stat(label, value, num, sub, cls) {
  const d = el('div', 'pf-accstat' + (cls ? ' ' + cls : ''));
  d.appendChild(el('span', null, label));
  d.appendChild(el('strong', num == null ? null : num >= 0 ? 'pf-up' : 'pf-down', value));
  if (sub) d.appendChild(el('small', null, sub));
  return d;
}

function card(title, dotCls, acct, stats, box, sub) {
  const c = el('section', 'pf-panel pf-acccard');
  const h = el('h2', 'pf-h2s'); const dot = el('i', 'pf-accdot ' + dotCls); dot.setAttribute('aria-hidden', 'true'); h.appendChild(dot); h.appendChild(document.createTextNode(title)); c.appendChild(h);
  c.appendChild(el('div', 'pf-accval', usd(acct.value)));
  c.appendChild(el('div', 'pf-s', sub));
  if (acct.missing?.length) c.appendChild(el('p', 'pf-warn', `가격 없음 ${acct.missing.join(', ')} — 평가액에서 빠진 부분합입니다.`));
  const st = el('div', 'pf-accstats'); stats.forEach((x) => st.appendChild(x)); c.appendChild(st);
  if (box) c.appendChild(box);
  const list = el('div', 'pf-acclist');
  if (!acct.rows.length) list.appendChild(el('p', 'pf-note', '보유 종목 없음'));
  for (const x of acct.rows) {
    const r = el('div', 'pf-accitem');
    const n = el('span'); n.appendChild(el('strong', null, x.ticker)); n.appendChild(el('small', null, ` ${Math.round(x.qty * 1e4) / 1e4}주`)); r.appendChild(n);
    const v = el('span', null, x.value == null ? '가격 없음' : usd(x.value) + ' ');
    if (x.vsAvg != null) v.appendChild(el('b', x.vsAvg >= 0 ? 'pf-up' : 'pf-down', pct(x.vsAvg)));
    r.appendChild(v); list.appendChild(r);
  }
  c.appendChild(list);
  return c;
}

// 환전 기록: 버튼 두 개(보기 · 기록). 기록 폼 = 종류(환전·역환전·배당·이자) · 날짜 · 원화 · 달러. 몫 달은 저장할 때 정해 root에 고정(설계 1절)
function fxSection(a, handlers) {
  const wrap = el('div', 'pf-accfx');
  const btns = el('div', 'pf-row');
  if (a.conflicts.length) showFx = true;
  const view = el('button', 'pf-btn pf-btn-quiet', showFx ? '환전 기록 접기' : `환전 기록 ${a.events.length}건 보기`); view.type = 'button';
  const add = el('button', 'pf-btn pf-btn-dark', '＋ 환전 기록'); add.type = 'button';
  btns.appendChild(view); btns.appendChild(add); wrap.appendChild(btns);
  const formBox = el('div', 'pf-accform'); formBox.hidden = true;
  const listBox = el('div', 'pf-accfxlist'); listBox.hidden = !showFx;
  wrap.appendChild(formBox); wrap.appendChild(listBox);
  view.addEventListener('click', () => { showFx = !showFx; listBox.hidden = !showFx; view.textContent = showFx ? '환전 기록 접기' : `환전 기록 ${a.events.length}건 보기`; });
  let editing = null;   // 고치는 중인 사건 {id, root}
  const f = el('div', 'pf-form');
  const field = (lab, input) => { const l = el('label', 'pf-field'); l.appendChild(el('span', null, lab)); l.appendChild(input); f.appendChild(l); return input; };
  const kind = field('종류', el('select'));
  for (const [v, t] of [['fx', '환전(원화 → 달러)'], ['fxOut', '역환전(달러 → 원화)'], ['income', '배당·이자(달러)']]) { const o = el('option', null, t); o.value = v; kind.appendChild(o); }
  const date = field('날짜', el('input')); date.type = 'date'; date.value = a.today; date.max = a.today;
  const krw = field('원화', el('input')); krw.type = 'number'; krw.min = '0'; krw.step = '1'; krw.placeholder = '₩';
  const usdIn = field('달러', el('input')); usdIn.type = 'number'; usdIn.min = '0'; usdIn.step = '0.01'; usdIn.placeholder = '$';
  const sync = () => { krw.closest('label').hidden = kind.value === 'income'; };
  kind.addEventListener('change', sync); sync();
  const save = el('button', 'pf-btn', '기록'); save.type = 'button';
  const msg = msgLine();
  f.appendChild(save); f.appendChild(msg); formBox.appendChild(f);
  const hint = el('p', 'pf-note', '환전한 달러는 그달 몫 입금으로 카드 매수 한도에 들어갑니다(원칙 3). 반영일은 기록한 다음 장 시작입니다.');
  formBox.appendChild(hint);
  const reset = () => { editing = null; kind.disabled = false; kind.value = 'fx'; date.value = a.today; usdIn.value = ''; krw.value = ''; sync(); save.textContent = '기록'; };
  add.addEventListener('click', () => { reset(); formBox.hidden = !formBox.hidden; });   // 고치던 값이 남아 같은 환전을 두 번 적지 않게(dr)
  twoStep(save, msg, '이대로 기록합니다. 맞으면 한 번 더 누르세요.', async () => {
    const u = Math.round(Number(usdIn.value) * 100) / 100, w = Math.round(Number(krw.value));
    if (!(u > 0)) throw new Error('달러를 0보다 크게 넣으세요.');
    if (kind.value !== 'income' && !(w > 0)) throw new Error('원화를 0보다 크게 넣으세요.');
    if (!date.value || date.value > a.today) throw new Error('날짜를 오늘이나 그 전으로 넣으세요.');
    const ev = { kind: kind.value, usd: u, date: date.value, account: 'kw', ...(kind.value !== 'income' ? { krw: w } : {}) };
    if (editing && ev.kind !== editing.kind) throw new Error('정정은 같은 종류만 — 종류를 바꾸려면 취소하고 새로 기록하세요.');
    if (editing) await handlers.ledgerCorrect(editing.id, editing.root, ev);   // 정정: 반영일·몫 달은 root의 것
    else {
      const dEff = depositTiming(new Date().toISOString()).day;
      if (kind.value !== 'income' && dEff) ev.forMonth = a.autoMonth(dEff);
      await handlers.ledgerAdd(ev);
    }
  }, f);
  // 목록
  const k = a.kw.krw;
  if (k && (k.krwIn || k.krwOut)) listBox.appendChild(el('p', 'pf-note', `환전에 쓴 원화 ${won(k.krwIn)} · 받은 달러 ${usd(k.usdIn)}` + (k.krwOut ? ` · 역환전 받은 원화 ${won(k.krwOut)}` : '') + (k.valueKrw != null ? ` · 지금 원화 가치 ${won(k.valueKrw)}` : '')));
  // 정정 충돌: 살아 있는 기록을 모두 보여 틀린 쪽을 취소하게(계산에서는 빠져 있음, dr)
  for (const c of a.conflicts) for (const x of c.ids) {
    const r = el('div', 'pf-accfxrow pf-warn');
    r.appendChild(el('span', null, `충돌 · ${md(x.date)} ${KIND[x.kind] || x.kind}` + (x.krw ? ` ${won(x.krw)}` : '')));
    r.appendChild(el('strong', null, usd(x.usd)));
    const del = el('button', 'pf-btn pf-btn-quiet', '이것 취소'); del.type = 'button';
    const m2 = msgLine();
    twoStep(del, m2, '이 기록을 취소합니다. 맞으면 한 번 더 누르세요.', async () => { await handlers.ledgerCancel(x.id); }, r);
    r.appendChild(del); r.appendChild(m2); listBox.appendChild(r);
  }
  if (!a.events.length && !a.conflicts.length) listBox.appendChild(el('p', 'pf-note', '아직 기록이 없습니다.'));
  for (const e of [...a.events].reverse()) {
    const r = el('div', 'pf-accfxrow');
    r.appendChild(el('span', null, `${md(e.date)} · ${KIND[e.kind]}` + (e.kind === 'income' ? '' : ` ${won(e.krw)}`)));
    r.appendChild(el('strong', null, (e.kind === 'fxOut' ? '−' : '') + usd(e.usd)));
    if (e.kind !== 'income' && e.krw && e.usd) r.appendChild(el('small', null, rate(e.krw / e.usd)));
    const fix = el('button', 'pf-btn pf-btn-quiet', '고치기'); fix.type = 'button';
    fix.addEventListener('click', () => { editing = { id: e.id, root: e.root, kind: e.kind }; kind.value = e.kind; kind.disabled = true; date.value = e.date; usdIn.value = String(e.usd); krw.value = e.krw ? String(e.krw) : ''; sync(); formBox.hidden = false; save.textContent = '고친 값으로 기록'; });
    const del = el('button', 'pf-btn pf-btn-quiet', '취소'); del.type = 'button';
    const m2 = msgLine();
    twoStep(del, m2, '이 기록을 취소합니다(원본은 남음). 맞으면 한 번 더 누르세요.', async () => { await handlers.ledgerCancel(e.id); }, r);
    r.appendChild(fix); r.appendChild(del); r.appendChild(m2);
    listBox.appendChild(r);
  }
  return wrap;
}
