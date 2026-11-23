CIK = '0001063761'
BUILD = {'cover_shares': True, 'no_dcf': '미완성 — 최근 4분기 순이익의 절반 이상이 Taubman 재평가 이익(일회성·비현금)'}   # 2026-11-20 일회성 기준으로 미완성
# SPG(사이먼 프로퍼티) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 12월 31일. 쇼핑몰·프리미엄 아웃렛 리츠(UPREIT).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-11-06 접수, 카드 기준일 11-19 종가), 실적 보도자료(8-K 2.02항 — 모두 동부 오후 4시대 접수 = 장 마감 뒤 → 다음 세션), 8-K(자사주 2/5, 경영진 3/24), StockAnalysis.
# 2026-10-22·10-24 두 번 보류(초안 v2/research/drafts/cfg_spg_draft.py) → 2026-11-20 다시 만듦:
#   ① 운영 파트너십 외부 파트너 유닛(5,576만, 보통주와 1:1 교환)은 share_claims 표(SPG-op-lp-units, 2026-09-30 행 추가)로 주식 수·배수 시가총액에 모두 들어간다 — 첫 보류 사유 해소.
#   ② Taubman 재평가 이익 — 일회성 기준(≥30% → 미완성, skipped_cards "일회성 크기 기준")으로 미완성 카드.
# 일회성(금액 기준, 세후·보통주 — 지분율은 2026-09-30 85.3%로 어림한 추정, Codex r1): 최근 4분기 보통주 순이익 $4,510M(4분기 $3,048M + 1~9월 $1,462M, 희석 EPS 9.35 + 1.48 + 1.49 + 1.54 = 13.86).
#   이익: Taubman 잔여 지분 인수에 따른 기존 지분 재평가 이익 $2,858M(10-Q, 보도자료 $2.89B) — 외부 파트너 몫 약 14.7%를 빼도 보통주 몫 약 $2.44B = 54%.
#   비용: 4분기 Catalyst Brands 구조조정·원가법 투자 평가 손실 $121M, Klépierre 교환사채 평가 손실 4분기 $21M, 3분기 평가 손실 $100M 등 — 빼도 순 일회성 40% 이상 → 미완성.
# 리츠: WELL·PLD·EQIX 선례대로 일반 규칙(영업이익 = 10-Q "Operating income before other items"), FFO는 판정에 쓰지 않는다. 순이익 = 보통주 귀속(NI_TAGS).
# EV 비지배지분 = 부동산 비지배 $355M + 임시 자본 $269M(EV_TAGS_BY_CIK). 주식 수는 보통주 + B주 8,000(표지 클래스별, BUILD cover_shares).
# 합작 지분법 투자는 지분법 이익만 순이익에 들어오고 매출·EBITDA·차입금은 연결 밖(MODEL_NOTE, 안건 E41). 4분기 EPS 2025 보도자료 $9.35(Q4_EPS_OVERRIDE).
NI_TAGS = ['NetIncomeLossAvailableToCommonStockholdersBasic']
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, 0, 0), '판정 보류'
CO = 'Simon'
S_ = 'https://www.sec.gov/Archives/edgar/data/1063761/'
SEC = S_
TENQ = S_ + '000110465926123591/spg-20260930x10q.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000110465926123325/tm2627777d2_ex99-1.htm', 'q2': S_ + '000110465926093361/tm2620726d2_ex99-1.htm',
      'q1': S_ + '000110465926058646/tm2611645d2_ex99-1.htm', 'q4': S_ + '000110465926009209/tm263695d2_ex99-1.htm'}
LINKS = {'ceo': S_ + '000110465926033931/tm269613d1_ex99-1.htm', 'buyback': S_ + '000110465926010999/tm265229d2_ex99-1.htm'}
FAIRBAND_TITLE = 'id="spgFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(최근 4분기 EPS의 절반 이상이 Taubman 재평가 이익이다)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (미완성 — 현금흐름 보류)</span>'
Y2 = (0, 80)
ACT_REASON = '리츠라 재고·매출채권 회전으로 보는 활동성이 잘 맞지 않는다'
NONOP_WHAT = '투자'
MODEL_NOTE = ('미완성 카드다. 최근 4분기 EPS($13.86)에는 2025년 10월 Taubman Realty Group 잔여 지분을 인수하면서 기존 지분(88%)을 공정가치로 다시 잰 비현금 이익 $2.86B가 들어 있다. 외부 파트너 몫(현재 지분율 14.7%로 어림)을 빼도 보통주 순이익의 절반이 넘는다(약 54%). 이 이익만 빼면 PER은 약 35배(같은 기간 일회성 손실까지 되돌리면 약 32배)로 5년 범위 상단이라, 지금 PER·자기 이력·동종업 점수는 실제보다 싸게 보인다 — 그래서 판정을 보류한다. 이 이익이 든 4분기가 최근 4분기에서 빠지는 2026년 4분기 실적(2027년 2월 초 예상) 무렵 새 최근 4분기로 다시 잰다(자동으로 정식이 되지는 않는다). '
              '리츠는 건물 감가상각이 커서 GAAP 순이익이 실제 현금 창출보다 작게 나오고, 업계는 FFO(순이익에 부동산 감가상각을 되더하고 매각·재평가 이익을 뺀 값)로 본다 — 3분기 회사 정의 Real Estate FFO는 주당 $3.37(1년 전 $3.22), 평가 손실까지 넣은 FFO는 $3.09(1년 전 $3.25)다. 사이트에는 리츠 전용 평가가 아직 없다. '
              '운영 파트너십 외부 파트너 유닛(약 5,576만, 보통주와 1:1 교환)은 주식 수와 PSR·PBR·PCR·EV/EBITDA의 시가총액에 더했다(PER은 보통주 EPS 기준이라 해당 없음). 합작 쇼핑몰과 기타 플랫폼 투자(재무상태표 지분법 투자 $4.0B, Klépierre 지분 포함 $5.3B)는 지분법 이익만 순이익에 들어오고 그 매출·EBITDA·차입금은 연결 숫자에 없다 — 시가총액에는 합작 가치가 들어 있어 PSR·EV/EBITDA는 그만큼 비싸 보이고, 회사 몫으로 합친 차입금($35.4B)은 연결 차입금($28.4B)보다 크다.')
HEALTH_EXTRA = '부채비율이 매우 높게 나오는 것은 누적 배당과 감가상각으로 장부상 자본이 작기 때문이다 — 리츠는 보통 부채를 자산 가치나 이익 대비로 본다 — 순차입금은 최근 4분기 EBITDA의 약 5.4배다.'
PH = ['PLD', 'WELL', 'EQIX', 'O', 'AMT', 'PSA']
PEER_FILE = 'peer_universe/real_estate.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '리츠 6곳 PER 비교 (점수는 S&P500 부동산 기준)', 'pbr': '리츠 PBR 비교', 'psr': '리츠 PSR 비교',
                'pcr': '리츠 PCR(FCF) 비교', 'evebitda': '리츠 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 부동산 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 부동산 대비 배수 순위 (v2/peer_universe/real_estate.json)'
PEER_TIP = ('S&P500 부동산(SPG 제외)과 배수 순위를 매긴 값이다.',
            '쇼핑몰·물류·데이터센터·통신탑·주거·헬스케어 리츠가 섞여 있다. 차트에는 대형 리츠 6곳만 보인다.')
# 매출(Q3 2026 10-Q 손익계산서) — 임대 수익 1,681.4 + 기타 수익 87.0 + 관리 수수료·기타 46.2 = 1,814.6. 1년 전 1,452.9·111.7·36.9 → 1,601.6.
SEG = [('임대 수익', 1681.4, '#1d3c6e'), ('기타 수익', 87.0, '#6b8fc7'), ('관리 수수료·기타', 46.2, '#a8bfe0')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 손익계산서 항목별'
# 손 뉴스: 실적 5건(EPS는 GAAP 보통주 귀속 — 보도자료의 FFO는 참고로만), 경영진 교체, 자사주. 가이던스는 쓰지 않는다.
# 반응일(SEC acceptanceDateTime UTC → 동부): 실적 8-K 2025-11-03T21:08Z·2026-02-02T21:12Z·05-11T20:07Z·08-10T20:07Z·11-05T21:08Z = 장 마감 뒤 → 다음 세션.
# 자사주 8-K 2026-02-05T21:44Z → 2/6. David Simon 별세(3/22) 보도자료는 3/23자, 8-K는 3/24T21:07Z — 반응일은 보도자료 날인 3/23(첫 공개일).
# 주가 변동(Yahoo 종가, 전 거래일 대비): 11/4 +3.4%, 2/3 −0.9%, 2/6 +1.2%, 3/23 −1.6%, 5/12 +2.3%, 8/11 −0.5%, 11/6 +0.8%.
# 넣지 않은 8-K: 신용 약정(3/5), 주총(5/15), 임원(2/5 5.02항).
NEWS_RANGE = '2025.11 ~ 2026.11'
NEWS = [
    ('neutral', '2026년 11월 5일 장 마감 뒤 — Q3 2026 실적', '2026-11-06',
     '총매출 $1.81B(+13.3%, 대부분 Taubman 연결 효과) · 희석 EPS $1.54(이번 분기 비현금 평가 손실 $0.27 포함) · 1년 전 $1.86 · 분기 배당 $2.30으로 인상 — 다음 날 주가 +0.8%', 'q3', 'Simon 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 8월 10일 장 마감 뒤 — Q2 2026 실적', '2026-08-11',
     '총매출 $1.79B(+19.5%) · 희석 EPS $1.49 · 1년 전 $1.70(그때 투자 관련 비현금 이익 $0.21 포함) — 다음 날 주가 −0.5%', 'q2', 'Simon 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 5월 11일 장 마감 뒤 — Q1 2026 실적', '2026-05-12',
     '총매출 $1.76B(+19%) · 희석 EPS $1.48(1년 전 $1.27) · 미국 몰·아웃렛 입점률 96.0% — 다음 날 주가 +2.3%', 'q1', 'Simon 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 3월 23일 — David Simon 회장 겸 CEO 별세', '2026-03-23',
     '3월 22일 별세 — 아들 Eli Simon(COO)이 CEO·사장, Larry Glasscock이 비상임 이사회 의장 — 그날 주가 −1.6%', 'ceo', 'Simon 보도자료·공시 (SEC 8-K)'),
    ('neutral', '2026년 2월 5일 장 마감 뒤 — 자사주 매입 $2.0B 승인', '2026-02-06',
     '새 보통주 매입 프로그램 최대 $2.0B — 만료를 앞둔 기존 $2.0B 프로그램(잔여 약 $1.7B)을 대체 — 다음 날 주가 +1.2%', 'buyback', 'Simon 공시 (SEC 8-K)'),
    ('neutral', '2026년 2월 2일 장 마감 뒤 — Q4 2025 실적', '2026-02-03',
     '희석 EPS $9.35(1년 전 $2.04) — 주로 Taubman 잔여 지분 인수에 따른 비현금 재평가 이익 $2.89B(Taubman 몫 $2.86B) 포함 — 다음 날 주가 −0.9%', 'q4', 'Simon 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 11월 3일 장 마감 뒤 — Q3 2025 실적', '2025-11-04',
     '희석 EPS $1.86(1년 전 $1.46) — 다음 날 주가 +3.4%', 'q3old', 'Simon 실적 보도자료 (SEC 8-K)'),
]
PR['q3old'] = S_ + '000110465925105545/tm2528944d2_ex99-1.htm'
ANALYST = {'rating': 'Buy', 'n': 21, 'nt': 17, 'mean': 233.5, 'median': 227, 'low': 207, 'high': 275, 'sb': 5, 'b': 1, 'h': 15, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-23'

INCOMPLETE_SHORT = 'Taubman 재평가 이익이 큼'
INCOMPLETE_WHY = '최근 4분기 EPS($13.86)에 2025년 4분기 Taubman 잔여 지분 인수로 생긴 비현금 재평가 이익($2.86B)이 들어 있어, 외부 파트너 몫을 빼도 보통주 순이익의 절반이 넘는다(현재 지분율로 어림하면 약 54%) — 배수 판정이 왜곡돼 보류한다. 이 분기가 빠지는 2026년 4분기 실적 뒤 다시 본다'
POST = [r"""
import re as _re0
_w = '최근 4분기 EPS($13.86)에 2025년 4분기 Taubman 잔여 지분 인수로 생긴 비현금 재평가 이익($2.86B)이 들어 있어, 외부 파트너 몫을 빼도 보통주 순이익의 절반이 넘는다(현재 지분율로 어림하면 약 54%) — 배수 판정이 왜곡돼 보류한다. 이 분기가 빠지는 2026년 4분기 실적 뒤 다시 본다'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — Taubman 재평가 이익이 큼 · 2027년 2월 재검토</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — Taubman 재평가 이익이 큼. 미완성 카드 규칙에 따라 종합 판정과 함께 현금흐름 내재가치도 보류했다.')
h = _re0.sub(r'(id="spgFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)
h = _re0.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re0.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")
h = _re0.sub(r'(<div class="verdict-summary-head">[^<]*)<span class="tag">[^<]*</span>', r'\1<span class="tag">Taubman 재평가 이익이 큼</span>', h, count=1)
h = _re0.sub(r'<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
h = _re0.sub(r'<div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
"""]

# 배당 칸 — 보통주 배당 지급 태그가 없어 "공시 없음"으로 나왔다(Fable r1 2026-10-22 ③). 10-Q 현금흐름표 "Preferred dividends and distributions to stockholders" 1~9월 $2,172.5M.
POST.append(r"""
h = h.replace('<span class="zone-label">보통주 배당 지급</span>\n          <span class="zone-val">공시 없음</span>', '<span class="zone-label">배당 지급 (연초~9/30, 39주 — 보통주·우선주 합계, 유닛 분배 $375M 별도)</span>\n          <span class="zone-val">$2.2B</span>', 1)
""")

# 엔진 공통 문구 고침(Codex·Fable r1 2026-11-20): 순차입금에 리스가 없다(10-Q 리스 부채 $725M 별도), 매출 항목은 손익계산서, 체크포인트 ①은 Taubman 연결 효과 주석.
POST.append(r"""
h = h.replace('순차입금(리스 포함)', '순차입금')
h = h.replace('Q3 2026 10-Q 부문 표 (SEC)', 'Q3 2026 10-Q 손익계산서 (SEC)')
import re as _re1
h = _re1.sub(r'(<strong style="color:var\(--accent2\);">①</strong>[^<]*?)(</div>)', lambda m: m.group(1) + ' — 2025년 10월 말 Taubman 연결로 커진 매출이 비교 분기에도 들어가 증가율이 저절로 낮아진다(미국 부동산 NOI 증가율 3분기 +6.6%를 함께 본다)' + m.group(2), h, count=1)
""")

# ── 자동 카드 — 손익계산서 항목 3개(축 없음). 원문 대조: Q3 2026 1,681.4/87.0/46.2, 1년 전 1,452.9/111.7/36.9(2026-11-20) ──
AUTO = True
SEG_MAP = {
 "concepts": [],
 "axis": None,
 "extra": {},
 "members": {"us-gaap:OperatingLeaseLeaseIncome": ["임대 수익", "#1d3c6e"], "us-gaap:OtherIncome": ["기타 수익", "#6b8fc7"],
             "spg:ManagementFeesAndOtherRevenues": ["관리 수수료·기타", "#a8bfe0"]},
 "ignore": []
}
