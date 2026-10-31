# LNT(얼라이언트 에너지) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 아이오와(IPL)·위스콘신(WPL) 규제 전력·가스, 부문 2개 + 기타(비규제).
# 출처: SEC XBRL + 인라인 XBRL 보충(BUILD overlay — companyfacts에 Q2·Q3 10-Q가 없다), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 장 마감 뒤 18시 발표 → 다음 날 반응), StockAnalysis. 사전 조사 scratchpad pre/LNT.md.
# 엔진 입력(2026-10-30): 차입금 = CP $704M + 기타 단기(텀론) $400M + 1년 안 장기부채 $374M + 장기 $11,085M = $12,563M(DEBT_TOTAL_TAG, CP 줄 없는 날짜는 ShortTermBorrowings 튜플), 단기투자 없음(2025-09 $250M 한 번뿐 — EV_TAGS_BY_CIK sti 빈 목록).
# Q3 10-Q가 10/30 11:21 장중 접수 — 가격은 10/30 장중. Q4 2021·2025 EPS는 보도자료 값(Q4_EPS_OVERRIDE). 풍력·태양광 세액공제로 실효세율이 음수다.
# 일회성: 최근 4분기 GAAP 3.58 대 회사 조정 약 3.58(Q4 2025 비규제 자산 평가 손실 −0.05, Q1 2026 주 세금 재측정 +0.05 — 순 0).
BUILD = {'overlay': True}   # SEC 요약 자료에 Q2·Q3 2026 10-Q가 없다 — 원문 인라인 XBRL 보충
CIK = '0000352541'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, -1, -2), '고평가'
CO = 'Alliant Energy'
S_ = 'https://www.sec.gov/Archives/edgar/data/352541/'
SEC = S_
SEC0 = S_ + '000'   # 보도자료 8-K 중 세 건은 제출 대리인 접수 번호(0001104659-…)
TENQ = S_ + '000035254126000047/lnt-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000035254126000045/lnt102920268-kex991.htm', 'q2': S_ + '000035254126000042/lnt073020268-kex991.htm',
      'q1': S_ + '000035254126000030/lnt043020268-kex991.htm', 'q4': S_ + '000035254126000005/lnt021920268-kex991.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="lntFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 30)
ACT_REASON = '유틸리티라 재고·매출채권 회전으로 보는 활동성이 잘 맞지 않는다'
NONOP_WHAT = '투자'
MODEL_NOTE = ('전력망·발전 설비 투자(9개월 $1.8B, 2027~2030년 $15.9B 계획)가 감가상각보다 훨씬 커서, 큰 차입금(약 $12.6B)을 뺀 현금흐름 모델의 값이 0 아래로 나온다 — 규제 유틸리티는 그 투자가 요금 기준 자산이 되어 이익으로 돌아오는 구조라 현금흐름 모델과 PCR은 의미가 약하다. '
              '풍력·태양광 세액공제로 법인세가 음수(세금 이익)이고, 3분기 EPS $1.52에는 연말까지 되돌아갈 법인세 시점 차이가 들어 있다(회사 설명). 현금흐름 모델의 설비투자는 2023-09 최근 4분기 값($1.8B, 최신은 약 $2.6B)이고 비영업 투자는 중복으로 $1,066M(원문 $794M)이 들어가 있다 — 둘 다 고치면 값이 더 낮아지는 쪽이라 판정은 같다. Q2·Q3 10-Q가 SEC 요약 자료에 아직 없어 원문 인라인 XBRL로 채웠다. 가격은 10/30 장중 값이다.')
HEALTH_EXTRA = '설비투자 자금을 사채·신주로 조달하는 구조라 차입금 비중이 높게 나온다 — 규제 유틸리티에서는 흔한 모습이다.'
# 현금흐름 0 이하 — SO·ATO와 같은 문구 보정(0 이하가 아니면 바뀌지 않는다)
POST = [r'''
_R = '현금흐름 모델의 주당 지분가치가 0 이하라(큰 차입금을 뺀 뒤) 기본 시나리오 환산 성장률은 해석할 수 없다.'
_pairs = [
 ("fill('[data-dcf-basev]', '$' + (Math.abs(D.base) < 10 ? D.base.toFixed(2) : Math.round(D.base)));",
  "fill('[data-dcf-basev]', '$' + (Math.abs(D.base) < 10 ? D.base.toFixed(2) : Math.round(D.base)));\n  if (D.base <= 0) { const _rv = document.querySelector('#dcf .reverse'); if (_rv) _rv.textContent = _XR; }"),
 ("const tv = D.tvShare != null ? `잔존가치(5년 뒤)가 내재가치의 ${Math.round(D.tvShare * 100)}%` : '';",
  "const tv = D.base <= 0 ? '잔존가치 비중 — 내재가치가 0 이하라 의미 없음' : (D.tvShare != null ? `잔존가치(5년 뒤)가 내재가치의 ${Math.round(D.tvShare * 100)}%` : '');"),
 ("`현재가 $${price.toFixed(2)} 가 정당화되려면 5년 내내`\n          + ` 연 ${(d.requiredGrowth*100).toFixed(1)}% 매출 성장이 필요하다.`)",
  "(d.base <= 0 ? _XR : `현재가 $${price.toFixed(2)} 가 정당화되려면 5년 내내`\n          + ` 연 ${(d.requiredGrowth*100).toFixed(1)}% 매출 성장이 필요하다.`))"),
]
for _x, _y in _pairs:
    if _x in h:
        h = h.replace(_x, _y)
if 'const _XR' not in h:
    h = h.replace('<script>', '<script>\nconst _XR = ' + repr(_R) + ';', 1)
import re as _re
h = _re.sub(r'잔존가치\(5년 뒤\)가 내재가치의 [0-9,]+%', '잔존가치 비중 — 내재가치가 0 이하라 의미 없음', h)
h = _re.sub(r'(id="lntDcfReq"[^>]*>)연 -[0-9.]+%', lambda m: m.group(1) + '해석 부적합', h)
h = _re.sub(r'현재가를 정당화하려면 매출이 5년간 연 [−-][0-9.]+% 커야 한다\. ', '현금흐름 값이 0 이하라 현재가 요구 성장률은 해석할 수 없다. ', h)
''']
# 헤더 '현재가 요구 성장' 칸 — 현금흐름 값이 0 이하이면 숫자 대신 '해석 부적합'(AEE Fable r1, 2026-10-25)
POST.append(r'''
h = h.replace("  if (req && price != null) {", "  if (req && d.base <= 0) { req.textContent = '해석 부적합'; req.style.color = 'var(--text3)'; const _c = req.closest('.meta-item'); if (_c) _c.title = '해석 부적합(현금흐름 0 이하) — 현금흐름 내재가치가 0 이하라 현재가 요구 성장률을 해석할 수 없다.'; }\n  if (req && price != null && d.base > 0) {", 1)
import re as _re2
h = _re2.sub(r'(id="lntDcfReq"[^>]*>)연 [−-][0-9.]+%', lambda m: m.group(1) + '해석 부적합', h)
''')
PH = ['NEE', 'SO', 'DUK', 'AEP', 'XEL', 'AEE']
PEER_FILE = 'peer_universe/utilities.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '유틸리티 6곳 PER 비교 (점수는 S&P500 유틸리티 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 유틸리티 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 유틸리티 대비 배수 순위 (v2/peer_universe/utilities.json)'
PEER_TIP = ('S&P500 유틸리티(LNT 제외)와 배수 순위를 매긴 값이다.',
            '규제 전력·가스, 독립 발전사, 수도가 섞여 있다. 차트에는 유틸리티 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문) — IPL 664 + WPL 595 + 기타 26 = 1,285.
SEG = [('IPL(아이오와)', 664, '#00548c'), ('WPL(위스콘신)', 595, '#8cc63f'), ('기타(비규제)', 26, '#5b6770')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'   # 분기는 fill.py가 실제 값으로 붙인다 — 손으로 적으면 분기를 넘길 때 두 번 나온다(2026-10-30)
NEWS_RANGE = '2026.02 ~ 2026.10'
NEWS = [
    ('green', '2026년 10월 29일 장 마감 뒤 — Q3 2026 실적', '2026-10-30',
     '매출 $1.29B(+6.2%) · 순이익 $398M · 희석 EPS $1.52(1년 전 $1.09) · 2026 조정 EPS 전망 3.41~3.46으로 좁힘 · 2027~2030 설비투자 $15.9B — 다음 날 장중 +2.2%', 'q3', 'Alliant Energy 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 7월 30일 장 마감 뒤 — Q2 2026 실적', '2026-07-31',
     '매출 $0.97B(+1.0%) · 순이익 $170M · 희석 EPS $0.65(1년 전 $0.68) — 다음 날 주가 −0.2%', 'q2', 'Alliant Energy 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 30일 장 마감 뒤 — Q1 2026 실적', '2026-05-01',
     '매출 $1.18B(+5.0%) · 순이익 $224M · 희석 EPS $0.87(1년 전 $0.83) — 주 세금 재측정 이익 주당 $0.05 포함 — 다음 날 주가 +0.9%', 'q1', 'Alliant Energy 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 19일 장 마감 뒤 — Q4 2025 실적', '2026-02-20',
     '매출 $1.06B(+9.0%) · 순이익 $142M · 희석 EPS $0.55(1년 전 $0.58) · 2025년 EPS $3.14 — 다음 날 주가 +1.4%', 'q4', 'Alliant Energy 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 14, 'nt': 9, 'mean': 75.94, 'median': 75, 'low': 68, 'high': 83, 'sb': 6, 'b': 2, 'h': 6, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-30'


# ── 자동 카드 — 원문 대조: Q3 2026 664/595/26(2026-10-30) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"lnt:IplMember": ["IPL(아이오와)", "#00548c"], "lnt:WplMember": ["WPL(위스콘신)", "#8cc63f"], "us-gaap:AllOtherSegmentsMember": ["기타(비규제)", "#5b6770"]},
 "ignore": []
}
