# TTWO(테이크투 인터랙티브) v2 카드 설정 — 자동 카드(AUTO). 회계연도 3월 31일. 게임(Rockstar — GTA·Red Dead, 2K — NBA 2K, Zynga 모바일).
# 출처: SEC XBRL, Q1 FY27 10-Q(2026-08-07), 실적 보도자료(Q2 FY26~Q1 FY27, 8-K 2.02항 — Q2~Q4 FY26은 장 마감 뒤, Q1 FY27은 장 전), 8-K(Xbox 라이선스 2026-09-30), StockAnalysis. 사전 조사 자료표 scratchpad pre/TTWO.md.
# 엔진 입력(2026-10-24): D&A = 감가상각 + 무형자산 상각·손상(회사 고유 태그 → company_tags·DDA_PARTS_BY_CIK — 빠지면 EV/EBITDA 1,120배).
# 최근 4분기 모두 GAAP 적자라 PER이 없다. 과거 영업이익에 영업권 손상(FY24 Q4 $2.18B, FY25 Q4 $3.55B)이 들어 있어 이익률 중앙값이 크게 음수다 — 일회성을 빼는 장치(안건 E54)는 보류(사용자 결정).
BUILD = {'company_tags': [('ttwo:AmortizationAndImpairmentOfIntangibleAssets', 'AmortizationAndImpairmentOfIntangibleAssetsTtwo')]}
CIK = '0000946581'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q1 FY27', 'Q1 FY26', 'Q4 FY26'
L8 = ['Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26', 'Q4 FY26', 'Q1 FY27']
FY_ENDS, FY_LABEL = ('2026-03-31', '2025-03-31'), 'FY2026'
VOTES, VERDICT = (0, -1, -2), '고평가'
CO = 'Take-Two'
S_ = 'https://www.sec.gov/Archives/edgar/data/946581/'
SEC = S_
TENQ = S_ + '000162828026054870/ttwo-20260630.htm'; TENQ_NAME = 'Q1 FY27 10-Q'
PR = {'q1': S_ + '000162828026054580/ttwo1q27earningsrelease.htm', 'q4': S_ + '000162828026037260/ttwo4q26earningsrelease.htm',
      'q3': S_ + '000162828026005010/ttwo3q26earningsrelease.htm', 'q2': S_ + '000162828025050182/ttwo2q26earningsrelease.htm'}
LINKS = {'xbox': S_ + '000162828026064001/ttwo-20260928.htm'}
FAIRBAND_TITLE = 'id="ttwoFairBand" title="최근 4분기 GAAP 순이익이 적자라 PER 기준 적정주가 밴드를 만들 수 없다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (-20, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
# 고정 문장.
MODEL_NOTE = ('최근 4분기 모두 GAAP 적자라 PER은 없다. 과거 영업이익에는 Zynga 인수에서 생긴 영업권·무형자산 손상(수십억 달러)이 들어 있어, '
              '과거 이익률에서 출발하는 현금흐름 모델이 그만큼 나쁘게 나온다(손상을 빼고 계산해도 현금흐름 값은 0 이하로 판정은 같다) — 일회성을 빼는 장치는 아직 없다. '
              '매출원가 안의 인수 무형자산 상각이 커서 GAAP 이익을 낮춘다. 회사가 앞세우는 순예약(Net Bookings)은 이익이 아니라 판매 지표이고, GAAP 매출과는 수익 인식 시점이 달라 차이가 난다. '
              'GTA VI(11월 19일 출시 예정)가 나오면 FY27 하반기 숫자가 과거와 비교하기 어려워진다.')
# 현금흐름 0 이하 — SO와 같은 문구 보정
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
h = _re.sub(r'(id="ttwoDcfReq"[^>]*>)연 -[0-9.]+%', lambda m: m.group(1) + '해석 부적합', h)
h = _re.sub(r'현재가를 정당화하려면 매출이 5년간 연 [−-][0-9.]+% 커야 한다\. ', '현금흐름 값이 0 이하라 현재가 요구 성장률은 해석할 수 없다. ', h)
''']
# 헤더 '현재가 요구 성장' 칸 — 현금흐름 값이 0 이하이면 숫자 대신 '해석 부적합'(AEE Fable r1, 2026-10-25)
POST.append(r'''
h = h.replace("  if (req && price != null) {", "  if (req && d.base <= 0) { req.textContent = '해석 부적합'; req.style.color = 'var(--text3)'; const _c = req.closest('.meta-item'); if (_c) _c.title = '해석 부적합(현금흐름 0 이하) — 현금흐름 내재가치가 0 이하라 현재가 요구 성장률을 해석할 수 없다.'; }\n  if (req && price != null && d.base > 0) {", 1)
import re as _re2
h = _re2.sub(r'(id="ttwoDcfReq"[^>]*>)연 [−-][0-9.]+%', lambda m: m.group(1) + '해석 부적합', h)
''')
PH = ['NFLX', 'DIS', 'META', 'GOOGL', 'TTD', 'LYV']
PEER_FILE = 'peer_universe/communication_services.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '미디어·플랫폼 6곳 PER 비교 (점수는 S&P500 커뮤니케이션 기준)', 'pbr': '미디어·플랫폼 PBR 비교', 'psr': '미디어·플랫폼 PSR 비교',
                'pcr': '미디어·플랫폼 PCR(FCF) 비교', 'evebitda': '미디어·플랫폼 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 커뮤니케이션 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 커뮤니케이션 대비 배수 순위 (v2/peer_universe/communication_services.json)'
PEER_TIP = ('S&P500 커뮤니케이션(TTWO 제외)과 배수 순위를 매긴 값이다.',
            '미디어·통신·인터넷 플랫폼이 섞여 있다(게임사는 TTWO뿐 — EA는 비상장 전환). 차트에는 미디어·플랫폼 6곳만 보인다.')
# 매출(Q1 FY27 10-Q) — 단일 부문. 플랫폼별: 모바일 762.3 + 콘솔 640.5 + PC·기타 131.1 = 1,533.9.
SEG = [('모바일', 762.3, '#d4232b'), ('콘솔', 640.5, '#f07a7f'), ('PC·기타', 131.1, '#f6b9bc')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 플랫폼별'   # 분기는 fill.py가 실제 값으로 붙인다 — 손으로 적으면 분기를 넘길 때 두 번 나온다(2026-10-30)
# 손 뉴스: 실적 4건(EPS는 GAAP 희석 — 순예약·가이던스는 쓰지 않는다) + Xbox 라이선스. 반응일: 장 마감 뒤 발표 → 다음 거래일, Q1 FY27은 장 전 → 같은 날.
# Xbox 라이선스 8-K 9/30 20:31(동부, 장 마감 뒤) → 10/1. 4분기 EPS는 연간 − 9개월 역산(손실 분기 주식 수 차이로 보도자료와 몇 센트 다름 — 덮어쓰지 않음). 넣지 않은 8-K: 주총(2025-09·2026-09), 투자자 자료(2025-09-10).
NEWS_RANGE = '2025.11 ~ 2026.10'
NEWS = [
    ('neutral', '2026년 9월 30일 — Microsoft와 새 Xbox 장기 퍼블리셔 계약', '2026-10-01',
     '기존 계약을 대체하는 장기 라이선스(금액 미공시)', 'xbox', 'Take-Two 공시 (SEC 8-K)'),
    ('green', '2026년 8월 7일 — Q1 FY27 실적', '2026-08-07',
     '매출 $1.53B(1년 전 $1.50B) · 순손실 $34M · 희석 EPS −$0.18(1년 전 −$0.07) — 개발을 멈춘 소프트웨어 손상 $43.4M 포함 · GTA VI 11/19 출시 재확인', 'q1', 'Take-Two 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 5월 21일 — Q4 FY26 실적', '2026-05-22',
     '매출 $1.68B · 순손실 $60M · 희석 EPS −$0.32(1년 전 −$21.08 — 영업권 손상) · FY2026 EPS −$1.62', 'q4', 'Take-Two 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 2월 3일 — Q3 FY26 실적', '2026-02-04',
     '매출 $1.70B · 순손실 $93M · 희석 EPS −$0.50(1년 전 −$0.71)', 'q3', 'Take-Two 실적 보도자료 (SEC 8-K)'),
    ('red', '2025년 11월 6일 — Q2 FY26 실적 · GTA VI 출시 2026년 11월 19일로 연기', '2025-11-07',
     '매출 $1.77B · 순손실 $134M · 희석 EPS −$0.73(1년 전 −$2.08) · 같은 발표에서 GTA VI 출시일을 2026년 11월 19일로 미뤘다', 'q2', 'Take-Two 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Strong Buy', 'n': 29, 'nt': 20, 'mean': 294.3, 'median': 300, 'low': 270, 'high': 330, 'sb': 25, 'b': 3, 'h': 0, 's': 1, 'ss': 0}
ANALYST_ASOF = '2026-10-31'


# ── 자동 카드 — 플랫폼 3개(수동 지도, 제품·서비스 축 — 같은 축에 다른 나눔이 겹쳐 있어 나머지는 ignore). 원문 대조: Q1 FY27 762.3/640.5/131.1(2026-10-24) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "srt:ProductOrServiceAxis",
 "extra": {},
 "members": {"ttwo:MobileMember": ["모바일", "#d4232b"], "ttwo:ConsoleMember": ["콘솔", "#f07a7f"], "ttwo:PCAndOtherProductsMember": ["PC·기타", "#f6b9bc"]},
 "ignore": ["ttwo:RecurrentCustomerSpendingMember", "ttwo:FullGameAndOtherMember", "ttwo:DigitalOnlineMember", "ttwo:PhysicalRetailAndOtherMember", "ttwo:GameMember", "us-gaap:AdvertisingMember"]
}
