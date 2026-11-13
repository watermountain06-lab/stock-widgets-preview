CIK = '0000882835'
BUILD = {'no_dcf': '미완성 — Indicor 지분 평가 이익이 최근 4분기 GAAP 이익의 약 40%'}   # 2026-11-07·08 사용자 규칙(일회성 30% 이상이면 미완성, 회사 분류를 따른다) — RVTY·AXON과 같은 처리
# ROP(로퍼 테크놀로지스) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 12월 말. 수직 산업 소프트웨어(응용·네트워크)와 기술 기반 제품(계측·의료 장비 등).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-11-02 장 마감 뒤 접수, 카드 기준일 11-12 종가), 실적 보도자료(8-K 2.02항 — 모두 장 전 07:00 동부 무렵 → 그날).
# 일회성(E54): 최근 4분기 GAAP 희석 EPS 25.34(3.97 + 4.87 + 11.62 + 4.88).
#   회사 조정표(세후 주당 $): 소수 지분 투자(Indicor — 2022년 매각한 산업 부문 지분, 공정가치 평가) 이익 Q4 2025 −0.30 · Q1 2026 −1.28 · Q2 2026 −7.86 · Q3 2026 −0.71,
#   거래 비용 Q3 2026 0.05 → 순 일회성 이익 $10.10(GAAP의 약 40%). 인수 무형자산 상각(분기 약 $1.5~1.7)은 반복 비용(사용자 규칙)으로 둔다.
#   Indicor 세전 이익은 2026년 9개월 $1,059M(세후 $996M — 회사 조정표 세율은 Indicor만 21%가 아님). Q3에 Indicor 계측 사업 매각 대금 $1,239M을 받았다(현금흐름표).
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, 1, 0), '판정 보류'
CO = 'Roper'
S_ = 'https://www.sec.gov/Archives/edgar/data/882835/'
SEC = S_
TENQ = S_ + '000088283526000047/rop-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000088283526000042/a2026q3earningsrelease.htm', 'q2': S_ + '000088283526000031/a2026q2earningsrelease.htm',
      'q1': S_ + '000088283526000015/a2026q1earningsrelease.htm', 'q4': S_ + '000088283526000003/a2025q4earningsrelease.htm',
      'q3p': S_ + '000088283525000041/a2025q3earningsrelease.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="ropFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(Indicor 지분 이익이 최근 4분기 GAAP 이익을 크게 부풀린다)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (미완성 — 현금흐름 보류)</span>'
Y2 = (-10, 30)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('미완성 카드다. 이 카드는 일회성 항목이 최근 4분기 GAAP 이익의 30% 이상이면 판정을 보류하는데, ROP는 최근 4분기 GAAP 희석 EPS $25.34 가운데 약 40%(세후 주당 약 $10.10)가 본업 밖 이익이다. '
              '2022년에 매각한 산업 부문(Indicor)의 소수 지분을 공정가치로 평가하는데, Indicor가 2026년 계측 사업을 팔기로 하면서 평가 이익이 크게 잡혔다(2026년 9개월 세전 $1,059M, 가장 큰 2분기 주당 $7.86). 회사도 이 손익을 조정 EPS에서 뺀다. '
              '인수 무형자산 상각(분기 주당 약 $1.5~1.7)은 매 분기 반복되는 비용이라 카드는 일회성으로 보지 않는다. 회사 조정 EPS는 상각을 더하지만 Indicor 이익을 빼는 폭이 더 커서 2026년 전망 $22.35~22.40으로 GAAP 전망($25.60~25.65)보다 낮다. Indicor 공정가치 평가는 매 분기 생기지만 회사가 앞으로도 비GAAP에서 계속 빼는 항목이라 카드도 일회성으로 센다. '
              '분기마다 다시 센다. 새 Indicor 손익이 없고 4분기 GAAP EPS가 회사 전망($4.27~4.32)대로면 2027년 1월 실적 때도 약 38%라 미완성이 이어지고, 가장 큰 2분기 이익(주당 $7.86)이 빠지는 2027년 2분기 실적(2027년 7월 예상)이 주요 확인 시점이다. 10-Q에 따르면 Indicor가 유량 제어 사업도 Xylem에 팔기로 해 4분기 종결 때 Roper가 세전 약 $600M을 받을 예정이다(남은 지분 장부가 $577M) — 그때 평가 손익이 새로 잡히면 계산이 달라진다. '
              'PER 18.9배(5년 중앙 41.5배)가 낮은 것은 이 이익 때문이다 — 카드 규칙대로 일회성만 빼면(EPS 약 $15.24) 약 31배, 회사 조정 EPS(2026년 전망, 상각까지 더함)로는 약 21배다. PSR·PCR·EV/EBITDA도 5년 중 하위 16% 안팎이라 PER만의 착시는 아니다. '
              '본업은 꾸준하다 — 3분기 매출 $2.17B(+8%, 유기 +7%), 응용 소프트웨어 $1.24B(+7%)·네트워크 소프트웨어 $446M(+8%)·기술 기반 제품 $486M(+10%), 조정 EBITDA $864M(+7%). 2026년 조정 EPS 전망을 세 번 올렸다($21.30~21.55 → $21.80~22.05 → $22.15~22.30 → $22.35~22.40) — 다만 회사도 자사주 매입을 상향 이유로 들었고, 3분기 조정 순이익은 +5%로 주당 +15%의 상당 부분은 주식 수 감소 덕이다. '
              '2025년 4분기부터 자사주를 대규모로 사들여(2026년 9개월 7.9M주 $2.73B) 유통 주식이 2025년 말 106.6M에서 9월 말 99.0M주가 됐다 — 3분기에는 사지 않았고 남은 한도는 $2.78B다. 차입금은 $9.72B(9월 말, 1년 안 만기 $1.42B), 현금 $311M. 3분기에 Indicor 매각 대금 $1.24B(세전 — 관련 현금 세금 약 $150M 예정)를 받았고 남은 Indicor 지분 장부가는 $577M이다. 카드 EV는 이 지분을 빼지 않는다(빼면 EV/EBITDA 17.2배 → 17.1배). '
              '주가는 2월 17일 종가 $315.53(5월에도 $316 부근)에서 11월 12일 $477.87로 회복했다(1월 실적 날 −9.6%, 10월 실적 날 +9.7%).')
PH = ['MSFT', 'ORCL', 'CRM', 'PANW', 'PLTR']   # 비교 자료(카드 유니버스 IT)에 값이 있는 종목만
PEER_FILE = None
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '소프트웨어 5곳 PER 비교 (점수는 카드 유니버스 IT 기준)', 'pbr': '소프트웨어 PBR 비교', 'psr': '소프트웨어 PSR 비교',
                'pcr': '소프트웨어 PCR(FCF) 비교', 'evebitda': '소프트웨어 EV/EBITDA 비교'}
PEER_NAME_TITLE = '카드 유니버스 IT 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = '카드 유니버스 IT 종목 대비 배수 순위'
PEER_TIP = ('카드 유니버스 IT 종목(ROP 제외)과 배수 순위를 매긴 값이다.',
            '반도체·하드웨어·소프트웨어가 섞여 있다. 차트에는 소프트웨어 5곳만 보인다.')
# 매출(Q3 2026 보도자료 부문): 응용 소프트웨어 1,239.7 + 네트워크 소프트웨어 446.1 + 기술 기반 제품 486.0 = 2,171.8.
SEG = [('응용 소프트웨어(정부·보험·의료·건설)', 1239.7, '#1f4e8c'), ('네트워크 소프트웨어(운송·식품 공급망 등)', 446.1, '#7fa7d8'), ('기술 기반 제품(계측·의료 장비)', 486.0, '#a8b3bf')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 실적 5건. 반응일: 모두 장 전 발표 → 그날. 색은 사건 성격, 수치는 그날 주가.
NEWS_RANGE = '2025.10 ~ 2026.11'
NEWS = [
    ('green', '2026년 10월 22일 장 전 — Q3 2026 실적', '2026-10-22',
     '매출 $2.17B(+8%, 유기 +7%) · GAAP 희석 EPS $4.88 · 조정 EPS $5.89(+15%) · Indicor 계측 사업 매각 대금 $1.2B 수령 · 연간 조정 EPS 전망 $22.35~22.40으로 상향 — 그날 주가 +9.7%', 'q3', 'Roper 보도자료 (SEC 8-K)'),
    ('green', '2026년 7월 23일 장 전 — Q2 2026 실적', '2026-07-23',
     '매출 $2.11B(+9%, 유기 +5%) · GAAP 희석 EPS $11.62(Indicor 평가 이익 주당 $7.86 포함) · 조정 EPS $5.38(+10%) · 2분기 자사주 3.6M주 $1.2B · 연간 전망 상향 — 그날 주가 +5.5%', 'q2', 'Roper 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 23일 장 전 — Q1 2026 실적', '2026-04-23',
     '매출 $2.10B(+11%, 유기 +6%) · GAAP 희석 EPS $4.87 · 조정 EPS $5.16(+8%) · 자사주 매입 한도 $3B 추가 · 연간 전망 상향 — 그날 주가 −0.3%', 'q1', 'Roper 보도자료 (SEC 8-K)'),
    ('red', '2026년 1월 27일 장 전 — 2025년 연간 실적', '2026-01-27',
     '4분기 매출 $2.06B(+10%, 유기 +4%) · GAAP 희석 EPS $3.97 · 조정 EPS $5.21(+8%) · 2026년 조정 EPS $21.30~21.55 전망 — 그날 주가 −9.6%', 'q4', 'Roper 보도자료 (SEC 8-K)'),
    ('red', '2025년 10월 23일 장 전 — Q3 2025 실적', '2025-10-23',
     '매출 $2.02B(+14%, 유기 +6%) · GAAP 희석 EPS $3.68 · 조정 EPS $5.14(+11%) — 그날 주가 −5.7%', 'q3p', 'Roper 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 19, 'nt': 11, 'mean': 476.27, 'median': 490, 'low': 335, 'high': 550, 'sb': 7, 'b': 0, 'h': 11, 's': 0, 'ss': 1}
ANALYST_ASOF = '2026-11-13'

# 재검토 기록용(자동 재판정 코드는 아직 없음) — 일회성이 든 분기(결산일: 항목, 세후 주당 $, +는 비용·−는 이익). 인수 무형자산 상각은 반복으로 빼지 않는다.
ONEOFF_QUARTERS = {'2025-12-31': 'Indicor 지분 이익 −0.30 (세후 주당 $)',
                   '2026-03-31': 'Indicor 지분 이익 −1.28 (세후 주당 $)',
                   '2026-06-30': 'Indicor 지분 평가 이익 −7.86 (세후 주당 $)',
                   '2026-09-30': 'Indicor 지분 이익 −0.71 · 거래 비용 0.05 (세후 주당 $)'}

# 미완성 카드 표시(2026-11-08 사용자 규칙, AXON·RVTY 방식).
INCOMPLETE_SHORT = 'Indicor 지분 이익이 큼'
INCOMPLETE_WHY = '최근 4분기 GAAP 이익의 약 40%(세후 주당 약 $10.10)가 2022년 매각한 Indicor 지분의 평가 이익이다 — 배수 판정이 왜곡돼 보류한다. 분기마다 다시 세고, 주요 확인은 2027년 7월(2분기 이익 주당 $7.86이 빠질 때) — 4분기 Indicor 손익이 새로 잡히면 늦어질 수 있다'
POST = [r"""
import re as _re0
_w = '최근 4분기 GAAP 이익의 약 40%(세후 주당 약 $10.10)가 2022년 매각한 Indicor 지분의 평가 이익이다 — 배수 판정이 왜곡돼 보류한다. 분기마다 다시 세고, 주요 확인은 2027년 7월(2분기 이익 주당 $7.86이 빠질 때) — 4분기 Indicor 손익이 새로 잡히면 늦어질 수 있다'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — Indicor 지분 이익이 큼 · 매 분기 재검토, 주요 확인 2027년 7월</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — Indicor 지분 이익이 큼. 미완성 카드 규칙에 따라 종합 판정과 함께 현금흐름 내재가치도 보류했다.')
h = _re0.sub(r'(id="ropFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)
h = _re0.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re0.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")
h = _re0.sub(r'(<div class="verdict-summary-head">[^<]*)<span class="tag">[^<]*</span>', r'\1<span class="tag">Indicor 지분 이익이 큼</span>', h, count=1)
h = _re0.sub(r'<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
h = _re0.sub(r'<div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
# ③ 차입금: 4분기 Indicor 유량 제어 매각 대금(세전 약 $600M)이 들어오면 본업 현금과 따로 본다(Codex r1)
_c3 = h[h.index('<strong style="color:var(--accent2);">③</strong>'):]; _c3 = _c3[:_c3.index('</div>')]
h = h.replace(_c3, '<strong style="color:var(--accent2);">③</strong> 차입금 $9.7B(1년 안 만기 $1.42B)이 줄어드는지 — 4분기 Indicor 유량 제어 매각 대금(세전 약 $600M 예상)이 들어오면 본업 현금과 나눠 본다. 4분기 Indicor 평가 손익이 얼마로 잡히는지도 미완성 해제에 영향을 준다', 1)
"""]

AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"rop:ApplicationSoftwareSegmentMember": ["응용 소프트웨어(정부·보험·의료·건설)", "#1f4e8c"], "rop:NetworkSoftwareSegmentMember": ["네트워크 소프트웨어(운송·식품 공급망 등)", "#7fa7d8"], "rop:TechnologyEnabledProductsSegmentMember": ["기술 기반 제품(계측·의료 장비)", "#a8b3bf"]}
}
