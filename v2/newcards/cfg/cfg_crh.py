# CRH v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 199(시총 203위). 골재·시멘트·아스팔트·건축 자재(북미 중심, 유럽·호주).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-07-30), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 2025년은 장 마감 뒤, 2026년은 장 전), 8-K(Arcosa 인수 계약 6/22·완료 10/23), StockAnalysis. 사전 조사 자료표 scratchpad pre/CRH.md.
# 짧은 이력(사용자 결정 2026-10-24 "CEG 방식"): 2023-09 미국 주 상장 이전(2024년부터 10-Q)으로 미국 회계 분기 이력이 2023년 말부터다 — 자기 이력 창이 약 2년, build_dcf HISTORY_WINDOW("2023-12-31", 11).
# 엔진 입력: 비지배지분 = 자본 안 $1,065M + 상환가능 $435M(EV_TAGS), 4분기 EPS 2024·2025 보도자료 값. EV/EBITDA는 2025년 3분기 누계 D&A 태그가 없어 오늘 값을 못 구한다(빠짐).
# Arcosa 인수(약 $8.5B, 10/23 완료)는 Q2 재무상태표 뒤 — 차입금이 Q4부터 크게 는다. Q3 실적 10/29 예정.
CIK = '0000849395'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, 0, -2), '적정~고평가'
CO = 'CRH'
S_ = 'https://www.sec.gov/Archives/edgar/data/849395/'
SEC = S_
TENQ = S_ + '000162828026050755/crh-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000162828026050752/q2resultsannouncement2026.htm', 'q1': S_ + '000162828026028554/q1resultsannouncement2026.htm',
      'q4': S_ + '000162828026009032/fullyearresultsannouncemen.htm', 'q3': S_ + '000162828025049547/q3resultsannouncement2025.htm'}
LINKS = {'arc': S_ + '000119312526429523/d187492dex991.htm', 'arc0': S_ + '000119312526276686/d864737d8k.htm'}
NEXT_CONFIRMED = {'quarter_end': '2026-09-30', 'date': '2026-10-29', 'src': '10/23 Arcosa 인수 완료 발표 — Q3 실적과 함께 전망 갱신'}
FAIRBAND_TITLE = 'id="crhFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (이력 약 2.5년 · 실제 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (-5, 25)
ACT_REASON = ''
NONOP_WHAT = '투자'
# 고정 문장(숫자 없음). D&A는 2025년 3분기 누계 태그가 없어 FY2025 연간 값(TTM 대비 약 $0.12B 작음 — 기본값 영향 약 $0.2)이 쓰였다(Codex r1, 엔진 공통 경로라 그대로).
MODEL_NOTE = ('2023년 9월 주 상장을 런던에서 뉴욕으로 옮겨 2024년부터 미국 회계 분기 보고서를 냈다 — 자료가 짧아 자기 이력은 약 2~2.5년 분포라 다른 카드의 5년보다 표본이 작고, 현금흐름 모델의 과거 성장·이익률도 짧은 이력에서 나온다. '
              '건설 자재라 겨울이 낀 1분기는 계절적으로 적자에 가깝다. 최근 4분기 이익에는 비핵심 사업 매각 이익과 자산 처분 이익이 들어 있다. '
              'Arcosa 인수(10월 완료)로 차입금이 Q4부터 크게 늘고 매출 구성도 바뀐다 — 이 카드의 재무는 인수 전이다. '
              '자기 이력이 매우 싸게 나오는 것은 짧은 이력 안에서 지금 배수가 바닥 근처라는 뜻이고(주가가 1년 새 크게 내림), 현금흐름 모델은 최근 인수 대금을 재투자로 넣고 할인율이 자본수익률과 비슷해 낮은 값을 낸다 — 두 판정은 같은 질문이 아니다.')
HEALTH_EXTRA = '이자보상배율은 Q2 단일 분기 값이다 — 계절성이 큰 회사라 최근 4분기로 보면 더 낮다.'   # 고정 문장(Fable r1 2026-10-24)
# 짧은 이력 표기 보정(Codex·Fable r1 필수) — 템플릿의 '5년'은 이 카드에선 약 2.5년이다. 배당 칸은 지급 태그가 없을 뿐 선언 배당이 있다.
POST = [r'''
h = h.replace('지난 5년', '지난 약 2.5년')
h = h.replace('자기 5년 위치', '자기 이력(약 2.5년) 위치')
h = h.replace('자신의 5년 배수 분포', '자신의 약 2.5년 배수 분포')
h = h.replace('3년 연평균', '2.5년 연평균')
h = h.replace('<span class="zone-label">보통주 배당 지급</span>\n          <span class="zone-val">공시 없음</span>', '<span class="zone-label">보통주 배당 지급</span>\n          <span class="zone-val">지급 태그 없음(선언 배당은 있음)</span>', 1)
''']
PH = ['VMC', 'MLM', 'LIN', 'SHW', 'ECL', 'APD']
PEER_FILE = 'peer_universe/materials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '소재 6곳 PER 비교 (점수는 S&P500 소재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 소재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 소재 대비 배수 순위 (v2/peer_universe/materials.json)'
PEER_TIP = ('S&P500 소재(CRH 제외)와 배수 순위를 매긴 값이다.',
            '골재·시멘트·화학·금속·포장이 섞여 있다. 차트에는 소재 6곳을 보인다.')
# 매출(Q2 2026 10-Q 주석 2 부문) — 미주 소재 4,957 + 미주 건축 2,117 + 국제 3,703 = 10,777(= 총매출). 1년 전 4,509·2,159·3,538.
SEG = [('미주 소재(골재·아스팔트)', 4957.0, '#1b5e20'), ('국제(유럽·호주)', 3703.0, '#66bb6a'), ('미주 건축 자재', 2117.0, '#0d3311')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석 — 조정 EPS·가이던스는 쓰지 않는다) + Arcosa 인수 계약·완료. 반응일: 2025년 실적 8-K 장 마감 뒤(21:09Z) → 다음 날, 2026년 실적 장 전(10:0xZ) → 같은 날, Arcosa 완료 12:51Z(장 전) → 같은 날.
# 넣지 않은 8-K: 사채(2025-10), 텀론(7/17), 광산 안전 명령(1.04), 임원·주총.
NEWS_RANGE = '2025.11 ~ 2026.10'
NEWS = [
    ('neutral', '2026년 10월 23일 — Arcosa 인수 완료', '2026-10-23',
     '기업가치 약 $8.5B(주당 현금 $150은 6/22 계약 기준) — 조달은 텀론 $2.5B(7/17 8-K)·브리지 대출(6/22 약정 기준) 계획, 전망은 10/29 Q3 실적에서 갱신', 'arc', 'CRH 공시 (SEC 8-K)'),
    ('red', '2026년 7월 30일 — Q2 2026 실적', '2026-07-30',
     '매출 $10.78B(1년 전 $10.21B) · 순이익 $1.49B · 희석 EPS $2.21(1년 전 $1.94) — 사업 매각 이익 등 영업외 이익 $282M 포함', 'q2', 'CRH 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 6월 22일 — Arcosa 인수 계약', '2026-06-22',
     '주당 현금 $150(기업가치 약 $8.5B), 브리지 대출 $5.75B 약정', 'arc0', 'CRH 공시 (SEC 8-K)'),
    ('green', '2026년 4월 30일 — Q1 2026 실적', '2026-04-30',
     '매출 $7.37B · 순손실 $176M · 희석 EPS −$0.27(1년 전 −$0.15, 계절적 1분기) — 매각 예정 사업 손상 $48M 포함', 'q1', 'CRH 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 18일 — Q4 2025 실적', '2026-02-19',
     '매출 $9.42B · 순이익 $1.03B · 희석 EPS $1.52(1년 전 $1.02) · 2025년 희석 EPS $5.51', 'q4', 'CRH 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 11월 5일 — Q3 2025 실적', '2025-11-06',
     '매출 $11.07B · 순이익 $1.50B · 희석 EPS $2.21(1년 전 $1.97)', 'q3', 'CRH 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Strong Buy', 'n': 23, 'nt': 14, 'mean': 123.86, 'median': 120, 'low': 107, 'high': 150, 'sb': 16, 'b': 6, 'h': 1, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-08'


# ── 자동 카드 — 부문 3개(수동 지도). 원문 대조: Q2 2026 4,957/2,117/3,703(2026-10-24) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax", "us-gaap:Revenues"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"crh:AmericasMaterialsSolutionsMember": ["미주 소재(골재·아스팔트)", "#1b5e20"], "crh:InternationalSolutionsMember": ["국제(유럽·호주)", "#66bb6a"],
             "crh:AmericasBuildingSolutionsMember": ["미주 건축 자재", "#0d3311"]},
 "ignore": []
}
