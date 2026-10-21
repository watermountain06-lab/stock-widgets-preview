// preview 전용 Portfolio 탭 — 전략 비교 하위 탭(2026-10-21 사용자 선택: 디자인 시안 "B 순위 + C 편집기 + B 카드"). 라이브로 옮기지 않는다 — pipeline/site_ui/UI_DIFF.md 1절 portfolio.
//
// 위: 수익률 순위(줄을 누르면 바로 아래에 편집기), 가운데: 내 전략 카드(수정 → 같은 편집기), 아래: 그래프·전체 표·매매 기록(접음).
// 편집기는 살 판정 칩과 매도 비율·회차·현금 유보 버튼으로 고치고, 고른 값을 문장으로 보여 준다. 저장은 handlers(scenario·editScenario·deleteScenario).
// 저평가만(C)·갈아타기(D)는 값을 바꾸지 않으면 그 전략 그대로 저장하고, 바꾸면 사용자 정의로 저장한다(C는 매도 알림을 남기지 않아 사용자 정의와 다르다).
// 순수 함수(draftOf·shapeOf·sentenceOf·rankRows)는 node 시험이 부른다(pipeline/portfolio/test_strategy_view.mjs).
import { el, msgLine, twoStep, usd, pct, pp, label, summarize, paramsText, checkScenario, MAX_SCENARIOS, NAME_MAX,
  compareSection, chartSection, detailSection } from './preview-only-portfolio-strategy.js?v=14';
import { BUY_PRINCIPLE } from './preview-only-portfolio-engine.js?v=1';

export const ALL_TIERS = ['초저평가', '저평가', '적정~저평가', '적정', '고평가~적정', '고평가', '초고평가'];
const C_TIERS = ['초저평가', '저평가'];
const SELL_OPTS = [0, 25, 50, 100], ROUND_OPTS = [1, 2, 3, 4], RESERVE_OPTS = [0, 10, 20];
const AUTO = new Set(['A', 'REAL']);

// ---- 순수 함수 ----

// 저장된 시나리오({strategy, params}) → 편집기 값(살 판정 목록, 매도 %, 회차, 유보 %). 없으면 새 전략 기본값(원칙과 같음).
export function draftOf(sc) {
  if (!sc) return { tiers: [...BUY_PRINCIPLE], sell: 0, rounds: 4, reserve: 0 };
  const p = sc.params || {};
  const tiers = sc.strategy === 'custom' ? [...(p.buyTiers || [])] : sc.strategy === 'C' ? [...C_TIERS] : [...BUY_PRINCIPLE];
  const sell = sc.strategy === 'D' ? 100 : sc.strategy === 'C' ? 0 : Math.round((p.sellFraction || 0) * 100);
  return { tiers, sell, rounds: p.splitWeeks || 4, reserve: Math.round((p.cashReserve || 0) * 100) };
}

const sameSet = (a, b) => a.length === b.length && a.every((t) => b.includes(t));
// 편집기 값 → 저장할 {strategy, params}. base = 고치기 전 전략('C'|'D'|'B'|'custom'|null)
export function shapeOf(base, d) {
  const common = { splitWeeks: d.rounds, cashReserve: d.reserve / 100 };
  if (base === 'C' && sameSet(d.tiers, C_TIERS) && d.sell === 0) return { strategy: 'C', params: common };
  if (base === 'D' && sameSet(d.tiers, BUY_PRINCIPLE) && d.sell === 100) return { strategy: 'D', params: common };
  return { strategy: 'custom', params: { buyTiers: ALL_TIERS.filter((t) => d.tiers.includes(t)), sellFraction: d.sell / 100, ...common } };
}

// 편집기 값 → "이 전략이 하는 일" 한 문장
export function sentenceOf(base, d) {
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
  const A = result.scenarios.find((s) => s.id === 'A');
  const pts = (A && A.baselines && A.baselines.SPY) || [];
  for (let i = pts.length - 1; i >= 0; i--) if (pts[i].twr != null) return pts[i].twr;
  return null;
}

// ---- 그리기 ----

const VIEW_KEY = 'pf-rank-view';
const view = (() => { try { return { sel: null, sort: 'twr', fold: false, ...JSON.parse(sessionStorage.getItem(VIEW_KEY) || '{}') }; } catch (_) { return { sel: null, sort: 'twr', fold: false }; } })();
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
  const byRow = new Map(rows.map((r) => [r.id, r]));
  const frag = document.createDocumentFragment();

  // 1) 수익률 순위
  if (result) {
    const sec = el('div', 'pf-st-block pf-rank');
    const head = el('div', 'pf-rankhead');
    head.appendChild(el('h3', null, '수익률 순위'));
    const sorts = el('div', 'pf-seg'); sorts.setAttribute('role', 'group'); sorts.setAttribute('aria-label', '정렬 기준');
    for (const [k, t] of [['twr', '수익률(TWR)'], ['spy', 'SPY 대비'], ['value', '평가액']]) {
      const s = btn(t, 'pf-pill'); s.setAttribute('aria-pressed', String(view.sort === k));
      s.addEventListener('click', () => { view.sort = k; keep(); draw(); });
      sorts.appendChild(s);
    }
    head.appendChild(sorts);
    sec.appendChild(head);
    const spy = spyLine(result);
    const vals = rows.map((r) => r.twr).filter((v) => v != null).concat(spy == null ? [] : [spy], [0]);
    const lo = Math.min(...vals), hi = Math.max(...vals) === lo ? lo + 0.01 : Math.max(...vals);
    const at = (v) => ((v - lo) / (hi - lo)) * 100;
    const list = el('div', 'pf-ranklist');
    rows.forEach((r, n) => {
      const row = btn(null, 'pf-rankrow'); row.setAttribute('aria-pressed', String(view.sel === r.id));
      row.appendChild(el('span', 'pf-rankn', r.twr == null ? '–' : String(n + 1)));
      const nm = el('span', 'pf-rankname' + (r.auto ? ' pf-auto' : '')); nm.appendChild(dot(r.slot)); nm.appendChild(el('span', null, r.name)); row.appendChild(nm);
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
      row.setAttribute('aria-label', `${r.name}, ${pct(r.twr)}, 눌러서 ${r.auto ? '설명' : '수정'} 열기`);
      row.addEventListener('click', () => { view.sel = view.sel === r.id ? null : r.id; keep(); draw(); });
      list.appendChild(row);
    });
    sec.appendChild(list);
    sec.appendChild(el('p', 'pf-note', (spy != null ? `세로선 = SPY(${pct(spy)}, A 출발 기준). ` : '') + '굵은 이름은 자동으로 있는 줄입니다. 줄을 누르면 아래에 그 전략이 열립니다. 막대는 수익률(TWR)입니다.'));
    frag.appendChild(sec);
  }

  // 2) 편집기(고른 줄 또는 새 전략)
  if (view.sel) {
    const sc = scen.find(([id]) => id === view.sel);
    const panel = editor(view.sel, sc ? sc[1] : null, byRow.get(view.sel), b, result, handlers, () => { view.sel = null; keep(); draw(); }, scen.length, st);
    if (panel) frag.appendChild(panel);
  }

  // 3) 내 전략 카드
  if (b) {
    const sec = el('div', 'pf-st-block');
    sec.appendChild(el('h3', null, `내 전략 (${scen.length}/${MAX_SCENARIOS})`));
    sec.appendChild(el('p', 'pf-note', '전략을 만들거나 고치면 시작일의 스냅샷에서 다시 계산합니다. "내 실제 계좌"와 "A. 그대로 보유"는 자동으로 있습니다.'));
    const grid = el('div', 'pf-scards');
    for (const [id, s] of scen) {
      const r = byRow.get(id);
      const card = el('article', 'pf-scard' + (view.sel === id ? ' pf-on' : ''));
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
      const fix = btn('수정'); fix.addEventListener('click', () => { view.sel = id; keep(); draw(); st.querySelector('.pf-editor')?.scrollIntoView?.({ block: 'nearest' }); });
      card.appendChild(fix);
      grid.appendChild(card);
    }
    if (scen.length < MAX_SCENARIOS) {
      const add = btn('＋ 새 전략', 'pf-scard pf-scardnew');
      add.addEventListener('click', () => { view.sel = '__new'; keep(); draw(); st.querySelector('.pf-editor')?.scrollIntoView?.({ block: 'nearest' }); });
      grid.appendChild(add);
    }
    sec.appendChild(grid);
    frag.appendChild(sec);
  }

  // 4) 그래프·전체 표·매매 기록(접음)
  let fold = null;
  if (result) {
    fold = el('details', 'pf-st-block pf-stfold');
    fold.open = !!view.fold;
    fold.addEventListener('toggle', () => { view.fold = fold.open; keep(); });
    fold.appendChild(el('summary', null, '누적 평가액 그래프 · 전체 비교 표 · 전략별 매매 기록'));
    frag.appendChild(fold);
  }

  // 앞부분(고정 안내·상태 줄)은 renderTabs가 이미 넣었다 — 그 뒤만 바꾼다
  st.querySelectorAll(':scope > .pf-rankpart').forEach((x) => x.remove());
  const wrap = el('div', 'pf-rankpart'); wrap.appendChild(frag); st.appendChild(wrap);
  // 그래프 폭은 탭 폭을 읽으므로 탭에 붙인 뒤 채운다
  if (fold) for (const sec of [compareSection, chartSection, detailSection]) fold.appendChild(sec(result, model.byId));
}

// 편집기 패널. id = 'A'|'REAL'|'__new'|시나리오 id, sc = 저장된 시나리오(없으면 null), r = 순위 줄
function editor(id, sc, r, b, result, handlers, close, count, st) {
  const isNew = id === '__new';
  if (!isNew && !AUTO.has(id) && !sc) return null;
  const panel = el('section', 'pf-st-block pf-editor');
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
    panel.appendChild(tradesLink(id, result, st));
    return panel;
  }
  if (!b) { panel.appendChild(el('p', 'pf-note', '전략 비교를 시작한 뒤(기록·관리 탭의 시작 스냅샷) 전략을 만들 수 있습니다.')); return panel; }

  const base = sc ? (sc.strategy === 'B' ? 'custom' : sc.strategy) : null;
  const d = draftOf(sc && sc.strategy === 'B' ? { strategy: 'custom', params: { ...sc.params, buyTiers: BUY_PRINCIPLE } } : sc);
  const body = el('div', 'pf-edbody');
  const left = el('div', 'pf-edleft'), right = el('div', 'pf-edright');
  const nameL = el('label', 'pf-field'); nameL.appendChild(el('span', null, '이름'));
  const name = el('input'); name.maxLength = NAME_MAX; name.value = sc?.name || ''; nameL.appendChild(name); left.appendChild(nameL);
  const sentence = el('p', 'pf-edsent');
  const msg = msgLine();
  const sync = () => { sentence.textContent = sentenceOf(base, d); };

  const tierBox = el('fieldset', 'pf-edgroup'); tierBox.appendChild(el('legend', null, '살 판정 · 원칙 1'));
  const chips = el('div', 'pf-tierchips');
  for (const t of ALL_TIERS) {
    const c = btn(t, 'pf-tierchip'); c.setAttribute('aria-pressed', String(d.tiers.includes(t)));
    c.addEventListener('click', () => { d.tiers = d.tiers.includes(t) ? d.tiers.filter((y) => y !== t) : [...d.tiers, t]; c.setAttribute('aria-pressed', String(d.tiers.includes(t))); sync(); });
    chips.appendChild(c);
  }
  tierBox.appendChild(chips); left.appendChild(tierBox);
  // 저장된 값이 버튼에 없으면(예전 양식으로 넣은 33% 등) 그 값도 버튼으로 둔다
  const seg = (title, key, opts, unit) => {
    const g = el('fieldset', 'pf-edgroup'); g.appendChild(el('legend', null, title));
    const row = el('div', 'pf-seg pf-segbox');
    for (const v of [...new Set([...opts, d[key]])].sort((p, q) => p - q)) {
      const o = btn(v + unit, 'pf-segbtn'); o.setAttribute('aria-pressed', String(d[key] === v));
      o.addEventListener('click', () => { d[key] = v; row.querySelectorAll('button').forEach((y) => y.setAttribute('aria-pressed', String(y === o))); sync(); });
      row.appendChild(o);
    }
    g.appendChild(row); left.appendChild(g);
  };
  seg('고평가가 되면 파는 비율 · 원칙 2·3', 'sell', SELL_OPTS, '%');
  seg('몇 번에 나눠 살까 · 원칙 5', 'rounds', ROUND_OPTS, '회');
  seg('남겨 둘 현금 · 원칙 7', 'reserve', RESERVE_OPTS, '%');

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
    const fold = st.querySelector('.pf-stfold'); if (!fold) return;
    fold.open = true;
    const d = fold.querySelectorAll('.pf-st-detail')[k];
    if (d) { d.open = true; d.scrollIntoView?.({ block: 'start' }); }
  });
  return a;
}
