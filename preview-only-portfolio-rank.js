// preview 전용 Portfolio 탭 — 전략 비교 하위 탭(2026-10-21 사용자 선택: 디자인 시안 "B 순위 + C 편집기 + B 카드"). 라이브로 옮기지 않는다 — pipeline/site_ui/UI_DIFF.md 1절 portfolio.
//
// 위: 수익률 순위(줄을 누르면 바로 아래에 편집기), 가운데: 내 전략 카드(수정 → 같은 편집기), 아래: 그래프·전체 표·매매 기록(접음).
// 편집기는 살 판정 칩과 매도 비율·회차·현금 유보 버튼으로 고치고, 고른 값을 문장으로 보여 준다. 저장은 handlers(scenario·editScenario·deleteScenario).
// 저평가만(C)·갈아타기(D)는 값을 바꾸지 않으면 그 전략 그대로 저장하고, 바꾸면 사용자 정의로 저장한다(C는 매도 알림을 남기지 않아 사용자 정의와 다르다).
// 순수 함수(draftOf·shapeOf·sentenceOf·rankRows)는 node 시험이 부른다(pipeline/portfolio/test_strategy_view.mjs).
import { el, msgLine, twoStep, usd, pct, pp, label, summarize, paramsText, checkScenario, MAX_SCENARIOS, NAME_MAX, ETF_ORDER,
  compareSection, chartSection, detailSection } from './preview-only-portfolio-strategy.js?v=27';
import { BUY_PRINCIPLE, BASELINES, followsPrinciple } from './preview-only-portfolio-engine.js?v=14';

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
  if (!sc) return { kind: 'verdict', tiers: [...BUY_PRINCIPLE], sell: 0, rounds: 4, reserve: 0, mode: 'split', ...etfDefault() };
  const p = sc.params || {};
  if (sc.strategy === 'E') return { ...draftOf(null), kind: 'etf', etfShare: toPct(p.etfShare ?? 1), etfs: ETFS.filter((e) => (p.etfs || ETFS).includes(e)) };
  // 원칙과 같은 살 판정(옛 판 포함)은 지금 원칙으로 보여 준다 — 엔진도 달마다 그달 원칙으로 계산(2026-10-28)
  const tiers = sc.strategy === 'custom' && !followsPrinciple(p.buyTiers) ? [...(p.buyTiers || [])] : sc.strategy === 'C' ? [...C_TIERS] : [...BUY_PRINCIPLE];
  const sell = sc.strategy === 'D' ? 100 : sc.strategy === 'C' ? 0 : toPct(p.sellFraction || 0);
  return { kind: 'verdict', tiers, sell, rounds: p.splitWeeks || 4, reserve: toPct(p.cashReserve || 0), mode: ['rank1', 'cap', 'tier'].includes(p.buyMode) ? p.buyMode : 'split', ...etfDefault() };
}

const sameSet = (a, b) => a.length === b.length && a.every((t) => b.includes(t));
// 편집기 값 → 저장할 {strategy, params}. base = 고치기 전 전략('C'|'D'|'B'|'custom'|null)
export function shapeOf(base, d) {
  if (d.kind === 'etf') return { strategy: 'E', params: { etfShare: fromPct(d.etfShare), etfs: BASELINES.filter((e) => d.etfs.includes(e)) } };
  const common = { splitWeeks: d.rounds, cashReserve: fromPct(d.reserve) };
  const rank1 = ['rank1', 'cap', 'tier'].includes(d.mode);   // 균등이 아닌 방법은 직접 만든 전략(custom)에서만 — 균등이면 칸을 두지 않아 예전 전략과 같은 값
  if (!rank1 && base === 'C' && sameSet(d.tiers, C_TIERS) && d.sell === 0) return { strategy: 'C', params: common };
  if (!rank1 && base === 'D' && sameSet(d.tiers, BUY_PRINCIPLE) && d.sell === 100) return { strategy: 'D', params: common };
  return { strategy: 'custom', params: { buyTiers: ALL_TIERS.filter((t) => d.tiers.includes(t)), sellFraction: fromPct(d.sell), ...common, ...(rank1 ? { buyMode: d.mode } : {}) } };
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
  const buy = d.mode === 'rank1'
    ? `매달 1일 판정이 ${tiers.length ? tiers.join('·') : '(없음)'}인 종목을 판정 순(같으면 기업 점수 순)으로 ${d.rounds === 1 ? '한 번에' : d.rounds + '주에 걸쳐'} 1주씩 이어서 삽니다. 1주 값이 모자라면 그 회차는 멈추고 남은 돈은 다음 회차로 넘깁니다. 그달 남은 돈으로도 1주가 안 되는 종목은 건너뜁니다.`
    : `매달 1일 판정이 ${tiers.length ? tiers.join('·') : '(없음)'}인 종목을 ${d.mode === 'cap' ? '시가총액 비례로' : d.mode === 'tier' ? '판정 무게(초저평가 3 : 저평가 2 : 적정~저평가 1, 10월 계획까지는 적정 포함 4:3:2:1) 비례로' : '똑같이'} 나눠 ${d.rounds === 1 ? '한 번에' : d.rounds + '주에 걸쳐'} 삽니다.`
      + (d.mode === 'cap' ? ' 시가총액을 모르는 종목은 그달 사지 않고 그 몫은 나머지에 돌아갑니다.' : d.mode === 'tier' ? ' 그 밖의 판정은 무게가 없어 사지 않습니다.' : '');
  // 매도(2026-10-28 사용자 결정, 11월 계획부터 매주 회차일에 판정을 본다): 원칙과 같은 살 판정 + 비율 0%면 원칙 4(고평가면 전부를 남은 회차에 나눠, 초고평가면 한 번에)
  const principleSell = !d.sell && shape.strategy !== 'C' && followsPrinciple(d.tiers);
  const sell = d.sell ? `판정이 고평가·초고평가가 되면 남은 수량의 ${d.sell}%를 팝니다(11월부터 매주 회차일에 봅니다).`
    : shape.strategy === 'C' ? '팔지 않습니다.'
    : principleSell ? '11월부터 매주 회차일에 판정을 보고, 고평가면 전부를 그달 남은 회차에 나눠 팔고 초고평가면 남은 것을 한 번에 팝니다(원칙 4). 10월까지는 알림만이었습니다.'
    : '고평가가 되어도 팔지 않고 매도 검토 알림만 남깁니다.';
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
      twr: m.twr, twrSince: s.twrSince ?? null, spy: m.vs ? m.vs.SPY ?? null : null, value: m.value, trades: m.trades, cashShare: m.cashShare, wait: m.waitText };
  });
  const key = (r) => (sort === 'spy' ? r.spy : sort === 'value' ? r.value : r.twr);
  return rows.sort((a, b) => {
    if ((a.id === 'REAL') !== (b.id === 'REAL')) return a.id === 'REAL' ? -1 : 1;   // 내 실제 계좌는 늘 맨 위(사용자 요청 2026-10-28), 나머지만 순위
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

// 전략 비교 판(2026-11-20 정리). rows = rankRows 결과, sort = 'twr'|'spy'|'value'.
// 큰 숫자 v = 새 비교 시작 뒤 수익률(twrSince). 값이 있는 줄 가운데 하나라도 twrSince가 없으면 모든 줄을 처음부터의 twr로 본다(기간이 다른 값을 견주지 않게) — since가 그 구분.
// 내 실제 계좌는 늘 맨 앞이고 순위를 매기지 않는다.
// 순위는 화면에 적히는 값이 같으면 같은 순위(1, 2, 2, 4). diff = 내 계좌와의 차이(%p, 소수 둘째 자리로 반올림 — 화면 글과 같게),
// tag = '앞섬'(+1%p 이상)|'뒤짐'(−1%p 이하)|'비슷'|'기준'(내 계좌)|null(내 계좌나 값이 없어 견줄 수 없음)
export function boardOf(rows, sort) {
  const since = rows.some((r) => r.twrSince != null) && rows.every((r) => r.twr == null || r.twrSince != null);
  const v = (r) => (since ? r.twrSince ?? null : r.twr);
  const key = (r) => (sort === 'spy' ? r.spy : sort === 'value' ? r.value : v(r));
  const text = (r) => (sort === 'spy' ? pp(r.spy) : sort === 'value' ? usd(r.value) : pct(v(r)));
  const real = rows.find((r) => r.id === 'REAL') || null, rv = real ? v(real) : null;
  const rest = rows.filter((r) => r.id !== 'REAL').sort((x, y) => {
    const a = key(x), b = key(y);
    if (a == null || b == null) return a == null && b == null ? x.idx - y.idx : a == null ? 1 : -1;
    return b - a || x.idx - y.idx;
  });
  let n = 0, prev = null, rank = 0;
  const cards = rest.map((r) => {
    let rk = null;
    if (key(r) != null) { n++; const t = text(r); if (t !== prev) { rank = n; prev = t; } rk = rank; }
    const diff = rv == null || v(r) == null ? null : Math.round((v(r) - rv) * 1e4) / 100;
    return { ...r, v: v(r), rank: rk, diff, tag: diff == null ? null : diff >= 1 ? '앞섬' : diff <= -1 ? '뒤짐' : '비슷' };
  });
  if (real) cards.unshift({ ...real, v: rv, rank: null, diff: null, tag: '기준' });
  return { cards, real: real ? cards[0] : null, since };
}

// 맨 위 큰 숫자 칸(자동 문구 — 어떤 값에서도 참인 말만). board = boardOf 결과. 값이 있는 줄만 센다.
// [{ k: 작은 제목, big: 큰 숫자, sub: 한 줄, v: 색을 정할 값|null, lead: 강조 칸 }]
export function heroCards(board) {
  const out = [], real = board.real, ok = board.cards.filter((c) => c.id !== 'REAL' && c.v != null);
  const dtxt = (d) => (d == null ? '' : d > 0 ? `내 계좌보다 ${d.toFixed(2)}%p 앞섬` : d < 0 ? `내 계좌보다 ${(-d).toFixed(2)}%p 뒤짐` : '내 계좌와 같음');
  if (real) {
    const cmp = ok.filter((c) => c.diff != null), up = cmp.filter((c) => c.diff > 0).length, down = cmp.filter((c) => c.diff < 0).length, m = cmp.length;
    out.push({ k: '내 실제 계좌', big: pct(real.v), v: real.v, lead: false,
      sub: real.v == null || !m ? '' : m === 1 ? (up ? '다른 전략 1개가 앞서 있음' : down ? '다른 전략 1개가 뒤져 있음' : '다른 전략 1개와 같음')
        : up === m ? `다른 전략 ${m}개가 모두 앞서 있음` : down === m ? `다른 전략 ${m}개가 모두 뒤져 있음` : `다른 전략 ${m}개 중 ${up}개가 앞서 있음` });
  }
  if (!ok.length) return out;
  const best = ok.reduce((a, c) => (c.v > a.v ? c : a), ok[0]);
  out.push({ k: (ok.length > 1 ? '다른 전략 중 수익률 1위 · ' : '') + best.name, big: pct(best.v), v: best.v, sub: dtxt(best.diff), lead: true });
  const others = ok.filter((c) => c !== best);
  if (others.length === 1) out.push({ k: others[0].name, big: pct(others[0].v), v: others[0].v, sub: dtxt(others[0].diff), lead: false });
  else if (others.length) {
    const vs = others.map((c) => c.v), lo = Math.min(...vs), hi = Math.max(...vs);
    const ds = others.map((c) => c.diff).filter((d) => d != null), dlo = ds.length ? Math.min(...ds) : null, dhi = ds.length ? Math.max(...ds) : null;
    const span = (x, y) => (x.toFixed(2) === y.toFixed(2) ? x.toFixed(2) : `${x.toFixed(2)}~${y.toFixed(2)}`);
    out.push({ k: `나머지 전략 ${others.length}개`, big: pct(lo) === pct(hi) ? pct(lo) : `${pct(lo)} ~ ${pct(hi)}`, v: hi < 0 ? hi : lo > 0 ? lo : null, lead: false,
      sub: dlo == null ? '' : dlo > 0 ? `내 계좌보다 ${span(dlo, dhi)}%p 앞섬` : dhi < 0 ? `내 계좌보다 ${span(-dhi, -dlo)}%p 뒤짐` : dlo === 0 && dhi === 0 ? '내 계좌와 같음' : dlo === 0 ? `내 계좌와 같거나 최대 ${dhi.toFixed(2)}%p 앞섬` : dhi === 0 ? `내 계좌와 같거나 최대 ${(-dlo).toFixed(2)}%p 뒤짐` : '내 계좌 앞뒤로 갈림' });
  }
  return out;
}

// 점 그래프: 0%(본전)를 꼭 넣은 눈금 위에 줄마다 점 하나. { lo, hi, zero: 0%의 자리(0~100), dots: [{ id, name, slot, v, pos(0~100), real }] } — 값 없는 줄은 뺀다
export function dotScale(cards) {
  const ok = cards.filter((c) => c.v != null);
  if (!ok.length) return null;
  let lo = Math.min(0, ...ok.map((c) => c.v)), hi = Math.max(0, ...ok.map((c) => c.v));
  if (hi - lo < 1e-9) { lo -= 0.01; hi += 0.01; }
  const pos = (x) => ((x - lo) / (hi - lo)) * 100;
  return { lo, hi, zero: pos(0), dots: ok.map((c) => ({ id: c.id, name: c.name, slot: c.slot, v: c.v, pos: pos(c.v), real: c.id === 'REAL' })) };
}

// 여러 전략의 설정 글(paramsText)에서 모두에게 같은 조각과 전략마다 다른 조각을 나눈다. texts = { id: 'a · b · c' }
// 전략이 둘 이상이고 같은 조각이 있을 때만 common을 채운다. { common: [조각], own: { id: [조각] } }
export function splitParams(texts) {
  const ids = Object.keys(texts), parts = Object.fromEntries(ids.map((id) => [id, texts[id].split(' · ')]));
  const common = ids.length < 2 ? [] : parts[ids[0]].filter((t) => ids.every((id) => parts[id].includes(t)));
  return { common, own: Object.fromEntries(ids.map((id) => [id, parts[id].filter((t) => !common.includes(t))])) };
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
  const open = (id, seed) => { view.sel = id; view.seed = seed || null; keep(); draw(); const ed = st.querySelector('.pf-editor'); if (ed) { ed.tabIndex = -1; ed.focus?.({ preventScroll: true }); ed.scrollIntoView?.({ block: 'nearest' }); } };
  const canAdd = !!b && scen.length < MAX_SCENARIOS;
  const byRow = new Map(rows.map((r) => [r.id, r]));
  const frag = document.createDocumentFragment();

  const md = (d) => (d ? `${+d.slice(5, 7)}/${d.slice(8, 10)}` : '');
  const tone = (v) => (v == null ? '' : v >= 0 ? ' pf-up' : ' pf-down');
  const board = result ? boardOf(rows, view.sort) : { cards: [], real: null, since: false };
  const sinceT = smodel.startDay ? md(smodel.startDay) + '부터' : '', fromT = smodel.from ? md(smodel.from) + '부터' : '처음부터';
  const twoSpans = board.since;   // 큰 숫자가 새 비교 시작 뒤 수익률인가(그러면 처음부터의 수익률은 카드 안 작은 칸에)
  const spanT = twoSpans && sinceT ? sinceT : fromT;

  // 1) 큰 숫자 칸과 점 그래프(2026-11-20 정리 — 디자인 시안 Strategy)
  if (result) {
    const sec = el('section', 'pf-panel pf-s2hero');
    sec.appendChild(el('div', 'pf-eyebrow2', '같은 출발점, 다른 선택' + (twoSpans && sinceT ? ` · ${sinceT}` : '')));
    const hero = heroCards(board);
    if (hero.length) {
      const hg = el('div', 'pf-s2stats');
      for (const h of hero) {
        const c = el('div', 'pf-s2stat' + (h.lead ? ' pf-s2lead' : ''));
        c.appendChild(el('span', 'pf-ac2k', h.k)); c.appendChild(el('strong', 'pf-s2big' + (h.lead ? '' : tone(h.v)), h.big)); if (h.sub) c.appendChild(el('span', 'pf-s', h.sub));
        hg.appendChild(c);
      }
      sec.appendChild(hg);
    }
    const sc0 = dotScale(board.cards);
    if (sc0) {
      const box = el('div', 'pf-s2dots');
      const track = el('div', 'pf-s2track'); track.setAttribute('role', 'img');
      track.setAttribute('aria-label', '수익률 점 그래프: ' + sc0.dots.map((d) => `${d.name} ${pct(d.v)}`).join(', '));
      const zero = el('i', 'pf-s2zero'); zero.style.left = sc0.zero + '%'; track.appendChild(zero);
      // 내 계좌 점은 크게, 맨 위에 그린다(겹쳐도 보이게)
      for (const d of [...sc0.dots].sort((x, y) => x.real - y.real)) {
        const e = el('i', 'pf-s2dot' + (d.real ? ' pf-s2me' : '') + (d.slot ? ' pf-c' + d.slot : '')); e.style.left = d.pos + '%'; e.title = `${d.name} ${pct(d.v)}`; track.appendChild(e);
      }
      box.appendChild(track);
      const ax = el('div', 'pf-s2axis');
      ax.appendChild(el('span', null, sc0.lo === 0 ? '0% (본전)' : pct(sc0.lo)));
      if (sc0.zero > 12 && sc0.zero < 88) { const z = el('span', 'pf-s2axz', '0% (본전)'); z.style.left = sc0.zero + '%'; ax.appendChild(z); }
      ax.appendChild(el('span', null, sc0.hi === 0 ? '0% (본전)' : pct(sc0.hi)));
      box.appendChild(ax);
      const lg = el('div', 'pf-s2legend');
      for (const d of sc0.dots) { const it = el('span'); it.appendChild(dot(d.slot)); it.appendChild(document.createTextNode(`${d.name} ${pct(d.v)}`)); lg.appendChild(it); }
      box.appendChild(lg);
      sec.appendChild(box);
    }
    frag.appendChild(sec);
  }

  // 2) 전략별로 보기: 줄마다 카드 하나(내 실제 계좌가 맨 앞). 누르면 바로 아래에서 고친다
  if (result || b) {
    const head = el('div', 'pf-s2head');
    const h2 = el('h2', 'pf-h2q', '전략별로 보기');
    const basis = { spy: 'SPY 대비', value: '평가액' }[view.sort];
    if (b || basis) h2.appendChild(el('small', null, [b && ` 모의 전략 ${scen.length} / ${MAX_SCENARIOS}`, basis && ` 순위는 ${basis} 순`].filter(Boolean).join(' ·')));
    head.appendChild(h2);
    if (result) {
      const sorts = el('div', 'pf-seg pf-segbox'); sorts.setAttribute('role', 'group'); sorts.setAttribute('aria-label', '정렬 기준');
      for (const [k, t] of [['twr', '수익률(TWR)'], ['spy', 'SPY 대비'], ['value', '평가액']]) {
        const x = btn(t, 'pf-segbtn'); x.setAttribute('aria-pressed', String(view.sort === k));
        x.dataset.sort = k;
        x.addEventListener('click', () => { view.sort = k; keep(); draw(); latest[0].querySelector(`.pf-s2head [data-sort="${k}"]`)?.focus?.(); });
        sorts.appendChild(x);
      }
      head.appendChild(sorts);
    }
    if (canAdd) { const add = btn('＋ 새 전략', 'pf-btn pf-s2add'); add.addEventListener('click', () => open('__new')); head.appendChild(add); }
    frag.appendChild(head);
    const texts = Object.fromEntries(scen.filter(([, x]) => x.strategy !== 'E').map(([id, x]) => [id, paramsText(x)]));
    const sp = splitParams(texts);
    const how = (c) => {
      if (c.id === 'REAL') return '내가 실제로 사고판 기록';
      if (c.id === 'A') return '시작 스냅샷을 그대로 들고 입금만 더함';
      const x = scen.find(([id]) => id === c.id)?.[1];
      if (!x) return '';
      return (sp.own[c.id] ? (sp.own[c.id].length ? sp.own[c.id] : ['공통 설정 그대로']) : paramsText(x).split(' · ')).join(' · ');
    };
    const grid = el('div', 'pf-s2cards');
    // 결과가 아직 없는 전략(방금 만든 것 등)도 카드로 보인다
    const list = [...board.cards, ...scen.filter(([id]) => !byRow.has(id)).map(([id, x]) => ({ id, name: x.name, v: null, rank: null, diff: null, tag: null, pending: true }))];
    for (const c of list) {
      const card = el('div', 'pf-s2card' + (c.id === 'REAL' ? ' pf-s2mine' : '') + (view.sel === c.id ? ' pf-on' : ''));
      const top = el('div', 'pf-s2top');
      const rk = el('span', 'pf-s2rank' + (c.rank === 1 ? ' pf-s2first' : ''), c.id === 'REAL' ? '나' : c.rank == null ? '–' : String(c.rank));
      if (c.id !== 'REAL') rk.setAttribute('aria-label', c.rank == null ? '순위 없음' : `${{ spy: 'SPY 대비 ', value: '평가액 ' }[view.sort] || '수익률 '}${c.rank}위`);
      top.appendChild(rk);
      const nm = el('strong', 'pf-s2name'); nm.appendChild(dot(c.slot)); nm.appendChild(document.createTextNode(c.name)); top.appendChild(nm);
      if (c.tag) top.appendChild(el('span', 'pf-s2tag' + (c.tag === '앞섬' ? ' pf-s2ahead' : c.tag === '뒤짐' ? ' pf-s2behind' : ''), c.tag));
      card.appendChild(top);
      const main = el('div', 'pf-s2main');
      main.appendChild(el('span', 'pf-s', c.pending ? '아직 계산 전' : spanT + ' · TWR'));
      main.appendChild(el('strong', 'pf-s2num' + tone(c.v), c.pending ? '—' : pct(c.v)));
      card.appendChild(main);
      card.appendChild(el('p', 'pf-s2how', how(c)));
      if (c.wait) card.appendChild(el('p', 'pf-warn', c.wait));
      if (!c.pending) {
        const g = el('div', 'pf-s2grid');
        const cell = (k, t, cls) => { const d = el('div'); d.appendChild(el('span', 'pf-s', k)); d.appendChild(el('strong', cls || null, t)); g.appendChild(d); };
        if (twoSpans) cell(fromT, pct(c.twr), tone(c.twr).trim());
        cell('SPY 대비', pp(c.spy), tone(c.spy).trim());
        cell('평가액', usd(c.value));
        cell('체결', c.trades + '건');
        cell('현금', c.cashShare != null ? (c.cashShare * 100).toFixed(1) + '%' : '—');
        if (c.id !== 'REAL' && board.real) cell('내 계좌 대비', c.diff == null ? '—' : pp(c.diff));
        card.appendChild(g);
      }
      const go = btn(AUTO.has(c.id) ? (view.sel === c.id ? '설명 닫기' : '설명 보기') : (view.sel === c.id ? '설정 닫기' : '설정 열기'), 'pf-btn pf-btn-quiet pf-s2open');
      go.setAttribute('aria-label', `${c.name} ${go.textContent}`); go.setAttribute('aria-expanded', String(view.sel === c.id)); go.dataset.id = c.id;
      go.addEventListener('click', () => { if (view.sel === c.id) { view.sel = null; keep(); draw(); latest[0].querySelector(`.pf-s2open[data-id="${CSS.escape(c.id)}"]`)?.focus?.(); } else open(c.id); });
      card.appendChild(go);
      grid.appendChild(card);
    }
    if (list.length) frag.appendChild(grid);
    if (b && !scen.length) frag.appendChild(el('p', 'pf-note', '아직 만든 전략이 없습니다. "＋ 새 전략"으로 만듭니다.'));
    if (sp.common.length) {
      const cm = el('div', 'pf-s2common');
      cm.appendChild(el('strong', null, `판정 전략 ${Object.keys(texts).length}개의 공통 설정`));
      for (const t of sp.common) cm.appendChild(el('span', null, t));
      frag.appendChild(cm);
    }
  }

  // 3) 편집기(고른 카드 또는 새 전략) — 카드 묶음 바로 아래
  if (view.sel) {
    const sc = scen.find(([id]) => id === view.sel);
    const panel = editor(view.sel, sc ? sc[1] : null, byRow.get(view.sel), b, result, handlers, () => { view.sel = null; keep(); draw(); }, scen.length, st,
      canAdd ? (seed) => open('__new', seed) : null);
    if (panel) frag.appendChild(panel);
  }

  // 한 줄 안내와 계산 설명(접음)
  if (result) {
    const spy = spyLine(result);
    frag.appendChild(el('p', 'pf-note pf-s2note', (smodel.since ? smodel.since + ' ' : '') + (spy != null ? `같은 기간(${fromT}) SPY ${pct(spy)}. ` : '')
      + '수익률은 입출금 영향을 뺀 시간가중수익률(TWR)입니다. 순위는 고른 정렬 기준으로 매기고, 적힌 값이 같으면 같은 순위입니다.'));
    const hd = el('details', 'pf-ac2how pf-s2help'); hd.open = !!view.help;
    hd.addEventListener('toggle', () => { view.help = hd.open; keep(); });
    hd.appendChild(el('summary', null, '계산 설명'));
    hd.appendChild(el('p', 'pf-note', '모든 전략은 시작 스냅샷에서 같이 출발하고, 입금은 반영일부터 모든 전략에 같이 들어갑니다. ' + `점 그래프와 카드의 큰 숫자는 ${spanT} 수익률입니다.`));
    hd.appendChild(el('p', 'pf-note', `카드의 "SPY 대비"는 ${fromT}, "내 계좌 대비"는 큰 숫자와 같은 기간의 차이입니다. ` + 'SPY 대비는 같은 출발 시점·평가액에서 SPY만 산 경우와의 차이입니다. 종목 선택뿐 아니라 현금 유보·나눠 사기 시점의 효과도 섞여 있어 판정 신호의 성과로 읽지 않습니다.'));
    if (smodel.info) hd.appendChild(el('p', 'pf-note', smodel.info));
    frag.appendChild(hd);
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
  const modeBox = el('fieldset', 'pf-edgroup'); modeBox.appendChild(el('legend', null, '어떻게 살까'));
  const modeRow = el('div', 'pf-seg pf-segbox');
  for (const [v, t] of [['split', '균등'], ['cap', '시총 비중'], ['tier', '판정 가중'], ['rank1', '순위 1주씩']]) {
    const o = btn(t, 'pf-segbtn'); o.setAttribute('aria-pressed', String((d.mode ?? 'split') === v));
    o.addEventListener('click', () => { d.mode = v; modeRow.querySelectorAll('button').forEach((y) => y.setAttribute('aria-pressed', String(y === o))); sync(); });
    modeRow.appendChild(o);
  }
  modeBox.appendChild(modeRow); verdictPart.appendChild(modeBox);
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
