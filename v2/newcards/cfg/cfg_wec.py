# WEC(WEC 에너지) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 위스콘신 규제 전력·가스(Wisconsin Electric·WPS 등) + 일리노이 가스(Peoples Gas)·기타 주, 비공익 에너지 인프라(We Power), ATC 송전 지분법.
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-30 07:35 장 전 접수), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 장 전 07:2x 동부 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/WEC.md.
# 엔진 입력(2026-11-03): 차입금 = 단기(CP) $1,904.3M + 1년 안 장기부채 $1,134.5M + 장기 $19,717.2M = $22,756.0M(DEBT_TOTAL_TAG — 전환사채 3종·후순위채 포함), 비지배지분 = OtherMinorityInterests $404.3M(EV_TAGS_BY_CIK), 자회사 우선주 $30.4M.
# 순이익은 NetIncomeLossAvailableToCommonStockholdersBasic(NI_TAGS — NetIncomeLoss 차원 없는 값이 2015년 뒤 없다), 희석 EPS는 계속사업 태그 우선, Q4 2021~2025는 보도자료 값(Q4_EPS_OVERRIDE).
# 일회성: 최근 4분기 GAAP 5.51 중 Q4 2025 일리노이 요금 환급 합의·부문 손상 주당 0.45(8.2%).
BUILD = {'eps_tag': 'IncomeLossFromContinuingOperationsPerDilutedShare,EarningsPerShareDiluted'}   # 10-Q는 계속사업 EPS 태그, 10-K는 EarningsPerShareDiluted(중단사업 없음 — 같은 값)
NI_TAGS = ['NetIncomeLossAvailableToCommonStockholdersBasic', 'ProfitLoss']   # NetIncomeLoss 차원 없는 값이 2015년 뒤 없다(ATC 지분법 주석 값만 차원으로)
CIK = '0000783325'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, -1, -2), '고평가'
CO = 'WEC Energy'
S_ = 'https://www.sec.gov/Archives/edgar/data/783325/'
SEC = S_
SEC0 = S_ + '000'   # 보도자료 8-K 중 세 건은 제출 대리인 접수 번호(0001104659-…)
TENQ = S_ + '000078332526000107/wec-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000078332526000104/a2026q3wecearningsreleasee.htm', 'q2': S_ + '000078332526000080/a2026q2wecearningsreleasee.htm',
      'q1': S_ + '000078332526000049/a2026q1wecearningsreleasee.htm', 'q4': S_ + '000078332526000011/a2025q4wecearningsreleasee.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="wecFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 30)
ACT_REASON = '유틸리티라 재고·매출채권 회전으로 보는 활동성이 잘 맞지 않는다'
NONOP_WHAT = '투자'
MODEL_NOTE = ('전력망·발전 설비 투자(9개월 $3.3B — 데이터센터 등 대규모 고객용 포함)가 감가상각보다 훨씬 커서, 큰 차입금(약 $22.8B)을 뺀 현금흐름 모델의 값이 0 아래로 나온다 — 규제 유틸리티는 그 투자가 요금 기준 자산이 되어 이익으로 돌아오는 구조라 현금흐름 모델과 PCR은 의미가 약하다. '
              '2027~2029년 만기 전환사채 3종(장부 $2.6B)은 차입금에 들어 있고, 주식으로 바뀌면 주식 수가 늘 수 있다. '
              '판정 경계: 최근 4분기 EPS에서 Q4 2025 일리노이 요금 환급 합의 손실(주당 0.45)을 빼면 동종업이 약 30점으로 문턱 근처다. 반대로 설비투자 이력이 2023-09에서 멈춰(연간 태그가 다르다) PCR이 빠져 있는데, 최신 설비투자(최근 4분기 약 $4.6B, FCF 음수)를 넣으면 자기 이력이 약 27점으로 내려간다 — 어느 쪽이든 판정은 고평가다.')
HEALTH_EXTRA = '설비투자 자금을 사채·신주로 조달하는 구조라 차입금 비중이 높게 나온다 — 규제 유틸리티에서는 흔한 모습이다.'
# 현금흐름 0 이하 — SO·ATO와 같은 문구 보정(0 이하가 아니면 바뀌지 않는다)
POST = [r'''
_R = '현금흐름 모델의 주당 지분가치가 0 이하라(큰 차입금을 뺀 뒤) 기본 시나리오 환산 성장률은 해석할 수 없다.'
_pairs = [
 ("fill('[data-dcf-basev]', '$' + (Math.abs(D.base) < 10 ? D.base.toFixed(2) : Math.round(D.base)));",
  "fill('[data-dcf-basev]', '$' + (Math.abs(D.base) < 10 ? D.base.toFixed(2) : Math.round(D.base)));\n  if (D.base <= 0) { const _rv = document.querySelector('#dcf .reverse'); if (_rv) _rv.textContent = _XR; }"),
 ("const tv = D.tvShare != null ? `잔존가치(5년 뒤)가 내재가치의 ${Math.round(D.tvShare * 100)}%` : '';",
  "const tv = D.base <= 0 ? '잔존가치 비중 — 내재가치가 0 이하라 의미 없음' : (D.tvShare != null ? `잔존가치(5년 뒤)가 내재가치의 ${Math.round(D.tvShare * 100)}%` : '');"),
 ("`현재가 $${price.toFixed(2)} 가 정당화되려면 5년 내내`\n          + ` 연 ${(d.requiredGrowth*100).toFixed(1)}% 매출 성장이 필요하다.`)",
  "(d.base <= 0 ? _XR : `현재가 $${price.toFixed(2)} 가 정당화되려면 5년 내내`\n          + ` 연 ${(d.requiredGrowth*100).toFixed(1)}% 매출 성장이 필요하다.`))"),
]
for _x, _y in _pairs:
    if _x in h:
        h = h.replace(_x, _y)
if 'const _XR' not in h:
    h = h.replace('<script>', '<script>\nconst _XR = ' + repr(_R) + ';', 1)
import re as _re
h = _re.sub(r'잔존가치\(5년 뒤\)가 내재가치의 [0-9,]+%', '잔존가치 비중 — 내재가치가 0 이하라 의미 없음', h)
h = _re.sub(r'(id="wecDcfReq"[^>]*>)연 -[0-9.]+%', lambda m: m.group(1) + '해석 부적합', h)
h = _re.sub(r'현재가를 정당화하려면 매출이 5년간 연 [−-][0-9.]+% 커야 한다\. ', '현금흐름 값이 0 이하라 현재가 요구 성장률은 해석할 수 없다. ', h)
''']
# 헤더 '현재가 요구 성장' 칸 — 현금흐름 값이 0 이하이면 숫자 대신 '해석 부적합'(AEE Fable r1, 2026-10-25)
POST.append(r'''
h = h.replace("  if (req && price != null) {", "  if (req && d.base <= 0) { req.textContent = '해석 부적합'; req.style.color = 'var(--text3)'; const _c = req.closest('.meta-item'); if (_c) _c.title = '해석 부적합(현금흐름 0 이하) — 현금흐름 내재가치가 0 이하라 현재가 요구 성장률을 해석할 수 없다.'; }\n  if (req && price != null && d.base > 0) {", 1)
import re as _re2
h = _re2.sub(r'(id="wecDcfReq"[^>]*>)연 [−-][0-9.]+%', lambda m: m.group(1) + '해석 부적합', h)
''')
PH = ['NEE', 'SO', 'DUK', 'AEP', 'XEL', 'AEE']
PEER_FILE = 'peer_universe/utilities.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '유틸리티 6곳 PER 비교 (점수는 S&P500 유틸리티 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 유틸리티 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 유틸리티 대비 배수 순위 (v2/peer_universe/utilities.json)'
PEER_TIP = ('S&P500 유틸리티(WEC 제외)와 배수 순위를 매긴 값이다.',
            '규제 전력·가스, 독립 발전사, 수도가 섞여 있다. 차트에는 유틸리티 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문) — 위스콘신 1,964.7 + 일리노이 183.2 + 기타 주 60.9 + 비공익 200.9 = 2,409.7, 부문 간 거래 −119.1 → 연결 2,290.6.
SEG = [('위스콘신', 1964.7, '#00467f'), ('일리노이', 183.2, '#f6a800'), ('기타 주', 60.9, '#5b9bd5'), ('비공익 에너지 인프라', 200.9, '#5b6770')]
SEG_ADJ = -119.1
SEG_ADJ_LABEL = '부문 간 거래(We Power → Wisconsin Electric)'
SEG_TITLE = '매출 구성 — 부문별(Q3 2026)'   # 분기는 fill.py가 실제 값으로 붙인다 — 손으로 적으면 분기를 넘길 때 두 번 나온다(2026-10-30)
NEWS_RANGE = '2026.02 ~ 2026.10'
NEWS = [
    ('neutral', '2026년 10월 29일 장 전 — Q3 2026 실적', '2026-10-29',
     '매출 $2.29B(+8.9%) · 순이익 $389M · 희석 EPS $1.18(1년 전 $0.83) · 2026 EPS 전망 5.60~5.64로 상향 — 당일 주가 +3.7%', 'q3', 'WEC Energy 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 7월 29일 장 전 — Q2 2026 실적', '2026-07-29',
     '매출 $2.06B(+2.6%) · 순이익 $299M · 희석 EPS $0.91(1년 전 $0.76) — 당일 주가 −2.0%', 'q2', 'WEC Energy 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 5월 5일 장 전 — Q1 2026 실적', '2026-05-05',
     '매출 $3.43B(+9.0%) · 순이익 $804M · 희석 EPS $2.45(1년 전 $2.27) — 당일 주가 −1.0%', 'q1', 'WEC Energy 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 5일 장 전 — Q4 2025 실적', '2026-02-05',
     '매출 $2.54B · 순이익 $317M · 희석 EPS $0.97(1년 전 $1.43) — 일리노이 요금 환급 합의 주당 $0.45 포함 · 2025년 EPS $4.81 — 당일 주가 −1.2%', 'q4', 'WEC Energy 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 20, 'nt': 15, 'mean': 116.93, 'median': 115, 'low': 106.5, 'high': 130, 'sb': 6, 'b': 2, 'h': 11, 's': 0, 'ss': 1}
ANALYST_ASOF = '2026-11-03'


# ── 자동 카드 — 원문 대조: Q3 2026 1,964.7/183.2/60.9/200.9, 부문 간 −119.1(2026-10-30) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"wec:WisconsinMember": ["위스콘신", "#00467f"], "wec:IllinoisMember": ["일리노이", "#f6a800"], "wec:OtherStatesMember": ["기타 주", "#5b9bd5"], "wec:NonUtilityEnergyInfrastructureMember": ["비공익 에너지 인프라", "#5b6770"]},
 "ignore": ["wec:PublicUtilityMember", "us-gaap:CorporateAndOtherMember"]
}
