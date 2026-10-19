// preview 전용 Portfolio 탭(2026-10-19). 라이브로 옮기지 않는다 — pipeline/site_ui/UI_DIFF.md 1절 portfolio.
//
// 나만 쓰기: Google 로그인(Firebase Auth) 뒤 Firestore `users/{uid}/portfolio/main` 문서 하나를 읽는다.
// 누가 읽을 수 있는지는 Firestore 규칙(pipeline/portfolio/firestore.rules)이 정한다 — 이 파일은 보호하지 않는다.
// 내 데이터는 GitHub 저장소에 올라가지 않는다(저장소에는 가짜 sample.json만). 로그인은 이 탭에서만 유지한다(사용자 결정):
// sessionStorage 기반이라 새 탭에서는 다시 묻는다. 브라우저의 '닫은 탭 다시 열기'·탭 복제는 로그인을 되살릴 수 있다.
// 화면은 입력한 값만 보여 준다. 평가액·수익률 같은 계산은 아직 없다(계산 정의는 다음 단계 dr).
import { initializeApp } from 'https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js';
import { getAuth, GoogleAuthProvider, signInWithPopup, signOut, onAuthStateChanged, setPersistence, browserSessionPersistence }
  from 'https://www.gstatic.com/firebasejs/10.12.2/firebase-auth.js';
import { getFirestore, doc, getDoc, setDoc, serverTimestamp }
  from 'https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js';
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
    ['pf-principles', 'pf-holdings', 'pf-watch', 'pf-scenarios', 'pf-account', 'pf-updated', 'pf-holdings-asof', 'pf-holdings-note', 'pf-upload-msg']
      .forEach((id) => { $(id).textContent = ''; });
    $('pf-sample').hidden = true;
    pending = null;
  }
  $('pf-msg').textContent = msg || '';
}

// 덮어쓰기 확인은 화면 안 문구로 한다(브라우저 확인 창을 쓰지 않는다): 같은 내용의 파일을 두 번째로 고르면 올린다.
let pending = null;
function confirmReplace(name, text) {
  if (pending === text) { pending = null; return true; }
  pending = text;
  $('pf-upload-msg').textContent = '지금 데이터를 ' + name + '(으)로 바꿉니다. 맞으면 같은 파일을 한 번 더 고르세요.';
  return false;
}

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
    if (!snap.exists()) { render({}); $('pf-updated').textContent = '아직 올린 데이터가 없습니다'; return; }
    try {
      render(validate(JSON.parse(snap.data().json)));
    } catch (e) {
      // 저장된 데이터가 깨져도 올리기 칸은 남겨 둔다 — 새 파일로 바꿔 복구한다
      render({});
      $('pf-upload-msg').textContent = '저장된 데이터를 읽지 못했습니다(' + e.message + '). 새 파일을 올려 바꾸세요.';
    }
  }

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

  // 데이터 올리기: 맥에 있는 JSON 파일(형식은 pipeline/portfolio/sample.json)을 골라 내 문서를 통째로 바꾼다.
  // 순서: 읽기 → 모양 검사 → 두 번 고르기 확인 → 화면에 그려 보기 → 저장. 앞 단계가 틀리면 저장하지 않는다.
  $('pf-upload').addEventListener('change', async (e) => {
    const input = e.target, file = input.files[0];
    input.value = '';
    const user = auth.currentUser, g = gen;
    if (!file || !user) return;
    if (file.size > MAX_BYTES) { $('pf-upload-msg').textContent = '파일이 너무 큽니다(900KB 이하).'; return; }
    const current = () => g === gen && auth.currentUser === user; // 로그인 상태가 그대로인지 — 아니면 화면을 건드리지 않는다
    let d, text, json;
    try {
      text = await file.text();
      d = validate(JSON.parse(text));
      json = JSON.stringify(d);
    } catch (err) {
      if (!current()) return;
      pending = null;
      $('pf-upload-msg').textContent = err instanceof SyntaxError ? 'JSON 형식이 아닙니다.' : '모양이 맞지 않습니다: ' + err.message;
      return;
    }
    if (!current()) return;
    if (new TextEncoder().encode(json).length > MAX_BYTES) { pending = null; $('pf-upload-msg').textContent = '데이터가 너무 큽니다(900KB 이하).'; return; }
    if (!confirmReplace(file.name, text)) return;
    input.disabled = true;
    try {
      render(d); // 그려 보다 실패하면 저장하지 않는다
      // 여기까지 오면 저장을 보낸다. 보낸 뒤 로그아웃해도 저장은 취소되지 않고, 결과 문구만 띄우지 않는다.
      await setDoc(ref(user), { json, uploaded: serverTimestamp() });
      if (current()) $('pf-upload-msg').textContent = file.name + '을(를) 올렸습니다.';
    } catch (err) {
      if (current()) $('pf-upload-msg').textContent = '올리지 못했습니다(' + (err.code || err.message) + '). 새로고침하면 저장된 데이터가 보입니다.';
    } finally { input.disabled = false; }
  });
}
