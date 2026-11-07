CIK = '0000842023'
BUILD = {'no_dcf': '미완성 — Merck KGaA 인수 종결 대기'}   # 2026-11-03 사용자 결정(보류 C군 → 미완성 카드), 2026-11-07 제작
NI_TAGS = ['ProfitLoss', 'NetIncomeLoss']   # FY26 10-K가 연간 순이익을 ProfitLoss로만 냈다($181.9M — 비지배지분 없어 같은 값), 없으면 Q4 FY26 순이익이 비어 빌드가 멈춤(2026-11-07)
# TECH(바이오-테크니) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 6월 30일. 연구용 단백질·항체 시약(Protein Sciences) + 진단·공간생물학 도구(Diagnostics and Spatial Biology).
# 출처: SEC XBRL, Q1 FY27 10-Q(2026-11-06 21:30 UTC = 16:30 동부 장 마감 뒤 접수 → 첫 세션 11-09; 주말에 11-06 종가로 만든다 — preflight EARLY_ASOF, 2026-11-07 사용자 결정).
#        합병 대기 중이라 Q1 FY27 실적 보도자료가 없다(10-Q만). 실적 보도자료(8-K 2.02항 — 장 전 06:30 동부 → 그날), 합병 계약 8-K(2026-06-25 08:21 동부 → 그날)·주총 8-K(09-23 17:08 동부 → 다음 날).
#        10-K/A(2026-10-28)는 원본 10-Q보다 앞이라 preflight 정정 검사에 걸리지 않는다.
# 엔진 입력(2026-11-07): 차입금 = 단기 $200M(회전 신용한도 — 6월 말엔 장기로 분류), 현금 $350.0M, 단기투자·비지배지분은 낡은 태그라 뺐다(EV_TAGS_BY_CIK).
#   4분기 EPS는 보도자료 값(Q4_EPS_OVERRIDE FY2023·FY2024·FY2026). 2022-11 4:1 분할.
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q1 FY27', 'Q1 FY26', 'Q4 FY26'
L8 = ['Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26', 'Q4 FY26', 'Q1 FY27']
FY_ENDS, FY_LABEL = ('2026-06-30', '2025-06-30'), 'FY2026'
VOTES, VERDICT = (0, -1, 0), '판정 보류'
CO = 'Bio-Techne'
S_ = 'https://www.sec.gov/Archives/edgar/data/842023/'
SEC = S_
TENQ = S_ + '000110465926123907/tech-20260930x10q.htm'; TENQ_NAME = 'Q1 FY27 10-Q'
PR = {'q4': S_ + '000110465926094391/tech-20260812xex99d1.htm', 'q3': S_ + '000110465926055887/tech-20260506xex99d1.htm',
      'q2': S_ + '000110465926009994/tech-20260204xex99d1.htm', 'deal': S_ + '000199937126013429/ex99-1.htm',
      'dealterms': S_ + '000199937126013527/tech-8k_062326.htm', 'vote': S_ + '000114036126037450/ef20082601_ex99-1.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="techFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(Merck KGaA 인수 종결 대기 — 주가가 인수가 주당 73달러 현금에 묶여 있다)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (-10, 40)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('미완성 카드다. 2026년 6월 25일 독일 Merck KGaA가 주당 73달러 현금(기업가치 약 $11.3B)에 인수하기로 계약했다. 미국 반독점(HSR) 대기 기간이 9월 18일 끝났고 9월 23일 주주가 승인했으며(찬성 약 99%), 회사는 남은 규제 승인을 받아 2026년 말~2027년 초 종결을 예상한다. '
              '2027년 3월 25일까지 끝나지 않으면 양쪽이 계약을 해지할 수 있다(독점·투자 심사 승인이나 그에 붙는 부담 조건만 남았으면 2027년 6월 25일·9월 25일로 두 번 자동 연장). '
              '계약이 깨져도 수수료가 늘 생기지는 않는다 — 회사가 Merck KGaA에 내는 $230M은 다른 인수 제안 수락·이사회 추천 변경 같은 사유라 주총 승인 뒤에는 사실상 남지 않았고, Merck KGaA가 회사에 내는 $576M은 규제 승인 미충족·금지명령 같은 사유다. '
              '카드 제작일 11월 6일 종가는 인수가보다 약 0.3% 낮고, 종결 전 기준일(11월 13일)을 지나면 분기 배당 $0.08은 그대로 받는다(11월 3일 선언). 합병 계약 중에는 Merck KGaA 동의 없이 자사주를 살 수 없다. '
              '합병 발표 뒤 실적 콘퍼런스콜을 중단했고(Q4 FY26 보도자료), Q1 FY27은 보도자료 없이 10-Q만 냈다. 이 분기 영업이익에는 인수 관련 비용 등 $17.8M(1년 전 $3.4M)이 들어 있다. '
              '애널리스트 평균 목표주가에는 인수가를 반영하지 않은 옛 목표가가 섞여 있다.')
PH = ['TMO', 'DHR', 'A', 'WAT', 'MTD', 'IQV']
PEER_FILE = 'peer_universe/health_care.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '생명과학 도구 6곳 PER 비교 (점수는 S&P500 헬스케어 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 헬스케어 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 헬스케어 대비 배수 순위 (v2/peer_universe/health_care.json)'
PEER_TIP = ('S&P500 헬스케어(TECH 제외)와 배수 순위를 매긴 값이다.',
            '제약·의료기기·보험이 섞여 있다. 차트에는 생명과학 도구 6곳만 보인다.')
# 매출(Q1 FY27 10-Q 부문 표): 단백질 과학 219,691 + 진단·공간생물학 80,164 − 부문 간 143 = 연결 299,712(천 달러).
SEG = [('단백질 과학(시약·분석 장비)', 219.7, '#00558f'), ('진단·공간생물학', 80.2, '#8dc63f')]
SEG_ADJ = -0.1
SEG_ADJ_LABEL = '부문 간 거래'
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 실적 3건 + 합병 계약·주총. 최신 실적 8-K(Q4 FY26)보다 뒤인 주총 항목이 있어 news_auto 자동 항목은 빠진다 — Q4 FY26도 손으로 쓴다.
# 반응일: 실적 8-K 장 전 06:30 동부 → 그날. 합병 계약 08:21 동부 → 그날. 주총 17:08 동부 → 다음 날.
NEWS_RANGE = '2026.02 ~ 2026.09'
NEWS = [
    ('neutral', '2026년 9월 23일 장 마감 뒤 — 주주총회 합병 승인', '2026-09-24',
     'Merck KGaA 인수안 주주 승인 · 미국 독점 심사 대기 기간 9월 18일 만료 · 2026년 말~2027년 초 종결 예상 — 다음 날 주가 +0.1%', 'vote', 'Bio-Techne 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 8월 12일 장 전 — Q4 FY26 실적', '2026-08-12',
     '매출 $321.2M(+1%, 유기 +3%) · 순이익 $55M · 희석 EPS $0.35(1년 전 −$0.11) · 조정 EPS $0.52 — 그날 주가 +0.1%(인수가에 묶임)', 'q4', 'Bio-Techne 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 6월 25일 장 전 — Merck KGaA 인수 계약', '2026-06-25',
     '주당 $73 현금, 기업가치 약 $11.3B · 해지 수수료 회사 $230M·Merck KGaA $576M — 그날 주가 +20.1%', 'dealterms', 'Bio-Techne 합병 계약 공시 (SEC 8-K)'),
    ('red', '2026년 5월 6일 장 전 — Q3 FY26 실적', '2026-05-06',
     '매출 $311.4M(−2%) · 순이익 $51M · 희석 EPS $0.32(1년 전 $0.14) · 조정 EPS $0.53(1년 전 $0.56) — 그날 주가 −16.4%', 'q3', 'Bio-Techne 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 4일 장 전 — Q2 FY26 실적', '2026-02-04',
     '매출 $295.9M(0%) · 순이익 $38M · 희석 EPS $0.24(1년 전 $0.22) · 조정 EPS $0.46 — 그날 주가 +6.3%', 'q2', 'Bio-Techne 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 13, 'nt': 11, 'mean': 67.09, 'median': 73, 'low': 50, 'high': 73, 'sb': 0, 'b': 0, 'h': 12, 's': 0, 'ss': 1}
ANALYST_ASOF = '2026-11-07'
BB_NONE = {'2026-09-30': '없음($0) — 합병 계약상 Merck KGaA 동의 없이 매입 불가(10-Q)'}   # Q1 FY27 10-Q 현금흐름표 매입 줄 —, Part II 매입 표 7~9월 0(Codex r1)

# 미완성 카드 표시(2026-11-03 사용자 결정, D·SRE 방식 — 현금 인수 대상).
INCOMPLETE_SHORT = 'Merck KGaA 인수 종결 대기'
INCOMPLETE_WHY = '2026년 6월 Merck KGaA가 주당 73달러 현금에 인수하기로 계약했다(9월 주주 승인, 2026년 말~2027년 초 종결 예상) — 주가가 인수가에 묶여 배수 판정이 의미 없고, 종결되면 상장 폐지된다. 종결 또는 무산 뒤 다시 본다'
POST = [r"""
import re as _re0
_w = '2026년 6월 Merck KGaA가 주당 73달러 현금에 인수하기로 계약했다(9월 주주 승인, 2026년 말~2027년 초 종결 예상) — 주가가 인수가에 묶여 배수 판정이 의미 없고, 종결되면 상장 폐지된다. 종결 또는 무산 뒤 다시 본다'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — Merck KGaA 인수 종결 대기</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — Merck KGaA 인수 종결 대기. 주가가 인수가 주당 73달러에 묶여 현금흐름 내재가치를 계산하지 않았다.')
h = _re0.sub(r'(id="techFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)
h = _re0.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re0.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")
h = _re0.sub(r'(<div class="verdict-summary-head">[^<]*)<span class="tag">[^<]*</span>', r'\1<span class="tag">Merck KGaA 인수 종결 대기</span>', h, count=1)
h = _re0.sub(r'<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
h = _re0.sub(r'<div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
h = h.replace('Bio-Techne Q1 FY27 실적 보도자료 (SEC 8-K) →', 'Bio-Techne Q1 FY27 10-Q (SEC) →')   # 합병 대기로 Q1 FY27 보도자료가 없다 — 링크는 10-Q(Codex r1)
"""]


# ── 자동 카드 — 부문 지도(seg_map_propose 전부 맞음). 원문 대조: Q1 FY27 10-Q 부문 표 219,691 + 80,164 − 부문 간 143 = 299,712(2026-11-07) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"tech:ProteinSciencesMember": ["단백질 과학(시약·분석 장비)", "#00558f"], "tech:DiagnosticsAndSpatialBiologyMember": ["진단·공간생물학", "#8dc63f"]},
 "ignore": []
}
