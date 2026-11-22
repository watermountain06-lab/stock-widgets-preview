CIK = '0001679788'
BUILD = {'no_dcf': '미완성 — 최근 4분기 GAAP가 적자(보유 가상자산·전략 투자 평가손실)', 'cover_shares': True}
# COIN(코인베이스) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 12월 31일. 가상자산 거래소 — 거래 수수료, 구독·서비스(USDC 이자 수익 분배·스테이킹·보관), 예측시장.
# 출처: SEC XBRL, Q3 2026 10-Q(카드 기준일 11-18 종가), 실적 발표 자료·주주 서한(8-K 2.02항 — 모두 장 마감 뒤 16:0x 동부 → 다음 날), 구조조정 8-K(05-05 06:57 장 전 → 그날).
# 엔진 입력(2026-11-19): 표지 주식 수 A + B(cover_shares). 설비투자는 2024년부터 따로 공시하지 않아(PaymentsToAcquirePropertyPlantAndEquipment 2023-09 멈춤) PCR이 빠진다. 우선주는 2024년 0.
# 일회성(E54): 최근 4분기 GAAP 순이익 −$701.6M(Q4 2025 −666.7 = 연간 1,260.3 − 9개월 1,927.1, Q1 −394.1, Q2 −359.5, Q3 +718.7), 희석 EPS −2.83(−2.49 − 1.49 − 1.36 + 2.51; Q4는 주주 서한 값 — Q4_EPS_OVERRIDE) — 적자라 미완성.
#   손익을 좌우하는 것은 투자용 가상자산 평가손익(Q3 이익 $715M)과 전략 투자 평가손익.
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, None, 0), '판정 보류'
CO = 'Coinbase'
S_ = 'https://www.sec.gov/Archives/edgar/data/1679788/'
SEC = S_
TENQ = S_ + '000167978826000122/coin-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000167978826000121/q326earningsdeck_vsec.htm', 'q2': S_ + '000167978826000087/q226earningsdeck_sec.htm',
      'q1': S_ + '000167978826000053/q126earningsdeck-finalse.htm', 'q4': S_ + '000167978826000011/q425shareholderletter.htm',
      'rs': S_ + '000167978826000049/coin-20260505.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="coinFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(최근 4분기 GAAP가 적자다)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (미완성 — 현금흐름 보류)</span>'
Y2 = (-60, 60)
ACT_REASON = '거래소라 재고·매출채권 회전으로 보는 활동성이 잘 맞지 않는다'
NONOP_WHAT = '투자'
MODEL_NOTE = ('미완성 카드다. 이 카드는 최근 4분기 GAAP 이익이 적자이거나 일회성이 30% 이상이면 판정을 보류하는데, 코인베이스는 최근 4분기 GAAP 순손실이 약 $702M(분기 희석 EPS 합 −$2.83)이다. '
              '회사가 들고 있는 투자용 가상자산(비트코인·이더리움 등)과 Circle 지분 등 투자의 평가손익이 분기마다 수억 달러씩 이익을 흔든다 — 2025년 4분기와 2026년 1·2분기는 가격 하락으로 손실, 3분기는 가상자산 평가이익 $715M로 순이익 $719M이었다. 평가손익을 뺀 회사 조정 순이익도 1·2분기는 적자(−$46M·−$105M)였다. 기본적 분석의 순이익률(3분기 59%)은 이 평가이익 때문에 높게 나온 값이다. '
              '본업 매출(3분기 $1.2B: 거래 수수료 $590M, 구독·서비스 $570M)도 가상자산 가격과 거래량에 크게 기대 있다. 5월에는 인력 약 14%(700명) 감축 계획을 발표했다. '
              '분기마다 다시 센다 — 손실 분기가 빠지는 2027년 2월(4분기 실적)부터 GAAP 흑자 여부를 다시 보지만, 흑자가 되어도 평가손익이 순이익의 30%를 넘기 쉬워 미완성이 이어질 수 있다. '
              '설비투자를 2024년부터 따로 공시하지 않아 PCR은 빠진다. 고객 예치 현금(보관 부채 $4.5B)은 회사 현금 $8.6B와 별도이고, 회사 현금에는 결제용 스테이블코인(USDC 등)이 들어 있다. 주식 수는 클래스 A와 B를 더한 값이다.')
PH = ['HOOD', 'CME', 'ICE', 'NDAQ', 'CBOE', 'SCHW']
PEER_FILE = 'peer_universe/payments_exchanges.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '거래소·증권 6곳 PER 비교 (점수는 결제·거래소 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = '결제·거래소 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = '결제·거래소 대비 배수 순위 (v2/peer_universe/payments_exchanges.json)'
PEER_TIP = ('결제·거래소 무리(COIN 제외)와 배수 순위를 매긴 값이다.',
            '카드 네트워크·결제 대행·전통 거래소가 섞여 있고 가상자산 거래소는 COIN뿐이다. 차트에는 거래소·증권 6곳이 보인다.')
# 매출(Q3 2026 10-Q 제품·서비스 축): 거래 수수료 590.2 + 구독·서비스 570.2 = 1,160.5, 기타 매출 55.1 → 1,215.6.
SEG = [('거래 수수료', 590.2, '#0052ff'), ('구독·서비스(USDC·스테이킹 등)', 570.2, '#7da7ff')]
SEG_ADJ = 55.1
SEG_ADJ_LABEL = '기타 매출'
SEG_TITLE = '매출 구성 — 수익 종류별'
NEWS_RANGE = '2026.02 ~ 2026.10'
NEWS = [
    ('neutral', '2026년 10월 29일 장 마감 뒤 — Q3 2026 실적', '2026-10-30',
     '매출 $1.2B · 순이익 $719M(투자용 가상자산 평가이익 $715M) · 조정 EBITDA $333M — 다음 날 주가 −10.6%', 'q3', 'Coinbase 실적 발표 자료 (SEC 8-K)'),
    ('red', '2026년 7월 30일 장 마감 뒤 — Q2 2026 실적', '2026-07-31',
     '매출 $1.2B · 순손실 $359M · 조정 EBITDA $208M — 다음 날 주가 −10.6%', 'q2', 'Coinbase 실적 발표 자료 (SEC 8-K)'),
    ('red', '2026년 5월 7일 장 마감 뒤 — Q1 2026 실적', '2026-05-08',
     '매출 $1.4B · 순손실 $394M · 조정 EBITDA $303M — 다음 날 주가 +4.2%', 'q1', 'Coinbase 실적 발표 자료 (SEC 8-K)'),
    ('neutral', '2026년 5월 5일 장 전 — 인력 약 14% 감축', '2026-05-05',
     '약 700명(14%)을 줄이는 구조조정, 비용 $50~60M 예상 — 그날 주가 −2.6%', 'rs', 'Coinbase 8-K'),
    ('red', '2026년 2월 12일 장 마감 뒤 — 2025년 연간 실적', '2026-02-13',
     '4분기 순손실 $667M·희석 주당 손실 $2.49(가상자산·Circle 지분 평가손실) · 2025년 순이익 $1.26B — 다음 날 주가 +16.5%', 'q4', 'Coinbase 주주 서한 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 37, 'nt': 31, 'mean': 197.03, 'median': 197, 'low': 100, 'high': 330, 'sb': 19, 'b': 5, 'h': 10, 's': 1, 'ss': 2}
ANALYST_ASOF = '2026-11-22'

INCOMPLETE_SHORT = 'GAAP 적자·가상자산 평가손익'
INCOMPLETE_WHY = '최근 4분기 GAAP가 적자(순손실 약 $702M, 분기 희석 EPS 합 −$2.83)다 — 보유 가상자산·전략 투자 평가손익이 분기마다 수억 달러씩 이익을 흔들어(4분기 손실, 3분기 평가이익 $715M) 배수 판정을 보류한다. 분기마다 다시 센다'
POST = [r"""
import re as _re0
_w = '최근 4분기 GAAP가 적자(순손실 약 $702M, 분기 희석 EPS 합 −$2.83)다 — 보유 가상자산·전략 투자 평가손익이 분기마다 수억 달러씩 이익을 흔들어(4분기 손실, 3분기 평가이익 $715M) 배수 판정을 보류한다. 분기마다 다시 센다'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — GAAP 적자·가상자산 평가손익 · 매 분기 재검토</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — GAAP 적자·가상자산 평가손익. 미완성 카드 규칙에 따라 종합 판정과 함께 현금흐름 내재가치도 보류했다.')
h = _re0.sub(r'(id="coinFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)
h = _re0.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re0.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")
h = _re0.sub(r'(<div class="verdict-summary-head">[^<]*)<span class="tag">[^<]*</span>', r'\1<span class="tag">GAAP 적자·가상자산 평가손익</span>', h, count=1)
h = _re0.sub(r'<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
h = _re0.sub(r'<div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
"""]

AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "srt:ProductOrServiceAxis",
 "extra": {},
 "members": {"us-gaap:BankServicingMember": ["거래 수수료", "#0052ff"], "us-gaap:SubscriptionAndCirculationMember": ["구독·서비스(USDC·스테이킹 등)", "#7da7ff"]},
 "ignore": []
}
