CIK = '0000010456'
BUILD = {'no_dcf': '미완성 — Q4 2025 손상으로 GAAP 적자', 'company_tags': [('bax:LongTermDebtAndLeaseObligationExcludingCurrentMaturities', 'LongTermDebtAndCapitalLeaseObligations', '2026-01-01')]}   # 2026-11-07 사용자 결정(일회성 30% 이상 → 미완성). 장기 차입금이 2026년부터 회사 고유 태그
# BAX(백스터 인터내셔널) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 12월 31일. 의료 제품·치료(수액·주사제·수술용품), 헬스케어 시스템·기술(병상·환자 감시·진단).
# 2025년 1월 신장 치료 사업(Vantive)을 Carlyle에 팔아 중단사업 — 숫자는 계속사업 기준.
# 출처: SEC XBRL(+ 회사 고유 태그 장기 차입금), Q3 2026 10-Q(2026-10-29 16:31 동부 장 마감 뒤 → 첫 세션 10-30, 카드 기준일 11-06 종가), 실적 보도자료(8-K 2.02항 — 모두 장 전 07:1x 동부 → 그날).
# 엔진 입력(2026-11-07): 차입금 = 1년 안 $844M + 장기 $7,757M(bax:LongTermDebtAndLeaseObligationExcludingCurrentMaturities — 2026년부터 회사 고유 태그, BUILD company_tags) = $8,601M,
#   설비투자 PaymentsToAcquireOtherProductiveAssets(2026년부터), 단기투자는 2016년 낡은 값이라 뺐다. 비지배지분 −$27M.
# 일회성(2026-11-07 기준 — 30% 이상이라 미완성): 최근 4분기 계속사업 GAAP 희석 EPS −1.21(−2.01 − 0.03 + 0.26 + 0.57) — Q4 2025 Front Line Care 영업권 손상 $485M·
#   미국 이연법인세 자산 평가충당금 $330M. Q3 2026에는 반대로 채무 조기상환 이익 $253M(세전). 손상은 2026년 10-K(2027-02) 뒤 최근 4분기에서 빠진다.
NI_TAGS = ['IncomeLossFromContinuingOperations', 'NetIncomeLoss']   # 순이익은 계속사업 기준(뉴스·보도자료와 같게 — Codex r1)
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, 0), '판정 보류'
CO = 'Baxter International'
S_ = 'https://www.sec.gov/Archives/edgar/data/10456/'
SEC = S_
TENQ = S_ + '000162828026068278/bax-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000001045626000004/bax-20260930xex991.htm', 'q2': S_ + '000162828026050795/bax-20260630xex991.htm',
      'q1': S_ + '000162828026028582/bax-20260331xex991.htm', 'q4': S_ + '000162828026007474/bax-20260212xex991.htm',
      'cfo': S_ + '000119312526356188/d154782dex991.htm', 'cfo0': S_ + '000119312526107345/d114675dex991.htm',
      'tender': S_ + '000162828026057739/bax-20260818exhibit991.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="baxFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(2025년 4분기 손상·세금 비용으로 최근 4분기 GAAP 이익이 적자다)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (-40, 30)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('미완성 카드다. 최근 4분기 계속사업 GAAP 희석 EPS가 약 −$1.21로 적자다 — 2025년 4분기에 환자 감시·진단 사업(Front Line Care) 영업권 손상 $485M과 미국 이연법인세 자산 평가충당금 $330M을 잡아 그 분기 계속사업 EPS가 −$2.01이었기 때문이다(세금 항목 등 다른 특별항목도 있다). '
              '적자라 PER은 점수에서 빠지고, 손상이 영업이익에 들어가 EBITDA가 낮게 잡혀 EV/EBITDA도 높게 나온다. 반대로 2026년 3분기에는 현금 $600M으로 액면 $864M의 채권을 사들여 소각하며 생긴 채무 조기상환 이익 $253M(세전, 세후 약 $195M)이 이익을 높였다. '
              '2025년 1월 신장 치료 사업(Vantive)을 팔아 그 사업은 중단사업으로 빠져 있고, "기타" 매출은 Vantive에 대한 공급 계약 매출이다. 회사는 2026년 조정 EPS 전망을 처음 $1.85~2.05에서 두 번 올려 $2.05~2.15로 잡았다. 2026년 2월 분기 배당을 주당 $0.17에서 $0.01로 줄였다. 수액 펌프 Novum IQ는 2025년 시정조치가 FDA 최고 위험 등급(Class I) 리콜로 분류돼 2025년 7월부터 미국·캐나다 출하·설치를 멈췄고(의학적 필요 예외), 2026년 9월에는 일리노이 Round Lake 무균 주사제 공장이 FDA 경고서한을 받아 10월 회신했다. '
              '자기 이력·동종업 점수는 참고값이고 판정은 보류한다. 손상 분기가 최근 4분기에서 빠지는 2026년 10-K(2027년 2월) 뒤, 남은 일회성(채무 조기상환 이익 등)이 30% 기준에 걸리는지 보고 정식 판정을 다시 정한다.')
PH = ['BDX', 'BSX', 'MDT', 'ABT', 'SYK', 'ZBH']
PEER_FILE = 'peer_universe/health_care.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '의료기기 6곳 PER 비교 (점수는 S&P500 헬스케어 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 헬스케어 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 헬스케어 대비 배수 순위 (v2/peer_universe/health_care.json)'
PEER_TIP = ('S&P500 헬스케어(BAX 제외)와 배수 순위를 매긴 값이다.',
            '제약·바이오·보험이 섞여 있다. 차트에는 의료기기 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문 표 — 2026년 2분기부터 의약품 부문이 의료 제품·치료로 합쳐져 1년 전 값은 재분류 기준): 의료 제품·치료 2,102 + 헬스케어 시스템·기술 806 + 기타(Vantive 공급 계약 등) 68 = 2,976.
SEG = [('의료 제품·치료(수액·주사제·수술)', 2102.0, '#1d4f91'), ('헬스케어 시스템·기술(병상·환자 감시)', 806.0, '#00a9e0')]
SEG_ADJ = 68
SEG_ADJ_LABEL = '기타(Vantive 공급 계약 등)'
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 실적 4건 + CFO 교체 2건 + 채권 공개매수(7건). 반응일: 실적 8-K 장 전 07:1x 동부 → 그날.
NEWS_RANGE = '2026.02 ~ 2026.10'
NEWS = [
    ('neutral', '2026년 10월 29일 장 전 — Q3 2026 실적', '2026-10-29',
     '매출 $2.98B(+5%) · 계속사업 순이익 $298M · 희석 EPS $0.57(채무 조기상환 이익 $253M 세전 포함) · 조정 EPS $0.58(높은 세율 탓에 −16%) · 2026년 매출·조정 EPS 전망 상향($2.05~2.15) — 그날 주가 −7.7%', 'q3', 'Baxter 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 8월 19일 장 전 — 새 CFO 선임', '2026-08-19',
     'John Rogers를 10월 1일부터 CFO로 — 그날 주가 +2.7%', 'cfo', 'Baxter 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 8월 18일 장 마감 뒤 — 채권 공개매수 한도 확대', '2026-08-19',
     '현금 매입 한도를 $500M에서 $600M으로 늘림(최종 액면 $864M 소각, 3분기 이익 $253M) — 다음 날 주가 +2.7%(같은 날 새 CFO 선임 발표)', 'tender', 'Baxter 보도자료 (SEC 8-K)'),
    ('green', '2026년 7월 30일 장 전 — Q2 2026 실적', '2026-07-30',
     '매출 $2.96B(+5%) · 순이익 $135M · 희석 EPS $0.26 · 조정 EPS $0.56(관세 환급 주당 $0.11 포함) · 연간 조정 EPS 전망 $1.95~2.15로 상향 — 회사 예상을 웃돎 — 그날 주가 +8.0%', 'q2', 'Baxter 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 30일 장 전 — Q1 2026 실적', '2026-04-30',
     '매출 $2.7B(+3%, 유기 성장 −1%) · 순손실 $17M · 희석 EPS −$0.03 · 조정 EPS $0.36(−35%) — 그날 주가 +4.0%', 'q1', 'Baxter 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 3월 16일 장 전 — CFO 사임', '2026-03-16',
     'CFO Joel Grade가 가족 사정으로 사임, Anita Zielinski 임시 CFO — 그날 주가 −1.8%', 'cfo0', 'Baxter 보도자료 (SEC 8-K)'),
    ('red', '2026년 2월 12일 장 전 — Q4 2025 실적', '2026-02-12',
     '매출 $2.97B(+8%) · 계속사업 순손실 $1,035M · 계속사업 희석 EPS −$2.01(Front Line Care 영업권 손상 $485M·이연법인세 평가충당금 $330M 포함) · 회사 예상에 못 미침 · 2026년 조정 EPS 첫 전망 $1.85~2.05 · 분기 배당 $0.17 → $0.01로 삭감 — 그날 주가 −16.0%', 'q4', 'Baxter 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 15, 'nt': 12, 'mean': 25.08, 'median': 25, 'low': 20, 'high': 29, 'sb': 1, 'b': 1, 'h': 12, 's': 1, 'ss': 0}
ANALYST_ASOF = '2026-11-07'

# 미완성 카드 표시(2026-11-07 사용자 결정 — 일회성 30% 이상).
INCOMPLETE_SHORT = '손상으로 GAAP 적자'
INCOMPLETE_WHY = '2025년 4분기 영업권 손상 $485M·이연법인세 평가충당금 $330M으로 최근 4분기 GAAP 이익이 적자다 — 배수 판정이 왜곡돼 보류한다. 손상 분기가 빠지는 2026년 10-K(2027년 2월) 뒤 다시 본다'
POST = [r"""
import re as _re0
_w = '2025년 4분기 영업권 손상 $485M·이연법인세 평가충당금 $330M으로 최근 4분기 GAAP 이익이 적자다 — 배수 판정이 왜곡돼 보류한다. 손상 분기가 빠지는 2026년 10-K(2027년 2월) 뒤 다시 본다'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — 손상으로 GAAP 적자</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — 손상으로 GAAP 적자. 최근 4분기 이익이 일회성 비용으로 적자라 현금흐름 내재가치를 계산하지 않았다.')
h = _re0.sub(r'(id="baxFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)
h = _re0.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re0.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")
h = _re0.sub(r'(<div class="verdict-summary-head">[^<]*)<span class="tag">[^<]*</span>', r'\1<span class="tag">손상으로 GAAP 적자</span>', h, count=1)
h = _re0.sub(r'<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
h = _re0.sub(r'<div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
"""]


# ── 자동 카드 — 부문 지도(seg_map_propose 1/2 + 의료 제품·치료 손 확인). 원문 대조: Q3 2026 10-Q 부문 표 2,102 + 806 + 기타 68 = 2,976(2026-11-07) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"bax:MedicalProductsAndTherapiesMember": ["의료 제품·치료(수액·주사제·수술)", "#1d4f91"],
             "bax:HealthcareSystemsAndTechnologiesMember": ["헬스케어 시스템·기술(병상·환자 감시)", "#00a9e0"]},
 "ignore": []
}
