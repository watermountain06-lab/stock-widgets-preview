CIK = '0000916076'
BUILD = {'eps_tag': 'IncomeLossFromContinuingOperationsPerDilutedShare,EarningsPerShareDiluted',   # 계속사업 EPS — 2026-02 Quikrete 교환의 처분이익(세전 $1,962M)이 든 중단사업 순이익(9개월 $1,428M)이 희석 EPS에 든다(BALL·EMR 방식)
         'no_dcf': '미완성 — LNA 인수 손익 누적 대기'}   # 2026-11-07 사용자 결정 — 미완성 카드(판정 보류)
# MLM(마틴 마리에타 머티리얼즈) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 12월 31일. 골재(동부·서부 건자재 그룹) + 특수 소재(석회·마그네시아 — Lhoist North America 포함).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-11-04 16:30 동부 장 마감 뒤 접수 → 첫 세션 11-05, 카드 기준일 11-06 종가), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 모두 07:0x 동부 장 전 → 같은 날),
#        Quikrete 교환 완료 8-K(2026-02-23 장 마감 뒤), LNA 인수 완료 8-K(2026-08-24 장 전).
# 미완성 사유(2026-11-07 사용자 결정): 2026-08-21 Lhoist North America 인수(총 $12.9B — 현금 $7.0B 차입 조달 + 신주 10,953,543주) 뒤 재무상태표(차입 $12,823M, 자본 $17,659M,
#   투하자본 약 $30.6B)는 인수를 다 담았는데 최근 4분기 손익(매출 $7.2B)은 LNA 40일치만 담는다 — 현금흐름 모형이 매출/자본 0.1~0.24·투하자본 수익률 2~4%로 읽어 내재가치가 음수(기본 −$198),
#   PER 38.8배·PSR·PCR·EV/EBITDA 23.7배도 같은 이유로 부푼다(PBR만 양쪽이 맞음). 2027년 3분기 10-Q 뒤 재검토. 자기 이력·동종업 점수는 부푼 배수로 매긴 참고값(Fable r1).
#   10-Q 프로포마(LNA·Quikrete를 2025-01-01부터 가정): Q3 2026 매출 $2,649M(실적 $2,369M), 9개월 계속사업 순이익 $802M(실적 $592M).
# 2026-02-23 Quikrete 자산 교환(시멘트·레미콘 사업 → 골재 사업) 완료 — 중단사업 순이익 9개월 $1,428M(처분이익 세전 $1,962M 포함). 계속사업 EPS 최근 4분기 보도자료 합 3.85 + 1.31 + 4.26 + 3.94 = 13.36 —
#   엔진은 Q4 2025를 FY 16.34 − 1~3분기(1.70 + 4.84 + 5.97)로 역산해 3.83 → 13.34(PER은 둘 다 38.8배). 계속사업 EPS에는 인수·처분·통합 비용, 인수 재고 평가 상향분, 자산·포트폴리오 합리화 비용이 든다(합계 Q3 세후 $99M, 주당 $1.53, 보도자료 각주 5 — Codex r2).
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, -1, 0), '판정 보류'
CO = 'Martin Marietta'
S_ = 'https://www.sec.gov/Archives/edgar/data/916076/'
SEC = S_
TENQ = S_ + '000119312526447418/mlm-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000119312526446178/mlm-ex99_1.htm', 'q2': S_ + '000119312526324863/mlm-ex99_1.htm',
      'q1': S_ + '000119312526193931/mlm-ex99_1.htm', 'q4': S_ + '000119312526045530/mlm-ex99_1.htm',
      'lna': S_ + '000095015726000946/form8-k.htm', 'quikrete': S_ + '000095015726000175/form8-k.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="mlmFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(LNA 손익이 40일치만 들어 PER이 부풀려져 있다)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 50)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('미완성 카드다. 2026년 8월 21일 Lhoist North America(석회·석회석, 총 $12.9B — 현금 $7.0B는 차입, 나머지는 신주 약 1,095만 주) 인수로 차입금·투하자본·주식 수는 이미 크게 늘었는데, 최근 4분기 손익에는 인수한 회사가 40일치만 들어 있다(회사가 낸 프로포마로는 Q3 매출이 $2.65B로 실적 $2.37B보다 크다). '
              '그래서 현금흐름 모형이 이 회사를 투자 대비 이익이 아주 낮은 회사로 읽어 내재가치가 음수로 나오고, PBR을 뺀 PER·PSR·PCR·EV/EBITDA도 부풀려진다 — 자기 이력·동종업 점수는 이 배수로 매긴 참고값이다. 인수 손익이 최근 4분기에 다 들어가는 2027년 3분기 보고서 뒤에 다시 본다. '
              'PER은 계속사업 EPS로 쓴다 — 2026년 2월 Quikrete와 사업 교환(시멘트·레미콘을 넘기고 골재 사업을 받음)의 처분이익은 중단사업이라 빠진다. 계속사업 EPS에는 인수·처분·통합 비용, 인수 재고 평가 상향분, 자산 정리 비용(합계 Q3 주당 약 $1.53)이 그대로 들어 있다.')
PH = ['VMC', 'CRH', 'NUE', 'STLD', 'SHW', 'PPG']
PEER_FILE = 'peer_universe/materials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '건자재·소재 6곳 PER 비교 (점수는 S&P500 소재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 소재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 소재 대비 배수 순위 (v2/peer_universe/materials.json)'
PEER_TIP = ('S&P500 소재(MLM 제외)와 배수 순위를 매긴 값이다.',
            '화학·금속·건자재·포장재가 섞여 있다. 차트에는 건자재·소재 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문): 동부 건자재 1,020 + 서부 건자재 987 + 특수 소재 362 = 연결 2,369(1년 전 943 + 772 + 131 = 1,846).
SEG = [('건자재 — 동부', 1020, '#00467f'), ('건자재 — 서부', 987, '#4a7db5'), ('특수 소재(석회·마그네시아)', 362, '#a9c1dc')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 실적 3건(계속사업 희석 EPS) + 사업 교환·인수 완료. 최신 Q3 2026(11-04 장 전)은 news_auto가 붙인다. 반응일: 실적 07:0x 동부 장 전 → 같은 날, Quikrete 8-K 장 마감 뒤 → 다음 날, LNA 8-K 장 전 → 같은 날.
NEWS_RANGE = '2026.02 ~ 2026.11'
NEWS = [
    ('neutral', '2026년 8월 21일 — Lhoist North America 인수 완료', '2026-08-24',
     '총 $12.9B(현금 $7.0B — 사채·대출로 조달, 신주 10,953,543주) · 석회·석회석 사업이 특수 소재 부문에 더해짐 — 공시일(8/24 장 전) 주가 −0.3%', 'lna', 'Martin Marietta 공시 (SEC 8-K)'),
    ('red', '2026년 7월 30일 장 전 — Q2 2026 실적', '2026-07-30',
     '매출 $1.95B(+21%) · 계속사업 순이익 $256M · 계속사업 희석 EPS $4.26(1년 전 $4.84) · 조정 EPS $5.00 — 당일 주가 −5.2%', 'q2', 'Martin Marietta 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 30일 장 전 — Q1 2026 실적', '2026-04-30',
     '매출 $1.36B(+17%) · 계속사업 순이익 $79M · 계속사업 희석 EPS $1.31(1년 전 $1.70) · 조정 EPS $1.93 — 당일 주가 +1.0%', 'q1', 'Martin Marietta 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 23일 장 마감 뒤 — Quikrete 사업 교환 완료', '2026-02-24',
     '시멘트·레미콘 사업을 넘기고 골재 사업을 받음 — 처분이익은 중단사업(2026년 9개월 중단사업 순이익 $1,428M, 처분이익 세전 $1,962M 포함) · 다음 날 주가 +1.9%', 'quikrete', 'Martin Marietta 공시 (SEC 8-K)'),
    ('red', '2026년 2월 11일 장 전 — Q4 2025 실적', '2026-02-11',
     '매출 $1.53B(+9%) · 계속사업 순이익 $233M · 계속사업 희석 EPS $3.85(1년 전 $4.03) — 당일 주가 −6.6%', 'q4', 'Martin Marietta 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 24, 'nt': 15, 'mean': 625.4, 'median': 639, 'low': 520, 'high': 680, 'sb': 13, 'b': 4, 'h': 7, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-08'


# 미완성 카드 표시(2026-11-03 사용자 결정, FISV 방식). BUILD no_dcf가 판정을 보류로 만들고, 보험사용 문구를 미완성 사유로 바꾼다.
INCOMPLETE_SHORT = 'LNA 인수 손익 누적 대기'
INCOMPLETE_WHY = '2026년 8월 Lhoist North America 인수($12.9B)로 차입금·투하자본·주식 수는 이미 늘었는데 최근 4분기 손익에는 인수 회사가 40일치만 들어 있어, 현금흐름 모형의 내재가치가 음수로 나오고 PER·PSR·PCR·EV/EBITDA도 부풀려진다 — 인수 손익이 4분기 모두 쌓이는 2027년 3분기 보고서 뒤 다시 본다'
POST = [r"""
import re as _re0
_w = '2026년 8월 Lhoist North America 인수($12.9B)로 차입금·투하자본·주식 수는 이미 늘었는데 최근 4분기 손익에는 인수 회사가 40일치만 들어 있어, 현금흐름 모형의 내재가치가 음수로 나오고 PER·PSR·PCR·EV/EBITDA도 부풀려진다 — 인수 손익이 4분기 모두 쌓이는 2027년 3분기 보고서 뒤 다시 본다'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — LNA 인수 손익 누적 대기</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — LNA 인수 손익 누적 대기. 인수로 투하자본은 늘었는데 최근 4분기 손익엔 인수 회사가 40일치만 들어 현금흐름 내재가치를 계산하지 않았다(2027년 3분기 보고서 뒤 재검토).')
h = _re0.sub(r'(id="mlmFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)   # 미완성 — PER 구간 범위를 보이지 않는다(FISV처럼, Codex·Fable r1)
h = _re0.sub(r'(?<!계속사업 )희석 EPS', '계속사업 희석 EPS', h)   # 카드 EPS는 모두 계속사업 기준 — 자동 문구의 '희석 EPS'(1년 전 $5.97 = 계속사업)를 맞춘다(Fable r1)
import re as _re3
h = _re3.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re3.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")
"""]


# ── 자동 카드 — 부문 지도(손 작성). 원문 대조: Q3 2026 10-Q 1,020/987/362 = 연결 2,369, 1년 전 943/772/131 = 1,846(2026-11-07) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"mlm:BuildingMaterialsBusinessEastGroupMember": ["건자재 — 동부", "#00467f"], "mlm:BuildingMaterialsBusinessWestGroupMember": ["건자재 — 서부", "#4a7db5"],
             "mlm:SpecialtiesMember": ["특수 소재(석회·마그네시아)", "#a9c1dc"]},
 "ignore": ["mlm:ReportableSegmentsMember", "mlm:BuildingMaterialsBusinessMember"]   # 부문 합계·동부+서부 소계
}
