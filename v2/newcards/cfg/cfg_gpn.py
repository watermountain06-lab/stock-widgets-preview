BUILD = {'eps_tag': 'IncomeLossFromContinuingOperationsPerDilutedShare,EarningsPerShareDiluted', 'no_dcf': '미완성 — 매각·인수 재작성 대기'}   # 2026-11-05 — 미완성 카드(판정 보류), EPS는 계속사업 희석 EPS 우선(APTV 방식)
# GPN(글로벌 페이먼츠) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 12월 31일. 가맹점 결제 — Enterprise·Platforms·SMB 3부문(2026 재편).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-11-05 17:19 동부 장 마감 뒤 → 첫 세션 11-06, 장중 가격), 실적 보도자료(Q4 2025~Q3 2026, 모두 장 전 → 같은 날).
# 미완성 사유(2026-11-06 갱신): 2026-01-09 Worldpay 인수와 Issuer Solutions 매각(중단사업)을 함께 마감 — 과거 이력은 인수·매각 전 회사(재작성 이력 부족, APTV 방식으로 쌓일 때까지 보류).
# PER: EPS는 계속사업 희석 EPS(BUILD eps_tag) — 최근 4분기 0.73(Q4'25 0.78 · Q1 −0.78 · Q2 0.43 · Q3 0.30 — Q4'25 0.78은 EPS 파일의 역산값(연간 계속사업 EPS − 앞 세 분기)이라 보도자료 Q4 계속사업 EPS 0.63과 다르다: 연간 값은 Issuer 매각 뒤 재작성 기준이고 앞 세 분기는 공시 시점이 섞인 값 — Q1'25 0.93은 2026-05 재작성 비교값, Q2·Q3'25는 처음 공시값(Fable 2026-11-06). 재작성값만 쓰면 순이익률 1.17%로 역시 2% 아래), A3 순이익률은 계속영업 기준(844ee580)으로 1.37% < 2%라 PER 해당 없음. Q2 기준(11-05)에는 Q3 2025 Payroll 매각 이익 $344M이 TTM에 있어 5.16%였다.
# 일회성 시험(E54 통일 규칙, Fable 2026-11-06): 구조조정(시설 철수·퇴직급여)이 2025~26 매 분기라 반복 → 빼지 않음, Q4'25 매각 손실 $32.2M은 순이익률 < 2%라 매출 1% 바닥(약 $115M)에 미달 → PER 제외는 그대로.
#  주의: GPN을 eps_oneoff.json에 넣을 때 퇴직급여를 구조조정 반복 셈에서 빼면 $138.7M이 바닥을 넘어 2.3%로 뒤집힌다.
# 빌드(11-06 장중 $97.12): 참고 점수 자기 49.0·동종 62.0. 현금흐름은 세 시나리오 모두 음수(Worldpay 무형자산 상각 분기 약 $750M, 영업권·무형자산이 투하자본; Q3 인수 무형자산 상각 전체 $754.5M) — 보류라 쓰지 않는다.
NI_TAGS = ['IncomeLossFromContinuingOperations', 'NetIncomeLoss']
CIK = '0001123360'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, 0), '판정 보류'
CO = 'Global Payments'
S_ = 'https://www.sec.gov/Archives/edgar/data/1123360/'
SEC = S_
TENQ = S_ + '000112336026000093/gpn-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000112336026000091/exhibit99120260930.htm', 'q2': S_ + '000112336026000082/exhibit99120260630.htm',
      'q1': S_ + '000112336026000070/exhibit99120260331.htm', 'q4': S_ + '000112336026000004/exhibit99120251231.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="gpnFairBand" title="미완성 카드이고 최근 4분기 계속사업 순이익률이 2% 아래라 PER 구간으로 낸 적정주가를 표시하지 않는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {pct(HIST[\'margin_now\'])})</span>'
Y2 = (-10, 40)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('미완성 카드다. 2026년 1월 Worldpay를 인수하고 카드 발급 처리 사업(Issuer Solutions)을 팔았다. 과거 이력은 인수·매각 전 회사라 PER과 성장률 비교가 섞이고, 최근 4분기 계속사업 이익은 Worldpay 무형자산 상각과 통합 비용 때문에 매출의 1.4%뿐이라 순이익률 2% 기준으로 PER을 점수에서 뺀다(1년 전 Payroll 매각 이익 $344M이 4분기 합에서 빠졌다). 매출은 Worldpay 편입으로 1년 전보다 크게 늘었다. '
              '비교 종목은 S&P500 결제·거래소·금융 데이터 18곳 중 GPN을 뺀 17곳이다.')
PRE = ['FB = None']
PH = ['FISV', 'FIS', 'JKHY', 'PYPL', 'V', 'MA']
PEER_FILE = 'peer_universe/payments_exchanges.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '결제 처리 6곳 PER 비교 (점수는 S&P500 결제·거래소·금융 데이터 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 결제·거래소·금융 데이터 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 결제·거래소·금융 데이터 대비 배수 순위 (v2/peer_universe/payments_exchanges.json)'
PEER_TIP = ('S&P500 결제 처리·거래소·금융 데이터 18곳 중 GPN을 뺀 17곳과 배수 순위를 매긴 값이다.',
            '카드 네트워크·결제 처리·거래소·신용평가가 섞여 있어 성장·마진 구조가 다르다. 차트에는 결제 처리 6곳만 보인다.')
# 매출(Q3 2026 실적 보도자료 부문 표, GAAP) — Enterprise 836.3 + Platforms 633.6 + SMB 1,663.9 = 3,133.8, 기타 매출 172.5는 SEG_ADJ — 합 3,306.3.
SEG = [('중소 가맹점(SMB)', 1663.9, '#1b1f63'), ('대형 가맹점(Enterprise)', 836.3, '#5c6bc0'), ('플랫폼', 633.6, '#b3b9e6')]
SEG_ADJ = 172.5
SEG_TITLE = '매출 구성 — 부문별(Q3 2026)'
# 손 뉴스: 실적 4건(희석 EPS는 GAAP 전체, 괄호 안 계속사업). 반응일: 모두 장 전 → 같은 날.
NEWS_RANGE = '2026.02 ~ 2026.11'
NEWS = [
    ('red', '2026년 11월 5일 장 전 — Q3 2026 실적', '2026-11-05',
     '매출 $3.31B(+63.7%, Worldpay 편입) · 희석 EPS $1.06(계속사업 $0.30, 중단사업 $0.76) · 조정 EPS $3.58 · 연간 전망 유지 — 당일 주가 −1.2%', 'q3', 'Global Payments 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 8월 5일 장 전 — Q2 2026 실적·전망 하향', '2026-08-05',
     '매출 $3.32B · 희석 EPS $0.05(계속사업 $0.43) · 조정 EPS $3.46 · 조정 EPS 연간 전망 $13.60~13.80으로 낮춤 — 당일 주가 −0.9%', 'q2', 'Global Payments 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 5월 6일 장 전 — Q1 2026 실적', '2026-05-06',
     '매출 $2.97B · 희석 EPS −$6.59(계속사업 −$0.78, 중단사업 −$5.81 — Issuer Solutions 매각 세금) · 조정 EPS $2.96 — 당일 주가 +0.2%', 'q1', 'Global Payments 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 18일 장 전 — Q4 2025 실적', '2026-02-18',
     '매출 $1.90B · 희석 EPS $0.92(계속사업 $0.63) · 조정 EPS $3.18 · 자사주 매입 승인 $2.5B — 당일 주가 +16.5%', 'q4', 'Global Payments 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 36, 'nt': 26, 'mean': 109.92, 'median': 110, 'low': 64, 'high': 194, 'sb': 15, 'b': 2, 'h': 17, 's': 1, 'ss': 1}
ANALYST_ASOF = '2026-11-08'


# 미완성 카드 표시(2026-11-03 사용자 결정 — C·D·E 보류 카드는 있는 자료로 만들고 판정 보류 + 이유를 잘 보이게, SPCX 방식). BUILD no_dcf가 판정을 보류로 만들고, 보험사용 문구를 미완성 사유로 바꾼다.
INCOMPLETE_SHORT = '매각·인수 재작성 대기'
INCOMPLETE_WHY = '2026년 1월 Worldpay 인수와 Issuer Solutions 매각(중단사업)이 함께 끝나, 과거 이력은 인수·매각 전 회사라 PER·성장 비교가 섞인다. 최근 4분기 계속사업 순이익률도 1.4%라 PER을 점수에서 뺀다(순이익률 2% 기준) — 합친 회사의 이력이 쌓일 때까지 보류'
POST = [r"""
_w = '2026년 1월 Worldpay 인수와 Issuer Solutions 매각(중단사업)이 함께 끝나, 과거 이력은 인수·매각 전 회사라 PER·성장 비교가 섞인다. 최근 4분기 계속사업 순이익률도 1.4%라 PER을 점수에서 뺀다(순이익률 2% 기준) — 합친 회사의 이력이 쌓일 때까지 보류'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — 매각·인수 재작성 대기</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — 매각·인수 재작성 대기. 현금흐름 내재가치는 계산하지 않았다.')
import re as _re3
h = _re3.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re3.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")   # 툴팁이 '계산 불가 — 미완성 — …'로 겹쳤다(Codex 2026-11-03)
import re as _re4
h = _re4.sub(r'부문 간 거래·조정 ([+−-]\$[\d.,]+[BM])를 더한 것이 매출이다', r'기타 매출(Other revenues) \1를 더한 것이 매출이다', h)   # 보도자료의 Other revenues — 부문 간 거래가 아니다(Codex 2026-11-06)
"""]


# ── 자동 카드 — 부문 지도 1판(원문 Q2 2026 838.3/652.8/1,649.0, 기타 180.7은 SEG_ADJ, 2026-11-05; Q3 2026 836.3/633.6/1,663.9, 기타 172.5) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
 ],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {
  "gpn:SmallAndMediumSizedBusinessesSegmentMember": [
   "중소 가맹점(SMB)",
   "#1b1f63"
  ],
  "gpn:EnterpriseSegmentMember": [
   "대형 가맹점(Enterprise)",
   "#5c6bc0"
  ],
  "gpn:PlatformsSegmentMember": [
   "플랫폼",
   "#b3b9e6"
  ]
 },
 "ignore": []
}
