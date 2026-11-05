# FIX(컴포트 시스템즈 USA) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 193. 기계(공조·배관)·전기 설비 시공 — 데이터센터·반도체 공장·병원 등 신축과 기존 건물 서비스.
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-23T00:12Z, 10/22 장 마감 뒤), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 장 마감 뒤 발표, 다음 날 10시(중부) 콜), 8-K(CFO 교체 10/22), StockAnalysis. 사전 조사 자료표 scratchpad pre/FIX.md.
# 엔진 입력(2026-10-24): D&A = 감가상각 + 무형자산 상각(DDA_PARTS_BY_CIK + EXCLUDE_TAGS — 합계 태그는 FY2025 한 해 $62.4M뿐, TTM $167M), 4분기 EPS 2021·2023·2024·2025 보도자료 값.
# 차입금 $49.6M(옛 주인에게 줄 어음 등, 리볼버 0), 현금 $2,158M. 인수 TTM $414M. companyfacts에 Q1 2025 값이 연간 기간으로 잘못 붙은 사실이 있다(사전 조사 — 엔진은 fp로 걸러 영향 없음, 연간 매출 9,101.6 대조).
CIK = '0001035983'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, 0), '적정'
CO = 'Comfort Systems'
S_ = 'https://www.sec.gov/Archives/edgar/data/1035983/'
SEC = S_
TENQ = S_ + '000110465926118159/fix-20260930x10q.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000110465926118156/fix-ex99d1.htm', 'q2': S_ + '000110465926086255/fix-20260723xex99d1.htm',
      'q1': S_ + '000110465926047679/fix-20260423xex99d1.htm', 'q4': S_ + '000110465926017529/fix-20260219xex99d1.htm'}
LINKS = {'cfo': S_ + '000110465926118149/tm2628079d1_8k.htm'}
FAIRBAND_TITLE = 'id="fixFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 25)
ACT_REASON = ''
NONOP_WHAT = '투자'
# 고정 문장(숫자 없음).
MODEL_NOTE = ('데이터센터·반도체 공장 같은 대형 신축 수요로 최근 2년 매출·이익이 빠르게 늘었다. 10월 주가 급락의 대부분은 Q3 실적 발표 전에 일어났고, 그 사이 회사 공시는 없었다. '
              '현금흐름 판정이 적정이 된 것은 가격이 내린 결과다 — 내재가치 기본값은 그동안 늘 가격보다 아래였다. 이 값은 과거의 높은 성장이 줄어들며 이어지고, 선수금 덕에 재투자가 거의 들지 않는다는 가정(매출/자본 상한 적용)에 기댄다. '
              '공사 계약 매출이라 수주 잔고와 진행률에 따라 분기 이익률이 움직이고, 고객 선수금이 많아 유동비율이 낮게 보인다. 차입금이 거의 없고 현금이 많다. 기계 부문 건물 매입으로 설비투자가 크게 늘었고 회사는 높은 투자가 다음 해까지 이어진다고 밝혔다.')
PH = ['PWR', 'ETN', 'VRT', 'GEV', 'TT', 'EMR']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '전력·공조·설비 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(FIX 제외)와 배수 순위를 매긴 값이다.',
            '항공·방산·기계·운송·건설이 섞여 있다. 차트에는 전력·공조·설비 6곳만 보인다.')
# 매출(Q3 2026 10-Q 주석 10 부문) — 기계 2,582.9 + 전기 1,183.4 = 3,766.3(= 총매출). 1년 전 1,810.5·640.5.
SEG = [('기계(공조·배관)', 2582.9, '#003a70'), ('전기', 1183.4, '#e87722')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석 — 회사는 조정 EPS를 내지 않는다) + CFO 교체. 반응일: 8-K 장 마감 뒤(00:05~00:10Z) 접수 → 다음 거래일.
# 넣지 않은 8-K: 투자자 자료(7.01 4건), 신용 한도 증액(2025-09).
NEWS_RANGE = '2026.02 ~ 2026.10'
NEWS = [
    ('red', '2026년 10월 22일 — Q3 2026 실적', '2026-10-23',
     '매출 $3.77B(1년 전 $2.45B) · 순이익 $489M · 희석 EPS $13.91(1년 전 $8.25) · 수주 잔고 $17.8B(1년 전 $9.4B, 인수분 제외 전분기 대비 +26%) · 분기 배당 $1.00으로 인상 — 발표 다음 날 주가 −9%(CFO 발표와 같은 날)', 'q3', 'Comfort Systems 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 10월 22일 — CFO 은퇴·후임 발표', '2026-10-23',
     'William George CFO가 2026년 10-K 제출 뒤 은퇴, 후임은 내부의 Julie Shaeff 최고회계책임자(이견 없음)', 'cfo', 'Comfort Systems 공시 (SEC 8-K)'),
    ('red', '2026년 7월 23일 — Q2 2026 실적', '2026-07-24',
     '매출 $3.27B · 순이익 $442M · 희석 EPS $12.53(1년 전 $6.53)', 'q2', 'Comfort Systems 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 23일 — Q1 2026 실적', '2026-04-24',
     '매출 $2.87B · 순이익 $370M · 희석 EPS $10.51(1년 전 $4.75)', 'q1', 'Comfort Systems 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 19일 — Q4 2025 실적', '2026-02-20',
     '매출 $2.65B · 순이익 $331M · 희석 EPS $9.37(1년 전 $4.09) · 2025년 희석 EPS $28.88', 'q4', 'Comfort Systems 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Strong Buy', 'n': 10, 'nt': 7, 'mean': 2026, 'median': 1979, 'low': 1808, 'high': 2500, 'sb': 9, 'b': 0, 'h': 1, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-31'


# ── 자동 카드 — 부문 2개(수동 지도). 원문 대조: Q3 2026 2,582.9/1,183.4(2026-10-24) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax", "us-gaap:Revenues"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"fix:MechanicalSegmentMember": ["기계(공조·배관)", "#003a70"], "fix:ElectricalSegmentMember": ["전기", "#e87722"]},
 "ignore": []
}
