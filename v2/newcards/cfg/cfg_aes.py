CIK = '0000874761'
BUILD = {'no_dcf': '미완성 — GIP·EQT 인수 종결 대기',   # 2026-11-03 사용자 결정(보류 C군 → 미완성 카드), 2026-11-07 제작
         # 재무상태표 차입금이 RecourseStatusAxis 차원으로만 실린다(companyfacts에 차원 없는 차입금 태그 없음) → 원문에서 꺼내 DEBT_TOTAL_TAG로 합산.
         # 모회사 보증 차입은 공정가치 주석의 장부가 총액(aes:RecourseDebtTotal — 1년 안 몫 포함)을 쓴다: 재무상태표 1년 안 recourse 줄이 Q3 2026에 "—"라
         # 차원 값이 없어(dim_fact_feed는 최신 공시에 없으면 멈춘다) — 2025-12 879 + 5,105 = 5,984로 맞는다.
         'dim_facts': [('aes:RecourseDebtTotal', 'us-gaap:FairValueByMeasurementBasisAxis', 'us-gaap:CarryingReportedAmountFairValueDisclosureMember', 'RecourseDebtTotalAes'),
                       ('us-gaap:ShortTermBorrowings', 'us-gaap:RecourseStatusAxis', 'us-gaap:NonrecourseMember', 'ShortTermBorrowingsNonrecourseAes'),
                       ('us-gaap:LongTermDebt', 'us-gaap:RecourseStatusAxis', 'us-gaap:NonrecourseMember', 'LongTermDebtNonrecourseAes')],
         # 옛 공시(2021-12·2023-03·06 등)는 비소구 차입을 차원 없는 회사 고유 태그로 냈다 — 없으면 그 분기 차입금이 모회사 몫만 남았다(Codex r1). DEBT_TOTAL_TAG 튜플이 날짜마다 차원 값 우선.
         'company_tags': [('aes:NonRecourseDebtCurrent', 'NonRecourseDebtCurrentAes', '2019-01-01'), ('aes:NonRecourseDebtNonCurrent', 'NonRecourseDebtNonCurrentAes', '2019-01-01')]}
# AES v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 12월 31일. 발전(재생에너지·가스·석탄, 미주 중심) + 미국 규제 송배전(AES Indiana·AES Ohio).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-11-03 16:09 동부 장 마감 뒤 → 첫 세션 11-04, 카드 기준일 11-06 종가), 인수 합의 보도자료(8-K 2026-03-02 07:07 장 전),
#        주주총회 승인(8-K 2026-06-26 장 마감 뒤), EU·뉴욕 승인(8-K 2026-10-19 장 마감 뒤), EU 외국보조금 심사 종결(8-K 2026-10-28 장 마감 뒤).
#        인수 합의 뒤 분기 실적 보도자료(8-K 2.02항)를 내지 않는다 — 손 뉴스의 분기 숫자는 10-Q.
# 미완성 사유: 2026-03-01 GIP(BlackRock 소속)·EQT Infrastructure VI 컨소시엄(CalPERS·QIA 공동 인수)이 주당 $15.00 현금으로 인수 합의(지분 가치 약 $10.7B, 기업가치 약 $33.4B).
#   주가가 인수가에 묶여(11-06 $14.87) 배수·현금흐름 판정이 의미 없다(보류 C군 사유). 주주 승인 2026-06-26, HSR 만료 06-22, EU 합병 승인 10-15, 뉴욕 PSC 10-19, EU 외국보조금 10-28.
#   PUCO 09-17 승인(OCC 재심 신청, AES Ohio 10-29 답변, 승인 유효). 남은 것은 다른 규제 승인과 통상 종결 조건 — 회사 예상 2026년 말 또는 2027년 초 종결. 해지 수수료: 인수자 → AES $100M 또는 약 $588M, AES → 인수자 약 $321M.
# 엔진 입력(2026-11-07): 합성 영업이익 = "Operating margin"(GrossProfit) − 일반관리비(DERIVED_OPINC — 영업이익 줄 없음, Q3 2026 982 − 68 = 914, 회사 보고 지표 아님). 자산 손상($91M)·사업 매각 손익·환차손은 합성 값에서 뺐다.
#   차입금 $33,264M = 모회사 보증 6,361 + 비소구 1년 안 2,950 + 비소구 장기 23,953(대부분 프로젝트 자회사 차입, 모회사 보증 없음). 비지배 $5,071M + 상환가능 자회사 주식 $3,100M.
# EPS: 2025년에 중단사업(손실)이 있어 Q3 2025 희석 EPS 0.89(계속사업 0.94). 일회성(E54) — 자산 손상·사업 매각 이익(2026 9개월 $212M)·채무 상환 손실 등이 분기마다 있어 GAAP 그대로(판정 보류라 판정 영향 없음).
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, 1, 0), '판정 보류'
CO = 'AES'
S_ = 'https://www.sec.gov/Archives/edgar/data/874761/'
SEC = S_
TENQ = S_ + '000087476126000156/aes-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000087476126000156/aes-20260930.htm', 'deal': S_ + '000119312526084157/d100078dex991.htm',
      'vote': S_ + '000114036126026562/ef20076870_ex99-1.htm', 'eu': S_ + '000114036126040117/ef20083812_8k.htm',
      'fsr': S_ + '000114036126041045/ef20084505_8k.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="aesFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(GIP·EQT 인수 종결 대기 — 주가가 인수가 $15에 묶여 있다)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 40)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('미완성 카드다. 2026년 3월 GIP(BlackRock 소속)·EQT가 이끄는 컨소시엄이 AES를 주당 $15.00 현금에 인수하기로 합의했다(지분 가치 약 $10.7B, 기업가치 약 $33.4B — 회사 계산은 2025년 말 지분 비례 순차입금 $22.7B + 7.12억 주 × $15로, 연결 차입금 기준이 아니다). 주가가 인수가 근처에 묶여 배수·현금흐름으로 낸 판정이 의미 없으므로 판정을 보류한다 — 자기 이력·동종업 점수는 참고값이다. '
              '주주는 2026년 6월 승인했고 미국 독점 심사 대기기간 만료, 오하이오 규제위원회(PUCO) 승인(9월 — 소비자 대변 기관이 재심을 신청했지만 승인은 유효), EU 합병·외국보조금 심사, 뉴욕 규제위원회 판단까지 받았다. 남은 규제 승인과 종결 조건이 채워지면 2026년 말 또는 2027년 초 종결될 예정이다. '
              '회사는 인수가 없으면 2027년 뒤 성장 투자 자금을 마련하려고 배당 축소·폐지나 대규모 신주 발행이 필요할 가능성이 높다고 설명했다. 차입금 약 $33B 가운데 약 $27B는 발전소·송배전 자회사가 진 비소구 차입(모회사가 보증하지 않음)이다. '
              '이번 분기 숫자는 실적 보도자료가 없어 10-Q에서 가져왔다. 영업이익 줄이 없어 "Operating margin − 일반관리비"로 만든 합성 값을 쓴다(자산 손상·사업 매각 손익·환차손은 합성 값에서 뺀다).')
PH = ['NEE', 'CEG', 'DUK', 'SO', 'AEP', 'EXC']
PEER_FILE = 'peer_universe/utilities.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '유틸리티 6곳 PER 비교 (점수는 S&P500 유틸리티 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 유틸리티 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 유틸리티 대비 배수 순위 (v2/peer_universe/utilities.json)'
PEER_TIP = ('S&P500 유틸리티(AES 제외)와 배수 순위를 매긴 값이다.',
            '규제 전력·가스, 독립 발전사, 수도가 섞여 있다. 차트에는 유틸리티 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문): 재생에너지 1,104 + 유틸리티 1,256 + 에너지 인프라 1,536 + 신에너지 기술 1 − 본사·상계 25 = 3,872.
SEG = [('에너지 인프라(가스·석탄 발전 등)', 1536.0, '#00a1de'), ('유틸리티(인디애나·오하이오 송배전)', 1256.0, '#7fc241'), ('재생에너지', 1104.0, '#c3e3f5')]
SEG_ADJ = -24
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 인수 진행 4건 + Q3 2026 10-Q(실적 보도자료 없음). 반응일: 장 마감 뒤 → 다음 거래일, 장 전 → 같은 날.
NEWS_RANGE = '2026.03 ~ 2026.11'
NEWS = [
    ('neutral', '2026년 11월 3일 장 마감 뒤 — Q3 2026 10-Q(실적 보도자료 없음)', '2026-11-04',
     '매출 $3.87B(+15.5%) · AES 귀속 순이익 $553M · 희석 EPS $0.76(1년 전 $0.89, 계속사업 기준 $0.94) — 다음 날 주가 −0.1%', 'q3', 'AES 분기 보고서 (SEC 10-Q)'),
    ('neutral', '2026년 10월 28일 장 마감 뒤 — EU 외국보조금 예비 심사 종결', '2026-10-29',
     '인수 종결 조건 하나 충족 · 남은 규제 승인·통상 조건 대기 — 다음 날 주가 +0.5%', 'fsr', 'AES 공시 (SEC 8-K)'),
    ('neutral', '2026년 10월 19일 장 마감 뒤 — EU 합병 승인·뉴욕 규제위원회 추가 심사 불필요', '2026-10-20',
     'EU 집행위원회 조건 없는 승인(10-15) · 뉴욕 PSC 추가 심사 불필요 판단(10-19) — 다음 날 주가 +0.1%', 'eu', 'AES 공시 (SEC 8-K)'),
    ('neutral', '2026년 6월 26일 장 마감 뒤 — 주주총회 인수 승인', '2026-06-29',
     '주주 승인 · 미국 독점 심사(HSR) 대기기간 6월 22일 만료(같은 8-K 본문) · 2026년 말~2027년 초 종결 예상 — 다음 거래일 주가 −0.3%', 'vote', 'AES 보도자료 (SEC 8-K)'),
    ('red', '2026년 3월 2일 장 전 — GIP·EQT 컨소시엄 인수 합의(주당 $15 현금)', '2026-03-02',
     '지분 가치 약 $10.7B · 첫 인수설 보도(2025-07-08) 전 30일 거래량가중평균가 대비 40.3% 프리미엄 · 2026년 말~2027년 초 종결 예상 — 발표 직전 종가 $17.28에서 당일 $14.21(−17.8%)', 'deal', 'AES 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 9, 'nt': 1, 'mean': 15, 'median': 15, 'low': 15, 'high': 15, 'sb': 0, 'b': 0, 'h': 9, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-07'


# 미완성 카드 표시(2026-11-03 사용자 결정, NSC·PTC 방식 — 인수 대상).
INCOMPLETE_SHORT = 'GIP·EQT 인수 종결 대기'
INCOMPLETE_WHY = '2026년 3월 GIP·EQT 컨소시엄이 주당 $15.00 현금에 인수하기로 합의했다(2026년 말~2027년 초 종결 예상) — 주가가 인수가에 묶여 배수·현금흐름 판정이 의미 없고, 종결되면 상장 폐지된다. 종결 또는 무산 뒤 다시 본다'
POST = [r"""
import re as _re0
_w = '2026년 3월 GIP·EQT 컨소시엄이 주당 $15.00 현금에 인수하기로 합의했다(2026년 말~2027년 초 종결 예상) — 주가가 인수가에 묶여 배수·현금흐름 판정이 의미 없고, 종결되면 상장 폐지된다. 종결 또는 무산 뒤 다시 본다'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — GIP·EQT 인수 종결 대기</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — GIP·EQT 인수 종결 대기. 주가가 인수가 $15에 묶여 현금흐름 내재가치를 계산하지 않았다.')
h = _re0.sub(r'(id="aesFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)
h = _re0.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re0.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")
h = _re0.sub(r'(<div class="verdict-summary-head">[^<]*)<span class="tag">[^<]*</span>', r'\1<span class="tag">GIP·EQT 인수 종결 대기</span>', h, count=1)
h = _re0.sub(r'<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
h = h.replace('합성 영업이익률(세전이익 기준)', '합성 영업이익률(Operating margin − 일반관리비)').replace('합성 영업이익(세전이익 기준)', '합성 영업이익(Operating margin − 일반관리비)')   # DERIVED_OPINC 기본 문구는 세전 기준 회사용(Codex r1)
h = _re0.sub(r'(<div class="verdict-summary-head">[^<]*?), 영업이익률 ', r'\1, 합성 영업이익률 ', h, count=1)   # 영업이익 줄 없음 — Operating margin − 일반관리비(Codex r2)
h = h.replace("label:'OPM(%)'", "label:'합성 OPM(%)'", 1)
h = _re0.sub(r'<div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
"""]


# ── 자동 카드 — 부문 지도(손 작성). 원문 대조: Q3 2026 10-Q 재생에너지 1,104 + 유틸리티 1,256 + 에너지 인프라 1,536 + 신에너지 1 − 본사·상계 25 = 3,872(2026-11-07) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"aes:EnergyInfrastructureMember": ["에너지 인프라(가스·석탄 발전 등)", "#00a1de"], "aes:UtilitiesMember": ["유틸리티(인디애나·오하이오 송배전)", "#7fc241"],
             "aes:RenewablesMember": ["재생에너지", "#c3e3f5"]},
 "ignore": ["aes:CorporateOtherAndOtherMember"],   # 부문 이익 표의 본사·기타 줄(29) — 매출 대조 표의 본사·상계 줄(−25)과 같은 축·같은 결산일에 같이 실린다
 "adjust": ["aes:NewEnergyTechnologiesMember", "aes:CorporateOtherAndOtherEliminationsMember"]
}
SEG_ADJ_LABEL = '신에너지 기술·본사·상계'
