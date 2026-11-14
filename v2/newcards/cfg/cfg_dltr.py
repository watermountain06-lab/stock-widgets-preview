BUILD = {'company_tags': [('dltr:DepreciationDepletionandAmortizationExcludingDebtDiscountAndIssuanceCosts', 'DepreciationDepletionAndAmortization')]}   # FY26부터 현금흐름표 D&A가 회사 고유 태그(상반기 $356.8M) — 표준 태그는 FY25에서 멈춤(Codex r1, 2026-11-09)
CIK = '0000935703'
# DLTR(달러 트리) v2 카드 설정 — 자동 카드(AUTO), 정식. 회계연도 1월 말 가까운 토요일(FY26 = 2026-02~2027-01). 균일가·다가격 할인 매장 Dollar Tree(2025-07 Family Dollar 매각, 중단사업).
# 출처: SEC XBRL, Q2 FY26 10-Q(2026-08-27 06:35 동부 장 전 → 그날, 카드 기준일 11-06 종가), 실적 보도자료(8-K 2.02항 — 모두 장 전 06:3x 동부 → 그날),
#        자사주 한도 보충(2026-07-02). Q3 FY26 실적은 2026-11-24 장 전 예정.
# 보류 목록 D군(안건 E54) — 30% 규칙: 최근 4분기 계속사업 GAAP 희석 EPS 8.22(1.20 + 2.56 + 1.76 + 2.70) 대 회사 조정 EPS 8.21(1.21 + 2.56 + 1.74 + 2.70 — 회사는 관세 환급을 조정에서 빼지 않는다).
#   일회성은 Q2 FY26 관세 환급 순효과 주당 $1.31(회사 조정 EPS에도 포함) 하나가 거의 전부 → GAAP의 약 16%라 정식(2026-11-09).
# 엔진 입력(2026-11-09): 차입금 $2,933.5M(장기, 1년 안 만기 0), 현금 $1,058M. 자본 StockholdersEquity(fetch_financials).
#   4분기 EPS FY25는 보도자료 계속사업 값(Q4_EPS_OVERRIDE — 역산 2.50은 중단사업 포함, 보도자료 계속사업 2.56).
CUR, YO, QO = '2026-08-01', '2025-08-02', '2026-05-02'
QLABEL, YL, QQL = 'Q2 FY26', 'Q2 FY25', 'Q1 FY26'
L8 = ['Q3 FY24', 'Q4 FY24', 'Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26']
FY_ENDS, FY_LABEL = ('2026-01-31', '2025-02-01'), 'FY2025'
VOTES, VERDICT = (0, 1, -1), '적정'
CO = 'Dollar Tree'
S_ = 'https://www.sec.gov/Archives/edgar/data/935703/'
SEC = S_
TENQ = S_ + '000093570326000109/dltr-20260801.htm'; TENQ_NAME = 'Q2 FY26 10-Q'
PR = {'q2': S_ + '000093570326000108/ex991q2-26earningspressrel.htm', 'q1': S_ + '000093570326000064/ex991q1-26earningspressrel.htm',
      'q4': S_ + '000093570326000024/ex991q4-25earningspressrel.htm', 'q3': S_ + '000093570325000104/ex991q3-25earningspressrel.htm',
      'bb': S_ + '000093570326000075/ex991sharebuybackreplenish.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="dltrFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (-120, 25)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('최근 4분기 계속사업 GAAP 희석 EPS($8.22)는 회사 조정 EPS($8.21)와 거의 같지만, 둘 다 2분기에 받은 관세 환급의 순효과(주당 $1.31)를 포함한다 — 회사는 이것을 조정 EPS에서 빼지 않지만 카드는 일회성으로 본다. 일회성은 이 환급이 대부분이고(그 밖엔 전략 검토 비용·보험 이익 등 주당 몇 센트) GAAP의 약 16%라 30% 기준 아래다. '
              '환급을 빼면 최근 4분기 EPS는 약 $6.9로, PER은 표시값보다 약 20% 높아 자기 이력 중앙값 쪽으로 간다. 영업이익률도 마찬가지다 — 2분기 영업이익률 상승 9.0%p 가운데 6.5%p가 환급 몫이다(회사 공시). 3분기 전망(조정 EPS $0.80~0.95)에는 환급분을 다시 투자하는 비용(주당 약 $0.50)이 들어 있어, 11월 24일 실적 뒤에는 환급과 재투자 비용을 순액으로 다시 센다. '
              '2025년 7월 Family Dollar를 팔아 지금은 Dollar Tree 매장만 남았다 — 과거 이력의 매출·EPS에는 Family Dollar 시절과 매각 손실이 섞여 있어, 현금흐름 모델은 네 분기가 모두 계속사업인 FY24 말 이후만 쓴다. 최근 현금흐름에는 관세 환급 현금과 Family Dollar 매각 손실에 따른 세금 절감도 들어 있어 그대로 이어진다고 보기 어렵다. 2026년 2분기 기존점 매출 +3.7%(1년 전 +6.5% 위), 객단가 +3.3%·방문객 +0.4%. 객단가를 끄는 것은 다가격 전환이다 — $1.25 기본가 위에 더 비싼 상품을 들인 매장이 2분기 말 약 6,600곳(1분기 5,900곳)이다. Family Dollar에 제공하는 전환 서비스 수입(2분기 $17.7M)은 매각 18개월 뒤인 2027년 초 끝난다. '
              '회사는 2026 회계연도 조정 EPS를 $7.70~8.05(관세 환급 순효과 약 $0.60 포함 — 빼면 $7.10~7.45, 직전 $6.70~7.10)로 올렸다. 2025년 10월 투자자 설명회에서는 2026~2028년 EPS 연평균 12~15% 성장을 목표로 냈는데, 기저 성장 8~10%에 일부 비용 소멸 효과를 더한 값이다. '
              '자사주를 크게 사고 있다 — 2025 회계연도 $1.55B, 2026년 1·2분기 $1.2B. 6월 행동주의 펀드 Mantle Ridge 등이 내놓은 블록에서 $500M을 샀고, 7월 매입 한도를 $2.5B로 다시 채웠다. 다만 8월 들어 매입은 거의 멈췄다(3분기 초 $5.3M). 3월에는 $500M 기한부 대출(2029년 만기)을 새로 받았다. '
              '주가는 2026년 5월 약 $87에서 11월 4일 $147까지 올랐다가 이틀 새 약 11% 내렸다(하락 원인은 공시에서 확인 못 함). 3분기 실적은 11월 24일 장 전에 나온다.')
PH = ['DG', 'WMT', 'COST', 'TGT', 'KR']
PEER_FILE = 'peer_universe/consumer_staples.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '할인·대형 소매 5곳 PER 비교 (점수는 S&P500 필수소비재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 필수소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 필수소비재 대비 배수 순위 (v2/peer_universe/consumer_staples.json)'
PEER_TIP = ('S&P500 필수소비재(DLTR 제외)와 배수 순위를 매긴 값이다.',
            '식품·음료·생활용품·유통이 섞여 있다. 차트에는 할인·대형 소매 회사만 보인다.')
# 매출(Q2 FY26 10-Q 상품군): 소모품 2,521.7 + 잡화 2,347.7 + 계절 상품 17.1 = 4,886.5.
SEG = [('소모품(식품·생활용품)', 2521.7, '#00843d'), ('잡화(파티·가정·완구 등)', 2347.7, '#d50032'), ('계절 상품', 17.1, '#bfe0cb')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 상품군별'
# 손 뉴스: 실적 4건 + 자사주 한도 보충. 반응일: 장 전 → 그날. 색은 사건 성격, 수치는 그날 주가.
NEWS_RANGE = '2025.12 ~ 2026.08'
NEWS = [
    ('green', '2026년 8월 27일 장 전 — Q2 FY26 실적', '2026-08-27',
     '매출 +7.0% · 기존점 +3.7% · 희석 EPS $2.70(관세 환급 순효과 $1.31 포함) · 연간 조정 EPS 전망 $7.70~8.05로 상향 · 자사주 $605M — 그날 주가 −3.9%', 'q2', 'Dollar Tree 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 7월 2일 — 자사주 매입 한도 보충', '2026-07-02',
     '6월 Mantle Ridge 관련 펀드 등의 블록 매도에서 $500M 매입 뒤 한도를 $2.5B로 다시 채움 — 그날 주가 +2.4%', 'bb', 'Dollar Tree 보도자료 (SEC 8-K)'),
    ('green', '2026년 5월 28일 장 전 — Q1 FY26 실적', '2026-05-28',
     '매출 +7.2% · 기존점 +3.5% · 희석 EPS $1.76 · 조정 EPS $1.74(+38%) · 연간 조정 EPS 전망 $6.70~7.10으로 상향 · 자사주 $595M — 그날 주가 +17.9%', 'q1', 'Dollar Tree 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 3월 16일 장 전 — FY25 4분기 실적', '2026-03-16',
     '4분기 기존점 +5.0% · 계속사업 희석 EPS $2.56(조정 +21%) · 20년 연속 기존점 증가 · FY26 조정 EPS $6.50~6.90 제시 — 그날 주가 +6.4%', 'q4', 'Dollar Tree 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 12월 3일 장 전 — Q3 FY25 실적', '2025-12-03',
     '기존점 +4.2% · 계속사업 희석 EPS $1.20 · 연간 조정 EPS 전망 $5.60~5.80으로 상향 · 연초 이후 자사주 $1.5B — 그날 주가 +3.6%', 'q3', 'Dollar Tree 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 29, 'nt': 21, 'mean': 134.24, 'median': 135, 'low': 98, 'high': 160, 'sb': 8, 'b': 3, 'h': 14, 's': 3, 'ss': 1}
ANALYST_ASOF = '2026-11-09'

AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "srt:ProductOrServiceAxis",
 "extra": {"us-gaap:StatementBusinessSegmentsAxis": "dltr:DollarTreeMember"},
 "members": {"dltr:ConsumableMember": ["소모품(식품·생활용품)", "#00843d"], "dltr:VarietyMember": ["잡화(파티·가정·완구 등)", "#d50032"], "dltr:SeasonalMember": ["계절 상품", "#bfe0cb"]}
}

NEXT_CONFIRMED = {'quarter_end': '2026-10-31', 'date': '2026-11-24', 'src': '11/3 회사 공지 — 장 시작 전, 콜 오전 8시(동부)'}
# Fable r1: 카드가 일회성으로 본 관세 환급이 마진·체크포인트·Bull/Bear에 그대로 쓰이지 않게(LUV·ZBH와 같은 처리)
POST = [r"""
import re as _re0
h = h.replace('GAAP · 1년 전 $0.91 (+197%)', 'GAAP 계속사업 · 1년 전 $0.75 (+260%, 보도자료)', 1)
_i = h.index('<div class="stat-label">FCF (')
_j = h.index('영업현금흐름 − 설비투자', _i)
h = h[:_j] + '영업현금흐름 − 설비투자 · 관세 환급 현금 포함' + h[_j + len('영업현금흐름 − 설비투자'):]
h = _re0.sub(r'(지배적 내러티브 · [^<]*영업이익률 [0-9.]+%)\(1년 전', r'\1(관세 환급 6.5%p 포함, 1년 전', h, count=1)
h = _re0.sub(r'(<span class="bb-head">마진</span><span class="bb-text">최근 4분기 영업이익률 [0-9.]+%\([^)]*\))\.', r'\1 — 2분기 관세 환급이 들어 있어 환급을 빼면 이보다 낮다.', h, count=1)
h = _re0.sub(r'(<span class="bb-head">밸류</span><span class="bb-text">[^<]*?)\.</span>', r'\1 — 관세 환급(주당 $1.31)을 빼면 PER이 중앙값 쪽으로 올라간다.</span>', h, count=1)
h = _re0.sub(r'(<span class="bb-text">순차입금\(리스 포함\) \$[0-9.]+B, 최근 4분기 영업이익의 [0-9.]+배)\.', r'\1 — 영업이익엔 관세 환급이 들어 있다.', h, count=1)
h = _re0.sub(r'<span class="bb-head">매출</span><span class="bb-text">[^<]*</span>', '<span class="bb-head">매출</span><span class="bb-text">회사 3분기 전망은 매출 $5.0~5.1B·기존점 +3~4%로 2분기(+7.0%)보다 느리다(과거 성장률은 Family Dollar 매각 뒤 이력만 쓴다).</span>', h, count=1)
_c1 = h[h.index('<strong style="color:var(--accent2);">①</strong>'):]; _c1 = _c1[:_c1.index('</div>')]
h = h.replace(_c1, '<strong style="color:var(--accent2);">①</strong> 매출이 회사 3분기 전망($5.0~5.1B, 기존점 +3~4%) 상단에 닿는지 — 다가격 매장 확대가 객단가를 계속 끌어올리는지', 1)
_c2 = h[h.index('<strong style="color:var(--accent2);">②</strong>'):]; _c2 = _c2[:_c2.index('</div>')]
h = h.replace(_c2, '<strong style="color:var(--accent2);">②</strong> 회사 조정 EPS가 3분기 전망($0.80~0.95, 관세 환급 재투자 비용 주당 약 $0.50 포함) 상단을 넘는지 — 2분기 영업이익률엔 관세 환급 6.5%p가 들어 있어 비교 기준으로 쓰지 않는다', 1)
"""]
