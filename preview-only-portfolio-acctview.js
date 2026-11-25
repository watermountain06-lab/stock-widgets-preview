// preview 전용 Portfolio 탭 — "내 계좌" 하위 탭(2026-10-28 사용자 결정 C안: 위는 합계·비중 막대, 아래는 미국·한국 칸 나란히,
// 한국 칸은 단순하게 — 주식 수익률·환율 수익률 두 칸과 평균/오늘 환율·원화로 보면 한 상자, 환전 기록은 버튼 안). 라이브로 옮기지 않는다.
// 2026-11-20 화면 정리(사용자: 표가 딱딱함 → 큰 숫자·카드): 칸마다 큰 금액과 수익률, 종목 비중 막대와 한 줄 설명, 종목 줄, 한국 칸 아래 환율 상자. 정보는 그대로.
// 숫자는 home.js accountsState가 만든다(한눈에 탭과 같은 계산). 장부 쓰기는 handlers.ledgerAdd·ledgerCancel·ledgerCorrect.
import { el, usd, pct, twoStep, msgLine } from './preview-only-portfolio-strategy.js?v=27';
import { depositTiming } from './preview-only-portfolio-engine.js?v=14';

const won = (v) => (v == null ? '—' : '₩' + Math.round(v).toLocaleString('en-US'));
const rate = (v) => (v == null ? '—' : '₩' + v.toLocaleString('en-US', { minimumFractionDigits: 1, maximumFractionDigits: 1 }));
const md = (d) => (d ? `${+d.slice(5, 7)}/${d.slice(8, 10)}` : '');
const KIND = { fx: '환전', fxOut: '역환전', income: '배당·이자' };
let showFx = false;   // 환전 기록 펼침(다시 그려도 유지)

// 비중 막대 아래 한 줄(자동 문구, 2026-11-20): 늘 참인 말만 쓴다. parts = [{ label, share(0~1), cash? }] — 현금 포함, 순서 무관.
// 가장 큰 종목과 그다음 두 종목(1% 이상만)을 적는다. 현금이 가장 큰 종목보다 크면 맨 앞에, 그렇지 않고 10% 이상이면 맨 뒤에 붙인다.
// 종목이 없으면 현금만, 아무것도 없으면 ''.
export function mixCaption(parts) {
  const pc = (x) => (x.share > 0 && x.share < 0.01 ? '<1' : Math.round(x.share * 100)) + '%';
  const st = parts.filter((x) => !x.cash && x.share > 0).sort((a, b) => b.share - a.share || (a.label < b.label ? -1 : 1));
  const cash = parts.find((x) => x.cash && x.share > 0);
  if (!st.length) return cash ? `현금 ${pc(cash)}` : '';
  const next = st.slice(1, 3).filter((x) => x.share >= 0.01);
  const stocks = `가장 큰 종목 ${st[0].label} ${pc(st[0])}` + (next.length ? ` · 다음 ${next.map((x) => `${x.label} ${pc(x)}`).join(', ')}` : '');
  if (cash && cash.share > st[0].share) return `현금 ${pc(cash)} · ${stocks}`;
  return stocks + (cash && cash.share >= 0.1 ? ` · 현금 ${pc(cash)}` : '');
}

// 큰 숫자 한 줄: 왼쪽(작은 제목 · 큰 금액 · 설명) + 오른쪽(작은 제목 · 큰 수익률)
function head(k1, big, sub, k2, ret) {
  const h = el('div', 'pf-ac2head');
  const l = el('div', 'pf-ac2main');
  l.appendChild(el('span', 'pf-ac2k', k1)); l.appendChild(el('strong', 'pf-ac2big', big)); if (sub) l.appendChild(el('span', 'pf-s', sub));
  h.appendChild(l);
  const r = el('div', 'pf-ac2ret');
  r.appendChild(el('span', 'pf-ac2k', k2));
  r.appendChild(el('strong', 'pf-ac2big' + (ret == null ? '' : ret >= 0 ? ' pf-up' : ' pf-down'), ret == null ? '—' : pct(ret)));
  h.appendChild(r);
  return h;
}

export function renderAccounts(root, a, handlers) {
  root.textContent = '';
  const fxDay = a.fx ? md(a.fx.bar || a.fx.from) : '';
  // 1) 합계: 큰 숫자 + 수익률, 그 아래 두 계좌 비중 막대(2026-11-20 시안 — 표 대신 큰 숫자·카드)
  const top = el('section', 'pf-panel pf-acctop');
  const th = head('두 계좌 합계', usd(a.total.value),
    a.fx ? `${won(a.total.value * a.fx.rate)} · 적용 환율 ${rate(a.fx.rate)} · ${fxDay}${a.fx.carried ? '(직전 값)' : ''}` : '환율 없음',
    a.from ? md(a.from) + '부터' : '합계 수익률', a.total.twr);
  top.appendChild(th);
  const tot = a.rh.value + a.kw.value;
  if (tot > 0 && a.kw.used) {
    const bar = el('div', 'pf-acctbar'); bar.setAttribute('role', 'img');
    const p = Math.round((a.rh.value / tot) * 100);
    bar.setAttribute('aria-label', `미국 계좌 ${p}%, 한국 계좌 ${100 - p}%`);
    const b1 = el('span', 'pf-acc-us'); b1.style.width = p + '%'; const b2 = el('span', 'pf-acc-kr'); b2.style.width = 100 - p + '%';
    bar.appendChild(b1); bar.appendChild(b2); top.appendChild(bar);
    const lg = el('div', 'pf-acclegend');
    lg.appendChild(el('span', 'pf-lg-us', `미국 계좌 ${p}% · ${usd(a.rh.value)}`)); lg.appendChild(el('span', 'pf-lg-kr', `한국 계좌 ${100 - p}% · ${usd(a.kw.value)}`));
    top.appendChild(lg);
  }
  if (a.conflicts.length) top.appendChild(el('p', 'pf-warn', `⚠ 정정 충돌 ${a.conflicts.length}건 — 같은 환전 기록을 두 번 고쳐 계산에서 뺐습니다. 한국 칸의 환전 기록에서 틀린 쪽을 취소하세요.`));
  root.appendChild(top);

  // 2) 두 계좌 칸
  const grid = el('div', 'pf-accgrid');
  grid.appendChild(card('미국 계좌', 'us', a.rh, a.hasCash ? `주식 ${usd(a.rh.value - a.rh.cash)} · 현금 ${usd(a.rh.cash)}` : '현금 모름(올린 보유에 현금 줄 없음)', null));
  const k = a.kw.krw;
  const kwSub = (a.fx ? won(a.kw.value * a.fx.rate) + ' · ' : '') + `주식 ${usd(a.kw.value - a.kw.cash)} · 달러 현금 ${usd(a.kw.cash)}`;
  const kc = card('한국 계좌', 'kr', a.kw, kwSub, a.kw.started ? md(a.kw.started) + '부터' : null);
  // 환율 상자: 환율로 생긴 차이(큰 숫자) · 평균 환전 환율 → 적용 환율 · 원화로 보면 · 환전 기록 버튼
  const fxb = el('div', 'pf-ac2fx');
  const fh = el('div', 'pf-ac2fxhead');
  const fl = el('div', 'pf-ac2main');
  fl.appendChild(el('strong', null, '환율로 생긴 차이'));
  fl.appendChild(el('span', 'pf-s', `평균 환전 환율 ${rate(k?.avgRate ?? null)} → 적용 환율 ${rate(a.fx?.rate ?? null)}` + (fxDay ? ` (${fxDay})` : '')));
  fh.appendChild(fl);
  fh.appendChild(el('strong', 'pf-ac2fxv' + (k?.fxReturn == null ? '' : k.fxReturn >= 0 ? ' pf-up' : ' pf-down'), k?.fxReturn == null ? '—' : pct(k.fxReturn)));
  fxb.appendChild(fh);
  const kl = el('div', 'pf-ac2krw');
  kl.appendChild(el('span', null, '원화로 보면 '));
  const krwTxt = k?.krwTwr == null && k?.pnlKrw == null ? '—' : [k.krwTwr == null ? null : pct(k.krwTwr), k.pnlKrw == null ? null : (k.pnlKrw >= 0 ? '+' : '−') + won(Math.abs(k.pnlKrw))].filter(Boolean).join(' · ');
  kl.appendChild(el('strong', k?.pnlKrw == null ? null : k.pnlKrw >= 0 ? 'pf-up' : 'pf-down', krwTxt));
  kl.appendChild(el('small', null, ' (이 계좌 전체를 원화로 바꿔 본 수익률)'));
  fxb.appendChild(kl);
  fxb.appendChild(fxSection(a, handlers));
  kc.appendChild(fxb);
  grid.appendChild(kc);
  root.appendChild(grid);
  // 계산 방법은 접어 둔다(글 최소) — 내용은 예전 안내문 그대로
  const how = el('details', 'pf-ac2how');
  how.appendChild(el('summary', null, '계산 방법'));
  how.appendChild(el('p', 'pf-note', '환율로 생긴 차이 = 오늘 환율 ÷ 내가 바꾼 평균 환율 − 1(매일 환율로 다시 계산, 평균 환율에는 환전 수수료가 들어 있음). 원화로 보면 = 한국 계좌 평가액을 그날 환율로 바꾼 원화 수익률과, 지금 원화 가치 + 역환전 받은 원화 − 환전에 쓴 원화. 환율은 Yahoo 원/달러 일봉(평가일 전날까지 완성된 봉).'));
  root.appendChild(how);
}

// 계좌 칸: 큰 숫자 한 줄 → 비중 막대와 한 줄 설명 → 종목 줄(점 · 티커와 수량·계좌 안 비중 · 평가액 · 평균 단가 대비)
function card(title, tone, acct, sub, since) {
  const c = el('section', 'pf-panel pf-acccard pf-ac2-' + tone);
  c.appendChild(head([title, `${acct.rows.length}종목`, since].filter(Boolean).join(' · '), usd(acct.value), sub, '주식 수익률', acct.twr));
  if (acct.missing?.length) c.appendChild(el('p', 'pf-warn', `가격 없음 ${acct.missing.join(', ')} — 평가액에서 빠진 부분합입니다.`));
  const known = acct.rows.filter((x) => x.value > 0);
  const total = acct.value;
  const SHADE = [1, 0.8, 0.62, 0.46, 0.34, 0.25];   // 큰 종목일수록 진하게, 여섯째부터는 같은 옅은 색 — 투명도가 아니라 --sh로 넘겨 CSS가 화면 밝기에 맞는 색과 섞는다(어두운 화면에서 묻히지 않게)
  const shade = (i) => SHADE[Math.min(i, SHADE.length - 1)];
  const mixOk = total > 0 && !(acct.cash < 0);   // 현금이 음수면 종목 비중 합이 100%를 넘는다 — 막대와 비중 글을 그리지 않는다
  if (mixOk && (known.length || acct.cash > 0)) {
    const mix = el('div', 'pf-ac2mix');
    const bar = el('div', 'pf-ac2bar'); bar.setAttribute('role', 'img');
    const parts = known.map((x) => ({ label: x.ticker, share: x.value / total }));
    if (acct.cash > 0) parts.push({ label: '현금', share: acct.cash / total, cash: true });
    const pcT = (v) => (v / total < 0.01 ? '<1' : Math.round((v / total) * 100)) + '%';
    known.forEach((x, i) => { const b = el('span'); b.style.width = (x.value / total) * 100 + '%'; b.style.setProperty('--sh', shade(i)); b.title = `${x.ticker} ${pcT(x.value)}`; bar.appendChild(b); });
    if (acct.cash > 0) { const b = el('span', 'pf-ac2cash'); b.style.width = (acct.cash / total) * 100 + '%'; b.title = `현금 ${pcT(acct.cash)}`; bar.appendChild(b); }
    const cap = acct.missing?.length ? '' : mixCaption(parts);   // 가격 없는 종목이 있으면 비중이 부분합 기준이라 문장을 쓰지 않는다
    // 막대 이름에는 모든 구간을 적는다(한 줄 설명은 큰 것만) — 가격 없는 종목이 있으면 부분합 기준임을 밝힌다
    bar.setAttribute('aria-label', `${title} 비중` + (acct.missing?.length ? '(가격 있는 종목 기준)' : '') + ': ' + parts.map((x) => `${x.label} ${pcT(x.share * total)}`).join(', '));
    mix.appendChild(bar);
    if (cap) mix.appendChild(el('span', 'pf-s', cap));
    c.appendChild(mix);
  }
  const list = el('div', 'pf-ac2list');
  if (!acct.rows.length) list.appendChild(el('p', 'pf-note', '보유 종목 없음'));
  let ki = 0;
  for (const x of acct.rows) {
    const r = el('div', 'pf-ac2row');
    const dot = el('i', 'pf-ac2dot'); dot.setAttribute('aria-hidden', 'true'); if (x.value > 0) dot.style.setProperty('--sh', shade(ki++)); else dot.classList.add('pf-ac2none'); r.appendChild(dot);
    const n = el('div', 'pf-ac2name'); n.appendChild(el('strong', null, x.ticker));
    n.appendChild(el('small', null, `${Math.round(x.qty * 1e4) / 1e4}주` + (x.value > 0 && mixOk ? ` · 계좌의 ${x.value / total < 0.01 ? '<1' : Math.round((x.value / total) * 100)}%` : '')));
    r.appendChild(n);
    r.appendChild(el('strong', 'pf-ac2val', x.value == null ? '가격 없음' : usd(x.value)));
    if (x.vsAvg != null) { const pl = el('span', 'pf-ac2pill ' + (x.vsAvg >= 0 ? 'pf-ac2pos' : 'pf-ac2neg'), pct(x.vsAvg)); pl.title = '평균 단가 대비'; r.appendChild(pl); } else r.appendChild(el('span'));
    list.appendChild(r);
  }
  c.appendChild(list);
  return c;
}

// 환전 기록: 버튼 두 개(보기 · 기록). 기록 폼 = 종류(환전·역환전·배당·이자) · 날짜 · 원화 · 달러. 몫 달은 저장할 때 정해 root에 고정(설계 1절)
function fxSection(a, handlers) {
  const wrap = el('div', 'pf-accfx');
  const btns = el('div', 'pf-row');
  if (a.conflicts.length) showFx = true;
  const view = el('button', 'pf-btn pf-btn-quiet', showFx ? '환전 기록 접기' : `환전 기록 ${a.events.length}건`); view.type = 'button'; view.setAttribute('aria-expanded', String(showFx));
  const add = el('button', 'pf-btn pf-btn-quiet pf-ac2add', '+ 환전 기록'); add.type = 'button';
  btns.appendChild(view); btns.appendChild(add); wrap.appendChild(btns);
  const formBox = el('div', 'pf-accform'); formBox.hidden = true;
  const listBox = el('div', 'pf-accfxlist'); listBox.hidden = !showFx;
  wrap.appendChild(formBox); wrap.appendChild(listBox);
  view.addEventListener('click', () => { showFx = !showFx; listBox.hidden = !showFx; view.setAttribute('aria-expanded', String(showFx)); view.textContent = showFx ? '환전 기록 접기' : `환전 기록 ${a.events.length}건`; });
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
