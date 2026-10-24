# VEEV(비바 시스템즈) v2 카드 설정 — 자동 카드(AUTO). 회계연도 1월 31일. 카드 순위 184. 생명과학 산업용 클라우드(CRM·Vault 임상·품질·규제), 단일 부문.
# 출처: SEC XBRL, Q2 FY27 10-Q(2026-08-27 장 마감 뒤 접수, 분기 끝 7/31), 실적 보도자료(Q3 FY26~Q2 FY27, 8-K 2.02항 — 모두 장 마감 뒤), 8-K(자사주 $2B 승인 2026-01-05), StockAnalysis.
# 엔진 입력(2026-10-23): 차입금 없음, 인수 대금 $81.8M(build_dcf ACQ_FIXED), 낡은 금융리스(2020) 제외, 설비투자 PaymentsForSoftware("Long-term assets")·D&A OtherDepreciationAndAmortization(EXTRA_TAGS·CONCEPTS_BY_CIK — 기본 태그가 2020년에 멈춤),
# 4분기 EPS FY2023·2025·2026은 보도자료 값(Q4_EPS_OVERRIDE). 현금·단기투자 약 $7.2B.
CIK = '0001393052'
CUR, YO, QO = '2026-07-31', '2025-07-31', '2026-04-30'
QLABEL, YL, QQL = 'Q2 FY27', 'Q2 FY26', 'Q1 FY27'
L8 = ['Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26', 'Q4 FY26', 'Q1 FY27', 'Q2 FY27']
FY_ENDS, FY_LABEL = ('2026-01-31', '2025-01-31'), 'FY2026'
VOTES, VERDICT = (0, 0, -2), '적정~고평가'
CO = 'Veeva'
S_ = 'https://www.sec.gov/Archives/edgar/data/1393052/'
SEC = S_
TENQ = S_ + '000139305226000036/veev-20260731.htm'; TENQ_NAME = 'Q2 FY27 10-Q'
PR = {'q2': S_ + '000139305226000032/veev-20260731xex991.htm', 'q1': S_ + '000139305226000022/veev-20260430xex991.htm',
      'q4': S_ + '000139305226000007/veev-20260131q426xex991.htm', 'q3': S_ + '000139305225000074/veev-20251031q326xex991.htm'}
LINKS = {'bb': S_ + '000139305226000003/veev20260105ex991sharerepu.htm'}
FAIRBAND_TITLE = 'id="veevFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 70)
ACT_REASON = ''
NONOP_WHAT = '장기 투자'
# 고정 문장(숫자 없음).
MODEL_NOTE = ('영업현금흐름이 영업이익보다 큰 것은 주식보상(비현금 비용)을 더하고 연초에 몰리는 구독료 청구분을 회수하기 때문이다 — 반기 단위로는 이연수익이 줄어 현금흐름을 깎기도 한다. '
              '현금흐름 모델은 세후 GAAP 영업이익에서 출발한다 — 주식보상을 비용으로 보고 선수금 유입은 넣지 않아, 영업현금흐름 기준 FCF보다 출발점이 낮고 성장·이익률도 장기 평균으로 낮춰 내재가치가 현재가보다 크게 낮다. '
              '차입금이 없고 현금·단기투자가 많아 순현금이 크다. 올해 Ostro·Copli 두 작은 회사를 인수했다(10-Q).')
HEALTH_EXTRA = '선수금(이연수익)이 유동부채의 큰 부분이라 현금창출주기·유동비율 해석에 주의 — 고객이 미리 낸 구독료는 현금으로 갚을 빚이 아니다.'   # 고정 문장(Codex r1)
PH = ['CRWD', 'PANW', 'CRM', 'MSFT', 'ORCL', 'PLTR']   # 비교 자료(카드 유니버스 IT)에 값이 있는 종목만
PEER_FILE = None
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '소프트웨어 6곳 PER 비교 (점수는 카드 유니버스 IT 기준)', 'pbr': '소프트웨어 PBR 비교', 'psr': '소프트웨어 PSR 비교',
                'pcr': '소프트웨어 PCR(FCF) 비교', 'evebitda': '소프트웨어 EV/EBITDA 비교'}
PEER_NAME_TITLE = '카드 유니버스 IT 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = '카드 유니버스 IT 종목 대비 배수 순위'
PEER_TIP = ('카드 유니버스 IT 종목(VEEV 제외)과 배수 순위를 매긴 값이다.',
            '반도체·하드웨어·소프트웨어가 섞여 있다. 차트에는 소프트웨어 6곳만 보인다.')
# 매출(Q2 FY27 10-Q) — 구독 766.8 + 전문 서비스 161.2 = 928.0(= 총매출).
SEG = [('구독', 766.764, '#f7931e'), ('전문 서비스', 161.199, '#f9b969')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 구독·서비스'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석 — 조정 EPS·가이던스는 쓰지 않는다), 자사주 승인.
# 반응일: 실적 8-K 2025-11-21T02:04Z·2026-03-05T02:03Z·06-04T00:04Z·08-27T00:06Z = 전날 장 마감 뒤(동부 저녁) → 다음 세션. 자사주 8-K 2026-01-06T02:04Z(1/5 저녁) → 1/6.
# 넣지 않은 8-K: 임원·이사(11/18·12/11·4/20·8/20), 주총(6/18).
NEWS_RANGE = '2025.11 ~ 2026.08'
NEWS = [
    ('green', '2026년 8월 26일 — Q2 FY27 실적', '2026-08-27',
     '매출 $928M(+18%) · GAAP 순이익 $273M(+37%) · 희석 EPS $1.66(1년 전 $1.19)', 'q2', 'Veeva 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 6월 3일 — Q1 FY27 실적', '2026-06-04',
     '매출 $883M(+16%) · GAAP 순이익 $261M · 희석 EPS $1.57(1년 전 $1.37)', 'q1', 'Veeva 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 3월 4일 — Q4 FY26 실적', '2026-03-05',
     '매출 $836M(+16%) · GAAP 순이익 $244M · 희석 EPS $1.45(1년 전 $1.18)', 'q4', 'Veeva 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 1월 5일 — 자사주 매입 $2B 승인', '2026-01-06',
     '이사회가 A주 최대 $2B 매입을 승인(첫 대규모 자사주 프로그램)', 'bb', 'Veeva 발표 (SEC 8-K)'),
    ('red', '2025년 11월 20일 — Q3 FY26 실적', '2025-11-21',
     '매출 $811M(+16%) · GAAP 순이익 $236M · 희석 EPS $1.40(1년 전 $1.13)', 'q3', 'Veeva 실적 보도자료 (SEC 8-K)'),
]
# 활동성 문장 보정(Codex r2): 선수금(구독료 선납)이 빠진 산식이라 현금창출주기를 '직접 현금으로 메워야 하는 기간'으로 단정하지 않는다 — 정적 HTML과 JS 템플릿 둘 다
POST = [r'''
import re as _re
_tail = '일은 선수금 효과를 뺀 산식상 기간이다 — 고객이 구독료를 미리 내므로 실제 자금 공백을 뜻하지 않는다. '
h = _re.sub(r'<strong style="color:var\(--gold\);">([0-9.]+)일은 회사가 직접 현금으로 메워야</strong> 하는 기간이다\. ', lambda m: m.group(1) + _tail, h)
_js = '<strong style="color:var(--gold);">${d1(A.now.ccc)}일은 회사가 직접 현금으로 메워야</strong> 하는 기간이다. '
h = h.replace(_js, '${d1(A.now.ccc)}' + _tail)
''']
ANALYST = {'rating': 'Buy', 'n': 29, 'nt': 21, 'mean': 295.71, 'median': 300, 'low': 180, 'high': 360, 'sb': 13, 'b': 7, 'h': 8, 's': 0, 'ss': 1}
ANALYST_ASOF = '2026-10-23'


# ── 자동 카드 — 구독·서비스 2개(수동 지도, 제품 축). 원문 대조: Q2 FY27 766.8/161.2(2026-10-23) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "srt:ProductOrServiceAxis",
 "extra": {},
 "members": {"us-gaap:SubscriptionAndCirculationMember": ["구독", "#f7931e"], "us-gaap:TechnologyServiceMember": ["전문 서비스", "#f9b969"]},
 "ignore": ["veev:SubscriptionServicesVeevaCommercialCloudMember", "veev:SubscriptionServicesVeevaResearchAndDevelopmentAndQualitySolutionsMember", "veev:ProfessionalServicesVeevaCommercialCloudMember", "veev:ProfessionalServicesVeevaResearchAndDevelopmentAndQualitySolutionsMember"]
}
