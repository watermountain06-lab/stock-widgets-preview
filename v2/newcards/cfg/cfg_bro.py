BUILD = {'no_dcf': '미완성 — 에스크로 평가손익 장치 대기'}   # 2026-11-03 사용자 결정 — 미완성 카드(판정 보류)
# BRO(브라운 앤 브라운) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일(submissions fiscalYearEnd "0119"는 오기). 보험 중개 — 리테일·전문 유통(Programs + Wholesale, 2025 Q3 재편) 2개 부문.
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-26 17:05 동부 장 마감 뒤 → 첫 세션 10-27), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 모두 월요일 17시 무렵 장 마감 뒤 → 다음 거래일 반응). 사전 조사 scratchpad pre/BRO.md.
# 엔진 입력(2026-11-05): 손익계산서에 영업이익 줄이 없어 합성 — 세전이익 + 이자비용(DERIVED_OPINC, HCA 규칙, 이자 태그 2024-06에 InterestExpense → InterestExpenseNonoperating).
# 감가상각 = Depreciation + AdjustmentForAmortization(DDA_PARTS_BY_CIK). 단기투자 태그는 2024-12 뒤 없음(EV_TAGS sti []). 수탁 현금 $2,442M·수탁 채권 $1,234M = 수탁 부채 $3,676M(회사 고유 태그)은 엔진 현금 밖.
# Accession Risk Management 인수(2025-08-01 종결, 대가 $9,608M — 2025-06 주식 공모 43.1백만 주·채권 $4.2B): 1년 전 대비 매출·이익 증가 대부분이 인수 몫(Q3 2026 유기 성장 1.2%).
# 희석 EPS는 에스크로 주식 평가이익(비과세·비현금, 최근 4분기 +$145M)을 빼고 에스크로 주식을 더한 값이라 순이익 ÷ 주식 수보다 낮다(Q3 0.67 대 0.73).
# 미완성 사유(E54, 2026-11-05 시험 scratchpad bro_e54/): 판정 전 (+1, +1, −1) 적정~저평가 — 자기 88.2·동종업 74.0·현금흐름 기본 $50.55(1.46배).
# 에스크로 평가이익(Q4 2025 62·Q1 64·Q2 5·Q3 14, 합 $145M)만 빼면 기본 $47.22(1.565배)로 현금흐름 −1 → −2(종합 적정).
# 에스크로 평가손익은 일회성이 아니라 자기 주가 연동 부채 재측정(Q4 2026은 주가 상승으로 약 $57M 비용 예상) — 영업외로 영구 제외하는 overlay 장치가 있으면 (+1, +1, −2) 적정으로 완성(Fable r1).
# 인수·통합 비용(120)·earn-out(−1)·처분(1)까지 함께 정리하면(영업이익 −$25M, EPS 3.16 → 3.43) 기본 $49.29(1.499배)로 −1 그대로, 자기 90.1·동종업 76.1 — 방식에 따라 갈려 보류(BBY와 같은 처리).
# 주식 수: 엔진은 표지 331,691,829주(10-23)를 쓴다. 재무상태표 327M주는 에스크로 주식(약 4.43M주)을 뺀 수 — 시총 1.4% 차이, 표 영향 없음(Fable r1).
CIK = '0000079282'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, 1, 0), '판정 보류'
CO = 'Brown & Brown'
S_ = 'https://www.sec.gov/Archives/edgar/data/79282/'
SEC = S_
TENQ = S_ + '000119312526432146/bro-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000119312526432142/bro-ex99_1.htm', 'q2': S_ + '000119312526318245/bro-ex99_1.htm',
      'q1': S_ + '000119312526182375/bro-ex99_1.htm', 'q4': S_ + '000119312526022760/bro-ex99_1.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="broFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (15, 40)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('미완성 카드다. 손익계산서에 영업이익 줄이 없어 세전이익 + 이자비용으로 영업이익을 만드는데, 여기에 Accession 인수 에스크로 주식 평가손익(비현금·비과세, 최근 4분기 이익 $145M)이 들어 있다. '
              '이 줄은 회사 고유 태그라 지금은 빼는 장치가 없고, 빼면 현금흐름 칸이 한 단계 더 비싼 쪽으로 바뀐다. 자기 이력·동종업 점수는 참고로 둔다. '
              '2025년 8월 Accession 인수로 1년 전 대비 매출·이익 증가의 대부분은 인수 몫이다(2026년 3분기 유기 성장 1.2%). '
              '희석 EPS는 에스크로 평가이익을 빼고 에스크로 주식을 더한 값이라 순이익 ÷ 주식 수보다 낮다. 비교 종목은 S&P500 보험 중개사 4곳과 결제·거래소·금융 데이터 회사다.')
HEALTH_EXTRA = '유동비율·부채비율에는 고객 수탁 자산과 수탁 부채(같은 금액)가 들어 있어 실제 지급능력보다 나쁘게 나온다.'
PH = ['AJG', 'AON', 'MRSH', 'WTW', 'SPGI', 'MCO']
PEER_FILE = 'peer_universe/brokers_fees.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '보험 중개·금융 데이터 6곳 PER 비교 (점수는 중개사 + 결제·거래소·데이터 기준)', 'pbr': '보험 중개·금융 데이터 PBR 비교', 'psr': '보험 중개·금융 데이터 PSR 비교',
                'pcr': '보험 중개·금융 데이터 PCR(FCF) 비교', 'evebitda': '보험 중개·금융 데이터 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 보험 중개사와 결제·거래소·금융 데이터 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 보험 중개 + 결제·거래소·금융 데이터 대비 배수 순위 (v2/peer_universe/brokers_fees.json)'
PEER_TIP = ('S&P500 보험 중개사(BRO 제외 4곳)와 결제·거래소·금융 데이터 회사(수수료로 버는 자산 경량 서비스)와 배수 순위를 매긴 값이다 — 중개사만으로는 비교 표본(8곳)이 모자란다.',
            '결제 처리·카드 네트워크·거래소가 섞여 있어 성장·마진 구조가 다르다. 차트에는 보험 중개·금융 데이터 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문 표, Revenues) — 리테일 978 + 전문 유통 739 = 1,717, 본사 기타 8은 SEG_ADJ — 합 1,725.
SEG = [('리테일', 978, '#003a70'), ('전문 유통(프로그램·도매)', 739, '#5b8db8')]
SEG_ADJ = 8
SEG_TITLE = '매출 구성 — 부문별(Q3 2026)'
# 손 뉴스: Q3 2026 실적(10/26)은 news_auto가 SEC 숫자로 붙인다. 반응일: 장 마감 뒤 발표 → 다음 거래일.
NEWS_RANGE = '2026.01 ~ 2026.10'
NEWS = [
    ('green', '2026년 7월 27일 장 마감 뒤 — Q2 2026 실적', '2026-07-28',
     '매출 $1.68B(+30.4%, 인수 포함) · 희석 EPS $0.84(1년 전 $0.78) · 조정 EPS $1.07 — 다음 날 주가 +5.7%', 'q2', 'Brown & Brown 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 4월 27일 장 마감 뒤 — Q1 2026 실적', '2026-04-28',
     '매출 $1.90B(+35.4%, 인수 포함) · 희석 EPS $1.06(1년 전 $1.15) · 조정 EPS $1.39 — 다음 날 주가 −4.5%', 'q1', 'Brown & Brown 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 1월 26일 장 마감 뒤 — Q4 2025 실적', '2026-01-27',
     '매출 $1.61B(+35.7%, 인수 포함) · 희석 EPS $0.59(1년 전 $0.73) · 조정 EPS $0.93 — 다음 날 주가 −6.9%', 'q4', 'Brown & Brown 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 21, 'nt': 16, 'mean': 74.06, 'median': 75, 'low': 55, 'high': 85, 'sb': 4, 'b': 3, 'h': 13, 's': 0, 'ss': 1}
ANALYST_ASOF = '2026-11-05'


# 미완성 카드 표시(2026-11-03 사용자 결정 — C·D·E 보류 카드는 있는 자료로 만들고 판정 보류 + 이유를 잘 보이게, SPCX 방식). BUILD no_dcf가 판정을 보류로 만들고, 보험사용 문구를 미완성 사유로 바꾼다.
INCOMPLETE_SHORT = '에스크로 평가손익 장치 대기'
INCOMPLETE_WHY = '합성 영업이익(세전이익 + 이자)에 Accession 인수 에스크로 주식 평가손익(비현금·비과세, 최근 4분기 이익 $145M)이 들어 있는데, 이 줄은 회사 고유 태그라 영업이익에서 빼는 장치가 없다. 빼면 현금흐름 표가 −1에서 −2로 바뀐다 — 장치를 만들 때까지 보류'
POST = [r"""
_w = '합성 영업이익(세전이익 + 이자)에 Accession 인수 에스크로 주식 평가손익(비현금·비과세, 최근 4분기 이익 $145M)이 들어 있는데, 이 줄은 회사 고유 태그라 영업이익에서 빼는 장치가 없다. 빼면 현금흐름 표가 −1에서 −2로 바뀐다 — 장치를 만들 때까지 보류'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — 에스크로 평가손익 장치 대기</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — 에스크로 평가손익 장치 대기. 현금흐름 내재가치는 계산하지 않았다.')
import re as _re3
h = _re3.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re3.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")   # 툴팁이 '계산 불가 — 미완성 — …'로 겹쳤다(Codex 2026-11-03)
"""]


# ── 자동 카드 — 부문 지도는 seg_map_propose.py 1판(영업 부문 Revenues, 손 표와 일치, 2026-11-05) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:Revenues"
 ],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {
  "srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"
 },
 "members": {
  "bro:RetailSegmentMember": [
   "리테일",
   "#003a70"
  ],
  "bro:SpecialtyDistributionMember": [
   "전문 유통(프로그램·도매)",
   "#5b8db8"
  ]
 },
 "ignore": []
}
