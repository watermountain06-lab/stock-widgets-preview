// 업종 묶음(preview-only-portfolio-sectors.js) 시험 — node --test pipeline/portfolio/test_sectors.mjs
// 계산 시험은 보유가 아닌 종목·가짜 티커만 쓴다(공개 저장소).
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { SECTOR, ETF, TOPS, SUB_LABEL, catOf, sectorGroups } from '../../preview-only-portfolio-sectors.js';

const root = new URL('../../', import.meta.url);
const snap = JSON.parse(readFileSync(new URL('pipeline/portfolio/sector_snapshot.json', root), 'utf8')).sector;
let cards = [];
try { cards = JSON.parse(readFileSync(new URL('site_data/stocks.json', root), 'utf8')).tickers; } catch (_) { /* 없으면 스냅숏만 */ }

test('모든 카드가 표에 정확히 한 분류, 기술이면 하위도 하나', () => {
  const tops = new Set(TOPS.map((d) => d.id));
  const missing = [...new Set([...Object.keys(snap), ...cards.map((c) => c.ticker)])].filter((t) => !(t in SECTOR));
  assert.deepEqual(missing, [], '표에 없는 카드: 사람이 분류해 preview-only-portfolio-sectors.js에 넣을 것');
  for (const t of Object.keys(SECTOR)) {
    const c = catOf(t);
    assert.ok(tops.has(c.top), t);
    if (c.top === 'tech') assert.ok(c.sub in SUB_LABEL, t); else assert.equal(c.sub, null, t);
  }
  for (const t of Object.keys(ETF)) assert.ok(!(t in SECTOR), 'ETF와 카드 표에 겹침: ' + t);
});

test('카드 업종 칸이 바뀌면 경고(실패 아님)', () => {
  const changed = cards.filter((c) => snap[c.ticker] != null && snap[c.ticker] !== c.sector).map((c) => c.ticker);
  if (changed.length) console.warn('업종 칸이 바뀐 카드(분류 다시 볼 것):', changed.join(', '));
});

test('경계 기대값', () => {
  const want = {
    semi: 'MRVL QCOM ADI AMAT TER SNDK AVGO MCHP KLAC',
    sw: 'SNPS CDNS IBM ACN VRSN CTSH PLTR',
    net: 'GOOGL META NFLX AMZN BKNG EBAY EXPE DASH UBER',   // 규칙 (b) 사용(사용자 결정 2026-11-18)
    hw: 'DELL WDC STX APH GLW LITE CDW MSI CSCO ANET',
    comm: 'DIS TTWO NWSA VZ TMUS CHTR T',
    health: 'UNH ELV VEEV CVS UHS',
    fin: 'PGR CB PYPL FIS FISV JKHY GPN HOOD WTW L',
    ind: 'GEV GNRC SPCX ADP LDOS',
    ener: 'AWK NEE ALB MOS',
    re: 'EQIX AMT WELL',
    cons: 'TSLA DPZ TGT HAS',
  };
  for (const [c, ts] of Object.entries(want)) for (const t of ts.split(' ')) {
    const g = catOf(t); assert.equal(g.sub || g.top, c, t);
  }
  assert.equal(catOf('QQQ').top, 'idx'); assert.equal(catOf('SPY').top, 'idx');
  assert.equal(catOf('TLT').top, 'bond'); assert.equal(catOf('GLD').top, 'bond');
  assert.equal(catOf('ZZZ1').top, 'none');
});

const near = (a, b) => assert.ok(Math.abs(a - b) < 1e-9, `${a} ≠ ${b}`);

test('합계: 상위 줄 + 표 밖 줄 = 총액, 기술 하위 합 = 기술', () => {
  const items = [{ ticker: 'AMD', value: 300 }, { ticker: 'TSM', value: 100 }, { ticker: 'MSFT', value: 50 }, { ticker: 'BKNG', value: 50 },
    { ticker: 'JPM', value: 200 }, { ticker: 'SPY', value: 100 }, { ticker: 'ZZZ1', value: 50 }];
  const total = 850 + 150;
  const { main, extra } = sectorGroups(items, 150, total);
  near([...main, ...extra].reduce((a, r) => a + r.value, 0), total);
  near([...main, ...extra].reduce((a, r) => a + r.share, 0), 1);
  const tech = main.find((r) => r.id === 'tech');
  assert.equal(main[0].id, 'tech');   // 금액 큰 순
  near(tech.value, 500); near(tech.subs.reduce((a, r) => a + r.value, 0), tech.value);
  assert.deepEqual(tech.subs.map((s) => s.id), ['semi', 'sw', 'net']);   // 금액 큰 순, 같으면 표 순서
  assert.deepEqual(tech.subs[0].tickers.map((x) => x.t), ['AMD', 'TSM']);
  assert.deepEqual(extra.map((r) => r.id), ['none', 'idx', 'cash']);   // 분류 안 됨 → 지수 ETF → 현금
  near(extra[0].value, 50);   // 표에 없는 종목도 금액 그대로
});

test('상위 줄은 표 순서가 아니라 금액 큰 순', () => {
  const { main } = sectorGroups([{ ticker: 'AMD', value: 10 }, { ticker: 'JPM', value: 30 }, { ticker: 'XOM', value: 20 }], 0, 60);
  assert.deepEqual(main.map((r) => r.id), ['fin', 'ener', 'tech']);
});

test('같은 티커 여러 건은 합치고 한 종목으로', () => {
  const { main } = sectorGroups([{ ticker: 'AMD', value: 10 }, { ticker: 'AMD', value: 30 }], 0, 40);
  assert.equal(main[0].subs[0].tickers.length, 1); near(main[0].subs[0].tickers[0].value, 40);
});

test('작은 종목 여럿: 줄 %는 반올림 전 합에서', () => {
  const items = ['AMD', 'TSM', 'INTC', 'TXN', 'LRCX'].map((t) => ({ ticker: t, value: 4 }));
  const { main } = sectorGroups(items, 990, 1010);
  near(main[0].share, 20 / 1010);   // 0.4% × 5 ≈ 2%
});

test('총액 0·현금만·음수 현금', () => {
  const z = sectorGroups([], 0, 0); assert.deepEqual(z, { main: [], extra: [] });
  const c = sectorGroups([], 100, 100); assert.deepEqual(c.extra.map((r) => [r.id, r.share]), [['cash', 1]]);
  const n = sectorGroups([{ ticker: 'AMD', value: 10 }], -5, 10); assert.equal(n.extra.length, 0);   // 음수 현금은 보유 막대처럼 줄에서 뺀다
  const nul = sectorGroups([{ ticker: 'AMD', value: 10 }], 0, 0); assert.equal(nul.main[0].share, null);
});
