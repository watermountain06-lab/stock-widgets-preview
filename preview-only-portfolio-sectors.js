// 업종 묶음(보기 전용, 2026-11-18 사용자 결정 + dr 4라운드 합의). 원칙(매수 규칙)은 바꾸지 않는다.
// 최종 기준은 이 표다. 카드 업종 칸(자유 문장)의 낱말 매칭은 새 카드 초안에만 쓰고, 사람이 확인해 여기에 넣는다.
// 경계는 GICS를 따르되 두 가지만 다르게: (a) 기술 아래 반도체를 따로 (b) 인터넷 플랫폼(검색·SNS·스트리밍·전자상거래·온라인 여행·배달·차량 호출)은 기술로.
// 판단이 갈린 카드: SNDK(NAND 칩 → 반도체), SNPS·CDNS(EDA → 소프트웨어), AVGO·TER → 반도체, VEEV → 헬스케어(고객이 생명과학뿐),
// SPCX → 산업재(항공우주), L → 금융(보험 CNA), EQIX·AMT → 부동산(리츠), PYPL·HOOD → 금융(플랫폼 아님), DPZ·TGT → 소비, TSLA → 소비.
// 카드 기준: origin/main site_data/stocks.json db27e27c(2026-11-18, 370개). BR·AXON → 산업재(GICS), TRMB·ROP → 소프트웨어. 시험: pipeline/portfolio/test_sectors.mjs
export const TOPS = [
  { id: 'tech', label: '기술', subs: ['semi', 'sw', 'net', 'hw'] },
  { id: 'comm', label: '통신·미디어' }, { id: 'cons', label: '소비' }, { id: 'fin', label: '금융' },
  { id: 'health', label: '헬스케어' }, { id: 'ind', label: '산업재' }, { id: 'ener', label: '에너지·소재·유틸리티' },
  { id: 're', label: '부동산' },
];
export const SUB_LABEL = { semi: '반도체', sw: '소프트웨어·서비스', net: '인터넷 플랫폼', hw: '하드웨어·부품' };
// 표 밖 줄(맨 아래): 지수 ETF는 속을 펼치지 않는다(직접 보유 기준)
export const EXTRA_LABEL = { idx: '지수 ETF', bond: '채권·금 ETF', cash: '현금', none: '분류 안 됨' };
const LIST = {
  semi: 'ADI AMAT AMD ASML AVGO INTC KLAC LRCX MCHP MRVL MU NVDA QCOM SKHY SNDK TER TSM TXN',
  sw: 'ACN ADBE ADSK CDNS CRM CRWD CTSH DDOG FFIV FICO FTNT GEN IBM INTU IT MSFT NOW ORCL PANW PLTR PTC ROP SNPS TRMB TWLO VRSN WDAY',
  net: 'AMZN BKNG DASH EBAY EXPE GOOGL META NFLX UBER',
  hw: 'AAPL ANET APH CDW CIEN COHR CSCO DELL GLW HPE HPQ JBL KEYS LITE MSI NTAP P STX TDY TEL WDC ZBRA',
  comm: 'CHTR DIS FOXA LYV NWSA OMC T TMUS TTWO VZ',
  cons: 'ADM APTV BBY BFB BG CASY CCL CHD CL CMG COST DECK DG DHI DLTR DPZ DRI EL F GIS GM GPC GRMN HAS HD HLT HRL KHC KMB KO LOW LULU LVS MAR MCD MDLZ MKC MNST MO NCLH NKE ORLY PEP PG PHM PM RCL RL ROST SBUX SJM SYY TGT TJX TPR TSCO TSLA TSN ULTA WMT WSM WYNN',
  fin: 'ACGL AIZ AJG ALL AON AXP BAC BEN BLK BNY BRKB BRO BX C CB CINF CME COF COIN CPAY EG FDS FIS FISV GPN GS HOOD ICE IVZ JKHY JPM L MA MCO MRSH MS MSCI MTB NDAQ PGR PYPL RJF SCHW SYF TROW TRV USB V WFC WRB WTW XYZ',
  health: 'A ABBV ABT ALGN AMGN BAX BIIB BMY BSX CNC COO COR CRL CVS DGX DHR DVA DXCM ELV GEHC GILD HCA HSIC IDXX ILMN INCY IQV ISRG JNJ LH LLY MCK MRK MRNA MTD PFE PODD REGN RMD RVTY SYK TECH TMO UHS UNH VEEV VRTX VTRS WST ZBH',
  ind: 'ADP ALLE AME AOS AXON BA BE BR CARR CAT CHRW CMI CSX CTAS DAL DE DOV EFX EME EMR ETN EXPD FAST FIX GD GE GEV GNRC GWW HII HUBB HWM IEX IR ITW JBHT LDOS LII LMT LUV MAS MMM NDSN NOC NSC ODFL OTIS PAYX PCAR PH PWR ROL RSG RTX SPCX SWK TDG TT UAL UNP UPS VLTO VRSK VRT WAB WM XYL',
  ener: 'AEE AEP AES ALB AMCR APD ATO AVY AWK BALL CEG CF CNP COP CRH CVX D DOW DUK ECL ED EIX EOG ES ETR EVRG EXC FANG FCX FE IP KMI LIN LNT LYB MLM MOS MPC NEE NEM NI NUE OKE PCG PEG PKG PNW PPG PPL PSX SHW SLB SO SRE STLD TRGP VLO VMC WEC WMB XEL XOM',
  re: 'AMT ARE BXP CPT CSGP DLR DOC EQIX ESS EXR FRT HST INVH IRM KIM MAA O PLD REG SBAC SPG UDR VICI WELL WY',
};
// ETF 표: 넓은 주식 지수 → idx, 채권·금 → bond. 업종 ETF를 사면 여기에 그 업종 코드(예: SOXX: 'semi')로 넣는다
export const ETF = { SPY: 'idx', QQQ: 'idx', DIA: 'idx', IWM: 'idx', RSP: 'idx', VOO: 'idx', VTI: 'idx', TLT: 'bond', GLD: 'bond' };
export const SECTOR = Object.fromEntries(Object.entries(LIST).flatMap(([c, s]) => s.split(' ').map((t) => [t, c])));
const SUB_TOP = { semi: 'tech', sw: 'tech', net: 'tech', hw: 'tech' };

// 티커 → { top, sub }. top: TOPS의 id | 'idx' | 'bond' | 'none'
export function catOf(t) {
  const c = SECTOR[t] ?? ETF[t];
  if (!c) return { top: 'none', sub: null };
  if (SUB_TOP[c]) return { top: SUB_TOP[c], sub: c };
  return { top: c, sub: null };
}

// items: [{ ticker, value }] (같은 티커가 여러 번이면 합친다), cash: 현금(0 이하면 줄 없음), total: 분모(보유 막대와 같은 값)
// 돌려줌: { main: [줄], extra: [줄] }. 줄 = { id, label, value, share, tickers: [{ t, value, share }], subs?: [줄] }
// main은 금액 큰 순, extra는 분류 안 됨 → 지수 ETF → 채권·금 ETF → 현금. 보유 0인 분류는 뺀다. share는 반올림 전 비율(0~1), total ≤ 0이면 null
export function sectorGroups(items, cash, total) {
  const val = new Map();
  for (const x of items) if (x.value > 0) val.set(x.ticker, (val.get(x.ticker) || 0) + x.value);
  const sh = (v) => (total > 0 ? v / total : null);
  const line = (id, label, ts) => {
    const tickers = ts.map((t) => ({ t, value: val.get(t), share: sh(val.get(t)) })).sort((a, b) => b.value - a.value || (a.t < b.t ? -1 : 1));
    const value = tickers.reduce((a, x) => a + x.value, 0);
    return { id, label, value, share: sh(value), tickers };
  };
  const by = new Map();
  for (const t of val.keys()) { const { top } = catOf(t); if (!by.has(top)) by.set(top, []); by.get(top).push(t); }
  const main = [];
  for (const d of TOPS) {
    const ts = by.get(d.id); if (!ts) continue;
    const r = line(d.id, d.label, ts);
    if (d.subs) r.subs = d.subs.map((s) => ts.filter((t) => catOf(t).sub === s)).map((g, i) => (g.length ? line(d.subs[i], SUB_LABEL[d.subs[i]], g) : null)).filter(Boolean).sort((a, b) => b.value - a.value);
    main.push(r);
  }
  main.sort((a, b) => b.value - a.value);
  const extra = ['none', 'idx', 'bond'].filter((k) => by.has(k)).map((k) => line(k, EXTRA_LABEL[k], by.get(k)));
  if (cash > 0) extra.push({ id: 'cash', label: EXTRA_LABEL.cash, value: cash, share: sh(cash), tickers: [] });
  return { main, extra };
}
