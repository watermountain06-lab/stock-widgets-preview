// preview 전용 Portfolio 탭 — 전략 비교 화면(2026-10-20, 3단계). 라이브로 옮기지 않는다 — pipeline/site_ui/UI_DIFF.md 1절 portfolio.
//
// 설계: pipeline/portfolio/STRATEGY_DESIGN.md 7·8절. 계산은 preview-only-portfolio-engine.js(replay)가 하고, 이 파일은
// Firestore 묶음 문서 → 엔진 입력 변환, 결과 요약, 전략 비교·기록 관리 구역 그리기만 한다(하위 탭 배치는 -home.js). Firebase를 직접 부르지 않는다 — 저장은
// preview-only-portfolio.js가 넘겨 준 함수(handlers)로 한다. 그래서 순수 함수(toEngineInput·summarize)는 node 시험이 부른다
// (pipeline/portfolio/test_strategy_view.mjs).
//
// 개인 값(보유·현금·입금·시나리오 이름)은 콘솔·URL에 넣지 않는다. 모든 글자는 textContent로 넣는다.
import { depositTiming, isTradingDay, ENGINE_VERSION, BUY_PRINCIPLE, BASELINES } from './preview-only-portfolio-engine.js?v=1';

export const MAX_SCENARIOS = 20;
export const NAME_MAX = 40;
const ALL_TIERS = ['초저평가', '저평가', '적정~저평가', '적정', '고평가~적정', '고평가', '초고평가'];
export const STRATEGY = {
  A: '그대로 보유 + 입금 적립',
  B: '내 원칙(임시)',
  C: '저평가만 매수',
  D: '고평가면 팔고 갈아타기',
  custom: '사용자 정의',
};
const NOTE = {
  provisionalPrinciple: '임시 모형 — 매도 검토는 알림만 반영',
  noPrinciple7: '원칙 7(급락 대비 현금) 미반영',
  offPrinciple: '원칙과 다름',
};
export const REASON = {
  noInfo: '정보 없음', pipelineFailed: '그날 기록 없음·실패', noRecord: '그날 기록 없음', tierOut: '판정이 조건 밖',
  noCard: '카드 없음', noVerdict: '판정 없음', stale: '묵은 판정', ruleVersion: '판정 방식 변경', noPrice: '가격 없음',
  splitCheck: '분할 확인 필요', reserveUnknown: '평가 미확정(유보 계산 불가)', cashLimit: '현금 한도로 줄임',
  noShares: '보유 없음', pastNextCheck: '다음 점검일 지남', beyondCalendar: '달력 밖', halted: '평가 중단',
  notStarted: '출발 전', splitDelay: '분할 지연', corporateEvent: '지원하지 않는 기업 사건', notYet: '아직 시작 전',
  aUndetermined: '출발 상태 미확정',
};
export const FIXED_NOTICE = '모의 운용입니다. 판정은 수익 예측이 검증된 신호가 아닙니다. 카드 목록은 직접 고른 종목이라 결과를 일반화할 수 없습니다. 배당·세금·환율·큰 사건 예외 제외.';

// ---- 순수 함수 ----

// Firestore 묶음 문서(시각은 ISO 문자열로 바꾼 뒤) + 일별 기록 → 엔진 입력
export function toEngineInput(bundle, records) {
  const snap = bundle.snapshot || {};
  const deposits = Object.entries(bundle.deposits || {}).map(([id, d]) => (d.cancels
    ? { id, cancels: d.cancels, recordedAt: d.recordedAt }
    : { id, amount: d.amount, recordedAt: d.recordedAt }));
  const scenarios = Object.entries(bundle.scenarios || {})
    .sort(([, a], [, b]) => (a.createdAt < b.createdAt ? -1 : a.createdAt > b.createdAt ? 1 : 0))
    .map(([id, s]) => ({ id, name: s.name, strategy: s.strategy, params: s.params || undefined, createdAt: s.createdAt, engineVersion: s.engineVersion }));
  return {
    records,
    snapshot: { date: snap.date, holdings: snap.holdings || {}, cash: snap.cash || 0 },
    settings: { holdOnly: snap.holdOnly || [] },
    deposits,
    scenarios,
  };
}

// 출발하지 않은 시나리오가 왜 기다리는지 한 줄로. 엔진이 waiting을 주면 그것, 아니면(출발 평가 미확정) 마지막 날의 사유
// (예: noPrice:APPL → "출발 대기 — 가격 없음 APPL"). 가격 없음이면 카드 목록 밖이거나 티커 오타일 수 있다고 덧붙인다.
export function waitText(s) {
  if (s.started) return null;
  if (s.waiting) return REASON[s.waiting] || s.waiting;
  const d = [...(s.days || [])].reverse().find((x) => (x.why || []).some((w) => w !== 'notStarted'));
  const why = (d?.why || []).filter((w) => w !== 'notStarted');
  if (!why.length) return '아직 시작 전';
  const text = why.map((w) => { const [k, t] = w.split(':'); return (REASON[k] || k) + (t ? ' ' + t : ''); }).join(', ');
  return `출발 대기 — ${text}` + (why.some((w) => w.startsWith('noPrice:')) ? '(카드 목록 밖 종목이거나 티커 오타일 수 있음)' : '');
}

// 시나리오 결과 하나 → 비교 표 한 줄
export function summarize(s) {
  const tail = s.started ? s.days.filter((d) => d.date >= s.started) : [];
  const last = tail[tail.length - 1] || null;
  const lastKnown = [...tail].reverse().find((d) => d.value !== null) || null;
  const byTicker = {};
  for (const t of s.trades || []) byTicker[t.ticker] = (byTicker[t.ticker] || 0) + 1;
  return {
    id: s.id,
    started: s.started || null,
    waiting: s.waiting || null,
    waitText: waitText(s),
    halted: s.halted || null,
    asOf: last ? last.date : null,
    value: last ? last.value : null,
    lastKnown: lastKnown && last && lastKnown.date !== last.date ? { date: lastKnown.date, value: lastKnown.value } : null,
    deposits: last ? last.deposits : 0,
    pnl: last ? last.pnl : null,
    twr: last ? last.twr : null,
    vs: last ? last.vs || null : null,
    trades: (s.trades || []).length,
    tradesByTicker: byTicker,
    skipped: (s.skips || []).filter((x) => x.action !== 'carried').length,
    cashShare: last && last.value ? s.cash / last.value : null,
    elapsed: tail.length ? tail.length - 1 : 0,
    pause: last && last.pause ? last.pause : null,
    provisional: !!(last && last.provisional),
  };
}

// 시나리오 입력 검사(저장 전) — 틀리면 사유 문자열, 맞으면 null
export function checkScenario(sc, count) {
  if (count >= MAX_SCENARIOS) return `시나리오는 ${MAX_SCENARIOS}개까지입니다.`;
  const name = (sc.name || '').trim();
  if (!name) return '이름을 넣으세요.';
  if (name.length > NAME_MAX) return `이름은 ${NAME_MAX}자까지입니다.`;
  if (!['B', 'C', 'D', 'custom'].includes(sc.strategy)) return '전략을 고르세요.';
  const p = sc.params || {};
  if (sc.strategy === 'custom' && !(p.buyTiers || []).length) return '살 판정을 하나 이상 고르세요.';
  return null;
}

export const usd = (v) => (v == null ? '—' : '$' + v.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }));
export const pct = (v) => (v == null ? '미확정' : (v >= 0 ? '+' : '') + (v * 100).toFixed(2) + '%');
export const pp = (v) => (v == null ? '미확정' : (v >= 0 ? '+' : '') + v.toFixed(2) + '%p');
export const shares = (v) => v.toLocaleString('en-US', { maximumFractionDigits: 6 });

// ---- 그리기 도우미 ----
export function el(tag, cls, text) {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (text != null && text !== '') e.textContent = text;
  return e;
}
export function table(heads, rows, numCols = [], cards = false) {
  const wrap = el('div', 'pf-scroll'), t = el('table', cards ? 'pf-table pf-cards' : 'pf-table'), tr = el('tr');
  heads.forEach((h) => tr.appendChild(el('th', null, h)));
  const thead = el('thead'); thead.appendChild(tr); t.appendChild(thead);
  const tbody = el('tbody');
  if (!rows.length) {
    const r0 = el('tr'), td = el('td', 'pf-empty', '없습니다.');
    td.colSpan = heads.length; r0.appendChild(td); tbody.appendChild(r0);
  }
  rows.forEach((cells) => {
    const r = el('tr');
    cells.forEach((c, i) => {
      const td = el('td', numCols.includes(i) ? 'pf-num' : null);
      td.dataset.label = heads[i];   // 좁은 화면에서는 카드로 바꿔 칸 이름을 앞에 붙인다(pf-cards)
      if (c instanceof Node) td.appendChild(c); else td.textContent = c == null ? '' : String(c);
      r.appendChild(td);
    });
    tbody.appendChild(r);
  });
  t.appendChild(tbody); wrap.appendChild(t);
  return wrap;
}
export function msgLine() { const p = el('p', 'pf-note pf-st-msg'); p.setAttribute('role', 'status'); p.setAttribute('aria-live', 'polite'); return p; }
// 저장은 같은 버튼을 두 번 눌러야 한다(브라우저 확인 창을 쓰지 않는다 — preview-only-portfolio.js의 업로드와 같은 방식).
// watch(입력 칸을 담은 요소)를 주면 첫 클릭 뒤 입력이 바뀌거나 그 안의 다른 버튼(후보 고르기·줄 빼기 등)을 누를 때 확인을 풀어,
// 두 번째 클릭이 확인한 값만 저장하게 한다.
export function twoStep(btn, msg, firstText, action, watch) {
  let armed = false;
  const disarm = () => { if (armed) { armed = false; delete btn.dataset.armed; msg.textContent = ''; } };
  if (watch) {
    watch.addEventListener('input', disarm); watch.addEventListener('change', disarm);
    watch.addEventListener('click', (e) => { if (!btn.contains(e.target)) disarm(); }, true);
  }
  btn.addEventListener('click', async () => {
    if (!armed) { armed = true; msg.textContent = firstText; btn.dataset.armed = '1'; return; }
    armed = false; delete btn.dataset.armed;
    btn.disabled = true;
    try { await action(); } catch (e) { msg.textContent = e.message || '저장하지 못했습니다.'; } finally { btn.disabled = false; }
  });
}
export const label = (s, scenarioById) => (s.id === 'A' ? 'A. ' + STRATEGY.A : (scenarioById[s.id]?.name || s.id));

// ---- 그래프: 누적 평가액(전략 최대 4개 + 기준선 3개), 빈칸은 끊어서 그린다 ----
const SVG = 'http://www.w3.org/2000/svg';
function svgEl(tag, attrs) { const e = document.createElementNS(SVG, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); return e; }

function chart(series, baselines, width) {
  const box = el('div', 'pf-chart');
  const all = [...series, ...baselines];
  const dates = [...new Set(all.flatMap((s) => s.points.map((p) => p.date)))].sort();
  const vals = all.flatMap((s) => s.points.map((p) => p.value)).filter((v) => v != null);
  if (dates.length < 2 || !vals.length) { box.appendChild(el('p', 'pf-empty', '그래프는 기록이 이틀 이상 쌓이면 보입니다.')); return box; }
  // 그리는 폭을 실제 칸 폭에 맞춘다 — 좁은 화면에서 글자가 줄어들지 않게
  const W = Math.max(300, Math.min(680, Math.round(width || 680))), H = W < 500 ? 230 : 260, L = 60, R = 10, T = 12, B = 28;
  let lo = Math.min(...vals), hi = Math.max(...vals);
  if (hi === lo) { if (lo === 0) { lo = -1; hi = 1; } else { lo *= 0.98; hi *= 1.02; } }
  const padY = (hi - lo) * 0.08; lo -= padY; hi += padY;
  const x = (d) => L + ((W - L - R) * dates.indexOf(d)) / (dates.length - 1);
  const y = (v) => T + ((H - T - B) * (hi - v)) / (hi - lo);
  const svg = svgEl('svg', { viewBox: `0 0 ${W} ${H}`, class: 'pf-chart-svg', role: 'img', 'aria-label': '누적 평가액 그래프. 같은 값은 아래 비교 표에 있습니다.' });
  // 눈금(가로선 4개)
  for (let k = 0; k <= 4; k++) {
    const v = lo + ((hi - lo) * k) / 4, yy = y(v);
    svg.appendChild(svgEl('line', { x1: L, x2: W - R, y1: yy, y2: yy, class: 'pf-grid' }));
    const t = svgEl('text', { x: L - 6, y: yy + 4, class: 'pf-axis', 'text-anchor': 'end' });
    t.textContent = '$' + Math.round(v).toLocaleString('en-US');
    svg.appendChild(t);
  }
  // 날짜 눈금: 처음·끝과 달이 바뀌는 날
  dates.forEach((d, i) => {
    if (i === 0 || i === dates.length - 1 || d.slice(5, 7) !== dates[i - 1].slice(5, 7)) {
      const t = svgEl('text', { x: x(d), y: H - 8, class: 'pf-axis', 'text-anchor': i === 0 ? 'start' : i === dates.length - 1 ? 'end' : 'middle' });
      t.textContent = d.slice(5).replace('-', '/');
      svg.appendChild(t);
    }
  });
  const line = (s) => {
    let dpath = '', pen = false;
    for (const p of s.points) {
      if (p.value == null) { pen = false; continue; }
      dpath += (pen ? 'L' : 'M') + x(p.date).toFixed(1) + ' ' + y(p.value).toFixed(1);
      pen = true;
    }
    return svgEl('path', { d: dpath, class: 'pf-line ' + s.cls, fill: 'none' });
  };
  baselines.forEach((s) => svg.appendChild(line(s)));
  series.forEach((s) => svg.appendChild(line(s)));
  // 마우스를 올리면 그날 값
  const cross = svgEl('line', { y1: T, y2: H - B, class: 'pf-cross', visibility: 'hidden' });
  svg.appendChild(cross);
  const hit = svgEl('rect', { x: L, y: T, width: W - L - R, height: H - T - B, fill: 'transparent' });
  svg.appendChild(hit);
  const tip = el('div', 'pf-tip'); tip.hidden = true;
  const at = new Map(all.map((s) => [s, new Map(s.points.map((p) => [p.date, p.value]))]));
  hit.addEventListener('pointermove', (ev) => {
    const r = svg.getBoundingClientRect(), px = ((ev.clientX - r.left) / r.width) * W;
    const i = Math.max(0, Math.min(dates.length - 1, Math.round(((px - L) / (W - L - R)) * (dates.length - 1))));
    const d = dates[i], xx = x(d);
    cross.setAttribute('x1', xx); cross.setAttribute('x2', xx); cross.setAttribute('visibility', 'visible');
    tip.textContent = '';
    tip.appendChild(el('strong', null, d));
    if (all.every((s) => at.get(s).get(d) == null)) tip.appendChild(el('div', null, '그날 기록이 없거나 평가할 수 없습니다.'));
    else for (const s of all) {
      const row = el('div', 'pf-tip-row');
      row.appendChild(el('span', 'pf-sw ' + s.cls));
      row.appendChild(el('span', null, s.name + ' ' + usd(at.get(s).get(d) ?? null)));
      tip.appendChild(row);
    }
    tip.hidden = false;
    const left = (xx / W) * r.width;
    tip.style.left = Math.min(Math.max(left + 12, 0), r.width - 220) + 'px';
  });
  hit.addEventListener('pointerleave', () => { tip.hidden = true; cross.setAttribute('visibility', 'hidden'); });
  box.appendChild(svg); box.appendChild(tip);
  return box;
}

function legend(items) {
  const ul = el('ul', 'pf-legend');
  for (const it of items) {
    const li = el('li');
    if (it.toggle) {
      const lab = el('label'), cb = el('input');
      cb.type = 'checkbox'; cb.checked = it.on; cb.disabled = it.disabled;
      cb.addEventListener('change', () => it.toggle(cb.checked));
      lab.appendChild(cb); lab.appendChild(el('span', 'pf-sw ' + it.cls)); lab.appendChild(el('span', null, it.name));
      li.appendChild(lab);
    } else { li.appendChild(el('span', 'pf-sw ' + it.cls)); li.appendChild(el('span', null, it.name)); }
    ul.appendChild(li);
  }
  return ul;
}

export function compareSection(result, byId) {
  const sec = el('div', 'pf-st-block');
  sec.appendChild(el('h3', null, '비교'));
  const rows = result.scenarios.map((s) => {
    const m = summarize(s);
    const name = el('div');
    name.appendChild(el('strong', null, label(s, byId)));
    const tags = el('div', 'pf-tags');
    const tag = (t, warn) => tags.appendChild(el('span', warn ? 'pf-tag pf-tag-warn' : 'pf-tag', t));
    if (s.strategy && s.strategy !== 'A') tag(STRATEGY[s.strategy]);
    (s.notes || []).forEach((n) => tag(NOTE[n] || n, n === 'offPrinciple'));
    if (s.engineMismatch) tag(`만든 때 ${s.engineCreated || '?'}, 지금 ${ENGINE_VERSION}로 계산`, true);
    if (m.waitText) tag(m.waitText, true);
    if (m.halted) tag(`${m.halted.since}부터 평가 불가(${REASON[m.halted.reason] || m.halted.reason})`, true);
    if (m.pause) tag(`가격 없음 ${m.pause}일 — 비교 일시 중단`, true);
    if (m.provisional) tag('잠정');
    if (m.started && s.id !== 'A') tag(m.started + ' 출발');
    name.appendChild(tags);
    const valueCell = m.value == null && m.lastKnown ? `미확정 (${m.lastKnown.date} ${usd(m.lastKnown.value)})` : usd(m.value);
    return [
      name, valueCell, usd(m.deposits), m.pnl == null ? '미확정' : usd(m.pnl), pct(m.twr),
      ...BASELINES.map((e) => pp(m.vs ? m.vs[e] : null)),
      m.trades, m.skipped, m.cashShare == null ? '—' : (m.cashShare * 100).toFixed(1) + '%', m.elapsed,
    ];
  });
  sec.appendChild(table(['전략', '평가액', '누적 입금', '손익', '수익률(TWR)', 'SPY 대비', 'RSP 대비', 'QQQ 대비', '체결', '건너뜀', '현금 비중', '경과 거래일'],
    rows, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], true));
  sec.appendChild(el('p', 'pf-note', '기준선 대비는 같은 출발 시점·출발 평가액에서 SPY·RSP·QQQ만 산 경우와의 수익률 차이입니다. 종목 선택뿐 아니라 현금 유보·분할 매수 시점의 효과도 섞여 있어 판정 신호의 성과로 읽지 않습니다. 늦게 만든 시나리오는 자기 출발일 기준선과 비교합니다.'));
  return sec;
}

const SHOW_KEY = 'pf-st-show';
export function chartSection(result, byId) {
  const sec = el('div', 'pf-st-block');
  sec.appendChild(el('h3', null, '누적 평가액'));
  const scen = result.scenarios.filter((s) => s.started);
  // 색은 시나리오에 고정(만든 순서로 1~8번). 9번째부터는 그래프에 넣지 않고 표에서만 본다.
  const slot = new Map(result.scenarios.map((s, i) => [s.id, i < 8 ? i + 1 : null]));
  let show;
  try { show = JSON.parse(sessionStorage.getItem(SHOW_KEY) || 'null'); } catch (_) { show = null; }
  // 다른 묶음에서 고른 선택이 남아 있으면 지금 그릴 수 있는 것만 남긴다
  if (Array.isArray(show)) show = show.filter((id) => scen.some((s) => s.id === id && slot.get(id))).slice(0, 4);
  if (!Array.isArray(show) || !show.length) show = scen.filter((s) => slot.get(s.id)).slice(0, 4).map((s) => s.id);
  const body = el('div');
  const draw = () => {
    body.textContent = '';
    const on = scen.filter((s) => show.includes(s.id) && slot.get(s.id));
    const A = result.scenarios[0];
    const series = on.map((s) => ({ name: label(s, byId), cls: 'pf-c' + slot.get(s.id), points: s.days.filter((d) => d.date >= s.started) }));
    const bases = A.started ? BASELINES.map((e, k) => ({ name: e + '(A 출발 기준)', cls: 'pf-b' + (k + 1), points: A.baselines[e] || [] })) : [];
    body.appendChild(legend([
      ...scen.map((s) => ({
        name: label(s, byId), cls: slot.get(s.id) ? 'pf-c' + slot.get(s.id) : 'pf-cx', on: show.includes(s.id),
        disabled: !slot.get(s.id) || (!show.includes(s.id) && show.length >= 4),
        toggle: (v) => {
          show = v ? [...show, s.id] : show.filter((x) => x !== s.id);
          try { sessionStorage.setItem(SHOW_KEY, JSON.stringify(show)); } catch (_) { /* 저장 못 해도 화면은 그대로 */ }
          draw();
        },
      })),
      ...bases.map((x) => ({ name: x.name, cls: x.cls })),
    ]));
    body.appendChild(chart(series, bases, document.getElementById('pf-strategy')?.clientWidth));
    body.appendChild(el('p', 'pf-note', '한 번에 전략 4개까지 그립니다. 빈칸은 가격이 없거나 평가할 수 없는 날입니다. 정확한 값은 위 표에 있습니다.'));
  };
  draw();
  sec.appendChild(body);
  return sec;
}

export function detailSection(result, byId) {
  const sec = el('div', 'pf-st-block');
  sec.appendChild(el('h3', null, '매매 기록'));
  for (const s of result.scenarios) {
    const d = el('details', 'pf-st-detail');
    const m = summarize(s);
    d.appendChild(el('summary', null, `${label(s, byId)} — 체결 ${m.trades}건 · 건너뜀 ${m.skipped}건`));
    d.appendChild(el('h4', null, '지금 보유'));
    d.appendChild(table(['티커', '수량'], Object.entries(s.holdings || {}).map(([t, q]) => [t, shares(q)]).concat([['현금', usd(s.cash)]]), [1]));
    d.appendChild(el('h4', null, '체결'));
    d.appendChild(table(['날짜', '종목', '매매', '수량', '가격', '금액', '회차'],
      (s.trades || []).slice().reverse().map((t) => [t.date, t.ticker, t.side === 'buy' ? (t.kind === 'deposit' ? '매수(입금)' : '매수') : '매도',
        shares(t.shares), usd(t.price), usd(t.amount), t.round ? t.round + (t.provisional ? ' 잠정' : '') : '']), [3, 4, 5]));
    if ((s.skips || []).length) {
      d.appendChild(el('h4', null, '건너뛴 회차'));
      d.appendChild(table(['날짜', '종목', '매매', '회차', '사유', '처리', '몫'],
        s.skips.slice().reverse().map((x) => [x.date || '—', x.ticker, x.side === 'buy' ? '매수' : '매도', x.round, REASON[x.reason] || x.reason,
          { erased: '지움', carried: '다음 회차로', dropped: '버림' }[x.action] || x.action,
          x.amount != null ? usd(x.amount) : shares(x.shares) + '주']), [6]));
    }
    if ((s.months || []).length) {
      d.appendChild(el('h4', null, '월별 결정'));
      d.appendChild(table(['점검일', '결정일', '쓴 기록', '후보', '발동', '예산', '종목별 완료 회차', '쓰지 않은 몫'],
        s.months.slice().reverse().map((mo) => [mo.checkDate, mo.decisionDate, mo.record, mo.candidates.join(', ') || '없음',
          mo.ruleChanged ? '판정 방식 변경 — 그달 매매 없음' : (mo.fires || []).map((f) => f.skip ? `${f.ticker}(${REASON[f.skip] || f.skip})` : `${f.ticker} ${f.observed}${f.warnOnly ? ' ⚠ 알림만' : ''}`).join(', ') || '없음',
          usd(mo.budget),
          (mo.summary || []).map((x) => `${x.ticker} ${x.side === 'buy' ? '매수' : '매도'} ${x.roundsDone}회`).join(', '),
          (mo.summary || []).filter((x) => x.notUsed > 0).map((x) => `${x.ticker} ${x.side === 'buy' ? usd(x.notUsed) : shares(x.notUsed) + '주'}`).join(', ') || '—']), [5]));
    }
    const ev = (s.events || []).filter((e) => e.kind === 'decisionDropped' || e.kind === 'decisionPending');
    if (ev.length) {
      d.appendChild(el('h4', null, '결정하지 못한 점검일'));
      d.appendChild(table(['점검일', '사유'], ev.map((e) => [e.checkDate, e.kind === 'decisionPending' ? '정보를 기다리는 중' : (REASON[e.reason] || '다음 점검일까지 정보 없음')])));
    }
    sec.appendChild(d);
  }
  return sec;
}

export function depositSection(b, handlers, now) {
  const sec = el('div', 'pf-st-block');
  sec.appendChild(el('h3', null, '입금'));
  sec.appendChild(el('p', 'pf-note', '이번 달 실제로 넣은 금액을 기록합니다. 기록한 뒤 처음 오는 장 시작(동부 09:30) 전에 모든 전략과 기준선에 같이 들어갑니다. 반영 전에만 취소할 수 있고, 반영된 입금은 고칠 수 없습니다(그때는 묶음을 끝내고 새로 시작).'));
  const form = el('div', 'pf-row');
  const input = el('input'); input.type = 'number'; input.min = '0.01'; input.step = '0.01'; input.placeholder = '금액(USD)'; input.setAttribute('aria-label', '입금 금액(USD)');
  const btn = el('button', 'pf-btn', '기록'); btn.type = 'button';
  const msg = msgLine();
  form.appendChild(input); form.appendChild(btn);
  sec.appendChild(form); sec.appendChild(msg);
  twoStep(btn, msg, '같은 금액을 기록합니다. 맞으면 한 번 더 누르세요.', async () => {
    const v = Number(input.value);
    if (!(v > 0) || Math.round(v * 100) / 100 !== v) throw new Error('0보다 큰 금액을 센트 단위까지 넣으세요.');
    await handlers.deposit(v);
  }, form);
  const deps = Object.entries(b.deposits || {});
  // 취소는 반영일 09:30 ET 전에 기록된 것만 효력이 있다(엔진과 같은 기준). 늦은 취소는 엔진이 무시한다.
  const cancelAt = new Map();
  for (const [, d] of deps) if (d.cancels && d.recordedAt && (!cancelAt.has(d.cancels) || d.recordedAt < cancelAt.get(d.cancels))) cancelAt.set(d.cancels, d.recordedAt);
  const rows = deps.filter(([, d]) => !d.cancels).sort(([, x], [, y]) => (x.recordedAt < y.recordedAt ? 1 : -1)).map(([id, d]) => {
    const t = depositTiming(d.recordedAt);
    let state, action = '';
    const cAt = cancelAt.has(id) ? Date.parse(cancelAt.get(id)) : null;
    if (cAt != null && t.day && cAt < t.cancelBefore) state = '취소됨';
    else if (cAt != null) state = (t.day ? t.day + ' 반영' : '반영일 계산 불가') + '(취소가 반영 뒤라 무시됨)';
    else if (t.day && now < t.cancelBefore) {
      state = t.day + ' 반영 예정';
      const c = el('button', 'pf-btn pf-btn-quiet', '취소'); c.type = 'button';
      twoStep(c, msg, '이 입금을 취소합니다. 맞으면 취소를 한 번 더 누르세요.', () => {
        if (Date.now() >= t.cancelBefore) throw new Error('반영일 장이 이미 열려 취소할 수 없습니다. 새로고침하세요.');
        return handlers.cancel(id);
      });
      action = c;
    } else state = t.day ? t.day + ' 반영' : '반영일 계산 불가';
    return [d.recordedAt ? d.recordedAt.slice(0, 16).replace('T', ' ') + ' UTC' : '기록 중', usd(d.amount), state, action];
  });
  sec.appendChild(table(['기록 시각', '금액', '상태', ''], rows, [1], true));
  return sec;
}

export function scenarioForm(b, handlers) {
  const sec = el('div', 'pf-st-block');
  const n = Object.keys(b.scenarios || {}).length;
  sec.appendChild(el('h3', null, `시나리오 추가 (${n}/${MAX_SCENARIOS})`));
  sec.appendChild(el('p', 'pf-note', '만든 다음 거래일부터 "A. 그대로 보유"의 그 전날 상태에서 출발합니다. 만든 뒤에는 고칠 수 없고, 설정을 바꾸려면 새로 만듭니다. 매도 단계는 고평가·초고평가로 고정입니다.'));
  const f = el('div', 'pf-form');
  const field = (lab, input) => { const l = el('label', 'pf-field'); l.appendChild(el('span', null, lab)); l.appendChild(input); f.appendChild(l); return input; };
  const name = field('이름', el('input')); name.maxLength = NAME_MAX;
  const strat = field('전략', el('select'));
  for (const k of ['B', 'C', 'D', 'custom']) { const o = el('option', null, STRATEGY[k]); o.value = k; strat.appendChild(o); }
  const sell = field('매도 비율 %(남은 수량 기준)', el('input')); sell.type = 'number'; sell.min = '0'; sell.max = '100'; sell.step = '1'; sell.value = '0';
  const weeks = field('나눠 체결 횟수', el('select'));
  for (const k of [1, 2, 3, 4]) { const o = el('option', null, k + '회'); o.value = String(k); weeks.appendChild(o); }
  weeks.value = '4';
  const reserve = field('현금 유보 %', el('input')); reserve.type = 'number'; reserve.min = '0'; reserve.max = '50'; reserve.step = '1'; reserve.value = '0';
  const tiers = el('fieldset', 'pf-tiers');
  tiers.appendChild(el('legend', null, '살 판정'));
  const boxes = ALL_TIERS.map((t) => {
    const l = el('label'), c = el('input'); c.type = 'checkbox'; c.value = t; c.checked = BUY_PRINCIPLE.includes(t);
    l.appendChild(c); l.appendChild(el('span', null, t)); tiers.appendChild(l); return c;
  });
  f.appendChild(tiers);
  const hint = el('p', 'pf-note');
  f.appendChild(hint);
  const sync = () => {
    const s = strat.value;
    sell.disabled = !(s === 'B' || s === 'custom');
    if (s === 'C') sell.value = '0';
    if (s === 'D') sell.value = '100';
    tiers.hidden = s !== 'custom';
    hint.textContent = {
      B: '판정이 초저평가~적정인 종목만 삽니다. 매도 비율이 0%면 고평가 발동을 알림(⚠)으로만 남깁니다(원칙 2 비율 미정).',
      C: '판정이 초저평가·저평가인 종목만 삽니다. 팔지 않습니다.',
      D: '고평가·초고평가가 되면 남은 수량을 모두 팔고, 초저평가~적정 종목을 삽니다.',
      custom: '초저평가~적정 밖의 판정을 고르면 "원칙과 다름" 표시가 붙습니다.',
    }[s];
  };
  strat.addEventListener('change', sync); sync();
  const btn = el('button', 'pf-btn', '시나리오 만들기'); btn.type = 'button';
  const msg = msgLine();
  f.appendChild(btn); f.appendChild(msg);
  twoStep(btn, msg, '이 설정으로 만듭니다(고칠 수 없음). 맞으면 한 번 더 누르세요.', async () => {
    const s = strat.value, params = {};
    const pctNum = (inp, lo, hi, what) => {
      const v = Number(inp.value);
      if (!Number.isInteger(v) || v < lo || v > hi) throw new Error(`${what}은(는) ${lo}~${hi} 사이 정수 %로 넣으세요.`);
      return v / 100;
    };
    if (s === 'B' || s === 'custom') params.sellFraction = pctNum(sell, 0, 100, '매도 비율');
    params.splitWeeks = Number(weeks.value);
    params.cashReserve = pctNum(reserve, 0, 50, '현금 유보');
    if (s === 'custom') params.buyTiers = boxes.filter((c) => c.checked).map((c) => c.value);
    const sc = { name: name.value.trim(), strategy: s, params };
    const bad = checkScenario(sc, n);
    if (bad) throw new Error(bad);
    await handlers.scenario(sc);
  }, f);
  sec.appendChild(f);
  return sec;
}

export function bundleSection(b, model, handlers) {
  const sec = el('div', 'pf-st-block');
  const s = b.snapshot || {};
  sec.appendChild(el('h3', null, `시작 스냅샷 (묶음 ${model.bundleNo})`));
  sec.appendChild(el('p', 'pf-note', `${s.date} 장 마감 뒤 · 현금 ${usd(s.cash)}` + ((s.holdOnly || []).length ? ` · 그대로 두는 보유: ${s.holdOnly.join(', ')}` : '')));
  sec.appendChild(table(['티커', '수량'], Object.entries(s.holdings || {}).sort().map(([t, q]) => [t, shares(q)]), [1]));
  if (model.closedCount) sec.appendChild(el('p', 'pf-note', `끝낸 묶음 ${model.closedCount}개`));
  sec.appendChild(el('p', 'pf-note', '시작 스냅샷을 잘못 넣었거나 이미 반영된 입금이 틀렸으면 이 묶음을 끝내고 새 스냅샷으로 다시 시작합니다. 끝낸 묶음은 "정정으로 종료"로 남습니다.'));
  const btn = el('button', 'pf-btn pf-btn-quiet', '이 묶음 끝내기'); btn.type = 'button';
  const msg = msgLine();
  sec.appendChild(btn); sec.appendChild(msg);
  twoStep(btn, msg, '이 묶음을 끝냅니다(되돌릴 수 없음). 맞으면 한 번 더 누르세요.', () => handlers.close());
  return sec;
}

export function startForm(model, handlers, lastSession) {
  const sec = el('div', 'pf-st-block');
  sec.appendChild(el('h3', null, model.bundle?.closed ? '새 묶음 시작' : '전략 비교 시작'));
  const pre = model.prefill || null;
  sec.appendChild(el('p', 'pf-note', '시작일 장 마감 뒤의 실제 보유 수량과 현금을 증권사 거래 내역이나 앱 값으로 확인해 넣습니다. 저장한 뒤에는 고칠 수 없습니다.'
    + (pre ? ` 아래 칸은 올린 보유(${pre.asOf || '기준일 없음'})에 ${pre.upTo || '—'}까지 체결한 실제 매매를 더한 값으로 미리 채웠습니다(미국 거래소 USD 종목만 지원).`
      + (pre.cash == null || pre.cash < 0 ? ' 현금은 올린 보유에 없거나 계산이 음수라 비워 두었습니다. 직접 넣으세요.' : '') : '')));
  sec.appendChild(el('p', 'pf-warn', `일별 기록은 다음 날 오전(미국 동부)에 나옵니다. 그래서 시작일은 마지막 기록 날짜${lastSession ? `(${lastSession})` : ''}의 장 마감입니다. 증권사 앱이 그 뒤 날의 보유를 보여 주면, 그 뒤에 체결한 매매를 빼고 그날 마감 기준 수량·현금을 넣으세요.`));
  if (pre?.clipped?.length) sec.appendChild(el('p', 'pf-warn', `⚠ 보유보다 많이 판 기록 ${pre.clipped.length}건이 있어 미리 채운 수량이 실제와 다를 수 있습니다. 확인해 고치세요.`));
  const f = el('div', 'pf-form');
  const dl = el('label', 'pf-field'); dl.appendChild(el('span', null, '시작일(마지막 일별 기록 날짜)'));
  const date = el('input'); date.type = 'date'; date.value = lastSession || ''; date.min = date.max = lastSession || ''; dl.appendChild(date); f.appendChild(dl);
  const cl = el('label', 'pf-field'); cl.appendChild(el('span', null, '현금(USD)'));
  // 현금을 모르거나(올린 보유에 현금 줄 없음) 계산이 음수면 빈칸으로 두고 직접 넣게 한다
  const cash = el('input'); cash.type = 'number'; cash.min = '0'; cash.step = '0.01'; cash.value = pre && pre.cash != null && pre.cash >= 0 ? String(pre.cash) : ''; cl.appendChild(cash); f.appendChild(cl);
  const rowsBox = el('div', 'pf-snap-rows');
  const rows = [];
  const addRow = (t = '', q = '', hold = false) => {
    const r = el('div', 'pf-row');
    const ti = el('input'); ti.placeholder = '티커'; ti.value = t; ti.setAttribute('aria-label', '티커'); ti.className = 'pf-ticker';
    const qi = el('input'); qi.type = 'number'; qi.min = '0'; qi.step = 'any'; qi.placeholder = '수량'; qi.value = q; qi.setAttribute('aria-label', '수량');
    const hl = el('label', 'pf-inline'); const hc = el('input'); hc.type = 'checkbox'; hc.checked = hold;
    hl.appendChild(hc); hl.appendChild(el('span', null, '그대로 두기'));
    const del = el('button', 'pf-btn pf-btn-quiet', '빼기'); del.type = 'button';
    del.addEventListener('click', () => { r.remove(); rows.splice(rows.indexOf(rec), 1); });
    r.appendChild(ti); r.appendChild(qi); r.appendChild(hl); r.appendChild(del);
    rowsBox.appendChild(r);
    const rec = { ti, qi, hc };
    rows.push(rec);
  };
  for (const h of pre?.holdings || []) addRow(h.ticker, String(Math.round(h.qty * 1e6) / 1e6));
  if (!rows.length) addRow();
  f.appendChild(el('p', 'pf-note', '"그대로 두기"를 고른 종목은 B·C·D가 사지도 팔지도 않습니다(A만 입금으로 비중대로 삽니다).'));
  f.appendChild(rowsBox);
  const add = el('button', 'pf-btn pf-btn-quiet', '종목 더하기'); add.type = 'button';
  add.addEventListener('click', () => addRow());
  f.appendChild(add);
  const btn = el('button', 'pf-btn', '이 스냅샷으로 시작'); btn.type = 'button';
  const msg = msgLine();
  f.appendChild(btn); f.appendChild(msg);
  const known = new Set((model.records || []).map((r) => r.session));
  // 시작일 기록에 가격이 없는 티커(카드·고정 ETF 밖이거나 오타)는 저장 전에 한 번 경고한다 — 그대로면 비교가 출발하지 못한다
  const startRec = (model.records || []).find((r) => r.session === lastSession);
  const priced = new Set([...Object.keys(startRec?.cards || {}), ...Object.keys(startRec?.prices || {})]);
  let ackUnknown = '';
  twoStep(btn, msg, '저장하면 고칠 수 없습니다. 맞으면 한 번 더 누르세요.', async () => {
    const d = date.value;
    // 앞으로만 쌓는다(설계 0절): 시작일은 마지막 일별 기록 날짜 하나만
    if (!lastSession || d !== lastSession || !isTradingDay(d) || !known.has(d)) throw new Error(`시작일은 마지막 일별 기록 날짜(${lastSession || '없음'})만 고를 수 있습니다.`);
    const c = cash.value.trim() === '' ? NaN : Number(cash.value);
    if (!(c >= 0) || Math.round(c * 100) / 100 !== c) throw new Error('현금은 0 이상, 센트 단위까지 넣으세요.');
    const holdings = {}, holdOnly = [];
    for (const r of rows) {
      const t = r.ti.value.trim().toUpperCase();
      if (!t && !r.qi.value) continue;
      if (!/^[A-Z][A-Z0-9.-]{0,9}$/.test(t)) throw new Error('티커 형식이 맞지 않는 줄이 있습니다.');
      const q = Number(r.qi.value);
      if (!(q > 0) || Math.round(q * 1e6) / 1e6 !== q) throw new Error('수량은 0보다 크고 소수 6자리까지입니다.');
      if (holdings[t] != null) throw new Error('같은 티커가 두 줄에 있습니다.');
      holdings[t] = q;
      if (r.hc.checked) holdOnly.push(t);
    }
    const unknown = Object.keys(holdings).filter((t) => !priced.has(t)).sort().join(', ');
    if (unknown && unknown !== ackUnknown) {
      ackUnknown = unknown;
      throw new Error(`⚠ ${d} 일별 기록에 가격이 없는 종목: ${unknown}. 티커 오타이거나 카드 목록 밖 종목이면 전략 비교가 출발하지 못합니다. 확인했고 그대로 저장하려면 다시 두 번 누르세요.`);
    }
    await handlers.create({ date: d, holdings, cash: c, holdOnly: holdOnly.sort() });
  }, f);
  sec.appendChild(f);
  return sec;
}
