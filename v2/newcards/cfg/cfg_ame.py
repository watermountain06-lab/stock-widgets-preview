# AME(아메텍) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 178. 전자 계측기(EIG)·전기기계(EMG) — 틈새 산업 기술 회사를 인수로 키운다.
# 출처: SEC XBRL, Q2 2026 10-Q(2026-08-04 장중 접수), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 보도자료는 장 전, 8:30 콜), 8-K(인수 합의·완료), StockAnalysis.
# 엔진 입력(2026-10-23): 차입금 = 1년 안 980.6 + 장기 1,055.5 = $2,036M(DEBT_TOTAL_TAG — 기본은 장기만), 이자비용 InterestExpenseNonoperating(CONCEPTS_BY_CIK).
# Indicor Instrumentation $5.0B 현금 인수 8/26 완료(연매출 약 $1.1B, CP·텀론 차입) — Q2 뒤라 숫자에 없음. First Aviation 인수 5/26 완료.
CIK = '0001037868'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, -1, -2), '고평가'
CO = 'AMETEK'
S_ = 'https://www.sec.gov/Archives/edgar/data/1037868/'
SEC = S_
TENQ = S_ + '000103786826000175/ame-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000103786826000173/ametek8kexhibit99108042026.htm', 'q1': S_ + '000103786826000141/ametek8kexhibit99104302026.htm',
      'q4': S_ + '000103786826000006/ametek8kexhibit99102032026.htm', 'q3': S_ + '000103786825000075/ametek8kexhibit991103025.htm'}
LINKS = {'indicor': S_ + '000103786826000191/exhibit-991indicorinstrume.htm', 'indicor_deal': S_ + '000103786826000146/exhibit-991projectivy5626.htm'}
FAIRBAND_TITLE = 'id="ameFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 40)
ACT_REASON = ''
NONOP_WHAT = '투자'
# 고정 문장(숫자 없음).
MODEL_NOTE = ('인수로 성장해 온 회사라 과거 성장률에는 인수가 섞여 있고, 인수한 회사의 무형자산 상각 때문에 GAAP 이익이 회사가 발표하는 조정 이익보다 작다. '
              '현금흐름 모델은 인수로 산 성장의 비용을 매출/투하자본 비율(영업권·무형자산이 커서 낮다)로 떼어, 새 매출마다 큰 재투자를 빼므로 모델 FCF가 실제 영업현금흐름보다 훨씬 작다 — 내재가치가 현재가보다 크게 낮게 나오는 이유다. '
              '8월에 끝낸 Indicor Instrumentation 인수(현금 $5.0B, 텀론·리볼버 차입으로 조달)는 기준 분기 뒤라 숫자에 없다 — 차입금·순차입금은 6월 말 기준이라 현재가 기준 EV에도 인수 뒤 늘어난 차입이 빠져 있고, 다음 분기부터 매출과 차입금이 함께 크게 늘어난다.')
PH = ['PH', 'ETN', 'EMR', 'ROK', 'DOV', 'FTV']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '산업 기술·자동화 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(AME 제외)와 배수 순위를 매긴 값이다.',
            '항공·방산·기계·운송·건설이 섞여 있다. 차트에는 산업 기술·자동화 6곳만 보인다.')
# 매출(Q2 2026 10-Q 부문) — 전자 계측기(EIG) 1,321.2 + 전기기계(EMG) 723.2 = 2,044.4(= 총매출). 1년 전 1,159.6·618.5.
SEG = [('전자 계측기(EIG)', 1321.153, '#003a70'), ('전기기계(EMG)', 723.244, '#4f79a8')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석 — 조정 EPS·가이던스는 쓰지 않는다), 인수 합의·완료.
# 반응일: 실적 보도자료 장 전(8:30 콜) — 8-K 접수 2025-10-30T14:59Z·2026-02-03T19:05Z·04-30T16:00Z·08-04T13:56Z(모두 장중) → 같은 날.
# Indicor 합의 5/6 보도자료(8-K 18:32Z 장중) → 5/6, 완료 보도자료 8/26 16:30 동부(8-K 20:42Z, 장 마감 뒤) → 8/27(Codex·Fable r1).
# 다음 실적: 10/15 회사 공지 — 11/3 장 전 발표, 8:30 콜.
NEXT_CONFIRMED = {'quarter_end': '2026-09-30', 'date': '2026-11-03', 'src': '10/15 회사 공지 — 장 시작 전 발표, 콜 오전 8시 30분(동부)'}
# 넣지 않은 8-K: 배당 인상(2/12), 임원·이사(11/10·5/8), 주총(5/11), 신용약정(6/12), CP 한도 증액(8/11), First Aviation 합의·완료(4/30·5/26 — 작은 인수).
NEWS_RANGE = '2025.10 ~ 2026.08'
NEWS = [
    ('neutral', '2026년 8월 26일 — Indicor Instrumentation 인수 완료', '2026-08-27',
     '계측기 사업군을 현금 $5.0B에 인수 마무리(장 마감 뒤 발표) — 연매출 약 $1.1B, 2026년 매출 기여 약 $350M 예상, 텀론·리볼버 차입으로 조달', 'indicor', 'AMETEK 보도자료 (SEC 8-K)'),
    ('green', '2026년 8월 4일 — Q2 2026 실적', '2026-08-04',
     '매출 $2.04B(+15%, 유기 +10%·인수 +5%) · 희석 EPS $1.77(1년 전 $1.55)', 'q2', 'AMETEK 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 5월 6일 — Indicor Instrumentation 인수 합의', '2026-05-06',
     'Indicor의 계측기 사업군을 현금 약 $5.0B에 인수 합의(연매출 약 $1.1B)', 'indicor_deal', 'AMETEK 보도자료 (SEC 8-K)'),
    ('green', '2026년 4월 30일 — Q1 2026 실적', '2026-04-30',
     '매출 $1.93B(+11%) · 희석 EPS $1.74(1년 전 $1.52)', 'q1', 'AMETEK 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 3일 — Q4 2025 실적', '2026-02-03',
     '매출 $2.0B(+13%) · 희석 EPS $1.73(1년 전 $1.67)', 'q4', 'AMETEK 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 10월 30일 — Q3 2025 실적', '2025-10-30',
     '매출 $1.89B(+11%) · 희석 EPS $1.60(1년 전 $1.47)', 'q3', 'AMETEK 실적 보도자료 (SEC 8-K)'),
]
# 인수 전 재무 표시 보정(Codex·Fable r1): Bull 부채 문장과 매출 증가율에 기준을 붙인다
POST = [r'''
import re as _re
h, _n = _re.subn(r'(순차입금\(리스 포함\) \$[0-9.]+B, 최근 4분기 영업이익의 [0-9.]+배)\.', r'\1(6월 말, $5.0B Indicor 인수 차입 전).', h)
assert _n == 1, _n
h, _n = _re.subn(r'(Q2 2026 매출 \+15\.0%\(보고 기준)', r'\1 — 유기 +10%·인수 +5%', h)
assert _n == 1, _n
''']
ANALYST = {'rating': 'Buy', 'n': 20, 'nt': 14, 'mean': 280.14, 'median': 285, 'low': 230, 'high': 316, 'sb': 12, 'b': 2, 'h': 5, 's': 1, 'ss': 0}
ANALYST_ASOF = '2026-10-23'


# ── 자동 카드 — 부문 2개(수동 지도). 원문 대조: Q2 2026 1,321.2/723.2(2026-10-23) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"ame:ElectronicInstrumentsGroupMember": ["전자 계측기(EIG)", "#003a70"], "ame:ElectromechanicalGroupMember": ["전기기계(EMG)", "#4f79a8"]},
 "ignore": []
}
