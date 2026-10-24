# RSG(리퍼블릭 서비스) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 185. 폐기물 수거·매립·재활용(Group 1·2), 환경 서비스(Group 3 — 2022 US Ecology 인수).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-08-07 장 전 접수), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 모두 장 마감 뒤), StockAnalysis. 사전 조사 자료표 scratchpad pre/RSG.md.
# 엔진 입력(2026-10-23): 차입금 = 1년 안 548 + 장기 13,521 = $14,069M(DEBT_TOTAL_TAG, 금융리스 포함). 4분기 EPS 역산 = 보도자료(2021~2025 같음).
# 세액공제 투자(태양광 등)의 지분법 손실과 그에 따른 낮은 세율로 분기 GAAP EPS가 흔들린다. 상반기 소규모 인수 $860M.
CIK = '0001060391'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, 0, -2), '고평가'
CO = 'Republic Services'
S_ = 'https://www.sec.gov/Archives/edgar/data/1060391/'
SEC = S_
TENQ = S_ + '000106039126000275/rsg-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000106039126000273/exhibit991q22026.htm', 'q1': S_ + '000106039126000210/exhibit991q12026.htm',
      'q4': S_ + '000106039126000093/exhibit991q42025.htm', 'q3': 'https://www.sec.gov/Archives/edgar/data/1060391/000162828025047534/exhibit991q32025.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="rsgFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 40)
ACT_REASON = ''
NONOP_WHAT = '투자'
# 고정 문장(숫자 없음).
MODEL_NOTE = ('세액공제를 받으려고 넣은 투자(태양광 등)는 지분법 손실을 내는 대신 세금을 줄여 준다 — 손실과 세금 혜택이 대부분 상쇄되지만 세전이익과 세율이 함께 출렁여, 영업이익보다 순이익의 움직임이 크다. '
              '2022년 US Ecology(환경 서비스) 대형 인수와 매년 이어지는 작은 인수로 과거 성장에 인수가 섞여 있다. '
              '현금흐름 모델은 인수 지출까지 재투자로 세어 새 매출을 얻는 데 자본이 많이 든다고 보고(매출/자본 효율이 낮다) 약 $14B의 순차입금을 빼므로, FCF에 비해 내재가치가 크게 낮게 나온다. 매립지·환경 충당부채는 따로 빼지 않았다. 세액공제 투자의 가치는 예측기간의 낮은 실효세율로 반영하고 투자 장부가는 비영업 자산으로 더하지 않는다. '
              '10월 22일 상승은 동종사 Waste Connections가 전날 장 마감 뒤 실적과 가이던스 상향을 발표한 다음 날이다(회사 공시 없음).')
PH = ['WM', 'CTAS', 'ROL', 'URI', 'FAST', 'GWW']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '폐기물·산업 서비스 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(RSG 제외)와 배수 순위를 매긴 값이다.',
            '항공·방산·기계·운송·건설이 섞여 있다. 차트에는 폐기물·산업 서비스 6곳만 보인다.')
# 매출(Q2 2026 10-Q 부문, 부문 간 거래 상계 전) — Group 1 2,325 + Group 2 2,180 + Group 3 463 = 4,968, 본사 108·부문 간 상계 −646 → 총매출 4,430.
SEG = [('Group 1(서부 폐기물)', 2325.0, '#003b71'), ('Group 2(동부 폐기물)', 2180.0, '#4f7aa6'), ('Group 3(환경 서비스)', 463.0, '#002448')]
SEG_ADJ = -538.0
SEG_TITLE = '매출 구성 — 부문별(부문 간 거래 상계 전)'
SEG_ADJ_LABEL = '본사·부문 간 거래 상계'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석 — 조정 EPS·가이던스는 쓰지 않는다). 반응일: 실적 8-K 2025-10-31T00:10Z·2026-02-18T02:06Z·05-08T00:10Z·08-07T00:08Z = 전날 장 마감 뒤 → 다음 세션.
# 넣지 않은 8-K: 배당(10/23·2/12·5/7·7/29 인상), 이사(2/12), 정관(2/13), 주총(5/11), 사채(6/23). 다음 실적: 회사 공지 — 10/29 장 마감 뒤.
NEXT_CONFIRMED = {'quarter_end': '2026-09-30', 'date': '2026-10-29', 'src': '회사 공지 — 장 마감 뒤 발표, 콜 오후 5시(동부)'}
NEWS_RANGE = '2025.10 ~ 2026.08'
NEWS = [
    ('green', '2026년 8월 6일 — Q2 2026 실적', '2026-08-07',
     '매출 $4.43B · 순이익 $566M · 희석 EPS $1.84(1년 전 $1.75) — 세액공제 투자 지분법 손실 $58M과 그 세금 혜택 $41M(순효과 주당 약 −$0.05), 연간 가이던스 상향', 'q2', 'Republic Services 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 5월 7일 — Q1 2026 실적', '2026-05-08',
     '매출 $4.11B · 순이익 $525M · 희석 EPS $1.70(1년 전 $1.58)', 'q1', 'Republic Services 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 2월 17일 — Q4 2025 실적', '2026-02-18',
     '매출 $4.14B · 순이익 $545M · 희석 EPS $1.76(1년 전 $1.63, 그 분기 사업 매각 이익 $0.07 포함)', 'q4', 'Republic Services 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 10월 30일 — Q3 2025 실적', '2025-10-31',
     '매출 $4.21B · 순이익 $550M · 희석 EPS $1.76(1년 전 $1.80) — 노사 분규 비용 $56M(EPS −$0.13) 포함, 연간 매출 가이던스 하단', 'q3', 'Republic Services 실적 보도자료 (SEC 8-K)'),
]
# 현금흐름 칸 템플릿 문구 보정(Codex r1, 공통은 안건 E52) — 정적 HTML과 JS 둘 다
POST = [r'''
import re as _re
h = h.replace("어떤 일정 성장률로도 현재가에 닿지 않는다", "연 −50~200% 범위의 일정 성장률(현재 이익률·재투자 가정)로는 현재가에 닿지 않는다")
h = h.replace("`잔존가치(5년 뒤)가 내재가치의 ${Math.round(D.tvShare * 100)}%`", "`잔존가치(5년 뒤)가 부채 차감 전 기업가치의 ${Math.round(D.tvShare * 100)}%`")
h = _re.sub(r'잔존가치\(5년 뒤\)가 내재가치의 ([0-9,]+)%', lambda m: '잔존가치(5년 뒤)가 부채 차감 전 기업가치의 ' + m.group(1) + '%', h)
''']
ANALYST = {'rating': 'Buy', 'n': 27, 'nt': 19, 'mean': 244.95, 'median': 244, 'low': 219, 'high': 272, 'sb': 12, 'b': 3, 'h': 12, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-23'


# ── 자동 카드 — 부문 3개(수동 지도, 상계 전 매출). 원문 대조: Q2 2026 2,325/2,180/463(2026-10-23) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"rsg:Group1SegmentMember": ["Group 1(서부 폐기물)", "#003b71"], "rsg:Group2SegmentMember": ["Group 2(동부 폐기물)", "#4f7aa6"], "rsg:Group3SegmentMember": ["Group 3(환경 서비스)", "#002448"]},
 "ignore": ["rsg:RecyclingAndSolidWasteSegmentsMember"]
}
