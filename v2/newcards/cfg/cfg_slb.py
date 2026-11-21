CIK = '0000087347'
BUILD = {'company_tags': [('slb:ShortTermBorrowingsAndLongTermDebtCurrent', 'LongTermDebtCurrent')]}   # 단기차입·1년 안 장기차입 $1,653M(9월 말)은 회사 고유 태그뿐 — 없으면 차입금이 장기 $11,147M만 잡혔다(Codex r1, 2026-11-18)
# SLB(옛 슐럼버거) v2 카드 설정 — 자동 카드(AUTO), 정식 판정. 회계연도 12월 말. 유전 서비스 — 디지털, 저류층 성능, 시추(Well Construction), 생산 시스템(2025년 7월 ChampionX 인수 포함).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-28 접수, 카드 기준일 11-17 종가), 실적 보도자료(8-K 2.02항 — 모두 장 전 06~07시 동부 → 그날), Kelvion 인수 계약(8-K 7.01항 2026-08-31 장 전 → 그날).
# 엔진 입력(2026-11-18): 영업이익 = 세전이익 + 이자비용(DERIVED_OPINC — OperatingIncomeLoss 태그 2024-03에 멈춤). "Interest & other income"(분기 약 $70M)은 태그가 없어 영업에 남는다.
#   현금은 "Cash and short-term investments" $3,551M(현금 2,621 + 단기투자 930). Q4 2025 EPS는 보도자료 0.55(역산 0.53, Q4_EPS_OVERRIDE).
# 일회성(E54 30% 규칙, 2026-11-18): 최근 4분기 GAAP 희석 EPS 2.06(0.55 + 0.50 + 0.52 + 0.49) 대 회사 조정 2.49(0.78 + 0.52 + 0.55 + 0.64).
#   회사 조정표 세후 순이익 기준($M): Q4 2025 영업권 손상 169·인력 감축 109·재고 공정가치 상각 77·통합 48·구조조정 44·이연법인세자산 평가충당금 환입 −92 = 355, Q1 통합 31, Q2 통합 47, Q3 연금 정산 187·통합 40 = 227.
#   순액 $660M / GAAP 순이익 $3,097M = 약 21%, 비용만 $752M = 약 24% → 정식(회사 분류를 따른다 — 통합 비용은 매 분기 나오지만 ChampionX 인수에 딸린 것).
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, -1), '적정~고평가'
CO = 'SLB'
S_ = 'https://www.sec.gov/Archives/edgar/data/87347/'
SEC = S_
TENQ = S_ + '000119312526435577/slb-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000119312526429435/d151271dex99.htm', 'q2': S_ + '000119312526315068/d122193dex99.htm',
      'q1': S_ + '000119312526174940/d111579dex99.htm', 'q4': S_ + '000119312526020133/d59412dex99.htm',
      'kel': S_ + '000119312526375358/d106278d8k.htm', 'me': S_ + '000119312526101131/d17166d8k.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="slbFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (-10, 30)
ACT_REASON = ''
BB_TAGS = ['PaymentsForRepurchaseOfEquity']   # 자사주 매입은 이 태그로만(9개월 $1,755M) — PaymentsForRepurchaseOfCommonStock 없음(Fable r1)
NONOP_WHAT = '투자'
MODEL_NOTE = ('최근 4분기 GAAP 희석 EPS $2.06은 회사 조정 EPS $2.49보다 낮다. 차이는 2025년 4분기 영업권 손상·인력 감축·ChampionX 인수 재고 공정가치 상각, 매 분기 나오는 인수 통합 비용, 2026년 3분기 연금 정산 손실($187M) 등이고, 반대로 이연법인세자산 평가충당금 환입($92M) 이익이 있다. '
              '회사 조정표 세후로 순액이 GAAP 순이익의 약 21%(비용만 약 24%)라 GAAP 숫자를 그대로 쓴다. '
              '손익계산서에 영업이익 줄이 없어 카드는 세전이익에 이자비용을 더해 영업이익으로 쓴다 — 이자수익과 지분법 이익("Interest & other income", 분기 $43~76M)·본사 비용·일회성이 함께 들어가 회사의 부문 영업이익과 산정 범위가 다르다. 최근 4분기 영업이익률에는 위 일회성 비용(세전 약 $0.9B, 약 2.5%포인트)이 들어 있어, 이 이익률과 짧은 기간 성장률을 함께 쓰는 낙관 시나리오가 오히려 가장 낮게 나온다. '
              '카드의 FCF는 영업현금흐름에서 설비투자만 뺀 값이라, APS(자산 성과 연계) 투자와 탐사자료 자본화까지 빼는 회사 FCF보다 크다(3분기 카드 $1.03B 대 회사 $828M, 최근 4분기 약 $4.6B 대 약 $3.8B). '
              '2025년 7월 ChampionX를 주식으로 인수해 생산 시스템 매출이 커지고 주식 수가 늘었다. 2026년 8월 31일 열관리 회사 Kelvion을 약 $3.4B 현금에 사고 차입 약 $0.7B를 떠안기로 했다(합계 약 $4.1B, 2027년 상반기 종결 예정) — 아직 숫자에는 없고, 현금 대가 $3.4B(9월 말 현금·단기투자 $3.55B와 비슷)와 떠안는 차입 $0.7B를 합치면 단순 계산으로 순차입이 약 $4.1B 늘어난다(피인수회사 현금·종결 조정 제외). '
              '2026년 3월 중동 분쟁으로 몇몇 나라에서 작업 철수를 시작했고, 회사는 그 영향을 1분기 주당 6~9센트로 추정했다(1분기 조정 EPS는 1년 전보다 28% 줄었다). 회사는 2026년 주주환원 $4B 이상을 약속했고 9개월 동안 자사주 3,400만 주를 $1.76B에 샀다.')
PH = ['HAL', 'BKR', 'XOM', 'CVX', 'COP', 'EOG']
PEER_FILE = 'peer_universe/energy.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '에너지 6곳 PER 비교 (점수는 S&P500 에너지 기준)', 'pbr': '에너지 PBR 비교', 'psr': '에너지 PSR 비교',
                'pcr': '에너지 PCR(FCF) 비교', 'evebitda': '에너지 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 에너지 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 에너지 대비 배수 순위 (v2/peer_universe/energy.json)'
PEER_TIP = ('S&P500 에너지(SLB 제외)와 배수 순위를 매긴 값이다.',
            '유전 서비스·통합 석유·탐사생산·정유·파이프라인이 섞여 있다. 차트에는 유전 서비스 2곳과 석유 생산 4곳이 보인다.')
# 매출(Q3 2026 보도자료 부문): 디지털 693 + 저류층 성능 1,634 + 시추 2,888 + 생산 시스템 4,000 + 기타 544 = 9,759, 부문 간 −310 → 9,449.
SEG = [('생산 시스템', 4000, '#0014dc'), ('시추(Well Construction)', 2888, '#3a5bff'), ('저류층 성능', 1634, '#00b4d8'), ('디지털', 693, '#7ad7f0'), ('기타', 544, '#c5d0ff')]
SEG_ADJ = -310
SEG_TITLE = '매출 구성 — 사업 부문별'
# 손 뉴스: 실적 4건 + Kelvion 인수 + 중동 운영 업데이트. 반응일: 모두 장 전 → 그날.
NEWS_RANGE = '2026.01 ~ 2026.10'
NEWS = [
    ('neutral', '2026년 10월 23일 장 전 — Q3 2026 실적', '2026-10-23',
     '매출 $9.45B(+6%) · GAAP 희석 EPS $0.49(연금 정산 $187M 포함) · 조정 EPS $0.64 · FCF $828M — 그날 주가 +7.1%', 'q3', 'SLB 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 8월 31일 장 전 — Kelvion 인수 계약', '2026-08-31',
     '열관리·열교환 기술 회사 Kelvion을 약 $3.4B 현금에 인수하고 차입 약 $0.7B를 떠안기로 — 그날 주가 +4.8%', 'kel', 'SLB 8-K'),
    ('green', '2026년 7월 24일 장 전 — Q2 2026 실적', '2026-07-24',
     '매출 $8.97B(+5%) · GAAP 희석 EPS $0.52 · 조정 EPS $0.55 · FCF $716M — 그날 주가 +11.0%', 'q2', 'SLB 보도자료 (SEC 8-K)'),
    ('red', '2026년 4월 24일 장 전 — Q1 2026 실적', '2026-04-24',
     '매출 $8.72B(+3%) · GAAP 희석 EPS $0.50(1년 전 $0.58) · 조정 EPS $0.52(−28%) — 그날 주가 +2.6%', 'q1', 'SLB 보도자료 (SEC 8-K)'),
    ('red', '2026년 3월 11일 장 전 — 중동 운영 업데이트', '2026-03-11',
     '중동 분쟁으로 지역 이동을 멈추고 일부 나라에서 작업 철수 시작 — 그날 주가 +0.1%, 다음 날 −7.5%', 'me', 'SLB 8-K'),
    ('neutral', '2026년 1월 23일 장 전 — 2025년 연간 실적', '2026-01-23',
     '4분기 매출 $9.75B · GAAP 희석 EPS $0.55(영업권 손상 등) · 조정 EPS $0.78 · 분기 배당 $0.295로 +3.5% · 2026년 주주환원 $4B 이상 약속 — 그날 주가 −0.3%', 'q4', 'SLB 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 30, 'nt': 19, 'mean': 62.05, 'median': 62, 'low': 48, 'high': 71, 'sb': 19, 'b': 7, 'h': 3, 's': 1, 'ss': 0}
ANALYST_ASOF = '2026-11-18'

AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"slb:ProductionSystemsMember": ["생산 시스템", "#0014dc"], "slb:WellConstructionMember": ["시추(Well Construction)", "#3a5bff"], "slb:ReservoirPerformanceMember": ["저류층 성능", "#00b4d8"], "slb:DigitalIntegrationMember": ["디지털", "#7ad7f0"], "us-gaap:AllOtherSegmentsMember": ["기타", "#c5d0ff"]},
 "ignore": ["slb:EliminationsOtherMember"]
}
