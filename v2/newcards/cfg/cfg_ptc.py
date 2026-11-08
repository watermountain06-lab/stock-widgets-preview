CIK = '0000857005'
BUILD = {'no_dcf': '미완성 — Schneider 인수 종결 대기'}   # 2026-11-03 사용자 결정(보류 C군 → 미완성 카드), 2026-11-07 제작
# PTC v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 9월 30일. 제품 설계(CAD, Creo·Onshape)·수명주기 관리(PLM, Windchill·Codebeamer) 소프트웨어.
# 출처: SEC XBRL, Q3 FY26 10-Q(2026-07-31 16:01 동부 장 마감 뒤 → 첫 세션 08-03, 카드 기준일 11-06 종가) — FY26 10-K는 아직(실적 8-K 11-04는 자동 뉴스),
#        실적 보도자료(8-K 2.02항 — 모두 16:0x 동부 장 마감 뒤 → 다음 거래일), Schneider 합병 8-K(2026-10-05 07:22 장 전 → 같은 날 +33.5%).
# 미완성 사유: 2026-10-04 Schneider Electric 합병 계약(주당 $205 현금, 상장 폐지), PTC가 더 나은 제안을 받거나 이사회가 권고를 바꾸면 PTC가 $700M 파기 수수료(8-K 1.01항).
#   참고 점수 자기 79.4·동종 78.2 — 둘 다 최근 4분기 EPS에 든 Kepware·ThingWorx 매각 이익(Q2 FY26 세전 $462.6M, 관련 세금 Q2 인식 $102.4M → 9개월 누계 $95.6M — 10-Q; 세후 이익을 빼면 PER 약 27배) 때문에 PER이 낮게 나온 영향이 크다.
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q3 FY26', 'Q3 FY25', 'Q2 FY26'
L8 = ['Q4 FY24', 'Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26']
FY_ENDS, FY_LABEL = ('2025-09-30', '2024-09-30'), 'FY25'
VOTES, VERDICT = (1, 1, 0), '판정 보류'
CO = 'PTC'
S_ = 'https://www.sec.gov/Archives/edgar/data/857005/'
SEC = S_
TENQ = S_ + '000119312526328444/ptc-20260630.htm'; TENQ_NAME = 'Q3 FY26 10-Q'
PR = {'q3': S_ + '000119312526323617/ptc-ex99_1.htm', 'q2': S_ + '000119312526208904/ptc-ex99_1.htm',
      'q1': S_ + '000119312526037588/ptc-ex99_1.htm', 'q4': S_ + '000119312525266865/ptc-ex99_1.htm',
      'deal': S_ + '000119312526413124/d174191d8k.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="ptcFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(주가가 인수가 $205에 묶여 있다)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 45)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('미완성 카드다. 2026년 10월 Schneider Electric이 PTC를 주당 $205 현금에 인수하기로 합의했다 — 주가가 인수가에 묶여 움직이므로 배수와 현금흐름으로 단독 가치를 판정하지 않고, 자기 이력·동종업 점수는 참고값이다. '
              '최근 4분기 EPS에는 2026년 1~3월 Kepware·ThingWorx(산업용 IoT) 사업을 TPG 계열에 판 매각 이익(세전 $462.6M)이 들어 있어 PER이 낮게 나온다. 매각 뒤 분기(Q3 FY26) 매출은 1년 전보다 줄었다. '
              '카드 재무는 Q3 FY26 10-Q 기준이다(11월 4일 발표한 FY26 4분기 실적은 10-K가 나오면 반영된다).')
PH = ['PANW', 'CRM', 'MSFT', 'ORCL', 'PLTR']   # 비교 자료(카드 유니버스 IT)에 값이 있는 종목만
PEER_FILE = None
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '소프트웨어 5곳 PER 비교 (점수는 카드 유니버스 IT 기준)', 'pbr': '소프트웨어 PBR 비교', 'psr': '소프트웨어 PSR 비교',
                'pcr': '소프트웨어 PCR(FCF) 비교', 'evebitda': '소프트웨어 EV/EBITDA 비교'}
PEER_NAME_TITLE = '카드 유니버스 IT 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = '카드 유니버스 IT 종목 대비 배수 순위'
PEER_TIP = ('카드 유니버스 IT 종목(PTC 제외)과 배수 순위를 매긴 값이다.',
            '반도체·하드웨어·소프트웨어가 섞여 있다. 차트에는 소프트웨어 5곳만 보인다.')
# 매출(Q3 FY26 10-Q 제품군): PLM 357.0 + CAD 243.1 = 600.0(1년 전 403.7 + 240.2 = 643.9 — Kepware·ThingWorx는 PLM에 있다가 매각).
SEG = [('PLM(수명주기 관리)', 357.0, '#1f8a3a'), ('CAD(제품 설계)', 243.1, '#5cb85c')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 제품군별'
# 손 뉴스: 실적 3건(GAAP 희석 EPS) + Schneider 합병. FY26 4분기(11-04 장 마감 뒤)는 news_auto. 반응일: 16:0x 동부 장 마감 뒤 → 다음 거래일.
NEWS_RANGE = '2026.02 ~ 2026.11'
NEWS = [
    ('green', '2026년 10월 5일 장 전 — Schneider Electric이 주당 $205 현금 인수 합의', '2026-10-05',
     '인수가 $205(전 거래일 종가 $144.03 대비 약 42% 높음) · 상장 폐지 예정 · 더 나은 제안을 받아 PTC가 해지하거나 이사회가 권고를 바꿔 Schneider가 해지하면 PTC가 $700M 파기 수수료 — 당일 주가 +33.5%', 'deal', 'PTC 공시 (SEC 8-K)'),
    ('green', '2026년 7월 29일 장 마감 뒤 — Q3 FY26 실적', '2026-07-30',
     '매출 $600M(−6.8%, Kepware·ThingWorx 매각 뒤) · 순이익 $119M · 희석 EPS $1.03(1년 전 $1.17) — 다음 날 주가 +2.9%', 'q3', 'PTC 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 5월 6일 장 마감 뒤 — Q2 FY26 실적', '2026-05-07',
     '매출 $774M(+21.7%) · 순이익 $591M(매각 이익 포함) · 희석 EPS $4.98(1년 전 $1.35) — 다음 날 주가 +8.0%', 'q2', 'PTC 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 4일 장 마감 뒤 — Q1 FY26 실적', '2026-02-05',
     '매출 $686M(+21.4%) · 순이익 $167M · 희석 EPS $1.39(1년 전 $0.68) — 다음 날 주가 +1.7%', 'q1', 'PTC 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 17, 'nt': 14, 'mean': 183, 'median': 205, 'low': 115, 'high': 205, 'sb': 1, 'b': 0, 'h': 16, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-08'


# 미완성 카드 표시(2026-11-03 사용자 결정, FISV·MLM·NSC 방식).
INCOMPLETE_SHORT = 'Schneider 인수 종결 대기'
INCOMPLETE_WHY = '2026년 10월 Schneider Electric이 주당 $205 현금 인수에 합의했다 — 주가가 인수가에 묶여 움직여 단독 가치평가의 의미가 약하다. 인수가 끝나면 상장 폐지되고, 무산되면 그때 다시 본다'
POST = [r"""
import re as _re0
_w = '2026년 10월 Schneider Electric이 주당 $205 현금 인수에 합의했다 — 주가가 인수가에 묶여 움직여 단독 가치평가의 의미가 약하다. 인수가 끝나면 상장 폐지되고, 무산되면 그때 다시 본다'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — Schneider 인수 종결 대기</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — Schneider 인수 종결 대기. 주가가 인수가(주당 $205 현금)에 묶여 있어 현금흐름 내재가치를 계산하지 않았다.')
h = _re0.sub(r'(id="ptcFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)   # 미완성 — PER 구간 범위를 보이지 않는다(FISV처럼, Codex·Fable r1)
import re as _re3
h = _re3.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re3.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")

# 판정처럼 읽히는 자동 문구 정리(Codex·Fable r1, 2026-11-07) — 미완성 카드라 점수는 참고값, 주가는 인수가에 묶임
h = _re0.sub(r'<div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
h = _re0.sub(r'(<div class="vs-premise">PER [^<]*?이다\.)(</div>)', r'\1 — 미완성 카드라 참고값이다(PER은 Kepware·ThingWorx 매각 이익이 든 EPS 기준이고, 주가는 인수가 $205에 묶여 있다).\2', h, count=1)
h = _re0.sub(r'(<div class="verdict-summary-head">[^<]*)<span class="tag">[^<]*</span>', r'\1<span class="tag">Schneider 인수 종결 대기</span>', h, count=1)
h = _re0.sub(r'🔍 다음 확인 포인트 · [^<]*', '🔍 다음 확인 포인트 · FY26 10-K 접수(4분기 실적은 11/4 발표) · Schneider 합병 승인·종결.', h, count=1)
for _id in ('ptcDcfVerdict', 'ptcDcfBox', 'dcfPickValue'):
    h = h.replace(f'id="{_id}">계산 불가<', f'id="{_id}">보류(미완성)<')
h = _re0.sub(r'(초과 매우 비싸다">)계산 불가(</div>)', r'\1보류(미완성)\2', h, count=1)
"""]


# ── 자동 카드 — 부문 지도(손 작성, 제품군). 원문 대조: Q3 FY26 10-Q 357.0/243.1 = 600.0, 1년 전 403.7/240.2 = 643.9(2026-11-07) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "srt:ProductOrServiceAxis",
 "extra": {},
 "members": {"ptc:ProductLifecycleManagementMember": ["PLM(수명주기 관리)", "#1f8a3a"], "ptc:ComputerAidedDesignMember": ["CAD(제품 설계)", "#5cb85c"]},
 "ignore": ["ptc:RecurringServicesMember", "ptc:PerpetualLicenseMember"]   # 같은 축의 다른 구분(반복 매출·영구 라이선스)
}
