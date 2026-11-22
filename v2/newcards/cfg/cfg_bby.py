BUILD = {}   # 2026-11-16 정식 전환 — 30% 규칙(2026-11-07)으로 다시 재니 일회성 순액 약 12%(아래). 11-03 미완성(일회성 처리 대기)에서 풀림
# BBY(베스트바이) v2 카드 설정 — 자동 카드(AUTO), 정식 판정. 회계연도 1월 말에 가까운 토요일(52/53주 — FY24 53주). 가전·전자제품 소매, 부문은 국내(미국)·해외(캐나다).
# 출처: SEC XBRL, Q2 FY27 10-Q(2026-09-04), 실적 보도자료(Q3 FY26~Q2 FY27, 8-K 2.02항 — 장 전 07시 동부 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/BBY.md.
# 엔진 입력(2026-11-03): 차입금 = 날짜별 DebtAndCapitalLeaseObligations 우선, 그 전 LongTermDebt($1,169M, 금융리스 포함 — DEBT_TOTAL_TAG). 낡은 단기투자(2021)·비지배지분(2016) 제외(EV_TAGS_BY_CIK). 운용리스 $2,964M.
# 일회성(E54, 2026-11-07 30% 규칙 — 11-16 재측정, 회사 조정표 세후 주당): 최근 4분기 GAAP 희석 EPS 6.01(0.66 + 2.56 + 1.31 + 1.48) 대 조정 6.76(1.40 + 2.61 + 1.28 + 1.47).
#   비용: Q3 FY26 영업권·무형 손상 0.73·장기 자산 손상 0.07, Q4 손상 0.02·장기 자산 0.01·자회사 처분 0.01·투자 손실 0.03 → 0.87(약 14.5%). 이익: 구조조정 환입 0.06·0.03·0.04·0.02 → 0.15.
#   순액 0.72(약 12%) → 정식(무형자산 상각은 반복). 관세 환급 $34M(Q2)은 회사가 조정하지 않아 회사 분류를 따른다.
# (옛 기록 — 아래 세 줄은 11-03 미완성 때 판단) 미완성 사유(E54): Q3 FY26 Best Buy Health 손상(세전 $192M, 주당 $0.80, 최근 4분기 EPS 6.01의 13%)을 되돌리면 자기 이력 25.8 → 30.9로 −1표가 0이 되어 판정이 적정~고평가 → 적정으로 바뀐다(scratchpad bby_e54).
# 2026-11-03 사용자 결정에 따라 미완성 카드. 이 손상은 Q3 FY27 실적(11월 하순 예상)이 나오면 최근 4분기에서 빠진다. Q4 FY24·FY25 EPS는 보도자료 값. 관세 환급 $34M(Q2)은 회사도 조정하지 않았다.
# 민감도(Codex r1): 환급까지 빼면 자기 이력 29.5~30.1(세율·현금 처리에 따라)로 다시 −1 문턱 근처 — 일회성 범위에 따라 판정이 갈려 미완성이 맞다.
# Fable r1: 5년 창 안 Q4 FY25 손상(세전 $477M)까지 이력에서 되돌리면 자기 이력 24.1(−1 유지) — 최근 4분기만 되돌리는 시험(앞 카드들 방식)에서만 뒤집힌다. 현금흐름은 세율 맞춰도 $75.26·1.28(−1).
CIK = '0000764478'
CUR, YO, QO = '2026-08-01', '2025-08-02', '2026-05-02'
QLABEL, YL, QQL = 'Q2 FY27', 'Q2 FY26', 'Q1 FY27'
L8 = ['Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26', 'Q4 FY26', 'Q1 FY27', 'Q2 FY27']
FY_ENDS, FY_LABEL = ('2026-01-31', '2025-02-01'), 'FY2026'
VOTES, VERDICT = (-1, 1, -1), '적정~고평가'
CO = 'Best Buy'
S_ = 'https://www.sec.gov/Archives/edgar/data/764478/'
SEC = S_
TENQ = S_ + '000076447826000042/bby-20260801.htm'; TENQ_NAME = 'Q2 FY27 10-Q'
PR = {'q2': S_ + '000076447826000037/bby-fy27q2xexx99.htm', 'q1': S_ + '000076447826000018/bby-fy27q1xexx991.htm', 'q4': S_ + '000076447826000005/bby-fy26q4xexx99.htm', 'q3': S_ + '000076447825000050/bby-fy26q3xexx99.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="bbyFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {pct(HIST[\'margin_now\'])})</span>'
Y2 = (0, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('최근 4분기 GAAP 희석 EPS $6.01은 회사 조정 EPS $6.76보다 조금 낮다. 차이는 대부분 2025년 3분기 Best Buy Health 영업권·무형자산 손상(세후 주당 $0.73)과 장기 자산 손상 등이고, 반대로 구조조정 충당금 환입이 분기마다 조금씩 있다. '
              '무형자산 상각을 빼고 세면 일회성 비용이 GAAP EPS의 약 15%, 환입을 상계한 순액이 약 12%라 GAAP 숫자를 그대로 쓴다. 이 손상은 다음 실적(Q3 FY27, 11월 하순 예상)에서 최근 4분기 밖으로 빠지는데, 주가와 다른 이익이 그대로라면 손상 분기(EPS $0.66)가 빠지는 것은 PER을 낮추는 쪽으로 작용한다. '
              '2분기 관세 환급 $34M은 회사도 조정하지 않아 그대로 둔다. 동종업 점수는 S&P500 경기소비재 기준이다.')
PH = ['HD', 'LOW', 'TJX', 'ROST', 'WSM', 'TSCO']
PEER_FILE = 'peer_universe/consumer_discretionary.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '소매 6곳 PER 비교 (점수는 S&P500 경기소비재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 경기소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 경기소비재 대비 배수 순위 (v2/peer_universe/consumer_discretionary.json)'
PEER_TIP = ('S&P500 경기소비재(BBY 제외)와 배수 순위를 매긴 값이다.',
            '자동차·주택·외식·호텔·소매가 섞여 있다. 차트에는 소매 6곳만 보인다.')
# 매출(Q2 FY27 10-Q 부문) — 국내 9,070 + 해외 709 = 9,779.
SEG = [('국내(미국)', 9070, '#0046be'), ('해외(캐나다)', 709, '#ffe000')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별(Q2 FY27)'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 전 발표(07시 동부) → 같은 날.
NEWS_RANGE = '2025.11 ~ 2026.08'
NEWS = [
    ('red', '2026년 8월 27일 장 전 — Q2 FY27 실적', '2026-08-27',
     '매출 $9.78B(+3.6%) · 순이익 $315M · 희석 EPS $1.48(1년 전 $0.87) · 조정 EPS $1.47 · 연간 전망 상향 — 당일 주가 −4.4%', 'q2', 'Best Buy 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 5월 28일 장 전 — Q1 FY27 실적', '2026-05-28',
     '매출 $8.94B(+1.9%) · 순이익 $276M · 희석 EPS $1.31(1년 전 $0.95) · 조정 EPS $1.28 — 당일 주가 +15.8%', 'q1', 'Best Buy 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 3월 3일 장 전 — Q4 FY26 실적', '2026-03-03',
     '매출 $13.81B(−1.0%) · 순이익 $541M · 희석 EPS $2.56(1년 전 $0.54, 손상) · 조정 EPS $2.61 — 당일 주가 +7.1%', 'q4', 'Best Buy 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 11월 25일 장 전 — Q3 FY26 실적', '2025-11-25',
     '매출 $9.67B(+2.4%) · 순이익 $140M · 희석 EPS $0.66(Best Buy Health 손상 포함, 1년 전 $1.26) · 조정 EPS $1.40 — 당일 주가 +5.3%', 'q3', 'Best Buy 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 26, 'nt': 17, 'mean': 91.24, 'median': 95, 'low': 71, 'high': 110, 'sb': 4, 'b': 0, 'h': 20, 's': 1, 'ss': 1}
ANALYST_ASOF = '2026-11-21'


# ── 자동 카드 — 부문(축 하나만 붙은 값). 원문 대조: Q2 FY27 9,070/709(2026-11-03) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerIncludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"bby:DomesticSegmentMember": ["국내(미국)", "#0046be"], "bby:InternationalSegmentMember": ["해외(캐나다)", "#ffe000"]},
 "ignore": []
}
