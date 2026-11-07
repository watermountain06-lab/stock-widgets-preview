CIK = '0000715957'
BUILD = {'no_dcf': '미완성 — NextEra 합병 종결 대기',   # 2026-11-03 사용자 결정(보류 C군 → 미완성 카드), 2026-11-07 제작
         'overlay': True,   # companyfacts가 Q2·Q3 2026 10-Q를 아직 싣지 않았다(2026-11-07 확인 — 최신 2026-03-31)
         # 설비투자를 Q3 2026 10-Q부터 회사 고유 태그로 낸다(9개월 $8,576M) — 그 전 공시는 PaymentsForProceedsFromProductiveAssets
         'company_tags': [('d:PaymentsToAcquirePropertyPlantAndEquipmentIncludingNuclearFuel', 'PaymentsForProceedsFromProductiveAssets', '2026-07-01')],
         # 자기 이력에서 PSR을 뺀다 — 2021·2022 4분기 매출이 재작성 값으로 섞여(3,061·3,810M 대 당시 역산 3,880·4,913M) 과거 PSR 분포를 못 믿는다.
         # 엔진 공통 과제로 고칠 때까지(동종업 PSR은 현재 TTM이라 그대로; Codex r2 → 2026-11-07 사용자 결정)
         'drop_self_multiples': ['psr']}
# D(도미니언 에너지) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 12월 31일.
# 사업: Dominion Energy Virginia(버지니아·노스캐롤라이나 규제 전력, CVOW 해상풍력 50%), Dominion Energy South Carolina(규제 전력·가스), Contracted Energy(Millstone 원전·재생천연가스 등).
# 출처: SEC XBRL(보충 자료 overlay), Q3 2026 10-Q(2026-10-30 11:38 동부 장중), 실적 보도자료(8-K 2.02항 — 모두 장 전 07:31 동부, 당일 반응),
#        NextEra 합병 계약 8-K(2026-05-18 08:08 장 전), 주주총회 결과 8-K(2026-09-03 16:18 장 마감 뒤), 버지니아 혜택안 8-K(2026-09-14 16:30 장 마감 뒤),
#        CVOW 공사 중지 명령 8-K(2025-12-22 20:46 — 명령은 그날 낮), CVOW 비용 갱신 8-K(2026-01-30 07:31 장 전).
# 미완성 사유: 2026-05-15 NextEra Energy와 전액 주식 합병 계약 — D 1주당 NEE 0.8138주 + 현금 합계 $3.6억 안분(주식·주식 보상 기준, 약 $0.41/주).
#   주가가 NEE 주가 × 합병 비율에 묶여(11-06 NEE $86.95 — NEE 카드 일봉 종가, × 0.8138 + 약 $0.41 ≈ $71.17, D $68.60 → 대가보다 3.6% 낮다) 배수 판정이 의미 없다. 종결되면 상장 폐지.
#   주주 승인 2026-09(양사), HSR 신고 2026-10, FERC·NRC·버지니아·노스캐롤라이나·사우스캐롤라이나 규제위원회 신청 2026-07. 회사 예상 2027년 하반기 종결(Q3 10-Q — 발표 때는 12~18개월),
#   계약 기한 2027-11(사유에 따라 2028-08까지 연장). 합병 계약상 분기 배당 $0.6675 초과는 NEE 동의 필요.
#   해지 수수료: D → NEE $2.24B, NEE → D $6.52B(비슷한 사유) 또는 $4.83B(규제 조건 미충족).
# 엔진 입력(2026-11-07): 매출 Revenues(손익계산서 총매출 — 고객 계약 매출 태그는 기타 매출 빠짐), 영업이익 OperatingIncomeLoss("Income from operations"),
#   이자비용 InterestAndDebtExpense, 설비투자 PaymentsForProceedsFromProductiveAssets(+ Q3 2026 회사 고유 태그).
#   차입금 $54,646M = 단기 3,308 + 1년 안 만기 2,399 + 장기 48,939(후순위채 7,461·증권화 채권 794 포함). 우선주 $991M, 비지배 $4,861M(대부분 CVOW 지분 50% Stonepeak).
# EPS: 4분기는 보도자료 값으로 덮는다(2024 $0.15 당시 공시값, 2025 $0.65 — Q4_EPS_OVERRIDE; 4분기 중단영업 2024 0·2025 −0.01은 Q4_OVERRIDE_BASIS). 일회성(E54) — Q2 2026 재생천연가스 설비 손상 등 — 판정 보류라 GAAP 그대로.
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, 0), '판정 보류'
CO = 'Dominion Energy'
S_ = 'https://www.sec.gov/Archives/edgar/data/715957/'
SEC = S_
TENQ = S_ + '000119312526440697/d-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000119312526439883/d-ex99.htm', 'q2': S_ + '000119312526326812/d-ex99.htm',
      'q1': S_ + '000119312526199099/d-ex99.htm', 'q4': S_ + '000119312526062432/d-ex99.htm',
      'q3y': S_ + '000119312525259408/d-ex99.htm', 'deal': S_ + '000119312526227930/d158175dex991.htm',
      'vote': S_ + '000119312526381919/d323818d8k.htm', 'va': S_ + '000119312526390654/d107020dex991.htm',
      'boem': S_ + '000119312525329224/d85059dex991.htm', 'cvow': S_ + '000119312526030493/d-20260130.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="dFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(NextEra 합병 종결 대기 — 주가가 NEE 주가 × 0.8138에 묶여 있다)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 40)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('미완성 카드다. 2026년 5월 NextEra Energy(NEE)와 전액 주식 합병 계약을 맺었다 — D 1주가 NEE 0.8138주와 현금(합계 $3.6억을 주식 수대로 나눈 약 $0.41)으로 바뀌고, 종결 뒤 D 주주는 합친 회사의 약 25.5%를 갖는다. '
              '주가가 NEE 주가 × 0.8138에 묶여 움직이므로 배수로 낸 판정이 의미 없어 판정을 보류한다(자기 이력·동종업 점수는 참고값). 합병 대가(NEE 주가 × 0.8138 + 약 $0.41)보다 조금 낮은 값에서 거래되는데, 그 차이는 종결 시점과 무산 위험에 대한 시장의 할인이다(카드 제작일 11월 6일 종가 기준 대가보다 약 3.6% 낮다). '
              '양사 주주는 2026년 9월 승인했고, 7월 연방 에너지 규제위원회(FERC)·원자력 규제위원회(NRC)·버지니아·노스캐롤라이나·사우스캐롤라이나 규제위원회에 승인을 신청했으며 10월 독점 심사(HSR)를 신고했다. 회사는 2027년 하반기 종결을 예상하고(Q3 10-Q — 발표 때는 12~18개월), 2027년 11월까지 끝나지 않으면 양쪽이 계약을 해지할 수 있다(사유에 따라 2028년 8월까지 연장). '
              '계약이 깨지면 사유에 따라 NEE가 D에 $6.52B 또는 $4.83B(규제 조건 미충족)를, D가 NEE에 $2.24B를 낸다. 종결 전 분기 배당을 $0.6675보다 올리려면 NEE 동의가 필요해 배당이 그대로다. '
              '버지니아 해상풍력 CVOW(2.6GW)는 2026년 7월 갱신에서 총사업비가 약 $11.7B(예비비 $0.1B 포함·금융비용 제외, 1월 $11.5B)로, 마지막 터빈 설치가 2027년 말로 늦춰졌다. 2026년 3월 첫 터빈이 가동했고 10월까지 176기 중 44기를 세웠다. 지분 50%를 Stonepeak이 가져 비지배지분($4.9B)의 대부분이다. '
              '2분기 순이익이 급감한 것은 재생천연가스 설비 손상($820M, 세전 — 세후 $640M) 등 일회성 비용 때문이다. 매출 증가(3분기 +24.1%)의 큰 몫은 연료비 상승을 요금으로 넘긴 연료 관련 매출(버지니아 +$348M)이라 이익 증가로 그대로 읽으면 안 된다. 기본적 분석의 영업이익 3년 연평균 45%도 2022년 자산 손상($1.4B)으로 기저가 낮아진 탓이다. 설비투자(2026년 9개월 $8.6B)가 영업현금흐름($4.7B)보다 커 FCF가 음수라 PCR은 계산하지 않는다. 자기 이력 점수에서는 PSR을 뺐다 — 2021·2022년 4분기 매출 이력에 오류가 있어 과거 PSR 분포를 믿기 어렵다(동종업 PSR은 최근 4분기 매출이라 그대로 쓴다).')
PH = ['NEE', 'DUK', 'SO', 'AEP', 'SRE', 'XEL']
PEER_FILE = 'peer_universe/utilities.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '유틸리티 6곳 PER 비교 (점수는 S&P500 유틸리티 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 유틸리티 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 유틸리티 대비 배수 순위 (v2/peer_universe/utilities.json)'
PEER_TIP = ('S&P500 유틸리티(D 제외)와 배수 순위를 매긴 값이다.',
            '규제 전력·가스, 독립 발전사, 수도가 섞여 있다. 차트에는 규제 전력·가스 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문): Virginia 4,218 + South Carolina 1,114 + Contracted Energy 337 − 본사·기타·부문 간 상계 52(본사·기타 335 − 상계 387) = 5,617.
SEG = [('Dominion Energy Virginia(버지니아·노스캐롤라이나 전력)', 4218.0, '#00a3e0'), ('Dominion Energy South Carolina(전력·가스)', 1114.0, '#7ab800'),
       ('Contracted Energy(Millstone 원전·재생천연가스 등)', 337.0, '#c6e6f5')]
SEG_ADJ = -52
SEG_ADJ_LABEL = '본사·기타·부문 간 상계'
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 합병 3건 + CVOW 2건 + 실적 5건(GAAP EPS, 보도자료 직접값). 반응일: 장 전 → 같은 날, 장 마감 뒤 → 다음 거래일.
NEWS_RANGE = '2025.10 ~ 2026.11'
NEWS = [
    ('green', '2026년 10월 30일 — Q3 2026 실적', '2026-10-30',
     '매출 $5.62B(+24.1%) · 순이익 $1.2B · EPS $1.30(1년 전 $1.16) · 영업 EPS(비GAAP) $1.28(1년 전 $1.06) · 2026 영업 EPS 전망($3.45~3.69) 상단 절반 예상 — 당일 주가 +2.3%', 'q3', 'Dominion Energy 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 9월 14일 장 마감 뒤 — 버지니아 혜택안 확대', '2026-09-15',
     'NEE와 공동 발표 · 가정용 요금 공제 2년 → 4년 · 저소득층 지원 $1억 추가 · 버지니아 일자리 1,000개 · 합병 비용 고객 부담 없음 — 다음 날 주가 −0.9%', 'va', 'NEE·Dominion 공동 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 9월 3일 장 마감 뒤 — 주주총회 합병 승인', '2026-09-04',
     '찬성 6억 7,132만 주 · 반대 857만 주 · 남은 조건은 규제 승인 — 다음 날 주가 −1.4%', 'vote', 'Dominion Energy 공시 (SEC 8-K)'),
    ('red', '2026년 7월 31일 — Q2 2026 실적', '2026-07-31',
     '매출 $4.48B(+17.6%) · 순이익 $340M · EPS $0.37(1년 전 $0.88 — 재생천연가스 설비 손상 $820M(세전) 등 일회성 비용) · 영업 EPS(비GAAP) $0.79(1년 전 $0.75) — 당일 주가 −0.8%', 'q2', 'Dominion Energy 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 5월 18일 장 전 — NextEra Energy와 합병 계약', '2026-05-18',
     '전액 주식 · D 1주당 NEE 0.8138주(+ 현금 합계 $3.6억 안분) · 종결 뒤 D 주주 약 25.5% · 발표 뒤 12~18개월 종결 예상 · 고객 요금 공제 $2.25B — 당일 주가 +9.4%', 'deal', 'NEE·Dominion 공동 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 5월 1일 — Q1 2026 실적', '2026-05-01',
     '매출 $5.02B(+23.1%) · 순이익 $621M · EPS $0.69(1년 전 $0.77) · 영업 EPS(비GAAP) $0.95(1년 전 $0.93) — 당일 주가 −0.9%', 'q1', 'Dominion Energy 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 23일 — Q4 2025 실적', '2026-02-23',
     '매출 $4.09B(+20.4%) · 순이익 $567M · EPS $0.65(1년 전 $0.14) · 2025년 연간 EPS $3.45(영업 EPS $3.42) · 2026 영업 EPS 전망 $3.45~3.69 · 2030년까지 연 5~7% 성장 전망 — 당일 주가 −2.6%', 'q4', 'Dominion Energy 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 1월 30일 장 전 — CVOW 비용·일정 갱신', '2026-01-30',
     '1월 16일 법원 가처분으로 공사 재개 · 공사 중지·관세 영향으로 총사업비 약 $11.2B → $11.5B · 완공 2027년 초로 — 당일 주가 −1.1%', 'cvow', 'Dominion Energy 공시 (SEC 8-K)'),
    ('red', '2025년 12월 22일 — 연방 정부 CVOW 공사 90일 중지 명령', '2025-12-22',
     '내무부 해양에너지관리국(BOEM) 명령 · 회사는 국가 안보·전력 수요를 들어 반박 — 당일 주가 −3.7%', 'boem', 'Dominion Energy 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 10월 31일 — Q3 2025 실적', '2025-10-31',
     '매출 $4.53B(+14.9%) · 순이익 $1.0B · EPS $1.16(1년 전 $1.09) · 영업 EPS(비GAAP) $1.06 · 2025 영업 EPS 전망 $3.33~3.48로 좁힘 — 당일 주가 −1.4%', 'q3y', 'Dominion Energy 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 16, 'nt': 10, 'mean': 71.3, 'median': 70, 'low': 62, 'high': 87, 'sb': 3, 'b': 1, 'h': 12, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-07'


# 미완성 카드 표시(2026-11-03 사용자 결정, AES·SRE 방식 — 합병 대상).
INCOMPLETE_SHORT = 'NextEra 합병 종결 대기'
INCOMPLETE_WHY = '2026년 5월 NextEra Energy와 전액 주식 합병 계약을 맺었다(D 1주당 NEE 0.8138주, 2027년 하반기 종결 예상) — 주가가 NEE 주가에 묶여 배수 판정이 의미 없고, 종결되면 상장 폐지된다. 종결 또는 무산 뒤 다시 본다'
POST = [r"""
import re as _re0
_w = '2026년 5월 NextEra Energy와 전액 주식 합병 계약을 맺었다(D 1주당 NEE 0.8138주, 2027년 하반기 종결 예상) — 주가가 NEE 주가에 묶여 배수 판정이 의미 없고, 종결되면 상장 폐지된다. 종결 또는 무산 뒤 다시 본다'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — NextEra 합병 종결 대기</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — NextEra 합병 종결 대기. 주가가 NEE 주가에 묶여 현금흐름 내재가치를 계산하지 않았다.')
h = _re0.sub(r'(id="dFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)
h = _re0.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re0.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")
h = _re0.sub(r'(<div class="verdict-summary-head">[^<]*)<span class="tag">[^<]*</span>', r'\1<span class="tag">NextEra 합병 종결 대기</span>', h, count=1)
h = _re0.sub(r'<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
h = _re0.sub(r'<div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
"""]


# ── 자동 카드 — 부문 지도(손 작성). 원문 대조: Q3 2026 10-Q Virginia 4,218 + South Carolina 1,114 + Contracted 337 − 본사·기타·상계 52 = 5,617(2026-11-07) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"d:DominionEnergyVirginiaMember": ["Dominion Energy Virginia(버지니아·노스캐롤라이나 전력)", "#00a3e0"],
             "d:DominionEnergySouthCarolinaMember": ["Dominion Energy South Carolina(전력·가스)", "#7ab800"],
             "d:ContractedEnergyMember": ["Contracted Energy(Millstone 원전·재생천연가스 등)", "#c6e6f5"]},
 "ignore": ["us-gaap:CorporateAndOtherMember"]   # 본사·기타 335는 대부분 부문 간 거래(상계 345) — 상계와 합친 −52를 SEG_ADJ로
}
