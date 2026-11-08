BUILD = {'eps_tag': 'IncomeLossFromContinuingOperationsPerDilutedShare,EarningsPerShareDiluted', 'no_dcf': '미완성 — 분사 재작성 대기'}   # 2026-04-01 EDS(Versigent) 분사 — 2026-11-04 사용자 기준(분사로 숫자가 깨진 카드는 미완성)
NI_TAGS = ['IncomeLossFromContinuingOperations', 'NetIncomeLoss']
# APTV(앱티브) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 12월 31일. 자동차 전장 — 커넥터·케이블(Engineered Components), 센서·컴퓨트·소프트웨어(Intelligent Systems). 저지 설립·스위스 세금 거주.
# 출처: SEC XBRL, Q3 2026 10-Q(2026-11-03 장 마감 뒤 접수 → 기준일 11-04 종가), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 장 전 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/APTV.md. 비교군 consumer_discretionary(CMG·GPC와 같음).
# 미완성 사유(2026-11-04 사용자 기준 — 분사로 숫자가 깨진 카드): 2026-04-01 EDS(Versigent, VGNT) 분사. 2026 Q2부터 계속사업 기준으로 재작성됐지만 FY2025 10-K·Q4 2025·Q1 2026은 EDS 포함 숫자라
# 최근 4분기 EPS·매출이 두 기준을 섞는다(Q4 2025 매출 $5.15B 대 Q3 2026 $3.20B). 과거 일봉도 분사 배당(3주당 VGNT 1주) 전후로 이어 붙여 PER·PBR 이력이 끊긴다. 계속사업 기준 Q4 2025는 FY2026 10-K(2027-02 예상)에서 처음 나온다.
# 보류 전 점수(참고): 자기 86.0·동종 89.5 — 섞인 숫자라 쓰지 않는다. Q4 2025 EPS는 보도자료 0.64(Q4_EPS_OVERRIDE — 역산 1.83은 분사 전 연간 − 재작성 9개월), 단기투자 2024 멈춘 태그는 EV_TAGS_BY_CIK로 뺐다(Codex·Fable r1). EPS 태그는 계속사업 희석 EPS 우선(BUILD eps_tag). 현금흐름은 계산하지 않는다(BUILD no_dcf).
CIK = '0001521332'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, 1, 0), '판정 보류'
CO = 'Aptiv'
S_ = 'https://www.sec.gov/Archives/edgar/data/1521332/'
SEC = S_
TENQ = S_ + '000152133226000075/aptv-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000152133226000071/aptvq32026ex991.htm', 'q2': S_ + '000152133226000057/aptvq22026ex991.htm', 'q1': S_ + '000152133226000044/aptvq12026ex991.htm', 'q4': S_ + '000152133226000004/aptv2025ex991.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="aptvFairBand" title="분사 전후 EPS가 섞여 PER 구간으로 낸 적정주가가 의미 없어 표시하지 않는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {pct(HIST[\'margin_now\'])})</span>'
Y2 = (0, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('미완성 카드다. 2026년 4월 1일 배선 사업(EDS)을 Versigent(VGNT)로 분사해, 최근 4분기 중 앞 두 분기는 분사 전 숫자이고 뒤 두 분기는 분사 뒤 숫자다. 그래서 PER·PSR과 그 이력이 같은 회사를 비교하지 못하고, 분사 전 기간이 다시 계산된 4분기 실적·연간 보고서(2027년 2월 예상)가 나와야 판정할 수 있다. 카드의 1년 전 비교(매출 −38.6% 등)는 분사 전 숫자와 비교한 값이고 같은 기준(계속사업)으로는 3분기 매출 +2.3%다. 1년 주가 수익률도 4월 분사 배당(3주당 VGNT 1주)을 반영하지 않아 손실이 크게 보인다. PER은 분사 전후 EPS를 더한 값이라 참고용이다. '
              '분사 뒤 회사의 2026년 가이던스는 매출 $12.65~12.75B, GAAP 계속사업 희석 EPS $3.95~4.15다. Motional·StradVision 지분(장부 약 $1.3B)이 있고 배당은 없다. 비교 종목은 S&P500 경기소비재 기준이다.')
PRE = ['FB = None']   # 분사 전후 EPS가 섞인 PER 구간 — 적정주가를 '해당 없음'으로(Codex·Fable r1)
PH = ['GM', 'F', 'TSLA', 'GPC', 'AZO', 'ORLY']
PEER_FILE = 'peer_universe/consumer_discretionary.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '자동차·부품 6곳 PER 비교 (점수는 S&P500 경기소비재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 경기소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 경기소비재 대비 배수 순위 (v2/peer_universe/consumer_discretionary.json)'
PEER_TIP = ('S&P500 경기소비재(APTV 제외)와 배수 순위를 매긴 값이다.',
            '자동차·주택·외식·호텔·소매가 섞여 있다. 차트에는 자동차·부품 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문 외부 매출) — 1,815 + 1,384 = 3,199. 부문 순매출(Revenues)은 내부 매출 38을 이중으로 세므로 쓰지 않는다.
SEG = [('Engineered Components', 1815, '#f84018'), ('Intelligent Systems', 1384, '#5f6b73')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별(Q3 2026)'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석 — Q4 2025·Q1 2026은 분사 전 연결, Q2·Q3 2026은 계속사업). 반응일: 장 전 발표 → 같은 날.
NEWS_RANGE = '2026.02 ~ 2026.11'
NEWS = [
    ('red', '2026년 11월 3일 장 전 — Q3 2026 실적', '2026-11-03',
     '매출 $3.20B(+2.3%, 계속사업) · 순이익 $194M · 희석 EPS $0.94(1년 전 계속사업 −$2.24, Wind River 영업권 손상) · 조정 EPS $1.42 · 연간 가이던스 조정 EPS $5.60~5.80 — 당일 주가 −6.5%', 'q3', 'Aptiv 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 8월 4일 장 전 — Q2 2026 실적(분사 뒤 첫 분기)', '2026-08-04',
     '매출 $3.27B(+2.3%, 계속사업) · 계속사업 순이익 $298M · 계속사업 희석 EPS $1.40(1년 전 $1.21) · 조정 EPS $1.63 · 연간 조정 EPS 가이던스 하향 — 당일 주가 −16.6%', 'q2', 'Aptiv 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 5월 5일 장 전 — Q1 2026 실적(분사 전 기준)', '2026-05-05',
     '매출 $5.09B(+5.4%, EDS 포함) · 순이익 $189M · 희석 EPS $0.88(1년 전 −$0.05) · 조정 EPS $1.71 — 당일 주가 −7.9%', 'q1', 'Aptiv 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 2일 장 전 — Q4 2025 실적(분사 전 기준)', '2026-02-02',
     '매출 $5.15B(+5.0%, EDS 포함) · 순이익 $138M · 희석 EPS $0.64(1년 전 $1.14, 세금 증가) · 조정 EPS $1.86 — 당일 주가 +2.9%', 'q4', 'Aptiv 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 20, 'nt': 14, 'mean': 62.71, 'median': 64, 'low': 45, 'high': 94, 'sb': 10, 'b': 5, 'h': 5, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-08'


# 미완성 카드 표시(2026-11-03 사용자 결정 — C·D·E 보류 카드는 있는 자료로 만들고 판정 보류 + 이유를 잘 보이게, SPCX 방식). BUILD no_dcf가 판정을 보류로 만들고, 보험사용 문구를 미완성 사유로 바꾼다.
INCOMPLETE_SHORT = '분사 재작성 대기'
INCOMPLETE_WHY = '2026년 4월 EDS(Versigent) 분사로 최근 4분기 중 앞 두 분기는 분사 전, 뒤 두 분기는 분사 뒤 숫자라 배수와 그 이력이 같은 회사를 비교하지 못한다 — 분사 전 기간이 재작성된 연간 보고서(2027년 2월 예상)가 나올 때까지 보류'
POST = [r"""
_w = '2026년 4월 EDS(Versigent) 분사로 최근 4분기 중 앞 두 분기는 분사 전, 뒤 두 분기는 분사 뒤 숫자라 배수와 그 이력이 같은 회사를 비교하지 못한다 — 분사 전 기간이 재작성된 연간 보고서(2027년 2월 예상)가 나올 때까지 보류'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — 분사 재작성 대기</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — 분사 재작성 대기. 현금흐름 내재가치는 계산하지 않았다.')
import re as _re3
h = _re3.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re3.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")   # 툴팁이 '계산 불가 — 미완성 — …'로 겹쳤다(Codex 2026-11-03)
""", "\nimport re as _re4\n# 분사 전후가 섞인 1년 전 비교를 추세로 읽는 자동 문장 — Q3 2026에만(다음 분기엔 맞지 않아 그대로 지나간다, Codex r2 2026-11-04)\nh = _re4.sub(r'매출 증가율\\(1년 전 대비\\)이 최근 흐름\\([^)]*\\)보다 낮아지지 않는지', '계속사업 매출이 회사 4분기 가이던스($3.11~3.21B) 안에 드는지 — 1년 전 대비 증가율은 분사 전후가 섞여 추세로 보지 않는다', h, count=1)\nh = _re4.sub(r'(지배적 내러티브 · Q3 2026 매출 \\$[\\d.]+B)\\([^)]*\\)(, 영업이익률 [\\d.]+%)\\(1년 전 [^)]*\\)\\. 주가는 1년 새 [^<]*?(<span)', r'\\1(계속사업 기준 1년 전 대비 +2.3%)\\2. 1년 전 수치와 주가 수익률은 분사 전 기준이라 견주지 않는다\\3', h, count=1)\nh = h.replace('·매출 감소 커짐</span>', '·분사로 1년 비교 불가</span>', 1)\nh = _re4.sub(r'Q3 2026 매출 [−\\-][\\d.]+%\\(보고 기준, 3년 연평균 [^)]*\\)\\.', 'Q3 2026 계속사업 매출 +2.3%로 성장이 느리다(분사 전 숫자와 비교한 보고 기준 감소율은 쓰지 않는다).', h, count=1)\n"]


# ── 자동 카드 — 부문(축 하나만 붙은 값). 원문 대조: Q3 2026 1,815/1,384(2026-11-04) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"aptv:EngineeredComponentsMember": ["Engineered Components", "#f84018"], "aptv:IntelligentSystemsMember": ["Intelligent Systems", "#5f6b73"]},
 "ignore": []
}
