CIK = '0000920522'
BUILD = {'overlay': True, 'company_tags': [('ess:RevenueGeneratingCapitalExpenditures', 'CapexRentalEss', '2020-01-01'), ('ess:RedevelopmentExpenditures', 'RedevelopEss', '2020-01-01'), ('ess:LinesOfCreditAndCommercialPaper', 'CreditLinesEss', '2020-01-01')]}   # Q3 2026 10-Q가 요약 자료에 늦음(Essex Portfolio L.P. 결합 공시) — 인라인 XBRL 보충
# ESS(에섹스 프로퍼티 트러스트) v2 카드 설정 — 자동 카드(AUTO), 정식. 회계연도 12월 31일. 리츠(REIT) — 미국 서부 해안(남·북 캘리포니아, 시애틀) 임대 아파트(UPREIT).
# 출처: SEC XBRL + 인라인 XBRL 보충(Q3 2026 10-Q 2026-10-28 접수, 카드 기준일 11-20 종가), 실적 보도자료(8-K 2.02항 — 모두 장 마감 뒤 → 다음 세션).
# 엔진 입력(2026-11-22): 영업이익 = 보고 "Earnings from operations" − 부동산·토지 매각 이익(DERIVED_OPINC), 순이익 = 보통주 귀속(EXTRA_TAGS·PREFER_TAGS),
#   설비투자 = 임대 단지 설비(9개월 $87.1M) + 재개발($49.8M) — 개발 $65.1M·인수 제외, 차입금 = 무담보 $5,844.7M + 담보 $761.1M = $6,605.8M,
#   비지배지분 = $160.9M + 상환 가능 $26.1M, 운용리스 $31.8M, 우선주 없음. 4분기 EPS 2025는 보도자료 값(1.25).
# 일회성(E54): 최근 4분기 보통주 순이익 $347.3M(4분기 $80.6M + 1~9월 $266.7M, 희석 EPS 1.25+1.65+0.97+1.52 = 5.39). 회사 FFO·Core FFO 조정 항목을 분기별로 —
#   분기별로 더하면 비용 쪽 $95.7M(27.6% — 2분기 RealPage 등 소송 합의 $55.8M 포함 일반관리비 조정, 손상 $23.3M, 세금 등), 이익 쪽 $48.8M(14.0% — 매각 이익 $23.8M, 기술 합작 지분 이익 등) — 모두 30% 아래라 정식(4분기 통산 상계면 26.3%·12.8%, Codex·Fable r1).
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, -2), '적정~고평가'
CO = 'Essex'
S_ = 'https://www.sec.gov/Archives/edgar/data/920522/'
SEC = S_
TENQ = S_ + '000092052226000030/ess-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
_E = 'https://www.sec.gov/Archives/edgar/data/920522/'
PR = {'q3': _E + '000114036126040903/ef20084268_ex99-1.htm', 'q2': _E + '000114036126030060/ef20078746_ex99-1.htm',
      'q1': _E + '000114036126017477/ef20071359_ex99-1.htm', 'q4': _E + '000114036126003709/ef20064474_ex99-1.htm',
      'q3old': _E + '000114036125039716/ef20057734_ex99-1.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="essFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). 리츠는 감가상각이 커서 PER이 높게 나온다 — PER만으로 낸 범위라 판정과 따로 읽는다. 최근 1년 PER 구간에는 2025년 매각 이익이 컸던 시기가 섞여 있다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 50)
ACT_REASON = '리츠라 재고·매출채권 회전으로 보는 활동성이 잘 맞지 않는다'
NONOP_WHAT = '투자'
CAPEX_LABEL = '설비투자(임대 단지 설비·재개발)'   # 개발·인수 지출은 넣지 않는다
MODEL_NOTE = ('리츠는 건물 감가상각이 커서 GAAP 순이익이 실제 현금 창출보다 작게 나오고, 업계는 FFO(순이익에 부동산 감가상각을 되더하고 매각 이익을 뺀 값)로 본다 — 에섹스의 2026년 Core FFO 전망은 주당 $16.10~16.22(중간값 $0.02 상향)로 GAAP EPS 전망 $5.62~5.74의 약 2.8배다. 이 카드는 다른 카드와 같은 GAAP 배수로 보므로 PER이 높게 나온다. 사이트에는 리츠 전용 평가(FFO·순자산가치)가 아직 없다. 현금흐름 내재가치는 이 모델의 가정에서 0 이하로 나온다 — 감가상각을 뺀 영업이익을 장부 투하자본에 비춰 보면 자본수익률이 할인율 10%보다 낮아 성장할수록 가치가 깎이고, 실제로는 법인세가 거의 없는데 5년 뒤 세율을 일반 기업 21%로 수렴시키며, 거기서 순차입금·비지배지분을 뺀다. 종합 판정의 −2는 이 현금흐름 칸에서만 나왔고, 동종업 점수는 PCR 한 칸에 기대어 경계(0표) 가까이에 있다. '
              '2025년에는 부동산 매각 이익이 커서(1~9월 $300M) 그때 PER이 낮았고, 2026년에는 매각 이익이 작아져 GAAP EPS가 줄었다 — 그래서 지금 PER이 5년 이력의 높은 쪽에 있고, 최근 1년 PER 구간으로 낸 적정주가 범위의 아래쪽도 그 시기 낮은 PER에서 나온다. 같은 기간 Core FFO는 소폭 늘었다. 최근 4분기 순이익에는 비용 쪽으로 2026년 2분기 RealPage 관련 소송 등 합의금 $55.8M과 손상 $23.3M(연결 단지 $10.7M + 합작 $12.6M), 이익 쪽으로 매각 이익 $23.8M(연결 $8.8M + 합작 몫 $15.0M)과 기술 합작 지분 이익이 들어 있다(회사 조정 항목을 분기별로 더하면 비용 쪽 약 28%, 이익 쪽 약 14%로 둘 다 30% 아래). 합의금은 법원 승인 전이라 아직 지급하지 않아 최근 4분기 FCF에는 빠지지 않았다. '
              '영업이익은 회사가 보고한 영업이익에서 연결 부동산·토지 매각 이익을 뺀 값이다(합의금이 든 일반관리비와 연결 단지 손상은 영업이익 안에 남는다 — 3분기 손상 $10.7M은 Marina City Club 처분 관련이다). 지역 부문 매출 증가율에는 2025년 인수 단지가 들어 있다. FCF의 설비투자는 기존 단지 설비와 재개발만 넣었고 신규 개발(1~9월 $65M)과 인수는 넣지 않았다. 운영 파트너십 유닛 등 비지배지분($161M)과 상환 가능 비지배지분($26M)은 장부가로 주주가치에서 뺀다.')
HEALTH_EXTRA = '아파트 매입·개발 자금을 채권으로 조달하는 리츠라 차입금 비중이 높게 나온다 — 리츠는 보통 부채를 자산 가치나 EBITDA 대비로 본다.'
PH = ['EQR', 'AVB', 'MAA', 'CPT', 'UDR', 'INVH']
PEER_FILE = 'peer_universe/real_estate.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '아파트 리츠 6곳 PER 비교 (점수는 S&P500 부동산 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 부동산 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 부동산 대비 배수 순위 (v2/peer_universe/real_estate.json)'
PEER_TIP = ('S&P500 부동산(ESS 제외)과 배수 순위를 매긴 값이다.',
            '물류·데이터센터·의료·쇼핑몰·주택 리츠와 부동산 서비스가 섞여 있다. 차트에는 아파트·단독주택 임대 리츠 6곳이 보인다.')
SEG = [('북부 캘리포니아', 208.6, '#7a1f2b'), ('남부 캘리포니아', 195.1, '#b85c66'), ('시애틀', 79.7, '#e8c4c8'), ('기타(부문 외 부동산·임대료 조정·관리 수수료)', 9.2, '#d9d9d9')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 지역 부문'
NEWS_RANGE = '2025.10 ~ 2026.11'
NEWS = [
    ('red', '2026년 10월 27일 장 마감 뒤 — Q3 2026 실적', '2026-10-28',
     '희석 EPS $1.52(1년 전 $2.56은 매각 이익 포함) · Core FFO $4.00(1년 전 $3.97) · 동일 단지 매출 +3.0% · 2026년 Core FFO 전망 $16.10~16.22(중간값 +$0.02) · 단지 3곳 매각(회사 지분 기준 $112M) — 다음 날 주가 −4.9%', 'q3', 'Essex 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 7월 29일 장 마감 뒤 — Q2 2026 실적', '2026-07-30',
     '희석 EPS $0.97(RealPage 등 소송 합의금 $55.8M 포함) · Core FFO $4.08(1년 전 $4.03) · 2026년 Core FFO 전망 상향(중간값 +$0.20), GAAP EPS 전망은 합의금 탓에 중간값 −$0.29 — 다음 날 주가 −5.0%', 'q2', 'Essex 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 28일 장 마감 뒤 — Q1 2026 실적', '2026-04-29',
     '희석 EPS $1.65(1년 전 $3.16은 매각 이익 포함) · Core FFO $4.06(1년 전 $3.97) · 동일 단지 매출 +2.9% — 다음 날 주가 −1.1%', 'q1', 'Essex 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 4일 장 마감 뒤 — 2025년 연간 실적', '2026-02-05',
     '4분기 희석 EPS $1.25(1년 전 $4.00은 매각·재측정 이익 포함) · Core FFO $3.98 · 2025년 Core FFO $15.94(+2.2%) — 다음 날 주가 −0.4%', 'q4', 'Essex 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 10월 29일 장 마감 뒤 — Q3 2025 실적', '2025-10-30',
     '희석 EPS $2.56(매각 이익 포함) · Core FFO $3.97(1년 전 $3.91) · 동일 단지 매출 +2.7% — 다음 날 주가 +1.1%', 'q3old', 'Essex 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 26, 'nt': 19, 'mean': 298.08, 'median': 295, 'low': 279, 'high': 330, 'sb': 4, 'b': 6, 'h': 14, 's': 1, 'ss': 1}
ANALYST_ASOF = '2026-11-23'
POST = [r"""
h = h.replace('· GAAP 기준 · FCF는 영업현금흐름 − 설비투자(임대 단지 설비·재개발) ·', '· GAAP 기준(영업이익은 부동산·토지 매각 이익 제외) · FCF는 영업현금흐름 − 설비투자(임대 단지 설비·재개발) ·')
h = h.replace('합성 영업이익률(세전이익 기준)', '카드 기준 영업이익률(매각 이익 제외)').replace('합성 영업이익(세전이익 기준)', '카드 기준 영업이익(매각 이익 제외)')
h = h.replace('Q3 2026 10-Q 부문 표 (SEC)', 'Q3 2026 10-Q 부문 주석 (SEC)')
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
 "concepts": ["us-gaap:OperatingLeaseLeaseIncome"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"ess:NorthernCaliforniaMember": ["북부 캘리포니아", "#7a1f2b"],
             "ess:SouthernCaliforniaMember": ["남부 캘리포니아", "#b85c66"],
             "ess:SeattleMetroMember": ["시애틀", "#e8c4c8"]},
 "ignore": [],
 "remainder": ["기타(부문 외 부동산·임대료 조정·관리 수수료)", "#d9d9d9", 0.019]
}
