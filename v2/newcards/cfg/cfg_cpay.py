BUILD = {'no_dcf': '미완성 — 일회성 비용 처리 대기'}   # 2026-11-03 사용자 결정 — 미완성 카드(판정 보류)
# CPAY(코페이) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 12월 31일. 기업 결제 — Corporate·Vehicle·Lodging Payments + 기타.
# 출처: SEC XBRL, Q2 2026 10-Q(2026-08-07 17:39 동부 장 마감 뒤). Q3 2026 10-Q는 아직 없다(실적은 11-04 장 마감 뒤 발표) — 새 10-Q는 매일 실행 auto_approve가 반영한다(2026-11-05 사용자 결정). 사전 조사 scratchpad pre/CPAY.md.
# 엔진 입력: 현금 $3,163.5M(제한 현금 $7,004.8M은 고객 예치금과 짝이라 제외), 차입 $10,623.5M(매출채권 유동화 $2,300M 포함), 상환가능 비지배지분 $314M(Mastercard).
# 인수 대금 TTM −$2,088M은 실제 순유입(2025-11 Alpha 인수 때 고객 자금 현금 약 $4B가 함께 들어옴) — 현금흐름 모델은 neg_acquisitions 규칙으로 평균 자본효율을 쓴다.
# 미완성 사유(E54, 2026-11-05 시험 scratchpad cpay_e54/, 차입금 수정 뒤): 판정 전 (−1, 0, −2) 적정~고평가 — 자기 26.9·동종업 54.5·현금흐름 기본 $237.55(1.76배).
# 좁은 일회성(매각 손익, FTC 합의 $100.9M, 조기상환, 이산 세금)만 빼면 자기 26.2(−1 그대로). 인수·통합 비용(FY2024 $33.7M·2025 상반기 $25.8M·Q3 2025 15.7·Q4 66.5·Q1 2026 16.9·Q2 38.1, 세후 0.75 가정)까지
# 과거 이력과 함께 빼면 자기 32.5(FY2024부터), 2021~2023 통합 비용까지 같은 규칙으로 빼면 30.5, Q4 2024 영업권 손상 $90M도 빼면 29.2, 같은 분기 매각 이익까지 빼면 31.2 —
# 30(표 경계) ±1에 걸려 −1/0이 방식에 따라 갈린다(Fable r1). 인수·통합 비용은 일회성 시험에 넣는다(2026-11-05 사용자 결정) — 다만 엔진 E54 장치(eps_oneoff.py)는 8분기 중 6개 이상 나온 항목을 만성으로 보고 빼지 않아, 장치가 생겨도 이 결정과 맞추는 손질이 필요하다. 현금흐름은 1.68배로 −2 그대로.
# 엔진 입력 수정(Codex r1): 차입 LongTermDebt $10,623.5M(DEBT_TOTAL_TAG — 기본은 유동분 $4,525M만), 비지배 $46M + 상환가능 $314M(EV_TAGS nci).
CIK = '0001175454'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, 0, 0), '판정 보류'
CO = 'Corpay'
S_ = 'https://www.sec.gov/Archives/edgar/data/1175454/'
SEC = S_
TENQ = S_ + '000117545426000050/cpay-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000117545426000045/ex991q2_2026.htm', 'q1': S_ + '000117545426000029/ex991q1_2026.htm',
      'q4': S_ + '000117545426000008/ex991q4_2025.htm', 'q3': S_ + '000117545425000025/ex991q3_2025.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="cpayFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (20, 55)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('미완성 카드다. 최근 4분기 이익에 사업 매각 이익(PayByPhone·BP 포트폴리오), FTC 합의 비용($100M), Alpha·AvidXchange 인수·통합 비용이 섞여 있는데, 이것들을 어떻게 빼느냐에 따라 자기 이력 칸이 ‘비싸다’ 경계(30점) 위아래를 오간다. '
              '카드 재무는 2분기 10-Q 기준이고 11월 4일 발표한 3분기 실적(희석 EPS $5.66, 연간 전망 상향)은 10-Q가 접수되면 자동으로 반영된다. '
              '현금에는 고객 예치금과 짝인 제한 현금($7.0B)을 넣지 않았고, 차입금 $10.6B에는 매출채권 유동화 $2.3B가 들어 있다. 정비 사업 매각이 승인·완료되면 매각 이익(회사 예상 세전 $460~515M)이 들어온다.')
PH = ['FISV', 'FIS', 'GPN', 'PYPL', 'V', 'MA']
PEER_FILE = 'peer_universe/payments_exchanges.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '결제 처리 6곳 PER 비교 (점수는 S&P500 결제·거래소·금융 데이터 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 결제·거래소·금융 데이터 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 결제·거래소·금융 데이터 대비 배수 순위 (v2/peer_universe/payments_exchanges.json)'
PEER_TIP = ('S&P500 결제 처리·거래소·금융 데이터 18곳 중 CPAY를 뺀 17곳과 배수 순위를 매긴 값이다.',
            '카드 네트워크·결제 처리·거래소·신용평가가 섞여 있어 성장·마진 구조가 다르다. 차트에는 결제 처리 6곳만 보인다.')
# 매출(Q2 2026 10-Q 부문 표) — Corporate 548.7 + Vehicle 580.2 + Lodging 123.2 + 기타 86.7 = 1,338.8.
SEG = [('법인 결제', 548.7, '#e3004f'), ('차량 결제', 580.2, '#2b2d42'), ('숙박 결제', 123.2, '#f39ab6'), ('기타', 86.7, '#8a96a3')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별(Q2 2026)'
# 손 뉴스: 실적 4건(희석 EPS GAAP). 반응일: 모두 장 마감 뒤 → 다음 거래일. Q3 2026(11-04 장 마감 뒤)은 반응일이 카드 날짜 뒤라 넣지 않는다.
NEWS_RANGE = '2025.11 ~ 2026.08'
NEWS = [
    ('green', '2026년 8월 5일 장 마감 뒤 — Q2 2026 실적', '2026-08-06',
     '매출 $1.34B(+21.5%) · 희석 EPS $3.70(1년 전 $3.98, FTC 합의 $100M 포함) · 조정 EPS $7.00 — 다음 날 주가 +1.0%', 'q2', 'Corpay 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 5월 7일 장 마감 뒤 — Q1 2026 실적', '2026-05-08',
     '매출 $1.26B(+25.4%) · 희석 EPS $5.07(1년 전 $3.40) — 이 가운데 PayByPhone 매각 이익이 주당 $1.19 · 조정 EPS $5.80 — 다음 날 주가 +12.5%', 'q1', 'Corpay 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 4일 장 마감 뒤 — Q4 2025 실적', '2026-02-05',
     '매출 $1.25B(+20.7%) · 희석 EPS $3.75(1년 전 $3.44) · 조정 EPS $6.04 · PayByPhone 매각 발표 — 다음 날 주가 +11.6%', 'q4', 'Corpay 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 11월 5일 장 마감 뒤 — Q3 2025 실적·Alpha 인수 완료', '2025-11-06',
     '매출 $1.17B(+13.9%) · 희석 EPS $3.91(1년 전 $3.90) · 조정 EPS $5.70 — 다음 날 주가 +6.2%', 'q3', 'Corpay 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 16, 'nt': 12, 'mean': 480.58, 'median': 481, 'low': 390, 'high': 539, 'sb': 8, 'b': 5, 'h': 3, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-05'


# 미완성 카드 표시(2026-11-03 사용자 결정 — C·D·E 보류 카드는 있는 자료로 만들고 판정 보류 + 이유를 잘 보이게, SPCX 방식). BUILD no_dcf가 판정을 보류로 만들고, 보험사용 문구를 미완성 사유로 바꾼다.
INCOMPLETE_SHORT = '일회성 비용 처리 대기'
INCOMPLETE_WHY = '일회성(매각 손익·FTC 합의·인수·통합 비용)을 빼는 방식에 따라 자기 이력 칸이 ‘비싸다’ 경계(30점) 위아래를 오간다 — 일회성 처리 규칙(안건 E54)이 정해질 때까지 보류'
POST = [r"""
_w = '일회성(매각 손익·FTC 합의·인수·통합 비용)을 빼는 방식에 따라 자기 이력 칸이 ‘비싸다’ 경계(30점) 위아래를 오간다 — 일회성 처리 규칙(안건 E54)이 정해질 때까지 보류'
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


# ── 자동 카드 — 부문 지도(부문 축 손 작성 — 제안기는 집중도 축과 겹친 제품 축을 골랐다. 원문 Q2 2026 548.7/580.2/123.2/86.7, 2026-11-05) ──
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
  "cpay:CorporatePaymentsMember": [
   "법인 결제",
   "#e3004f"
  ],
  "cpay:VehiclePaymentsMember": [
   "차량 결제",
   "#2b2d42"
  ],
  "cpay:LodgingPaymentsMember": [
   "숙박 결제",
   "#f39ab6"
  ],
  "cpay:OtherOperatingSegmentsMember": [
   "기타",
   "#8a96a3"
  ]
 },
 "ignore": []
}
