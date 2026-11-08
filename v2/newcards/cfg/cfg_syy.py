CIK = '0000096021'
BUILD = {'no_dcf': '미완성 — Jetro 인수 종결 대기'}   # 2026-11-03 사용자 결정(보류 C군 → 미완성 카드), 2026-11-07 제작
# SYY(시스코) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 6월 말(52·53주). 외식 식자재 유통 — 미국 외식·해외·SYGMA(체인 전용).
# 출처: SEC XBRL, Q1 FY27 10-Q(2026-11-03 18:55 동부 장 마감 뒤 → 첫 세션 11-04, 카드 기준일 11-06 종가), 실적 보도자료(8-K 2.02항 — 08:0x 동부 장 전 → 같은 날),
#        Jetro 인수 발표 8-K(2026-03-30 06:38 동부 장 전, FY26 가이던스 재확인·3분기 예비 지표 포함).
# 미완성 사유: Jetro Restaurant Depot(JRD) 인수 — 약 $29.1B(현금 $21.6B + 신주 91.5M주), FY27 3분기까지 종결 예상(10-Q). 종결 뒤 상장 모회사가 바뀌고(Sysco Holdings) 주식 수 약 19%·차입 증가.
#   인수 대비 금리 고정(deal contingent rate lock)을 Q1 FY27에 청산 — 기타수익 세전 $234M 일회성(대금 $241M 에스크로, 10-Q 주석 7). 빼면 Q1 EPS 약 $0.72(1년 전 $0.99).
#   2026-10 인수용 채권 약 $16.9B 발행(주석 15 — Q2 FY27 재무상태표부터), 남은 FY27 이자비용 약 $787M 예고. 해지 수수료 $1.164B(10-Q). 참고 점수 자기 80.3·동종 64.8.
#   데이터 한계: 감가상각 분기 값이 2015~2024년 요약 자료에 없어(10-K 연간만) EV/EBITDA 이력이 134일뿐 — 참고 점수에 영향. 순이익률 약 2.4%(A3 2% 기준선 근처).
CUR, YO, QO = '2026-09-26', '2025-09-27', '2026-06-27'
QLABEL, YL, QQL = 'Q1 FY27', 'Q1 FY26', 'Q4 FY26'
L8 = ['Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26', 'Q4 FY26', 'Q1 FY27']
FY_ENDS, FY_LABEL = ('2026-06-27', '2025-06-28'), 'FY26'
VOTES, VERDICT = (1, 0, 0), '판정 보류'
CO = 'Sysco'
S_ = 'https://www.sec.gov/Archives/edgar/data/96021/'
SEC = S_
TENQ = S_ + '000009602126000050/syy-20260926.htm'; TENQ_NAME = 'Q1 FY27 10-Q'
PR = {'q1': S_ + '000009602126000046/syy2027q1pressrelease.htm', 'q4': S_ + '000009602126000026/syy2026q4pressrelease.htm',
      'q3': S_ + '000009602126000019/syypressrelease-fy26q3.htm', 'q2': S_ + '000009602126000006/syypressrelease-fy26q2.htm',
      'deal': S_ + '000095014226000899/eh260758391_ex9901.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="syyFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(Jetro 인수 종결 대기)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 30)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('미완성 카드다. 2026년 3월 현금·창고형 식자재 도매업체 Jetro Restaurant Depot을 약 $29.1B(현금 $21.6B + 신주 약 9,150만 주)에 사기로 했다(회계연도 2027년 3분기까지 종결 예상). 종결되면 주식 수가 약 19% 늘고 차입이 크게 늘어 지금 재무로 낸 판정이 이어지지 않으므로 판정을 보류한다 — 자기 이력·동종업 점수는 참고값이다. '
              '최근 분기(Q1 FY27) 이익에는 인수 자금 금리를 미리 고정한 파생상품을 청산한 일회성 이익(세전 $234M)이 들어 있다 — 빼면 그 분기 희석 EPS는 약 $0.72로 1년 전($0.99)보다 낮다. 2026년 10월 인수 자금용 채권 약 $16.9B를 발행해 다음 분기부터 차입과 이자비용(남은 회계연도 약 $787M 예고)이 늘어난다. '
              '감가상각 분기 자료가 요약 자료에 비어 지금 계산된 EV/EBITDA 이력은 최근 몇 달뿐이다. 순이익률이 2%대 초반이라 이익이 조금만 흔들려도 PER이 크게 움직인다.')
PH = ['KR', 'COST', 'WMT', 'DG', 'ADM', 'KDP']
PEER_FILE = 'peer_universe/consumer_staples.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '유통·식품 6곳 PER 비교 (점수는 S&P500 필수소비재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 필수소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 필수소비재 대비 배수 순위 (v2/peer_universe/consumer_staples.json)'
PEER_TIP = ('S&P500 필수소비재(SYY 제외)와 배수 순위를 매긴 값이다.',
            '식품·음료·생활용품·유통이 섞여 있다. 차트에는 유통·식품 6곳만 보인다.')
# 매출(Q1 FY27 10-Q 부문 — 부문 축만 붙은 값): 미국 외식 15,142 + 해외 4,168 + SYGMA 2,152 + 기타 282 = 21,744(1년 전 14,780 + 3,966 + 2,129 + 273 = 21,148).
SEG = [('미국 외식 유통', 15142, '#0058a3'), ('해외 외식 유통', 4168, '#4d8fd1'), ('SYGMA(체인 전용)', 2152, '#a9c9ea'), ('기타', 282, '#c9c9c9')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 실적 3건(GAAP 희석 EPS) + Jetro 인수 발표. 최신 Q1 FY27(11-03 장 전)은 news_auto.
NEWS_RANGE = '2026.01 ~ 2026.11'
NEWS = [
    ('neutral', '2026년 8월 4일 장 전 — Q4 FY26 실적', '2026-08-04',
     '매출 $22.1B(+4.7%) · 순이익 $551M · 희석 EPS $1.15(1년 전 $1.10) — 당일 주가 −2.6%', 'q4', 'Sysco 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 28일 장 전 — Q3 FY26 실적', '2026-04-28',
     '매출 $20.5B(+4.7%) · 순이익 $340M · 희석 EPS $0.71(1년 전 $0.82) — 당일 주가 −2.6%', 'q3', 'Sysco 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 3월 30일 장 전 — Jetro Restaurant Depot 인수 발표', '2026-03-30',
     '약 $29.1B(현금 $21.6B + 신주 약 9,150만 주) · FY26 가이던스 재확인·3분기 예비 지표와 함께 발표 — 당일 주가 −15.3%', 'deal', 'Sysco 공시 (SEC 8-K)'),
    ('green', '2026년 1월 27일 장 전 — Q2 FY26 실적', '2026-01-27',
     '매출 $20.8B(+3.0%) · 순이익 $389M · 희석 EPS $0.81(1년 전 $0.82) — 당일 주가 +11.0%', 'q2', 'Sysco 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 14, 'nt': 11, 'mean': 91.82, 'median': 91, 'low': 84, 'high': 102, 'sb': 5, 'b': 2, 'h': 6, 's': 0, 'ss': 1}
ANALYST_ASOF = '2026-11-08'


# 미완성 카드 표시(2026-11-03 사용자 결정, FISV·MLM·NSC·PTC·CHRW 방식).
INCOMPLETE_SHORT = 'Jetro 인수 종결 대기'
INCOMPLETE_WHY = '2026년 3월 Jetro Restaurant Depot 인수(약 $29.1B — 현금 $21.6B + 신주 9,150만 주, 회계연도 2027년 3분기까지 종결 예상)를 발표했다 — 종결되면 주식 수 약 19%·차입이 크게 늘어 지금 재무로 낸 판정이 이어지지 않는다. 종결 뒤 분기가 쌓이면 다시 본다'
POST = [r"""
import re as _re0
_w = '2026년 3월 Jetro Restaurant Depot 인수(약 $29.1B — 현금 $21.6B + 신주 9,150만 주, 회계연도 2027년 3분기까지 종결 예상)를 발표했다 — 종결되면 주식 수 약 19%·차입이 크게 늘어 지금 재무로 낸 판정이 이어지지 않는다. 종결 뒤 분기가 쌓이면 다시 본다'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — Jetro 인수 종결 대기</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — Jetro 인수 종결 대기. 인수 뒤 재무가 크게 바뀌어 현금흐름 내재가치를 계산하지 않았다.')
h = _re0.sub(r'(id="syyFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)   # 미완성 — PER 구간 범위를 보이지 않는다(FISV처럼, Codex·Fable r1)
import re as _re3
h = _re3.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re3.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")

h = _re0.sub(r'(<div class="verdict-summary-head">[^<]*)<span class="tag">[^<]*</span>', r'\1<span class="tag">Jetro 인수 종결 대기</span>', h, count=1)
for _id in ('syyDcfVerdict', 'syyDcfBox', 'dcfPickValue'):
    h = h.replace(f'id="{_id}">계산 불가<', f'id="{_id}">보류(미완성)<')

h = _re0.sub(r'<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)   # 참고 점수를 약점으로 올리지 않는다(Fable r1)

h = _re0.sub(r'<div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)   # 참고 점수를 강점으로 올리지 않는다(Codex·Fable r1)
h = _re0.sub(r'(<strong style="color:var\(--accent2\);">③</strong> )차입금 \$[0-9.]+B이 줄어드는지', r'\1Jetro 인수 승인·종결 여부와 인수 자금 이자비용(남은 FY27 약 $787M 예고)', h, count=1)   # 인수자라 차입은 늘어난다(Fable r1)

h = _re0.sub(r'(<div class="bb-title bb-bull">🐂 Bull 요인</div>)\s*(</div>)', r'\1\n      <div class="bb-row bull"><span class="bb-icon">·</span><span class="bb-head">보류</span><span class="bb-text">미완성 카드라 배수 점수를 강점으로 올리지 않는다 — Jetro 인수 종결 뒤 다시 본다.</span></div>\n    \2', h, count=1)   # 빈 Bull 칸(Codex r2)
"""]


# ── 자동 카드 — 부문 지도(손 작성, 부문 축만 붙은 값). 원문 대조: Q1 FY27 10-Q 15,142/4,168/2,152/282 = 21,744, 1년 전 21,148(2026-11-07) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"syy:U.S.FoodserviceOperationsMember": ["미국 외식 유통", "#0058a3"], "syy:InternationalFoodserviceOperationsMember": ["해외 외식 유통", "#4d8fd1"],
             "syy:SygmaSegmentMember": ["SYGMA(체인 전용)", "#a9c9ea"], "us-gaap:AllOtherSegmentsMember": ["기타", "#c9c9c9"]},
 "ignore": []
}
