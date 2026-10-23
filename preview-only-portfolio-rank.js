// preview 전용 Portfolio 탭 — 전략 비교 하위 탭(2026-10-21 사용자 선택: 디자인 시안 "B 순위 + C 편집기 + B 카드"). 라이브로 옮기지 않는다 — pipeline/site_ui/UI_DIFF.md 1절 portfolio.
//
// 위: 수익률 순위(줄을 누르면 바로 아래에 편집기), 가운데: 내 전략 카드(수정 → 같은 편집기), 아래: 그래프·전체 표·매매 기록(접음).
// 편집기는 살 판정 칩과 매도 비율·회차·현금 유보 버튼으로 고치고, 고른 값을 문장으로 보여 준다. 저장은 handlers(scenario·editScenario·deleteScenario).
// 저평가만(C)·갈아타기(D)는 값을 바꾸지 않으면 그 전략 그대로 저장하고, 바꾸면 사용자 정의로 저장한다(C는 매도 알림을 남기지 않아 사용자 정의와 다르다).
// 순수 함수(draftOf·shapeOf·sentenceOf·rankRows)는 node 시험이 부른다(pipeline/portfolio/test_strategy_view.mjs).
import { el, msgLine, twoStep, usd, pct, pp, label, summarize, paramsText, checkScenario, MAX_SCENARIOS, NAME_MAX, ETF_ORDER,
  compareSection, chartSection, detailSection } from './preview-only-portfolio-strategy.js?v=18';
import { BUY_PRINCIPLE, BASELINES } from './preview-only-portfolio-engine.js?v=3';

export const ALL_TIERS = ['초저평가', '저평가', '적정~저평가', '적정', '고평가~적정', '고평가', '초고평가'];
const C_TIERS = ['초저평가', '저평가'];
const SELL_OPTS = [0, 25, 50, 100], ROUND_OPTS = [1, 2, 3, 4], RESERVE_OPTS = [0, 10, 20], ETF_SHARE_OPTS = [0, 25, 50, 75, 100];
const ETFS = ETF_ORDER;
// 저장된 비율(0~1, 소수 6자리) ↔ 편집기 %(소수 4자리) — 반올림 없이 오가서 열었다 저장해도 값이 바뀌지 않는다(dr r1)
const toPct = (v) => Math.round(v * 1e6) / 1e4, fromPct = (v) => Math.round(v * 1e4) / 1e6;
const AUTO = new Set(['A', 'REAL']);

// ---- 순수 함수 ----

// 저장된 시나리오({strategy, params}) → 편집기 값. kind = 'verdict'(판정으로 사고팔기: 살 판정 목록, 매도 %, 회차, 유보 %)
// | 'etf'(ETF 섞기: 바꿀 비율 %, 고른 ETF). 두 종류의 값을 다 들고 있어 종류를 바꿔도 고른 값이 남는다. 없으면 새 전략 기본값(원칙과 같음).
const etfDefault = () => ({ etfShare: 100, etfs: [...ETFS] });
export function draftOf(sc) {
  if (!sc) return { kind: 'verdict', tiers: [...BUY_PRINCIPLE], sell: 0, rounds: 4, reserve: 0, ...etfDefault() };
  const p = sc.params || {};
  if (sc.strategy === 'E') return { ...draftOf(null), kind: 'etf', etfShare: toPct(p.etfShare ?? 1), etfs: ETFS.filter((e) => (p.etfs || ETFS).includes(e)) };
  const tiers = sc.strategy === 'custom' ? [...(p.buyTiers || [])] : sc.strategy === 'C' ? [...C_TIERS] : [...BUY_PRINCIPLE];
  const sell = sc.strategy === 'D' ? 100 : sc.strategy === 'C' ? 0 : toPct(p.sellFraction || 0);
  return { kind: 'verdict', tiers, sell, rounds: p.splitWeeks || 4, reserve: toPct(p.cashReserve || 0), ...etfDefault() };
}

const sameSet = (a, b) => a.length === b.length && a.every((t) => b.includes(t));
// 편집기 값 → 저장할 {strategy, params}. base = 고치기 전 전략('C'|'D'|'B'|'custom'|null)
export function shapeOf(base, d) {
  if (d.kind === 'etf') return { strategy: 'E', params: { etfShare: fromPct(d.etfShare), etfs: BASELINES.filter((e) => d.etfs.includes(e)) } };
  const common = { splitWeeks: d.rounds, cashReserve: fromPct(d.reserve) };
  if (base === 'C' && sameSet(d.tiers, C_TIERS) && d.sell === 0) return { strategy: 'C', params: common };
  if (base === 'D' && sameSet(d.tiers, BUY_PRINCIPLE) && d.sell === 100) return { strategy: 'D', params: common };
  return { strategy: 'custom', params: { buyTiers: ALL_TIERS.filter((t) => d.tiers.includes(t)), sellFraction: fromPct(d.sell), ...common } };
}

// 편집기 값 → "이 전략이 하는 일" 한 문장
export function sentenceOf(base, d) {
  if (d.kind === 'etf') {
    const etfs = ETFS.filter((e) => d.etfs.includes(e));
    if (!etfs.length) return '살 ETF를 하나 이상 고르세요.';
    if (!d.etfShare) return '보유 종목을 그대로 들고 입금도 시작 때 비중대로 나눠 넣습니다(ETF로 바꾸지 않음). 그 뒤로는 사고팔지 않습니다.';
    return `시작일 종가에 보유 종목(고른 ETF는 빼고)${d.etfShare === 100 ? '을 모두' : `의 ${d.etfShare}%를`} 팔아 ${etfs.join('·')}에 똑같이 나눠 삽니다. `
      + '고르지 않은 ETF를 가지고 있으면 그것도 같은 비율로 팝니다. 현금은 그대로 둡니다. 입금은 시작 때 비중대로 현금·주식·ETF에 나눠 넣고, 그 뒤로는 사고팔지 않습니다.';
  }
  const shape = shapeOf(base, d);
  const tiers = ALL_TIERS.filter((t) => d.tiers.includes(t));
  const buy = `매달 1일 판정이 ${tiers.length ? tiers.join('·') : '(없음)'}인 종목을 ${d.rounds === 1 ? '한 번에' : d.rounds + '주에 나눠'} 삽니다.`;
  const sell = d.sell ? `판정이 고평가·초고평가가 되면 남은 수량의 ${d.sell}%를 팝니다.`
    : shape.strategy === 'C' ? '팔지 않습니다.' : '고평가가 되어도 팔지 않고 매도 검토 알림만 남깁니다.';
  const cash = d.reserve ? `현금은 ${d.reserve}%를 남겨 둡니다.` : '현금은 남기지 않습니다.';
  const off = tiers.some((t) => !BUY_PRINCIPLE.includes(t)) ? ' 원칙 1 밖의 판정도 사므로 "원칙과 다름" 표시가 붙습니다.' : '';
  return `${buy} ${sell} ${cash}${off}`;
}

// 엔진 결과 → 순위 줄. sort = 'twr'|'spy'|'value'. 값이 없는 줄(출발 전·미확정)은 맨 뒤, 같은 값은 원래 순서.
// slot = 그래프와 같은 색 번호(결과 순서 1~8, 그 뒤는 null)
export function rankRows(result, byId, sort) {
  const rows = result.scenarios.map((s, i) => {
    const m = summarize(s);
    return { id: s.id, idx: i, name: label(s, byId), auto: AUTO.has(s.id), slot: i < 8 ? i + 1 : null,
      twr: m.twr, spy: m.vs ? m.vs.SPY ?? null : null, value: m.value, trades: m.trades, cashShare: m.cashShare, wait: m.waitText };
  });
  const key = (r) => (sort === 'spy' ? r.spy : sort === 'value' ? r.value : r.twr);
  return rows.sort((a, b) => {
    const x = key(a), y = key(b);
    if (x == null || y == null) return x == null && y == null ? a.idx - b.idx : x == null ? 1 : -1;
    return y - x || a.idx - b.idx;
  });
}

// A의 SPY 기준선 마지막 수익률(순위 막대의 세로선). 없으면 null
export function spyLine(result) {
  const A = result.baseA || result.scenarios.find((s) => s.id === 'A');   // A는 화면에서 숨겨도 기준선으로 남는다
  const pts = (A && A.baselines && A.baselines.SPY) || [];
  for (let i = pts.length - 1; i >= 0; i--) if (pts[i].twr != null) return pts[i].twr;
  return null;
}

// ---- 그리기 ----

const VIEW_KEY = 'pf-rank-view';
const view = (() => { try { return { sel: null, seed: null, sort: 'twr', folds: {}, help: false, ...JSON.parse(sessionStorage.getItem(VIEW_KEY) || '{}') }; } catch (_) { return { sel: null, seed: null, sort: 'twr', folds: {}, help: false }; } })();
const keep = () => { try { sessionStorage.setItem(VIEW_KEY, JSON.stringify(view)); } catch (_) { /* 기억 못 해도 화면은 그대로 */ } };
const dot = (slot) => el('i', 'pf-sdot' + (slot ? ' pf-c' + slot : ''));
const btn = (text, cls) => { const b = el('button', cls || 'pf-btn pf-btn-quiet', text); b.type = 'button'; return b; };

// st = #pf-strategy, model = renderTabs의 model(result·byId), smodel = { bundle, … }. 고르기·정렬은 이 탭만 다시 그린다.
let latest = null;
export function renderStrategy(st, model, smodel, handlers) {
  latest = [st, model, smodel, handlers];
  const draw = () => renderStrategy(...latest);   // 저장 뒤 늦게 부르는 닫기도 새로 받은 값으로 그린다
  const { result } = model, b = smodel.bundle && !smodel.bundle.closed ? smodel.bundle : null;
  const scen = b ? Object.entries(b.scenarios || {}).sort(([, x], [, y]) => (x.createdAt < y.createdAt ? -1 : 1)) : [];
  if (view.sel && view.sel !== '__new' && !AUTO.has(view.sel) && !scen.some(([id]) => id === view.sel)) view.sel = null;
  const rows = result ? rankRows(result, model.byId, view.sort) : [];
  // 고르기(줄·카드·새 전략)는 순위 바로 아래 편집기를 연다 — 카드까지 내려가지 않게(사용자 요청 10-21)
  const open = (id, seed) => { view.sel = id; view.seed = seed || null; keep(); draw(); st.querySelector('.pf-editor')?.scrollIntoView?.({ block: 'nearest' }); };
  const canAdd = !!b && scen.length < MAX_SCENARIOS;
  const byRow = new Map(rows.map((r) => [r.id, r]));
  const frag = document.createDocumentFragment();

  // 1) 수익률 순위
  if (result) {
    const sec = el('section', 'pf-panel pf-rank');
    const head = el('div', 'pf-rankhead');
    // 제목은 질문형(최종 시안), 계산 설명은 "?"를 눌러야 펼친다(반복 안내 줄이 많던 것을 줄임 — 사용자 요청 10-21)
    const ttl = el('div');
    ttl.appendChild(el('div', 'pf-eyebrow2', '같은 출발점, 다른 선택'));
    const tl = el('div', 'pf-titleline'); tl.appendChild(el('h2', 'pf-h2q', '어떤 전략이 앞서고 있을까요?'));
    const help = btn('?', 'pf-help'); help.setAttribute('aria-label', '순위 계산 설명'); help.setAttribute('aria-expanded', String(!!view.help));
    tl.appendChild(help); ttl.appendChild(tl); head.appendChild(ttl);
    const tools = el('div', 'pf-seg');
    const sorts = el('div', 'pf-seg pf-segbox'); sorts.setAttribute('role', 'group'); sorts.setAttribute('aria-label', '정렬 기준');
    for (const [k, t] of [['twr', '수익률(TWR)'], ['spy', 'SPY 대비'], ['value', '평가액']]) {
      const s = btn(t, 'pf-segbtn'); s.setAttribute('aria-pressed', String(view.sort === k));
      s.addEventListener('click', () => { view.sort = k; keep(); draw(); });
      sorts.appendChild(s);
    }
    tools.appendChild(sorts);
    if (canAdd) { const add = btn('＋ 새 전략', 'pf-pill pf-pilladd'); add.addEventListener('click', () => open('__new')); tools.appendChild(add); }
    head.appendChild(tools);
    sec.appendChild(head);
    const spy = spyLine(result);
    const helpBox = el('div', 'pf-helpbox'); helpBox.hidden = !view.help;
    helpBox.appendChild(el('p', null, (spy != null ? `점선 = SPY(${pct(spy)}, 시작 스냅샷에서 같은 날 출발). ` : '') + '막대는 수익률(TWR)입니다. 모든 전략은 시작 스냅샷에서 같이 출발하고, 입금은 반영일부터 모든 전략에 같이 들어갑니다.'));
    helpBox.appendChild(el('p', null, '기준선 대비는 같은 출발 시점·평가액에서 SPY·RSP·QQQ만 산 경우와의 차이입니다. 종목 선택뿐 아니라 현금 유보·나눠 사기 시점의 효과도 섞여 있어 판정 신호의 성과로 읽지 않습니다.'));
    if (smodel.info) helpBox.appendChild(el('p', null, smodel.info));
    help.addEventListener('click', () => { view.help = !view.help; keep(); helpBox.hidden = !view.help; help.setAttribute('aria-expanded', String(view.help)); });
    sec.appendChild(helpBox);
    const vals = rows.map((r) => r.twr).filter((v) => v != null).concat(spy == null ? [] : [spy], [0]);
    const lo = Math.min(...vals), hi = Math.max(...vals) === lo ? lo + 0.01 : Math.max(...vals);
    const at = (v) => ((v - lo) / (hi - lo)) * 100;
    const list = el('div', 'pf-ranklist');
    rows.forEach((r, n) => {
      const row = btn(null, 'pf-rankrow'); row.setAttribute('aria-pressed', String(view.sel === r.id));
      row.appendChild(el('span', 'pf-rankn', r.twr == null ? '–' : String(n + 1)));
      const nm = el('span', 'pf-rankname' + (r.auto ? ' pf-auto' : ''));
      const nl = el('span', 'pf-ranknl'); nl.appendChild(dot(r.slot)); nl.appendChild(el('span', null, r.name)); nm.appendChild(nl);
      nm.appendChild(el('small', null, r.id === 'REAL' ? '고정 비교 · 실제 매매 기록' : r.auto ? '고정 비교 · 수정 불가' : '모의 전략 · 눌러서 설정'));
      row.appendChild(nm);
      const track = el('span', 'pf-rankbar');
      if (r.twr != null) {
        const bar = el('i', r.slot ? 'pf-c' + r.slot : '');
        bar.style.left = Math.min(at(0), at(r.twr)) + '%'; bar.style.width = Math.max(Math.abs(at(r.twr) - at(0)), 0.5) + '%';
        track.appendChild(bar);
      } else track.appendChild(el('small', null, r.wait || '미확정'));
      if (spy != null) { const ln = el('b'); ln.style.left = at(spy) + '%'; ln.title = 'SPY ' + pct(spy); track.appendChild(ln); }
      row.appendChild(track);
      const main = view.sort === 'value' ? usd(r.value) : view.sort === 'spy' ? pp(r.spy) : pct(r.twr);
      const sub = view.sort === 'value' ? pct(r.twr) : usd(r.value);
      row.appendChild(el('strong', 'pf-ranknum', r.twr == null && view.sort !== 'value' ? '—' : main));
      row.appendChild(el('small', 'pf-ranksub', r.twr == null && view.sort === 'value' ? '' : sub));
      const mk = el('span', 'pf-rankmark', r.auto ? '—' : view.sel === r.id ? '⌃' : '⌄'); mk.setAttribute('aria-hidden', 'true'); row.appendChild(mk);
      row.setAttribute('aria-label', `${r.name}, ${pct(r.twr)}, 눌러서 ${r.auto ? '설명' : '수정'} 열기`);
      row.addEventListener('click', () => { if (view.sel === r.id) { view.sel = null; keep(); draw(); } else open(r.id); });
      list.appendChild(row);
    });
    sec.appendChild(list);
    sec.appendChild(el('p', 'pf-note', (spy != null ? `점선 = SPY ${pct(spy)}. ` : '') + '바꿀 수 있는 줄은 누르면 바로 아래에서 고칩니다.'));
    frag.appendChild(sec);
  }

  // 2) 편집기(고른 줄 또는 새 전략)
  if (view.sel) {
    const sc = scen.find(([id]) => id === view.sel);
    const panel = editor(view.sel, sc ? sc[1] : null, byRow.get(view.sel), b, result, handlers, () => { view.sel = null; keep(); draw(); }, scen.length, st,
      canAdd ? (seed) => open('__new', seed) : null);
    if (panel) frag.appendChild(panel);
  }

  // 3) 내 전략 카드
  if (b) {
    const sec = el('section', 'pf-panel');
    const sh = el('div', 'pf-sidehead'); sh.appendChild(el('h2', 'pf-h2s', '내 전략')); sh.appendChild(el('span', 'pf-note', `${scen.length} / ${MAX_SCENARIOS}`)); sec.appendChild(sh);
    if (!scen.length) sec.appendChild(el('p', 'pf-note', '아직 만든 전략이 없습니다. 위 "＋ 새 전략"이나 A 줄의 "이 줄을 바탕으로 새 전략 만들기"로 만듭니다.'));
    const grid = el('div', 'pf-scards');
    for (const [id, s] of scen) {
      const r = byRow.get(id);
      const card = btn(null, 'pf-scard' + (view.sel === id ? ' pf-on' : ''));
      card.setAttribute('aria-pressed', String(view.sel === id));
      card.addEventListener('click', () => open(id));
      const top = el('div', 'pf-scardtop'); top.appendChild(dot(r?.slot)); top.appendChild(el('h4', null, s.name)); top.appendChild(el('strong', null, r ? pct(r.twr) : '계산 전'));
      card.appendChild(top);
      const chips = el('div', 'pf-chips');
      for (const t of paramsText(s).split(' · ')) chips.appendChild(el('span', null, t));
      card.appendChild(chips);
      const stats = el('div', 'pf-sstats');
      for (const [k, v] of [['SPY 대비', r ? pp(r.spy) : '—'], ['체결', r ? r.trades + '건' : '—'], ['현금', r && r.cashShare != null ? (r.cashShare * 100).toFixed(1) + '%' : '—']]) {
        const c = el('span', null, k); c.appendChild(el('b', null, v)); stats.appendChild(c);
      }
      card.appendChild(stats);
      if (r?.wait) card.appendChild(el('p', 'pf-warn', r.wait));
      card.appendChild(el('span', 'pf-cardlink', '설정 열기'));
      card.setAttribute('aria-label', `${s.name} 수정 열기`);
      grid.appendChild(card);
    }
    if (scen.length < MAX_SCENARIOS) {
      const add = btn('＋ 새 전략', 'pf-scard pf-scardnew');
      add.addEventListener('click', () => open('__new'));
      grid.appendChild(add);
    }
    sec.appendChild(grid);
    frag.appendChild(sec);
  }

  // 4) 그래프·전체 표·매매 기록(접음)
  // 그래프·표·매매 기록은 각각 접는 칸(최종 시안 — 그래프도 접어 둔다, 사용자 결정 10-21)
  const folds = [];
  if (result) for (const [k, t, make] of [['chart', '누적 평가액 그래프 · 전략 최대 4개 + 기준선', chartSection], ['table', '전체 비교 표 · 12개 항목', compareSection], ['trades', '전략별 매매 기록', detailSection]]) {
    const fd = el('details', 'pf-foldcard pf-stfold pf-fold-' + k);
    fd.open = !!view.folds?.[k];
    fd.addEventListener('toggle', () => { view.folds = { ...(view.folds || {}), [k]: fd.open }; keep(); });
    fd.appendChild(el('summary', null, t));
    frag.appendChild(fd); folds.push([fd, make]);
  }

  // 앞부분(고정 안내·상태 줄)은 renderTabs가 이미 넣었다 — 그 뒤만 바꾼다
  st.querySelectorAll(':scope > .pf-rankpart').forEach((x) => x.remove());
  const wrap = el('div', 'pf-rankpart'); wrap.appendChild(frag); st.appendChild(wrap);
  // 그래프 폭은 탭 폭을 읽으므로 탭에 붙인 뒤 채운다
  for (const [fd, make] of folds) fd.appendChild(make(result, model.byId));
}

// 편집기 패널. id = 'A'|'REAL'|'__new'|시나리오 id, sc = 저장된 시나리오(없으면 null), r = 순위 줄
function editor(id, sc, r, b, result, handlers, close, count, st, openNew) {
  const isNew = id === '__new';
  if (!isNew && !AUTO.has(id) && !sc) return null;
  const panel = el('section', 'pf-panel pf-editor');
  panel.setAttribute('aria-label', '전략 편집기');
  const head = el('div', 'pf-edhead');
  const ttl = el('div', 'pf-edtitle'); ttl.appendChild(dot(r?.slot));
  const tt = el('div'); tt.appendChild(el('small', null, AUTO.has(id) ? '자동으로 있는 줄' : isNew ? '새 전략' : '전략 수정'));
  tt.appendChild(el('h3', null, isNew ? '새 전략' : r?.name || sc?.name || id)); ttl.appendChild(tt);
  head.appendChild(ttl);
  const nums = el('div', 'pf-ednums');
  if (r) for (const [k, v] of [['수익률', pct(r.twr)], ['SPY 대비', pp(r.spy)], ['체결', r.trades + '건']]) { const c = el('span', null, k); c.appendChild(el('b', null, v)); nums.appendChild(c); }
  const x = btn('닫기'); x.setAttribute('aria-label', '편집기 닫기'); x.addEventListener('click', close); nums.appendChild(x);
  head.appendChild(nums);
  panel.appendChild(head);
  if (r?.wait) panel.appendChild(el('p', 'pf-warn', r.wait));

  if (AUTO.has(id)) {
    panel.appendChild(el('p', 'pf-lockbox', id === 'REAL'
      ? '한눈에 탭의 실제 매매 기록과 기록·관리 탭의 입금으로 정해지는 줄이라 고칠 설정이 없습니다. 매매를 고치려면 기록·관리 탭에서 고칩니다.'
      : '시작 스냅샷을 그대로 들고 입금만 더하는 기준 줄이라 고칠 설정이 없습니다. 스냅샷은 기록·관리 탭에서 고칩니다.'));
    const acts = el('div', 'pf-acts pf-edacts');
    // 자동 줄을 바탕으로 새 전략: A(내 종목 그대로)는 ETF 섞기로, 실제 계좌는 판정으로 사고팔기로 연다(사용자 요청 10-21)
    if (openNew) { const nb = btn('이 줄을 바탕으로 새 전략 만들기', 'pf-btn'); nb.addEventListener('click', () => openNew(id === 'A' ? 'etf' : null)); acts.appendChild(nb); }
    acts.appendChild(tradesLink(id, result, st));
    panel.appendChild(acts);
    return panel;
  }
  if (!b) { panel.appendChild(el('p', 'pf-note', '전략 비교를 시작한 뒤(기록·관리 탭의 시작 스냅샷) 전략을 만들 수 있습니다.')); return panel; }

  const base = sc ? (sc.strategy === 'B' ? 'custom' : sc.strategy) : null;
  const d = draftOf(sc && sc.strategy === 'B' ? { strategy: 'custom', params: { ...sc.params, buyTiers: BUY_PRINCIPLE } } : sc);
  if (isNew && view.seed === 'etf') d.kind = 'etf';
  const body = el('div', 'pf-edbody');
  const left = el('div', 'pf-edleft'), right = el('div', 'pf-edright');
  const nameL = el('label', 'pf-field'); nameL.appendChild(el('span', null, '이름'));
  const name = el('input'); name.maxLength = NAME_MAX; name.value = sc?.name || ''; nameL.appendChild(name); left.appendChild(nameL);
  const sentence = el('p', 'pf-edsent');
  const msg = msgLine();
  const sync = () => { sentence.textContent = sentenceOf(base, d); };

  // 전략 종류: 판정으로 사고팔기 | ETF 섞기(2026-10-21 사용자 요청 — ETF와 주식을 섞어 사면 어떤지 보려고)
  const kindBox = el('fieldset', 'pf-edgroup'); kindBox.appendChild(el('legend', null, '전략 종류'));
  const kindRow = el('div', 'pf-seg pf-segbox');
  const verdictPart = el('div', 'pf-edpart'), etfPart = el('div', 'pf-edpart');
  const showKind = () => { verdictPart.hidden = d.kind !== 'verdict'; etfPart.hidden = d.kind !== 'etf'; };
  for (const [k, t] of [['verdict', '판정으로 사고팔기'], ['etf', 'ETF 섞기']]) {
    const o = btn(t, 'pf-segbtn'); o.setAttribute('aria-pressed', String(d.kind === k));
    o.addEventListener('click', () => { d.kind = k; kindRow.querySelectorAll('button').forEach((y) => y.setAttribute('aria-pressed', String(y === o))); showKind(); sync(); });
    kindRow.appendChild(o);
  }
  kindBox.appendChild(kindRow); left.appendChild(kindBox);
  left.appendChild(verdictPart); left.appendChild(etfPart);

  const tierBox = el('fieldset', 'pf-edgroup'); tierBox.appendChild(el('legend', null, '살 판정 · 원칙 1'));
  const chips = el('div', 'pf-tierchips');
  for (const t of ALL_TIERS) {
    const c = btn(t, 'pf-tierchip'); c.setAttribute('aria-pressed', String(d.tiers.includes(t)));
    c.addEventListener('click', () => { d.tiers = d.tiers.includes(t) ? d.tiers.filter((y) => y !== t) : [...d.tiers, t]; c.setAttribute('aria-pressed', String(d.tiers.includes(t))); sync(); });
    chips.appendChild(c);
  }
  tierBox.appendChild(chips); verdictPart.appendChild(tierBox);
  // 저장된 값이 버튼에 없으면(예전 양식으로 넣은 33% 등) 그 값도 버튼으로 둔다
  const seg = (title, key, opts, unit, into = verdictPart) => {
    const g = el('fieldset', 'pf-edgroup'); g.appendChild(el('legend', null, title));
    const row = el('div', 'pf-seg pf-segbox');
    for (const v of [...new Set([...opts, d[key]])].sort((p, q) => p - q)) {
      const o = btn(v + unit, 'pf-segbtn'); o.setAttribute('aria-pressed', String(d[key] === v));
      o.addEventListener('click', () => { d[key] = v; row.querySelectorAll('button').forEach((y) => y.setAttribute('aria-pressed', String(y === o))); sync(); });
      row.appendChild(o);
    }
    g.appendChild(row); into.appendChild(g);
  };
  seg('고평가가 되면 파는 비율 · 원칙 4', 'sell', SELL_OPTS, '%');
  seg('몇 번에 나눠 살까 · 원칙 2', 'rounds', ROUND_OPTS, '회');
  seg('남겨 둘 현금 · 원칙 5', 'reserve', RESERVE_OPTS, '%');
  seg('ETF로 바꿀 비율 · 주식 평가액 기준', 'etfShare', ETF_SHARE_OPTS, '%', etfPart);
  const etfBox = el('fieldset', 'pf-edgroup'); etfBox.appendChild(el('legend', null, '살 ETF · 고른 것끼리 똑같이'));
  const etfChips = el('div', 'pf-tierchips');
  for (const e of ETFS) {
    const c = btn(e, 'pf-tierchip'); c.setAttribute('aria-pressed', String(d.etfs.includes(e)));
    c.addEventListener('click', () => { d.etfs = d.etfs.includes(e) ? d.etfs.filter((y) => y !== e) : [...d.etfs, e]; c.setAttribute('aria-pressed', String(d.etfs.includes(e))); sync(); });
    etfChips.appendChild(c);
  }
  etfBox.appendChild(etfChips); etfPart.appendChild(etfBox);
  showKind();

  right.appendChild(el('small', 'pf-note', '이 전략이 하는 일'));
  right.appendChild(sentence);
  const save = btn(isNew ? '전략 만들기' : '저장하고 다시 계산', 'pf-btn');
  right.appendChild(save);
  const row2 = el('div', 'pf-acts pf-edacts');
  const dup = btn('복제'), del = btn('지우기');
  if (!isNew) { row2.appendChild(dup); row2.appendChild(del); }
  right.appendChild(row2);
  right.appendChild(msg);
  if (!isNew) right.appendChild(tradesLink(id, result, st));
  right.appendChild(el('p', 'pf-note', '저장하면 시작 스냅샷부터 다시 계산합니다.'));
  body.appendChild(left); body.appendChild(right);
  panel.appendChild(body);
  sync();

  const build = (nm) => { const sh = shapeOf(base, d); return { name: nm.trim(), strategy: sh.strategy, params: sh.params }; };
  twoStep(save, msg, isNew ? '이 설정으로 만듭니다. 맞으면 한 번 더 누르세요.' : '이 설정으로 고칩니다(처음부터 다시 계산). 맞으면 한 번 더 누르세요.', async () => {
    const s = build(name.value), bad = checkScenario(s, isNew ? count : 0);
    if (bad) throw new Error(bad);
    if (isNew) { await handlers.scenario(s); close(); } else await handlers.editScenario(id, s);   // 새 전략은 저장된 뒤에만 닫는다(실패하면 입력이 남게)
  }, panel);
  twoStep(dup, msg, '지금 화면의 설정으로 사본을 만듭니다. 맞으면 한 번 더 누르세요.', async () => {
    const s = build(((name.value.trim() || sc.name) + ' 사본').slice(0, NAME_MAX)), bad = checkScenario(s, count);
    if (bad) throw new Error(bad);
    await handlers.scenario(s);
  }, panel);
  twoStep(del, msg, `"${sc?.name}" 전략을 지웁니다. 맞으면 지우기를 한 번 더 누르세요.`, async () => { await handlers.deleteScenario(id); close(); });
  return panel;
}

// 접어 둔 매매 기록에서 그 전략을 열어 보여 준다
function tradesLink(id, result, st) {
  const k = result ? result.scenarios.findIndex((s) => s.id === id) : -1;
  const a = btn('이 전략의 매매 기록 보기');
  a.disabled = k < 0;
  a.addEventListener('click', () => {
    const fold = st.querySelector('.pf-fold-trades'); if (!fold) return;
    fold.open = true;
    const d = fold.querySelectorAll('.pf-st-detail')[k];
    if (d) { d.open = true; d.scrollIntoView?.({ block: 'start' }); }
  });
  return a;
}
