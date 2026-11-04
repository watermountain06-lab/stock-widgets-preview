BUILD = {'no_dcf': '미완성 — 매출 구성 장치 대기'}   # 2026-11-03 사용자 결정 — 미완성 카드(판정 보류)
# ULTA(얼타 뷰티) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 1월 말에 가까운 토요일(52/53주). 뷰티 전문 소매, 단일 보고 부문(매장·살롱·온라인, 2025-07 영국 Space NK 인수).
# 출처: SEC XBRL, Q2 FY26 10-Q(2026-08-27), 실적 보도자료(Q3 FY25~Q2 FY26, 8-K 2.02항 — 장 마감 뒤 16:07 동부 → 다음 날 반응), StockAnalysis. 사전 조사 scratchpad pre/ULTA.md.
# 미완성 사유: 품목별 매출을 금액 없이 정수 비중(%)으로만 공시(코스메틱 37·스킨케어 24·헤어 20·향수 13·서비스 4·기타 2) — 자동 카드 매출 구성 장치가 처리 못 함(FSLR과 같은 E 장치).
# 2026-11-03 사용자 결정: 미완성 카드. 빌드는 '매출 전체' 한 줄(차원 없는 us-gaap:Revenues)로 통과시킨다. 입력값(현금 $158.5M·단기투자 $55.0M·단기차입 $339.6M·운용리스 $2,184.5M·주식 42.76M)은 원문과 일치.
# Q4 FY21~FY25 EPS는 보도자료 값(Q4_EPS_OVERRIDE). 보류 전 점수: 자기 이력 29.5, 동종업 41.5.
CIK = '0001403568'
CUR, YO, QO = '2026-08-01', '2025-08-02', '2026-05-02'
QLABEL, YL, QQL = 'Q2 FY26', 'Q2 FY25', 'Q1 FY26'
L8 = ['Q3 FY24', 'Q4 FY24', 'Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26']
FY_ENDS, FY_LABEL = ('2026-01-31', '2025-02-01'), 'FY2025'
VOTES, VERDICT = (-1, 0, 0), '판정 보류'
CO = 'Ulta Beauty'
S_ = 'https://www.sec.gov/Archives/edgar/data/1403568/'
SEC = S_
TENQ = S_ + '000110465926102442/ulta-20260801x10q.htm'; TENQ_NAME = 'Q2 FY26 10-Q'
PR = {'q2': S_ + '000110465926102438/ulta-20260827xex99d1.htm', 'q1': S_ + '000110465926069464/ulta-20260602xex99d1.htm', 'q4': S_ + '000110465926027061/ulta-20260312xex99d1.htm', 'q3': S_ + '000110465925118457/ulta-20251204xex99d1.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="ultaFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {pct(HIST[\'margin_now\'])})</span>'
Y2 = (0, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('품목별 매출을 금액 없이 비중(%)으로만 공시한다(코스메틱 37%·스킨케어 24%·헤어 20%·향수 13%·서비스 4%·기타 2%, Q2 FY26). '
              '그래서 매출 구성은 전체 한 줄로만 보인다. 동종업 점수는 S&P500 경기소비재 기준이다.')
PH = ['TJX', 'ROST', 'BBY', 'TSCO', 'WSM', 'LULU']
PEER_FILE = 'peer_universe/consumer_discretionary.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '소매 6곳 PER 비교 (점수는 S&P500 경기소비재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 경기소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 경기소비재 대비 배수 순위 (v2/peer_universe/consumer_discretionary.json)'
PEER_TIP = ('S&P500 경기소비재(ULTA 제외)와 배수 순위를 매긴 값이다.',
            '자동차·주택·외식·호텔·소매가 섞여 있다. 차트에는 소매 6곳만 보인다.')
# 매출(Q2 FY26 10-Q) — 단일 부문 3,035.7.
SEG = [('매출 전체(단일 부문)', 3035.7, '#f26b21')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 단일 부문(Q2 FY26)'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 마감 뒤 발표(16:07 동부) → 다음 날.
NEWS_RANGE = '2025.12 ~ 2026.08'
NEWS = [
    ('red', '2026년 8월 27일 장 마감 뒤 — Q2 FY26 실적', '2026-08-28',
     '매출 $3.04B(+8.9%) · 순이익 $282M · 희석 EPS $6.55(1년 전 $5.78) · FY26 EPS 전망 $28.70~29.00로 상향 — 다음 날 주가 −4.2%', 'q2', 'Ulta Beauty 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 6월 2일 장 마감 뒤 — Q1 FY26 실적', '2026-06-03',
     '매출 $3.16B(+11.1%) · 순이익 $340M · 희석 EPS $7.74(1년 전 $6.70) · 전망 상향 — 다음 날 주가 −4.8%', 'q1', 'Ulta Beauty 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 3월 12일 장 마감 뒤 — Q4 FY25 실적', '2026-03-13',
     '매출 $3.90B(+11.8%) · 순이익 $357M · 희석 EPS $8.01(1년 전 $8.46) · FY25 EPS $25.64 — 다음 날 주가 −14.2%', 'q4', 'Ulta Beauty 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 12월 4일 장 마감 뒤 — Q3 FY25 실적', '2025-12-05',
     '매출 $2.86B(+12.9%) · 순이익 $231M · 희석 EPS $5.14(1년 전 $5.14) — 다음 날 주가 +12.7%', 'q3', 'Ulta Beauty 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 28, 'nt': 22, 'mean': 634.32, 'median': 635, 'low': 500, 'high': 731, 'sb': 15, 'b': 4, 'h': 8, 's': 1, 'ss': 0}
ANALYST_ASOF = '2026-11-03'


# 미완성 카드 표시(2026-11-03 사용자 결정 — C·D·E 보류 카드는 있는 자료로 만들고 판정 보류 + 이유를 잘 보이게, SPCX 방식). BUILD no_dcf가 판정을 보류로 만들고, 보험사용 문구를 미완성 사유로 바꾼다.
INCOMPLETE_SHORT = '매출 구성 장치 대기'
INCOMPLETE_WHY = '품목별 매출을 금액 없이 비중(%)으로만 공시해 자동 카드가 매출 구성을 처리하지 못한다 — 처리 장치가 생길 때까지 보류'
POST = [r"""
_w = '품목별 매출을 금액 없이 비중(%)으로만 공시해 자동 카드가 매출 구성을 처리하지 못한다 — 처리 장치가 생길 때까지 보류'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — 매출 구성 장치 대기</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — 매출 구성 장치 대기. 현금흐름 내재가치는 계산하지 않았다.')
import re as _re3
h = _re3.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re3.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")   # 툴팁이 '계산 불가 — 미완성 — …'로 겹쳤다(Codex 2026-11-03)
"""]


# ── 자동 카드 — 부문(축 하나만 붙은 값). 원문 대조: Q2 FY26 연결 매출 3,035.7 한 줄(2026-11-03) ──
AUTO = True
SEG_MAP = {
 "concepts": [],
 "axis": None,
 "extra": {},
 "members": {"us-gaap:Revenues": ["매출 전체(단일 부문)", "#f26b21"]},
 "ignore": []
}
