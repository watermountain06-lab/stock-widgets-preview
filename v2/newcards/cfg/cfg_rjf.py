BUILD = {'no_dcf': '미완성 — 은행 방식 장치 대기'}   # 2026-11-03 사용자 결정 — 미완성 카드(판정 보류)
# RJF(레이먼드 제임스) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 9월 30일. 자산관리·증권(PCG·자본시장·자산운용) + 은행 부문(예금 $63B).
# 출처: SEC XBRL, Q3 FY26 10-Q(2026-08-05), 실적 보도자료(Q1~Q4 FY26, 8-K 2.02항 — 장 마감 뒤 16시 동부 → 다음 거래일 반응), StockAnalysis. 사전 조사 scratchpad pre/RJF.md. FY2026 10-K는 11월 하순 예상.
# 미완성 사유(데이터 장치 없음, 2026-11-03 사용자 기준): 2026-11-04 사용자 결정으로 SCHW처럼 은행 경로(P/TBV·RIM)로 판정하기로 했으나, bank_fill.py가 연간 값을 12월 31일 결산만 읽어(253행)
# 9월 결산 RJF는 연간 시리즈가 비어 멈춘다(2026-11-04 시도). 은행 경로 장치를 고칠 때까지 일반 카드 틀로 보류. 은행 경로용 등록(daily_price.BANKS 등)은 되돌렸다.
# 일반 엔진 입력: 영업이익 = 순매출 − 비이자비용(DERIVED_OPINC, = 세전이익), 매출은 순매출(EXTRA_TAGS·EXCLUDE_TAGS — 총수익은 이자수익 포함), 차입 = 선순위채 $3,522M + 기타 차입 $950M(EV_TAGS_BY_CIK — 기본 태그 2022 멈춤), 예금은 차입 아님.
CIK = '0000720005'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q3 FY26', 'Q3 FY25', 'Q2 FY26'
L8 = ['Q4 FY24', 'Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26']
FY_ENDS, FY_LABEL = ('2025-09-30', '2024-09-30'), 'FY2025'
VOTES, VERDICT = (0, 0, 0), '판정 보류'
CO = 'Raymond James'
S_ = 'https://www.sec.gov/Archives/edgar/data/720005/'
SEC = S_
TENQ = S_ + '000072000526000070/rjf-20260630.htm'; TENQ_NAME = 'Q3 FY26 10-Q'
PR = {'q4': S_ + '000072000526000080/rjf20260930q426earnings.htm', 'q3': S_ + '000072000526000066/rjf20260630q326earnings.htm', 'q2': S_ + '000072000526000046/rjf20260331q226earnings.htm', 'q1': S_ + '000072000526000030/rjf20251231q126earnings.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="rjfFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {pct(HIST[\'margin_now\'])})</span>'
Y2 = (0, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('미완성 카드다. 은행 자회사(예금 $63B)를 가진 증권·자산관리 회사라 은행처럼 장부가치·초과이익으로 판정하기로 했지만, 그 계산 장치가 아직 9월 결산 회사를 읽지 못한다. 일반 기업용 배수(PSR·EV/EBITDA)와 현금흐름은 예금·고객 자금 때문에 뜻이 없어 판정에 쓰지 않는다. 재무 건전성의 순현금·이자보상배율은 은행·증권 자회사가 예금·고객 돈으로 들고 있는 현금($10.0B, 지주 현금은 약 $2.5B) 때문에 뜻이 없어 비웠고, 분기 FCF ‘적자 전환’도 고객 자금 변동 탓이다. 카드의 영업이익률은 세전이익률(순매출 − 비이자비용)이다. '
              'FY2026 4분기(7~9월) 실적은 10월 28일 이미 나왔다(순매출 $4.27B, +14.5%, 희석 EPS $3.40, 세전이익률 20.2%) — 카드 숫자는 연간 보고서(10-K, 11월 하순 예상) 전이라 3분기 10-Q 기준이고, 다음 실적 칸과 체크포인트도 그 분기를 가리킨다. 비교 종목은 S&P500 자산운용·수탁은행 기준이다.')
PRE = ['FB = None']   # 미완성 — 적정주가 '해당 없음'
BB_TAGS = ['StockRepurchasedDuringPeriodValue']   # 자사주 매입: PaymentsForRepurchaseOfCommonStock는 2023-06에 멈춤 — 자본변동표 값(Q3 FY26 $400M, 9M $1,200M, Fable r1)
PH = ['AMP', 'BLK', 'BNY', 'NTRS', 'STT', 'TROW']
PEER_FILE = 'peer_universe/asset_managers.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '자산관리·수탁 6곳 PER 비교 (점수는 S&P500 자산운용·수탁은행 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 자산운용·수탁은행 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 자산운용·수탁은행 대비 배수 순위 (v2/peer_universe/asset_managers.json)'
PEER_TIP = ('S&P500 자산운용·수탁은행 12곳과 배수 순위를 매긴 값이다.',
            '전통 운용사·대체투자사·수탁은행이 섞여 있다. 차트에는 6곳만 보인다.')
# 매출(Q3 FY26 10-Q 부문 순매출) — 2,841 + 477 + 362 + 488 = 4,168, Other·부문 간 제거 −240 → 3,928. 은행은 RjBankMember·BankSegmentMember 두 멤버에 같은 값이라 한쪽만.
SEG = [('PCG(재무설계사)', 2841, '#003c71'), ('자본시장', 477, '#4f86c6'), ('자산운용', 362, '#a7c4e4'), ('은행', 488, '#6b7f99')]
SEG_ADJ = -240
SEG_TITLE = '매출 구성 — 부문별 순매출(Q3 FY26)'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 마감 뒤 발표 → 다음 거래일.
NEWS_RANGE = '2026.01 ~ 2026.10'
NEWS = [
    ('green', '2026년 10월 28일 장 마감 뒤 — Q4 FY26 실적', '2026-10-29',
     '순매출 $4.27B(+14.5%) · 순이익 $666M · 희석 EPS $3.40(1년 전 $2.95) · 조정 EPS $3.59 · FY2026 희석 EPS $11.91 — 다음 날 주가 +2.5%', 'q4', 'Raymond James 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 7월 22일 장 마감 뒤 — Q3 FY26 실적', '2026-07-23',
     '순매출 $3.93B(+15.6%) · 순이익 $595M · 희석 EPS $3.01(1년 전 $2.12, 전년 소송 충당 $58M) · 조정 EPS $3.14 — 다음 날 주가 −1.1%', 'q3', 'Raymond James 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 4월 22일 장 마감 뒤 — Q2 FY26 실적', '2026-04-23',
     '순매출 $3.86B(+13.4%) · 순이익 $542M · 희석 EPS $2.72(1년 전 $2.36) · 조정 EPS $2.83 — 다음 날 주가 −0.7%', 'q2', 'Raymond James 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 1월 28일 장 마감 뒤 — Q1 FY26 실적', '2026-01-29',
     '순매출 $3.74B(+5.6%) · 순이익 $562M · 희석 EPS $2.79(1년 전 $2.86) · 조정 EPS $2.86 — 다음 날 주가 −0.4%', 'q1', 'Raymond James 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 16, 'nt': 11, 'mean': 181.91, 'median': 179, 'low': 160, 'high': 205, 'sb': 3, 'b': 3, 'h': 10, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-04'


# 미완성 카드 표시(2026-11-03 사용자 결정 — C·D·E 보류 카드는 있는 자료로 만들고 판정 보류 + 이유를 잘 보이게, SPCX 방식). BUILD no_dcf가 판정을 보류로 만들고, 보험사용 문구를 미완성 사유로 바꾼다.
INCOMPLETE_SHORT = '은행 방식 장치 대기'
INCOMPLETE_WHY = '은행 자회사를 가진 증권·자산관리 회사라 은행 방식(장부가치·초과이익)으로 판정하기로 했지만, 그 계산 장치가 12월 결산만 읽어 9월 결산인 이 회사를 아직 계산하지 못한다 — 장치를 고칠 때까지 보류'
POST = [r"""
_w = '은행 자회사를 가진 증권·자산관리 회사라 은행 방식(장부가치·초과이익)으로 판정하기로 했지만, 그 계산 장치가 12월 결산만 읽어 9월 결산인 이 회사를 아직 계산하지 못한다 — 장치를 고칠 때까지 보류'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — 은행 방식 장치 대기</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — 은행 방식 장치 대기. 현금흐름 내재가치는 계산하지 않았다.')
import re as _re3
h = _re3.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re3.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")   # 툴팁이 '계산 불가 — 미완성 — …'로 겹쳤다(Codex 2026-11-03)
""", '\nimport re as _re5\n# 증권·은행 지주라 일반 기업 안정성 판정이 맞지 않는다 — 순현금 Bull 줄을 빼고, 순현금·이자보상배율·안정성 종합 진단을 비운다(Codex r1 2026-11-04)\nh = _re5.sub(r\'<div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">부채</span><span class="bb-text">[^<]*순현금\\)\\.</span></div>\', \'\', h, count=1)\nh = _re5.sub(r\'이자보상배율 [\\d.,]+배\\.\', \'이자보상배율은 금융사라 뜻이 없어 쓰지 않는다.\', h, count=1)\n_js = ("<script>document.addEventListener(\'DOMContentLoaded\', function(){ setTimeout(function(){"\n       "var g=function(i){return document.getElementById(i)};"\n       "if(g(\'fundNetCashPs\')) g(\'fundNetCashPs\').textContent=\'해당 없음\';"\n       "if(g(\'fundNetCashNote\')) g(\'fundNetCashNote\').textContent=\'증권·은행 지주 — 현금 대부분이 은행·증권 자회사의 예금·고객 돈이라 순현금을 계산하지 않는다(지주 현금 약 $2.5B)\';"\n       "if(g(\'fundHealthTitle\')) g(\'fundHealthTitle\').textContent=\'종합 진단: 판정하지 않음 — 증권·은행 지주라 일반 기업 안정성 비율이 맞지 않는다\';"\n       "var r=document.querySelector(\'[data-fund-metric=\\"interestCoverage\\"]\'); if(r){var v=r.querySelector(\'.diag-value\'); if(v) v.textContent=\'해당 없음\'; var b=r.querySelector(\'.diag-badge\'); if(b){b.className=\'diag-badge\'; b.textContent=\'\'; b.title=\'\';}}"\n       "}, 0); });</script>\\n</body>")\nassert h.count(\'</body>\') == 1\nh = h.replace(\'</body>\', _js, 1)\n']


# ── 자동 카드 — 부문(축 하나만 붙은 값). 원문 대조: Q3 FY26 2,841/477/362/488, 조정 −240(2026-11-04) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenuesNetOfInterestExpense"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"rjf:PrivateClientGroupMember": ["PCG(재무설계사)", "#003c71"], "rjf:CapitalMarketsMember": ["자본시장", "#4f86c6"], "rjf:AssetManagementSegmentMember": ["자산운용", "#a7c4e4"], "rjf:RjBankMember": ["은행", "#6b7f99"]},
 "ignore": ["rjf:BankSegmentMember"]
}
