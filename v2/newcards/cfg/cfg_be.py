# BE(블룸 에너지) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 고체산화물 연료전지 발전 설비(데이터센터·유틸리티·산업), 설치·서비스·전력 판매.
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-22), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 장 마감 뒤 발표 → 다음 거래일 반응), 8-K(Hunterbrook 반박 7/9), StockAnalysis. 사전 조사 scratchpad pre/BE.md.
# 엔진 입력(2026-10-24): 매출 = Revenues(EXCLUDE_TAGS·fetch_financials — 고객 계약 매출 태그는 전력 판매·리스 일부가 빠짐). 차입금 $2,479M(대부분 2030 무이자 전환사채), 현금 $2,487M.
# EPS 이력: Q3 2025 10-Q가 EPS를 −100(단위 오류)으로 달아 fetch_eps_history RESTATED_LATEST에 BE(2026 10-Q 비교 열 −0.10). 이익 확대가 2026년에 몰려 자기 이력 PER은 짧다. 법인세가 거의 0(이월결손금 충당금)이라 GAAP EPS가 정상 세율보다 높다.
# 순이익: 보통주 귀속 태그는 2025년부터, 그 전은 ProfitLoss(비지배 몫 작음 — NetIncomeLoss 태그 없음)
NI_TAGS = ['NetIncomeLossAvailableToCommonStockholdersBasic', 'ProfitLoss']
CIK = '0001664703'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, -1, -2), '고평가'
CO = 'Bloom Energy'
S_ = 'https://www.sec.gov/Archives/edgar/data/1664703/'
SEC = S_
TENQ = S_ + '000162828026066931/be-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000162828026066890/ex991_q326financialresults.htm', 'q2': S_ + '000162828026050150/ex991_q226financialresults.htm',
      'q1': S_ + '000162828026027913/ex991_q126financialresults.htm', 'q4': S_ + '000162828026005798/ex991_q42025financialresul.htm'}
LINKS = {'hb': S_ + '000162828026047734/be-20260709.htm'}
FAIRBAND_TITLE = 'id="beFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (-20, 25)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('이익 확대가 2026년에 몰려 있다 — 그 전에는 적자 해가 많아 자기 이력의 PER 비교는 짧은 기간이고, 과거 5년 이익률 중앙값은 적자 시기가 섞여 낮다. '
              '이월결손금 충당금 때문에 세금비용이 매우 낮아 GAAP EPS가 정상 세율 기준보다 높게 나온다. 판매 후 리스로 생긴 금융 조달 의무(약 $0.2B, 회사 고유 태그)는 차입금에 넣지 않았다. '
              '매출이 소수 고객(특수관계자 포함)에 몰려 있고, 7월 공매도 보고서와 이를 따른 증권 집단소송이 진행 중이다(회사는 반박). '
              '전환사채 교환·증자로 주식 수가 빠르게 늘었다.')
# 적정주가 밴드: 흑자 이력이 2개월뿐이라 1년 PER 구간이 이익이 아주 작던 때의 수백 배 — 밴드를 '해당 없음'으로(Codex r1)
POST = [r'''
import re as _re
h = _re.sub(r'(id="beFairBand" )title="[^"]*" style="font-size:22px;color:var\(--[a-z0-9]+\);">[^<]*<', r'\1title="흑자 이력이 짧아(최근 1년 PER이 이익이 아주 작던 때의 수백 배) PER 기준 적정주가 밴드를 내지 않는다." style="font-size:22px;color:var(--text3);">해당 없음<', h, count=1)
''']
PH = ['GEV', 'VRT', 'ETN', 'CEG', 'VST', 'NEE']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '전력 설비·발전 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(BE 제외)와 배수 순위를 매긴 값이다.',
            '항공·방산·기계·운송·전기 설비가 섞여 있다. 차트에는 전력 설비·발전 6곳만 보인다.')
# 매출(Q3 2026 10-Q, 단일 부문 — 종류별) — 제품 1,073.6 + 설치 84.9 + 서비스 67.6 + 전력 9.8 = 1,235.8.
SEG = [('제품(연료전지)', 1073.6, '#2e8b57'), ('설치', 84.9, '#7fc79f'), ('서비스', 67.6, '#b5e0c5'), ('전력 판매', 9.8, '#d9efe1')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 종류별(Q3 2026)'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석) + 공매도 보고서. 반응일: 장 마감 뒤 발표 → 다음 거래일, Hunterbrook 보고서 7/8 장중 → 7/8.
# 넣지 않은 8-K: CFO 선임(3/26), 주총·정관(5/27), CEO 성과주식(6/17), 증자 설명서(4/27), Oracle 협력·워런트(2025-10-30).
NEWS_RANGE = '2026.02 ~ 2026.10'
NEWS = [
    ('red', '2026년 10월 22일 — Q3 2026 실적', '2026-10-23',
     '매출 $1.24B(1년 전 $0.52B) · 순이익 $250M · 희석 EPS $0.78(1년 전 −$0.10) — 발표 다음 날 주가 −11%', 'q3', 'Bloom Energy 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 7월 28일 — Q2 2026 실적', '2026-07-29',
     '매출 $1.07B(1년 전 $0.40B) · 순이익 $196M · 희석 EPS $0.62(1년 전 −$0.18) · 한 고객 매출 비중 약 73%(10-Q)', 'q2', 'Bloom Energy 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 7월 8일 — Hunterbrook 공매도 보고서', '2026-07-08',
     '회계·공급망(스칸듐) 의혹 제기 — 회사는 다음 날 반박(8-K 7.01), 이를 따른 증권 집단소송 제기', 'hb', 'Bloom Energy 공시 (SEC 8-K·10-Q)'),
    ('green', '2026년 4월 28일 — Q1 2026 실적', '2026-04-29',
     '매출 $751M(1년 전 $326M) · 순이익 $71M · 희석 EPS $0.23(1년 전 −$0.10) — 발표 다음 날 주가 +27%', 'q1', 'Bloom Energy 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 5일 — Q4 2025 실적', '2026-02-06',
     '매출 $778M(1년 전 $572M) · 희석 EPS $0.00(1년 전 $0.38) · 2025년 희석 EPS −$0.37', 'q4', 'Bloom Energy 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 29, 'nt': 21, 'mean': 292.86, 'median': 298, 'low': 176, 'high': 351, 'sb': 10, 'b': 5, 'h': 13, 's': 0, 'ss': 1}
ANALYST_ASOF = '2026-10-24'


# ── 자동 카드 — 종류 4개(수동 지도, 제품·서비스 축). 원문 대조: Q3 2026 1,073.6/84.9/67.6/9.8(2026-10-24) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "srt:ProductOrServiceAxis",
 "extra": {},
 "members": {"us-gaap:ProductMember": ["제품(연료전지)", "#2e8b57"], "be:InstallationMember": ["설치", "#7fc79f"],
             "us-gaap:ServiceMember": ["서비스", "#b5e0c5"], "us-gaap:ElectricityMember": ["전력 판매", "#d9efe1"]},
 "ignore": []
}
