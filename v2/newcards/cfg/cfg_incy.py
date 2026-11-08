CIK = '0000879169'
BUILD = {'no_dcf': '미완성 — Vega 인수 IPR&D 비용(2027년 2분기까지 반영)'}   # 2026-11-07 사용자 결정(D군 → 미완성 카드: 일회성이 GAAP 이익을 크게 왜곡)
# INCY(인사이트) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 12월 31일. 혈액암·골수 질환(Jakafi), 피부질환 크림(Opzelura), 혈액·종양 신약, 로열티(Jakavi·Olumiant).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-29 16:03 동부 장 마감 뒤 → 첫 세션 10-30, 카드 기준일 11-06 종가), 실적 보도자료(8-K 2.02항 — 모두 장 전 07:0x 동부 → 그날),
#        Vega 인수 계약(2026-06-08 07:05 동부)·종결(07-06 16:06 동부 → 07-07), CMS 합의(06-22 07:00 동부, 08-31 16:29 동부 → 09-01).
# 엔진 입력(2026-11-07): 차입금 없음(2020 전환사채 전환 뒤 0 — EV_ZERO_AT_BY_CIK), 현금 $3,275.9M + 시장성 증권 $578.7M(새 태그 — EV_TAGS_BY_CIK 튜플),
#   설비투자 PaymentsToAcquireOtherProductiveAssets(2021-12부터 — 기본 태그 2022-12에 멈춤).
# 일회성: Q3 2026 Vega IPR&D $1,231.5M(세금 공제 안 됨, 주당 약 6.06) → 분기 EPS −3.86, 최근 4분기 GAAP 희석 EPS 1.88(1.46 + 1.47 + 2.81 − 3.86).
#   Q2 2026 매출에 CMS 합의 일회성 이익 $246M(Opzelura 리베이트). IPR&D는 2027년 3분기 10-Q(2027년 10~11월)부터 최근 4분기에서 빠진다 — 그때 정식 판정으로 다시 본다(Fable r1).
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, -1, 0), '판정 보류'
CO = 'Incyte'
S_ = 'https://www.sec.gov/Archives/edgar/data/879169/'
SEC = S_
TENQ = S_ + '000087916926000066/incy-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000087916926000063/incy-q32026xexx991.htm', 'q2': S_ + '000087916926000053/incy-q22026xexx991.htm',
      'q1': S_ + '000087916926000023/incy-q12026xexx991.htm', 'q4': S_ + '000087916926000006/incy-q42025xexx991.htm',
      'vega': S_ + '000087916926000040/june2026skyline-exhibit991.htm', 'vegadone': S_ + '000087916926000048/ax2026skylineclosingxex99.htm', 'zynyz': S_ + '000087916926000013/incy-20260227.htm', 'cms': S_ + '000087916926000046/incy-20260622.htm',
      'cms2': S_ + '000087916926000058/incy-20260831.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="incyFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(Q3 2026 Vega 인수 IPR&D 비용 $1.23B가 최근 4분기 이익을 크게 낮춘다)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (-50, 50)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('미완성 카드다. 2026년 7월 Vega Therapeutics를 선급금 $1.25B(미국 매출 마일스톤 최대 $0.75B 별도)에 인수하면서, 가장 흔한 유전성 출혈 질환인 폰 빌레브란트병 신약 후보(latarcibart·옛 VGA039, 임상 3상)가 가치의 거의 전부라 회계상 자산 인수로 처리했다. 그리고 다른 용도가 없는 연구개발 자산이라 인수 대금 대부분($1.23B)을 3분기 연구개발비(IPR&D)로 한 번에 비용 처리했다. '
              '그래서 3분기 희석 EPS가 −$3.86이고 최근 4분기 GAAP EPS가 약 $1.88로 크게 낮아져 PER이 높게 나온다 — 이 비용은 세금 공제가 안 돼 주당 약 $6.06에 해당하고, 2027년 2분기 10-Q까지 최근 4분기에 남는다. '
              '한편 2분기 매출에는 Opzelura 리베이트 소송을 끝낸 CMS 합의로 한 번 생긴 비현금 이익 $246M이 들어 있다. 차입금이 없고 현금·시장성 증권이 $3.9B다. '
              '매출의 절반 남짓이 주력 Jakafi인데 핵심 특허가 2028년 중·후반에 끝나, 회사는 Opzelura와 혈액·종양 제품으로 성장을 넓히는 중이다(2026년 Opzelura 매출 전망 $1,100~1,120M로 상향 — CMS 일회성 $246M 포함). '
              '자기 이력·동종업 점수는 참고값이고 판정은 보류한다. IPR&D가 최근 4분기에서 빠지면 정식 판정으로 다시 본다.')
PH = ['VRTX', 'REGN', 'BIIB', 'GILD', 'AMGN', 'MRNA']
PEER_FILE = 'peer_universe/health_care.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '바이오 6곳 PER 비교 (점수는 S&P500 헬스케어 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 헬스케어 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 헬스케어 대비 배수 순위 (v2/peer_universe/health_care.json)'
PEER_TIP = ('S&P500 헬스케어(INCY 제외)와 배수 순위를 매긴 값이다.',
            '제약·의료기기·보험이 섞여 있다. 차트에는 바이오 6곳만 보인다.')
# 매출(Q3 2026 보도자료 매출 표): Jakafi 826.5 + Opzelura 254.9 + 혈액·종양 신약(Iclusig 33.5·Pemazyre 21.2·Minjuvi/Monjuvi 54.6·Niktimvo 67.4·Zynyz 58.3) 235.0
#   + 로열티 191.0 + 마일스톤·계약 49.8 = 1,557.2.
SEG = [('Jakafi(골수섬유증 등, XR 포함)', 826.5, '#003b71'), ('Opzelura(피부 크림)', 254.9, '#d94f2b'), ('혈액·종양 기타 제품', 235.0, '#7fa7cf'),
       ('로열티(Jakavi·Olumiant 등)', 191.0, '#f2b8a8'), ('마일스톤·계약', 49.8, '#c9c9c9')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 제품별'
# 손 뉴스: 실적 4건(Q3는 IPR&D·전망 상향이 함께 나와 손 항목) + Vega 인수 + CMS 합의 2건. 반응일: 실적 8-K 장 전 07:0x 동부 → 그날.
NEWS_RANGE = '2026.02 ~ 2026.10'
NEWS = [
    ('neutral', '2026년 10월 29일 장 전 — Q3 2026 실적', '2026-10-29',
     '매출 $1.56B(+14%) · 순손실 $785M · 희석 EPS −$3.86(1년 전 $2.11) — Vega IPR&D 비용 $1.23B · Opzelura 매출 +36% · 2026년 제품 순매출 전망 $5.21~5.30B로 상향(Opzelura·혈액종양 포함) — 그날 주가 −0.1%', 'q3', 'Incyte 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 8월 31일 장 마감 뒤 — CMS 약가 합의', '2026-09-01',
     '주 Medicaid에 Jakafi를 다른 선진국 수준 가격으로 공급 · 앞으로의 일부 CMS 약가 규제(GUARD·GLOBE 모델) 적용 제외 예상 · 회사는 2026년 가이던스에 영향 없다고 봄 — 다음 날 주가 +1.5%', 'cms2', 'Incyte 공시 (SEC 8-K)'),
    ('green', '2026년 7월 28일 장 전 — Q2 2026 실적', '2026-07-28',
     '매출 $1.67B(+38%, CMS 합의 일회성 $246M 포함) · 순이익 $586M · 희석 EPS $2.81(1년 전 $2.04) — 그날 주가 +9.3%', 'q2', 'Incyte 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 7월 6일 장 마감 뒤 — Vega 인수 완료', '2026-07-07',
     '임상 3상 폰 빌레브란트병 신약 후보 VGA039(latarcibart) 확보 — 다음 날 주가 +2.1%', 'vegadone', 'Incyte 보도자료 (SEC 8-K)'),
    ('green', '2026년 6월 22일 장 전 — CMS와 Opzelura 리베이트 소송 합의', '2026-06-22',
     'CMS가 Opzelura에 Jakafi의 라인 확장(기존 약의 변형 제품) 리베이트 규정을 적용하지 않기로 함 · 2분기 매출로 잡히는 비현금 일회성 이익 약 $246M — 그날 주가 +5.5%', 'cms', 'Incyte 공시 (SEC 8-K)'),
    ('neutral', '2026년 6월 8일 장 전 — Vega Therapeutics 인수 계약', '2026-06-08',
     '선급금 $1.25B + 판매 마일스톤 최대 $0.75B(총 최대 $2.0B) — 그날 주가 −1.7%', 'vega', 'Incyte 보도자료 (SEC 8-K)'),
    ('green', '2026년 4월 28일 장 전 — Q1 2026 실적', '2026-04-28',
     '매출 $1.27B(+21%) · 순이익 $303M · 희석 EPS $1.47(1년 전 $0.80) — 그날 주가 +2.1%', 'q1', 'Incyte 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 3월 6일 장 마감 뒤 — Zynyz 폐암 적응증 FDA 보완 요구(CRL)', '2026-03-09',
     '전이성 비소세포폐암 병용 적응증 추가 신청에 보완 요구 — 효능·안전성이 아니라 위탁 충전 공장(Catalent Indiana) 점검 문제 때문 — 다음 거래일 주가 +1.2%', 'zynyz', 'Incyte 공시 (SEC 8-K)'),
    ('red', '2026년 2월 10일 장 전 — Q4 2025 실적', '2026-02-10',
     '매출 $1.51B(+28%) · 순이익 $299M · 희석 EPS $1.46(1년 전 $1.02) — 그날 주가 −8.2%', 'q4', 'Incyte 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 28, 'nt': 21, 'mean': 133.71, 'median': 130, 'low': 108, 'high': 157, 'sb': 11, 'b': 2, 'h': 14, 's': 1, 'ss': 0}
ANALYST_ASOF = '2026-11-07'

# 미완성 카드 표시(2026-11-07 사용자 결정, D·SRE 방식).
INCOMPLETE_SHORT = 'Vega 인수 IPR&D 비용 반영 중'
INCOMPLETE_WHY = '2026년 3분기에 Vega 인수 대금 대부분($1.23B)을 연구개발비로 한 번에 처리해 최근 4분기 GAAP 이익이 크게 낮아졌다(2027년 2분기까지 반영) — 배수 판정이 왜곡돼 보류한다. 이 비용이 최근 4분기에서 빠지면 다시 본다'
POST = [r"""
import re as _re0
_w = '2026년 3분기에 Vega 인수 대금 대부분($1.23B)을 연구개발비로 한 번에 처리해 최근 4분기 GAAP 이익이 크게 낮아졌다(2027년 2분기까지 반영) — 배수 판정이 왜곡돼 보류한다. 이 비용이 최근 4분기에서 빠지면 다시 본다'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — Vega 인수 IPR&D 비용 반영 중</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — Vega 인수 IPR&D 비용 반영 중. 최근 4분기 이익이 일회성 비용으로 크게 낮아 현금흐름 내재가치를 계산하지 않았다.')
h = _re0.sub(r'(id="incyFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)
h = _re0.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re0.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")
h = _re0.sub(r'(<div class="verdict-summary-head">[^<]*)<span class="tag">[^<]*</span>', r'\1<span class="tag">Vega 인수 IPR&D 비용 반영 중</span>', h, count=1)
h = _re0.sub(r'<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
h = _re0.sub(r'<div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
"""]


# ── 자동 카드 — 제품별 매출 지도(seg_map_propose 4/5 + 신약 5종을 한 묶음으로 손 작성). 원문 대조: Q3 2026 보도자료 826.5/254.9/235.0/191.0/49.8 = 1,557.2(2026-11-07) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "srt:ProductOrServiceAxis",
 "extra": {},
 "members": {"incy:JAKAFIMember": ["Jakafi(골수섬유증 등, XR 포함)", "#003b71"], "incy:OPZELURAMember": ["Opzelura(피부 크림)", "#d94f2b"],
             "incy:ICLUSIGMember": ["혈액·종양 기타 제품", "#7fa7cf"], "incy:PEMAZYREMember": ["혈액·종양 기타 제품", "#7fa7cf"],
             "incy:MINJUVIMONJUVIMember": ["혈액·종양 기타 제품", "#7fa7cf"], "incy:NIKTIMVOMember": ["혈액·종양 기타 제품", "#7fa7cf"],
             "incy:ZYNYZMember": ["혈액·종양 기타 제품", "#7fa7cf"],
             "us-gaap:RoyaltyMember": ["로열티(Jakavi·Olumiant 등)", "#f2b8a8"], "incy:MilestoneAndContractRevenuesMember": ["마일스톤·계약", "#c9c9c9"]},
 "ignore": ["us-gaap:ProductMember", "incy:JAKAVIRoyaltyRevenuesMember", "incy:OLUMIANTRoyaltyRevenuesMember", "incy:TABRECTARoyaltyRevenuesMember", "incy:OtherProductRoyaltyRevenuesMember"]
}
