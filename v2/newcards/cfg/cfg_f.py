CIK = '0000037996'
BUILD = {'no_dcf': '미완성 — 최근 4분기 GAAP가 적자(EV 관련 손상·BlueOval SK 합작 처분 손실)', 'cover_shares': True,
         'dim_facts': [('us-gaap:DebtCurrent', 'us-gaap:StatementBusinessSegmentsAxis', 'f:CompanyExcludingFordCreditMember', 'DebtCurrentAutoF'),
                       ('us-gaap:LongTermDebtNoncurrent', 'us-gaap:StatementBusinessSegmentsAxis', 'f:CompanyExcludingFordCreditMember', 'LongTermDebtAutoF')]}
# F(포드) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 12월 31일. 포드 블루(내연·하이브리드), Model e(전기차), 포드 프로(상용), 금융 자회사 Ford Credit.
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-28 19:21 동부 접수 → 첫 세션 10-29, 카드 기준일 11-17 종가), 실적 보도자료(8-K 2.02항 — 모두 장 마감 뒤 16:07~16:12 동부 → 다음 날).
# 엔진 입력(2026-11-18): 차입금은 Ford Credit을 뺀 회사 몫만(GM·CAT·DE와 같은 규칙) — 재무상태표가 StatementBusinessSegmentsAxis로만 실어 BUILD dim_facts + DEBT_TOTAL_TAG.
#   Q3 2026 1년 안 $4,154M + 장기 $19,535M = $23,689M(회사 "Debt (excl. Ford Credit)" $23.7B와 같다), Ford Credit $139,393M 제외. 현금·시장성 증권은 연결 값(GM 선례).
#   표지 주식 수는 클래스별(보통주 + B주 70.85M — B주는 포드 가문 보유, 경제적 권리 같음)이라 cover_shares로 합산. 순이익 = 보통주 귀속(NetIncomeLoss 2025-06 멈춤 — EXTRA_TAGS).
#   EV/EBITDA 이력은 차원 차입금이 들어간 공시(2025-10-24)부터라 짧다(약 1년). 금융리스는 회사 차입금 안에 있어 따로 더하지 않는다(build_dcf·build_fundamental_score, Codex r1).
# 일회성(E54): 최근 4분기 GAAP 희석 EPS −1.97(−2.77 + 0.63 − 0.33 + 0.50) — 적자라 미완성. 회사 조정 EPS 1.70(0.13 + 0.66 + 0.42 + 0.49).
#   회사 특별 항목(세전): Q4 2025 약 $15.5B(Model e·EV 관련 손상·정리 — 연간 $17,356M − 9개월 $1,859M), 2026년 1분기 $0.2B, 2분기 $4.2B(BlueOval SK 합작 처분 $3.6B), 3분기 $0.1B.
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 1, 0), '판정 보류'
CO = 'Ford'
S_ = 'https://www.sec.gov/Archives/edgar/data/37996/'
SEC = S_
TENQ = S_ + '000003799626000191/f-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000003799626000190/exhibit99tooctober282026.htm', 'q2': S_ + '000003799626000155/exhibit99tojuly282026for.htm',
      'q1': S_ + '000003799626000084/exhibit99toapril292026fo.htm', 'q4': S_ + '000003799626000014/exhibit99tofebruary10202.htm',
      'ev': S_ + '000003799625000238/exhibit99todecember15202.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="fFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(최근 4분기 GAAP가 적자다)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (미완성 — 현금흐름 보류)</span>'
Y2 = (-30, 15)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('미완성 카드다. 이 카드는 최근 4분기 GAAP 이익이 적자이거나 일회성이 30% 이상이면 판정을 보류하는데, 포드는 최근 4분기 GAAP 희석 EPS가 −$1.97로 적자다. '
              '2025년 12월 전기차 전략을 바꾸며 잡은 2025년 4분기 특별 항목(세전 약 $15.5B — Model e 손상·EV 프로그램 취소 $10.7B, BlueOval SK(SK온과의 배터리 합작) 처분 $3.2B 등)과 2026년 2분기 BlueOval SK 추가 처분 손실($3.6B)이 크다. 회사 조정 EPS로는 최근 4분기 $1.70이다. '
              '이 조정 EPS에는 회사가 일회성이라 밝힌 2026년 1분기 관세(IEEPA) 환급 이익 $1.3B(1분기 조정 실효세율로 추정한 세후 주당 약 $0.27)가 들어 있고, 현금은 일부만 받았다. '
              '분기마다 GAAP 흑자 여부와 특별 항목 비중을 다시 센다. 2026년 4분기 실적(2027년 2월 예상)에서 손상이 든 2025년 4분기가, 2027년 2분기 실적(7월 말 예상)에서 합작 처분 손실이 든 2026년 2분기가 최근 4분기에서 빠진다. 그때마다 GAAP 흑자 여부와 일회성 비중(관세 환급 이익 같은 일회성 이익 포함)을 다시 세서 판단한다. 계획상 남은 EV 취소 비용과 연말 연금 재측정에 따라 해제가 더 늦어질 수 있다. '
              '차입금은 Ford Credit을 뺀 회사 몫($23.7B)만 넣었다 — Ford Credit의 차입금($139B)은 할부·리스 채권과 짝을 이룬 영업 자금이라 뺀다(GM·CAT과 같은 규칙). '
              '순현금은 연결 현금·증권(Ford Credit 몫 포함)에서 회사 몫 빚만 뺀 값이라 회사 전체의 무차입 여력이 아니다. 감가상각에는 Ford Credit 리스 차량 감가상각과 2025년 4분기 전기차(Model e) 자산 손상차손(약 $8.1B — 감가상각 집계에 포함)이 들어 있어 EBITDA가 크게 나오고 EV/EBITDA는 낮게 보인다. '
              '표지 주식 수는 보통주와 B주(포드 가문 보유 약 7,100만 주)를 더한 값이다.')
PH = ['GM', 'TSLA', 'APTV', 'BWA', 'LKQ', 'GPC']
PEER_FILE = 'peer_universe/consumer_discretionary.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '자동차·부품 6곳 PER 비교 (점수는 S&P500 경기소비재 기준)', 'pbr': '자동차 PBR 비교', 'psr': '자동차 PSR 비교',
                'pcr': '자동차 PCR(FCF) 비교', 'evebitda': '자동차 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 경기소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 경기소비재 대비 배수 순위 (v2/peer_universe/consumer_discretionary.json)'
PEER_TIP = ('S&P500 경기소비재(F 제외)와 배수 순위를 매긴 값이다.',
            '유통·외식·호텔·의류·자동차가 섞여 있어 자동차 회사는 배수가 늘 낮게 나온다 — 높은 점수가 곧 저평가를 뜻하지는 않는다. 차트에는 자동차·부품 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문, 외부 매출): 포드 블루 27,079 + 포드 프로 17,772 + Ford Credit 3,444 + Model e 1,223 = 49,518, 기타 8 → 49,526.
SEG = [('포드 블루(내연·하이브리드)', 27079.0, '#003478'), ('포드 프로(상용)', 17772.0, '#6f9fd8'), ('Ford Credit', 3444.0, '#9aa7b8'), ('Model e(전기차)', 1223.0, '#00a3e0')]
SEG_ADJ = 8
SEG_ADJ_LABEL = '기타'
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석) + EV 전략 전환·손상 발표. 반응일: 모두 장 마감 뒤(16:0x 동부) → 다음 날.
NEWS_RANGE = '2025.12 ~ 2026.10'
NEWS = [
    ('green', '2026년 10월 28일 장 마감 뒤 — Q3 2026 실적', '2026-10-29',
     '매출 $49.5B · 순이익 $2.0B · 희석 EPS $0.50(1년 전 $0.60) · 조정 EBIT $2.7B · 연간 조정 EBIT 전망 하단 상향($10.5~11B) — 다음 날 주가 +3.4%', 'q3', 'Ford 보도자료 (SEC 8-K)'),
    ('red', '2026년 7월 28일 장 마감 뒤 — Q2 2026 실적', '2026-07-29',
     '매출 $48.3B · 순손실 $1.3B(BlueOval SK 합작 처분 손실 $3.6B) · 희석 주당 손실 $0.33 · 조정 EBIT $2.5B · 연간 전망 상향 — 다음 날 주가 +2.1%', 'q2', 'Ford 보도자료 (SEC 8-K)'),
    ('green', '2026년 4월 29일 장 마감 뒤 — Q1 2026 실적', '2026-04-30',
     '매출 $43.3B · 순이익 $2.5B(관세 환급 이익 $1.3B 포함) · 희석 EPS $0.63 · 연간 조정 EBIT 전망 상향 — 다음 날 주가 −1.3%', 'q1', 'Ford 보도자료 (SEC 8-K)'),
    ('red', '2026년 2월 10일 장 마감 뒤 — 2025년 연간 실적', '2026-02-11',
     '4분기 순손실 $11.1B·희석 주당 손실 $2.77(EV 관련 특별 항목) · 연간 매출 $187.3B · 조정 EBIT $6.8B — 다음 날 주가 +2.1%', 'q4', 'Ford 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 12월 15일 장 마감 뒤 — 전기차 전략 전환·EV 관련 비용', '2025-12-16',
     '대형 전기차 대신 하이브리드·저가 전기차·배터리 저장 사업으로 전환, EV 관련 특별 항목 약 $19.5B 예상(대부분 2025년 4분기 — 실제 4분기 특별 항목은 약 $15.5B) — 다음 날 주가 +0.1%', 'ev', 'Ford 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 20, 'nt': 13, 'mean': 15.42, 'median': 15, 'low': 12, 'high': 20, 'sb': 5, 'b': 3, 'h': 12, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-18'

ONEOFF_QUARTERS = {'2025-12-31': '특별 항목 세전 약 $15.5B — Model e 손상·EV 프로그램 취소 $10.7B · BlueOval SK 처분 $3.2B · 연금 $0.7B 등',
                   '2026-03-31': '특별 항목 세전 약 $0.2B(관세 환급 이익 $1.3B는 회사 조정 EBIT 안)',
                   '2026-06-30': '특별 항목 세전 약 $4.2B — BlueOval SK 합작 처분 $3.6B',
                   '2026-09-30': '특별 항목 세전 순 약 $0.1B(비용 약 $0.5B — EV 취소·법률·유럽, 연금 재측정 이익 $0.3B)'}

INCOMPLETE_SHORT = 'GAAP 적자·EV 손상'
INCOMPLETE_WHY = '최근 4분기 GAAP EPS가 적자(−$1.97)이고 EV 관련 손상(2025년 4분기)과 BlueOval SK 합작 처분 손실(2025년 4분기·2026년 2분기)이 커서 배수 판정이 왜곡돼 보류한다. 분기마다 다시 세고, 주요 재검토는 2027년 2월(손상 분기가 빠질 때)·7월 말(처분 손실 분기가 빠질 때) 예상 실적'
POST = [r"""
import re as _re0
_w = '최근 4분기 GAAP EPS가 적자(−$1.97)이고 EV 관련 손상(2025년 4분기)과 BlueOval SK 합작 처분 손실(2025년 4분기·2026년 2분기)이 커서 배수 판정이 왜곡돼 보류한다. 분기마다 다시 세고, 주요 재검토는 2027년 2월(손상 분기가 빠질 때)·7월 말(처분 손실 분기가 빠질 때) 예상 실적'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — GAAP 적자·EV 손상 · 매 분기 재검토, 주요 확인 2027년 2월부터</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — GAAP 적자·EV 손상. 미완성 카드 규칙에 따라 종합 판정과 함께 현금흐름 내재가치도 보류했다.')
h = _re0.sub(r'(id="fFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)
h = _re0.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re0.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")
h = _re0.sub(r'(<div class="verdict-summary-head">[^<]*)<span class="tag">[^<]*</span>', r'\1<span class="tag">GAAP 적자·EV 손상</span>', h, count=1)
h = _re0.sub(r'<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
h = _re0.sub(r'<div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
# Codex r1: 순현금은 연결 현금(Ford Credit 몫 $9.0B 포함)에서 회사 몫 빚만 뺀 값이라 강점으로 쓰지 않는다
h = _re0.sub(r'(<span class="bb-head">부채</span><span class="bb-text">현금·단기투자가 차입금·리스보다 \$[0-9.]+B 많다\(순현금\))\.', lambda m: m.group(1) + ' — 다만 현금은 Ford Credit 몫을 포함한 연결 값이고 빚은 Ford Credit을 뺀 회사 몫이다. 회사 발표 기준으로는 회사 현금 $25.3B − 차입금(금융리스 제외) $22.4B = $2.9B다.', h, count=1)
"""]

AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"f:FordBlueMember": ["포드 블루(내연·하이브리드)", "#003478"], "f:FordProMember": ["포드 프로(상용)", "#6f9fd8"], "f:FordCreditMember": ["Ford Credit", "#9aa7b8"], "f:FordModelEMember": ["Model e(전기차)", "#00a3e0"]},
 "ignore": []
}
