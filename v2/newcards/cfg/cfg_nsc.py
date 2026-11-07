CIK = '0000702165'
BUILD = {'no_dcf': '미완성 — UNP 인수 종결 대기'}   # 2026-11-03 사용자 결정(보류 C군 → 미완성 카드), 2026-11-07 제작
# NSC(노퍽 서던) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 12월 31일. 미국 동부 화물 철도 — 일반 화물·복합운송(컨테이너)·석탄.
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-22 13:05 동부 장중 접수 → 카드 기준일 11-06 종가), 실적 보도자료(8-K 2.02항 — 08:0x~08:2x 동부 장 전 → 같은 날), 주주총회 승인 8-K(2025-11-17).
# 미완성 사유: 2025-07-28 Union Pacific 합병 계약(주식 + 현금), 2025-11-14 주주 승인, STB 승인 대기, 파기 수수료 $2.5B(10-Q 주석 1) — 주가가 인수 조건에 묶여 배수·내재가치 판정 의미가 약하다.
#   합병 관련 비용: Q3 2026 $42M·9개월 $145M(영업비용). 참고 점수 자기 28.4·동종 40.5. 엔진 경고: 단기투자 태그 2014 멈춤(없음), 리스 2025-12(10-K만) — 현금흐름은 계산하지 않으므로 영향 없음.
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, 0, 0), '판정 보류'
CO = 'Norfolk Southern'
S_ = 'https://www.sec.gov/Archives/edgar/data/702165/'
SEC = S_
TENQ = S_ + '000162828026066836/nsc-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000119312526428384/nsc-ex99_1.htm', 'q2': S_ + '000119312526313393/nsc-ex99_1.htm',
      'q1': S_ + '000119312526175084/nsc-ex99_1.htm', 'q4': S_ + '000119312526028244/nsc-ex99_1.htm',
      'vote': S_ + '000119312525283950/d30760dex991.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="nscFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(주가가 인수 조건에 묶여 있다)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 45)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('미완성 카드다. 2025년 7월 Union Pacific과 합병 계약을 맺었고(NSC 1주당 UNP 1주 + 현금 $88.82), 2025년 11월 주주가 승인해 미 육상교통위원회(STB) 승인을 기다린다(회사 예상 종결 2027년 초). 주가가 인수 조건(UNP 주가)에 묶여 움직이므로 — 자기 이력 대비 비싸 보이는 것도 인수 프리미엄 때문이라 — 배수와 현금흐름으로 단독 가치를 판정하지 않는다 — 자기 이력·동종업 점수는 참고값이다. '
              '계약에 정한 특정 사유로 해지되면 NSC나 UNP 중 한쪽이 $2.5B 파기 수수료를 낸다. 최근 4분기 이익에는 합병 관련 비용(2026년 9개월만 $145M, 2025년 4분기에도 있음)과 2023년 오하이오 탈선 사고 관련 비용·회수가 섞여 있다.')
PH = ['UNP', 'CSX', 'ODFL', 'JBHT', 'FDX', 'UPS']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '철도·화물 운송 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': '철도·화물 운송 PBR 비교', 'psr': '철도·화물 운송 PSR 비교',
                'pcr': '철도·화물 운송 PCR(FCF) 비교', 'evebitda': '철도·화물 운송 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(NSC 제외)와 배수 순위를 매긴 값이다.',
            '기계·항공·운송·건설·업무 서비스 회사가 섞여 있다. 차트에는 철도·화물 운송 6곳만 보인다.')
# 매출(Q3 2026 10-Q 시장별): 일반 화물 2,188 + 복합운송 919 + 석탄 419 = 3,526(1년 전 1,969 + 759 + 375 = 3,103).
SEG = [('일반 화물', 2188, '#1b3a6b'), ('복합운송(컨테이너)', 919, '#4f6f9f'), ('석탄', 419, '#a9bcd6')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 시장별'
# 손 뉴스: 실적 3건(GAAP 희석 EPS) + 주주 승인. 최신 Q3 2026(10-22 장 전)은 news_auto가 붙인다.
NEWS_RANGE = '2025.11 ~ 2026.10'
NEWS = [
    ('green', '2026년 7월 23일 장 전 — Q2 2026 실적', '2026-07-23',
     '매출 $3.47B(+11.4%) · 순이익 $734M · 희석 EPS $3.26(1년 전 $3.41) — 당일 주가 +5.3%', 'q2', 'Norfolk Southern 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 24일 장 전 — Q1 2026 실적', '2026-04-24',
     '매출 $3.00B(+0.2%) · 순이익 $547M · 희석 EPS $2.43(1년 전 $3.31) — 당일 주가 −0.5%', 'q1', 'Norfolk Southern 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 1월 29일 장 전 — Q4 2025 실적', '2026-01-29',
     '매출 $2.97B(−1.7%) · 순이익 $644M · 희석 EPS $2.87(1년 전 $3.23) — 당일 주가 +2.0%', 'q4', 'Norfolk Southern 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 11월 14일 장 전 — 주주총회에서 Union Pacific 합병 승인', '2025-11-14',
     '찬성 약 99% · NSC 1주당 UNP 1주 + 현금 $88.82 · STB 승인 대기, 회사 예상 종결 2027년 초 — 발표일 주가 +0.2%', 'vote', 'Norfolk Southern 공시 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 21, 'nt': 13, 'mean': 362, 'median': 355, 'low': 323, 'high': 400, 'sb': 4, 'b': 1, 'h': 16, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-07'


# 미완성 카드 표시(2026-11-03 사용자 결정, FISV·MLM 방식).
INCOMPLETE_SHORT = 'UNP 인수 종결 대기'
INCOMPLETE_WHY = '2025년 7월 Union Pacific과 합병 계약(주식 + 현금)을 맺어 미 육상교통위원회(STB) 승인을 기다리고 있다 — 주가가 인수 조건(UNP 주가)에 묶여 움직여 단독 가치평가의 의미가 약하다. 합병이 끝나면 상장 폐지되고, 무산되면 그때 다시 본다'
POST = [r"""
import re as _re0
_w = '2025년 7월 Union Pacific과 합병 계약(주식 + 현금)을 맺어 미 육상교통위원회(STB) 승인을 기다리고 있다 — 주가가 인수 조건(UNP 주가)에 묶여 움직여 단독 가치평가의 의미가 약하다. 합병이 끝나면 상장 폐지되고, 무산되면 그때 다시 본다'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — UNP 인수 종결 대기</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — UNP 인수 종결 대기. 주가가 인수 조건에 묶여 있어 현금흐름 내재가치를 계산하지 않았다.')
h = _re0.sub(r'(id="nscFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)   # 미완성 — PER 구간 범위를 보이지 않는다(FISV처럼, Codex·Fable r1)
import re as _re3
h = _re3.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re3.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")
"""]


# ── 자동 카드 — 부문 지도(손 작성, 시장별). 원문 대조: Q3 2026 10-Q 2,188/919/419 = 3,526, 1년 전 1,969/759/375 = 3,103(2026-11-07) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"nsc:RailwayOperatingRevenuesMarketGroupMerchandiseMember": ["일반 화물", "#1b3a6b"],
             "nsc:RailwayOperatingRevenuesMarketGroupIntermodalMember": ["복합운송(컨테이너)", "#4f6f9f"],
             "nsc:RailwayOperatingRevenuesMarketGroupCoalMember": ["석탄", "#a9bcd6"]},
 "ignore": ["nsc:ReportableSegmentMember", "us-gaap:ReportableSegmentMember"]
}
