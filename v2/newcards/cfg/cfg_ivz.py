BUILD = {'no_dcf': '미완성 — 일회성 비용 처리 대기'}   # 2026-11-03 사용자 결정 — 미완성 카드(판정 보류)
# IVZ(인베스코) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 12월 31일. 자산운용 — ETF(QQQ 등)·뮤추얼펀드·대체투자, 단일 보고 부문. 버뮤다 법인.
# 출처: SEC XBRL, Q3 2026 10-Q(2026-11-03 장중 접수 → 기준일 11-04 종가), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 장 전 07시 동부 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/IVZ.md. 비교군 asset_managers(2026-10-25 등록).
# 엔진 입력(2026-11-04): 순이익은 NetIncomeLossAvailableToCommonStockholdersBasic("Net income attributable to Invesco Ltd." = 우선주 배당·재매입 비용 뒤 보통주 몫, EXTRA_TAGS — NetIncomeLoss는 2025-03 멈춤, 기본 대체 ProfitLoss는 순이익률 −1.15%로 틀렸다).
# 현금 $965.5M·차입 $1,281.3M은 회사 몫(CIP 현금 $772.8M·CIP 차입 $7,919.6M은 차원 값이라 안 섞임), 우선주 $2,510.5M, 비지배 $701.6M + 상환가능 $297.0M(모두 CIP 몫, BEN처럼 둘 다 둠 — Fable r1), 운용리스 $406.7M(10-K 총액), 단기투자 없음(2018 멈춘 태그 — EV_TAGS_BY_CIK).
# 기말 뒤: 2026-10-26 우선주 $1.5B를 12.5% 프리미엄에 재매입하고 같은 금액을 5년 기한부대출로 조달 — 9월 말 재무상태표에는 없다(Q4 2026에 재매입 비용 약 $187.5M이 보통주 몫에서 빠질 예정).
# 미완성 사유(E54): Q4 2025 무형자산 손상 세전 $1,794.9M(세후 $1,367.9M, 주당 3.01)로 최근 4분기 GAAP EPS −0.69라 PER 해당 없음(A3), EV/EBITDA 0점. 손상을 빼면 동종업이 기권(배수 2개)에서 +1(89.6, PER 12.7이 돌아옴)로 바뀌고,
# 자기는 현재값만 바꾸면 28.3·재매입 비용 $80.7M까지 30.2·이력 창까지 바꾸면 32.6으로 −1/0이 방식에 따라 갈린다(Codex·Fable r1). 현금흐름은 이력 마진까지 정리해도 기본 약 $13(2년 중앙 17.2%, 비율 2.3) — −2 유지.
# 보류 전 점수: 자기 18.7(PER 빠짐)·동종 95.5(유효 배수 PBR·PSR 2개라 기권)·현금흐름 −2. 등록해도 A3가 GAAP 순이익률로 PER을 빼므로 eps_oneoff만으로는 PER이 안 돌아온다(Fable r1).
CIK = '0000914208'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, None, 0), '판정 보류'
CO = 'Invesco'
S_ = 'https://www.sec.gov/Archives/edgar/data/914208/'
SEC = S_
TENQ = S_ + '000091420826000376/ivz-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000091420826000370/ivzpressrelease3q2026.htm', 'q2': S_ + '000091420826000229/ivzpressrelease2q2026.htm', 'q1': S_ + '000091420826000102/ivzpressrelease1q2026.htm', 'q4': S_ + '000091420826000017/ivzpressrelease4q2025.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="ivzFairBand" title="최근 4분기 EPS가 무형자산 손상으로 적자라 PER 구간으로 낸 적정주가가 의미 없어 표시하지 않는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {pct(HIST[\'margin_now\'])})</span>'
Y2 = (0, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('미완성 카드다. 2025년 4분기 무형자산 손상($1.8B)으로 최근 4분기 이익이 적자라 PER을 쓸 수 없고, 손상을 빼면 PER이 돌아와 동종업 칸이 기권에서 표를 던지는 쪽으로 바뀌고, 자기 이력 칸도 계산 방식에 따라 바뀐다. '
              '연결 재무제표에 회사가 운용하는 펀드(CIP — 자산 $10.7B, 차입 $7.9B)가 섞여 있어 현금·차입은 회사 몫만 썼다. 2026년 10월 26일 우선주 $1.5B를 프리미엄 12.5%에 사들이고 같은 금액을 5년 대출로 빌렸다 — 9월 말 숫자에는 아직 없다. '
              '2025년 12월 QQQ가 개방형 ETF로 바뀌어 운용보수가 늘고 판매 수수료가 줄었으므로 1년 전 매출과 성격이 다르다. 비교 종목은 S&P500 자산운용·수탁은행 12곳 중 IVZ를 뺀 11곳이다.')
PH = ['BLK', 'TROW', 'BEN', 'AMP', 'NTRS', 'STT']
PEER_FILE = 'peer_universe/asset_managers.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '자산운용 6곳 PER 비교 (점수는 S&P500 자산운용·수탁은행 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 자산운용·수탁은행 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 자산운용·수탁은행 대비 배수 순위 (v2/peer_universe/asset_managers.json)'
PEER_TIP = ('S&P500 자산운용·수탁은행 12곳 중 IVZ를 뺀 11곳과 배수 순위를 매긴 값이다.',
            '전통 운용사·대체투자사·수탁은행이 섞여 있다. 차트에는 6곳만 보인다.')
# 매출(Q3 2026 10-Q, srt:ProductOrServiceAxis) — 1,512.2 + 313.2 + 2.0 + 45.8 = 1,873.2.
SEG = [('운용보수', 1512.2, '#000ab4'), ('판매·서비스 수수료', 313.2, '#4a63d6'), ('성과보수', 2.0, '#9fb0ee'), ('기타', 45.8, '#8a96a3')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 항목별(Q3 2026)'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석, 순이익은 보통주 몫). 반응일: 장 전 발표(07시 동부) → 같은 날.
NEWS_RANGE = '2026.01 ~ 2026.10'
NEWS = [
    ('red', '2026년 10월 27일 장 전 — Q3 2026 실적·우선주 재매입', '2026-10-27',
     '매출 $1.87B(+14.2%) · 순이익 $295M · 희석 EPS $0.65(1년 전 $0.66, 전년 세금 환입 포함) · 조정 EPS $0.72 · 우선주 $1.5B 재매입·5년 대출 $1.5B — 당일 주가 −0.4%', 'q3', 'Invesco 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 7월 28일 장 전 — Q2 2026 실적', '2026-07-28',
     '매출 $1.83B(+20.5%) · 순이익 $345M · 희석 EPS $0.76(1년 전 −$0.03, 우선주 재매입 비용) · 조정 EPS $0.71 — 당일 주가 −2.3%', 'q2', 'Invesco 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 4월 28일 장 전 — Q1 2026 실적', '2026-04-28',
     '매출 $1.74B(+14.1%) · 순이익 $230M · 희석 EPS $0.51(1년 전 $0.38) · 조정 EPS $0.57 — 당일 주가 +1.5%', 'q1', 'Invesco 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 1월 27일 장 전 — Q4 2025 실적', '2026-01-27',
     '매출 $1.69B(+6.2%) · 순손실 $1,186M · 희석 EPS −$2.61(무형자산 손상 $1.8B, 주당 −3.01) · 조정 EPS $0.62 — 당일 주가 −5.1%', 'q4', 'Invesco 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 15, 'nt': 11, 'mean': 35.68, 'median': 36, 'low': 29.5, 'high': 41, 'sb': 4, 'b': 2, 'h': 9, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-04'


# 미완성 카드 표시(2026-11-03 사용자 결정 — C·D·E 보류 카드는 있는 자료로 만들고 판정 보류 + 이유를 잘 보이게, SPCX 방식). BUILD no_dcf가 판정을 보류로 만들고, 보험사용 문구를 미완성 사유로 바꾼다.
INCOMPLETE_SHORT = '일회성 비용 처리 대기'
INCOMPLETE_WHY = '2025년 4분기 무형자산 손상($1.8B)으로 최근 4분기 EPS가 적자라 PER을 쓸 수 없고, 손상을 빼면 동종업 칸이 기권에서 표를 던지는 쪽으로 바뀌고 자기 이력 표도 계산 방식에 따라 갈린다 — 일회성 처리 규칙(안건 E54)이 정해질 때까지 보류'
POST = [r"""
_w = '2025년 4분기 무형자산 손상($1.8B)으로 최근 4분기 EPS가 적자라 PER을 쓸 수 없고, 손상을 빼면 동종업 칸이 기권에서 표를 던지는 쪽으로 바뀌고 자기 이력 표도 계산 방식에 따라 갈린다 — 일회성 처리 규칙(안건 E54)이 정해질 때까지 보류'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — 일회성 비용 처리 대기</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — 일회성 비용 처리 대기. 현금흐름 내재가치는 계산하지 않았다.')
import re as _re3
h = _re3.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re3.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")   # 툴팁이 '계산 불가 — 미완성 — …'로 겹쳤다(Codex 2026-11-03)
"""]


# ── 자동 카드 — 부문(축 하나만 붙은 값). 원문 대조: Q3 2026 1,512.2/313.2/2.0/45.8(2026-11-04) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "srt:ProductOrServiceAxis",
 "extra": {},
 "members": {"us-gaap:InvestmentAdviceMember": ["운용보수", "#000ab4"], "us-gaap:DistributionAndShareholderServiceMember": ["판매·서비스 수수료", "#4a63d6"], "us-gaap:InvestmentPerformanceMember": ["성과보수", "#9fb0ee"], "us-gaap:FinancialServiceOtherMember": ["기타", "#8a96a3"]},
 "ignore": []
}
