CIK = '0001289490'
BUILD = {'company_tags': [('exr:GainsLossesOnRealEstateTransactionsAndEarnOutFromPriorAcquisitionAndSaleOfOtherAssets', 'GainRealEstateExr', '2020-01-01')]}
# EXR(엑스트라 스페이스 스토리지) v2 카드 설정 — 자동 카드(AUTO), 정식. 회계연도 12월 31일. 리츠(REIT) — 미국 최대 셀프 스토리지(개인 창고 임대) 운영사(UPREIT, 2023년 Life Storage 합병).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-30 접수, 카드 기준일 11-20 종가), 실적 보도자료(8-K 2.02항 — 모두 장 마감 뒤 → 다음 세션).
# 엔진 입력(2026-11-22): 영업이익 = 보고 "Income from operations" − 부동산 매각·매각 예정 손익(DERIVED_OPINC, 회사 고유 태그), 순이익 = NetIncomeLoss(보통주 귀속 값),
#   설비투자 = 개발·재개발 + 집기·설비(기존 점포 개량은 인수 줄에 섞여 제외), 차입금 = 담보 + 기간 대출 + 선순위채 + 신용한도·CP = $13,405.8M, 비지배 = OP 유닛 $868.0M + 우선 OP 유닛 $47.8M.
#   4분기 EPS 2025·2024는 보도자료 값(1.36·1.24).
# 일회성(E54): 최근 4분기 보통주 순이익 $1,039.6M(4분기 $287.4M + 1~9월 $752.2M, 희석 EPS 1.36+1.14+1.25+1.17 = 4.92). FFO·Core FFO 조정표 — 이익 쪽 $46.0M(4.4%: 4분기 합작 매각 이익 $45.2M 등), 비용 쪽 $31.8M(3.1%: 부동산 매각 손실 $11.9M, 합작 손상 $13.9M, 주식보상 가속·소송 $6.0M) — 30%와 거리가 멀어 정식(Codex·Fable r1).
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, -2), '적정~고평가'
CO = 'Extra Space'
S_ = 'https://www.sec.gov/Archives/edgar/data/1289490/'
SEC = S_
TENQ = S_ + '000128949026000065/exr-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000128949026000061/q32026ex991earningsrelease.htm', 'q2': S_ + '000128949026000048/q22026ex991earningsrelease.htm',
      'q1': S_ + '000128949026000034/q12026ex991earningsrelease.htm', 'q4': S_ + '000128949026000007/q42025ex991earningsrelease.htm',
      'q3old': S_ + '000128949025000020/q32025ex991earningsrelease.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="exrFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). 리츠는 감가상각이 커서 PER이 높게 나온다 — PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])} — 2023년 합병 포함)</span>'
Y2 = (0, 60)
ACT_REASON = '리츠라 재고·매출채권 회전으로 보는 활동성이 잘 맞지 않는다'
NONOP_WHAT = '투자'
CAPEX_LABEL = '설비투자(개발·재개발·집기)'   # 점포 인수와, 인수 줄에 섞인 기존 점포 개량은 넣지 않는다
MODEL_NOTE = ('리츠는 건물 감가상각이 커서 GAAP 순이익이 실제 현금 창출보다 작게 나오고, 업계는 FFO(순이익에 부동산 감가상각을 되더하고 매각 이익을 뺀 값)로 본다 — 엑스트라 스페이스의 2026년 Core FFO 전망은 주당 $8.40~8.50(직전 $8.25~8.40)으로 최근 4분기 GAAP EPS의 약 1.7배다(전망과 지난 실적이라 기간은 다르다). 최근 4분기 Core FFO는 주당 $8.44라 주가는 그 약 18배다. 이 카드는 다른 카드와 같은 GAAP 배수로 보므로 PER이 높게 나온다. 사이트에는 리츠 전용 평가(FFO·순자산가치)가 아직 없다. '
              '현금흐름 내재가치는 숫자보다 방향만 본다. 세 시나리오 중 둘은 0 이하이고, 기본 시나리오만 주당 1달러 안팎의 양수다 — 카드 설비투자와 인수 지출이 감가상각보다 작아 엔진이 기본 시나리오에서만 "성장에 자본이 거의 들지 않는다"는 높은 자본효율로 시작하기 때문이고(이익률 차이 때문이 아니다), 현재가 요구 성장률도 이 가정에서 나온 숫자다. 평균 자본효율로 보면 감가상각을 뺀 영업이익의 자본수익률(합병 때 시가로 다시 잡힌 자산 기준)이 할인율 10%보다 낮고, 실제로는 법인세가 거의 없는데 5년 뒤 세율을 21%로 수렴시키며, 과거 5년 매출 성장률에는 합병으로 커진 몫이 들어 있다. 종합 판정의 −2는 이 현금흐름 칸에서만 나왔다. '
              '2023년 7월 Life Storage 합병으로 매출·자산·주식 수가 크게 늘어, 자기 이력 비교는 최근 4분기가 모두 합병 뒤인 2024년 8월부터만 한다. 3년 성장률·이익 성장 점수에도 합병 효과가 들어 있다. 2025년 3분기에는 매각 예정 점포 손실 $105M이, 4분기에는 합작 매각 이익 $45M이 순이익에 들어 있었다(최근 4분기 일회성은 이익 쪽 약 4%, 비용 쪽 약 3%). 영업이익은 회사 보고 영업이익에서 부동산 매각·매각 예정 손익을 뺀 값이다. '
              'FCF의 설비투자에는 개발·재개발과 집기·설비만 넣었다 — 기존 점포 개량 지출은 현금흐름표에서 점포 인수와 한 줄("인수와 개량")로 묶여 있다. 그 줄에서 인수 현금을 뺀 잔액(1~9월 약 $206M, 최근 4분기 약 $262M — 토지 매입도 섞일 수 있다)을 개량으로 보면 최근 4분기 FCF는 약 $1.5B로 줄고 PCR은 그만큼 높아져 카드 값보다 덜 좋다. 이자비용은 원문 손익계산서에 있지만(3분기 $151M + 비현금 상각 $10M) 회사가 쓰는 태그가 카드 재무 자료와 연결되지 않아 이자보상배율 칸이 비어 있다. 고객 창고 보험(임차인 재보험)은 매출의 약 10%지만 이익률이 높아 카드 영업이익의 약 5분의 1을 낸다. 보통 OP 유닛·기타 비지배지분($868M)과 우선 OP 유닛($48M)은 장부가로 주주가치에서 뺀다.')
HEALTH_EXTRA = '점포 매입 자금을 채권으로 조달하는 리츠라 차입금 비중이 높게 나온다 — 리츠는 보통 부채를 자산 가치나 EBITDA 대비로 본다.'
PH = ['PSA', 'AMT', 'O', 'PLD', 'SPG', 'DLR']
PEER_FILE = 'peer_universe/real_estate.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '리츠 6곳 PER 비교 (점수는 S&P500 부동산 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 부동산 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 부동산 대비 배수 순위 (v2/peer_universe/real_estate.json)'
PEER_TIP = ('S&P500 부동산(EXR 제외)과 배수 순위를 매긴 값이다.',
            '물류·데이터센터·의료·쇼핑몰·주택 리츠와 부동산 서비스가 섞여 있다. 셀프 스토리지 리츠는 S&P500에 PSA와 엑스트라 스페이스다.')
SEG = [('셀프 스토리지 임대', 760.8, '#00843d'), ('임차인 재보험', 94.2, '#4caf7a'), ('관리 수수료·기타', 34.8, '#bfe3cc')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문'
NEWS_RANGE = '2025.10 ~ 2026.11'
NEWS = [
    ('neutral', '2026년 10월 27일 장 마감 뒤 — Q3 2026 실적', '2026-10-28',
     '희석 EPS $1.17(1년 전 $0.78은 매각 예정 점포 손실 $105M 포함) · Core FFO $2.17(+4.3%) · 동일 점포 NOI +4.6% · 2026년 Core FFO 전망 $8.40~8.50으로 상향 — 다음 날 주가 +0.1%', 'q3', 'Extra Space 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 7월 28일 장 마감 뒤 — Q2 2026 실적', '2026-07-29',
     '희석 EPS $1.25 · Core FFO $2.15(+4.9%) · 동일 점포 NOI +3.5% · 점포 17곳 인수 — 다음 날 주가 +0.4%', 'q2', 'Extra Space 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 28일 장 마감 뒤 — Q1 2026 실적', '2026-04-29',
     '희석 EPS $1.14(1년 전은 매각 이익 포함) · Core FFO $2.04(+2.0%) · 동일 점포 매출 +1.7% — 다음 날 주가 −0.3%', 'q1', 'Extra Space 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 19일 장 마감 뒤 — 2025년 연간 실적', '2026-02-20',
     '4분기 희석 EPS $1.36 · Core FFO $2.08(+2.5%) · 동일 점포 매출 +0.4% · 점포 27곳 $305M 인수 — 다음 날 주가 +4.6%', 'q4', 'Extra Space 실적 보도자료 (SEC 8-K)'),
    ('red', '2025년 10월 29일 장 마감 뒤 — Q3 2025 실적', '2025-10-30',
     '희석 EPS $0.78(매각 예정 점포 손실 $105M 포함) · Core FFO $2.08(+0.5%) · 동일 점포 매출 −0.2%·NOI −2.5% — 다음 날 주가 −4.9%', 'q3old', 'Extra Space 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 21, 'nt': 16, 'mean': 161.19, 'median': 158, 'low': 152, 'high': 178, 'sb': 7, 'b': 3, 'h': 11, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-23'
POST = [r"""
h = h.replace('· GAAP 기준 · FCF는 영업현금흐름 − 설비투자(개발·재개발·집기) ·', '· GAAP 기준(영업이익은 부동산 매각 손익 제외) · FCF는 영업현금흐름 − 설비투자(개발·재개발·집기 — 기존 점포 개량 제외) ·')
h = h.replace('합성 영업이익률(세전이익 기준)', '카드 기준 영업이익률(매각 손익 제외)').replace('합성 영업이익(세전이익 기준)', '카드 기준 영업이익(매각 손익 제외)')
h = h.replace('Q3 2026 10-Q 부문 표 (SEC)', 'Q3 2026 10-Q 부문 주석 (SEC)')
import re as _rx
h = _rx.sub(r'(최근 4분기 FCF \$[0-9.]+B, 매출의 [0-9.]+%)\.', r'\1 — 기존 점포 개량(인수 줄에 섞임, 2026년 9월까지 최근 4분기 약 $0.26B 추정)은 빠진 값.', h)
h = _rx.sub(r'(FCF\(최근 4분기 \$[0-9.]+B\))(가 배당 지급)', r'\1 — 기존 점포 개량 추정분을 빼기 전 값 —\2', h)
h = _rx.sub(r'(매출 \+?[−-]?[0-9.]+%\(보고 기준, 3년 연평균 [0-9.]+%)\)', r'\1 — 2023년 합병 포함)', h)
h = h.replace('그 분기 이자비용 미공시', '이자비용 태그 연결 안 됨(원문에는 있다)')
h = _rx.sub(r'잔존가치\(5년 뒤\)가 내재가치의 ([0-9]+)%', r'잔존가치(5년 뒤)가 영업 기업가치의 \1%', h)
h = h.replace('`잔존가치(5년 뒤)가 내재가치의 ${', '`잔존가치(5년 뒤)가 영업 기업가치의 ${')
"""]

# 현금흐름 0 이하 보정 — ED·SO와 같은 POST
POST += [r'''
_R = '현금흐름 모델의 주당 지분가치가 0 이하라 현재가 요구 성장률·영업이익률은 해석할 수 없다.'
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
h = _re.sub(r'(id="oDcfReq"[^>]*>)연 -[0-9.]+%', lambda m: m.group(1) + '해석 부적합', h)
h = _re.sub(r'현재가를 정당화하려면 매출이 5년간 연 [−-][0-9.]+% 커야 한다\. ', '현금흐름 값이 0 이하라 현재가 요구 성장률은 해석할 수 없다. ', h)
''']
# 헤더 '현재가 요구 성장' 칸 — 현금흐름 값이 0 이하이면 숫자 대신 '해석 부적합'(AEE Fable r1, 2026-10-25)
POST.append(r'''
h = h.replace("  if (req && price != null) {", "  if (req && d.base <= 0) { req.textContent = '해석 부적합'; req.style.color = 'var(--text3)'; const _c = req.closest('.meta-item'); if (_c) _c.title = '해석 부적합(현금흐름 0 이하) — 현금흐름 내재가치가 0 이하라 현재가 요구 성장률·영업이익률을 해석할 수 없다.'; }\n  if (req && price != null && d.base > 0) {", 1)
import re as _re2
h = _re2.sub(r'(id="oDcfReq"[^>]*>)연 [−-][0-9.]+%', lambda m: m.group(1) + '해석 부적합', h)
''')

AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"exr:SelfStorageOperationsMember": ["셀프 스토리지 임대", "#00843d"],
             "exr:TenantReinsuranceMember": ["임차인 재보험", "#4caf7a"]},
 "ignore": [],
 "remainder": ["관리 수수료·기타", "#bfe3cc", 0.039]
}
