// preview 전용 Portfolio 탭(2026-10-19). 라이브로 옮기지 않는다 — pipeline/site_ui/UI_DIFF.md 1절 portfolio.
//
// 나만 쓰기: Google 로그인(Firebase Auth) 뒤 Firestore `users/{uid}/portfolio/main` 문서 하나를 읽는다.
// 누가 읽을 수 있는지는 Firestore 규칙(pipeline/portfolio/firestore.rules)이 정한다 — 이 파일은 보호하지 않는다.
// 내 데이터는 GitHub 저장소에 올라가지 않는다(저장소에는 가짜 sample.json만). 로그인은 이 탭에서만 유지한다(사용자 결정):
// sessionStorage 기반이라 새 탭에서는 다시 묻는다. 브라우저의 '닫은 탭 다시 열기'·탭 복제는 로그인을 되살릴 수 있다.
// 위 구역(원칙·실제 자산·관심 종목·모의 운용 기록)은 올린 값만 보여 준다. 전략 비교 구역(2026-10-20)은 따로 저장하는 묶음 문서
// users/{uid}/portfolio/strategy_N 과 공개 일별 기록으로 계산한다 — preview-only-portfolio-strategy.js, 설계 STRATEGY_DESIGN.md.
import { initializeApp } from 'https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js';
import { getAuth, GoogleAuthProvider, signInWithPopup, signOut, onAuthStateChanged, setPersistence, browserSessionPersistence }
  from 'https://www.gstatic.com/firebasejs/10.12.2/firebase-auth.js';
import { getFirestore, doc, getDoc, setDoc, updateDoc, deleteField, serverTimestamp }
  from 'https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js';
import { toEngineInput } from './preview-only-portfolio-strategy.js?v=15';
import { renderTabs, etDate } from './preview-only-portfolio-home.js?v=23';
import { parseCSV, importTable } from './preview-only-portfolio-import.js?v=1';
import { replay, ENGINE_VERSION } from './preview-only-portfolio-engine.js?v=2';
import { attachActual } from './preview-only-portfolio-actual.js?v=7';
import { firebaseConfig } from './preview-only-portfolio-config.js?v=2';

const $ = (id) => document.getElementById(id);

// ---- 그리기: 모든 글자는 textContent로 넣는다 ----
function el(tag, cls, text) {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (text != null && text !== '') e.textContent = text;
  return e;
}
const num = (v) => typeof v === 'number' ? v.toLocaleString('ko-KR', { maximumFractionDigits: 4 }) : (v == null ? '' : String(v));
function table(t, heads, rows) {
  t.textContent = '';
  const tr = el('tr');
  heads.forEach((h) => tr.appendChild(el('th', null, h)));
  const thead = el('thead'); thead.appendChild(tr); t.appendChild(thead);
  const tbody = el('tbody');
  if (!rows.length) {
    const r0 = el('tr'), td = el('td', 'pf-empty', '아직 없습니다.');
    td.colSpan = heads.length; r0.appendChild(td); tbody.appendChild(r0);
  }
  rows.forEach((cells) => {
    const r = el('tr');
    cells.forEach((c) => r.appendChild(el('td', typeof c === 'number' ? 'pf-num' : null, num(c))));
    tbody.appendChild(r);
  });
  t.appendChild(tbody);
}

function render(d) {
  $('pf-sample').hidden = !d.sample;
  $('pf-updated').textContent = d.updated ? '갱신 ' + d.updated : '';

  const pr = $('pf-principles'); pr.textContent = '';
  const ol = el('ol', 'pf-principles');
  (d.principles || []).forEach((p) => {
    const li = el('li'); li.appendChild(el('strong', null, p.title)); li.appendChild(el('p', null, p.body)); ol.appendChild(li);
  });
  pr.appendChild((d.principles || []).length ? ol : el('p', 'pf-empty', '아직 없습니다.'));

  const h = d.holdings || {};
  $('pf-holdings-asof').textContent = h.asOf ? h.asOf + ' 기준' : '';
  $('pf-holdings-note').textContent = h.note || '';
  table($('pf-holdings'), ['종목', '티커', '수량', '평균 단가', '통화', '계좌'],
    (h.rows || []).map((r) => [r.name, r.ticker, r.qty, r.avgPrice, r.currency, r.account]));

  table($('pf-watch'), ['종목', '티커', '관심 이유', '검토 조건'],
    (d.watchlist || []).map((w) => [w.name, w.ticker, w.reason, w.trigger]));

  const sc = $('pf-scenarios'); sc.textContent = '';
  (d.scenarios || []).forEach((s) => {
    const box = el('article', 'pf-scenario');
    const head = el('h3', null, s.name);
    if (s.start) head.appendChild(el('small', null, s.start + ' 시작'));
    box.appendChild(head);
    box.appendChild(el('p', 'pf-note', s.rule));
    const wrap = el('div', 'pf-scroll'), t = el('table', 'pf-table');
    table(t, ['날짜', '거래', '티커', '수량', '가격', '메모'],
      (s.entries || []).map((x) => [x.date, x.action, x.ticker, x.qty, x.price, x.note]));
    wrap.appendChild(t); box.appendChild(wrap); sc.appendChild(box);
  });
  if (!(d.scenarios || []).length) sc.appendChild(el('p', 'pf-empty', '아직 없습니다.'));
}

// 올릴 데이터의 모양 검사 — 저장 전에 한다. 틀리면 저장하지 않는다.
const MAX_BYTES = 900 * 1024; // Firestore 문서 한도 1 MiB보다 작게
function validate(d) {
  const isObj = (x) => x && typeof x === 'object' && !Array.isArray(x);
  const arr = (x, name) => { if (x != null && !Array.isArray(x)) throw new Error(name + '은(는) 목록이어야 합니다.'); return x || []; };
  if (!isObj(d)) throw new Error('맨 바깥은 { }여야 합니다.');
  // 칸 값은 글자·숫자·참거짓·빈 값만 받는다({ }나 [ ]가 칸에 들어가면 화면에 [object Object]로 나온다)
  const leaf = (o, where) => Object.keys(o).forEach((k) => {
    const v = o[k];
    if (!(v == null || typeof v === 'string' || typeof v === 'boolean' || (typeof v === 'number' && isFinite(v)))) throw new Error(where + '.' + k + ' 값이 글자·숫자가 아닙니다.');
  });
  arr(d.principles, 'principles').forEach((x) => { if (!isObj(x)) throw new Error('principles 항목이 { }가 아닙니다.'); leaf(x, 'principles'); });
  if (d.holdings != null && !isObj(d.holdings)) throw new Error('holdings는 { }여야 합니다.');
  arr(d.holdings && d.holdings.rows, 'holdings.rows').forEach((x) => { if (!isObj(x)) throw new Error('holdings.rows 항목이 { }가 아닙니다.'); leaf(x, 'holdings.rows'); });
  arr(d.watchlist, 'watchlist').forEach((x) => { if (!isObj(x)) throw new Error('watchlist 항목이 { }가 아닙니다.'); leaf(x, 'watchlist'); });
  arr(d.scenarios, 'scenarios').forEach((x) => {
    if (!isObj(x)) throw new Error('scenarios 항목이 { }가 아닙니다.');
    const { entries, ...rest } = x;
    leaf(rest, 'scenarios');
    arr(entries, 'scenarios.entries').forEach((y) => { if (!isObj(y)) throw new Error('scenarios.entries 항목이 { }가 아닙니다.'); leaf(y, 'scenarios.entries'); });
  });
  if (d.sample != null && typeof d.sample !== 'boolean') throw new Error('sample 값은 true/false여야 합니다.');
  if (d.updated != null && typeof d.updated !== 'string') throw new Error('updated 값은 글자(날짜)여야 합니다.');
  if (d.holdings) { const { rows, ...rest } = d.holdings; leaf(rest, 'holdings'); }
  return d;
}

function show(state, msg) {
  // state: 'out' 로그인 전 · 'in' 내용 보임. 'out'이면 화면에 남은 내용·계정을 모두 지운다.
  $('pf-lock').hidden = state === 'in';
  $('pf-body').hidden = state !== 'in';
  if (state !== 'in') {
    ['pf-principles', 'pf-holdings', 'pf-watch', 'pf-scenarios', 'pf-strategy', 'pf-home', 'pf-manage', 'pf-account', 'pf-updated', 'pf-holdings-asof', 'pf-holdings-note', 'pf-upload-msg']
      .forEach((id) => { $(id).textContent = ''; });
    $('pf-sample').hidden = true;
    pending = null;
    $('pf-upload-confirm').hidden = true;
  }
  $('pf-msg').textContent = msg || '';
}

// 덮어쓰기 확인은 화면 안에서 한다(브라우저 확인 창을 쓰지 않는다): 파일을 고르면 무엇을 바꿀지 보여 주고
// "이대로 올리기"를 눌러야 저장한다(2026-10-21 사용자 요청 — 같은 파일을 두 번 고르던 방식에서 바꿈).
let pending = null;   // { save() } — 확인을 기다리는 올리기 하나
function askConfirm(what, save) {
  pending = { save };
  $('pf-upload-msg').textContent = what + ' 맞으면 "이대로 올리기"를 누르세요.';
  $('pf-upload-confirm').hidden = false;
}
function clearConfirm() { pending = null; $('pf-upload-confirm').hidden = true; }

// Excel(.xlsx·.xls)은 고를 때만 SheetJS를 cdnjs에서 불러와 첫 시트를 CSV 글자로 바꾼다(무결성 해시로 고정)
const XLSX_SRC = 'https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js';
const XLSX_SRI = 'sha384-vtjasyidUo0kW94K5MXDXntzOJpQgBKXmE7e2Ga4LG0skTTLeBi97eFAXsqewJjw';
let xlsxLoading = null;
function loadXLSX() {
  if (window.XLSX) return Promise.resolve(window.XLSX);
  xlsxLoading ??= new Promise((resolve, reject) => {
    const sc = document.createElement('script');
    sc.src = XLSX_SRC; sc.integrity = XLSX_SRI; sc.crossOrigin = 'anonymous';
    sc.onload = () => (window.XLSX ? resolve(window.XLSX) : reject(new Error('Excel 읽기 도구가 비었습니다.')));
    sc.onerror = () => { xlsxLoading = null; reject(new Error('Excel 읽기 도구를 불러오지 못했습니다(네트워크).')); };
    document.head.appendChild(sc);
  });
  return xlsxLoading;
}
// 올린 파일 → 표 글자(CSV). JSON이면 null
async function fileToCSV(file) {
  const ext = (file.name.split('.').pop() || '').toLowerCase();
  if (ext === 'csv' || file.type === 'text/csv') return file.text();
  if (ext === 'xlsx' || ext === 'xls') {
    const X = await loadXLSX();
    const wb = X.read(new Uint8Array(await file.arrayBuffer()), { type: 'array' });
    const sh = wb.Sheets[wb.SheetNames[0]];
    if (!sh) throw new Error('첫 시트가 비었습니다.');
    return X.utils.sheet_to_csv(sh, { blankrows: false });
  }
  return null;
}
let currentMain = {};    // 지금 올라가 있는 원칙·보유·관심 종목 — CSV·Excel은 이 가운데 보유만 바꾼다
let refreshTabs = null;  // 올린 뒤 한눈에·기록·관리를 새 보유로 다시 그린다

if (!firebaseConfig.apiKey || !firebaseConfig.projectId || !firebaseConfig.authDomain || !firebaseConfig.appId) {
  show('out', '아직 설정 전입니다(pipeline/portfolio/SETUP.md).');
  $('pf-login').disabled = true;
} else {
  const app = initializeApp(firebaseConfig);
  const auth = getAuth(app);
  const db = getFirestore(app);
  const ref = (user) => doc(db, 'users', user.uid, 'portfolio', 'main');
  let gen = 0; // 로그인 상태가 바뀔 때마다 늘린다 — 늦게 끝난 옛 요청은 화면을 건드리지 않는다
  let quietOut = ''; // 다음 로그아웃 화면에 띄울 문구

  async function open(user, g) {
    $('pf-msg').textContent = '불러오는 중…';
    let snap;
    try {
      snap = await getDoc(ref(user));
    } catch (e) {
      if (g !== gen) return;
      if (e.code === 'permission-denied') {
        quietOut = '이 계정은 볼 수 없습니다.';
        try { await signOut(auth); } catch (_) { show('out', quietOut); }
      } else {
        quietOut = '불러오지 못했습니다(' + (e.code || e.message) + '). 다시 로그인해 보세요.';
        try { await signOut(auth); } catch (_) { show('out', quietOut); }
      }
      return;
    }
    if (g !== gen) return;
    show('in');
    $('pf-account').textContent = user.email || '';
    let main = {};
    if (!snap.exists()) { render({}); $('pf-updated').textContent = '아직 올린 데이터가 없습니다'; }
    else {
      try {
        const d = validate(JSON.parse(snap.data().json));
        render(d);
        main = d;
      } catch (e) {
        // 저장된 데이터가 깨져도 올리기 칸은 남겨 둔다 — 새 파일로 바꿔 복구한다
        render({});
        $('pf-upload-msg').textContent = '저장된 데이터를 읽지 못했습니다(' + e.message + '). 새 파일을 올려 바꾸세요.';
      }
    }
    currentMain = main;
    refreshTabs = (m) => { if (g === gen && auth.currentUser === user) loadAll(user, g, m); };
    loadAll(user, g, main);
  }

  // ---- 전략 비교 ----
  // 묶음 문서 users/{uid}/portfolio/strategy_1, _2, … — 마지막 번호가 지금 묶음이다. 끝낸 묶음 뒤에는 새 번호로 시작한다.
  // 보안 규칙(pipeline/portfolio/firestore.rules)은 나만 읽고 쓰기다. 값은 고치고 지울 수 있다(2026-10-20 사용자 결정).
  const sref = (user, n) => doc(db, 'users', user.uid, 'portfolio', 'strategy_' + n);
  let ledger = null;   // 공개 일별 기록 — 한 번 받으면 이 탭에서 다시 받지 않는다(기록은 고치지 않으므로)
  async function loadLedger() {
    if (ledger) return ledger;
    const base = 'site_data/strategy_ledger/';
    const res = await fetch(base + 'index.json', { cache: 'no-cache' });
    if (!res.ok) throw new Error('index');
    const { sessions } = await res.json();
    const recs = await Promise.all(sessions.map(async (d) => {
      const r = await fetch(base + d + '.json');
      if (!r.ok) throw new Error('record');
      return r.json();
    }));
    ledger = recs;
    return recs;
  }
  const iso = (v) => (v && typeof v.toDate === 'function' ? v.toDate().toISOString() : v ?? null);
  const plain = (data) => {
    const map = (m, f) => Object.fromEntries(Object.entries(m || {}).map(([k, v]) => [k, f(v)]));
    return {
      snapshot: { ...data.snapshot, createdAt: iso(data.snapshot && data.snapshot.createdAt) },
      deposits: map(data.deposits, (x) => ({ ...x, recordedAt: iso(x.recordedAt) })),
      scenarios: map(data.scenarios, (x) => ({ ...x, createdAt: iso(x.createdAt) })),
      closed: data.closed ? { ...data.closed, at: iso(data.closed.at) } : null,
    };
  };
  const newId = (p) => p + Date.now().toString(36) + Math.random().toString(36).slice(2, 6);
  const why = (e) => (e && e.code === 'permission-denied' ? '규칙이 막았습니다. 새로고침한 뒤 다시 해 보세요.' : '저장하지 못했습니다(' + ((e && (e.code || e.message)) || '알 수 없음') + ').');

  // 실제 매매 기록: users/{uid}/portfolio/trades 문서 하나(고치기·지우기 가능, 규칙 firestore.rules). 모의 운용 계산과는 따로다.
  const tref = (user) => doc(db, 'users', user.uid, 'portfolio', 'trades');

  async function loadAll(user, g, main) {
    ['pf-home', 'pf-strategy', 'pf-manage'].forEach((id) => { $(id).textContent = '불러오는 중…'; });
    let records = [], recordsError = false;
    try { records = await loadLedger(); } catch (_) { recordsError = true; }
    let n = 1, cur = null, closedCount = 0, trades = {}, tradesExist = false;
    const allDeposits = {};
    try {
      for (; n < 100; n++) {
        const s = await getDoc(sref(user, n));
        if (!s.exists()) break;
        cur = { no: n, data: s.data({ serverTimestamps: 'estimate' }) };
        if (cur.data.closed) closedCount++;
        // 실제로 넣은 돈은 묶음을 끝내도 사라지지 않는다 — 한눈에 내 자산은 모든 묶음의 입금을 본다(dr r2)
        for (const [k, v] of Object.entries(cur.data.deposits || {})) allDeposits['b' + n + ':' + k] = { ...v, recordedAt: iso(v.recordedAt), ...(v.cancels ? { cancels: 'b' + n + ':' + v.cancels } : {}) };
      }
      const ts = await getDoc(tref(user));
      if (ts.exists()) {
        tradesExist = true;
        const e = ts.data({ serverTimestamps: 'estimate' }).entries || {};
        trades = Object.fromEntries(Object.entries(e).map(([k, v]) => [k, { ...v, recordedAt: iso(v.recordedAt) }]));
      }
    } catch (e) {
      if (g === gen) ['pf-home', 'pf-strategy', 'pf-manage'].forEach((id) => { $(id).textContent = '불러오지 못했습니다(' + (e.code || e.message) + '). 규칙을 새로 게시했는지 확인하세요(SETUP.md 7절).'; });
      return;
    }
    if (g !== gen) return;
    const bundle = cur ? plain(cur.data) : null;
    const no = !cur ? 1 : cur.data.closed ? cur.no + 1 : cur.no;
    const ref = sref(user, no);
    const byId = (bundle && bundle.scenarios) || {};
    let result = null, calcError = null;
    if (bundle && !bundle.closed && records.length) {
      // 원칙 시나리오(숨김)를 같이 돌리고, 실제 매매 기록으로 "내 실제 계좌" 줄을 A 뒤에 넣는다(사용자 결정 10-21)
      try { result = attachActual(replay(toEngineInput(bundle, records, { plan: true })), { records, bundle, trades }); } catch (e) { calcError = e.message; }
    }
    const reload = async () => { if (g === gen && auth.currentUser === user) await loadAll(user, g, main); };
    const act = (f) => async (...a) => {
      try { await f(...a); } catch (e) { throw new Error(why(e)); }
      await reload();
    };
    const addTrade = async (entry) => {
      if (!tradesExist) { await setDoc(tref(user), { entries: {} }); tradesExist = true; }   // 다음 단계가 실패해 다시 눌러도 빈 문서를 또 만들지 않게
      const k = newId('t');
      await updateDoc(tref(user), { ['entries.' + k]: { ...entry, recordedAt: serverTimestamp() } });
    };
    // 지운 입금을 가리키는 예전 취소 기록도 같이 지운다
    const cancelsOf = (id) => Object.entries((bundle && bundle.deposits) || {}).filter(([, d]) => d.cancels === id).map(([k]) => k);
    const handlers = {
      // 모든 값은 고치고 지울 수 있다(사용자 결정 10-20). 기록 시각(recordedAt·createdAt)은 반영일·출발일을 정하므로 고칠 때 그대로 둔다.
      create: act((snap) => setDoc(ref, { snapshot: { ...snap, createdAt: serverTimestamp() }, deposits: {}, scenarios: {} })),
      editSnapshot: act((snap) => updateDoc(ref, { 'snapshot.date': snap.date, 'snapshot.holdings': snap.holdings, 'snapshot.cash': snap.cash, 'snapshot.holdOnly': snap.holdOnly })),
      deposit: act((amount) => updateDoc(ref, { ['deposits.' + newId('d')]: { amount, recordedAt: serverTimestamp() } })),
      editDeposit: act((id, amount) => updateDoc(ref, { ['deposits.' + id + '.amount']: amount })),
      deleteDeposit: act((id) => updateDoc(ref, Object.fromEntries([id, ...cancelsOf(id)].map((k) => ['deposits.' + k, deleteField()])))),
      scenario: act((sc) => updateDoc(ref, { ['scenarios.' + newId('s')]: { ...sc, createdAt: serverTimestamp(), engineVersion: ENGINE_VERSION } })),
      deleteScenario: act((id) => updateDoc(ref, { ['scenarios.' + id]: deleteField() })),
      // 전략 고치기: 이름·전략·설정만 바꾸고 만든 시각은 그대로(순서·색 자리 유지). 엔진 판도 지금 것으로
      editScenario: act((id, sc) => updateDoc(ref, { ['scenarios.' + id + '.name']: sc.name, ['scenarios.' + id + '.strategy']: sc.strategy,
        ['scenarios.' + id + '.params']: sc.params, ['scenarios.' + id + '.engineVersion']: ENGINE_VERSION })),
      close: act(() => updateDoc(ref, { closed: { reason: 'correction', at: serverTimestamp() } })),
      trade: act((t) => addTrade(t)),
      editTrade: act((id, t) => updateDoc(tref(user), Object.fromEntries(['date', 'ticker', 'side', 'qty', 'price'].map((f) => ['entries.' + id + '.' + f, t[f]])))),
      deleteTrade: act((id) => updateDoc(tref(user), Object.fromEntries([id, ...Object.entries(trades).filter(([, x]) => x.cancels === id).map(([k]) => k)].map((k) => ['entries.' + k, deleteField()])))),
      goto: (tab) => selectTab(tab),
    };
    const model = { main, trades, result, bundle, byId, records, now: Date.now(), allDeposits };

    renderTabs({ home: $('pf-home'), strategy: $('pf-strategy'), manage: $('pf-manage') }, model,
      { bundle, bundleNo: no, closedCount, records, recordsError, calcError, holdingsRows: (main.holdings && main.holdings.rows) || [] }, handlers);
  }

  // ---- 하위 탭 ----
  const TAB_KEY = 'pf-tab';
  function selectTab(name) {
    // 없어진 탭(원칙·관심 종목은 2026-10-21 한눈에 아래 접는 칸으로 옮김)을 기억하고 있으면 한눈에로
    if (!document.querySelector(`.pf-tabpanel[data-panel="${name}"]`)) name = 'home';
    document.querySelectorAll('.pf-tabs [role=tab]').forEach((b) => b.setAttribute('aria-selected', String(b.dataset.tab === name)));
    document.querySelectorAll('.pf-tabpanel').forEach((p) => { p.hidden = p.dataset.panel !== name; });
    try { sessionStorage.setItem(TAB_KEY, name); } catch (_) { /* 저장 못 해도 탭은 바뀐다 */ }
    window.scrollTo({ top: 0 });
  }
  document.querySelectorAll('.pf-tabs [role=tab]').forEach((b) => b.addEventListener('click', () => selectTab(b.dataset.tab)));
  try { const t = sessionStorage.getItem(TAB_KEY); if (t) selectTab(t); } catch (_) { /* 기본 탭 */ }

  // 로그인 유지 방식(이 탭만)을 먼저 정하고 나서 로그인 상태를 본다. 정하지 못하면 기본(계속 유지)으로
  // 넘어가지 않고 여기서 멈춘다 — '이 탭에서만' 결정을 지키지 못하는 상태로는 열지 않는다.
  let persisted = true;
  try { await setPersistence(auth, browserSessionPersistence); } catch (_) { persisted = false; }
  if (!persisted) {
    show('out', '이 브라우저에서는 탭 단위 로그인을 쓸 수 없어 열지 않습니다(사생활 보호 모드·저장소 차단을 확인하세요).');
    $('pf-login').disabled = true;
  } else onAuthStateChanged(auth, (user) => {
    gen += 1;
    if (user) open(user, gen);
    else { show('out', quietOut); quietOut = ''; }
  });

  if (persisted) $('pf-login').disabled = false; // 준비가 끝난 뒤에만 누를 수 있다(HTML에서는 꺼져 있다)
  if (persisted) $('pf-login').addEventListener('click', async () => {
    $('pf-login').disabled = true;
    $('pf-msg').textContent = '';
    try {
      await signInWithPopup(auth, new GoogleAuthProvider());
    } catch (e) {
      if (e.code !== 'auth/popup-closed-by-user' && e.code !== 'auth/cancelled-popup-request') {
        $('pf-msg').textContent = '로그인하지 못했습니다(' + (e.code || e.message) + ').';
      }
    } finally { $('pf-login').disabled = false; }
  });

  $('pf-logout').addEventListener('click', async () => {
    quietOut = '로그아웃했습니다.';
    try { await signOut(auth); } catch (e) { show('out', '로그아웃하지 못했습니다(' + (e.code || e.message) + ').'); }
  });

  // 데이터 올리기: JSON 파일(형식은 pipeline/portfolio/sample.json)은 내 문서를 통째로 바꾼다. CSV·Excel(2026-10-21)은
  // Robinhood 거래 내역이나 보유 표에서 '올린 보유'만 만들어 바꾸고 원칙·관심 종목은 그대로 둔다(preview-only-portfolio-import.js).
  // 순서: 읽기 → 모양 검사 → 두 번 고르기 확인 → 화면에 그려 보기 → 저장. 앞 단계가 틀리면 저장하지 않는다.
  $('pf-upload').addEventListener('change', async (e) => {
    const input = e.target, file = input.files[0];
    input.value = '';
    const user = auth.currentUser, g = gen;
    if (!file || !user) return;
    clearConfirm();
    if (file.size > MAX_BYTES) { $('pf-upload-msg').textContent = '파일이 너무 큽니다(900KB 이하).'; return; }
    const current = () => g === gen && auth.currentUser === user; // 로그인 상태가 그대로인지 — 아니면 화면을 건드리지 않는다
    let d, text, json, what = null;
    try {
      const csv = await fileToCSV(file);
      if (csv == null) {
        text = await file.text();
        d = validate(JSON.parse(text));
      } else {
        text = csv;
        const res = importTable(parseCSV(csv));
        const today = etDate(Date.now());
        const holdings = { ...res.holdings, asOf: res.holdings.asOf || today + ' 올린 표 기준' };
        d = validate({ ...currentMain, holdings, updated: today });
        what = res.summary + ' 원칙·관심 종목은 그대로 두고 "올린 보유"만 바꿉니다.' + (res.warnings.length ? ' ⚠ ' + res.warnings.join(' · ') + '.' : '');
      }
      json = JSON.stringify(d);
    } catch (err) {
      if (!current()) return;
      $('pf-upload-msg').textContent = err instanceof SyntaxError ? 'JSON 형식이 아닙니다.' : '읽지 못했습니다: ' + err.message;
      return;
    }
    if (!current()) return;
    if (new TextEncoder().encode(json).length > MAX_BYTES) { $('pf-upload-msg').textContent = '데이터가 너무 큽니다(900KB 이하).'; return; }
    const n = d.holdings?.rows?.filter((r) => r.ticker).length ?? 0;
    askConfirm(what || `${file.name}: 원칙 ${(d.principles || []).length}개 · 보유 ${n}종목 · 관심 종목 ${(d.watchlist || []).length}개로 지금 데이터를 통째로 바꿉니다.`, async () => {
      if (!current()) return;
      input.disabled = true;
      try {
        render(d); // 그려 보다 실패하면 저장하지 않는다
        // 여기까지 오면 저장을 보낸다. 보낸 뒤 로그아웃해도 저장은 취소되지 않고, 결과 문구만 띄우지 않는다.
        await setDoc(ref(user), { json, uploaded: serverTimestamp() });
        currentMain = d;
        if (current()) { $('pf-upload-msg').textContent = file.name + '을(를) 올렸습니다.'; if (refreshTabs) refreshTabs(d); }
      } catch (err) {
        if (current()) $('pf-upload-msg').textContent = '올리지 못했습니다(' + (err.code || err.message) + '). 새로고침하면 저장된 데이터가 보입니다.';
      } finally { input.disabled = false; }
    });
  });
  $('pf-upload-ok').addEventListener('click', async () => {
    const p = pending; clearConfirm();
    if (p) await p.save();
  });
  $('pf-upload-cancel').addEventListener('click', () => { clearConfirm(); $('pf-upload-msg').textContent = '올리지 않았습니다.'; });
}
