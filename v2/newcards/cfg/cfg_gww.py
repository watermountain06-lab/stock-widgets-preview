# GWW(그레인저) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 175. MRO(유지·보수·운영) 산업용품 유통 — 대면 영업(High-Touch, 북미)·온라인(Endless Assortment: Zoro·MonotaRO).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-08-04 장 마감 뒤 접수), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항), StockAnalysis.
# 엔진 입력(2026-10-23): 차입금 = LongTermDebt $2,408M(1년 안 2 + 장기 2,406, 엔진 값 = 원문), 비지배지분 $382M(MonotaRO 외부 지분 장부가), 이자비용 순이자·매입채무(CONCEPTS_BY_CIK),
# D&A = 현금흐름표 줄(EXCLUDE_TAGS — 부문 주석 합계는 비현금 리스비용 포함), 낡은 금융리스 $205M(2019-01-01) 제외(build_dcf, 안건 E49).
# 2025년 4분기 영국 시장 철수(Cromwell 매각·Zoro U.K. 폐쇄) — Q3 2025에 손상 손실(세금 혜택 없음), 이후 분기는 영국 매출 없음.
CIK = '0000277135'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, -1, -2), '고평가'
CO = 'Grainger'
S_ = 'https://www.sec.gov/Archives/edgar/data/277135/'
SEC = S_
TENQ = S_ + '000027713526000079/gww-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000027713526000076/gww8kex991q22026.htm', 'q1': S_ + '000027713526000056/gww8kex991q12026.htm',
      'q4': S_ + '000027713526000004/gww8kex991q42025.htm', 'q3': S_ + '000027713525000145/gww8kex991q32025.htm'}
LINKS = {'cfo': 'https://www.sec.gov/Archives/edgar/data/277135/000110465926089478/tm2621790d1_8k.htm'}
FAIRBAND_TITLE = 'id="gwwFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 50)
ACT_REASON = ''
NONOP_WHAT = '투자'
# 고정 문장(숫자 없음).
MODEL_NOTE = ('최근 4분기 EPS에는 2025년 3분기 영국 시장 철수 손실(세금 혜택 없음)이 들어 있어 PER이 그만큼 높게 보인다 — 다음 실적에서 그 분기가 빠지면 실적이 제자리여도 PER이 내려간다. 2026년 2분기에는 관세 환급이 원가를 낮췄다. '
              '비지배지분은 일본 상장 자회사 MonotaRO의 외부 주주 몫으로 장부가로 뺀다 — 시가는 장부가보다 클 수 있어 내재가치가 그만큼 후할 수 있다.')
PH = ['FAST', 'MSM', 'WSO', 'CTAS', 'URI', 'PH']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '산업재 유통·서비스 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(GWW 제외)와 배수 순위를 매긴 값이다.',
            '항공·방산·기계·운송·건설이 섞여 있다. 차트에는 산업재 유통·서비스 6곳만 보인다.')
# 매출(Q2 2026 10-Q 부문) — High-Touch Solutions N.A. 3,967 + Endless Assortment 1,054 = 5,021(= 총매출). 1년 전 3,544·929 + 기타(Cromwell) 81 = 4,554.
SEG = [('대면 영업(북미)', 3967.0, '#d6001c'), ('온라인(Zoro·MonotaRO)', 1054.0, '#e8606f')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석 — 조정 EPS·가이던스는 쓰지 않는다).
# 반응일: 보도자료 날짜·콜 기준 — Q2 8-K 2026-08-04T12:03Z(장 전) → 8/4, Q1 보도자료 5/7(콜 5/7, 8-K 접수는 5/7 22:05Z) → 5/7, Q4 2026-02-03T13:09Z → 2/3, Q3 2025-10-31T12:07Z → 10/31.
# 넣지 않은 8-K: 주총(5/1), 정관(12/11). 2/12 −7.1%는 1차 자료 없음.
NEWS_RANGE = '2025.10 ~ 2026.08'
# CFO 사임 8-K 5.02 2026-08-03T12:03Z(장 전) → 8/3. 다음 실적: 회사 IR 일정(이벤트 피드) — 11/4 발표·콜.
NEXT_CONFIRMED = {'quarter_end': '2026-09-30', 'date': '2026-11-04', 'src': '회사 IR 일정 — 11/4 실적 발표·콜'}
NEWS = [
    ('neutral', '2026년 8월 3일 — CFO 사임', '2026-08-03',
     'Deidra Merriwether CFO가 9/4자로 사임 — 회계 책임자(Controller)가 임시 CFO, 후임 탐색', 'cfo', 'Grainger 공시 (SEC 8-K)'),
    ('red', '2026년 8월 4일 — Q2 2026 실적', '2026-08-04',
     '매출 $5.0B(+10.3%) · 희석 EPS $12.01(+20.5%) · 관세(IEEPA) 환급으로 매출원가 $43M 감소 포함(영업이익률 약 0.9%p)', 'q2', 'Grainger 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 5월 7일 — Q1 2026 실적', '2026-05-07',
     '매출 $4.7B(+10.1%) · 희석 EPS $11.65(+18.2%) · 분기 배당 10% 인상', 'q1', 'Grainger 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 3일 — Q4 2025 실적', '2026-02-03',
     '매출 $4.4B(+4.5%) · 희석 EPS $9.44(−2.8%) · 2025년 희석 EPS $35.40(−8.6%, 영국 철수 손실 포함)', 'q4', 'Grainger 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 10월 31일 — Q3 2025 실적 · 영국 시장 철수', '2025-10-31',
     '매출 $4.7B(+6.1%) · 희석 EPS $6.12(−38.0%) — Cromwell 매각 예정 손상 등 영국 철수 손실(세금 혜택 없음) 포함', 'q3', 'Grainger 실적 보도자료 (SEC 8-K)'),
]
# 체크포인트 ② 보정(Fable r1): 1년 전 Q3 2025 영업이익률 11.0%는 영국 철수 손실 포함 — 손실 제외 15.2%(보도자료), 직전 Q2 16.1%는 관세 환급 포함
POST = [r'''
import re as _re
h, _n = _re.subn(r'(1년 전 같은 분기\(Q3 2025 11\.0%\)보다 높은지)\(직전 Q2 2026 16\.1%\)', r'\1(영국 철수 손실 제외 15.2%, 직전 Q2 2026 16.1%는 관세 환급 포함)', h)
assert _n == 1, _n
''']
ANALYST = {'rating': 'Hold', 'n': 19, 'nt': 9, 'mean': 1335.44, 'median': 1355, 'low': 1172, 'high': 1500, 'sb': 3, 'b': 1, 'h': 13, 's': 2, 'ss': 0}
ANALYST_ASOF = '2026-10-23'


# ── 자동 카드 — 부문 2개(수동 지도). 원문 대조: Q2 2026 3,967/1,054(2026-10-23) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"gww:HighTouchSolutionsNAMember": ["대면 영업(북미)", "#d6001c"], "gww:EndlessAssortmentMember": ["온라인(Zoro·MonotaRO)", "#e8606f"]},
 "ignore": []
}
