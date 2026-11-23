CIK = '0000072741'
BUILD = {'overlay': True}
# ES(에버소스 에너지) v2 카드 설정 — 자동 카드(AUTO), 정식. 회계연도 12월 31일. 코네티컷·매사추세츠·뉴햄프셔 규제 전력 배전·송전, 가스 배전(수도 Aquarion은 2026-06-30 매각).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-11-06 14:07 동부 접수, 카드 기준일 11-18 종가), 실적 보도자료(8-K 2.02항 — 모두 장 마감 뒤 16:1x~16:2x 동부 → 다음 날).
# 요약 자료 누락: SEC companyfacts가 Q3 2026 10-Q를 아직 싣지 않아 인라인 XBRL 보충(BUILD overlay, preflight OVERLAY_OK)으로 만든다. 이 10-Q는 희석 EPS 태그가 기본 EPS 태그 안에 겹쳐 있어
#   보충 도구가 겹친 태그도 읽게 했다(ixbrl_supplement NESTED_CIKS — ES만, 2026-11-19).
# 엔진 입력(2026-11-19): 순이익 = 보통주 귀속(NetIncomeLoss 2023 멈춤 — EXTRA_TAGS), 단기투자 제외(2015 낡은 값)·비지배지분 = 자회사 우선주 $155.6M(EV_TAGS).
#   차입금 = 1년 안 $2,875M + 장기 $26,023M = $28,898M(어음 0). 해상풍력 우발부채(유동 $409M)는 차입금에 넣지 않았다.
# 일회성(E54): 최근 4분기 GAAP 희석 EPS 3.79(1.12 + 1.61 + 0.14 + 0.92) 대 회사 비GAAP 4.64(1.12 + 1.73 + 0.87 + 0.92) — 조정 0.85(22%),
#   모두 비용(해상풍력 우발부채 증가 0.43·Aquarion 매각 손실 0.30·FERC 환급 0.12) → 30% 미만이라 정식. 회사가 빼지 않은 Q3 폭풍 비용 불인정($40.8M 세전, 주당 약 0.08)을 더해도 약 24.5%(Fable r1).
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 1, -2), '적정~고평가'
CO = 'Eversource'
S_ = 'https://www.sec.gov/Archives/edgar/data/72741/'
SEC = S_
TENQ = S_ + '000162828026071541/es-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000110465926122703/tm2628949d1_ex99-1.htm', 'q2': S_ + '000110465926088698/tm2621633d1_ex99-1.htm',
      'q1': S_ + '000110465926056267/tm2613673d1_ex99-1.htm', 'q4': S_ + '000110465926014302/tm266120d1_ex99-1.htm',
      'aquarion': S_ + '000110465926079426/tm2619364d1_ex99-1.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="esFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). EPS에 비GAAP 제외 비용 주당 85센트가 들어 있다. PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 30)
ACT_REASON = '유틸리티라 재고·매출채권 회전으로 보는 활동성이 잘 맞지 않는다'
NONOP_WHAT = '투자'
MODEL_NOTE = ('최근 4분기 GAAP EPS($3.79)에는 회사가 비GAAP에서 빼는 비용이 주당 85센트 들어 있다 — 2024년 9월 해상풍력(South Fork·Revolution Wind) 매각 때 진 우발부채를 2026년 2분기에 늘린 $0.43, 같은 분기 수도 회사 Aquarion 매각 손실 $0.30, 1분기 FERC 송전 자기자본이익률 인하(10.57% → 9.57%)에 따른 환급 $0.12다. GAAP 이익의 약 22%라 카드는 GAAP 그대로 쓴다. '
              'Aquarion은 6월 30일 약 $2.4B(종결 때 상환하거나 매수자에게 넘긴 장기차입금 약 $650M 포함)에 매각됐고 순수입 약 $1.7B는 차입금 상환에 쓴다. 3분기 매출 감소 $242M 가운데 $69M만 Aquarion 제외분이고, 나머지는 주로 이익에 영향이 없는 전가(추적) 매출 감소다 — 요금 기준 매출은 전력 +$24M, 가스 +$27M 늘었다. '
              '해상풍력 우발부채는 2024년 매각 손실 뒤 2025년 3분기($0.20)·2026년 2분기($0.43)에 늘었고, 2027년 정산 때 더 늘 수 있다(별도 보증 최대 $972M). 유동 $409M은 차입금에 넣지 않았다(넣어도 현금흐름 값은 0 이하 그대로). '
              '송배전 설비투자가 감가상각보다 훨씬 커서 큰 차입금을 뺀 현금흐름 모델의 값이 낮게 나온다 — 규제 유틸리티는 그 투자가 요금 기준 자산이 되어 이익으로 돌아오는 구조라 현금흐름 모델과 PCR은 의미가 약하다. '
              '코네티컷 규제 당국과의 관계가 주가에 크게 작용한다 — 2025년 11월 규제 당국(PURA)이 Aquarion 매각을 거부한 주에 주가가 하루(11월 19일) −12.4% 빠졌다(2026년 3월 승인). 판정 등급은 유틸리티에 잘 맞지 않는 현금흐름 칸(−2)에 달려 있다.')
HEALTH_EXTRA = '설비투자 자금을 사채·신주로 조달하는 구조라 차입금 비중이 높게 나온다 — 규제 유틸리티에서는 흔한 모습이다.'
# 현금흐름 0 이하 보정 — ED·SO와 같은 POST
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
h = _re.sub(r'(id="esDcfReq"[^>]*>)연 -[0-9.]+%', lambda m: m.group(1) + '해석 부적합', h)
h = _re.sub(r'현재가를 정당화하려면 매출이 5년간 연 [−-][0-9.]+% 커야 한다\. ', '현금흐름 값이 0 이하라 현재가 요구 성장률은 해석할 수 없다. ', h)
''']
# 헤더 '현재가 요구 성장' 칸 — 현금흐름 값이 0 이하이면 숫자 대신 '해석 부적합'(AEE Fable r1, 2026-10-25)
POST.append(r'''
h = h.replace("  if (req && price != null) {", "  if (req && d.base <= 0) { req.textContent = '해석 부적합'; req.style.color = 'var(--text3)'; const _c = req.closest('.meta-item'); if (_c) _c.title = '해석 부적합(현금흐름 0 이하) — 현금흐름 내재가치가 0 이하라 현재가 요구 성장률을 해석할 수 없다.'; }\n  if (req && price != null && d.base > 0) {", 1)
import re as _re2
h = _re2.sub(r'(id="esDcfReq"[^>]*>)연 [−-][0-9.]+%', lambda m: m.group(1) + '해석 부적합', h)
''')
PH = ['NEE', 'DUK', 'SO', 'AEP', 'ED', 'EIX']
PEER_FILE = 'peer_universe/utilities.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '유틸리티 6곳 PER 비교 (점수는 S&P500 유틸리티 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 유틸리티 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 유틸리티 대비 배수 순위 (v2/peer_universe/utilities.json)'
PEER_TIP = ('S&P500 유틸리티(ES 제외)와 배수 순위를 매긴 값이다.',
            '규제 전력·가스, 독립 발전사, 수도가 섞여 있다. 차트에는 유틸리티 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문): 전력 배전 2,599.7 + 전력 송전 568.1 + 가스 배전 265.4 = 3,433.2, 본사·기타 458.8 − 부문 간 제거 913.1 = −454.3 → 2,978.9.
SEG = [('전력 배전', 2599.7, '#0b3b70'), ('전력 송전', 568.1, '#7ac142'), ('가스 배전', 265.4, '#5b8db8')]
SEG_ADJ = -454.3
SEG_ADJ_LABEL = '본사·기타 − 부문 간 제거'
SEG_TITLE = '매출 구성 — 부문별'
NEWS_RANGE = '2026.02 ~ 2026.11'
NEWS = [
    ('neutral', '2026년 11월 4일 장 마감 뒤 — Q3 2026 실적', '2026-11-05',
     '희석 EPS $0.92(1년 전 GAAP $0.99·비GAAP $1.19, 이번 분기 조정 없음) · 2026년 비GAAP EPS 전망을 $4.62~4.70으로 좁힘(연초 $4.80~4.95) · 2030년까지 연 5~7% 성장 목표 유지 — 다음 날 주가 +2.1%', 'q3', 'Eversource 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 7월 30일 장 마감 뒤 — Q2 2026 실적', '2026-07-31',
     '희석 EPS $0.14(해상풍력 우발부채 증가 $0.43·Aquarion 매각 손실 $0.30) · 비GAAP EPS $0.87 — 다음 날 주가 −3.0%', 'q2', 'Eversource 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 6월 30일 — 수도 회사 Aquarion 매각 완료', '2026-07-01',
     '매각가 약 $2.4B(종결 때 상환하거나 매수자에게 넘긴 장기차입금 약 $650M 포함), 순수입 약 $1.7B는 차입금 상환에 — 다음 날 주가 −0.1%', 'aquarion', 'Eversource 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 5월 6일 장 마감 뒤 — Q1 2026 실적', '2026-05-07',
     '희석 EPS $1.61(1년 전 $1.50, FERC 환급 $0.12 포함) · 비GAAP EPS $1.73 — 다음 날 주가 −2.2%', 'q1', 'Eversource 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 12일 장 마감 뒤 — 2025년 연간 실적', '2026-02-13',
     '4분기 희석 EPS $1.12(1년 전 $0.20은 Aquarion 손실 $0.81 포함, 비GAAP $1.01) · 2025년 희석 EPS $4.56, 비GAAP $4.76 — 다음 날 주가 +4.3%', 'q4', 'Eversource 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 17, 'nt': 10, 'mean': 72.7, 'median': 74, 'low': 59, 'high': 81, 'sb': 4, 'b': 0, 'h': 10, 's': 2, 'ss': 1}
ANALYST_ASOF = '2026-11-23'


AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"es:EversourceElectricDistributionMember": ["전력 배전", "#0b3b70"], "es:EversourceElectricTransmissionMember": ["전력 송전", "#7ac142"], "es:NaturalGasDistributionMember": ["가스 배전", "#5b8db8"]},
 "ignore": ["es:WaterDistributionSegmentMember", "es:EversourceWaterMember"]
}
