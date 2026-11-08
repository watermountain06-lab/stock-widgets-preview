BUILD = {'no_dcf': '미완성 — 주식 수 이력 처리 대기'}   # 2026-11-03 사용자 결정 — 미완성 카드(판정 보류)
# CCL(카니발) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 11월 30일. 크루즈 — 북미(카니발·프린세스·홀랜드 아메리카 등)·유럽(코스타·AIDA·P&O 등).
# 출처: SEC XBRL, Q3 FY26 10-Q(2026-09-29), 실적 보도자료(Q4 FY25~Q3 FY26, 8-K 2.02항 — 장 전 09:16 동부 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/CCL.md.
# 미완성 사유: 2026-05-07 Carnival Corporation·plc 이중 상장(DLC) 단일화 — 그 전 주식 수 이력이 Corporation 주식만 세어 plc 약 1.88억 주가 빠진다. 자기 이력 배수가 그만큼 싸 보인다.
# share_adjust.json은 '빼기만' 규칙이라 더할 수 없다. 2026-11-03 사용자 결정: 미완성 카드. 보류 전 점수: 자기 이력 44.9, 동종업 77.9.
# 입력: 차입금 $23.9B, 현금 $1.2B, 운용리스 $1.25B, 주식 1,344.6M(2026-09). Q4 FY21~FY25 EPS는 보도자료 값(Q4_EPS_OVERRIDE).
CIK = '0000815097'
CUR, YO, QO = '2026-08-31', '2025-08-31', '2026-05-31'
QLABEL, YL, QQL = 'Q3 FY26', 'Q3 FY25', 'Q2 FY26'
L8 = ['Q4 FY24', 'Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26']
FY_ENDS, FY_LABEL = ('2025-11-30', '2024-11-30'), 'FY2025'
VOTES, VERDICT = (0, 1, 0), '판정 보류'
CO = 'Carnival'
S_ = 'https://www.sec.gov/Archives/edgar/data/815097/'
SEC = S_
TENQ = S_ + '000081509726000107/ccl-20260831.htm'; TENQ_NAME = 'Q3 FY26 10-Q'
PR = {'q3': S_ + '000081509726000104/a20263qearningsrelease8-k.htm', 'q2': S_ + '000081509726000086/a20262qearningsrelease8-k.htm', 'q1': S_ + '000081509726000034/a20261qearningsrelease8-k.htm', 'q4': S_ + '000162828025058106/a20254qearningsrelease8-k.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="cclFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {pct(HIST[\'margin_now\'])})</span>'
Y2 = (0, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('2026년 5월 Carnival Corporation과 plc가 한 회사로 합쳤다. 그 전 주식 수 기록에 plc 몫(약 1.9억 주)이 빠져 있어 과거 배수가 실제보다 낮게 잡힌다. '
              '그래서 자기 이력 점수는 참고로만 둔다. 동종업 점수는 S&P500 경기소비재 기준이다.')
PH = ['RCL', 'NCLH', 'BKNG', 'EXPE', 'MAR', 'HLT']
PEER_FILE = 'peer_universe/consumer_discretionary.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '크루즈·여행 6곳 PER 비교 (점수는 S&P500 경기소비재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 경기소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 경기소비재 대비 배수 순위 (v2/peer_universe/consumer_discretionary.json)'
PEER_TIP = ('S&P500 경기소비재(CCL 제외)와 배수 순위를 매긴 값이다.',
            '자동차·주택·외식·호텔·소매가 섞여 있다. 차트에는 크루즈·여행 6곳만 보인다.')
# 매출(Q3 FY26 10-Q 상품 축) — 승객 티켓 5,529 + 선내·기타 2,906 = 8,435(연결과 일치).
SEG = [('승객 티켓', 5529, '#004b8d'), ('선내·기타', 2906, '#e31837')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 티켓·선내(Q3 FY26)'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 전 발표(09:16 동부) → 같은 날.
NEWS_RANGE = '2025.12 ~ 2026.09'
NEWS = [
    ('green', '2026년 9월 29일 장 전 — Q3 FY26 실적', '2026-09-29',
     '매출 $8.44B(+3.5%) · 순이익 $1.92B · 희석 EPS $1.40(1년 전 $1.33) · 조정 EPS $1.43 — 당일 주가 +13.4%', 'q3', 'Carnival 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 6월 23일 장 전 — Q2 FY26 실적', '2026-06-23',
     '매출 $6.66B(+5.3%) · 순이익 $537M · 희석 EPS $0.39(1년 전 $0.42) · 조정 EPS $0.41 — 당일 주가 −4.9%', 'q2', 'Carnival 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 3월 27일 장 전 — Q1 FY26 실적', '2026-03-27',
     '매출 $6.17B(+6.1%) · 순이익 $258M · 희석 EPS $0.19(1년 전 −$0.06) · 조정 EPS $0.20 — 당일 주가 −4.3%', 'q1', 'Carnival 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 12월 19일 장 전 — Q4 FY25 실적', '2025-12-19',
     '매출 $6.33B(+6.6%) · 순이익 $422M · 희석 EPS $0.31(1년 전 $0.23) · FY25 EPS $2.02 — 당일 주가 +9.8%', 'q4', 'Carnival 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 30, 'nt': 21, 'mean': 32.89, 'median': 34, 'low': 1.45, 'high': 42, 'sb': 18, 'b': 6, 'h': 6, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-08'


# 미완성 카드 표시(2026-11-03 사용자 결정 — C·D·E 보류 카드는 있는 자료로 만들고 판정 보류 + 이유를 잘 보이게, SPCX 방식). BUILD no_dcf가 판정을 보류로 만들고, 보험사용 문구를 미완성 사유로 바꾼다.
INCOMPLETE_SHORT = '주식 수 이력 처리 대기'
INCOMPLETE_WHY = '2026-05 Carnival plc와 합치기 전 주식 수 기록에 plc 몫(약 1.9억 주)이 빠져 과거 배수가 틀린다 — 주식 수 이력을 바로잡을 때까지 보류'
POST = [r"""
_w = '2026-05 Carnival plc와 합치기 전 주식 수 기록에 plc 몫(약 1.9억 주)이 빠져 과거 배수가 틀린다 — 주식 수 이력을 바로잡을 때까지 보류'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — 주식 수 이력 처리 대기</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — 주식 수 이력 처리 대기. 현금흐름 내재가치는 계산하지 않았다.')
import re as _re3
h = _re3.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re3.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")   # 툴팁이 '계산 불가 — 미완성 — …'로 겹쳤다(Codex 2026-11-03)
"""]


# ── 자동 카드 — 부문(축 하나만 붙은 값). 원문 대조: Q3 FY26 5,529/2,906(2026-11-03) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "srt:ProductOrServiceAxis",
 "extra": {},
 "members": {"ccl:CruisePassengerTicketMember": ["승객 티켓", "#004b8d"], "ccl:CruiseOnboardAndOtherMember": ["선내·기타", "#e31837"]},
 "ignore": []
}
