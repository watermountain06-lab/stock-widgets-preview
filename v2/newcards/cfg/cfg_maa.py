CIK = '0000912595'
BUILD = {'overlay': True, 'company_tags': [('us-gaap:PaymentsForCapitalImprovements', 'CapexImprovementsMaa', '2022-01-01')]}   # Q2·Q3 10-Q가 요약 자료에 늦음(Mid-America Apartments LP 결합 공시) — 인라인 XBRL 보충
# MAA(미드아메리카 아파트먼트) v2 카드 설정 — 자동 카드(AUTO), 정식. 회계연도 12월 31일. 리츠(REIT) — 미국 남동·남서부(선벨트) 임대 아파트(UPREIT, Mid-America Apartments L.P.와 결합 공시).
# 출처: SEC XBRL + 인라인 XBRL 보충(Q2·Q3 2026 10-Q 요약 자료 미반영 — Q3 10-Q 2026-10-29 16:15 동부 접수, 카드 기준일 11-20 종가), 실적 보도자료(8-K 2.02항 — 모두 장 마감 뒤 16:15 동부 → 다음 세션).
# 엔진 입력(2026-11-21): 영업이익 = 세전이익 + 이자 − 부동산 매각 이익 − 기타 영업외 수익(DERIVED_OPINC — 손익계산서에 영업이익 줄이 없다) = 매출 − 부동산 운영비용(감가상각 포함) − 관리비 − 일반관리비,
#   순이익 = 보통주 귀속(EXTRA_TAGS·PREFER_TAGS), 설비투자 = 기존 부동산 개량(9개월 $275.7M — 개발 $213.8M·인수 $59.1M 제외), 차입금 = 무담보 $5,478.8M + 담보 $360.5M = $5,839.3M,
#   비지배지분 = 운영 파트너십 유닛 $132.1M + 연결 부동산 법인 $11.8M, 우선주 없음(Series I 2026-10-01 상환). 감가상각 = 손익계산서 기준(EXCLUDE_TAGS). 4분기 EPS 2024·2022·2020은 보도자료 값.
# 일회성(E54): 최근 4분기 보통주 귀속 순이익 $384.0M(4분기 $56.6M + 1~9월 $327.3M, 희석 EPS 0.48+1.06+1.04+0.72 = 3.30). 회사가 FFO·Core FFO에서 빼는 항목 —
#   분기별로 나눈 회사 조정 항목: 이익 약 $79.5M(20.7% — 매각 이익 $55.6M, 투자 이익 등), 비용 약 $62.8M(16.4% — 4분기 RealPage 합의 등 $53.0M, 우선주 내재 파생·재해 등), 순액 이익 약 $16.6M(4.3%) — 모두 30% 아래라 정식.
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, 0, -2), '적정~고평가'
CO = 'MAA'
S_ = 'https://www.sec.gov/Archives/edgar/data/912595/'
SEC = S_
TENQ = S_ + '000119312526437813/maa-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000119312526436173/maa-ex99_1.htm', 'q2': S_ + '000119312526323756/maa-ex99_1.htm',
      'q1': S_ + '000119312526191620/maa-ex99_1.htm', 'q4': S_ + '000119312526037610/maa-ex99_1.htm',
      'q3old': S_ + '000119312525256342/maa-ex99_1.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="maaFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). 리츠는 감가상각이 커서 PER이 높게 나온다 — PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 50)
ACT_REASON = '리츠라 재고·매출채권 회전으로 보는 활동성이 잘 맞지 않는다'
NONOP_WHAT = '투자'
CAPEX_LABEL = '설비투자(기존 부동산 개량)'   # 개발·인수 지출은 넣지 않는다
MODEL_NOTE = ('리츠는 건물 감가상각이 커서 GAAP 순이익이 실제 현금 창출보다 작게 나오고, 업계는 FFO(순이익에 부동산 감가상각을 되더하고 매각 이익을 뺀 값)로 본다 — MAA의 2026년 연간 Core FFO 전망은 주당 $8.43~8.55(직전 $8.41~8.65)로 지난 4분기 GAAP EPS($3.30)의 약 2.6배다(전망과 지난 실적이라 기간은 다르다). 이 카드는 다른 카드와 같은 GAAP 배수로 보므로 PER이 높게 나온다. 사이트에는 리츠 전용 평가(FFO·순자산가치)가 아직 없고, 현금흐름 내재가치가 0 이하인 것은 모델 구조 탓이다 — 감가상각을 뺀 영업이익을 장부 투하자본에 비춰 보면 자본수익률이 할인율 10%보다 낮아 성장할수록 가치가 깎이고, 실제로는 법인세가 거의 없는데 5년 뒤 세율을 일반 기업 21%로 수렴시키며, 거기서 순차입금·비지배지분을 뺀다(할인율 10%에서는 성장이 없어도 사업 가치가 순차입금 수준에 그친다). '
              '손익계산서에 영업이익 줄이 없어 영업이익은 매출에서 부동산 운영비용(감가상각 포함)·관리비·일반관리비를 뺀 값으로 쓴다 — 이자·매각 이익·기타 영업외 손익은 밖이다. 최근 4분기 순이익에는 매각 이익 $56M과 투자 이익 $17M, 2025년 4분기 소송 비용·합의 $53M이 함께 들어 있다(회사 조정 항목을 분기별로 나눠 보면 이익 쪽 약 21%, 비용 쪽 약 16%, 순액 약 4%). '
              'FCF의 설비투자는 기존 단지 개량 지출만 넣었고 신규 개발(1~9월 $214M)과 인수($59M)는 넣지 않았다 — 현금흐름 모델의 재투자는 실제 지출이 아니라 매출 증가 ÷ 매출/투하자본으로 따로 추정한다. 운영 파트너십 유닛($132M, 장부가)과 연결 부동산 법인의 비지배지분($12M)은 주주가치에서 뺀다. Series I 우선주($43M)는 2026년 10월 1일 모두 상환해 넣지 않았다.')
HEALTH_EXTRA = '아파트 매입·개발 자금을 채권으로 조달하는 리츠라 차입금 비중이 높게 나온다 — 리츠는 보통 부채를 자산 가치나 EBITDA 대비로 본다.'
PH = ['EQR', 'AVB', 'CPT', 'ESS', 'UDR', 'INVH']
PEER_FILE = 'peer_universe/real_estate.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '아파트 리츠 6곳 PER 비교 (점수는 S&P500 부동산 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 부동산 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 부동산 대비 배수 순위 (v2/peer_universe/real_estate.json)'
PEER_TIP = ('S&P500 부동산(MAA 제외)과 배수 순위를 매긴 값이다.',
            '물류·데이터센터·의료·쇼핑몰·주택 리츠와 부동산 서비스가 섞여 있다. 차트에는 아파트·단독주택 임대 리츠 6곳이 보인다.')
# 매출(Q3 2026 10-Q 부문 주석): 동일 점포 519.1 + 그 외(신규·개발 단지 등) 41.1 = 560.1(반올림 0.1). 1년 전은 부문 기준이 해마다 바뀐다(동일 점포 재분류).
SEG = [('동일 점포 단지', 519.1, '#e07b24'), ('그 외 단지(신규·개발 등)', 41.1, '#f7d6b5')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 동일 점포 기준 부문'
NEWS_RANGE = '2025.10 ~ 2026.11'
NEWS = [
    ('neutral', '2026년 10월 28일 장 마감 뒤 — Q3 2026 실적', '2026-10-29',
     '보통주 순이익 $83M · 희석 EPS $0.72(1년 전 $0.84) · Core FFO $2.10(1년 전 $2.16) · 2026년 Core FFO 전망 $8.43~8.55(직전 $8.41~8.65, 중간값 −$0.04) · GAAP EPS 전망 $3.61~3.73으로 하향(직전 $3.96~4.20) — 다음 날 주가 +1.3%', 'q3', 'MAA 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 7월 29일 장 마감 뒤 — Q2 2026 실적', '2026-07-30',
     '희석 EPS $1.04(1년 전 $0.92, 매각 이익 포함) · Core FFO $2.08(1년 전 $2.15) — 다음 날 주가 −3.0%', 'q2', 'MAA 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 29일 장 마감 뒤 — Q1 2026 실적', '2026-04-30',
     '희석 EPS $1.06(매각 이익 포함, 1년 전 $1.54도 매각 이익 $72M 포함) · Core FFO $2.13(1년 전 $2.20) — 다음 날 주가 −0.4%', 'q1', 'MAA 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 2월 4일 장 마감 뒤 — 2025년 연간 실적', '2026-02-05',
     '4분기 보통주 순이익 $57M · 희석 EPS $0.48(RealPage 임대료 담합 집단소송 합의 등 $53M 비용 포함 · 1년 전 $1.42는 매각 이익 $55M 포함) · Core FFO $2.23(1년 전과 같음) · 2025년 Core FFO $8.74 — 다음 날 주가 −3.2%', 'q4', 'MAA 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 10월 29일 장 마감 뒤 — Q3 2025 실적', '2025-10-30',
     '희석 EPS $0.84(1년 전 $0.98) · Core FFO $2.16(1년 전 $2.21) — 다음 날 주가 +2.0%', 'q3old', 'MAA 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 26, 'nt': 20, 'mean': 135.3, 'median': 134, 'low': 122, 'high': 155, 'sb': 7, 'b': 1, 'h': 15, 's': 2, 'ss': 1}
ANALYST_ASOF = '2026-11-21'
POST = [r'''
h = h.replace('순차입금(리스 포함)', '순차입금').replace('차입금·리스 $', '차입금 $')
h = h.replace('· GAAP 기준 · FCF는 영업현금흐름 − 설비투자(기존 부동산 개량) ·', '· GAAP 기준(영업이익은 이자·매각 이익·기타 영업외 제외 합성) · FCF는 영업현금흐름 − 설비투자(기존 부동산 개량) ·')
import re as _rp
h = _rp.sub(r'PER ([0-9.]+)배\(5년 중앙값 ([0-9.]+)배\)로 자기 이력', r'PER은 \1배로 5년 중앙값(\2배)보다 높지만 PSR·PBR·EV/EBITDA가 5년 바닥권이라 자기 이력', h)
h = h.replace('합성 영업이익률(세전이익 기준)', '합성 영업이익률(이자·매각 이익 제외)').replace('합성 영업이익(세전이익 기준)', '합성 영업이익(이자·매각 이익 제외)')
''']

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
 "extra": {},
 "members": {"maa:SameStoreMember": ["동일 점포 단지", "#e07b24"],
             "maa:NonSameStoreAndOtherMember": ["그 외 단지(신규·개발 등)", "#f7d6b5"]},
 "ignore": []
}
