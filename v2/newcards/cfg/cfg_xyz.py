CIK = '0001512673'
BUILD = {'no_dcf': '미완성 — 최근 4분기 일회성(충당·구조조정·비트코인 평가 등)이 GAAP 순이익의 수 배', 'cover_shares': True}
# XYZ(블록) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 12월 31일. Square(가맹점 결제·소프트웨어)·Cash App(개인 송금·카드·대출)·Afterpay·비트코인.
# 출처: SEC XBRL, Q3 2026 10-Q(2026-11-03 16:16 동부 접수 → 첫 세션 11-04, 카드 기준일 11-18 종가), 주주 서한·실적 보도자료(8-K 2.02항 — 모두 장 마감 뒤 16:1x 동부 → 다음 날).
# 엔진 입력(2026-11-19): 차입금 = 1년 안 0 + 담보 차입 $447M + 장기 신용한도 $1,096M + 장기 채권 $5,723M = $7,266M(DEBT_TOTAL_TAG), 단기투자 = 단기 채권투자 $385M(DebtSecuritiesAvailableForSaleExcludingAccruedInterestCurrent, EV_TAGS), 표지 주식 수 A + B(cover_shares).
#   현금 $7.9B에 고객 예치금($5.4B, 별도 줄)은 들어 있지 않다. 비트코인 보유 $772M은 비영업 자산으로 더하지 않았다.
# 2023 EPS: 1~3분기는 처음 공시 값(−0.03·−0.20·−0.05), 연간은 재작성 뒤 값이라 Q4 2023 역산이 섞인다 — PER은 순이익률 2% 미만이라 점수에서 빠져 판정 영향 없음(Codex r1).
# 일회성(E54): 최근 4분기 GAAP 순이익 $461.2M(115.8 − 308.7 + 88.5 + 565.6), 희석 EPS 0.74(0.19 − 0.52 + 0.15 + 0.92) 대 회사 조정 순이익 $2,231M(조정 EPS 0.65 + 0.85 + 1.02 + 1.13 = 3.65).
#   세전 조정: 충당·구조조정 1,597(54·743·365·435 — 인력 감축 $495M + 소송·규제 충당), 구조조정 주식보상 127, 비트코인 평가손 265(234·173·88·−230), 지분 평가 11 — 세금 효과 뒤에도 GAAP의 3배 넘음 → 미완성.
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, 0, 0), '판정 보류'
CO = 'Block'
S_ = 'https://www.sec.gov/Archives/edgar/data/1512673/'
SEC = S_
TENQ = S_ + '000162828026069524/xyz-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000162828026069513/q32026shareholderletter.htm', 'q2': S_ + '000119312526335117/d91486dex991.htm',
      'q1': S_ + '000119312526212032/d132441dex991.htm', 'q4': S_ + '000119312526076557/d108590dex991.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="xyzFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(최근 4분기 일회성이 GAAP 이익의 수 배다)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (미완성 — 현금흐름 보류)</span>'
Y2 = (-10, 15)
ACT_REASON = '결제 회사라 재고·매출채권 회전으로 보는 활동성이 잘 맞지 않는다'
NONOP_WHAT = '투자'
MODEL_NOTE = ('미완성 카드다. 이 카드는 최근 4분기 GAAP 이익이 적자이거나 일회성이 30% 이상이면 판정을 보류하는데, 블록은 최근 4분기 GAAP 순이익 $461M(희석 EPS $0.74)보다 회사가 조정에서 빼는 항목이 훨씬 크다. '
              '회사가 "충당·구조조정·기타"로 빼는 비용이 최근 4분기 세전 $1.6B다 — 대부분 소송·규제 충당(미국 법무부(DOJ) 자금세탁방지 건은 10월 원칙적 합의(최종 계약·법원 승인 전)에 따른 예상 순지급액 약 $764M을 충당했고 아직 내지 않았다)이고, 2026년 2월 인력을 40% 넘게 줄인 구조조정 비용도 들어 있다(전체 $495M 가운데 주식보상 $104.7M은 별도 줄). 보유 비트코인($772M) 평가손익도 분기마다 이익을 흔든다(3분기는 평가이익 $230M). 회사 조정 EPS로는 최근 4분기 $3.65다. '
              '분기마다 다시 센다. 인력 감축 계획은 2분기에 끝났지만 소송·규제 충당은 3분기에도 나왔고, 회사는 DOJ 건 손실이 충당액을 넘을 수 있다고 밝혔다. 2027년 1분기 실적(5월 예상)에도 2·3분기 충당·구조조정·기타($800M)가 남아, 지금 이익 규모라면 2026년 2분기가 빠지는 2027년 2분기 실적(8월 예상) 무렵부터 해제를 다시 볼 수 있다 — 새 충당이나 큰 비트코인 평가손이 나오면 더 늦어진다. '
              '매출에는 비트코인 판매 매출(3분기 $1.8B)이 크게 들어 있는데 이익률이 아주 낮아, 회사는 매출보다 매출총이익을 본다 — PSR이 낮게 보이는 이유다. 현금 $7.9B에는 고객 예치금(별도 $5.4B)이 들어 있지 않다. 순현금은 아직 내지 않은 소송 충당(9월 말 $981M)을 빼지 않은 값이다. EV/EBITDA도 일회성 $1.7B가 EBITDA를 깎아 높게 나온다. 주식 수는 클래스 A와 B를 더한 값이다.')
PH = ['PYPL', 'FIS', 'FISV', 'V', 'MA', 'COIN']
PEER_FILE = 'peer_universe/payments_exchanges.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '결제·핀테크 6곳 PER 비교 (점수는 결제·거래소 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = '결제·거래소 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = '결제·거래소 대비 배수 순위 (v2/peer_universe/payments_exchanges.json)'
PEER_TIP = ('결제·거래소 무리(XYZ 제외)와 배수 순위를 매긴 값이다.',
            '카드 네트워크·결제 대행·거래소가 섞여 있다. 비트코인 판매 매출 때문에 블록의 PSR은 낮게 나온다. 차트에는 결제·핀테크 6곳이 보인다.')
# 매출(Q3 2026 10-Q 제품·서비스 축): 커머스(가맹점 결제·소프트웨어 등) 3,475.9 + 비트코인 1,803.8 + 금융 서비스(Cash App 카드·대출·이자 등) 1,439.6 = 6,719.4(본사 51.8 포함 연결 6,719.4).
SEG = [('커머스(결제·소프트웨어·Cash App 수수료 등)', 3475.9, '#111111'), ('비트코인', 1803.8, '#f7931a'), ('금융 서비스(Cash App 카드·대출 등)', 1439.6, '#00d64f')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 제품·서비스별'
NEWS_RANGE = '2026.02 ~ 2026.11'
NEWS = [
    ('green', '2026년 11월 3일 장 마감 뒤 — Q3 2026 실적', '2026-11-04',
     '매출 $6.72B · 희석 EPS $0.92(1년 전 $0.74, 충당·구조조정·기타 $435M과 비트코인 평가이익 $230M 포함) · 조정 EPS $1.13 · 연간 전망 상향 — 다음 날 주가 +15.3%', 'q3', 'Block 주주 서한 (SEC 8-K)'),
    ('red', '2026년 8월 5일 장 마감 뒤 — Q2 2026 실적', '2026-08-06',
     '희석 EPS $0.15(1년 전 $0.87, 충당·구조조정 $365M) · 조정 EPS $1.02 — 다음 날 주가 −6.2%', 'q2', 'Block 주주 서한 (SEC 8-K)'),
    ('red', '2026년 5월 7일 장 마감 뒤 — Q1 2026 실적', '2026-05-08',
     '영업손실 $172M(구조조정·소송 충당 $852M) · 희석 주당 손실 $0.52 · 조정 EPS $0.85(+52%) — 다음 날 주가 +6.7%', 'q1', 'Block 주주 서한 (SEC 8-K)'),
    ('neutral', '2026년 2월 26일 장 마감 뒤 — 2025년 연간 실적·인력 40% 감축', '2026-02-27',
     '4분기 희석 EPS $0.19 · 조정 EPS $0.65 · 인력 40% 넘게 줄이는 구조조정 발표 — 다음 날 주가 +16.8%', 'q4', 'Block 주주 서한·8-K (SEC)'),
]
ANALYST = {'rating': 'Buy', 'n': 48, 'nt': 38, 'mean': 98.76, 'median': 102, 'low': 55, 'high': 125, 'sb': 29, 'b': 10, 'h': 9, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-23'

INCOMPLETE_SHORT = '일회성이 GAAP 이익의 수 배'
INCOMPLETE_WHY = '최근 4분기 GAAP 순이익 $461M(희석 EPS $0.74)보다 회사가 조정에서 빼는 항목이 훨씬 크다 — 소송·규제 충당과 인력 40% 감축 구조조정(세전 $1.6B), 비트코인 평가손실 등. 무형자산 상각을 반복 비용으로 쳐도 일회성이 GAAP 이익의 3배가 넘어 배수 판정이 왜곡돼 보류한다. 분기마다 다시 센다'
POST = [r"""
import re as _re0
_w = '최근 4분기 GAAP 순이익 $461M(희석 EPS $0.74)보다 회사가 조정에서 빼는 항목이 훨씬 크다 — 소송·규제 충당과 인력 40% 감축 구조조정(세전 $1.6B), 비트코인 평가손실 등. 무형자산 상각을 반복 비용으로 쳐도 일회성이 GAAP 이익의 3배가 넘어 배수 판정이 왜곡돼 보류한다. 분기마다 다시 센다'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — 일회성이 GAAP 이익의 수 배 · 매 분기 재검토</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — 일회성이 GAAP 이익의 수 배. 미완성 카드 규칙에 따라 종합 판정과 함께 현금흐름 내재가치도 보류했다.')
h = _re0.sub(r'(id="xyzFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)
h = _re0.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re0.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")
h = _re0.sub(r'(<div class="verdict-summary-head">[^<]*)<span class="tag">[^<]*</span>', r'\1<span class="tag">일회성이 GAAP 이익의 수 배</span>', h, count=1)
h = _re0.sub(r'<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
h = _re0.sub(r'<div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
"""]

# Fable r1: 순현금 강점 줄 — 미지급 소송 충당($981M, DOJ 순 $764M)을 빼지 않은 값이다
POST.append(r"""
import re as _re5
h = _re5.sub(r'(<span class="bb-head">부채</span><span class="bb-text">현금·단기투자가 차입금·리스보다 \$[0-9.,]+[BM] 많다\(순현금\))\.', lambda m: m.group(1) + ' — 다만 아직 내지 않은 소송 충당(9월 말 $981M — DOJ 원칙적 합의 예상 순지급 약 $764M 포함)을 빼면 순차입이다.', h, count=1)
""")

AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "srt:ProductOrServiceAxis",
 "extra": {},
 "members": {"xyz:CommerceEnablementMember": ["커머스(결제·소프트웨어·Cash App 수수료 등)", "#111111"], "xyz:BitcoinEcosystemMember": ["비트코인", "#f7931a"], "xyz:FinancialSolutionsMember": ["금융 서비스(Cash App 카드·대출 등)", "#00d64f"]},
 "ignore": []
}
