CIK = '0000726728'
BUILD = {'company_tags': [('o:LineOfCreditAndCommercialPaper', 'LineOfCredit', '2020-07-01'), ('o:RevolvingCreditFacilityAndCommercialPaper', 'LineOfCredit', '2020-07-01')]}   # 신용한도·CP 줄 이름이 2025년에 바뀌었다(옛 o:LineOfCreditAndCommercialPaper — 2021년 말 $1,551M 등, Codex r1)
# O(리얼티 인컴) v2 카드 설정 — 자동 카드(AUTO), 정식. 회계연도 12월 31일. 리츠(REIT) — 상업용 부동산 장기 순임대(편의점·약국·물류·유럽 등), 월 배당.
# 출처: SEC XBRL, Q3 2026 10-Q(2026-11-02 17:39 동부 접수 → 첫 세션 11-03, 카드 기준일 11-18 종가), 실적 보도자료(8-K 2.02항 — 모두 장 마감 뒤 16:0x 동부 → 다음 날).
# 엔진 입력(2026-11-19): 영업이익 = 매출 − 비용 합계 + 이자비용(DERIVED_OPINC, WELL 방식 — 손상차손은 영업 안, 매각 이익·환율·지분법은 밖), 순이익 = 보통주 귀속(EXTRA_TAGS),
#   설비투자 = 기존 자산 개량 지출(PaymentsForCapitalImprovements, WELL 선례 — 부동산 인수는 제외), 차입금 = 신용한도·CP(회사 고유 태그, company_tags) + 기간 대출 + 담보 + 채권 = $31.4B,
#   단기투자 제외(2020 낡은 값), 비지배지분 = 일반 $3,111M + 상환 가능 $72M.
# 일회성(E54): 최근 4분기 보통주 귀속 순이익 $1,355.8M(EPS 0.32+0.33+0.37+0.43 = 1.45). 회사가 FFO에서 빼는 손상차손 $375.4M(119.4·90.2·54.2·111.6), 매각 이익 $255.2M(67.4·35.6·38.3·113.9)
#   회사가 Normalized FFO·AFFO에서 더 빼는 비용(신용손실 충당 65.6·환율·파생 손실 47.2·합병·거래 25.8)까지 비용만 합치면 $514.0M = 37.9%, 순액(매각 이익 상계) 19.1%.
#   손상차손은 2021년부터 매 분기 나온 회사 조정 비용이라 반복분으로 빼면 나머지 $138.6M = 10.2% → 정식(2026-11-19 사용자 결정 — LH 반복분 규칙을 경계 밖까지 적용).
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, 0, -2), '적정~고평가'
CO = 'Realty Income'
S_ = 'https://www.sec.gov/Archives/edgar/data/726728/'
SEC = S_
TENQ = S_ + '000072672826000059/o-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000072672826000056/o-991q32026.htm', 'q2': S_ + '000072672826000044/o-991q22026.htm',
      'q1': S_ + '000072672826000028/o-991q12026.htm', 'q4': S_ + '000072672826000009/o-991q42025.htm',
      'cv': S_ + '000110465926094098/tm2622133d1_ex99-1.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="oFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). 리츠는 감가상각이 커서 PER이 높게 나온다 — PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 50)
ACT_REASON = '리츠라 재고·매출채권 회전으로 보는 활동성이 잘 맞지 않는다'
NONOP_WHAT = '투자'
MODEL_NOTE = ('리츠는 건물 감가상각이 커서 GAAP 순이익이 실제 현금 창출보다 작게 나오고, 업계는 FFO(순이익에 부동산 감가상각·손상을 되더하고 매각 이익을 뺀 값)와 AFFO(추가 조정)로 본다 — 리얼티 인컴의 2026년 연간 AFFO 전망은 주당 $4.45~4.46으로 최근 4분기 GAAP EPS($1.45)의 약 3배다. 이 카드는 다른 카드와 같은 GAAP 배수로 보므로 PER이 높게 나온다. 사이트에는 리츠 전용 평가(FFO·순자산가치)가 아직 없고, 현금흐름 내재가치가 0 이하인 것은 차입금 $31.6B를 빼는 모델 구조 때문이다. '
              '최근 4분기 순이익에는 회사가 FFO에서 빼는 부동산 손상차손 $375M과 매각 이익 $255M이 들어 있다(순 $120M, 순이익의 약 9%). 손상차손은 매 분기 나오는 비용이라 카드는 GAAP 그대로 쓴다. '
              '설비투자는 기존 건물 개량 지출만 넣었고 부동산 매입(1~9월 $5.6B)과 대출·우선주 투자($1.9B)는 넣지 않았다 — 그래서 FCF·PCR이 실제 투자 규모보다 좋게 보이고, 성장은 신주·차입으로 산 새 부동산에서 온다. 희석 주식 수가 2021년 연평균 약 4.1억 주에서 2026년 3분기 약 9.5억 주로 약 2.3배 늘어, 주당 AFFO 성장(2021년 $3.59 → 2026년 전망 $4.45~4.46)은 연 4%대다. 자사주 매입 $291M은 전환사채 발행과 함께 한 것이고 같은 기간 신주 $1.28B를 발행했다. '
              '비지배지분($3.1B, 전년 말 $0.7B)은 Core Plus 펀드와 Apollo 합작(기존 부동산 492곳 지분 49%) 등 외부 투자자 몫이다. 차입금에는 신용한도·기업어음 $2.1B가 들어 있다.')
HEALTH_EXTRA = '부동산 매입 자금을 채권·신주로 조달하는 리츠라 차입금 비중이 높게 나온다 — 회사가 보는 순차입금 ÷ 연환산 추정 조정 EBITDAre는 5.4배다.'
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
h = _re.sub(r'(id="oDcfReq"[^>]*>)연 -[0-9.]+%', lambda m: m.group(1) + '해석 부적합', h)
h = _re.sub(r'현재가를 정당화하려면 매출이 5년간 연 [−-][0-9.]+% 커야 한다\. ', '현금흐름 값이 0 이하라 현재가 요구 성장률은 해석할 수 없다. ', h)
''']
# 헤더 '현재가 요구 성장' 칸 — 현금흐름 값이 0 이하이면 숫자 대신 '해석 부적합'(AEE Fable r1, 2026-10-25)
POST.append(r'''
h = h.replace("  if (req && price != null) {", "  if (req && d.base <= 0) { req.textContent = '해석 부적합'; req.style.color = 'var(--text3)'; const _c = req.closest('.meta-item'); if (_c) _c.title = '해석 부적합(현금흐름 0 이하) — 현금흐름 내재가치가 0 이하라 현재가 요구 성장률을 해석할 수 없다.'; }\n  if (req && price != null && d.base > 0) {", 1)
import re as _re2
h = _re2.sub(r'(id="oDcfReq"[^>]*>)연 [−-][0-9.]+%', lambda m: m.group(1) + '해석 부적합', h)
''')
PH = ['SPG', 'PLD', 'WELL', 'VICI', 'NNN', 'ADC']
PEER_FILE = 'peer_universe/real_estate.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '리츠 6곳 PER 비교 (점수는 S&P500 부동산 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 부동산 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 부동산 대비 배수 순위 (v2/peer_universe/real_estate.json)'
PEER_TIP = ('S&P500 부동산(O 제외)과 배수 순위를 매긴 값이다.',
            '물류·데이터센터·의료·쇼핑몰·주택 리츠와 부동산 서비스가 섞여 있다. 차트에는 리츠 6곳이 보인다.')
# 매출(Q3 2026 10-Q 손익계산서): 임대 1,483.8 + 대출·우선주 투자 이자·배당 105.0 + 금융채권 이자 32.2 + 기타 0.6 = 1,621.6.
SEG = [('임대 수익', 1483.8, '#1f4e79'), ('대출·우선주 투자 이자·배당', 105.0, '#c8a24a'), ('금융채권(금융리스형 임대) 이자', 32.2, '#7da3c8'), ('기타', 0.6, '#9aa7b8')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 수익 종류별'
NEWS_RANGE = '2026.02 ~ 2026.11'
NEWS = [
    ('neutral', '2026년 11월 2일 장 마감 뒤 — Q3 2026 실적', '2026-11-03',
     '보통주 순이익 $404M · 희석 EPS $0.43(1년 전 $0.35) · AFFO $1.12(+3.7%) · 투자 $2.6B · 2026년 AFFO 전망 $4.45~4.46 — 다음 날 주가 −0.1%', 'q3', 'Realty Income 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 8월 11일 장 마감 뒤 — 전환사채 발행', '2026-08-12',
     '2031년 만기 전환사채 $750M 계획을 같은 날(8/11) $875M으로 늘려 가격 확정, 8/12 장 전 공시(이자 3.75%, 전환가 $72.72, 옵션 포함 $1.0B 발행) — 다음 날 주가 +1.1%', 'cv', 'Realty Income 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 8월 5일 장 마감 뒤 — Q2 2026 실적', '2026-08-06',
     '보통주 순이익 $344M · 희석 EPS $0.37(1년 전 $0.22) · AFFO $1.09(+3.8%) · 투자 $2.6B — 다음 날 주가 −0.5%', 'q2', 'Realty Income 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 5월 6일 장 마감 뒤 — Q1 2026 실적', '2026-05-07',
     '보통주 순이익 $312M · 희석 EPS $0.33(1년 전 $0.28) · AFFO $1.13(+6.6%) · 투자 $2.8B — 다음 날 주가 −3.5%', 'q1', 'Realty Income 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 24일 장 마감 뒤 — 2025년 연간 실적', '2026-02-25',
     '4분기 보통주 순이익 $296M · 희석 EPS $0.32(1년 전 $0.23) · AFFO $1.08 · 2025년 EPS $1.17 — 다음 날 주가 −0.8%', 'q4', 'Realty Income 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 25, 'nt': 15, 'mean': 63.85, 'median': 63, 'low': 59, 'high': 72, 'sb': 6, 'b': 1, 'h': 17, 's': 1, 'ss': 0}
ANALYST_ASOF = '2026-11-19'


AUTO = True
SEG_MAP = {
 "parts": [
  {
   "concepts": [],
   "axis": None,
   "extra": {},
   "members": {
    "us-gaap:LeaseIncome": ["임대 수익", "#1f4e79"],
    "us-gaap:InterestAndDividendIncomeSecurities": ["대출·우선주 투자 이자·배당", "#c8a24a"],
    "us-gaap:InterestAndFeeIncomeLoansAndLeases": ["금융채권(금융리스형 임대) 이자", "#7da3c8"],
    "us-gaap:OtherIncome": ["기타", "#9aa7b8"]
   }
  }
 ]
}
