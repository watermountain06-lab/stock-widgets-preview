CIK = '0000051434'
BUILD = {'no_dcf': '미완성 — 두 번의 영업권 손상(EMEA)으로 최근 4분기 GAAP가 적자'}   # 2026-11-08 사용자 규칙(D군 — 일회성이 GAAP를 적자로 만들면 미완성)
# IP(인터내셔널 페이퍼) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 12월 말. 골판지 포장 북미(PS NA)·EMEA(PS EMEA, 2025-01 DS Smith 인수).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-11-04 16:52 동부 장 마감 뒤 → 11-05, 카드 기준일 11-06 종가), 실적 보도자료(8-K 2.02항 — 모두 장 전 06:1x~07:4x 동부 → 그날),
#        GCF(셀룰로스 섬유) 매각 완료(2026-01-23 16:06 동부 → 01-26), 두 회사 분리 계획(2026-01-29 실적과 같은 날).
# 엔진 입력(2026-11-08): 영업이익 줄이 없어 세전이익 − 순이자로 합성(DERIVED_OPINC), 차입금 $9,691M(1년 안 2,203 + 장기 7,488, 금융리스 $97M 포함 — DEBT_TOTAL_TAG; VIE 비소구 금융부채 $2,132M은 대응 금융자산이 있어 뺀다), 현금 $815M.
#   EPS 이력은 중단사업(GCF) 포함 총 EPS — 계속사업 EPS와 다르다(Q3 2026 총 −2.13, 계속 −2.07).
# 일회성(E54): 최근 4분기 계속사업 GAAP 희석 EPS −6.43(−4.48 + 0.14 − 0.02 − 2.07) 대 회사 조정 영업 EPS 0.48(−0.08 + 0.15 + 0.04 + 0.37).
#   Q4 2025 PS EMEA 영업권 손상 $2,467M(세후 $2,196M)·구조조정 $162M, Q3 2026 PS EMEA 영업권 손상 $1,377M(세후 같음)·EMEA 분리 비용 $65M → GAAP를 적자로 만든다.
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, 0, 0), '판정 보류'
CO = 'International Paper'
S_ = 'https://www.sec.gov/Archives/edgar/data/51434/'
SEC = S_
TENQ = S_ + '000005143426000154/ip-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000005143426000147/nextgenip-20260930ex991.htm', 'q2': S_ + '000005143426000115/nextgenip-20260630ex991.htm',
      'q1': S_ + '000005143426000067/nextgenip-20260331ex991.htm', 'q4': S_ + '000005143426000016/nextgenip-20251231ex991.htm',
      'q3p': S_ + '000005143425000068/nextgenip-20250930ex991.htm', 'gcf': S_ + '000162828026003279/bluebellclosingpr.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="ipFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(최근 4분기 GAAP가 영업권 손상으로 적자)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (-50, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('미완성 카드다. 이 카드는 일회성이 최근 4분기 GAAP 이익을 적자로 만들면 판정을 보류하는데, IP는 EMEA 사업의 영업권 손상이 두 번 잡혀 최근 4분기 계속사업 GAAP 희석 EPS가 −$6.43이다(회사 조정 영업 EPS는 $0.48). '
              '2025년 4분기에 DS Smith 인수로 생긴 EMEA 영업권 $2.47B(비현금)를, 2026년 3분기에 다시 $1.38B를 손상 처리했고, 구조조정(80/20 전략에 따른 공장 정리)·EMEA 분리 비용이 이어졌다. '
              '손상을 빼도 본업 이익은 얇다 — 조정 영업 EPS가 최근 4분기 합계 $0.48에 그치고(분기 −0.08 → 0.15 → 0.04 → 0.37로 3분기에 개선), 2026년 3분기 잉여현금흐름은 −$267M였다. 다만 북미 부문 영업이익은 1년 전 −$166M에서 2분기 $204M, 3분기 $427M로 올라왔다. '
              '회사는 2026년 1월 북미와 EMEA를 두 상장사로 나누겠다고 밝혔고(12~15개월 목표, 과세 스핀오프 등 구조·시점은 미확정, EMEA 쪽은 11월 3일 런던에서 투자자 설명회), 같은 달 셀룰로스 섬유(GCF) 사업을 AIP에 $1.5B(우선주 $190M 포함)에 팔았다. '
              '북미에서는 5월 Delmarva에서 델라웨어 Dover 상자 공장($95M)을, 6월 NORPAC 제지 공장(워싱턴주 롱뷰, $362M)을 인수했다. Pine Hill 공장(앨라배마)은 지붕 피해로 3분기 중 가동을 멈췄다가 예상보다 일찍 재가동했다. 회사는 북미 부문 2026년 영업이익을 $1.3~1.4B로 제시하고, 분리를 앞둔 EMEA 전망은 더 내지 않기로 했다. '
              '카드의 EPS·순이익은 중단사업(GCF) 손익을 포함한 총액이고(2026년 3분기 −$2.13, 계속사업만은 −$2.07), 영업이익 줄이 손익계산서에 없어 계속사업 세전이익에 순이자를 더한 합성 영업이익을 쓴다 — 비영업 연금 손익이 들어 있어 회사의 부문 영업이익과 다르다. 2023년부터는 GCF를 뺀 재작성 값이지만 2021~2022년 매출은 GCF를 포함해, 5년 성장률·PSR 이력은 사업 범위가 바뀐 구간이 섞여 있다. 최근 4분기 GAAP가 적자라 PER 숫자는 나오지 않으며, 평가와 평균에서 뺀다. 두 손상 분기가 최근 4분기에서 모두 빠지는 것은 2027년 3분기 실적 때다 — 2027년 1월 말 실적 때 2025년 4분기 손상은 빠지지만 2026년 3분기 손상($1.38B)이 남는다. 그 뒤로도 분기마다 GAAP 흑자 회복 여부를 다시 본다. 다만 EMEA 분리가 끝나면 두 손상이 중단사업으로 재작성돼 계속사업 GAAP가 흑자로 돌아설 수 있어, 그 경우 분리 뒤 첫 실적에서 다시 본다. Q3 2026 10-Q는 옛 DS Smith 전산 통제 결함을 내부통제의 중대한 약점으로 판정했다(공시 통제 비유효, 분리 뒤 해소 예정). 신용등급은 S&P BBB(안정적)·Moody’s Baa2(부정적 전망)이다. 미국 골판지 가격 담합 집단소송(2025년 7월 제소)과 이탈리아 고객 손해배상 청구가 진행 중이다.')
PH = ['PKG', 'SW', 'AMCR', 'BALL', 'AVY']
PEER_FILE = 'peer_universe/materials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '포장재 5곳 PER 비교 (점수는 S&P500 소재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 소재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 소재 대비 배수 순위 (v2/peer_universe/materials.json)'
PEER_TIP = ('S&P500 소재(IP 제외)와 배수 순위를 매긴 값이다.',
            '화학·금속·건자재가 섞여 있다. 차트에는 포장재 5곳만 보인다.')
# 매출(Q3 2026 10-Q 주석 매출 표): 북미 3,880 + EMEA 2,280 + 본사·부문 간 37 = 6,197.
SEG = [('포장 북미(PS NA — 골판지 상자·원지)', 3880.0, '#003a70'), ('포장 EMEA(PS EMEA — DS Smith)', 2280.0, '#6cace4')]
SEG_ADJ = 37
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 실적 5건 + GCF 매각 완료. 반응일: 실적 8-K 장 전 → 그날, GCF 매각 장 마감 뒤 → 다음 거래일. 색은 사건 성격, 수치는 그날 주가.
NEWS_RANGE = '2025.10 ~ 2026.10'
NEWS = [
    ('red', '2026년 10월 28일 장 전 — Q3 2026 실적', '2026-10-28',
     '매출 $6.20B · 계속사업 희석 EPS −$2.07(EMEA 영업권 손상 $1.38B) · 조정 영업 EPS $0.37 · 잉여현금흐름 −$267M · EMEA 전망 제시 중단 — 그날 주가 +3.3%', 'q3', 'International Paper 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 7월 30일 장 전 — Q2 2026 실적', '2026-07-30',
     '매출 $6.00B · 계속사업 희석 EPS −$0.02 · 조정 영업 EPS $0.04 · NORPAC 공장 인수 · 연간 조정 EBITDA 전망 $3.20~3.40B로 낮춤 — 그날 주가 +1.2%', 'q2', 'International Paper 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 4월 30일 장 전 — Q1 2026 실적', '2026-04-30',
     '매출 $5.97B · 계속사업 희석 EPS $0.14 · 조정 영업 EPS $0.15 · GCF 매각 대금으로 차입금 $660M 상환 · 연간 조정 EBITDA 전망 $3.5~3.7B → $3.20~3.50B 하향(겨울 폭풍·투입비 상승) — 그날 주가 −9.4%', 'q1', 'International Paper 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 1월 29일 장 전 — 2025년 연간 실적 · 두 회사 분리 계획', '2026-01-29',
     '4분기 계속사업 희석 EPS −$4.48(EMEA 영업권 손상 $2.47B) · 조정 영업 EPS −$0.08 · 북미·EMEA 두 상장사로 분리 계획(12~15개월) — 그날 주가 −6.0%', 'q4', 'International Paper 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 1월 23일 장 마감 뒤 — GCF 사업 매각 완료', '2026-01-26',
     '셀룰로스 섬유(GCF) 사업을 AIP에 $1.5B(우선주 $190M 포함)에 매각 완료 — 다음 거래일 주가 −0.1%', 'gcf', 'International Paper 공시 (SEC 8-K)'),
    ('red', '2025년 10월 30일 장 전 — Q3 2025 실적', '2025-10-30',
     '계속사업 손실 $426M(공장 폐쇄 가속 감가상각 $675M) · GCF를 중단사업으로 분류 — 그날 주가 −12.7%', 'q3p', 'International Paper 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 11, 'nt': 8, 'mean': 43.5, 'median': 45, 'low': 35, 'high': 51, 'sb': 6, 'b': 4, 'h': 1, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-08'

# 파이프라인 자동 재판정용 — 일회성이 든 분기(결산일: 항목).
ONEOFF_QUARTERS = {'2025-12-31': 'PS EMEA 영업권 손상 $2,467M(세후 $2,196M) · 구조조정 $162M',
                   '2026-09-30': 'PS EMEA 영업권 손상 $1,377M · EMEA 분리 비용 $65M'}

# 미완성 카드 표시(2026-11-08 사용자 규칙, D·SRE 방식).
INCOMPLETE_SHORT = '영업권 손상으로 GAAP 적자'
INCOMPLETE_WHY = '최근 4분기 GAAP 이익이 EMEA 영업권 손상 두 번($2.47B·$1.38B)으로 적자다 — 배수 판정이 왜곡돼 보류한다. 판정 재개는 이르면 2027년 11월(2027년 3분기 실적) 뒤'
POST = [r"""
import re as _re0
_w = '최근 4분기 GAAP 이익이 EMEA 영업권 손상 두 번($2.47B·$1.38B)으로 적자다 — 배수 판정이 왜곡돼 보류한다. 판정 재개는 이르면 2027년 11월(2027년 3분기 실적) 뒤'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — 영업권 손상으로 GAAP 적자 · 판정 재개 이르면 2027년 11월(EMEA 분리가 끝나면 앞당겨질 수 있음)</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — 영업권 손상으로 GAAP 적자. 미완성 카드 규칙에 따라 종합 판정과 함께 현금흐름 내재가치도 보류했다.')
h = _re0.sub(r'(id="ipFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)
h = _re0.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re0.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")
h = _re0.sub(r'(<div class="verdict-summary-head">[^<]*)<span class="tag">[^<]*</span>', r'\1<span class="tag">영업권 손상으로 GAAP 적자</span>', h, count=1)
h = _re0.sub(r'<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
h = _re0.sub(r'<div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
# 영업권 손상이 섞인 합성 영업이익률을 Bear·체크포인트 근거로 쓰지 않는다(CRL Fable r1과 같은 처리)
_b1 = '<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">마진</span><span class="bb-text">최근 4분기 영업이익률 −14.2%(영업적자).</span></div>'
assert _b1 in h
h = h.replace(_b1, '<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">이익</span><span class="bb-text">영업권 손상을 빼도 회사 조정 영업 EPS는 최근 4분기 합계 $0.48로 얇다.</span></div>', 1)
_c2 = h[h.index('<strong style="color:var(--accent2);">②</strong>'):]; _c2 = _c2[:_c2.index('</div>')]
assert '합성 영업이익률' in _c2
h = h.replace(_c2, '<strong style="color:var(--accent2);">②</strong> 북미 부문 영업이익이 회사 4분기 전망 $460~500M 안에 드는지(직전 Q3 2026 $427M) — 합성 영업이익률은 영업권 손상이 섞여 비교에 쓰지 않는다', 1)
h = h.replace('영업이익률 −17.7%(1년 전 −9.5%).', '영업이익률 −17.7%(1년 전 −9.5%, 각각 영업권 손상 $1.38B·공장 폐쇄 가속 감가상각 $675M 포함).', 1)
h = h.replace('다음 확인 포인트 · 2027년 1월 28일 무렵 (예상) Q4 2026 실적 공시.', '다음 확인 포인트 · 2027년 1월 28일 무렵 (예상) Q4 2026 실적 공시 — 이때도 2026년 3분기 손상($1.38B)이 남아 판정은 보류된다.', 1)
_bu = '<div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">—</span><span class="bb-text">기준을 넘는 강세 지표가 없다.</span></div>'
assert _bu in h
h = h.replace(_bu, '<div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">부문</span><span class="bb-text">북미 부문 영업이익 Q3 2026 $427M(1년 전 −$166M, 전분기 $204M), 4분기 전망 $460~500M.</span></div>', 1)
h = h.replace('<span class="bb-text">Q3 2026 매출 −0.4%(보고 기준, 3년 연평균 7.5%).', '<span class="bb-text">Q3 2026 매출 −0.4%(보고 기준, 3년 연평균 7.5%는 2025년 1월 DS Smith 인수 포함).', 1)
_bb = '<span class="zone-label">자사주 매입 (연초~9/30, 39주)</span>\n          <div style="display:flex;align-items:center;gap:8px;">\n            <span class="zone-val">$31M</span>'
assert _bb in h
h = h.replace(_bb, _bb.replace('<span class="zone-val">$31M</span>', '<span class="zone-val" style="font-size:13px;">매입 프로그램 집행 없음 · 주식보상 원천징수 $31M</span>'), 1)
"""]

# ── 자동 카드 — 부문 지도(seg_map_propose 뒤 원문 대조). 원문: Q3 2026 10-Q 3,880 + 2,280 + 37 = 6,197 ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"ip:PackagingSolutionsNorthAmericaSegmentMember": ["포장 북미(PS NA — 골판지 상자·원지)", "#003a70"],
             "ip:PackagingSolutionsEMEASegmentMember": ["포장 EMEA(PS EMEA — DS Smith)", "#6cace4"]}
}
