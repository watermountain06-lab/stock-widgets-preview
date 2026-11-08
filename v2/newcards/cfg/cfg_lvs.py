CIK = '0001300514'
# LVS(라스베이거스 샌즈) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카지노 리조트 — 마카오 5개 단지(Sands China, 지분 약 75.6%·홍콩 상장)과 싱가포르 마리나베이샌즈. 라스베이거스는 2022-02 매각(중단사업).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-23), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 장 마감 뒤 16:0x 동부 → 다음 날 반응), StockAnalysis. 사전 조사 scratchpad pre/LVS.md.
# 엔진 입력(2026-11-03): 차입금 = 합계 태그 $15,444M(금융리스 $147M 포함, DEBT_TOTAL_TAG — 기본은 2025-12 값에 멈춤). 자본 −$344M(PBR 해당 없음). 비지배지분은 장부 $229M(Sands China 소수지분 24% — 시장가는 훨씬 크다).
# 마카오 봉쇄(2020~2022) 기저: 자기 이력은 재개장 뒤 첫 최근 4분기 합 공시일 2024-02-07부터(HISTORY_START), 현금흐름 성장은 2023-12-31 합부터(HISTORY_WINDOW). Q4 2024·2025 EPS는 보도자료 값.
# 비지배지분 시장가 민감도(Fable r1): SCL HKD 11.38 × 약 80.9억 주 × 24.44% ≈ $2.87B → 기본 $23.60·비율 1.62 → 현금흐름 −2·합계 0 “적정”. 장부 유지는 엔진 관례(NWSA와 같음).
# 배당 지급 $723M은 현금흐름표 줄이 Sands China 소수주주 배당을 함께 담는다(Codex r1) — POST로 라벨에 적는다.
# 일회성: 최근 4분기 GAAP 2.44 중 Q4 2025 처분·손상 주당 0.24(약 10%, 비용 쪽) — 빼면 이익이 커져 더 싸 보이므로 표는 같다.
CIK = '0001300514'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, 1, -1), '적정~저평가'
CO = 'Las Vegas Sands'
S_ = 'https://www.sec.gov/Archives/edgar/data/1300514/'
SEC = S_
TENQ = S_ + '000130051426000103/lvs-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000130051426000099/lvs_ex991x09302026.htm', 'q2': S_ + '000130051426000078/lvs_ex991x06302026.htm', 'q1': S_ + '000130051426000039/lvs_ex991x03312026.htm', 'q4': S_ + '000130051426000004/lvs_ex991x12312025.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="lvsFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 연 {pct(HIST[\'growth_5y\'])}, 2023년 말부터)</span>'
Y2 = (0, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('Sands China(마카오) 지분의 약 24%를 다른 주주가 갖고 있는데 내재가치는 비지배지분을 장부가 $0.2B만 뺀다. 시장가(약 $2.9B, 11/3 Sands China 종가)로 빼면 내재가치가 약 $23.6(현재가 ÷ 내재가치 1.62)이 되어 현금흐름 칸이 −2, 합계 0 “적정”이 된다. '
              '자사주 매입이 커서 자본이 마이너스라 PBR은 쓰지 않는다. 마카오 봉쇄(2020~2022) 시기를 빼려고 자기 이력은 2024-02부터, 현금흐름 성장 이력은 2023년 말부터 잡는다. '
              '최근 4분기 이익에 2025년 4분기 자산 처분·손상 비용(주당 $0.24)이 들어 있다. 동종업 점수는 S&P500 경기소비재 기준이다.')
PH = ['WYNN', 'MGM', 'MAR', 'HLT', 'RCL', 'BKNG']
PEER_FILE = 'peer_universe/consumer_discretionary.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '카지노·호텔·여행 6곳 PER 비교 (점수는 S&P500 경기소비재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 경기소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 경기소비재 대비 배수 순위 (v2/peer_universe/consumer_discretionary.json)'
PEER_TIP = ('S&P500 경기소비재(LVS 제외)와 배수 순위를 매긴 값이다.',
            '자동차·주택·외식·호텔·소매가 섞여 있다. 차트에는 카지노·호텔·여행 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문, 외부 매출 — 회사 간 제거 축 없는 값, 지역 축은 함께 붙음) — 1,291 + 685 + 647 + 238 + 231 + 99 + 25 = 3,216.
SEG = [('마리나베이샌즈(싱가포르)', 1291, '#00205b'), ('런더너 마카오', 685, '#7a1f2b'), ('베네시안 마카오', 647, '#c5a35a'), ('플라자·포시즌스 마카오', 238, '#5b7f95'), ('파리지앵 마카오', 231, '#a3a8ad'), ('샌즈 마카오', 99, '#d9c08c'), ('페리·기타', 25, '#c9ccd1')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 리조트별(Q3 2026)'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 마감 뒤 발표(16:0x 동부) → 다음 날.
NEWS_RANGE = '2026.01 ~ 2026.10'
NEWS = [
    ('red', '2026년 10월 21일 장 마감 뒤 — Q3 2026 실적', '2026-10-22',
     '매출 $3.22B(−3.5%) · 순이익 $304M · 희석 EPS $0.48(1년 전 $0.61) · 마리나베이샌즈 EBITDA $590M(1년 전 $743M) — 다음 날 주가 −2.6%', 'q3', 'Las Vegas Sands 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 7월 22일 장 마감 뒤 — Q2 2026 실적', '2026-07-23',
     '매출 $3.15B(−0.7%) · 순이익 $346M · 희석 EPS $0.53(1년 전 $0.66) — 다음 날 주가 +1.7%', 'q2', 'Las Vegas Sands 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 4월 22일 장 마감 뒤 — Q1 2026 실적', '2026-04-23',
     '매출 $3.59B(+25.3%) · 순이익 $567M · 희석 EPS $0.85(1년 전 $0.49) — 다음 날 주가 −8.6%', 'q1', 'Las Vegas Sands 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 1월 28일 장 마감 뒤 — Q4 2025 실적', '2026-01-29',
     '매출 $3.65B(+26.0%) · 순이익 $395M · 희석 EPS $0.58(1년 전 $0.45, 처분·손상 주당 $0.24 포함) · FY2025 EPS $2.35 — 다음 날 주가 −14.0%', 'q4', 'Las Vegas Sands 실적 보도자료 (SEC 8-K)'),
]
POST = [r"h = re.sub(r'배당 지급 \(([^)]*)\)<', r'배당 지급 (\1 · Sands China 소수주주 몫 포함)<', h)"]
ANALYST = {'rating': 'Buy', 'n': 21, 'nt': 14, 'mean': 51.29, 'median': 50, 'low': 37, 'high': 73, 'sb': 11, 'b': 3, 'h': 7, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-08'


# ── 자동 카드 — 부문(축 하나만 붙은 값). 원문 대조: Q3 2026 1,291/685/647/238/231/99/25(2026-11-03) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"lvs:MarinaBaySandsMember": ["마리나베이샌즈(싱가포르)", "#00205b"], "lvs:TheLondonerMacaoMember": ["런더너 마카오", "#7a1f2b"], "lvs:VenetianMacaoMember": ["베네시안 마카오", "#c5a35a"], "lvs:ThePlazaMacaoAndFourSeasonsMacaoMember": ["플라자·포시즌스 마카오", "#5b7f95"], "lvs:ParisianMacaoMember": ["파리지앵 마카오", "#a3a8ad"], "lvs:SandsMacaoMember": ["샌즈 마카오", "#d9c08c"], "lvs:FerryOperationsandOtherMember": ["페리·기타", "#c9ccd1"]},
 "ignore": ["lvs:CorporateAndOtherMember"],
 "free_axes": ["srt:StatementGeographicalAxis"]
}
