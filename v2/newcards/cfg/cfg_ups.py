# UPS(유나이티드 파슬 서비스) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 152(시총 150위). 소포 배송(미국 국내·국제)·공급망 물류.
# 출처: SEC XBRL, Q2 2026 10-Q(2026-08-05), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 모두 동부 오전 6시대 접수 = 장 전), 8-K(사채 8/12·8/18, 임원 8/31), StockAnalysis.
# 엔진 입력(2026-10-22): 주식 수 = 표지 A주 101,432,177 + B주 749,349,405 = 850.8M(BUILD cover_shares — 엔진 기본값 713.9M은 틀렸다, 표지 태그는 2010년에 멈춤).
# 차입금 $24,484M = 1년 안 634 + 장기·금융리스 23,850(DEBT_TOTAL_TAG — 1년 안 만기가 빠져 $23,850M이었다; 금융리스 포함 태그라 리스에서 또 더하지 않음). 현금 $4,653M = 원문(단기 증권 없음).
# 영업이익: Q2 2026 $930M에 구조조정(트랜스포메이션) 비용 세전 $1,172M(대부분 운전기사 자발적 퇴직 프로그램) — 최근 4분기 이익률이 그만큼 낮다.
# 연금·퇴직 의무 $6,341M(비유동)은 내재가치에서 빼지 않는다(전 카드 공통 — 연금 부채 미차감). 4분기 EPS 보도자료 값.
BUILD = {'cover_shares': True}
CIK = '0001090727'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 1, -2), '적정~고평가'
CO = 'UPS'
S_ = 'https://www.sec.gov/Archives/edgar/data/1090727/'
SEC = S_
TENQ = S_ + '000162828026053249/ups-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000162828026049912/exhibit991-earningspressre.htm', 'q1': S_ + '000162828026027717/exhibit991-earningspressre.htm',
      'q4': S_ + '000162828026003510/exhibit991-earningspressre.htm', 'q3': S_ + '000162828025046550/exhibit991-earningspressre.htm'}
LINKS = {'ahg': 'https://investors.ups.com/news-events/press-releases/detail/2151/ups-acquires-andlauer-healthcare-group-for-1-6-billion'}
FAIRBAND_TITLE = 'id="upsFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다. 최근 4분기 EPS에는 구조조정 비용이 들어 있다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 15)
ACT_REASON = ''
HEALTH_EXTRA = '이자보상배율은 최근 분기 기준이라 구조조정 비용이 크게 든 분기에는 낮게 나온다. 차입금은 분기 말 값으로, 그 뒤 8월에 사채를 더 발행했다.'   # 고정 문장(Fable 필수 2026-10-22) — 분기 바뀌면 고칠 것
NONOP_WHAT = '투자'
# 고정 문장(숫자 없음). 구조조정 비용, 아마존 물량 축소, 연금 부채.
MODEL_NOTE = ('최근 분기 영업이익에는 아마존 물량 축소에 맞춘 구조조정(인력 감축) 비용이 크게 들어 있어 최근 4분기 이익률이 낮게 나온다. '
              '연금·퇴직 의무는 내재가치에서 빼지 않았다 — 빼면 내재가치가 더 낮아진다.')
PH = ['FDX', 'UNP', 'CSX', 'ODFL', 'CHRW', 'EXPD']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '운송·물류 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(UPS 제외)와 배수 순위를 매긴 값이다.',
            '항공우주·기계·서비스·건설이 섞여 있다. 차트에는 운송·물류 6곳만 보인다.')
# 매출(Q2 2026 10-Q 부문) — 미국 국내 14,930 + 국제 5,044 + 공급망 2,860 = 22,834. 1년 전 14,083/4,485/2,653 → 21,221.
SEG = [('미국 국내 소포', 14930.0, '#351c15'), ('국제 소포', 5044.0, '#ffb500'), ('공급망 솔루션(기타 사업)', 2860.0, '#a0826d')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 최신 실적(Q2 2026, 7/28)도 손으로 — 구조조정 비용 $891M(세후)을 적으려고. 가이던스·조정 EPS는 쓰지 않는다.
# 반응일(SEC acceptanceDateTime UTC → 동부): 2025-10-28T10:09Z·2026-01-27T11:08Z·04-28T10:09Z·07-28T10:03Z = 동부 06~07시(장 전) → 같은 날.
# AHG 인수 완료: 회사 보도자료(SEC 8-K 없음), 11/3(Codex r1 권장). 감가상각은 DepreciationAndAmortization(Codex r1 필수 — 합산 태그가 $940M 적었다).
# 넣지 않은 8-K: 사채 발행(8/12 $1.0B 중 $200M은 연금 신탁 출연, 8/18 변동금리 $325M), 이사 사임(Warsh 2/6·5/13, Boratto 6/15), 임원 은퇴(8/31), 주총(5/11).
NEWS_RANGE = '2025.10 ~ 2026.07'
NEWS = [
    ('red', '2026년 7월 28일 — Q2 2026 실적 · 구조조정 비용', '2026-07-28',
     '매출 $22.8B(+7.6%) · 희석 EPS $0.71(1년 전 $1.51) — 운전기사 자발적 퇴직 등 구조조정 비용 세후 $891M(주당 $1.05) · 아마존 물량 축소 완료', 'q2', 'UPS 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 4월 28일 — Q1 2026 실적', '2026-04-28',
     '매출 $21.2B(−1.6%) · 희석 EPS $1.02(1년 전 $1.40) · 미국 국내 영업이익률 3.6%', 'q1', 'UPS 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 1월 27일 — Q4 2025 실적', '2026-01-27',
     '매출 $24.5B(−3.2%) · 희석 EPS $2.10(1년 전 $2.01) — MD-11 화물기 전량 퇴역 상각 세후 $137M 포함', 'q4', 'UPS 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 11월 3일 — Andlauer Healthcare Group 인수 완료', '2025-11-03',
     '캐나다 의약품 물류(콜드체인) 회사 AHG를 주당 C$55 현금, 약 US$1.6B에 인수', 'ahg', 'UPS 보도자료'),
    ('green', '2025년 10월 28일 — Q3 2025 실적', '2025-10-28',
     '매출 $21.4B(−3.7%) · 희석 EPS $1.55(1년 전 $1.80) — 부동산 매각후리스 차익 세전 $330M·구조조정 비용 포함', 'q3', 'UPS 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 29, 'nt': 19, 'mean': 113.68, 'median': 115, 'low': 76, 'high': 132, 'sb': 14, 'b': 0, 'h': 12, 's': 2, 'ss': 1}
ANALYST_ASOF = '2026-10-22'


# ── 자동 카드 — 부문 지도는 손으로(seg_map_propose는 2/3 — 공급망은 부문 표에서 CorporateNonSegment로 실림). 매출 분해 표의 부문 축을 쓴다:
# 미국 국내는 나라 축(country:US), 국제는 NonUs가 함께 붙어 free_axes로 둔다. 원문 대조: Q2 2026 14,930/5,044/2,860, 1년 전 14,083/4,485/2,653(2026-10-22) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "free_axes": ["srt:StatementGeographicalAxis"],
 "members": {
  "ups:USDomesticPackageMember": ["미국 국내 소포", "#351c15"],
  "ups:InternationalPackageMember": ["국제 소포", "#ffb500"],
  "ups:SupplyChainSolutionsMember": ["공급망 솔루션(기타 사업)", "#a0826d"]
 },
 "ignore": ["ups:U.S.DomesticPackageSegmentMember", "ups:InternationalSegmentMember"]
}
