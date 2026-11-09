CIK = '0000092380'
# LUV(사우스웨스트 항공) v2 카드 설정 — 자동 카드(AUTO), 정식. 회계연도 12월 말. 미국 국내선 중심 항공사 — 2025~2026년 수하물 요금·지정 좌석·기본 운임 도입 등 사업 모델 전환.
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-22 16:25 동부 장 마감 뒤 → 10-23, 카드 기준일 11-06 종가), 실적 보도자료(8-K 2.02항 — 모두 장 마감 뒤 16:0x~16:1x 동부 → 다음 날).
# 보류 목록 D군(안건 E54) — 30% 규칙: 최근 4분기 GAAP 희석 EPS 2.08(0.61 + 0.45 + 0.47 + 0.55) 대 특별 항목 제외 EPS 2.63(0.58 + 0.45 + 0.94 + 0.66).
#   특별 항목(세후 주당): Q4 2025 −0.03(DOT 합의 면제 이익 등), Q2 2026 +0.47(미사용 항공권 크레딧 수익 환입 $285M), Q3 2026 +0.11(퇴직금·소송·자산 손상)
#   → 순 약 0.55(EPS 기준 26.4%, 세후 순이익 금액 기준 268/1,053 = 25.4%), 순비용 분기(Q2·Q3)만 290/1,053 = 27.5% — 모두 30% 아래라 정식(ALGN 28.6%와 같은 경계 사례, 2026-11-09).
#   회사 특별 항목에 없는 항공기 매각·세일앤리스백 이익(9개월 세전 272 + 118 = $390M, Q3 214)은 GAAP 이익을 올리는 쪽 — 회사 분류를 따라 특별 항목에 넣지 않고(VTRS 결정과 같은 원칙) MODEL_NOTE에 공개(Fable r1).
# 엔진 입력(2026-11-09): 차입금 $5,887M(1년 안 2,153 + 장기 3,734, 금융리스 포함 — 2025년 말 공시 $78M; DEBT_TOTAL_TAG·FL_IN_DEBT), 현금 $3,624M.
#   4분기 EPS 2025·2024는 보도자료(Q4_EPS_OVERRIDE — 0.61·0.42). 재고 = 부품·소모품 AirlineRelatedInventory $997M(CONCEPTS_BY_CIK).
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 1, -2), '적정~고평가'
CO = 'Southwest Airlines'
S_ = 'https://www.sec.gov/Archives/edgar/data/92380/'
SEC = S_
TENQ = S_ + '000009238026000107/luv-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000009238026000104/er-9302026xerdoc.htm', 'q2': S_ + '000009238026000074/er-6302026xerdoc.htm',
      'q1': S_ + '000009238026000044/er-3312026xerdoc.htm', 'q4': S_ + '000009238026000002/er-12312025xerdoc.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="luvFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (-15, 15)
ACT_REASON = '항공사라 재고가 팔 상품이 아니라 정비용 부품·소모품뿐이고 미리 받은 항공권 대금(항공 운송 부채)이 커서 재고·매출채권 회전으로 보는 활동성이 잘 맞지 않는다'
NONOP_WHAT = '투자'
MODEL_NOTE = ('최근 4분기 GAAP 희석 EPS($2.08)와 특별 항목 제외 EPS($2.63)의 차이는 대부분 2026년 2분기 회계 조정이다 — 2022~2025년에 낙전 수익으로 잡았던 만료 없는 항공권 크레딧 일부를 사용 추세에 맞춰 되돌렸다($285M, 매출 차감). '
              '여기에 3분기 퇴직금·소송·자산 손상을 더해도 세후 주당 약 $0.55(GAAP의 약 26%, 비용이 난 분기만 보면 약 28%)라 30% 기준 아래다 — 기준에 가까운 경계 사례라 GAAP 이익이 조금 눌려 있다는 점을 감안해 읽는다. 반대로 GAAP 이익에는 회사가 특별 항목으로 빼지 않은 항공기 매각·세일앤리스백 이익(2026년 9개월 세전 약 $390M, 3분기 약 $214M)이 들어 있어 이 부분은 이익을 올려 준다 — 노후 기체를 팔고 다시 빌리는 일이라 해마다 같은 크기로 이어진다고 보기 어렵다. '
              '2025년 수하물 요금·지정 좌석·기본 운임·프리미엄 좌석을 도입한 사업 모델 전환이 2026년에 실적으로 나타났다 — 3분기 매출 $8.4B(+21%), 좌석 마일당 매출 +21.6%로 기록이었다. 다만 연료비가 크게 올라(3분기 +$821M, 갤런당 $3.92) 이익 개선 폭을 줄였다. 2025년에 연료 헤지 프로그램을 끝내 지금은 연료 가격 변동에 그대로 노출된다 — 4분기 예상 연료 단가는 갤런당 약 $4.55, 사용량 약 5.73억 갤런이라 1센트가 분기 약 $5.7M이다. '
              '회사는 2026년 조정 EPS 전망을 1월 $4.00 이상에서 7월 $3.25~4.25, 10월 $2.60~2.85로 두 차례 낮췄고(연료비), 4분기는 조정 EPS $0.55~0.80, 좌석 마일당 매출 +19~21%를 예상한다. 2026년 보잉 737 67대를 받고 약 60대를 퇴역시키며, 순 설비투자는 $2.5~2.75B로 본다. 2027년 3월 2일 뉴욕 투자자 설명회(Capital Markets Day)에서 다년 재무 목표를 내놓겠다고 했다(Q3 보도자료). '
              '2025년 11월 $1.5B, 2026년 11월 $1.25B 회사채를 발행하고 3월 기한부 대출을 새로 맺었다. 9월 말 차입금은 금융리스 포함 $5.9B, 그중 1년 안 만기가 $2.2B다(11월 채권 발행 전). 자사주 한도 $2.0B 중 $450M이 남아 있다. '
              '2월 이사 2명(C. David Cush·Gregg A. Saretsky)이 물러났고 8월 Rocket Companies CEO Varun Krishna와 Royal Caribbean CEO Jason Liberty가 새 이사가 됐다. 주가는 2025년 11월 약 $31에서 2026년 2월 약 $55까지 올랐다가 일부 내려왔다.')
PH = ['DAL', 'UAL', 'FDX', 'UPS']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '항공·운송 4곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(LUV 제외)와 배수 순위를 매긴 값이다.',
            '항공·운송·기계·방산이 섞여 있다. 차트에는 항공(DAL·UAL)과 운송(FDX·UPS) 4곳만 보인다.')
# 매출(Q3 2026 10-Q): 여객 7,754 + 화물 48 + 기타(마일리지 판매 등) 621 = 8,422(반올림 차 −1).
SEG = [('여객', 7754.0, '#304cb2'), ('기타(마일리지 판매 등)', 621.0, '#ffbf27'), ('화물', 48.0, '#c9d2ee')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 종류별'
# 손 뉴스: 실적 4건. 반응일: 장 마감 뒤 → 다음 날. 색은 사건 성격, 수치는 그날 주가.
NEWS_RANGE = '2026.01 ~ 2026.10'
NEWS = [
    ('neutral', '2026년 10월 21일 장 마감 뒤 — Q3 2026 실적', '2026-10-22',
     '매출 $8.4B(+21%) · GAAP 희석 EPS $0.55 · 특별 항목 제외 EPS $0.66 · 연간 조정 EPS 전망 $2.60~2.85로 낮춤(연료비) · 2027년 3월 투자자 설명회 예고 — 다음 날 주가 +5.4%', 'q3', 'Southwest 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 7월 22일 장 마감 뒤 — Q2 2026 실적', '2026-07-23',
     '매출 $8.4B(+16%) · GAAP 희석 EPS $0.47(항공권 크레딧 수익 환입 $285M) · 특별 항목 제외 EPS $0.94 · 연간 조정 EPS 전망 $4.00 이상 → $3.25~4.25 — 다음 날 주가 −6.2%', 'q2', 'Southwest 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 22일 장 마감 뒤 — Q1 2026 실적', '2026-04-23',
     '순이익 $227M · GAAP 희석 EPS $0.45 · 영업이익률 4.6%(+8.1%p) · 1분기 기록 매출 — 다음 날 주가 −4.1%', 'q1', 'Southwest 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 1월 28일 장 마감 뒤 — 2025년 연간 실적 · 2026년 전망', '2026-01-29',
     '4분기 GAAP 희석 EPS $0.61 · 2025년 조정 EPS $0.93 · 2026년 조정 EPS $4.00 이상(300% 넘는 증가) 전망 — 다음 날 주가 +18.7%', 'q4', 'Southwest 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 26, 'nt': 17, 'mean': 50.06, 'median': 50, 'low': 34, 'high': 65, 'sb': 7, 'b': 5, 'h': 11, 's': 2, 'ss': 1}
ANALYST_ASOF = '2026-11-09'

AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "srt:ProductOrServiceAxis",
 "extra": {},
 "members": {"us-gaap:PassengerMember": ["여객", "#304cb2"], "us-gaap:ProductAndServiceOtherMember": ["기타(마일리지 판매 등)", "#ffbf27"], "us-gaap:CargoAndFreightMember": ["화물", "#c9d2ee"]},
 "ignore": ["luv:PassengerAncillarySoldSeparatelyMember", "luv:PassengerLoyaltyAirTransportationMember", "luv:PassengerRevenueNonLoyaltyMember", "luv:ProductAndServiceOtherLoyaltyProgramMember", "luv:ProductAndServiceOtherOtherMiscellaneousMember"]
}
# Fable r1: 5년 성장 기준점이 코로나 저점(2021)이라 부풀려졌다 — 2019 $22,428M → 2025 $28,063M은 연 약 3.8%(XBRL 연간 매출).
# 체크포인트 ①은 회사 4분기 가이던스(좌석 마일당 매출 +19~21%)로, 자사주 칸은 실제 지급액 $1,250M(Q3 10-Q 현금흐름표)로 맞춘다.
POST = [r"""
_c1 = h[h.index('<strong style="color:var(--accent2);">①</strong>'):]; _c1 = _c1[:_c1.index('</div>')]
h = h.replace(_c1, '<strong style="color:var(--accent2);">①</strong> 4분기 좌석 마일당 매출이 회사 전망(1년 전 대비 +19~21%) 안에 드는지, 연료비(가정 갤런당 약 $4.55)가 그보다 오르지 않는지 — 헤지 없이 그대로 노출된다', 1)
_n = '<div class="note">세 값은 확률이 아니라'
assert h.count(_n) == 1
h = h.replace(_n, '<div class="note">5년 성장률은 코로나로 매출이 꺼졌던 시기에서 출발해 크게 부풀려져 있다 — 코로나 전 2019년($22.4B)에서 2025년($28.1B)까지는 연 약 3.8%다. 기본 시나리오의 성장 가정은 그만큼 낙관적으로 읽어야 한다.</div>\n    ' + _n, 1)
h = h.replace('<span class="zone-val">$1.2B</span>', '<span class="zone-val">$1.25B</span>', 1)
"""]
