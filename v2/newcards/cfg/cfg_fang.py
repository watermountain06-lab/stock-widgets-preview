CIK = '0001539838'
BUILD = {'no_dcf': '미완성 — 유가 자산 감액 등 일회성이 최근 4분기 GAAP 이익보다 크다(약 150%)'}   # 2026-11-07·08 사용자 규칙(일회성 30% 이상이면 미완성, 회사 분류를 따른다) — RVTY·ROP와 같은 처리
# FANG(다이아몬드백 에너지) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 12월 말. 퍼미안 분지 셰일 원유·가스 생산, 자회사 Viper(광물·로열티, 비지배지분).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-11-04 장 마감 뒤 접수, 카드 기준일 11-12 종가), 실적 보도자료(8-K 2.02항 — 모두 장 마감 뒤 16:0x 동부 → 다음 날).
# 일회성(E54): 최근 4분기 GAAP 희석 EPS 7.31(−5.11 + 0.08 + 6.65 + 5.69 — 보도자료; XBRL 역산 Q4는 −4.99라 Q4_EPS_OVERRIDE).
#   회사 조정표(Diamondback 귀속, 주당 $): 조정 EPS 1.74 · 4.23 · 6.48 · 5.86 = 18.31 → GAAP와 차이 $11.00(GAAP의 약 150%).
#   항목(세전, 비지배 포함 금액 기준): Q4 2025 유가 자산 감액 $3,652M · 파생상품 평가이익 −119 · 채무 상환 이익 −33 · 기타 비현금 −417, Q1 2026 감액 $1,400M · 파생 16 · 기타 16,
#   Q2 2026 파생 64 · 채무 상환 이익 −134(장기채 공개매수) · 기타 11, Q3 2026 파생 85 · 채무 상환 이익 −4 · 기타 −15. 감액은 영업이익 안에 있어 영업이익·EV/EBITDA도 왜곡된다.
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, 0), '판정 보류'
CO = 'Diamondback'
S_ = 'https://www.sec.gov/Archives/edgar/data/1539838/'
SEC = S_
TENQ = S_ + '000153983826000183/fang-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000153983826000180/diamondbackex991-11x2x26.htm', 'q2': S_ + '000153983826000137/diamondbackex991-8x3x26.htm',
      'q1': S_ + '000153983826000073/diamondbackex991-5x4x26.htm', 'q4': S_ + '000153983826000006/diamondbackex991-2x23x26.htm',
      'q3p': S_ + '000153983825000144/diamondbackex991-11x3x25.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="fangFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(유가 자산 감액 등 일회성이 최근 4분기 GAAP 이익을 크게 깎는다)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (미완성 — 현금흐름 보류)</span>'
Y2 = (-10, 30)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('미완성 카드다. 이 카드는 일회성 항목이 최근 4분기 GAAP 이익의 30% 이상이면 판정을 보류하는데, FANG은 최근 4분기 GAAP 희석 EPS 합계가 $7.31로 회사 조정 EPS $18.31보다 $11.00(GAAP의 약 150%) 작다. '
              '대부분 유가 자산 감액이다 — 2025년 4분기 $3,652M, 2026년 1분기 $1,400M(세전). 전부원가법 상한 시험에서 직전 12개월 월초 평균 유가(SEC 가격)가 내려가 장부가를 깎은 비현금 비용이다(그 분기 실현 유가는 4분기 $58, 1분기 $73). 영업비용 안에 있어 순이익·영업이익·EBITDA가 낮아지고 PER·EV/EBITDA는 높아진다(감액만 되돌리면 EV/EBITDA 9.2배 → 약 5.5배). 헤지 파생상품 평가손익, 장기채 조기 상환 이익(2분기 $134M), 2025년 4분기 기타 비현금 이익($417M)도 회사가 조정에서 빼는 항목이다. 감액은 되돌리지 않고 앞으로 감가상각을 줄인다. '
              '분기마다 다시 센다. 가장 큰 4분기 감액이 빠지는 2026년 4분기 실적(2027년 2월 예상)이 주요 확인 시점이다 — 그때 남는 차이는 주당 약 $4.15(1분기 감액 중심)라, 4분기에 새 일회성이 없고 4분기 GAAP EPS가 약 $1.4를 넘으면 30% 아래가 된다. 회사는 10-Q에서 4분기 추가 감액을 예상하지 않는다고 밝혔다. 1분기 감액까지 모두 빠지는 것은 2027년 5월(예상)이다. '
              '본업은 유가에 크게 기대 있다 — 3분기 원유 생산 525천 배럴/일(+4%)인데 실현 유가가 배럴당 $87.30(2분기 $96.82)로 1년 전(약 $65)보다 높아 매출이 $5.43B(+38%)로 늘었다. 천연가스 실현가는 퍼미안 운송 병목으로 2분기에 음수(−$2.15/Mcf)였다가 3분기 $1.12로 돌아왔다. 매출 중 구매 원유 판매($536M)는 남는 송유관 약정 물량을 채우려 사고파는 것이라 이익이 거의 없다(비용 $540M). '
              '현금 창출이 크다 — 3분기 영업현금흐름 $2.6B, 설비투자 $1.0B(카드 FCF $1.57B; 회사 FCF $2.1B는 운전자본 변동 전 영업현금흐름 기준). 2026년 연간 설비투자 전망은 3분기에 $3.95~4.00B로 올렸다. 기본 배당을 연 $4.72로 올렸고(+7.3%) 3분기 자사주 1.3M주 $251M를 샀다. 카드 FCF·매출은 자회사 Viper까지 합친 연결 값이다. '
              '차입금은 $13.2B(9월 말, 1년 안 만기 $1.55B — 2분기에 줄였다가 3분기에 다시 늘었다), 현금 $558M. 자회사 Viper의 외부 주주 몫(비지배지분 장부가 $6.2B)은 EV에 더한다. 주가는 1월 7일 종가 $140.45에서 5월 4일 종가 $213.69까지 올랐다가 11월 12일 $182.20이다.')
PH = ['XOM', 'CVX', 'COP', 'EOG', 'OXY', 'DVN']
PEER_FILE = 'peer_universe/energy.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '석유·가스 6곳 PER 비교 (점수는 S&P500 에너지 기준)', 'pbr': '석유·가스 PBR 비교', 'psr': '석유·가스 PSR 비교',
                'pcr': '석유·가스 PCR(FCF) 비교', 'evebitda': '석유·가스 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 에너지 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 에너지 대비 배수 순위 (v2/peer_universe/energy.json)'
PEER_TIP = ('S&P500 에너지(FANG 제외)와 배수 순위를 매긴 값이다.',
            '통합 석유·탐사생산·정유·파이프라인 회사가 섞여 있다. 차트에는 석유·가스 생산 6곳만 보인다.')
# 매출(Q3 2026 10-Q 손익계산서): 원유 4,216 + NGL 487 + 천연가스 151 + 구매 원유 판매 536 + 기타 41 = 5,431.
SEG = [('원유', 4216, '#3b3b38'), ('천연가스액(NGL)', 487, '#8c7b6b'), ('천연가스', 151, '#b5a999'), ('구매 원유 판매', 536, '#d97a6c')]
SEG_ADJ = 41   # 기타 영업수익·서비스(XBRL 제품 축 사실 없음)
SEG_ADJ_LABEL = '기타 영업수익·서비스'
SEG_TITLE = '매출 구성 — 제품별'
# 손 뉴스: 실적 5건. 반응일: 모두 장 마감 뒤 발표 → 다음 날. 색은 사건 성격, 수치는 그날 주가.
NEWS_RANGE = '2025.11 ~ 2026.11'
NEWS = [
    ('neutral', '2026년 11월 2일 장 마감 뒤 — Q3 2026 실적', '2026-11-03',
     '원유 525천 배럴/일 · 실현 유가 $87.30 · GAAP 희석 EPS $5.69 · 조정 EPS $5.86 · 기본 배당 연 $4.72로 +7.3% · 자사주 $251M — 다음 날 주가 −3.7%', 'q3', 'Diamondback 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 8월 3일 장 마감 뒤 — Q2 2026 실적', '2026-08-04',
     '생산 1,018천 BOE/일(100만 돌파) · 실현 유가 $96.82 · GAAP 희석 EPS $6.65 · 조정 EPS $6.48 · 차입금 약 $1.3B 감축 — 다음 날 주가 −3.5%', 'q2', 'Diamondback 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 5월 4일 장 마감 뒤 — Q1 2026 실적', '2026-05-05',
     'GAAP 희석 EPS $0.08(유가 자산 감액 $1.4B) · 조정 EPS $4.23 · 원유 생산 전망 520천 배럴/일 이상으로 상향 · 연간 설비투자 약 $3.9B로 상향 — 다음 날 주가 −3.5%', 'q1', 'Diamondback 보도자료 (SEC 8-K)'),
    ('red', '2026년 2월 23일 장 마감 뒤 — 2025년 연간 실적', '2026-02-24',
     '4분기 GAAP 희석 주당 손실 $5.11(유가 자산 감액 $3.65B) · 조정 EPS $1.74 · 기본 배당 연 $4.20으로 +5% · 자사주 $434M — 다음 날 주가 −0.7%', 'q4', 'Diamondback 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 11월 3일 장 마감 뒤 — Q3 2025 실적', '2025-11-04',
     '원유 503.8천 배럴/일 · 영업현금흐름 $2.4B · 자사주 4.3M주 $603M · Viper의 Sitio 인수 종결(8월) — 다음 날 주가 −1.3%', 'q3p', 'Diamondback 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 32, 'nt': 21, 'mean': 236.05, 'median': 235, 'low': 192, 'high': 263, 'sb': 20, 'b': 6, 'h': 6, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-13'

# 재검토 기록용(자동 재판정 코드는 아직 없음) — 일회성이 든 분기(결산일: GAAP와 조정 EPS 차이, Diamondback 귀속 주당 $, +는 비용·−는 이익).
ONEOFF_QUARTERS = {'2025-12-31': '차이 6.85 — 유가 자산 감액 $3,652M(세전) · 파생 평가이익 · 채무 상환 이익 · 기타 비현금 이익',
                   '2026-03-31': '차이 4.15 — 유가 자산 감액 $1,400M(세전) · 파생 평가손실 · 채무 상환 손실 $1M · 기타',
                   '2026-06-30': '차이 −0.17 — 채무 상환 이익 $134M · 파생 평가손실 $64M · 기타',
                   '2026-09-30': '차이 0.17 — 파생 평가손실 $85M · 채무 상환 이익 $4M · 기타 비현금 이익'}

# 미완성 카드 표시(2026-11-08 사용자 규칙, AXON·RVTY·ROP 방식).
INCOMPLETE_SHORT = '유가 자산 감액이 큼'
INCOMPLETE_WHY = '최근 4분기 GAAP EPS($7.31)가 회사 조정 EPS($18.31)보다 $11.00 작다 — 대부분 2025년 4분기·2026년 1분기 유가 자산 감액($3.65B·$1.4B)이라 배수 판정이 왜곡돼 보류한다. 분기마다 다시 세고, 주요 확인은 2027년 2월(4분기 감액이 빠질 때)'
POST = [r"""
import re as _re0
_w = '최근 4분기 GAAP EPS($7.31)가 회사 조정 EPS($18.31)보다 $11.00 작다 — 대부분 2025년 4분기·2026년 1분기 유가 자산 감액($3.65B·$1.4B)이라 배수 판정이 왜곡돼 보류한다. 분기마다 다시 세고, 주요 확인은 2027년 2월(4분기 감액이 빠질 때)'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — 유가 자산 감액이 큼 · 매 분기 재검토, 주요 확인 2027년 2월</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — 유가 자산 감액이 큼. 미완성 카드 규칙에 따라 종합 판정과 함께 현금흐름 내재가치도 보류했다.')
h = _re0.sub(r'(id="fangFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)
h = _re0.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re0.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")
h = _re0.sub(r'(<div class="verdict-summary-head">[^<]*)<span class="tag">[^<]*</span>', r'\1<span class="tag">유가 자산 감액이 큼</span>', h, count=1)
h = _re0.sub(r'<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
h = _re0.sub(r'<div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
# 자본배분: 9개월 누계 자사주·배당을 표준 태그로 싣지 않아 "공시 없음"이 나온다 — 10-Q 현금흐름표 값으로(자사주: 프로그램 $431M + 특수관계인 SGF $509M, 배당 지급 $918M)
_bb = '<span class="zone-label">자사주 매입</span>\n          <div style="display:flex;align-items:center;gap:8px;">\n            <span class="zone-val">공시 없음</span>'
assert _bb in h
h = h.replace(_bb, '<span class="zone-label">자사주 매입 (연초~9/30, 39주)</span>\n          <div style="display:flex;align-items:center;gap:8px;">\n            <span class="zone-val">$940M</span>', 1)
_dv = '<span class="zone-label">보통주 배당 지급</span>\n          <span class="zone-val">공시 없음</span>'
assert _dv in h
h = h.replace(_dv, '<span class="zone-label">보통주 배당 지급 (연초~9/30, 39주)</span>\n          <span class="zone-val">$918M</span>', 1)
# ② 1년 전 4분기 GAAP 영업이익률(−82.4%)은 감액 $3.65B가 든 값이라 비교 기준으로 쓰지 않는다 — 회사 4분기 전망으로
_c2 = h[h.index('<strong style="color:var(--accent2);">②</strong>'):]; _c2 = _c2[:_c2.index('</div>')]
h = h.replace(_c2, '<strong style="color:var(--accent2);">②</strong> 4분기에 유가 자산 감액이 또 생기는지(2025년 4분기 $3.65B, 2026년 1분기 $1.4B) — Q4 2025 GAAP 영업이익률(−82.4%)은 감액이 든 값이라 비교 기준으로 쓰지 않는다. 연간 원유 생산 약 524천 배럴/일 전망을 지키는지', 1)
# 약세 요인 마진: 최근 4분기 영업이익률은 감액 $5.05B가 깎은 값이다
h = _re0.sub(r'(<span class="bb-head">마진</span><span class="bb-text">[^<]*?)\.?(</span>)', lambda m: m.group(1) + ' — 4분기·1분기 유가 자산 감액 $5.05B가 깎은 값이다.' + m.group(2), h, count=1)
h = _re0.sub(r'(<span class="bb-head">부채</span><span class="bb-text">[^<]*?)\.?(</span>)', lambda m: m.group(1) + ' — 영업이익이 감액 $5.05B로 깎인 값이라, 감액을 빼면 약 1.7배다.' + m.group(2), h, count=1)
"""]

AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "srt:ProductOrServiceAxis",
 "extra": {},
 "members": {"fang:OilExplorationandProductionMember": ["원유", "#3b3b38"], "fang:NaturalGasLiquidsProductionMember": ["천연가스액(NGL)", "#8c7b6b"], "us-gaap:NaturalGasProductionMember": ["천연가스", "#b5a999"], "fang:OilPurchasedMember": ["구매 원유 판매", "#d97a6c"]},
 "ignore": ["fang:OilNaturalGasAndNaturalGasLiquidMember"]
}
