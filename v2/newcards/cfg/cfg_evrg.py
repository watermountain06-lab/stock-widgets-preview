# EVRG(에버지) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 캔자스·미주리 규제 전력(발전·송배전, Evergy Kansas Central·Evergy Metro·Missouri West), 단일 부문.
# 출처: SEC XBRL + 인라인 XBRL 보충(BUILD overlay — companyfacts에 8/5 Q2 10-Q가 없다), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 장 전 07시 발표 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/EVRG.md.
# 엔진 입력(2026-10-30): 차입금 = 어음·CP $2,331.0M + 매출채권 담보차입 $356.0M + 1년 안 장기부채 $1,495.3M(2027 전환사채 $1,155.9M 포함) + 장기 $12,315.7M = $16,498.0M(DEBT_TOTAL_TAG — 증권화 채권 $288.1M은 장기부채 안), 현금 $21.8M.
# 2026-10-30 사용자 결정(공시 대기만으로 보류하지 않는다) — Q3 10-Q(11월 초 예상) 전 Q2 기준. Q4 2022·2023·2025 EPS는 보도자료 값(Q4_EPS_OVERRIDE). 자기 이력은 2022-02-25부터(HISTORY_START — 2021년 1~3분기 장기부채 태그 없음), 단기 차입은 어음·CP 줄 없으면 CommercialPaper(튜플).
# 일회성: 최근 4분기 GAAP 3.94 대 회사 조정 4.02(약 2% — 초기 단계 청정에너지 투자 손익, 전환사채 매입 손실).
BUILD = {'overlay': True}
CIK = '0001711269'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, 0, -2), '고평가'
CO = 'Evergy'
S_ = 'https://www.sec.gov/Archives/edgar/data/1711269/'
SEC = S_
SEC0 = S_ + '000'   # 보도자료 8-K 중 세 건은 제출 대리인 접수 번호(0001104659-…)
TENQ = S_ + '000171126926000100/evrg-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': SEC0 + '119312526336661/d55157dex991.htm', 'q1': SEC0 + '119312526210269/d947347dex991.htm',
      'q4': SEC0 + '119312526058075/d29762dex991.htm', 'q3': SEC0 + '119312525268034/d94343dex991.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="evrgFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 30)
ACT_REASON = '유틸리티라 재고·매출채권 회전으로 보는 활동성이 잘 맞지 않는다'
NONOP_WHAT = '투자'
MODEL_NOTE = ('발전·송배전 설비 투자(상반기 $1.8B)가 감가상각보다 커서, 큰 차입금(약 $16.5B)을 뺀 현금흐름 모델의 값이 0 아래로 나온다 — 규제 유틸리티는 그 투자가 요금 기준 자산이 되어 이익으로 돌아오는 구조라 현금흐름 모델과 PCR은 의미가 약하다. '
              '2027년 만기 전환사채($1.16B)는 주가 조건을 채워 전환 가능해 1년 안 차입금으로 분류됐다. 주식 선도 매각(ATM)이 미결제라 주식 수가 늘 수 있다. 리스 $191M(금융리스 $130M 포함)은 10-Q에 리스 줄이 없어 2025-12 값이다. Q2 10-Q가 SEC 요약 자료에 아직 없어 원문 인라인 XBRL로 채웠다.')
HEALTH_EXTRA = '설비투자 자금을 사채·신주로 조달하는 구조라 차입금 비중이 높게 나온다 — 규제 유틸리티에서는 흔한 모습이다.'
# 현금흐름 0 이하 — SO·ATO와 같은 문구 보정(0 이하가 아니면 바뀌지 않는다)
POST = [r'''
_R = '현금흐름 모델의 주당 지분가치가 0 이하라(큰 차입금을 뺀 뒤) 기본 시나리오 환산 성장률은 해석할 수 없다.'
_pairs = [
 ("fill('[data-dcf-basev]', '$' + (Math.abs(D.base) < 10 ? D.base.toFixed(2) : Math.round(D.base)));",
  "fill('[data-dcf-basev]', '$' + (Math.abs(D.base) < 10 ? D.base.toFixed(2) : Math.round(D.base)));\n  if (D.base <= 0) { const _rv = document.querySelector('#dcf .reverse'); if (_rv) _rv.textContent = _XR; }"),
 ("const tv = D.tvShare != null ? `잔존가치(5년 뒤)가 내재가치의 ${Math.round(D.tvShare * 100)}%` : '';",
  "const tv = D.base <= 0 ? '잔존가치 비중 — 내재가치가 0 이하라 의미 없음' : (D.tvShare != null ? `잔존가치(5년 뒤)가 내재가치의 ${Math.round(D.tvShare * 100)}%` : '');"),
 ("`현재가 $${price.toFixed(2)} 가 정당화되려면 5년 내내`\n          + ` 연 ${(d.requiredGrowth*100).toFixed(1)}% 매출 성장이 필요하다.`)",
  "(d.base <= 0 ? _XR : `현재가 $${price.toFixed(2)} 가 정당화되려면 5년 내내`\n          + ` 연 ${(d.requiredGrowth*100).toFixed(1)}% 매출 성장이 필요하다.`))"),
]
for _x, _y in _pairs:
    if _x in h:
        h = h.replace(_x, _y)
if 'const _XR' not in h:
    h = h.replace('<script>', '<script>\nconst _XR = ' + repr(_R) + ';', 1)
import re as _re
h = _re.sub(r'잔존가치\(5년 뒤\)가 내재가치의 [0-9,]+%', '잔존가치 비중 — 내재가치가 0 이하라 의미 없음', h)
h = _re.sub(r'(id="evrgDcfReq"[^>]*>)연 -[0-9.]+%', lambda m: m.group(1) + '해석 부적합', h)
h = _re.sub(r'현재가를 정당화하려면 매출이 5년간 연 [−-][0-9.]+% 커야 한다\. ', '현금흐름 값이 0 이하라 현재가 요구 성장률은 해석할 수 없다. ', h)
''']
# 헤더 '현재가 요구 성장' 칸 — 현금흐름 값이 0 이하이면 숫자 대신 '해석 부적합'(AEE Fable r1, 2026-10-25)
POST.append(r'''
h = h.replace("  if (req && price != null) {", "  if (req && d.base <= 0) { req.textContent = '해석 부적합'; req.style.color = 'var(--text3)'; const _c = req.closest('.meta-item'); if (_c) _c.title = '해석 부적합(현금흐름 0 이하) — 현금흐름 내재가치가 0 이하라 현재가 요구 성장률을 해석할 수 없다.'; }\n  if (req && price != null && d.base > 0) {", 1)
import re as _re2
h = _re2.sub(r'(id="evrgDcfReq"[^>]*>)연 [−-][0-9.]+%', lambda m: m.group(1) + '해석 부적합', h)
''')
PH = ['NEE', 'SO', 'DUK', 'AEP', 'XEL', 'AEE']
PEER_FILE = 'peer_universe/utilities.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '유틸리티 6곳 PER 비교 (점수는 S&P500 유틸리티 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 유틸리티 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 유틸리티 대비 배수 순위 (v2/peer_universe/utilities.json)'
PEER_TIP = ('S&P500 유틸리티(EVRG 제외)와 배수 순위를 매긴 값이다.',
            '규제 전력·가스, 독립 발전사, 수도가 섞여 있다. 차트에는 유틸리티 6곳만 보인다.')
# 매출(Q2 2026 10-Q 고객 구분, 계약 매출 1,425.7) — 주거 528.4 + 상업 507.1 + 산업 170.2 + 송전 134.5 + 도매 68.1 + 기타 소매 12.2 + 기타 5.2, 계약 외 매출 74.4는 조정.
SEG = [('소매 — 주거', 528.4, '#0057b8'), ('소매 — 상업', 507.1, '#4f8fd6'), ('소매 — 산업', 170.2, '#9cc3ea'), ('송전', 134.5, '#78be20'), ('도매', 68.1, '#5b6770'), ('기타 소매·기타', 17.4, '#bbbbbb')]
SEG_ADJ = 74.4
SEG_ADJ_LABEL = '계약 외 매출(대체 수익 프로그램 등)'
SEG_TITLE = '매출 구성 — 고객 구분'   # 분기는 fill.py가 실제 값으로 붙인다 — 손으로 적으면 분기를 넘길 때 두 번 나온다(2026-10-30)
NEWS_RANGE = '2025.11 ~ 2026.08'
NEWS = [
    ('neutral', '2026년 8월 6일 장 전 — Q2 2026 실적', '2026-08-06',
     '매출 $1.50B(+4.4%) · 순이익 $215M · 희석 EPS $0.91(1년 전 $0.74) · 조정 EPS $0.88 · 2026 조정 EPS 전망 4.14~4.34 재확인 — 당일 주가 0.0%', 'q2', 'Evergy 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 5월 7일 장 전 — Q1 2026 실적', '2026-05-07',
     '매출 $1.44B(+5.0%) · 순이익 $152M · 희석 EPS $0.64(1년 전 $0.54) — 전환사채 매입 손실 주당 $0.05 포함 — 당일 주가 +2.1%', 'q1', 'Evergy 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 19일 장 전 — Q4 2025 실적', '2026-02-19',
     '순이익 $84M · 희석 EPS $0.36(1년 전 $0.34) · 2025년 EPS $3.66 — 당일 주가 −1.1%', 'q4', 'Evergy 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 11월 6일 장 전 — Q3 2025 실적', '2025-11-06',
     '매출 $1.81B · 순이익 $475M · 희석 EPS $2.03(1년 전 $2.02) — 당일 주가 −1.6%', 'q3', 'Evergy 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 16, 'nt': 13, 'mean': 91.23, 'median': 92, 'low': 85, 'high': 97, 'sb': 9, 'b': 2, 'h': 5, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-30'


# ── 자동 카드 — 원문 대조: Q2 2026 528.4/507.1/170.2/134.5/68.1/12.2+5.2(2026-10-30) ──
AUTO = True
SEG_MAP = {
 "parts": [
  {"concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"], "axis": "srt:MajorCustomersAxis", "extra": {},
   "members": {"evrg:ElectricUtilityCustomerClassResidentialMember": ["소매 — 주거", "#0057b8"], "evrg:ElectricUtilityCustomerClassCommercialMember": ["소매 — 상업", "#4f8fd6"], "evrg:ElectricUtilityCustomerClassIndustrialMember": ["소매 — 산업", "#9cc3ea"], "evrg:ElectricUtilityCustomerClassTransmissionMember": ["송전", "#78be20"], "evrg:ElectricUtilityCustomerClassWholesaleMember": ["도매", "#5b6770"], "evrg:ElectricUtilityCustomerClassOtherRetailMember": ["기타 소매·기타", "#bbbbbb"], "evrg:ElectricUtilityCustomerClassOtherMember": ["기타 소매·기타", "#bbbbbb"]},
   "ignore": ["evrg:ElectricUtilityCustomerClassTotalElectricRetailMember"]}
 ]
}
