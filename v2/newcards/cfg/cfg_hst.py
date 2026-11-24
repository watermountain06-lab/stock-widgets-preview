CIK = '0001070750'
BUILD = {}
# HST(호스트 호텔스 앤드 리조트) v2 카드 설정 — 자동 카드(AUTO), 정식. 회계연도 12월 31일. 리츠(REIT) — 미국 최대 숙박 리츠, 고급·최고급 호텔 약 70곳(UPREIT, Host Hotels & Resorts L.P.와 결합 공시).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-11-06 접수, 카드 기준일 11-20 종가), 실적 보도자료(8-K 2.02항 — 모두 장 마감 뒤 → 다음 세션).
# 엔진 입력(2026-11-22): 영업이익 = 보고 영업이익(매각 이익은 영업 밖 '기타 이익', 보험 정산 이익은 영업 안 — 9개월 $7M), 순이익 = Host Inc. 귀속,
#   설비투자 = 교체(9개월 $218M) + 투자형 개보수($174M) — 호텔 인수 제외, 차입금 = 총차입금 $5,084M(선순위채 $3,992M + 신용한도·기간 대출 $999M + 담보·기타 $93M),
#   비지배지분 = 상환 가능 OP 유닛 $211M + 기타 $4M, 우선주 없음. 이자비용 태그 InterestExpenseNonoperating(fetch_financials).
# 일회성(E54): 최근 4분기 Host 귀속 순이익 $936M(4분기 $135M + 1~9월 $801M, 희석 EPS 0.20+0.72+0.35+0.10 = 1.37). 처분 이익(FFO 조정표) 4분기 0, 1~9월 $235M(1분기 Four Seasons 두 곳 $242M) − 처분 세금 $5M,
#   손상 $12M(4분기 8 + 1~9월 4) — 이익 쪽 약 25%, 순액 약 23%. 콘도 분양 이익(4분기 $17M + 1~9월 약 $12M)·보험 정산 이익($7M)까지 넣어도 약 29%로 30% 아래라 정식(Fable r1 — 가장 넓게 매출총이익 기준이면 30.2%).
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, 1, -2), '적정~고평가'
CO = 'Host'
S_ = 'https://www.sec.gov/Archives/edgar/data/1070750/'
SEC = S_
TENQ = S_ + '000107075026000156/hst-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000107075026000152/hst-ex991.htm', 'q2': S_ + '000107075026000122/hst-ex991.htm',
      'q1': S_ + '000107075026000077/hst-ex991.htm', 'q4': S_ + '000107075026000038/hst-ex991.htm',
      'q3old': S_ + '000107075025000164/hst-ex991.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="hstFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). 리츠는 감가상각이 커서 PER이 높게 나온다 — PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])} — 코로나 저점 기준)</span>'
Y2 = (0, 30)
ACT_REASON = '리츠라 재고·매출채권 회전으로 보는 활동성이 잘 맞지 않는다'
NONOP_WHAT = '투자'
CAPEX_LABEL = '설비투자(교체·개보수)'   # 호텔 인수는 넣지 않는다
MODEL_NOTE = ('리츠는 건물 감가상각이 커서 GAAP 순이익이 실제 현금 창출보다 작게 나오고, 업계는 FFO(순이익에 부동산 감가상각을 되더하고 매각 이익을 뺀 값)로 본다 — 호스트의 2026년 NAREIT FFO 전망은 주당 $2.17(직전 중간값 $2.12)로 GAAP EPS 전망 $1.40보다 크다. 이 카드는 다른 카드와 같은 GAAP 배수로 본다. 사이트에는 리츠 전용 평가(FFO·순자산가치)가 아직 없다. '
              '최근 4분기 순이익 $936M(EPS $1.37)에는 2026년 1분기 Four Seasons 올랜도·잭슨홀 두 곳($1.1B) 매각 이익 $242M을 포함한 처분 이익 $235M(약 25%)이 들어 있다. 40채 한정인 올랜도 콘도 분양 이익(약 $29M)과 보험 정산 이익($7M)까지 넣으면 약 29%로, 사이트 기준(30%)에 가깝지만 아래라 정식 카드로 둔다. 처분 이익을 빼면 EPS는 약 $1.03으로 PER이 23배 안팎이 되고, 1분기 매각 이익이 최근 4분기에서 빠지는 2027년 1분기 실적 뒤에는 주가가 그대로여도 PER이 그만큼 오른다. 세법상 매각 이익 약 $500M은 2분기에 결의해 7월 15일 특별 배당(주당 $0.72)으로 지급해, 1~9월 배당 지급이 $1,007M으로 평소의 약 2배다. '
              '호스트는 호텔을 소유하고 운영은 Marriott 등 운영사에 맡기지만, 호텔 영업 매출(객실·식음료)을 그대로 연결 매출로 잡아 경기와 계절(1·2분기가 성수기)에 따라 크게 흔들린다. 보고 매출 증가율은 호텔을 사고판 영향이 섞여 있다 — 2026년 3분기 보고 매출은 1년 전보다 1.2% 늘었지만 매각으로 $80M이 빠졌고, 같은 호텔끼리 비교한 매출은 7.4%, 객실 매출(RevPAR)은 8.8% 늘었다. 10월에는 1 Hotel Brooklyn Bridge($202M)와 Renaissance Dallas at Plano($172M)를 샀다. 상환 가능 운영 파트너십 유닛($211M, 장부가)은 주주가치에서 뺀다. '
              '현금흐름 내재가치는 숫자보다 방향만 본다. 과거 5년 매출 성장률은 코로나로 매출이 크게 줄었던 2021년에서 출발해 회복분이 크고(2019년 대비로는 7년간 약 14%), 최근 설비투자가 감가상각보다 작아 엔진이 기본 시나리오에서 "성장에 돈이 거의 들지 않는다"는 높은 자본효율로 시작한다 — 그래서 기본 시나리오가 보수·낙관보다 크고 현재가 요구 성장률도 이 가정에 기댄다. 콘도 분양 매출을 빼면 최근 매출 증가가 2%에 못 미쳐 이 가정이 사라지고 기본값이 주당 몇 달러로 내려간다. 평균 자본효율로 보면 감가상각을 뺀 자본수익률이 할인율 10%보다 낮아 성장할수록 가치가 깎이고, 실제로는 법인세가 거의 없는데 5년 뒤 세율을 21%로 수렴시킨다. 어느 가정에서도 현금흐름 값은 현재가보다 낮다.')
HEALTH_EXTRA = '호텔 매입 자금을 무담보 채권으로 조달하는 리츠라 차입금 비중이 높게 나온다 — 리츠는 보통 부채를 자산 가치나 EBITDA 대비로 본다.'
PH = ['SPG', 'O', 'VICI', 'KIM', 'REG', 'PLD']
PEER_FILE = 'peer_universe/real_estate.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '리츠 6곳 PER 비교 (점수는 S&P500 부동산 기준)', 'pbr': '리츠 PBR 비교', 'psr': '리츠 PSR 비교',
                'pcr': '리츠 PCR(FCF) 비교', 'evebitda': '리츠 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 부동산 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 부동산 대비 배수 순위 (v2/peer_universe/real_estate.json)'
PEER_TIP = ('S&P500 부동산(HST 제외)과 배수 순위를 매긴 값이다.',
            '물류·데이터센터·의료·쇼핑몰·주택 리츠와 부동산 서비스가 섞여 있다. 호텔 리츠는 S&P500에 호스트뿐이라 차트에는 쇼핑몰·순임대·카지노 리츠 등 6곳이 보인다. 호텔은 영업 매출이 커 PSR이 임대 리츠보다 낮게 나온다.')
SEG = [('객실', 841, '#00205b'), ('식음료', 367, '#4a6fa5'), ('기타 호텔 매출', 132, '#8aa3c8'), ('콘도 분양', 7, '#b8c7e0')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 항목별'
NEWS_RANGE = '2025.11 ~ 2026.11'
NEWS = [
    ('red', '2026년 11월 4일 장 마감 뒤 — Q3 2026 실적', '2026-11-05',
     '희석 EPS $0.10(1년 전 $0.23은 매각 이익 포함) · NAREIT FFO $0.38(1년 전 $0.34) · 동일 호텔 RevPAR +8.8% · 2026년 FFO 전망 $2.17로 상향, 10월 호텔 2곳 $374M 인수 — 다음 날 주가 −5.7%', 'q3', 'Host 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 8월 5일 장 마감 뒤 — Q2 2026 실적', '2026-08-06',
     '희석 EPS $0.35 · NAREIT FFO $0.62 · 동일 호텔 RevPAR +7.0%(월드컵 효과) · 2026년 FFO 전망 $2.11~2.14로 상향 · 7월 특별 배당 $0.72 지급 — 다음 날 주가 −7.0%', 'q2', 'Host 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 5월 6일 장 마감 뒤 — Q1 2026 실적', '2026-05-07',
     '희석 EPS $0.72(Four Seasons 두 곳 $1.1B 매각 이익 $242M 포함) · NAREIT FFO $0.66 · 동일 호텔 RevPAR +4.4% · 특별 배당 $0.72 결의 — 다음 날 주가 0.0%', 'q1', 'Host 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 18일 장 마감 뒤 — 2025년 연간 실적', '2026-02-19',
     '4분기 희석 EPS $0.20 · NAREIT FFO $0.49(1년 전 $0.44) · 2025년 동일 호텔 RevPAR +3.8% · 호텔 2곳 $237M 매각 — 다음 날 주가 −0.9%', 'q4', 'Host 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 11월 5일 장 마감 뒤 — Q3 2025 실적', '2025-11-06',
     '희석 EPS $0.23(매각 이익 포함) · NAREIT FFO $0.34 · 동일 호텔 RevPAR +0.2% — 다음 날 주가 +6.8%', 'q3old', 'Host 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 21, 'nt': 17, 'mean': 26.16, 'median': 27, 'low': 23, 'high': 28, 'sb': 11, 'b': 1, 'h': 9, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-23'
POST = [r"""
h = h.replace('Q3 2026 10-Q 부문 표 (SEC)', 'Q3 2026 10-Q 매출 주석 (SEC)')
h = h.replace('· GAAP 기준 · FCF는 영업현금흐름 − 설비투자(교체·개보수) ·', '· GAAP 기준(매각 이익은 영업 밖) · FCF는 영업현금흐름 − 설비투자(교체·개보수) ·')
import re as _rh
h = _rh.sub(r'잔존가치\(5년 뒤\)가 내재가치의 ([0-9]+)%', r'잔존가치(5년 뒤)가 영업 기업가치의 \1%', h)
h = h.replace('`잔존가치(5년 뒤)가 내재가치의 ${', '`잔존가치(5년 뒤)가 영업 기업가치의 ${')
h = h.replace('FCF(최근 4분기 $1.2B)가 배당 지급(연 환산 약 $1.3B)을 넘는지', 'FCF(최근 4분기 $1.2B)가 배당 지급(연 환산 약 $1.3B — 7월 특별 배당 $0.72 포함, 정기 배당만이면 그 절반 수준)을 넘는지')
h = h.replace('Q3 2026 매출 +1.2%(보고 기준, 3년 연평균 5.9%).', 'Q3 2026 매출 +1.2%(보고 기준, 3년 연평균 5.9%) — 호텔 매각으로 $80M이 빠진 값이고 같은 호텔끼리는 +7.4%.')
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
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "srt:ProductOrServiceAxis",
 "extra": {},
 "members": {"us-gaap:OccupancyMember": ["객실", "#00205b"],
             "us-gaap:FoodAndBeverageMember": ["식음료", "#4a6fa5"],
             "us-gaap:HotelOtherMember": ["기타 호텔 매출", "#8aa3c8"],
             "us-gaap:HomeBuildingMember": ["콘도 분양", "#b8c7e0"]},
 "ignore": ["srt:HotelMember"]
}
