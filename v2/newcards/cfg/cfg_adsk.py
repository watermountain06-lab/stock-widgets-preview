# ADSK(오토데스크) v2 카드 설정 — 자동 카드(AUTO). 회계연도 1월 31일. 카드 순위 180. 설계·엔지니어링 소프트웨어(AutoCAD·Revit·Fusion), 단일 부문.
# 출처: SEC XBRL, Q2 FY27 10-Q(2026-08-28 장 마감 뒤 접수, 분기 끝 7/31), 실적 보도자료(Q3 FY26~Q2 FY27, 8-K 2.02항 — 모두 장 마감 뒤), 8-K(구조조정 1/22, MaintainX 인수 합의 5/28·완료 8/3), StockAnalysis.
# 엔진 입력(2026-10-23): 차입금 = 단기 차입(CP) 994 + 1년 안 사채 499 + 장기 사채 1,985 = $3,478M(DEBT_TOTAL_TAG — 기본은 대체값 $3,494M). 4분기 EPS FY2021·2022·2024·2025·2026은 보도자료 값(Q4_EPS_OVERRIDE).
# MaintainX $3.6B 현금 인수 8/3 완료(분기 끝 7/31 뒤 — 숫자에 없음, CP·사채로 조달).
CIK = '0000769397'
CUR, YO, QO = '2026-07-31', '2025-07-31', '2026-04-30'
QLABEL, YL, QQL = 'Q2 FY27', 'Q2 FY26', 'Q1 FY27'
L8 = ['Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26', 'Q4 FY26', 'Q1 FY27', 'Q2 FY27']
FY_ENDS, FY_LABEL = ('2026-01-31', '2025-01-31'), 'FY2026'
VOTES, VERDICT = (1, 0, -2), '적정~고평가'
CO = 'Autodesk'
S_ = 'https://www.sec.gov/Archives/edgar/data/769397/'
SEC = S_
TENQ = S_ + '000076939726000061/adsk-20260731.htm'; TENQ_NAME = 'Q2 FY27 10-Q'
PR = {'q2': S_ + '000076939726000059/q227pressrelease.htm', 'q1': S_ + '000076939726000041/q127pressrelease.htm',
      'q4': S_ + '000076939726000010/q426pressrelease.htm', 'q3': S_ + '000076939725000126/q326pressrelease.htm'}
LINKS = {'notes': S_ + '000119312526387877/d103766d8k.htm', 'restr': S_ + '000076939726000006/adsk-20260122.htm', 'mx': 'https://www.sec.gov/Archives/edgar/data/769397/000121390026062125/ea029248301ex99-1.htm',
         'mx_close': 'https://www.sec.gov/Archives/edgar/data/769397/000121390026084276/ea0300009-8k_autodesk.htm'}
FAIRBAND_TITLE = 'id="adskFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 70)
ACT_REASON = ''
NONOP_WHAT = '장기 투자'
# 고정 문장(숫자 없음).
MODEL_NOTE = ('구독 소프트웨어라 주식보상·계약 비용 상각 같은 비현금 비용과 연간 이연수익 증가가 더해져 영업현금흐름이 영업이익보다 크다(반기 단위로는 이연수익이 줄어 현금흐름을 깎기도 한다). '
              'PER이 지난 5년 중 낮은 쪽인 데에는 주가 하락뿐 아니라 최근 GAAP 이익 증가도 크게 작용했다. '
              'MaintainX 인수(8/3, 약 $3.5B 지급)는 분기 끝 뒤라 인수 회계는 숫자에 없지만, 조달용 CP는 이미 7월 말 차입금·현금에 들어 있다 — 8/3에 현금·CP·1년 만기 텀론 $1B로 지급했고 9월 사채 $1B로 텀론을 갚았다. 순현금·내재가치는 인수 전 7월 말 재무 기준이라 지금은 순차입 상태다.')
HEALTH_EXTRA = '유동부채의 상당 부분(약 60%)이 이연수익(이미 받은 구독료)이라 현금 지급 의무가 아니다 — 유동비율·부채비율이 실제보다 나쁘게 보인다. 매출원가가 작은 소프트웨어 회사라 매입채무 지급기간·현금창출주기는 의미가 약하다.'   # 고정 문장(Fable r1)
PH = ['CRWD', 'PANW', 'CRM', 'MSFT', 'ORCL', 'PLTR']   # 비교 자료(카드 유니버스 IT)에 값이 있는 종목만
PEER_FILE = None
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '소프트웨어 6곳 PER 비교 (점수는 카드 유니버스 IT 기준)', 'pbr': '소프트웨어 PBR 비교', 'psr': '소프트웨어 PSR 비교',
                'pcr': '소프트웨어 PCR(FCF) 비교', 'evebitda': '소프트웨어 EV/EBITDA 비교'}
PEER_NAME_TITLE = '카드 유니버스 IT 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = '카드 유니버스 IT 종목 대비 배수 순위'
PEER_TIP = ('카드 유니버스 IT 종목(ADSK 제외)과 배수 순위를 매긴 값이다.',
            '반도체·하드웨어·소프트웨어가 섞여 있다. 차트에는 소프트웨어 6곳만 보인다.')
# 매출(Q2 FY27 10-Q 제품군) — 건축·엔지니어링·건설·운영 1,029 + AutoCAD 500 + 제조 385 + 미디어·엔터 92 + 기타 40 = 2,046(= 총매출). 1년 전 878·440·334·80·31.
SEG = [('건축·건설·운영(AECO)', 1029.0, '#0696d7'), ('AutoCAD·LT', 500.0, '#5cbbe6'), ('제조(MFG)', 385.0, '#045e87'), ('미디어·엔터', 92.0, '#9fd8f2'), ('기타', 40.0, '#c9c9c9')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 제품군별'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석 — 조정 EPS·가이던스는 쓰지 않는다; 매출·증가율은 XBRL 분기 값), 구조조정, 인수.
# 반응일: 실적 8-K 2025-11-25T21:03Z·2026-02-26T21:07Z·05-28T20:14Z·08-27T20:05Z = 장 마감 뒤 → 다음 세션. 구조조정 1/22 14:00Z(장 전) → 1/22.
# MaintainX 합의는 Q1 실적과 같은 5/28 장 마감 뒤 → 5/29(실적 줄에 함께), 완료 8-K 8/3 12:38Z(장 전) → 8/3.
# 넣지 않은 8-K: 이사 후보(4/20), 주총(6/17), 신용약정(6/15), CP 프로그램(7/13). 사채 8-K 9/10 20:09Z(장 마감 뒤) → 9/11.
NEWS_RANGE = '2025.11 ~ 2026.09'
NEWS = [
    ('neutral', '2026년 9월 10일 — 사채 $1.0B 발행(텀론 상환)', '2026-09-11',
     '2029년 만기 5.05%·2033년 만기 5.65% 각 $500M — 대금으로 MaintainX 인수에 쓴 1년 만기 텀론 $1.0B를 갚는다', 'notes', 'Autodesk 공시 (SEC 8-K)'),
    ('red', '2026년 8월 27일 — Q2 FY27 실적', '2026-08-28',
     '매출 $2.05B(+16%) · 희석 EPS $2.33(1년 전 $1.46)', 'q2', 'Autodesk 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 8월 3일 — MaintainX 인수 완료', '2026-08-03',
     '설비 유지보수·운영 소프트웨어 MaintainX 인수를 마무리(합의 가격 약 $3.6B, 현금)', 'mx_close', 'Autodesk 공시 (SEC 8-K)'),
    ('red', '2026년 5월 28일 — Q1 FY27 실적 · MaintainX 인수 합의', '2026-05-29',
     '매출 $1.93B(+18%) · 희석 EPS $2.32(1년 전 $0.70) · 같은 날 MaintainX를 현금 약 $3.6B에 인수 합의', 'q1', 'Autodesk 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 26일 — Q4 FY26 실적', '2026-02-27',
     '매출 $1.96B(+19%) · 희석 EPS $1.48(1년 전 $1.40)', 'q4', 'Autodesk 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 1월 22일 — 구조조정(인력 약 7%)', '2026-01-22',
     '영업·마케팅 개편 마지막 단계로 전 세계 인력의 약 7%(약 1,000명) 감축 계획', 'restr', 'Autodesk 공시 (SEC 8-K)'),
    ('green', '2025년 11월 25일 — Q3 FY26 실적', '2025-11-26',
     '매출 $1.85B(+18%) · 희석 EPS $1.60(1년 전 $1.27)', 'q3', 'Autodesk 실적 보도자료 (SEC 8-K)'),
]
# 활동성 문장 보정(Codex r2): 소프트웨어사의 음(−)의 현금창출주기를 '공급업체 돈으로 운영'으로 단정하지 않는다 — 정적 HTML과 JS 템플릿 둘 다
POST = [r'''
import re as _re
_soft = '매출원가가 작은 소프트웨어 회사라 매입채무(대부분 영업비용 채무)가 크게 잡힌 값이어서 공급업체 돈으로 운영한다는 뜻으로 읽기 어렵다. '
h, _n1 = _re.subn(r'<strong style="color:var\(--gold\);">판매 대금을 받고도 ([0-9.]+)일 동안 공급업체 돈으로 운영하는</strong> 구조다\. ', lambda m: '계산상 현금창출주기는 −' + m.group(1) + '일이지만, ' + _soft, h)
_js = '<strong style="color:var(--gold);">판매 대금을 받고도 ${d1(-A.now.ccc)}일 동안 공급업체 돈으로 운영하는</strong> 구조다. '
_n2 = h.count(_js)
h = h.replace(_js, '계산상 현금창출주기는 ${d1(A.now.ccc)}일이지만, ' + _soft)
# 채우기 단계엔 JS 템플릿만, 마지막 단계엔 정적 문장도 있다 — 단계마다 있는 것만 바꾸고, 결과는 빌드 뒤 '공급업체 돈으로 운영하는'이 없는지로 확인
''']
ANALYST = {'rating': 'Buy', 'n': 36, 'nt': 22, 'mean': 305.5, 'median': 300, 'low': 215, 'high': 355, 'sb': 23, 'b': 7, 'h': 6, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-23'


# ── 자동 카드 — 제품군 5개(수동 지도, 제품 축). 원문 대조: Q2 FY27 1,029/500/385/92/40(2026-10-23) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "srt:ProductOrServiceAxis",
 "extra": {},
 "members": {"adsk:ArchitectureEngineeringConstructionAndOperationsMember": ["건축·건설·운영(AECO)", "#0696d7"], "adsk:AutoCADandAutoCADLTFamilyMember": ["AutoCAD·LT", "#5cbbe6"],
             "adsk:ManufacturingMember": ["제조(MFG)", "#045e87"], "adsk:MediaAndEntertainmentMember": ["미디어·엔터", "#9fd8f2"], "adsk:OtherMember": ["기타", "#c9c9c9"]},
 "ignore": ["us-gaap:SubscriptionAndCirculationMember", "us-gaap:ProductAndServiceOtherMember"]
}
