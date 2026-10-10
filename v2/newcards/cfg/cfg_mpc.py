# MPC(마라톤 페트롤리엄) v2 카드 설정 — fill.py MPC. 회계연도 12월 31일. 시총 100위(S&P500 현재 시총 순, 2026-10-02 StockAnalysis 기준, 루트 카드 없음).
# 출처: SEC XBRL(+ 2분기 10-Q 인라인 XBRL 보충), Q2 2026 10-Q(2026-08-04), 실적 보도자료(Q3 2025~Q2 2026, SEC 접수 모두 오전 6시 33~49분 = 장 시작 전 → 당일 반응),
# 8-K(회장 선임 2025-10-29, CFO 선임 12/18, 신용 약정 4/7), StockAnalysis.
# 엔진 수정(2026-10-02): 기본 차입금 태그(LongTermDebtCurrent·Noncurrent)가 2012-03에 멈춰 DEBT_TOTAL_TAG(DebtCurrent + LongTermDebtAndCapitalLeaseObligations),
# 재무 데이터 장기차입금 별칭(overlay_feed ALIAS). 단기투자 태그는 2024-12에 멈췄지만 마지막 값이 0이고 재무상태표에 줄이 없어 그대로 둔다.
# 연결 재무에 MPLX(상장 자회사)가 들어 있어 비지배지분 $6.6B가 EV에 더해진다.
BUILD = {'overlay': True}
CIK = '0001510295'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
RELEASE = {'rev': 51994, 'op': 7322, 'ni': 5138, 'ocf': 10327, 'cap': 1186}   # 10-Q, 순이익은 MPC 귀속, 현금흐름은 상반기 − 1분기
VOTES, VERDICT = (-1, 0, -2), '고평가'
CO = 'Marathon Petroleum'
S_ = 'https://www.sec.gov/Archives/edgar/data/1510295/'
SEC = S_
PR = {'q2': S_ + '000151029526000060/mpcq22026earningsrelease.htm', 'q1': S_ + '000151029526000039/mpcq12026earningsrelease.htm',
      'q4': S_ + '000151029526000003/mpcq42025earningsrelease.htm', 'q3': S_ + '000151029525000059/mpcq32025earningsrelease.htm'}
PR_CUR = 'q2'
TENQ = S_ + '000151029526000061/mpc-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
LINKS = {'credit': S_ + '000151029526000029/mpc-20260407.htm', 'cfo': S_ + '000151029525000070/mpc-20251212.htm', 'chair': S_ + '000151029525000065/mpc-20251029.htm'}
FAIRBAND_TITLE = 'id="mpcFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다. 최근 4분기 EPS에는 2분기 $17.73이 들어 있고 PER 구간은 그 전 이익 수준에서 잰 값이라 범위가 높게 나온다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
OPM_RANGE, Y2 = (-5, 20), (0, 20)
FCF_SUB = '영업현금흐름 − 설비투자'
CAPEX_SUB = '유형자산 취득(현금흐름표)'
STAT3 = ('정제·판매 마진 (Q2 2026)', '$36.33/배럴', '1년 전 $17.58 · 원유 가동률 94%')
NEXT = ('11월 초 예상', '일정 · Q3 2026 (회사 미확정)'); NEXT_OP = ('11월 초', 'Q3 2026 예상')
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
HEALTH_NOTE = ('6월 말 현금은 $7.8B(MPLX 현금 $1.0B 포함), 차입금은 $32.8B(유동 $2.1B + 장기 $30.7B, MPLX 포함 연결)다. '
               'MPLX 지분 중 외부 투자자 몫인 비지배지분이 $6.6B다. 4월에 5년 만기 회전 신용 $5B를 새로 맺었고 6월 말 인출액은 없다.')
ACT_REASON = ''
YOY_EXTRA = '매출 +54% · 정제·판매 부문 조정 EBITDA $6.7B(1년 전 $1.9B) · 정제·판매 마진 배럴당 $36.33(1년 전 $17.58) · '
SEG = [('정제·판매', 49299, '#b22222'), ('미드스트림(MPLX)', 1455, '#e07b39'), ('재생 디젤', 1240, '#6aa84f')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별(외부 고객)'
SEG_NOTE = ('1년 전보다 정제·판매 +54.9%, 미드스트림 +8.6%, 재생 디젤 +96.5% · '
            '출처: <a href="{TENQ}" target="_blank" rel="noopener">Q2 2026 10-Q (SEC) →</a>')
CAPITAL = [('자사주 매입 (2026 상반기)', '$3.3B'),
           ('남은 자사주 매입 승인 (6월 말)', '$6.1B'),
           ('분기 배당 (2026)', '$1.00', '+10%')]
CHECK_WHEN = '2026년 11월 초 (예상) · Q3 2026'
CHECK = ['정제·판매 마진(2분기 배럴당 $36.33)과 크랙 스프레드',
         '미국·이란 분쟁과 시장 반응(회사가 위험 요인으로 적음)',
         'MPLX 분배금 증가(회사 예상 2026·2027년 연 12.5%)',
         '자사주 매입 속도(상반기 $3.3B)']
NONOP_WHAT = '투자'
PH = ['VLO', 'PSX', 'XOM', 'CVX', 'COP', 'OXY']
PEER_FILE = 'peer_universe/energy.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '정유·석유 6곳 PER 비교 (점수는 S&P500 에너지 기준)', 'pbr': '정유·석유 PBR 비교', 'psr': '정유·석유 PSR 비교',
                'pcr': '정유·석유 PCR(FCF) 비교', 'evebitda': '정유·석유 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 에너지 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 에너지 대비 배수 순위 (v2/peer_universe/energy.json)'
FUND_ASOF_NOTE = 'Q2 2026 10-Q (2026-08-04 공시, 인라인 XBRL 보충)'
PREMISE = ('주가가 1년 새 {CH_TXT} 올라 PSR·PBR이 5년 중 가장 비싼 쪽, PER {SM[\'PER\'][\'current\']:.1f}배도 5년 중앙값 {SM[\'PER\'][\'median\']:.1f}배보다 높아 자기 이력 {selfsc:.1f}점(비싸다)이다. '
           'S&P500 에너지 안에서는 PSR·PCR이 싼 쪽, PBR은 비싼 쪽이라 {peersc:.1f}점(중간)이다. '
           '<strong>현금흐름 내재가치(기본 ${DCF[\'base\']:.2f})는 현재가보다 크게 낮다</strong>.')
RISK = ('세 칸이 {VOTES_TXT}, 합계 {TOTAL_TXT} “{VERDICT}”다. 현재가를 정당화하려면 5년 매출 성장이 연 {pct(DCF[\'requiredGrowth\'])}여야 한다(실제 5년 연 {pct(HIST[\'growth_5y\'])}). '
        '최근 4분기 이익에는 정제·판매 마진이 1년 전의 두 배였던 2분기가 들어 있다.')
FUND_TIP = ('차입금(MPLX 포함 연결)이 총자산의 34.8%다. 매출·영업이익 CAGR(연간 결산 2022→2025)이 음수인 것은 매출이 컸던 2022년 결산과 비교해서다. '
            '2분기 영업현금흐름에는 운전자본 유입이 들어 있다(상반기 유동부채 등 +$7.6B, 매출채권 −$5.4B). '
            '활동성은 영업순환주기 기준이다.')
SELF_TIP = 'PSR·PBR은 5년 중 가장 비싼 쪽이다. PER {SM[\'PER\'][\'current\']:.1f}배는 2분기 큰 이익이 들어간 최근 4분기 EPS로 잰 값이다.'
PEER_TIP = ('S&P500 에너지(MPC 제외)와 배수 순위를 매긴 값이다.',
            '통합 석유사·탐사생산·정유·장비·가스관 회사가 섞여 있다. 정유사는 매출이 커 PSR이 낮게 나온다. 차트에는 정유·석유 6곳만 보인다.')
STORIES = ['5년 성장률의 절반(연 {pct(HIST[\'growth_5y\'] / 2)})로 시작해 식고, 영업이익률이 최근 4분기 {pct(HIST[\'margin_now\'])}에서 5년에 걸쳐 5년 중앙값 {pct(HIST[\'margin_5y\'])}로 간다.',
           '5년 성장률(연 {pct(HIST[\'growth_5y\'])})로 시작해 식고, 영업이익률이 최근 4분기 {pct(HIST[\'margin_now\'])}에서 5년에 걸쳐 최근 2년 중앙값 {pct(HIST[\'margin_2y\'])}로 간다.',
           '3년 성장률(최근 4분기 합 기준, 연 {pct(HIST[\'growth_3y\'])})로 시작해 식고, 최근 4분기 영업이익률 {pct(HIST[\'margin_now\'])}가 이어진다.']
DCF_NOTE = ('세 시나리오 모두 현재가보다 낮다. 값을 가르는 것은 성장보다 영업이익률이다(지난 시점의 시나리오 선도 같은 이유로 “낙관”이 가장 낮게 그려지는 때가 있다). 최근 4분기 {pct(HIST[\'margin_now\'])}가 이어지는 “낙관”(${DCF[\'high\']:.0f})이 가장 높고, '
            '5년 중앙값 {pct(HIST[\'margin_5y\'])}로 가는 “보수”(${DCF[\'low\']:.0f})가 최근 2년 중앙값 {pct(HIST[\'margin_2y\'])}로 가는 “기본”(${DCF[\'base\']:.0f})보다 높다. '
            '5년 중앙값에는 매출이 컸던 2022년 무렵이 들어 있다. 사업 가치에서 차입금($32.8B)과 MPLX 비지배지분을 빼고 현금을 더한다(운용리스는 영업이익이 임차료를 이미 뺐으므로 빼지 않는다).')
NEWS_RANGE = '2025.10 ~ 2026.09'
NEWS = [
    ('green', '2026년 8월 4일 장 시작 전 — Q2 2026 실적', '2026-08-04',
     '순이익 $5.1B(1년 전 $1.2B) · EPS $17.73 · 정제·판매 마진 배럴당 $36.33 · 2분기 주주환원 $2.8B · 당일 주가 +1.8%', 'q2', 'MPC 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 5월 5일 장 시작 전 — Q1 2026 실적', '2026-05-05',
     '순이익 $511M · EPS $1.73(조정 $1.65) · 정기 보수 일정 앞당김 · 자사주 매입 $5B 추가 승인 · 당일 주가 +3.2%', 'q1', 'MPC 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 7일 — 회전 신용 $5B 약정', None,
     '5년 만기, JPMorgan 등 대주단', 'credit', 'MPC 공시 (SEC 8-K)'),
    ('green', '2026년 2월 3일 장 시작 전 — Q4 2025 실적', '2026-02-03',
     'EPS $5.12(조정 $4.07) · 2025년 EPS $13.22 · 당일 주가 +6.0%', 'q4', 'MPC 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 12월 18일 — 새 CFO 선임', None,
     'Maria Khoury, 2026년 1월 19일부터', 'cfo', 'MPC 공시 (SEC 8-K)'),
    ('red', '2025년 11월 4일 장 시작 전 — Q3 2025 실적', '2025-11-04',
     'EPS $4.51(조정 $3.01) · 당일 주가 −6.1%', 'q3', 'MPC 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 10월 29일 — 회장 교체 결정', None,
     'Maryann Mannen CEO가 2026년 1월 1일부터 회장 겸임(Michael Hennigan 은퇴)', 'chair', 'MPC 공시 (SEC 8-K)'),
]
SUMMARY = ('정제·판매 마진이 1년 전의 두 배가 되며 2분기 순이익이 4배로 늘었고, 주가는 1년 새 {CH_TXT}', '정제 마진 급등',
           ['2분기 순이익 $5.1B(1년 전 $1.2B), EPS $17.73였다. 정제·판매 마진은 배럴당 $36.33으로 1년 전($17.58)의 두 배였다.',
            '회사는 모든 지역의 크랙 스프레드 상승을 주된 이유로 들었다.',
            '2분기에 $2.8B를 주주에게 돌려줬고, 6월 말 남은 자사주 매입 승인은 $6.1B다.'],
           '배수는 5년 이력에서 비싼 쪽, 에너지 업종 안에서는 중간이고, 현금흐름 모델 기본값은 주당 ${DCF[\'base\']:.2f}로 현재가보다 크게 낮다.',
           'Q3 2026 실적(11월 초 예상)의 정제·판매 마진.')
BULL = [('정제 마진', '배럴당 $36.33, 1년 전의 두 배.'),
        ('주주환원', '2분기 $2.8B, 배당 +10%.'),
        ('MPLX', '분배금 2026·2027년 연 12.5% 증가 예상(회사).')]
BEAR = [('마진 변동', '정제·판매 마진이 1년 새 $17.58에서 $36.33으로 움직였다.'),
        ('배수', 'PBR·PSR이 5년 중 가장 비싼 쪽.'),
        ('현금흐름 모델', '기본값이 현재가의 약 {DCF[\'base\'] / px * 100:.0f}%.')]
ANALYST = {'rating': 'Buy', 'n': 19, 'nt': 17, 'mean': 374.35, 'median': 400, 'low': 210, 'high': 472, 'sb': 5, 'b': 4, 'h': 9, 's': 0, 'ss': 1}
ANALYST_ASOF = '2026-10-06'


# ── 자동 카드(설계 D, 2026-10-10) — 분기마다 고치던 칸을 auto_card.py가 채운다. 부문 지도는 seg_map_propose.py 제안(손 표와 숫자 일치) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
 ],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {
  "mpc:RefiningAndMarketingMember": [
   "정제·판매",
   "#b22222"
  ],
  "mpc:MidstreamMember": [
   "미드스트림(MPLX)",
   "#e07b39"
  ],
  "mpc:RenewableDieselMember": [
   "재생 디젤",
   "#6aa84f"
  ]
 },
 "ignore": []
}
