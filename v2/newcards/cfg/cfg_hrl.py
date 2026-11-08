CIK = '0000048465'
BUILD = {'no_dcf': '미완성 — 사업 매각 손실·손상·소송 합의로 최근 4분기 GAAP 이익이 크게 낮다', 'cover_shares': True}   # 2026-11-07 사용자 규칙(D군 — 일회성 30% 이상이면 미완성 카드)
# HRL(호멜 푸드) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 10월 마지막 일요일(FY26 = 2026-10-25). 리테일(SPAM·Planters·Skippy·Applegate 등), 외식(Foodservice), 해외.
# 출처: SEC XBRL, Q3 FY26 10-Q(2026-08-27 14:06 동부 장중 → 그날, 카드 기준일 11-06 종가),
#        실적 보도자료(8-K 2.02항 — 접수는 전날 17:3x~18:3x 동부라 공개는 다음 날 장 전 → 그날), Q1 예비 실적(2026-02-17 19:45 동부 → 02-18), Brakebush 인수 계약(09-30 06:45 동부 → 그날).
# 엔진 입력(2026-11-07): 차입금 $2,855.1M = 1년 안 만기 $505.6M + 장기 $2,349.5M(LongTermDebtAndCapitalLeaseObligationsIncludingCurrentMaturities), 현금 $839.6M + 단기 증권 $28.8M.
#   주식 수는 10-Q 표지 값(2026-08-23 현재 550,350,800주, cover_shares — companyfacts에 발행주식 수 태그가 없어 PSR·PBR·PCR·EV/EBITDA가 계산 불가였다).
#   이자비용 InterestExpenseNonoperating·매출채권 AccountsAndOtherReceivablesNetCurrent(CONCEPTS_BY_CIK — 기본 태그가 2024-04·2026-01에 멈춤).
# 일회성(E54 규칙): 최근 4분기 GAAP 희석 EPS 0.63(Q4 FY25 −0.10, Q1 0.33, Q2 0.29, Q3 0.11) 대 회사 조정 EPS 1.43(0.32 + 0.34 + 0.40 + 0.37) — 차이 0.80(GAAP의 약 127%).
#   Q4 FY25 손상 $234M(인도네시아 Garudafood 지분 투자·리테일 무형자산), Q2 통칠면조 사업 매각 손실 $61.0M, Q3 브라질(Ceratti) 매각 손실 $57.4M·인도네시아 지분 투자 손상 $48.2M·반독점 소송 합의 $37.5M, 매 분기 T&M 비용.
CUR, YO, QO = '2026-07-26', '2025-07-27', '2026-04-26'
QLABEL, YL, QQL = 'Q3 FY26', 'Q3 FY25', 'Q2 FY26'
L8 = ['Q4 FY24', 'Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26']
FY_ENDS, FY_LABEL = ('2025-10-26', '2024-10-27'), 'FY2025'
VOTES, VERDICT = (0, 0, 0), '판정 보류'
CO = 'Hormel Foods'
S_ = 'https://www.sec.gov/Archives/edgar/data/48465/'
SEC = S_
TENQ = S_ + '000004846526000055/hrl-20260726.htm'; TENQ_NAME = 'Q3 FY26 10-Q'
PR = {'q3': S_ + '000004846526000053/hormelearningsreleaseq32026.htm', 'q2': S_ + '000004846526000024/hormelearningsreleaseq22026.htm',
      'q1': S_ + '000004846526000018/hormelearningsreleaseq12026.htm', 'q4': S_ + '000004846525000056/hrlearningsrelease2025q4.htm',
      'prelim': S_ + '000004846526000013/exhibit991-2172026.htm', 'brakebush': S_ + '000110465926112101/tm2626547d1_ex99-1.htm',
      'ceo': S_ + '000004846526000047/hrl-20260727.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="hrlFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(사업 매각 손실·손상·소송 합의로 최근 4분기 GAAP 이익이 크게 낮다)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (-5, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('미완성 카드다. 최근 4분기 GAAP 희석 EPS 합계는 약 $0.63인데, 회사가 핵심 이익에서 빼는 항목을 빼면 조정 EPS는 약 $1.43이라 차이가 GAAP 이익보다 크다. '
              '회사 조정 EPS로 보면 PER은 5년 최저 수준이지만, GAAP로는 5년 최고 수준이라 어느 쪽으로도 판정하지 않는다. '
              '차이의 대부분은 사업 정리에서 나왔다 — 2025 회계연도 4분기에 인도네시아 Garudafood 지분 투자와 리테일 무형자산 손상 $234M(비현금)이 잡혀 분기 희석 EPS가 −$0.10이었고, '
              '2026 회계연도에는 2분기 통칠면조 사업 매각 손실 $61M, 3분기 브라질 Ceratti 사업 매각 손실 $57M(7월 말 매각 완료)과 Garudafood 추가 손상 $48M, 칠면조 가격 담합 소송의 직접 구매자 집단과 맺은 합의 $37.5M(법원 승인 대기)이 이어졌다. '
              '1분기에는 Justin’s 지분 51% 매각 이익 $22M이 구조조정(약 250명)·전 CEO 자문 계약·사업 혁신 비용과 거의 상쇄됐고, 사업 혁신(Transform and Modernize) 비용은 분기마다 들어간다(2025 회계연도 4분기 $19M, 2026 회계연도 1~3분기 $11~16M). '
              'Garudafood 남은 장부가 $184M은 인도네시아 상장 주가 그대로라 주가가 더 빠지면 또 손상될 수 있고, 칠면조 소송은 간접 구매자 집단·개별 원고 소송이 남아 있다(충당금 없음). '
              '아래 약세 요인의 영업이익률·차입 배수도 이 일회성을 포함한 GAAP 기준이다 — 조정 영업이익으로 보면 최근 4분기 영업이익률은 약 8.7%로 5년 중앙값과 비슷하다. '
              '본업은 엇갈린다 — 외식 부문은 3분기에도 매출·이익이 늘었지만, 리테일은 칠면조 시세 하락과 비핵심 자체상표 견과 철수로 물량이 9% 줄었다. '
              '회사는 3분기 실적과 함께 2026 회계연도 매출 전망을 $12.1~12.2B로 낮추고 조정 EPS 전망은 $1.45~1.51로 올렸다(GAAP EPS 전망 $1.06~1.12). '
              '9월에 가공 닭고기 회사 Brakebush(최근 1년 매출 약 $1.2B)를 약 $1.055B 현금에 사기로 했다 — 2027 회계연도 1분기 마감 예정, 조정 EPS에는 2028 회계연도부터 보탬이 된다고 봤다. 1년 안 만기 채권 $500M도 있어 차입금은 당분간 늘 가능성이 크다. '
              '경영진도 바뀌었다 — 2025년 6월부터 임시 CEO였던 Jeff Ettinger에 이어 John Ghingo 사장이 2026년 10월 26일 CEO가 됐고, 9월에 Tyson 닭고기 부문 CFO 출신 Ash Bhumbla가 CFO로 왔다. 분기 배당은 주당 $0.2925다. '
              '12월 초 4분기 실적으로는 보류가 풀리지 않을 가능성이 크다 — 회사 2026 회계연도 전망대로면 GAAP와 조정 EPS 차이가 여전히 GAAP의 약 36%다. '
              '2026년 2·3분기 손실이 최근 4분기에서 빠지는 2027년 5~8월 실적 뒤, 일회성 차이가 GAAP 이익의 30% 아래면 정식 판정으로 다시 본다(그 전에 Brakebush 인수 비용이 새 일회성으로 들어올 수 있다).')
CHECK_DEBT = {'2026-07-26': 'Brakebush 인수 대금($1.055B) 조달과 1년 안 만기 채권 $500M 상환 방식 — 차입금 {debt}이 얼마나 늘어나는지'}
PH = ['TSN', 'GIS', 'SJM', 'KHC', 'MKC', 'MDLZ']
PEER_FILE = 'peer_universe/consumer_staples.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '포장식품 6곳 PER 비교 (점수는 S&P500 필수소비재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 필수소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 필수소비재 대비 배수 순위 (v2/peer_universe/consumer_staples.json)'
PEER_TIP = ('S&P500 필수소비재(HRL 제외)와 배수 순위를 매긴 값이다.',
            '식품·음료·생활용품·유통이 섞여 있다. 차트에는 포장식품 6곳만 보인다.')
# 매출(Q3 FY26 보도자료 부문 표): 리테일 1,779.4 + 외식 1,003.2 + 해외 178.7 = 2,961.3.
SEG = [('리테일(SPAM·Planters·Skippy 등)', 1779.4, '#c8102e'), ('외식(Foodservice)', 1003.2, '#1f3a68'), ('해외', 178.7, '#f3d0d6')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 실적 4건 + Q1 예비 실적·통칠면조 매각 + CEO 선임 + Brakebush 인수. 반응일 — 실적 보도자료는 전날 저녁 접수·당일 아침 공개라 그날.
NEWS_RANGE = '2025.12 ~ 2026.09'
NEWS = [
    ('neutral', '2026년 9월 30일 장 전 — Brakebush 인수 계약', '2026-09-30',
     '가공 닭고기 회사 Brakebush를 약 $1.055B에 인수 — 외식 부문 강화, 2027 회계연도 1분기 마감 예정 — 그날 주가 +0.5%', 'brakebush', 'Hormel Foods 보도자료 (SEC 8-K)'),
    ('red', '2026년 8월 27일 장 전 — Q3 FY26 실적', '2026-08-27',
     '매출 $2.96B(−2.4%) · 희석 EPS $0.11(1년 전 $0.33) · 조정 EPS $0.37 — 브라질 매각 손실·인도네시아 손상·소송 합의 · 연간 매출 전망 $12.1~12.2B로 하향, 조정 EPS 전망 $1.45~1.51로 상향 — 그날 주가 −10.2%', 'q3', 'Hormel Foods 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 7월 28일 장 전 — John Ghingo CEO 선임', '2026-07-28',
     '사장 John Ghingo를 10월 26일부터 CEO로 — 임시 CEO Jeff Ettinger는 10월 25일 퇴임(이사회에는 남음) — 그날 주가 −1.9%', 'ceo', 'Hormel Foods 공시 (SEC 8-K)'),
    ('green', '2026년 5월 28일 장 전 — Q2 FY26 실적', '2026-05-28',
     '매출 $2.97B · 희석 EPS $0.29 · 조정 EPS $0.40 — 통칠면조 사업 매각 손실 $61M · 세 부문 모두 매출·이익 증가 — 그날 주가 +12.5%', 'q2', 'Hormel Foods 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 26일 장 전 — Q1 FY26 실적', '2026-02-26',
     '매출 $3.03B · 희석 EPS $0.33 · 조정 EPS $0.34(예비 실적과 같음) — 그날 주가 −1.9%', 'q1', 'Hormel Foods 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 17일 장 마감 뒤 — Q1 예비 실적·통칠면조 사업 매각 계약', '2026-02-18',
     'Q1 매출 약 $3B · 희석 EPS $0.33 · 조정 EPS $0.34 예상, 조정 EPS 연간 전망 유지 · 통칠면조 사업 매각 계약 — 다음 날 주가 +4.4%', 'prelim', 'Hormel Foods 보도자료 (SEC 8-K)'),
    ('green', '2025년 12월 4일 장 전 — 2025 회계연도 실적', '2025-12-04',
     '4분기 매출 $3.2B · 희석 EPS −$0.10(비현금 손상 $234M) · 조정 EPS $0.32 · 연간 희석 EPS $0.87 · 조정 $1.37 — 그날 주가 +3.8%', 'q4', 'Hormel Foods 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 10, 'nt': 7, 'mean': 25.14, 'median': 24, 'low': 23, 'high': 29, 'sb': 1, 'b': 2, 'h': 7, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-08'

# 미완성 카드 표시(2026-11-07 사용자 규칙, D·SRE 방식).
INCOMPLETE_SHORT = '일회성 손실로 이익 왜곡'
INCOMPLETE_WHY = '최근 4분기 GAAP 이익에 사업 매각 손실·지분 투자와 무형자산 손상·소송 합의 같은 일회성 비용이 커서 회사 조정 이익의 절반에 못 미친다 — 배수 판정이 왜곡돼 보류한다. 이 비용이 최근 4분기에서 빠지면 다시 본다'
POST = [r"""
import re as _re0
_w = '최근 4분기 GAAP 이익에 사업 매각 손실·지분 투자와 무형자산 손상·소송 합의 같은 일회성 비용이 커서 회사 조정 이익의 절반에 못 미친다 — 배수 판정이 왜곡돼 보류한다. 이 비용이 최근 4분기에서 빠지면 다시 본다'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — 일회성 손실로 이익 왜곡</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — 일회성 손실로 이익 왜곡. 미완성 카드 규칙에 따라 종합 판정과 함께 현금흐름 내재가치도 보류했다.')
h = _re0.sub(r'(id="hrlFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)
h = _re0.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re0.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")
h = _re0.sub(r'(<div class="verdict-summary-head">[^<]*)<span class="tag">[^<]*</span>', r'\1<span class="tag">일회성 손실로 이익 왜곡</span>', h, count=1)
h = _re0.sub(r'<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
h = _re0.sub(r'<div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
"""]


# ── 자동 카드 — 부문 지도(seg_map_propose 뒤 원문 대조). 원문: Q3 FY26 보도자료 리테일 1,779.4 + 외식 1,003.2 + 해외 178.7 = 2,961.3 ──
AUTO = True
BB_NONE = {'2026-07-26': '없음 · 10-Q 주석'}   # 현금흐름표 매입 줄·태그 없음 — Q3 FY26 10-Q "did not repurchase any shares during the first nine months of fiscal 2026", 남은 승인 3,677,494주. 새 10-Q마다 주석 확인
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerIncludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"hrl:RetailSegmentMember": ["리테일(SPAM·Planters·Skippy 등)", "#c8102e"],
             "hrl:FoodserviceSegmentMember": ["외식(Foodservice)", "#1f3a68"],
             "hrl:InternationalSegmentMember": ["해외", "#f3d0d6"]}
}
