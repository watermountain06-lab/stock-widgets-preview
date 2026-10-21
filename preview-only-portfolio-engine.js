// preview 전용 전략 비교 재생 엔진(2026-10-19, 2단계). 라이브로 옮기지 않는다 — pipeline/site_ui/UI_DIFF.md 1절 portfolio.
//
// 설계: pipeline/portfolio/STRATEGY_DESIGN.md(3~6절). 고정된 일별 기록(site_data/strategy_ledger/)과 Firestore의 시작
// 스냅샷·입금·시나리오로 시작일부터 마지막 기록까지 매번 처음부터 다시 계산한다. 결과는 저장하지 않는다.
// 같은 입력이면 같은 결과다(ENGINE_VERSION 안에서). 화면·Firestore와 무관한 순수 함수라 node 시험이 그대로 부른다
// (pipeline/portfolio/test_strategy_engine.mjs).
//
// 개인 값(보유·현금·입금·시나리오 이름)은 콘솔·오류 문구에 넣지 않는다. 오류는 형식만 말한다.
// 단위: 현금은 정수 센트, 수량은 정수 마이크로주(1e-6주). 산 수량·배분 금액은 내림하고, 대금·평가액은 센트로
// 반올림한다. 내림으로 남는 금액은 현금으로 남는다.

export const ENGINE_VERSION = 'strategy-engine-1';
export const BUY_PRINCIPLE = ['초저평가', '저평가', '적정~저평가', '적정'];   // 원칙 1
export const SELL_TIERS = ['고평가', '초고평가'];                           // 이번 버전 고정
export const BASELINES = ['SPY', 'RSP', 'QQQ'];
const MICRO = 1e6;
const STALE_SESSIONS = 5;      // verdictAsOf가 기록 session보다 5거래일 넘게 오래되면 묵음(원칙 6)
const INFO_WINDOW = 2;         // 정보 마감: 쓸 기록의 session이 D보다 2거래일 넘게 앞서면 정보 없음
const SPLIT_LOW = 0.6, SPLIT_HIGH = 1.6, SPLIT_HOLD = 5;   // 분할 안전망
const PAUSE_AFTER = 5;         // 평가 미확정이 5거래일 넘게 이어지면 "비교 일시 중단"
const END = '9999-12-31';      // 달력 끝 뒤의 날짜(회차·점검일) — 어떤 기록 날짜와도 맞지 않는다

// NYSE 휴장일(pipeline/watchdog.py HOLIDAYS와 같은 목록). 기록이 목록 밖 해에 닿으면 멈춘다 — 그해를 두 곳에 함께
// 더한다. 마지막 해의 12월 결정은 다음 점검일을 모르므로 그달 회차를 모두 남겨 두고, 회차가 해를 넘으면 버린다.
const HOLIDAYS = {
  2026: ['2026-01-01', '2026-01-19', '2026-02-16', '2026-04-03', '2026-05-25', '2026-06-19', '2026-07-03',
    '2026-09-07', '2026-11-26', '2026-12-25'],
  2027: ['2027-01-01', '2027-01-18', '2027-02-15', '2027-03-26', '2027-05-31', '2027-06-18', '2027-07-05',
    '2027-09-06', '2027-11-25', '2027-12-24'],
};

const PRESETS = {
  A: { hold: true },
  E: { hold: true, etf: true },   // ETF 섞기(2026-10-21 사용자 결정): 출발일에 주식 평가액의 일부를 기준선 ETF로 바꾸고 그 뒤 보유만
  B: { buyTiers: BUY_PRINCIPLE, sellFraction: 0, observeSells: true, editable: ['sellFraction', 'splitWeeks', 'cashReserve'] },
  C: { buyTiers: ['초저평가', '저평가'], sellFraction: 0, observeSells: false, editable: ['splitWeeks', 'cashReserve'] },
  D: { buyTiers: BUY_PRINCIPLE, sellFraction: 1, observeSells: true, editable: ['splitWeeks', 'cashReserve'] },
  custom: { buyTiers: null, sellFraction: 0, observeSells: true, editable: ['buyTiers', 'sellFraction', 'splitWeeks', 'cashReserve'] },
};

class EngineInputError extends Error {}
const fail = (msg) => { throw new EngineInputError(msg); };

// ---- 날짜·달력 ----
const pad = (n) => String(n).padStart(2, '0');
function addDays(d, n) {
  const t = new Date(Date.UTC(+d.slice(0, 4), +d.slice(5, 7) - 1, +d.slice(8, 10) + n));
  return `${t.getUTCFullYear()}-${pad(t.getUTCMonth() + 1)}-${pad(t.getUTCDate())}`;
}
const isDate = (d) => typeof d === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(d);

const ET_PARTS = new Intl.DateTimeFormat('en-US', {
  timeZone: 'America/New_York', hourCycle: 'h23', year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit',
});
function etWall(ms) {
  const p = Object.fromEntries(ET_PARTS.formatToParts(new Date(ms)).map((x) => [x.type, x.value]));
  return { date: `${p.year}-${p.month}-${p.day}`, utcOfWall: Date.UTC(+p.year, +p.month - 1, +p.day, +p.hour, +p.minute) };
}
// D 09:30 ET(장 시작)의 UTC 시각(ms). 서머타임 전환은 새벽 2시라 그날 아침의 오프셋이면 맞다.
export function openUtcMs(d) {
  const wall = Date.UTC(+d.slice(0, 4), +d.slice(5, 7) - 1, +d.slice(8, 10), 9, 30);
  const probe = wall + 5 * 3600e3;
  return wall - (etWall(probe).utcOfWall - probe);
}
const toMs = (iso) => { const t = Date.parse(iso); return Number.isFinite(t) ? t : NaN; };

function makeCalendar() {
  const sessions = [];
  for (const y of Object.keys(HOLIDAYS).map(Number).sort()) {
    const off = new Set(HOLIDAYS[y]);
    for (let d = `${y}-01-01`; d.startsWith(String(y)); d = addDays(d, 1)) {
      const wd = new Date(d + 'T12:00:00Z').getUTCDay();
      if (wd > 0 && wd < 6 && !off.has(d)) sessions.push(d);
    }
  }
  const first = sessions[0], last = sessions[sessions.length - 1];
  const lower = (d) => {   // d 이상인 첫 session의 위치
    let lo = 0, hi = sessions.length;
    while (lo < hi) { const m = (lo + hi) >> 1; if (sessions[m] < d) lo = m + 1; else hi = m; }
    return lo;
  };
  const guard = (d) => { if (d > last) fail(`calendar: ${d.slice(0, 4)}년 휴장일이 없다 — HOLIDAYS에 더할 것`); };
  return {
    sessions,
    first,
    index(d) { guard(d); return lower(d); },             // d가 session이면 그 위치, 아니면 다음 session의 위치
    isSession(d) { guard(d); return sessions[lower(d)] === d; },
    onOrAfter(d) { return d > last ? END : sessions[lower(d)]; },        // 달력 끝 뒤면 END
    checkDay(d) { return this.onOrAfter(d.slice(0, 8) + '01'); },          // 그달 점검일(1일, 휴장이면 다음 거래일)
    nextCheckDay(d) {
      const y = +d.slice(0, 4), m = +d.slice(5, 7);
      return this.onOrAfter(m === 12 ? `${y + 1}-01-01` : `${y}-${pad(m + 1)}-01`);
    },
  };
}

// ---- 시장 기록(모든 시나리오가 함께 쓴다) ----
function makeMarket(records, cal) {
  const recs = [...records].sort((a, b) => (a.session < b.session ? -1 : 1));
  const by = new Map();
  for (const r of recs) {
    if (!r || !isDate(r.session)) fail('records: session 형식 오류');
    if (by.has(r.session)) fail('records: 같은 session이 두 번');
    if (!cal.isSession(r.session)) fail('records: 거래일이 아닌 session');
    by.set(r.session, r);
  }
  // 기록 X의 공개 시각 = X 다음 기록의 prevPublishedAt. 다음 기록이 있는데 값이 없으면 "공개 시각을 모름 → 공개 전으로 본다"
  // (build_strategy_ledger.py published_at). 다음 기록이 아직 없으면 미정(잠정).
  const pub = new Map();
  for (const r of recs) if (r.prevSession) pub.set(r.prevSession, r.prevPublishedAt ? toMs(r.prevPublishedAt) : null);

  // 그날 데이터가 있는가: 기록이 있고 파이프라인이 정상(pipelineFull)이어야 한다(설계 2절 "빠진 날"). 실패 기록의 종가·판정은
  // 쓰지 않는다. 분할과 기업 사건은 실패 기록에서도 받는다 — 처음 보인 기록에만 실려서 버리면 다시 오지 않는다.
  const dayOk = (d) => !!by.get(d)?.pipelineFull;
  const close = (t, d) => {
    if (!dayOk(d)) return null;
    const r = by.get(d), c = r.cards?.[t]?.close ?? r.prices?.[t];
    return typeof c === 'number' && c > 0 ? c : null;
  };
  const splitsOn = (d) => [...(by.get(d)?.splits || [])].sort((a, b) => (a.id < b.id ? -1 : 1));
  const eventsOn = (d) => (by.get(d)?.events || []).map((e) => {
    if (!e || !isDate(e.date) || typeof e.ticker !== 'string') fail('records: events 형식 오류');
    if (e.date > d) fail('records: 사건일이 기록 날짜보다 뒤인 사건');
    return e;
  });

  // 분할 안전망: 마지막 정상 종가(값이 없던 날은 건너뜀) 대비 0.6배 이하·1.6배 이상이고 그날 그 티커 분할 기록이 없으면
  // "확인 필요". 분할 기록이 오거나 5거래일이 지나면 풀린다. 이어지는 동안 평가·매매를 보류한다.
  const flagged = new Set();
  const lastSession = recs.length ? recs[recs.length - 1].session : null;
  if (recs.length) {
    const tickers = new Set();
    for (const r of recs) {
      Object.keys(r.cards || {}).forEach((t) => tickers.add(t));
      Object.keys(r.prices || {}).forEach((t) => tickers.add(t));
    }
    const i0 = cal.index(recs[0].session), i1 = cal.index(lastSession);
    for (const t of tickers) {
      let ref = null, since = null;
      for (let i = i0; i <= i1; i++) {
        const d = cal.sessions[i], c = close(t, d);
        if (since !== null && i - since >= SPLIT_HOLD) { since = null; ref = null; }
        if (splitsOn(d).some((s) => s.ticker === t)) { since = null; ref = c; continue; }
        if (since !== null) { flagged.add(t + '|' + d); continue; }
        if (c === null) continue;
        if (ref !== null && (c / ref <= SPLIT_LOW || c / ref >= SPLIT_HIGH)) { since = i; flagged.add(t + '|' + d); continue; }
        ref = c;
      }
    }
  }

  // 날 D의 결정·재확인에 쓰는 기록: 공개 시각이 D 09:30 ET 전인 정상 기록(pipelineFull) 가운데 가장 최근 것.
  // 다음 기록이 아직 없는 기록은 공개 시각이 미정이다 — generatedAt(공개 시각의 하한)이 장 시작 전이면 "잠정"으로 쓴다.
  // 재생 안에서는 D를 체결하려면 D 기록이 있어야 하고 그때 직전 기록의 공개 시각은 이미 정해져 있으므로 잠정은 생기지
  // 않는다. 잠정은 아직 D 기록이 없는 '오늘 할 일' 미리보기(3단계 화면)에서만 쓰인다.
  const infoCache = new Map();
  function infoFor(d) {
    if (infoCache.has(d)) return infoCache.get(d);
    const open = openUtcMs(d);
    let got = null;
    for (let j = recs.length - 1; j >= 0 && !got; j--) {
      const r = recs[j];
      if (r.session >= d || !r.pipelineFull) continue;
      if (pub.has(r.session)) {
        const t = pub.get(r.session);
        if (t !== null && t < open) got = { rec: r, provisional: false };
      } else if (toMs(r.generatedAt) < open) {
        got = { rec: r, provisional: true };
      }
    }
    if (got && cal.index(d) - cal.index(got.rec.session) > INFO_WINDOW) got = null;
    infoCache.set(d, got);
    return got;
  }

  const usable = (t, d) => close(t, d) !== null && !flagged.has(t + '|' + d);
  return { by, lastSession, dayOk, close, splitsOn, eventsOn, infoFor, usable, flagged: (t, d) => flagged.has(t + '|' + d) };
}

// 원칙 6: 카드 없음·판정 없음·묵음이면 그 종목은 보류한다. 걸리면 사유, 아니면 null.
function blocked(card, rec, cal) {
  if (!card) return 'noCard';
  if (!card.tier) return 'noVerdict';
  if (card.priceStale) return 'stale';
  if (!isDate(card.verdictAsOf) || card.verdictAsOf < cal.first || card.verdictAsOf > rec.session) return 'stale';
  if (cal.index(rec.session) - cal.index(card.verdictAsOf) > STALE_SESSIONS) return 'stale';
  return null;
}

// 분할 하나를 수량에 적용할지와, 늦게 와서 멈춰야 하는지. 분할 판단 기준일(splitBase)은 시나리오는 A의 시작 스냅샷
// 날짜, 기준선은 자기 출발일이다 — 효력일이 그날이나 그 전이면 수량에 이미 들어 있어 무시한다. 파생 시나리오는 A가
// 이미 본 id를 물려받는다(설계 4절, A의 판단을 그대로 따른다).
// 늦게 온 분할(효력일 < 오늘)은 효력일 전날 장 마감에 그 종목을 보유했는지(own — 수량이 아니라 보유 여부라 그 사이 다른
// 분할로 단위가 바뀌어도 맞다)와 [효력일, 오늘) 사이의 그 종목 매매(log)로 판단한다.
//   - 전날 보유하지 않았으면: 그 뒤 사고판 것은 모두 분할 뒤 가격·수량이라 맞다 → 무시.
//   - 보유했는데 그 사이 사고판 적이 있으면: 분할 전 수량으로 체결했거나 섞였다 → 효력일부터 멈춘다.
//   - 보유했고 매매가 없으면: 적용하고, 그 사이 시나리오 평가가 나온 날(valued — 틀린 수량으로 평가)이 있으면 멈춘다.
function splitAction(s, d, i, splitBase, seen, valued, own, log, mk, cal) {
  if (seen.has(s.id)) return null;
  seen.add(s.id);
  if (!(s.ratio > 0)) fail('records: split ratio 오류');
  if (s.effectiveDate > d) fail('records: 효력일이 기록 날짜보다 뒤인 분할');
  if (s.effectiveDate <= splitBase) return { action: 'ignored' };
  if (s.effectiveDate === d) return { action: 'applied', halt: false };
  const from = cal.index(s.effectiveDate);
  if (!own.get(s.ticker)?.has(from - 1)) return { action: 'ignored', why: 'notHeldAtEffective' };
  if (log.some((x) => x.t === s.ticker && x.i >= from && x.i < i)) return { action: 'applied', halt: true };
  const halt = (valued.get(s.ticker) || []).some((k) => k >= from && k < i);
  return { action: 'applied', halt };
}

// ---- 입력 정리 ----
function cents(x, what) {
  if (typeof x !== 'number' || !Number.isFinite(x) || x < 0) fail(`${what}: 0 이상 숫자여야 한다`);
  return Math.round(x * 100);
}
function micro(x, what) {
  if (typeof x !== 'number' || !Number.isFinite(x) || x < 0) fail(`${what}: 0 이상 숫자여야 한다`);
  return Math.round(x * MICRO);
}
// 비율(0~1)은 백만분율 정수로 바꿔 곱하고 내린다 — 0.29 × 100센트가 실수 오차로 28이 되지 않게
const PPM = 1000000n;
const toPpm = (x) => BigInt(Math.round(x * 1e6));
const mulFloor = (n, ppm) => Number((BigInt(n) * ppm) / PPM);
const inRange = (x, lo, hi) => typeof x === 'number' && Number.isFinite(x) && x >= lo && x <= hi
  && Math.abs(x * 1e6 - Math.round(x * 1e6)) < 1e-6;   // 소수 6자리까지만 받는다(백만분율로 계산하므로)

function scenarioParams(sc) {
  const p = PRESETS[sc.strategy];
  if (!p) fail('scenario: strategy는 A·B·C·D·E·custom');
  if (p.hold && !p.etf) return { hold: true, notes: [] };
  if (p.etf) {
    const given = sc.params || {};
    for (const k of Object.keys(given)) if (!['etfShare', 'etfs'].includes(k)) fail(`scenario: E에서 바꿀 수 없는 값 ${k}`);
    const share = given.etfShare ?? 1, etfs = given.etfs ?? [...BASELINES];
    if (!inRange(share, 0, 1)) fail('scenario: etfShare는 0~1, 소수 6자리까지');
    if (!Array.isArray(etfs) || !etfs.length || etfs.some((e) => !BASELINES.includes(e)) || new Set(etfs).size !== etfs.length) fail(`scenario: etfs는 ${BASELINES.join('·')} 가운데 겹치지 않게 하나 이상`);
    return { hold: true, etf: { ppm: toPpm(share), etfs: [...etfs].sort() }, notes: [] };
  }
  const given = sc.params || {};
  for (const k of Object.keys(given)) if (!p.editable.includes(k)) fail(`scenario: ${sc.strategy}에서 바꿀 수 없는 값 ${k}`);
  const q = { buyTiers: p.buyTiers, sellFraction: p.sellFraction, splitWeeks: 4, cashReserve: 0, observeSells: p.observeSells, ...given };
  if (!Array.isArray(q.buyTiers) || !q.buyTiers.length || q.buyTiers.some((t) => typeof t !== 'string')) fail('scenario: buyTiers 형식 오류');
  if (!inRange(q.sellFraction, 0, 1)) fail('scenario: sellFraction은 0~1, 소수 6자리까지');
  if (!Number.isInteger(q.splitWeeks) || q.splitWeeks < 1 || q.splitWeeks > 4) fail('scenario: splitWeeks는 1~4 정수');
  if (!inRange(q.cashReserve, 0, 0.5)) fail('scenario: cashReserve는 0~0.5, 소수 6자리까지');
  const notes = [];
  if (q.buyTiers.some((t) => !BUY_PRINCIPLE.includes(t))) notes.push('offPrinciple');
  if (sc.strategy === 'B') {
    notes.push('provisionalPrinciple');                 // 원칙 2 비율 미정 — 매도 검토는 알림만 반영한 임시 모형
    if (q.cashReserve === 0) notes.push('noPrinciple7');  // 원칙 7(급락 대비 현금) 미반영
  }
  return { ...q, hold: false, notes, sellPpm: toPpm(q.sellFraction), reservePpm: toPpm(q.cashReserve) };
}

// ---- 시나리오 하나 재생 ----
// init: { idx(출발 상태가 그날 장 마감 뒤인 session의 위치), shares Map(T→마이크로주), cash(센트), seen(이미 판단한 분할 id),
//         splitBase, noDecisionBefore(이 날짜 전 점검일에는 결정하지 않음), depositsFrom(기준선이 입금을 받기 시작하는 위치 —
//         시나리오 자신은 init.idx 다음 날부터 받는다), log·own·preEvents(파생이 A에서 물려받는 것) }
function runScenario(ctx, prm, init, keepStates) {
  const { cal, mk, holdOnly, depositsBy } = ctx;
  const last = cal.index(mk.lastSession);
  const st = { shares: new Map(init.shares), cash: init.cash };
  const seen = new Set(init.seen);
  const valued = new Map();     // T → 그 종목을 보유한 채 시나리오 평가가 나온 session 위치들(늦은 분할 판단용)
  const own = new Map();        // T → 장 마감 때 보유했던 session 위치들(출발 전 포함, 파생은 A의 기록을 물려받는다)
  for (const [t, ks] of init.own || []) own.set(t, new Set(ks));
  const log = [...(init.log || [])];   // 매매 기록 {i, t, side, q(마이크로주)} — 파생은 출발일까지의 A 기록을 물려받는다
  let curIdx = init.idx;
  const out = {
    days: [], trades: [], skips: [], months: [], events: [...(init.preEvents || [])], splitLog: [],
    halted: null, started: null, startValue: null,
  };
  const lastStage = new Map();
  let lastRule = null, plan = null, pendingDecision = null, weights = null, preDep = 0;
  const pendingA = new Map();   // A: 가격이 없어 못 산 입금 몫(T → 센트)
  const pendingE = new Map();   // E: 출발일에 바꾼 금액 가운데 ETF 가격이 없어 아직 못 산 몫(T → 센트)
  let keepCash = null;          // E: 입금 가운데 현금으로 둘 비율 {num, den}(출발 때 현금 ÷ 평가액, 출발 전 입금은 빼고)
  const states = keepStates ? new Map() : null;

  const hasShares = (t) => (st.shares.get(t) || 0) > 0;
  const value = (d) => {
    if (!mk.dayOk(d)) return { v: null, why: [mk.by.has(d) ? 'pipelineFailed' : 'noRecord'] };
    let v = 0; const why = [];
    for (const [t, q] of [...st.shares].sort()) {
      if (q <= 0) continue;
      if (!mk.usable(t, d)) { why.push((mk.flagged(t, d) ? 'splitCheck:' : 'noPrice:') + t); continue; }
      v += (q * mk.close(t, d)) / 1e4;   // 마이크로주 × 달러 → 센트
    }
    return why.length ? { v: null, why } : { v: st.cash + Math.round(v), why };
  };
  // 금액 기준 매수: 수량 = 금액 ÷ 종가(내림), 대금 = 수량 × 종가(센트 반올림, 금액을 넘지 않는다). 남은 금액은 현금.
  const buy = (t, amt, d, extra) => {
    const c = mk.close(t, d), q = Math.floor((amt * 1e4) / c);
    if (q <= 0) return 0;
    const cost = Math.min(amt, Math.round((q * c) / 1e4));
    if (!hasShares(t)) lastStage.delete(t);   // 새로 보유하면 상태표는 "없음"부터(시작 보유와 같은 기준)
    st.shares.set(t, (st.shares.get(t) || 0) + q);
    st.cash -= cost;
    out.trades.push({ date: d, ticker: t, side: 'buy', shares: q / MICRO, price: c, amount: cost / 100, ...extra });
    log.push({ i: curIdx, t, side: 'buy', q });
    return cost;
  };

  for (let i = init.idx; i <= last; i++) {
    const d = cal.sessions[i];
    curIdx = i;
    const started = out.started !== null;
    let flow = 0;
    // 1) 장 시작 전: 입금, 분할
    if (i > init.idx) {
      for (const dep of depositsBy.get(d) || []) {
        st.cash += dep.amount; flow += dep.amount;
        if (!started) preDep += dep.amount;
        else if (prm.hold) addPendingA(dep.amount);
      }
      for (const s of mk.splitsOn(d)) applySplit(s, d, i);
      for (const e of mk.eventsOn(d)) applyEvent(e, i);
    }
    // 2) 출발: 그날 평가가 확정되는 첫날(시작일·S 전 거래일이 미확정이면 다음 확정일로 미룬다). 미룬 사이의 입금은
    //    출발 평가액에 들고, A는 그 입금을 출발일 종가에 출발 비중대로 산다(기준선이 출발일에 전부 사는 것과 같다).
    if (!started) {
      const v = value(d);
      if (v.v === null) {
        out.days.push({ date: d, value: null, why: ['notStarted', ...v.why], flow: 0 });
        // 출발 전에 지나간 점검일은 결정하지 않는다 — 화면이 설명할 수 있게 사건으로 남긴다
        dropUnstarted(d);
        recordOwn(i);
        continue;
      }
      out.started = d; out.startValue = v.v; out.startIdx = i;
      if (prm.hold) {
        if (prm.etf) {
          keepCash = { num: BigInt(st.cash - preDep), den: BigInt(v.v - preDep) };
          convertToEtf(d);
        }
        // 비중은 종목별 평가액(정수 센트)으로 두고 배분은 BigInt로 내림한다 — 실수 비중의 오차로 센트를 잃지 않게.
        // E의 ETF 몫은 이 시점에 아직 사기 전이므로 pendingE 금액(배정액)으로 넣는다(그날 가격이 없으면 돌아온 날 산다)
        const val = new Map([...st.shares].filter(([, q]) => q > 0).map(([t, q]) => [t, BigInt(Math.round((q * mk.close(t, d)) / 1e4))]));
        for (const [t, a] of pendingE) val.set(t, (val.get(t) || 0n) + BigInt(a));
        const vs = [...val].sort();
        const tot = vs.reduce((a, [, x]) => a + x, 0n);
        weights = tot > 0n ? { vs, tot } : null;
        if (preDep > 0) addPendingA(preDep);
        buyPendingA(d);
      }
      out.days.push({ date: d, value: value(d).v, why: [], flow: 0, start: true });
      dropUnstarted(d);   // 출발일에도 결정하지 않는다(출발 상태가 그날 장 마감 뒤라서)
      recordOwn(i); recordValued(i);
      if (states) states.set(i, snapshotState());
      continue;
    }
    if (out.halted) { if (plan) closePlan('halted'); out.days.push({ date: d, value: null, why: ['halted'], flow }); recordOwn(i); continue; }

    // 3) 장 마감 체결
    if (prm.hold) buyPendingA(d);
    else monthly(d, i);
    const v = value(d);
    out.days.push({ date: d, value: v.v, why: v.why, flow });
    recordOwn(i);
    if (v.v !== null) recordValued(i);
    if (states) states.set(i, snapshotState());
  }
  if (plan) closePlan('open');
  if (pendingDecision) out.events.push({ date: mk.lastSession, kind: 'decisionPending', checkDate: pendingDecision });
  out.holdings = Object.fromEntries([...st.shares].filter(([, q]) => q > 0).sort().map(([t, q]) => [t, q / MICRO]));
  out.cash = st.cash / 100;
  out.lastStage = Object.fromEntries([...lastStage].sort());
  out.states = states;
  out.log = log;
  out.own = own;
  return out;

  function snapshotState() { return { shares: new Map(st.shares), cash: st.cash, seen: new Set(seen) }; }
  function recordValued(i) { for (const [t, q] of st.shares) if (q > 0) (valued.get(t) || valued.set(t, []).get(t)).push(i); }
  function recordOwn(i) { for (const [t, q] of st.shares) if (q > 0) (own.get(t) || own.set(t, new Set()).get(t)).add(i); }
  // 출발 전·출발일에 지나간 점검일은 결정하지 않는다 — 화면이 설명할 수 있게 사건으로 남긴다
  function dropUnstarted(d) {
    if (!prm.hold && d === cal.checkDay(d) && d >= init.noDecisionBefore) out.events.push({ date: d, kind: 'decisionDropped', checkDate: d, reason: 'notStarted' });
  }

  function addPendingA(amt) {   // 남는 센트는 현금으로 둔다
    if (!weights) return;
    // E: 출발 때 현금 비중만큼은 현금으로 두고 나머지만 비중대로 산다(현금 비중 유지). 현금 몫을 센트 내림하므로 1센트
    //    입금처럼 아주 작은 입금은 현금 몫이 0이 되어 전부 매수 쪽으로 가고, 종목별로 나눈 몫마저 내림으로 0이면 현금에 남는다. 평가액이 0 이하(den ≤ 0)면 현금 몫 없이 비중대로 — 그런 출발에는 weights도 없다
    if (keepCash) amt -= keepCash.den > 0n ? Number((BigInt(amt) * keepCash.num) / keepCash.den) : 0;
    for (const [t, v] of weights.vs) {
      const a = Number((BigInt(amt) * v) / weights.tot);
      if (a > 0) pendingA.set(t, (pendingA.get(t) || 0) + a);
    }
  }
  function buyPendingA(d) {
    for (const [t, amt] of [...pendingE].sort()) {
      if (amt > 0 && mk.usable(t, d)) { buy(t, amt, d, { kind: 'etf' }); pendingE.delete(t); }
    }
    for (const [t, amt] of [...pendingA].sort()) {
      if (amt > 0 && mk.usable(t, d)) { buy(t, amt, d, { kind: 'deposit' }); pendingA.delete(t); }
    }
  }
  // E 출발: 고른 ETF가 아닌 보유 종목마다 수량의 etfShare만큼(마이크로주 내림)을 그날 종가에 팔고, 대금 합을 고른 ETF에 똑같이
  // 나눈다(센트 내림, 남는 센트는 현금). 출발일 평가가 확정됐으므로 보유 종목 가격은 모두 있다. 산 뒤로는 사고팔지 않는다.
  function convertToEtf(d) {
    let total = 0;
    for (const [t, q] of [...st.shares].sort()) {
      if (q <= 0 || prm.etf.etfs.includes(t)) continue;
      const sq = Number((BigInt(q) * BigInt(prm.etf.ppm)) / 1000000n);
      if (sq <= 0) continue;
      const c = mk.close(t, d), amt = Math.round((sq * c) / 1e4);
      st.shares.set(t, q - sq); st.cash += amt; total += amt;
      out.trades.push({ date: d, ticker: t, side: 'sell', shares: sq / MICRO, price: c, amount: amt / 100, kind: 'etf' });
      log.push({ i: curIdx, t, side: 'sell', q: sq });
    }
    const each = Math.floor(total / prm.etf.etfs.length);
    if (each > 0) for (const e of prm.etf.etfs) pendingE.set(e, each);
  }

  function applySplit(s, d, i) {
    const r = splitAction(s, d, i, init.splitBase, seen, valued, own, log, mk, cal);
    if (!r) return;
    out.splitLog.push({ id: s.id, date: d, action: r.action, ...(r.why ? { why: r.why } : {}) });
    if (r.action !== 'applied') return;
    const t = s.ticker;
    if (st.shares.has(t)) st.shares.set(t, Math.round(st.shares.get(t) * s.ratio));
    if (plan) for (const leg of plan.legs) if (leg.side === 'sell' && leg.ticker === t) leg.amt = scaleRounds(leg.amt, s.ratio);
    if (r.halt) haltAt('splitDelay', s.effectiveDate, t);
  }
  // 남은 매도 회차에 분할 비율을 곱한다: 남은 합계를 반올림하고, 회차별로 내린 뒤 차이는 마지막 남은 회차에 더한다
  // (설계 3절 "마지막 회차에는 자기 몫과 앞 회차들의 반올림 잔량"). 보유 수량 반올림과 같은 합계가 된다.
  function scaleRounds(amt, ratio) {
    const total = Math.round(amt.reduce((a, b) => a + b, 0) * ratio);
    const out2 = amt.map((q) => Math.floor(q * ratio));
    const lastK = amt.reduce((m, q, k) => (q > 0 ? k : m), -1);
    if (lastK >= 0) out2[lastK] += total - out2.reduce((a, b) => a + b, 0);
    return out2;
  }
  // 멈춘 날은 늘 더 이른 쪽으로 당긴다(늦게 온 두 번째 사건이 더 이른 오류를 밝힐 수 있다)
  function haltAt(reason, since, ticker) {
    if (!out.halted || since < out.halted.since) out.halted = { reason, since, ticker };
  }
  // 지원하지 않는 기업 사건(특별 배당·분사·합병·티커 변경, 설계 4절): 기록의 events에 실려 오면, 사건일 전날 장 마감에
  // 그 종목을 보유했던 시나리오는 사건일부터 평가 불가로 멈춘다(그날 판 경우 포함, 사건 뒤에 산 경우는 영향 없음). 보유
// 기록(own)은 출발 상태 날부터만 있으므로 시작 스냅샷 날(기준선은 출발일)이나 그 전 사건은 저절로 빠진다. 1단계 기록은 아직 이 필드를 만들지 않는다 — 받는 자리만 둔다.
  function applyEvent(e, i) {
    const from = cal.index(e.date);
    if (own.get(e.ticker)?.has(from - 1)) haltAt('corporateEvent', e.date, e.ticker);   // 사건일 전날 장 마감에 보유했으면(분할과 같은 기준)
  }

  // ---- 월 점검과 회차 ----
  function monthly(d, i) {
    if (d === cal.checkDay(d)) {
      if (plan) closePlan('nextCheck');
      if (pendingDecision) out.events.push({ date: d, kind: 'decisionDropped', checkDate: pendingDecision });
      pendingDecision = d >= init.noDecisionBefore ? d : null;
    }
    if (pendingDecision) {
      const info = mk.infoFor(d);
      if (!info) out.events.push({ date: d, kind: 'decisionDeferred', checkDate: pendingDecision, reason: 'noInfo' });
      else { decide(d, info); pendingDecision = null; }
    }
    if (plan) runRound(d);
  }

  function decide(d, info) {
    const R = info.rec, N = prm.splitWeeks;
    const changed = lastRule !== null && R.ruleVersion !== lastRule;
    lastRule = R.ruleVersion;
    const next = cal.nextCheckDay(pendingDecision);
    const rounds = [];
    for (let k = 0; k < N; k++) {
      const day = cal.onOrAfter(addDays(d, 7 * k));
      rounds.push({ date: day, dropped: day >= next });
    }
    plan = {
      checkDate: pendingDecision, decisionDate: d, record: R.session, ruleVersion: R.ruleVersion,
      provisional: info.provisional, rounds, legs: [], candidates: [], ruleChanged: changed, fires: [], budget: 0, unallocated: 0,
    };
    // 매도 발동(상태표) — 점검일 결정 때 보유 종목만 관측한다. 0주에서 새로 사면 buy()가 상태를 "없음"으로 되돌리므로,
    // 다 판 뒤 다시 산 종목이나 고평가에서 산 종목도 다음 점검일에 시작 보유와 같은 기준으로 발동한다.
    if (prm.observeSells) {
      for (const t of [...st.shares.keys()].sort()) {
        if (!hasShares(t) || holdOnly.has(t)) continue;
        const why = blocked(R.cards?.[t], R, cal);
        if (why) { plan.fires.push({ ticker: t, observed: null, skip: why }); continue; }
        const tier = R.cards[t].tier;
        const obs = SELL_TIERS.includes(tier) ? tier : 'out';
        const prev = lastStage.get(t) || 'none';
        lastStage.set(t, obs);
        if (changed) { plan.fires.push({ ticker: t, observed: obs, skip: 'ruleVersion' }); continue; }
        const fire = (obs === '고평가' && (prev === 'none' || prev === 'out')) || (obs === '초고평가' && prev !== '초고평가');
        if (!fire) continue;
        const q = mulFloor(st.shares.get(t), prm.sellPpm);
        plan.fires.push({ ticker: t, observed: obs, prev, shares: q / MICRO, warnOnly: q <= 0 });
        if (q > 0) plan.legs.push({ ticker: t, side: 'sell', amt: split(q, N), done: 0, notUsed: 0 });
      }
    }
    // 매수 예산: 그날 쓸 수 있는 현금만(아직 체결 안 된 매도 대금 제외). 새 돈만 후보에 같은 금액.
    if (!changed) {
      const cands = Object.keys(R.cards || {}).sort().filter((t) =>
        !holdOnly.has(t) && !blocked(R.cards[t], R, cal) && prm.buyTiers.includes(R.cards[t].tier));
      plan.candidates = cands;
      plan.budget = st.cash;
      const each = cands.length ? Math.floor(st.cash / cands.length) : 0;
      plan.unallocated = st.cash - each * cands.length;   // 후보 수로 나눈 잔돈(현금으로 남음)
      for (const t of cands) plan.legs.push({ ticker: t, side: 'buy', amt: split(each, N), done: 0, notUsed: 0 });
    }
    out.months.push(plan);
  }

  function split(total, n) {   // n회로 나누고 마지막 회차에 나머지를 더한다
    const per = Math.floor(total / n);
    return Array.from({ length: n }, (_, k) => (k === n - 1 ? total - per * (n - 1) : per));
  }

  function skip(leg, k, d, reason, carry, info) {
    const a = leg.amt[k];
    leg.amt[k] = 0;
    const nxt = carry ? plan.rounds.findIndex((r, j) => j > k && !r.dropped) : -1;
    let action = 'erased';
    if (carry) {
      if (nxt === k + 1) { leg.amt[nxt] += a; action = 'carried'; } else action = 'dropped';
    }
    if (action !== 'carried') leg.notUsed += a;
    out.skips.push({
      date: d, ticker: leg.ticker, side: leg.side, round: k + 1, reason, action,
      [leg.side === 'buy' ? 'amount' : 'shares']: leg.side === 'buy' ? a / 100 : a / MICRO,
      provisional: !!info?.provisional,
    });
  }

  // 회차 재확인: 판정이 조건을 벗어났거나 원칙 6이면 그 회차는 지운다(설계 3절). 정보 없음과 파이프라인 실패(그날
  // 기록이 없거나 실패)로 못 한 회차는 바로 다음 회차로 넘긴다(2026-10-19·20 사용자 결정). 종목 하나의 가격 없음·
  // 확인 필요·유보 계산 불가는 지운다(설계 4절, 사용자 결정 10-20).
  function check(leg, d, info) {
    if (!info) return ['noInfo', true];
    const R = info.rec;
    if (R.ruleVersion !== plan.ruleVersion) return ['ruleVersion', false];
    const why = blocked(R.cards?.[leg.ticker], R, cal);
    if (why) return [why, false];
    const tiers = leg.side === 'sell' ? SELL_TIERS : prm.buyTiers;
    if (!tiers.includes(R.cards[leg.ticker].tier)) return ['tierOut', false];
    if (!mk.dayOk(d)) return ['pipelineFailed', true];
    if (!mk.usable(leg.ticker, d)) return [mk.flagged(leg.ticker, d) ? 'splitCheck' : 'noPrice', false];
    return null;
  }

  function runRound(d) {
    const k = plan.rounds.findIndex((r) => r.date === d && !r.dropped);
    if (k < 0) return;
    const info = mk.infoFor(d);
    const prov = { provisional: !!info?.provisional || plan.provisional, round: k + 1 };
    const pre = value(d);                       // 유보 기준(그날 종가, 매매 전)
    let proceeds = 0;
    for (const leg of plan.legs.filter((l) => l.side === 'sell')) {
      if (leg.amt[k] <= 0) continue;
      const bad = check(leg, d, info);
      if (bad) { skip(leg, k, d, bad[0], bad[1], info); continue; }
      const q = Math.min(leg.amt[k], st.shares.get(leg.ticker) || 0);
      if (q <= 0) { skip(leg, k, d, 'noShares', false, info); continue; }
      const c = mk.close(leg.ticker, d), p = Math.round((q * c) / 1e4);
      st.shares.set(leg.ticker, st.shares.get(leg.ticker) - q);
      st.cash += p; proceeds += p;
      leg.notUsed += leg.amt[k] - q;
      leg.amt[k] = 0; leg.done++;
      out.trades.push({ date: d, ticker: leg.ticker, side: 'sell', shares: q / MICRO, price: c, amount: p / 100, ...prov });
      log.push({ i: curIdx, t: leg.ticker, side: 'sell', q });
    }
    // 매도 대금: 그달 후보 수로 똑같이 나눠 각 후보의 다음 회차부터 남은 회차에 더한다. 같은 날 매수에는 쓰지 않는다.
    if (proceeds > 0) {
      const rest = plan.rounds.map((r, j) => j).filter((j) => j > k && !plan.rounds[j].dropped);
      const buys = plan.legs.filter((l) => l.side === 'buy');
      if (buys.length && rest.length) {
        const each = Math.floor(proceeds / buys.length);
        plan.unallocated += proceeds - each * buys.length;
        for (const leg of buys) split(each, rest.length).forEach((a, x) => { leg.amt[rest[x]] += a; });
        out.events.push({ date: d, kind: 'proceedsSpread', amount: proceeds / 100, candidates: buys.length, rounds: rest.length });
      } else {
        out.events.push({ date: d, kind: 'proceedsToCash', amount: proceeds / 100 });
      }
    }
    const ready = [];
    for (const leg of plan.legs.filter((l) => l.side === 'buy')) {
      if (leg.amt[k] <= 0) continue;
      const bad = check(leg, d, info);
      if (bad) skip(leg, k, d, bad[0], bad[1], info); else ready.push(leg);
    }
    if (!ready.length) return;
    let reserve = 0;
    if (prm.cashReserve > 0) {
      if (pre.v === null) { for (const leg of ready) skip(leg, k, d, 'reserveUnknown', false, info); return; }
      reserve = mulFloor(pre.v, prm.reservePpm);
    }
    // 매수 한도 = max(0, 현금 − 당일 매도 대금 − 유보액). 넘치면 그날 회차들을 같은 비율로 줄인다(순서와 무관).
    const limit = Math.max(0, st.cash - proceeds - reserve);
    const want = ready.reduce((a, l) => a + l.amt[k], 0);
    for (const leg of ready) {
      const a = leg.amt[k], spend = want > limit ? Number((BigInt(a) * BigInt(limit)) / BigInt(want)) : a;   // 정수로 내림
      leg.amt[k] = 0;
      if (spend < a) out.skips.push({ date: d, ticker: leg.ticker, side: 'buy', round: k + 1, reason: 'cashLimit', action: 'erased', amount: (a - spend) / 100, provisional: prov.provisional });
      const cost = spend > 0 ? buy(leg.ticker, spend, d, prov) : 0;
      leg.notUsed += a - cost;
      if (cost > 0) leg.done++;
    }
  }

  function closePlan(why) {
    const p = plan;
    for (const leg of p.legs) {
      p.rounds.forEach((r, j) => {
        if ((r.dropped || why === 'halted') && leg.amt[j] > 0) {   // 멈추면 남은 회차는 모두 실행되지 않는다
          out.skips.push({ date: r.date === END ? null : r.date, ticker: leg.ticker, side: leg.side, round: j + 1,
            reason: why === 'halted' ? 'halted' : r.date === END ? 'beyondCalendar' : 'pastNextCheck', action: 'dropped',
            [leg.side === 'buy' ? 'amount' : 'shares']: leg.side === 'buy' ? leg.amt[j] / 100 : leg.amt[j] / MICRO, provisional: p.provisional });
          leg.notUsed += leg.amt[j];
          leg.amt[j] = 0;
        }
      });
    }
    p.closed = why;
    p.unallocated /= 100;
    p.budget /= 100;   // 출력은 모두 달러
    // 종목별: 실제 완료 회차, 쓰지 않은 몫(지움·버림·한도 축소·내림 잔액 — 매수는 현금으로 남음, 매도는 팔지 않은 수량),
    // 아직 예정인 몫(그달이 진행 중일 때만)
    const unit = (l, x) => (l.side === 'buy' ? x / 100 : x / MICRO);
    p.summary = p.legs.map((l) => ({
      ticker: l.ticker, side: l.side, roundsDone: l.done, notUsed: unit(l, l.notUsed),
      scheduled: unit(l, l.amt.reduce((a, b) => a + b, 0)),
    }));
    plan = null;
  }
}

// ---- 기준선 하나: 출발 평가액을 출발일 종가에 전부 넣고, 입금은 반영일 종가에 한 번에 산다. 분할은 출발일 뒤 효력만
// 적용하고, 늦은 분할로 틀린 수량으로 평가한 날이 있으면 효력일부터 평가 불가 ----
function runBaseline(ctx, etf, startIdx, startValue, depositsFrom) {
  const { cal, mk, depositsBy } = ctx;
  const last = cal.index(mk.lastSession);
  let shares = 0, cash = startValue, pending = startValue, halt = null;
  const seen = new Set(), valued = new Map([[etf, []]]), own = new Map([[etf, new Set()]]), log = [];
  const haltAt = (reason, since) => { if (!halt || since < halt.since) halt = { reason, since }; };
  const days = [];
  for (let i = startIdx; i <= last; i++) {
    const d = cal.sessions[i];
    let flow = 0;
    if (i > startIdx) {
      for (const dep of depositsBy.get(d) || []) if (i >= depositsFrom) { cash += dep.amount; pending += dep.amount; flow += dep.amount; }
      for (const s of mk.splitsOn(d)) {
        if (s.ticker !== etf) continue;
        const r = splitAction(s, d, i, cal.sessions[startIdx], seen, valued, own, log, mk, cal);
        if (r?.action !== 'applied') continue;
        shares = Math.round(shares * s.ratio);
        if (r.halt) haltAt('splitDelay', s.effectiveDate);
      }
      // 지원하지 않는 기업 사건: 시나리오와 같이, 사건일 전날 장 마감에 그 ETF를 보유했으면 사건일부터 평가 불가
      for (const e of mk.eventsOn(d)) {
        if (e.ticker !== etf) continue;
        const from = cal.index(e.date);
        if (own.get(etf).has(from - 1)) haltAt('corporateEvent', e.date);
      }
    }
    if (pending > 0 && mk.usable(etf, d)) {
      const c = mk.close(etf, d), q = Math.floor((pending * 1e4) / c);
      if (q > 0) { shares += q; cash -= Math.min(pending, Math.round((q * c) / 1e4)); pending = 0; log.push({ i, t: etf, side: 'buy', q }); }
    }
    let v = null;
    if (shares === 0) v = mk.dayOk(d) ? cash : null;
    else if (mk.usable(etf, d)) v = cash + Math.round((shares * mk.close(etf, d)) / 1e4);
    if (shares > 0) { own.get(etf).add(i); if (v !== null) valued.get(etf).push(i); }
    days.push({ date: d, value: v, flow });
  }
  if (days.length) days[0].flow = 0;
  if (halt) for (const x of days) if (x.date >= halt.since) x.value = null;
  return { days, halted: halt };
}

// ---- TWR: 입금은 그날 장 시작 전에 들어온 것으로 보고 일별로 잇는다. 미확정일은 건너뛰어 다음 확정일까지 한 구간으로
// 잇고, 그 구간에 입금이 끼면 그 뒤 누적 TWR은 미확정이다(설계 4절, 사용자 확인 10-20). ----
export function twr(days) {
  const out = [];
  let cum = 1, lastV = null, gap = 0, flows = 0, broken = false;
  days.forEach((x, j) => {
    if (j === 0) { lastV = x.value; out.push(x.value === null ? null : 0); if (x.value === null) broken = true; return; }
    gap++; flows += x.flow || 0;
    if (x.value === null || broken) { out.push(null); if (x.value !== null) lastV = x.value; return; }
    let r;
    if (gap === 1) {
      const base = lastV + flows;
      r = base > 0 ? x.value / base : (x.value === 0 ? 1 : NaN);
    } else if (flows === 0) {
      r = lastV > 0 ? x.value / lastV : (x.value === 0 ? 1 : NaN);
    } else r = NaN;
    if (!Number.isFinite(r)) { broken = true; out.push(null); lastV = x.value; gap = 0; flows = 0; return; }
    cum *= r; out.push(cum - 1); lastV = x.value; gap = 0; flows = 0;
  });
  return out;
}

function finish(res, ctx, depositsFrom) {
  // 늦은 분할로 멈춘 시나리오는 효력일부터 평가 불가
  if (res.halted) for (const x of res.days) if (x.date >= res.halted.since) { x.value = null; x.why = ['halted:' + res.halted.reason]; }
  // 출발일이나 그 전부터 멈췄으면 출발 평가액 자체가 틀렸다 — 출발하지 않은 것으로 보고하고 기준선도 만들지 않는다
  if (res.halted && res.started !== null && res.halted.since <= res.started) { res.started = null; res.waiting = res.halted.reason; }
  const started = res.started !== null;
  const tail = started ? res.days.filter((x) => x.date >= res.started) : [];
  const t = twr(tail);
  const base = {}, baseHalts = {};
  if (started) {
    for (const e of BASELINES) {
      const b = runBaseline(ctx, e, res.startIdx, res.startValue, depositsFrom);
      const bt = twr(b.days);
      base[e] = b.days.map((x, j) => ({ date: x.date, value: x.value === null ? null : x.value / 100, twr: bt[j] }));
      if (b.halted) baseHalts[e] = b.halted;
    }
  }
  let provisional = false, run = 0, cumDep = 0;
  const provDays = new Set([...res.trades, ...res.skips].filter((x) => x.provisional).map((x) => x.date)
    .concat(res.months.filter((m) => m.provisional).map((m) => m.decisionDate)));
  res.days = res.days.map((x) => {
    const j = tail.indexOf(x);
    if (provDays.has(x.date)) provisional = true;
    const live = j >= 0 && !(res.halted && x.date >= res.halted.since);   // 출발 뒤, 멈추기 전
    run = live && x.value === null ? run + 1 : 0;
    if (j > 0) cumDep += x.flow;
    const row = {
      date: x.date, value: x.value === null ? null : x.value / 100, deposits: cumDep / 100,
      pnl: x.value === null || j < 0 ? null : (x.value - res.startValue - cumDep) / 100,
      twr: j < 0 ? null : t[j], provisional, why: x.why,
    };
    if (run > PAUSE_AFTER) row.pause = run;
    if (j >= 0) row.vs = Object.fromEntries(BASELINES.map((e) => {
      const b = base[e][j]?.twr;
      return [e, row.twr === null || b == null ? null : (row.twr - b) * 100];
    }));
    return row;
  });
  res.startValue = res.startValue === null || !started ? null : res.startValue / 100;
  res.cumDeposits = cumDep / 100;
  res.baselines = base;
  res.baselineHalts = baseHalts;   // 기준선별 평가 불가 사유(배열 속성이 아니라 따로 — JSON으로도 남게)
  delete res.states;
  delete res.startIdx;
  delete res.log;
  delete res.own;
  return res;
}

// ---- 공개 진입점 ----
// input = {
//   records: [ledger 기록 …],
//   snapshot: { date: 'YYYY-MM-DD'(시작일, 장 마감 뒤 수량), holdings: {T: 주식 수}, cash: 달러 },
//   deposits: [{ id, amount(달러), recordedAt(ISO, 서버 시각) } | { id, cancels: 입금 id, recordedAt }],
//   settings: { holdOnly: [T] },
//   scenarios: [{ id, name, strategy: 'B'|'C'|'D'|'custom', params?, createdAt(ISO), engineVersion }],
// }
// A(그대로 보유 + 입금 적립)는 늘 계산해 맨 앞에 둔다 — 파생 시나리오의 출발점이기 때문이다.
export function replay(input) {
  const cal = makeCalendar();
  const { records, snapshot, deposits = [], settings = {}, scenarios = [] } = input || {};
  if (!Array.isArray(records) || !records.length) fail('records: 비어 있다');
  if (!snapshot || !isDate(snapshot.date) || !cal.isSession(snapshot.date)) fail('snapshot.date: 거래일이어야 한다');
  const mk = makeMarket(records, cal);
  if (mk.lastSession < snapshot.date) fail('records: 시작일 뒤 기록이 없다');
  const shares0 = new Map();
  for (const [t, q] of Object.entries(snapshot.holdings || {})) shares0.set(t, micro(q, 'snapshot.holdings'));
  const cash0 = cents(snapshot.cash ?? 0, 'snapshot.cash');
  const holdOnly = new Set(settings.holdOnly || []);
  const snapIdx = cal.index(snapshot.date);
  const lastIdx = cal.index(mk.lastSession);

  // 입금 반영일 = 기록 시각 뒤 처음 오는 09:30 ET의 거래일. 반영일 장 시작 전에 들어온 취소 기록만 그 입금을 없앤다.
  const warnings = [];
  const effective = (ms) => effectiveDay(cal, ms);
  const deps = [], cancels = [];
  for (const x of deposits) {
    const ms = toMs(x?.recordedAt);
    if (!Number.isFinite(ms)) fail('deposits: recordedAt 형식 오류');
    if (x.cancels) cancels.push({ ...x, ms });
    else deps.push({ id: x.id, amount: cents(x.amount, 'deposits.amount'), ms, day: effective(ms) });
  }
  const gone = new Set();
  for (const c of cancels) {
    const dep = deps.find((p) => p.id === c.cancels);
    if (dep && dep.day !== END && c.ms < openUtcMs(dep.day)) gone.add(dep.id);
    else warnings.push({ kind: 'cancelIgnored', id: c.id });
  }
  const depositsBy = new Map();
  for (const p of deps) {
    if (gone.has(p.id)) continue;
    if (p.day <= snapshot.date) { warnings.push({ kind: 'depositBeforeStart', id: p.id }); continue; }
    (depositsBy.get(p.day) || depositsBy.set(p.day, []).get(p.day)).push(p);
  }
  const ctx = { cal, mk, holdOnly, depositsBy };

  const aInit = {
    idx: snapIdx, shares: shares0, cash: cash0, seen: new Set(), splitBase: snapshot.date,
    noDecisionBefore: addDays(snapshot.date, 1), depositsFrom: snapIdx + 1,
  };
  const A = runScenario(ctx, scenarioParams({ strategy: 'A' }), aInit, true);
  const aDay = new Map(A.days.map((x) => [x.date, x]));
  const results = [null];

  for (const sc of scenarios) {
    if (!sc || sc.strategy === 'A') fail('scenario: A는 따로 넣지 않는다');
    const prm = scenarioParams(sc);
    const created = toMs(sc.createdAt);
    if (!Number.isFinite(created)) fail('scenario: createdAt 형식 오류');
    // 만든 날 다음 거래일 S부터다. S가 점검일이면 그날은 결정하지 않는다(어느 출발 경로든 같다). 출발이 S 뒤로 미뤄져도
    // 결정 금지일은 S 하나뿐이다 — 출발 전 날에는 어차피 결정하지 않는다.
    // S가 A의 첫 활동일 이하면 시작 스냅샷에서 출발하고, 아니면 S 전 거래일 장 마감 뒤 A의 상태에서 출발한다.
    const S = cal.onOrAfter(addDays(etWall(created).date, 1));
    const meta = { id: sc.id, strategy: sc.strategy, name: sc.name ?? null, notes: prm.notes,
      engineCreated: sc.engineVersion ?? null, engineMismatch: (sc.engineVersion ?? null) !== ENGINE_VERSION };
    let init;
    const firstActive = cal.onOrAfter(addDays(snapshot.date, 1));
    const noS = addDays(S, 1);   // S 다음 날부터 결정할 수 있다(S가 첫 활동일보다 이르면 첫 활동일부터)
    if (S !== END && S <= firstActive) init = { ...aInit, noDecisionBefore: firstActive === END ? END : (noS > firstActive ? noS : firstActive) };
    else if (S === END || cal.index(S) - 1 > lastIdx) { results.push({ ...meta, started: null, waiting: 'notYet' }); continue; }
    else {
      // A의 평가가 확정된 첫날(≥ S 전 거래일)에서 출발한다. A가 늦은 분할로 멈췄으면 멈춘 효력일 전까지만 출발할 수 있다.
      const okA = (j) => A.states.has(j) && aDay.get(cal.sessions[j])?.value !== null
        && !(A.halted && cal.sessions[j] >= A.halted.since);
      let j = cal.index(S) - 1;
      while (j <= lastIdx && !okA(j)) j++;
      if (j > lastIdx) { results.push({ ...meta, started: null, waiting: 'aUndetermined' }); continue; }
      const s = A.states.get(j);
      init = {
        idx: j, shares: s.shares, cash: s.cash, seen: s.seen, splitBase: snapshot.date, log: A.log.filter((x) => x.i <= j),
        own: [...A.own].map(([t, ks]) => [t, [...ks].filter((k) => k <= j)]),
        // 기다리는 동안 지나간 점검일(S 다음 날 ~ 출발 전날)도 사건으로 남긴다
        preEvents: cal.sessions.slice(cal.index(S), j).filter((x) => x === cal.checkDay(x) && x >= addDays(S, 1))
          .map((x) => ({ date: x, kind: 'decisionDropped', checkDate: x, reason: 'notStarted' })),
        noDecisionBefore: addDays(S, 1), depositsFrom: j + 1,
      };
    }
    const r = runScenario(ctx, prm, init, false);
    results.push({ ...meta, ...finish(r, ctx, init.depositsFrom) });
  }
  results[0] = { id: 'A', strategy: 'A', name: null, notes: [], ...finish(A, ctx, aInit.depositsFrom) };
  const missingSessions = [];
  for (let i = cal.index(mk.by.keys().next().value); i <= lastIdx; i++) {
    if (!mk.dayOk(cal.sessions[i])) missingSessions.push(cal.sessions[i]);
  }
  return { engineVersion: ENGINE_VERSION, lastSession: mk.lastSession, missingSessions, warnings, scenarios: results };
}

function effectiveDay(cal, ms) {
  const wall = etWall(ms).date;
  let d = cal.onOrAfter(wall < cal.first ? cal.first : wall);
  if (d !== END && openUtcMs(d) <= ms) d = cal.onOrAfter(addDays(d, 1));
  return d;
}

// 화면용: 입금 기록 시각(ISO)의 반영일과 취소 마감(반영일 09:30 ET, ms). 달력 밖이면 { day: null }.
export function depositTiming(iso) {
  const ms = toMs(iso);
  if (!Number.isFinite(ms)) return { day: null, cancelBefore: null };
  const d = effectiveDay(makeCalendar(), ms);
  return d === END ? { day: null, cancelBefore: null } : { day: d, cancelBefore: openUtcMs(d) };
}

// 화면용: 거래일인지(달력 밖이면 false).
export function isTradingDay(d) {
  const cal = makeCalendar();
  return isDate(d) && d >= cal.first && d <= cal.sessions[cal.sessions.length - 1] && cal.isSession(d);
}

export const _internal = { makeCalendar, makeMarket, blocked, EngineInputError };
