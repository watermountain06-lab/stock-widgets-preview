# P(에버퓨어, 옛 Pure Storage — 2026-02 사명 변경, 티커 PSTG → P) v2 카드 설정 — 자동 카드(AUTO). 회계연도 1월 말 무렵 일요일. 카드 순위 194. 기업용 올플래시 스토리지·구독 서비스.
# 출처: SEC XBRL, Q2 FY27 10-Q(2026-09-05T00:03Z), 실적 보도자료(Q3 FY26~Q2 FY27, 8-K 2.02항 — 장 마감 뒤 발표, 5시 ET 콜), 8-K(사명 변경 2026-02-23), StockAnalysis. 사전 조사 자료표 scratchpad pre/P.md.
# 엔진 입력(2026-10-24): 인수 TTM $129.6M(build_dcf ACQ_FIXED — 1touch, 분기 공백으로 0이었다), 단기투자 = 유동 매도가능 채무증권 $622.2M(EV_TAGS — 기본 태그 2021 멈춤), 차입금 없음(리볼버 미사용), 4분기 EPS FY2022·2023·2024·2025 보도자료 값.
CIK = '0001474432'
CUR, YO, QO = '2026-08-02', '2025-08-03', '2026-05-03'
QLABEL, YL, QQL = 'Q2 FY27', 'Q2 FY26', 'Q1 FY27'
L8 = ['Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26', 'Q4 FY26', 'Q1 FY27', 'Q2 FY27']
FY_ENDS, FY_LABEL = ('2026-02-01', '2025-02-02'), 'FY2026'
VOTES, VERDICT = (0, -1, -2), '고평가'
CO = 'Everpure'
S_ = 'https://www.sec.gov/Archives/edgar/data/1474432/'
SEC = S_
TENQ = S_ + '000147443226000088/pstg-20260802.htm'; TENQ_NAME = 'Q2 FY27 10-Q'
PR = {'q2': S_ + '000147443226000084/everpure-ex991q2fy2027xpre.htm', 'q1': S_ + '000147443226000046/pstg-ex991q1fy2027xpressre.htm',
      'q4': S_ + '000147443226000015/pstg-ex991q4fy2026.htm', 'q3': S_ + '000147443225000062/pstg-ex991q3fy2026xpressre.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="pFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (-5, 15)
ACT_REASON = ''
NONOP_WHAT = '투자'
# 고정 문장(숫자 없음).
MODEL_NOTE = ('2026년 2월 Pure Storage에서 Everpure로 이름을 바꿨고, 그 뒤 거래소 티커도 PSTG에서 P로 바뀌었다(같은 회사·같은 SEC 등록번호). '
              '주식보상비용이 매출에서 차지하는 몫이 커서 GAAP 이익률이 낮고, 현금흐름 모델은 그 낮은 GAAP 이익률에서 출발해 성장에 드는 재투자를 빼므로 내재가치가 매우 작게 나온다 — PER·EV/EBITDA가 매우 높은 것도 같은 이유다. '
              'Q2 FY27 영업현금흐름이 마이너스인 것은 설비투자 때문이 아니라 고객 수요에 맞춘 전략적 부품 구매와 위탁 생산업체에 판 부품 대금(기타 미수금) 같은 운전자본 증가 때문이다 — 그래서 PCR·FCF가 크게 악화됐다. '
              '대형 클라우드 고객용 제품 판매로 최근 매출이 빠르게 늘었다. 실적 발표 다음 날마다 주가가 크게 내렸지만 1년 전체로는 크게 올랐다. 차입금이 없다.')
HEALTH_EXTRA = '부채비율이 높게 보이지만 부채의 대부분은 구독 선수금(이연수익)이고 차입금은 없다. 재무건전성 칸의 순현금은 운용리스까지 뺀 값이고, 내재가치 계산은 운용리스를 빼지 않는다.'   # 고정 문장(Fable r1 2026-10-24)
PH = ['DELL', 'CSCO', 'ANET', 'STX', 'IBM', 'MU']
PEER_FILE = None
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '하드웨어·저장장치 6곳 PER 비교 (점수는 카드 유니버스 IT 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = '카드 유니버스 IT 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = '카드 유니버스 IT 종목 대비 배수 순위'
PEER_TIP = ('카드 유니버스 IT 종목(P 제외)과 배수 순위를 매긴 값이다.',
            '반도체·하드웨어·소프트웨어가 섞여 있다. 차트에는 하드웨어·저장장치 6곳만 보인다.')
# 매출(Q2 FY27 10-Q) — 제품 686.8 + 구독 서비스 499.1 = 1,185.9. 1년 전 446.3·414.7. 단일 부문.
SEG = [('제품', 686.8, '#fe5000'), ('구독 서비스', 499.1, '#ff9a66')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 제품·구독'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석 — 조정 EPS·가이던스는 쓰지 않는다). 사명 변경은 MODEL_NOTE로. 반응일: 실적 8-K 장 마감 뒤 → 다음 거래일. 사명 변경 8-K 2026-02-24T02:23Z → 2/24.
# 넣지 않은 8-K: CRO 선임·전망 재확인(2025-11-05), 주총(6/12). 9/23 투자자 행사(9/24 +11%)는 8-K 없음.
NEWS_RANGE = '2025.12 ~ 2026.08'
NEWS = [
    ('red', '2026년 8월 26일 — Q2 FY27 실적', '2026-08-27',
     '매출 $1.19B(1년 전 $0.86B) · 순이익 $74M · 희석 EPS $0.21(1년 전 $0.14, 평가이익 $28M 포함) · 영업현금흐름 −$136M(부품 구매·기타 미수금 증가 — 10-Q) — 발표 다음 날 주가 −9%', 'q2', 'Everpure 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 5월 27일 — Q1 FY27 실적', '2026-05-28',
     '매출 $1.05B · 순이익 $24M · 희석 EPS $0.07(1년 전 −$0.04) — 발표 다음 날 주가 −15%', 'q1', 'Everpure 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 2월 25일 — Q4 FY26 실적', '2026-02-26',
     '매출 $1.06B · 순이익 $100M · 희석 EPS $0.29(1년 전 $0.12) — 발표 다음 날 주가 −10%', 'q4', 'Everpure 실적 보도자료 (SEC 8-K)'),
    ('red', '2025년 12월 2일 — Q3 FY26 실적', '2025-12-03',
     '매출 $965M · 순이익 $55M · 희석 EPS $0.16(1년 전 $0.19) — 발표 다음 날 주가 −27%', 'q3', 'Pure Storage 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 20, 'nt': 18, 'mean': 151.11, 'median': 155, 'low': 80, 'high': 215, 'sb': 13, 'b': 5, 'h': 1, 's': 0, 'ss': 1}
ANALYST_ASOF = '2026-11-08'


# ── 자동 카드 — 제품·구독 2개(수동 지도, 제품·서비스 축). 원문 대조: Q2 FY27 686.8/499.1(2026-10-24) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "srt:ProductOrServiceAxis",
 "extra": {},
 "members": {"us-gaap:ProductMember": ["제품", "#fe5000"], "us-gaap:ServiceMember": ["구독 서비스", "#ff9a66"]},
 "ignore": []
}
