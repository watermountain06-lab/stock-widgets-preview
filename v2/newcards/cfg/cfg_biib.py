# BIIB(바이오젠) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 바이오의약품(다발성 경화증·희귀질환·알츠하이머 협업, 바이오시밀러).
# 요약 자료 누락(사용자 결정 2026-10-24): SEC 요약 자료(companyfacts)에서 Q2가 빠져 Q1 2026 10-Q(2026-04-29) 기준 — preflight ALLOW_LAGGED, 기준표 2026-04-29.
# 출처: SEC XBRL, Q1 2026 10-Q, 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 장 전 발표), 8-K(Apellis 인수 계약 3/31·완료 5/14), StockAnalysis. 사전 조사 자료표 scratchpad pre/BIIB.md.
# 엔진 입력(2026-10-24): 영업이익 = 세전이익 − "Other (income) expense, net"(DERIVED_OPINC — 영업이익 줄 없음), 현금 = 제한 현금 포함 태그($3,382.7M = 재무상태표 줄).
# 차입금 $6,288.5M(사채, 1년 안 없음). 4분기 EPS 2025 보도자료 값. 인수 IPR&D(계약금·마일스톤)는 영업이익·GAAP EPS 안(회사 비GAAP도 빼지 않는다).
# Apellis 인수(5/14 완료 — 지급 약 $5.3B, 텀론 $2.0B·리볼버 차입 포함, 6월 말 순차입 약 $6.8B — Q2 보도자료)는 Q1 재무상태표 뒤라 차입금·현금에 없다 — MODEL_NOTE.
CIK = '0000875045'
CUR, YO, QO = '2026-03-31', '2025-03-31', '2025-12-31'
QLABEL, YL, QQL = 'Q1 2026', 'Q1 2025', 'Q4 2025'
L8 = ['Q2 2024', 'Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, 0, -2), '고평가'
CO = 'Biogen'
S_ = 'https://www.sec.gov/Archives/edgar/data/875045/'
SEC = S_
TENQ = S_ + '000087504526000045/biib-20260331.htm'; TENQ_NAME = 'Q1 2026 10-Q'
PR = {'q2': S_ + '000087504526000073/exhibit991-q22026pressrele.htm', 'q1': S_ + '000087504526000042/exhibit991-q12026pressrele.htm',
      'q4': S_ + '000087504526000011/exhibit991-q42025pressrele.htm', 'q3': S_ + '000087504525000047/exhibit991-q32025pressrele.htm'}
LINKS = {'apls': S_ + '000119312526134889/d14986d8k.htm'}
FAIRBAND_TITLE = 'id="biibFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 40)
ACT_REASON = ''
NONOP_WHAT = '장기 시장성 증권·지분 투자'
# 고정 문장.
MODEL_NOTE = ('SEC 요약 자료에서 최근 분기가 빠져 있어, 이 카드의 재무는 요약 자료에 실린 마지막 분기 기준이다 — 최신 10-Q는 나왔지만 숫자는 그보다 한두 분기 이전일 수 있다(자료가 돌아오면 자동으로 바뀐다; 실적 뉴스는 발표 기준). '
              '그래서 5월 14일 끝난 Apellis 인수(지급 약 $5.3B — 현금·증권 약 $3.6B에 은행 차입 약 $2.0B를 보탰다)가 차입금·현금에 들어 있지 않다. 회사가 밝힌 6월 말 순차입은 약 $6.8B(차입 $8.1B − 현금 $1.3B)로 이 카드의 Q1 값보다 훨씬 크고, Apellis 제품 매출·비용도 빠져 있다 — 판정과 현금흐름 값은 인수 전 Q1 재무 기준의 잠정 평가로 읽는다. '
              '분기 이익에는 신약 계약금·마일스톤 같은 인수 IPR&D 비용이 자주 크게 섞인다(회사의 조정 EPS도 빼지 않는다). 다발성 경화증 제품은 특허 만료·경쟁으로 줄고 있다.')
NEXT_CONFIRMED = {}
PH = ['AMGN', 'GILD', 'REGN', 'VRTX', 'BMY', 'ABBV']
PEER_FILE = 'peer_universe/health_care.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '제약·바이오 6곳 PER 비교 (점수는 S&P500 헬스케어 기준)', 'pbr': '제약·바이오 PBR 비교', 'psr': '제약·바이오 PSR 비교',
                'pcr': '제약·바이오 PCR(FCF) 비교', 'evebitda': '제약·바이오 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 헬스케어 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 헬스케어 대비 배수 순위 (v2/peer_universe/health_care.json)'
PEER_TIP = ('S&P500 헬스케어(BIIB 제외)와 배수 순위를 매긴 값이다.',
            '제약·바이오·의료기기·보험·유통이 섞여 있다. 차트에는 제약·바이오 6곳만 보인다.')
# 다음 실적 칸 보정 — 10-Q는 이미 접수됐고, 기다리는 것은 SEC 요약 자료 반영이다(SO·DUK·ED와 같음)
POST = [r'''
h = h.replace('다음 확인 포인트 · Q2 2026 실적 공시.', '다음 확인 포인트 · SEC 요약 자료의 Q2 반영(나오면 카드가 자동으로 바뀐다)과 Q3 2026 실적.', 1)
h = h.replace('실적 7/29 발표, 보고서 반영 대기', '실적 7/29 발표·10-Q 접수, SEC 요약 자료 반영 대기', 1)
h = h.replace('<span class="op-sub">Q2 2026 · 반영 대기</span>', '<span class="op-sub">Q2 2026 · 요약 자료 반영 대기</span>', 1)
h = h.replace('Q2 2026 실적은 발표됐고 카드는 10-Q·10-K 접수 뒤 반영', 'Q2 2026 실적·10-Q는 나왔고 카드는 SEC 요약 자료에 실린 뒤 반영(다음은 Q3, 10월 말~11월 초 예상)', 1)
''']
# 매출(Q1 2026 10-Q 손익계산서) — 제품 1,752.3(다발성 경화증 957.5·희귀질환 557.2·바이오시밀러 182.2·기타 55.4) + 항CD20 419.1 + 알츠하이머 협업 59.5 + 위탁 생산·로열티·기타 246.9 = 2,477.8.
SEG = [('다발성 경화증', 957.5, '#0a3d7a'), ('희귀질환(Spinraza 등)', 557.2, '#3f7fc4'), ('항CD20(Ocrevus 로열티 등)', 419.1, '#7fb0e0'),
       ('위탁 생산·기타', 246.9, '#a9c6e6'), ('바이오시밀러', 182.2, '#5b8fb9'), ('알츠하이머 협업(Leqembi)', 59.5, '#c8d9ee'), ('기타 제품(Zurzuvae)', 55.4, '#dbe6f3')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 제품·수익 종류별'   # 분기는 fill.py가 실제 값으로 붙인다 — 손으로 적으면 분기를 넘길 때 두 번 나온다(2026-10-28)
# IPR&D는 보도자료의 비용 총액($M)으로 쓴다 — 주당 값은 사전 안내 8-K에만 있다(Fable r1). Apellis 조달: Q1 10-Q MD&A 현금·증권 약 $3.6B + 은행 차입 약 $2.0B, 완료 8-K 지급 약 $5.3B.
# 손 뉴스: 실적 4건(Q2 2026 포함 — 재무는 Q1 기준, EPS는 GAAP 희석, 비GAAP·가이던스는 쓰지 않는다) + Apellis 인수 계약. 반응일: 보도자료 장 전 → 같은 날.
# Apellis 계약 3/31 공동 보도자료·웹캐스트(8-K 접수는 장 마감 뒤) → 3/31. 인수 완료(5/14)는 Q2 실적 줄에. 넣지 않은 8-K: IPR&D 비용 사전 안내(2.02항), 임원·주총.
NEWS_RANGE = '2025.10 ~ 2026.07'
NEWS = [
    ('red', '2026년 7월 29일 — Q2 2026 실적(카드 재무는 Q1 기준)', '2026-07-29',
     '매출 $2.74B · 희석 EPS $0.66(1년 전 $4.33) — 인수 IPR&D 비용 $164.0M · Apellis는 5/14 인수 완료 뒤부터 반영', 'q2', 'Biogen 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 4월 29일 — Q1 2026 실적', '2026-04-29',
     '매출 $2.48B · 희석 EPS $2.15(1년 전 $1.64) — 인수 IPR&D 비용 $34.0M(1년 전 $200.7M)', 'q1', 'Biogen 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 3월 31일 — Apellis 인수 계약', '2026-03-31',
     '주당 현금 $41 + 조건부 가치권 최대 $4(지분 가치 약 $5.6B) · 안구·신장 희귀질환 치료제(Syfovre·Empaveli)', 'apls', 'Biogen 공시 (SEC 8-K)'),
    ('green', '2026년 2월 6일 — Q4 2025 실적', '2026-02-06',
     '매출 $2.28B · 희석 EPS −$0.33(1년 전 $1.83) — 인수 IPR&D 비용 $222.4M · 2025년 희석 EPS $8.79(1년 전 $11.18)', 'q4', 'Biogen 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 10월 30일 — Q3 2025 실적', '2025-10-30',
     '매출 $2.53B · 희석 EPS $3.17(1년 전 $2.66)', 'q3', 'Biogen 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 36, 'nt': 26, 'mean': 245.12, 'median': 245, 'low': 175, 'high': 310, 'sb': 20, 'b': 4, 'h': 11, 's': 0, 'ss': 1}
ANALYST_ASOF = '2026-10-24'


# ── 자동 카드 — 제품·수익 종류 7개(수동 지도). 원문 대조: Q1 2026 합 2,477.8(2026-10-24) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "srt:ProductOrServiceAxis",
 "extra": {},
 "members": {"biib:MSProductRevenuesMember": ["다발성 경화증", "#0a3d7a"], "biib:RareDiseaseProductRevenueMember": ["희귀질환(Spinraza 등)", "#3f7fc4"],
             "biib:Revenuesfromanticd20therapeuticprogramsMember": ["항CD20(Ocrevus 로열티 등)", "#7fb0e0"], "us-gaap:ProductAndServiceOtherMember": ["위탁 생산·기타", "#a9c6e6"],
             "biib:BiosimilarsMember": ["바이오시밀러", "#5b8fb9"], "biib:LEQEMBICollaborationMember": ["알츠하이머 협업(Leqembi)", "#c8d9ee"],
             "biib:OtherProductsMember": ["기타 제품(Zurzuvae)", "#dbe6f3"],
             # 2026 Q2 10-Q부터 새 제품군(Apellis 제품 — Q2 $127.8M = Syfovre 97.4 + Empaveli 30.4, Q3 $242.8M). 2025년 비교 분기는 0(2026-10-28)
             "biib:SpecializedImmunologyMember": ["특수 면역(Syfovre·Empaveli)", "#2a6ba8"]},
 "ignore": ["us-gaap:ProductMember", "biib:AlzheimersCollaborationMember", "biib:RoyaltyAttributedToOCREVUSMember", "biib:ContractManufacturingAndOtherRevenueMember", "us-gaap:RoyaltyMember",
            "biib:TECFIDERAMember", "biib:VUMERITYMember", "biib:FumarateMember", "biib:AVONEXMember", "biib:PLEGRIDYMember", "biib:InterferonMember", "biib:TysabriProductMember",
            "biib:FAMPYRAMember", "biib:SPINRAZAMember", "biib:SKYCLARYSMember", "biib:QALSODYMember", "biib:BENEPALIMember", "biib:IMRALDIMember", "biib:FLIXABIMember",
            "biib:BYOOVIZMember", "biib:TOFIDENCEMember", "biib:ZURZUVAEMember", "biib:FUMADERMAndADUHELMMember",
            "biib:SYFOVREMember", "biib:EMPAVELIMember"]   # 특수 면역 제품군의 개별 제품(2026-10-28)
}
