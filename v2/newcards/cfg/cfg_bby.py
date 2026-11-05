BUILD = {'no_dcf': '미완성 — 일회성 비용 처리 대기'}   # 2026-11-03 사용자 결정 — 미완성 카드(판정 보류)
# BBY(베스트바이) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 1월 말에 가까운 토요일(52/53주 — FY24 53주). 가전·전자제품 소매, 부문은 국내(미국)·해외(캐나다).
# 출처: SEC XBRL, Q2 FY27 10-Q(2026-09-04), 실적 보도자료(Q3 FY26~Q2 FY27, 8-K 2.02항 — 장 전 07시 동부 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/BBY.md.
# 엔진 입력(2026-11-03): 차입금 = 날짜별 DebtAndCapitalLeaseObligations 우선, 그 전 LongTermDebt($1,169M, 금융리스 포함 — DEBT_TOTAL_TAG). 낡은 단기투자(2021)·비지배지분(2016) 제외(EV_TAGS_BY_CIK). 운용리스 $2,964M.
# 미완성 사유(E54): Q3 FY26 Best Buy Health 손상(세전 $192M, 주당 $0.80, 최근 4분기 EPS 6.01의 13%)을 되돌리면 자기 이력 25.8 → 30.9로 −1표가 0이 되어 판정이 적정~고평가 → 적정으로 바뀐다(scratchpad bby_e54).
# 2026-11-03 사용자 결정에 따라 미완성 카드. 이 손상은 Q3 FY27 실적(11월 하순 예상)이 나오면 최근 4분기에서 빠진다. Q4 FY24·FY25 EPS는 보도자료 값. 관세 환급 $34M(Q2)은 회사도 조정하지 않았다.
# 민감도(Codex r1): 환급까지 빼면 자기 이력 29.5~30.1(세율·현금 처리에 따라)로 다시 −1 문턱 근처 — 일회성 범위에 따라 판정이 갈려 미완성이 맞다.
# Fable r1: 5년 창 안 Q4 FY25 손상(세전 $477M)까지 이력에서 되돌리면 자기 이력 24.1(−1 유지) — 최근 4분기만 되돌리는 시험(앞 카드들 방식)에서만 뒤집힌다. 현금흐름은 세율 맞춰도 $75.26·1.28(−1).
CIK = '0000764478'
CUR, YO, QO = '2026-08-01', '2025-08-02', '2026-05-02'
QLABEL, YL, QQL = 'Q2 FY27', 'Q2 FY26', 'Q1 FY27'
L8 = ['Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26', 'Q4 FY26', 'Q1 FY27', 'Q2 FY27']
FY_ENDS, FY_LABEL = ('2026-01-31', '2025-02-01'), 'FY2026'
VOTES, VERDICT = (-1, 1, 0), '판정 보류'
CO = 'Best Buy'
S_ = 'https://www.sec.gov/Archives/edgar/data/764478/'
SEC = S_
TENQ = S_ + '000076447826000042/bby-20260801.htm'; TENQ_NAME = 'Q2 FY27 10-Q'
PR = {'q2': S_ + '000076447826000037/bby-fy27q2xexx99.htm', 'q1': S_ + '000076447826000018/bby-fy27q1xexx991.htm', 'q4': S_ + '000076447826000005/bby-fy26q4xexx99.htm', 'q3': S_ + '000076447825000050/bby-fy26q3xexx99.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="bbyFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {pct(HIST[\'margin_now\'])})</span>'
Y2 = (0, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('미완성 카드다. 최근 4분기 이익에 2025년 3분기 Best Buy Health 손상(주당 $0.80)이 들어 있다. 최근 4분기에서만 빼면 판정이 바뀌고, 과거 손상까지 같이 빼면 그대로라 일회성 처리 규칙이 정해질 때까지 보류한다. '
              '이 손상은 다음 실적(11월 하순)에서 최근 4분기 밖으로 빠진다. 동종업 점수는 S&P500 경기소비재 기준이다.')
PH = ['HD', 'LOW', 'TJX', 'ROST', 'WSM', 'TSCO']
PEER_FILE = 'peer_universe/consumer_discretionary.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '소매 6곳 PER 비교 (점수는 S&P500 경기소비재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 경기소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 경기소비재 대비 배수 순위 (v2/peer_universe/consumer_discretionary.json)'
PEER_TIP = ('S&P500 경기소비재(BBY 제외)와 배수 순위를 매긴 값이다.',
            '자동차·주택·외식·호텔·소매가 섞여 있다. 차트에는 소매 6곳만 보인다.')
# 매출(Q2 FY27 10-Q 부문) — 국내 9,070 + 해외 709 = 9,779.
SEG = [('국내(미국)', 9070, '#0046be'), ('해외(캐나다)', 709, '#ffe000')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별(Q2 FY27)'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 전 발표(07시 동부) → 같은 날.
NEWS_RANGE = '2025.11 ~ 2026.08'
NEWS = [
    ('red', '2026년 8월 27일 장 전 — Q2 FY27 실적', '2026-08-27',
     '매출 $9.78B(+3.6%) · 순이익 $315M · 희석 EPS $1.48(1년 전 $0.87) · 조정 EPS $1.47 · 연간 전망 상향 — 당일 주가 −4.4%', 'q2', 'Best Buy 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 5월 28일 장 전 — Q1 FY27 실적', '2026-05-28',
     '매출 $8.94B(+1.9%) · 순이익 $276M · 희석 EPS $1.31(1년 전 $0.95) · 조정 EPS $1.28 — 당일 주가 +15.8%', 'q1', 'Best Buy 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 3월 3일 장 전 — Q4 FY26 실적', '2026-03-03',
     '매출 $13.81B(−1.0%) · 순이익 $541M · 희석 EPS $2.56(1년 전 $0.54, 손상) · 조정 EPS $2.61 — 당일 주가 +7.1%', 'q4', 'Best Buy 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 11월 25일 장 전 — Q3 FY26 실적', '2025-11-25',
     '매출 $9.67B(+2.4%) · 순이익 $140M · 희석 EPS $0.66(Best Buy Health 손상 포함, 1년 전 $1.26) · 조정 EPS $1.40 — 당일 주가 +5.3%', 'q3', 'Best Buy 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 25, 'nt': 16, 'mean': 87.25, 'median': 88, 'low': 71, 'high': 100, 'sb': 4, 'b': 0, 'h': 19, 's': 1, 'ss': 1}
ANALYST_ASOF = '2026-11-04'


# 미완성 카드 표시(2026-11-03 사용자 결정 — C·D·E 보류 카드는 있는 자료로 만들고 판정 보류 + 이유를 잘 보이게, SPCX 방식). BUILD no_dcf가 판정을 보류로 만들고, 보험사용 문구를 미완성 사유로 바꾼다.
INCOMPLETE_SHORT = '일회성 비용 처리 대기'
INCOMPLETE_WHY = '최근 4분기 EPS에 2025년 3분기 Best Buy Health 손상(세전 $192M)이 들어 있고, 손상을 빼는 방식에 따라 판정이 갈린다 — 일회성 처리 규칙(안건 E54)이 정해질 때까지 보류'
POST = [r"""
_w = '최근 4분기 EPS에 2025년 3분기 Best Buy Health 손상(세전 $192M)이 들어 있고, 손상을 빼는 방식에 따라 판정이 갈린다 — 일회성 처리 규칙(안건 E54)이 정해질 때까지 보류'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — 일회성 비용 처리 대기</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — 일회성 비용 처리 대기. 현금흐름 내재가치는 계산하지 않았다.')
import re as _re3
h = _re3.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re3.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")   # 툴팁이 '계산 불가 — 미완성 — …'로 겹쳤다(Codex 2026-11-03)
"""]


# ── 자동 카드 — 부문(축 하나만 붙은 값). 원문 대조: Q2 FY27 9,070/709(2026-11-03) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerIncludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"bby:DomesticSegmentMember": ["국내(미국)", "#0046be"], "bby:InternationalSegmentMember": ["해외(캐나다)", "#ffe000"]},
 "ignore": []
}
