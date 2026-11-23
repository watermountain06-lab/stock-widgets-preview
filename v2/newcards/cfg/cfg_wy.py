CIK = '0000106535'
BUILD = {'eps_tag': 'EarningsPerShareBasicAndDiluted,EarningsPerShareDiluted', 'no_dcf': '미완성 — 최근 4분기 순이익의 약 64%가 특별 항목(산림 매각 이익 등)', 'company_tags': [('wy:PaymentsForCapitalExpendituresOfPropertyPlantAndEquipment', 'CapexPpeWy', '2019-01-01')]}
# WY(웨어하우저) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 12월 31일. 리츠(REIT) — 산림(원목 판매)·토지 솔루션(부동산·에너지·탄소)·목재 제품(제재목·OSB·엔지니어드 목재).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-30 접수, 카드 기준일 11-20 종가), 실적 보도자료(8-K 2.02항 — 모두 장 마감 뒤 → 다음 세션).
# 엔진 입력(2026-11-22): 영업이익 = 보고 영업이익 − 산림 매각 이익(DERIVED_OPINC), 설비투자 = 설비(회사 고유 태그, 9개월 $350M) + 조림(9개월 $38M) — 산림 인수 제외,
#   차입금 $5,354M(장기채 + CP), 4분기 EPS 2025·2024는 보도자료 값(0.10·0.11). EPS 태그는 2022년 1분기까지 EarningsPerShareBasicAndDiluted(BUILD eps_tag — 희석 태그만 쓰면 2018~2021년 3분기가 비고 2022년 1분기 공시일이 1년 늦다, Codex r1).
# 일회성(E54): 최근 4분기 순이익 $453M(4분기 $74M + 1~9월 $379M), 특별 항목 제외 $162M(−67 + 77 + 91 + 61) → 세후 특별 이익 $291M = 약 64% → 미완성.
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, 0), '판정 보류'
CO = 'Weyerhaeuser'
S_ = 'https://www.sec.gov/Archives/edgar/data/106535/'
SEC = S_
TENQ = S_ + '000119312526441693/wy-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000119312526437799/wy-ex99_1.htm', 'q2': S_ + '000119312526326124/wy-ex99_1.htm',
      'q1': S_ + '000119312526197281/wy-ex99_1.htm', 'q4': S_ + '000119312526029351/wy-ex99_1.htm',
      'q3old': S_ + '000119312525258510/wy-ex99_1.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="wyFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(최근 4분기 순이익의 약 64%가 산림 매각 이익 등 특별 항목이다)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (미완성 — 현금흐름 보류)</span>'
Y2 = (-5, 30)
ACT_REASON = '리츠라 재고·매출채권 회전으로 보는 활동성이 잘 맞지 않는다'
NONOP_WHAT = '투자'
CAPEX_LABEL = '설비투자(설비·조림)'   # 산림 인수는 넣지 않는다
MODEL_NOTE = ('미완성 카드다. 최근 4분기 순이익 $453M(EPS $0.63)의 약 64%가 회사가 특별 항목으로 빼는 일회성 이익이다 — 2025년 4분기 조지아·앨라배마·오리건 산림 매각 이익 $266M(세후 연금 정산 손실 $111M·환경 복구 비용 $14M과 상계해 세후 $141M), 2026년 1분기 버지니아 산림 매각 이익 $58M과 보험 회수 $21M, 2분기 오리건 산림 매각 이익 $71M이다. 특별 항목을 빼면 최근 4분기 순이익은 $162M(2025년 4분기는 −$67M 손실), EPS 약 $0.22로 PER이 약 87배가 돼 카드의 PER 순위가 맞지 않는다 — 그래서 판정을 보류한다. '
              '웨어하우저는 산림을 사고팔며 포트폴리오를 바꾸는 중이다(2025년 3분기 산림 약 $0.46B 인수 뒤, 2025년 4분기 오리건·조지아·앨라배마 약 $0.41B와 2026년 1~9월 $306M을 팔았고 4분기 아칸소 매각이 남아 있다). 실적은 제재목·OSB 가격에 크게 흔들린다 — 목재 제품이 매출의 약 4분의 3이다. 영업이익은 회사 보고 영업이익에서 산림 매각 이익을 뺀 값이다(제재소 매각 이익·보험 회수·환경 복구 비용·소송 비용 등은 회사 배치대로 남는다). '
              '리츠는 업계가 보완 지표로 FFO나 조정 EBITDA를 쓴다 — 웨어하우저는 조정 EBITDA(2025년 $1.0B)와 조정 FAD를 쓴다. 사이트에는 리츠 전용 평가가 아직 없다.')
HEALTH_EXTRA = '산림을 담보 없이 채권으로 조달해 보유하는 리츠라 차입금이 이익보다 크게 나온다 — 리츠는 보통 부채를 자산 가치나 EBITDA 대비로 본다.'
PH = ['PLD', 'O', 'SPG', 'PSA', 'KIM', 'DOC']
PEER_FILE = 'peer_universe/real_estate.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '리츠 6곳 PER 비교 (점수는 S&P500 부동산 기준)', 'pbr': '리츠 PBR 비교', 'psr': '리츠 PSR 비교',
                'pcr': '리츠 PCR(FCF) 비교', 'evebitda': '리츠 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 부동산 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 부동산 대비 배수 순위 (v2/peer_universe/real_estate.json)'
PEER_TIP = ('S&P500 부동산(WY 제외)과 배수 순위를 매긴 값이다.',
            '물류·데이터센터·의료·쇼핑몰·주택 리츠와 부동산 서비스가 섞여 있다. 산림 리츠는 S&P500에 웨어하우저뿐이라 차트에는 다른 리츠 6곳이 보인다. 매출의 약 4분의 3이 목재 제품 제조라 PSR·PBR은 임대 리츠보다 낮게 나온다.')
SEG = [('목재 제품', 1385, '#1d5c3a'), ('산림(원목 판매)', 378, '#5e9a6e'), ('토지 솔루션(부동산·에너지·탄소)', 99, '#b9d8bf')]
SEG_ADJ = 0
SEG_TITLE = '부문별 외부 매출'
NEWS_RANGE = '2025.10 ~ 2026.11'
NEWS = [
    ('green', '2026년 10월 29일 장 마감 뒤 — Q3 2026 실적', '2026-10-30',
     '희석 EPS $0.08(특별 항목 없음) · 조정 EBITDA $248M(1년 전보다 14% 증가) · 4분기 아칸소 산림 매각 마감 예정 — 다음 날 주가 +3.0%', 'q3', 'Weyerhaeuser 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 7월 30일 장 마감 뒤 — Q2 2026 실적', '2026-07-31',
     '희석 EPS $0.23(오리건 산림 매각 이익 $71M 포함, 제외 시 $0.13) · 조정 EBITDA $310M — 다음 날 주가 +6.5%', 'q2', 'Weyerhaeuser 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 4월 30일 장 마감 뒤 — Q1 2026 실적', '2026-05-01',
     '희석 EPS $0.22(버지니아 산림 매각 이익·보험 회수 포함, 제외 시 $0.11) · 조정 EBITDA $308M — 다음 날 주가 −2.2%', 'q1', 'Weyerhaeuser 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 1월 29일 장 마감 뒤 — 2025년 연간 실적', '2026-01-30',
     '4분기 희석 EPS $0.10(산림 매각 이익·연금 정산 손실 등 특별 항목을 빼면 −$0.09 손실) · 2025년 조정 EBITDA $1.0B · 주주 환원 $766M(자사주 $160M 포함) — 다음 날 주가 −0.6%', 'q4', 'Weyerhaeuser 실적 보도자료 (SEC 8-K)'),
    ('red', '2025년 10월 30일 장 마감 뒤 — Q3 2025 실적', '2025-10-31',
     '희석 EPS $0.11(특별 이익 포함, 제외 시 $0.06) · 조정 EBITDA $217M · 프린스턴 제재소 $85M에 매각 — 다음 날 주가 −2.2%', 'q3old', 'Weyerhaeuser 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 12, 'nt': 10, 'mean': 27.2, 'median': 27, 'low': 23, 'high': 34, 'sb': 8, 'b': 2, 'h': 2, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-23'

INCOMPLETE_SHORT = '산림 매각 등 특별 이익이 큼'
INCOMPLETE_WHY = '최근 4분기 순이익 $453M(EPS 0.10+0.22+0.23+0.08 = $0.63)의 약 64%가 특별 항목이다 — 세후 특별 이익이 2025년 4분기 $141M(조지아·앨라배마·오리건 산림 매각 이익 $266M에서 세후 연금 정산 손실 $111M과 환경 복구 비용 $14M을 뺀 값), 2026년 1분기 $79M(버지니아 산림 매각 이익 $58M, 제품 하자 보험 회수 $21M), 2분기 $71M(오리건 산림 매각 이익)으로 합 $291M(약 64%)이다. 특별 항목을 빼면 최근 4분기 순이익은 $162M뿐이라 배수 판정이 왜곡돼 보류한다. 2025년 4분기가 빠지는 2026년 4분기 실적 뒤부터 분기마다 다시 본다(4분기에는 아칸소 산림 매각이 마감될 예정이다)'
POST = [r"""
import re as _re0
_w = '최근 4분기 순이익 $453M(EPS 0.10+0.22+0.23+0.08 = $0.63)의 약 64%가 특별 항목이다 — 세후 특별 이익이 2025년 4분기 $141M(조지아·앨라배마·오리건 산림 매각 이익 $266M에서 세후 연금 정산 손실 $111M과 환경 복구 비용 $14M을 뺀 값), 2026년 1분기 $79M(버지니아 산림 매각 이익 $58M, 제품 하자 보험 회수 $21M), 2분기 $71M(오리건 산림 매각 이익)으로 합 $291M(약 64%)이다. 특별 항목을 빼면 최근 4분기 순이익은 $162M뿐이라 배수 판정이 왜곡돼 보류한다. 2025년 4분기가 빠지는 2026년 4분기 실적 뒤부터 분기마다 다시 본다(4분기에는 아칸소 산림 매각이 마감될 예정이다)'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — 산림 매각 등 특별 이익이 큼</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — 산림 매각 등 특별 이익이 큼. 미완성 카드 규칙에 따라 종합 판정과 함께 현금흐름 내재가치도 보류했다.')
h = _re0.sub(r'(id="wyFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)
h = _re0.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re0.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")
h = _re0.sub(r'(<div class="verdict-summary-head">[^<]*)<span class="tag">[^<]*</span>', r'\1<span class="tag">산림 매각 등 특별 이익이 큼</span>', h, count=1)
h = _re0.sub(r'<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
h = _re0.sub(r'<div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
h = h.replace('합성 영업이익률(세전이익 기준)', '카드 기준 영업이익률(산림 매각 이익 제외)').replace('합성 영업이익(세전이익 기준)', '카드 기준 영업이익(산림 매각 이익 제외)')
h = h.replace('· GAAP 기준 · FCF는 영업현금흐름 − 설비투자(설비·조림) ·', '· 매출·순이익은 GAAP, 영업이익은 산림 매각 이익을 뺀 카드 계산값 · FCF는 영업현금흐름 − 설비투자(설비·조림) ·')
h = h.replace('영업이익률 5.4%(1년 전 7.2%)', '영업이익률 5.4%(1년 전 7.2%는 제재소 매각 이익 $29M·보험 회수 $26M 포함, 빼면 4.0%)')
h = h.replace('최근 4분기 FCF −$7M, 매출의 −0.1%.', '최근 4분기 FCF −$7M, 매출의 −0.1%(2025년 4분기 자발적 연금 출연 $200M과 Monticello 공장 투자 포함 — 회사 조정 FAD는 4분기 합 $351M).')
"""]

AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"wy:WoodProductsMember": ["목재 제품", "#1d5c3a"],
             "wy:TimberlandsMember": ["산림(원목 판매)", "#5e9a6e"],
             "wy:StrategicLandSolutionsMember": ["토지 솔루션(부동산·에너지·탄소)", "#b9d8bf"]},
 "ignore": []
}
