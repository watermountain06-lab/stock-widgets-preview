BUILD = {'no_dcf': '미완성 — 이익률 조정 대기'}   # 2026-11-03 사용자 결정 — 미완성 카드(판정 보류). 11-05 사유 변경: PER은 E54 장치로 돌아옴, 현금흐름 이익률이 12-01 A-2 대기(사용자 결정)
# FISV(파이서브) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 12월 31일. 가맹점 결제(Clover)·은행 코어 처리 — 보고부문 2개 + Corporate and Other(우편료 대납).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-11-04 07:12 동부 장 전 → 같은 날), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 모두 장 전), 8-K(CEO 교체 06-15, 유로채 06-23, President 사임 07-07). 사전 조사 scratchpad pre/FISV.md.
# 티커: 2025-11-11 NYSE "FI" → Nasdaq "FISV"(같은 CIK, Yahoo 일봉은 이어진 시계열).
# 미완성 사유(2026-11-05 사용자 결정 — 이익률 조정 대기): FISV 일회성 입력(v2/eps_oneoff.json 71항목, f7bf4eb9)으로 최근 4분기 EPS −7.42 → 4.70, PER 13.35배(자기 PER 점수 79.6)가 돌아왔다.
# 정식으로 빌드하면 자기 64.6(+1)·동종 70.6(+1)이지만, Q3 2026 영업권 손상 세전 $6,452M이 영업이익 안에 있어 현금흐름 margin_now −10.9%(2년 28.1%, 5년 25.2%) → 기본 $17.18, 낙관 −$78.69, 비율 3.65(−2)로 일그러진다.
# 장치는 이익률을 12-01 A-2 검정 뒤에 조정하므로(10-25 결정 ⑥) 그때까지 미완성. 같은 문제: 영업이익 안 손상이 큰 카드(KHC·GIS·SJM·IP 등).
CIK = '0000798354'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 1, 0), '판정 보류'
CO = 'Fiserv'
S_ = 'https://www.sec.gov/Archives/edgar/data/798354/'
SEC = S_
TENQ = S_ + '000079835426000042/fisv-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000079835426000039/fisvq326earningsrelease.htm', 'q2': S_ + '000079835426000028/fisvq226earningsrelease.htm',
      'q1': S_ + '000079835426000014/fisvq126earningsrelease.htm', 'q4': S_ + '000079835426000006/fisv4q25earningsrelease.htm'}
LINKS = {'ceo': S_ + '000119312526270336/d153349d8k.htm', 'euro': S_ + '000119312526279413/d38671d8k.htm', 'pres': S_ + '000119312526297448/d110419d8k.htm'}
FAIRBAND_TITLE = 'id="fisvFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {pct(HIST[\'margin_now\'])})</span>'
Y2 = (-120, 40)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('미완성 카드다. 2026년 3분기 영업권 손상($6.5B)이 영업이익 안에 있어 현금흐름 모형이 최근 4분기 영업이익률을 −10.9%로 읽고, 그래서 현금흐름 가치가 크게 낮게 나온다. PER은 손상과 그 밖의 일회성 손익을 뺀 EPS로 계산했지만, 영업이익률과 EV/EBITDA는 아직 손상을 그대로 담고 있다. 이익률에서 일회성을 빼는 규칙은 12월 1일 검정 뒤에 정해지므로 그때까지 판정을 보류한다. '
              '손상은 보고상 Corporate and Other 영업손실에 들어가 부문 영업이익에는 없다(귀속은 가맹점 $3.7B, 금융기관 $2.8B). 매출의 Corporate and Other는 우편료 대납이다. '
              'EV/EBITDA의 감가상각은 SEC 요약 자료에 있는 값만 읽어 최근 4분기 약 $2.3B로, 현금흐름표 합계(약 $3.4B)보다 작다 — 인수 무형자산 상각이 회사 고유 태그로만 공시돼서다. 그래서 EV/EBITDA는 실제보다 높게 나온다. '
              '2025년 11월 11일 티커가 FI(뉴욕증권거래소)에서 FISV(나스닥)로 바뀌었다. 비교 종목은 S&P500 결제·거래소·금융 데이터 18곳 중 FISV를 뺀 17곳이다.')
PRE = ['FB = None']
BB_TAGS = ['TreasuryStockValueAcquiredCostMethod']   # 자사주 매입: PaymentsForRepurchaseOfCommonStock는 2018에 멈추고 현금흐름표 줄은 회사 고유 태그(원천징수 포함 9M $395M) — 자본변동표 매입액(9M $301M, Q3 0)
PH = ['FIS', 'GPN', 'JKHY', 'PYPL', 'V', 'MA']
PEER_FILE = 'peer_universe/payments_exchanges.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '결제 처리 6곳 PER 비교 (점수는 S&P500 결제·거래소·금융 데이터 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 결제·거래소·금융 데이터 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 결제·거래소·금융 데이터 대비 배수 순위 (v2/peer_universe/payments_exchanges.json)'
PEER_TIP = ('S&P500 결제 처리·거래소·금융 데이터 18곳 중 FISV를 뺀 17곳과 배수 순위를 매긴 값이다.',
            '카드 네트워크·결제 처리·거래소·신용평가가 섞여 있어 성장·마진 구조가 다르다. 차트에는 결제 처리 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문 표) — 가맹점 2,521 + 금융기관 2,331 = 4,852, Corporate and Other(우편료 대납) 344는 다른 축(CorporateNonSegmentMember)이라 SEG_ADJ로 대조만 — 합 5,196.
SEG = [('가맹점 솔루션', 2521, '#ff6600'), ('금융기관 솔루션', 2331, '#1f2a44')]
SEG_ADJ = 344
SEG_TITLE = '매출 구성 — 보고부문별(Q3 2026, 우편료 대납 $344M 제외)'
# 손 뉴스: Q3 2026 실적은 영업권 손상과 함께 발표돼 손 항목으로 쓴다(자동 항목은 빠진다, README 6). 반응일: 실적은 모두 장 전 → 같은 날, 16시 뒤 8-K는 다음 거래일.
NEWS_RANGE = '2026.02 ~ 2026.11'
NEWS = [
    ('green', '2026년 11월 3일 장 전 — Q3 2026 실적·영업권 손상', '2026-11-03',
     '매출 $5.20B(−1.3%) · 순손실 $5,941M · 희석 EPS −$11.17(1년 전 $1.46, 영업권 손상 $6,452M 포함) · 조정 EPS $1.75 — 당일 주가 +12.5%', 'q3', 'Fiserv 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 8월 6일 장 전 — Q2 2026 실적', '2026-08-06',
     '매출 $5.29B(−4.1%) · 희석 EPS $1.17(1년 전 $1.86) · 조정 EPS 연간 전망을 $8.00~8.30에서 $7.20~7.40으로 낮춤 — 당일 주가 0.0%', 'q2', 'Fiserv 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 7월 7일 장 마감 뒤 — President 사임', '2026-07-08',
     'Dhivya Suryadevara President가 7월 7일 사임(7월 31일까지 비임원 직원으로 인수인계) — 다음 날 주가 −4.0%', 'pres', 'Fiserv 공시 (SEC 8-K)'),
    ('neutral', '2026년 6월 23일 장 마감 뒤 — 유로채 €1.0B 발행', '2026-06-24',
     '3.750% 2030년·4.250% 2034년 만기 각 €500M, 공개매수로 기존 채권 장부가 $1.3B를 $1.2B에 사들임', 'euro', 'Fiserv 공시 (SEC 8-K)'),
    ('red', '2026년 6월 15일 장 전 — CEO 교체', '2026-06-15',
     'Mike Lyons CEO가 6월 12일 사임, Takis Georgakopoulos가 6월 14일 CEO로 — 당일 주가 −10.9%', 'ceo', 'Fiserv 공시 (SEC 8-K)'),
    ('red', '2026년 5월 5일 장 전 — Q1 2026 실적', '2026-05-05',
     '매출 $5.03B(−2.0%) · 희석 EPS $1.07(1년 전 $1.51) · 조정 EPS $1.79 — 당일 주가 −8.8%', 'q1', 'Fiserv 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 10일 장 전 — Q4 2025 실적', '2026-02-10',
     '매출 $5.28B(+0.6%) · 희석 EPS $1.51(1년 전 $1.64) · 조정 EPS $1.99 — 당일 주가 +4.1%', 'q4', 'Fiserv 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 37, 'nt': 21, 'mean': 61.33, 'median': 60, 'low': 46, 'high': 85, 'sb': 4, 'b': 2, 'h': 27, 's': 2, 'ss': 2}
ANALYST_ASOF = '2026-11-05'


# 미완성 카드 표시(2026-11-03 사용자 결정 — C·D·E 보류 카드는 있는 자료로 만들고 판정 보류 + 이유를 잘 보이게, SPCX 방식). BUILD no_dcf가 판정을 보류로 만들고, 보험사용 문구를 미완성 사유로 바꾼다.
INCOMPLETE_SHORT = '이익률 조정 대기'
INCOMPLETE_WHY = '2026년 3분기 영업권 손상($6.5B)이 영업이익 안에 있어 현금흐름 모형이 최근 4분기 영업이익률을 −10.9%로 읽는다(2년 28.1%). PER은 일회성 장치(안건 E54)가 손상을 빼고 계산했지만, 영업이익률에서 일회성을 빼는 규칙은 12월 1일 검정 뒤에 정해진다 — 그때까지 보류'
POST = [r"""
_w = '2026년 3분기 영업권 손상($6.5B)이 영업이익 안에 있어 현금흐름 모형이 최근 4분기 영업이익률을 −10.9%로 읽는다(2년 28.1%). PER은 일회성 장치(안건 E54)가 손상을 빼고 계산했지만, 영업이익률에서 일회성을 빼는 규칙은 12월 1일 검정 뒤에 정해진다 — 그때까지 보류'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — 이익률 조정 대기</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — 이익률 조정 대기. 현금흐름 내재가치는 계산하지 않았다.')
import re as _re3
h = _re3.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re3.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")   # 툴팁이 '계산 불가 — 미완성 — …'로 겹쳤다(Codex 2026-11-03)
import re as _re4
h = _re4.sub(r'부문 간 거래·조정 ([+−-]\$[\d.]+B)를 더한 것이 매출이다', r'우편료 대납(Corporate and Other) \1를 더한 것이 매출이다', h)   # 매출 각주 — 차이는 부문 간 거래가 아니라 우편료 대납(2026-11-05)
"""]


# ── 자동 카드 — 부문 지도는 seg_map_propose.py 1판(보고부문 2개, 원문 대조 Q3 2026 2,521/2,331, 1년 전 2,586/2,333). 우편료 대납 344는 SEG_ADJ(2026-11-05) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
 ],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {
  "srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"
 },
 "members": {
  "fisv:MerchantSegmentMember": [
   "가맹점 솔루션",
   "#ff6600"
  ],
  "fisv:FinancialSegmentMember": [
   "금융기관 솔루션",
   "#1f2a44"
  ]
 },
 "ignore": []
}
