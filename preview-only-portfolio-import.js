// preview 전용 Portfolio 탭 — 데이터 올리기에서 CSV·Excel 읽기(2026-10-21 사용자 요청). 라이브로 옮기지 않는다 — pipeline/site_ui/UI_DIFF.md 1절 portfolio.
//
// 두 가지 표를 받아 '올린 보유'(holdings: {asOf, note, rows})를 만든다. 원칙·관심 종목은 JSON 올리기에서만 바뀐다.
//   1) Robinhood 거래 내역 CSV(Activity Date·Instrument·Trans Code·Quantity·Price·Amount): 매수·매도·분할(SPR)로 보유를,
//      평균 원가 방식으로 평균 단가를, 그 밖의 금액(입금 ACH·배당 CDIV·원천징수 NRAT·이자 INT 등)을 더해 현금을 계산한다.
//      2026-10-19 vault finance/portfolio_site.json을 만든 계산과 같다(같은 CSV로 맞춰 봄).
//   2) 보유 표(티커·수량·평균 단가 열, 이름·통화는 있으면): 그대로 옮긴다. 티커가 CASH·현금인 줄은 현금(수량 칸 = 금액).
// Excel은 화면이 첫 시트를 CSV 글자로 바꾼 뒤 여기로 넘긴다(preview-only-portfolio.js). 순수 함수라 node 시험이 부른다
// (pipeline/portfolio/test_portfolio_import.mjs). 실제 거래 내역은 공개 저장소에 넣지 않는다 — 시험은 가짜 티커만 쓴다.

// RFC 4180 CSV: 따옴표 안의 쉼표·줄바꿈·""를 처리한다(Robinhood 설명 칸에 줄바꿈이 있다)
export function parseCSV(text) {
  const s = String(text || '').replace(/^﻿/, '');
  const rows = [];
  let row = [], cell = '', q = false;
  for (let i = 0; i < s.length; i++) {
    const c = s[i];
    if (q) {
      if (c === '"') { if (s[i + 1] === '"') { cell += '"'; i++; } else q = false; }
      else cell += c;
    } else if (c === '"') q = true;
    else if (c === ',') { row.push(cell); cell = ''; }
    else if (c === '\n' || c === '\r') {
      if (c === '\r' && s[i + 1] === '\n') i++;
      row.push(cell); rows.push(row); row = []; cell = '';
    } else cell += c;
  }
  if (cell !== '' || row.length) { row.push(cell); rows.push(row); }
  return rows.filter((r) => r.some((x) => x.trim() !== ''));
}

const norm = (h) => String(h || '').toLowerCase().replace(/[\s_\-().]/g, '');
const money = (s) => {
  const t = String(s ?? '').trim();
  if (!t) return 0;
  const neg = /^\(.*\)$/.test(t) || t.startsWith('-');
  const v = Number(t.replace(/[()$,\s-]/g, ''));
  if (!Number.isFinite(v)) throw new Error('금액을 읽지 못했습니다: ' + t);
  return neg ? -v : v;
};
const num = (s) => { const t = String(s ?? '').replace(/[,\s$]/g, ''); if (!t) return NaN; const v = Number(t); return Number.isFinite(v) ? v : NaN; };   // 빈칸은 0이 아니라 모름
const r2 = (v) => Math.round(v * 100) / 100;
const r6 = (v) => Math.round(v * 1e6) / 1e6;
const DUST = 1e-4;   // 이보다 작은 잔량은 버린다(10-19 계산과 같음)

// Robinhood 날짜 m/d/yyyy → yyyy-mm-dd
function rhDate(s) {
  const m = /^(\d{1,2})\/(\d{1,2})\/(\d{4})$/.exec(String(s || '').trim());
  return m ? `${m[3]}-${m[1].padStart(2, '0')}-${m[2].padStart(2, '0')}` : null;
}

// 표(첫 줄 = 머리) → 어떤 표인지 보고 holdings를 만든다. 반환: { kind, holdings, summary, warnings }
export function importTable(rows) {
  if (!rows.length) throw new Error('빈 파일입니다.');
  const head = rows[0].map(norm);
  if (head.includes('activitydate') && head.includes('transcode')) return fromRobinhood(rows);
  return fromHoldingsTable(rows);
}

export function fromRobinhood(rows) {
  const H = rows[0].map(norm), col = (n) => H.indexOf(n);
  const ci = { date: col('activitydate'), sym: col('instrument'), desc: col('description'), code: col('transcode'), qty: col('quantity'), amt: col('amount') };
  if (Object.values(ci).some((i) => i < 0)) throw new Error('Robinhood 거래 내역의 열(Activity Date·Instrument·Description·Trans Code·Quantity·Amount)을 찾지 못했습니다.');
  // 파일은 최신이 위 — 날짜순(같은 날은 파일 아래쪽이 먼저)으로 돌린다
  const ev = [];
  rows.slice(1).forEach((r, i) => { const d = rhDate(r[ci.date]); if (d) ev.push({ d, i, r }); });
  if (!ev.length) throw new Error('날짜가 있는 거래가 없습니다.');
  ev.sort((a, b) => (a.d < b.d ? -1 : a.d > b.d ? 1 : b.i - a.i));
  const pos = new Map(), warnings = [], unknown = new Map();
  let cash = 0;
  const get = (t, name) => { if (!pos.has(t)) pos.set(t, { qty: 0, cost: 0, name: '' }); const p = pos.get(t); if (name && !p.name) p.name = name; return p; };
  for (const { d, r } of ev) {
    const code = String(r[ci.code] || '').trim(), t = String(r[ci.sym] || '').trim().toUpperCase();
    const name = String(r[ci.desc] || '').split('\n')[0].trim();
    const q = String(r[ci.qty] || '').trim();
    if (code === 'Buy' || code === 'Sell') {
      const n = num(q), a = money(r[ci.amt]);
      if (!t || !(n > 0)) throw new Error(`${d} ${code} 줄의 종목·수량을 읽지 못했습니다.`);
      const p = get(t, name);
      if (code === 'Buy') { p.qty += n; p.cost += -a; }
      else {
        const avg = p.qty > 0 ? p.cost / p.qty : 0;
        if (n > p.qty + 1e-9) warnings.push(`${d} ${t} 보유(${r6(p.qty)}주)보다 많이 판 기록(${n}주) — 가진 만큼만 뺐습니다`);
        const m = Math.min(n, p.qty);
        p.qty -= m; p.cost -= avg * m;
      }
      cash += a;
    } else if (code === 'SPR') {
      // 분할: 끝에 S가 붙은 수량은 빠지는 옛 주식, 붙지 않은 수량은 들어오는 새 주식. 원가는 그대로 둔다
      const out = /S$/i.test(q), n = num(q.replace(/S$/i, ''));
      if (!t || !(n > 0)) throw new Error(`${d} SPR 줄의 수량을 읽지 못했습니다.`);
      const p = get(t, name);
      p.qty += out ? -n : n;
    } else {
      // 금액만 있는 줄(입금·배당·원천징수·이자 등)은 현금에 더한다. 종목 수량이 걸린 모르는 코드는 처리하지 않고 알린다
      if (q && t) unknown.set(code || '(빈 코드)', (unknown.get(code || '(빈 코드)') || 0) + 1);
      cash += money(r[ci.amt]);
    }
  }
  for (const [c, n] of unknown) warnings.push(`수량이 있는 처리하지 않은 거래 ${c} ${n}건 — 보유 수량을 확인하세요`);
  const dust = [...pos.entries()].filter(([, p]) => p.qty > 1e-9 && p.qty < DUST).map(([t]) => t);
  const list = [...pos.entries()].filter(([, p]) => p.qty >= DUST).sort(([a], [b]) => (a < b ? -1 : 1))
    .map(([t, p]) => ({ name: p.name || t, ticker: t, qty: r6(p.qty), avgPrice: r2(p.cost / p.qty), currency: 'USD', account: 'Robinhood' }));
  cash = r2(cash);
  const first = ev[0].d, last = ev[ev.length - 1].d;
  const holdings = {
    asOf: `${last} 거래까지`,
    note: `Robinhood 거래 내역 CSV(${first}~${last})에서 화면이 계산. 평균 단가는 평균 원가 방식. 현금은 입금·매매·배당·원천징수·이자를 더한 계산값.`
      + (dust.length ? ` ${DUST}주 미만 잔량(${dust.join('·')})은 뺐다.` : ''),
    rows: [...list, { name: '현금(계산값)', ticker: '', qty: 1, avgPrice: cash, currency: 'USD', account: 'Robinhood' }],
  };
  return { kind: 'robinhood', holdings, warnings, summary: `Robinhood 거래 내역 ${ev.length}건(${first}~${last})에서 보유 ${list.length}종목과 현금 $${cash.toLocaleString('en-US')}를 계산했습니다.` };
}

const ALIAS = {
  ticker: ['ticker', 'symbol', '티커', '종목코드', '심볼'],
  qty: ['qty', 'quantity', 'shares', '수량', '보유수량', '주수'],
  avg: ['avgprice', 'averageprice', 'averagecost', 'avgcost', 'costpershare', 'costbasispershare', '평균단가', '매입단가', '평단', '평균매입가'],
  name: ['name', 'description', 'security', '종목', '종목명', '이름'],
  currency: ['currency', '통화'],
  account: ['account', '계좌', '증권사'],
};

export function fromHoldingsTable(rows) {
  const H = rows[0].map(norm);
  const find = (k) => H.findIndex((h) => ALIAS[k].includes(h));
  const ci = Object.fromEntries(Object.keys(ALIAS).map((k) => [k, find(k)]));
  if (ci.ticker < 0 || ci.qty < 0) throw new Error('보유 표에서 티커와 수량 열을 찾지 못했습니다(머리 줄에 Ticker/티커, Quantity/수량, Avg Price/평균 단가). Robinhood 거래 내역이면 Activity Date·Trans Code 열이 있어야 합니다.');
  const warnings = [], seen = new Set(), list = [];
  let cash = null;
  rows.slice(1).forEach((r, i) => {
    const t = String(r[ci.ticker] || '').trim().toUpperCase(), q = num(r[ci.qty]);
    if (!t && !String(r[ci.qty] || '').trim()) return;
    if (t === 'CASH' || t === '현금') {
      if (!Number.isFinite(q)) throw new Error(`${i + 2}번째 줄 현금 금액을 읽지 못했습니다.`);
      cash = (cash || 0) + q; return;
    }
    if (!/^[A-Z][A-Z0-9.-]{0,9}$/.test(t)) throw new Error(`${i + 2}번째 줄 티커(${t || '빈칸'})를 읽지 못했습니다.`);
    if (!(q > 0)) throw new Error(`${i + 2}번째 줄 ${t} 수량을 읽지 못했습니다.`);
    const a = ci.avg >= 0 ? num(r[ci.avg]) : NaN;
    if (ci.avg >= 0 && !Number.isFinite(a)) warnings.push(`${t} 평균 단가를 읽지 못해 비웠습니다`);
    if (seen.has(t)) warnings.push(`${t}가 두 줄 있습니다(내 자산에서는 합쳐 보입니다)`);
    seen.add(t);
    const cur = ci.currency >= 0 ? String(r[ci.currency] || '').trim().toUpperCase() || 'USD' : 'USD';
    list.push({ name: (ci.name >= 0 && String(r[ci.name] || '').trim()) || t, ticker: t, qty: r6(q), avgPrice: Number.isFinite(a) ? r2(a) : null,
      currency: cur, account: ci.account >= 0 ? String(r[ci.account] || '').trim() || null : null });
  });
  if (!list.length && cash == null) throw new Error('보유 줄이 없습니다.');
  if (cash == null) warnings.push('현금 줄(티커 CASH 또는 현금)이 없어 현금은 모름으로 둡니다');
  const holdings = {
    asOf: null,   // 화면이 올린 날(미국 동부)로 채운다
    note: '보유 표에서 옮김.' + (cash == null ? ' 현금 줄 없음.' : ''),
    rows: [...list, ...(cash == null ? [] : [{ name: '현금', ticker: '', qty: 1, avgPrice: r2(cash), currency: 'USD', account: null }])],
  };
  return { kind: 'table', holdings, warnings, summary: `보유 표에서 ${list.length}종목` + (cash == null ? '' : `과 현금 $${r2(cash).toLocaleString('en-US')}`) + '를 읽었습니다.' };
}
