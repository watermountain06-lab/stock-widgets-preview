CIK = '0001297996'
BUILD = {'overlay': True, 'no_dcf': '미완성 — 최근 4분기 성과보수·매각 이익 등 일회성 이익이 커서 순 일회성 약 32%'}   # 2026-11-19: O 반복분 규칙 적용 결과 미완성
# DLR(디지털 리얼티) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 12월 31일. 데이터센터 리츠 — 코로케이션·대형(하이퍼스케일) 임대, 세계 300곳 넘는 데이터센터.
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-30 접수, 카드 기준일 11-18 종가), 실적 보도자료(8-K 2.02항 — 모두 장 마감 뒤 16:1x 동부 → 다음 날).
# 요약 자료 누락: SEC companyfacts가 Q2·Q3 2026 10-Q를 싣지 않아 인라인 XBRL 보충(BUILD overlay, preflight OVERLAY_OK)으로 만든다.
# 엔진 입력(2026-11-19): 차입금 = 신용한도·CP $1,640M + 기간 대출 $424M + 선순위 채권 $15,809M + 담보 $1,620M = $19,494M(DEBT_TOTAL_TAG),
#   설비투자 = 부동산 개발·개량 지출(PaymentsToDevelopRealEstateAssets, 9개월 $3.17B — EXTRA_TAGS; 인수·합작 출자 제외), 비지배지분 = 일반 $532M + 임시 자본 $1,596M(Teraco 풋 등), 우선주 $732M.
# 일회성(E54, 금액 기준 — 보충자료 13쪽 FFO→Core FFO 조정표, Codex·Fable r1): 최근 4분기 보통주 순이익 $885.8M(EPS 0.24 + 0.46 + 1.21 + 0.48 = 2.39).
#   이익 $390.9M(매각 이익 59.5·순 성과보수 187.9·기타 비핵심 수익 94.7·환·파생 22.3·기타 26.5 = 44%), 비용 $257.6M(손상 78.6·거래·통합 139.4·퇴직·법무 14.8 등 = 29%).
#   거래·통합·퇴직 비용은 매 분기 나와 반복분(2026-11-19 O 규칙)으로 빼면 비용 $103.4M(12%), 순 일회성 $287.5M = 32.5% → 미완성.
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, -1, 0), '판정 보류'
CO = 'Digital Realty'
S_ = 'https://www.sec.gov/Archives/edgar/data/1297996/'
SEC = S_
TENQ = S_ + '000110465926120710/dlr-20260930x10q.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000110465926120212/dlr-ex99d1.htm', 'q2': S_ + '000110465926086270/dlr-20260723xex99d1.htm',
      'q1': S_ + '000110465926047702/dlr-20260423xex99d1.htm', 'q4': S_ + '000110465926010887/dlr-20260205xex99d1.htm',
      'eur': S_ + '000119312526415815/d106844dex991.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="dlrFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(최근 4분기 EPS에 성과보수 등 일회성 이익이 크다)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (미완성 — 현금흐름 보류)</span>'
Y2 = (0, 50)
ACT_REASON = '리츠라 재고·매출채권 회전으로 보는 활동성이 잘 맞지 않는다'
NONOP_WHAT = '투자'
MODEL_NOTE = ('미완성 카드다. 최근 4분기 EPS($2.39)에는 회사가 FFO·Core FFO·성과보수 제외 Core FFO를 낼 때 빼는 이익이 크게 들어 있다 — 6월 펀드 인수 때 받은 성과보수(순 $188M, 일반 Core FFO에는 포함되고 "성과보수 제외 Core FFO"에서 빠진다), 기타 비핵심 수익 $95M, 부동산 매각 이익 $59M 등 $391M(순이익의 44%). 매 분기 나오는 거래·통합·퇴직·법무 비용을 반복분으로 빼고 나면 순 일회성이 약 32%라 판정을 보류한다. 성과보수가 든 2분기가 최근 4분기에서 빠지는 2027년 2분기 실적(7월 말 예상) 무렵 다시 본다. '
              '리츠는 건물 감가상각이 커서 GAAP 순이익이 실제 현금 창출보다 작게 나오고, 업계는 FFO(순이익에 부동산 감가상각·손상을 되더하고 매각 이익을 뺀 값)와 Core FFO로 본다 — 3분기 Core FFO는 주당 $2.10, 회사의 2026년 성과보수 제외 Core FFO 전망은 $8.30~8.35다. 사이트에는 리츠 전용 평가가 아직 없다. '
              '데이터센터 개발이 본업이라 설비투자에 개발·개량 지출(1~9월 $3.2B, 인수는 제외)을 넣었고, 그래서 FCF가 마이너스라 PCR은 빠진다. 영업이익은 손익계산서 값이다(최근 분기만 소액의 매각손익 포함 — 2025년 4분기 $43M 등). 보통주 배당은 분기 $1.22다. '
              '비지배지분에는 Teraco(남아공) 소수 지분 풋 등 상환 가능 지분 $1.6B가 들어 있고, 성장 자금은 신주·운영 파트너십 유닛·채권(10월 유로 채권 €10억)으로 조달한다.')
HEALTH_EXTRA = '데이터센터 개발 자금을 채권·신주로 조달하는 리츠라 차입금 비중이 높게 나온다.'
PH = ['EQIX', 'AMT', 'CCI', 'PLD', 'O', 'WELL']
PEER_FILE = 'peer_universe/real_estate.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '리츠 6곳 PER 비교 (점수는 S&P500 부동산 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 부동산 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 부동산 대비 배수 순위 (v2/peer_universe/real_estate.json)'
PEER_TIP = ('S&P500 부동산(DLR 제외)과 배수 순위를 매긴 값이다.',
            '물류·의료·쇼핑몰·주택·통신탑 리츠와 부동산 서비스가 섞여 있다. 차트에는 데이터센터·통신탑·대형 리츠 6곳이 보인다.')
# 매출(Q3 2026 10-Q 제품·서비스 축): 임대·기타 서비스 1,827.1 + 수수료·기타 75.3 = 1,902.4.
SEG = [('임대·기타 서비스', 1827.1, '#1f3a5f'), ('수수료·기타', 75.3, '#00a3e0')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 수익 종류별'
NEWS_RANGE = '2026.02 ~ 2026.10'
NEWS = [
    ('neutral', '2026년 10월 29일 장 마감 뒤 — Q3 2026 실적', '2026-10-30',
     '희석 EPS $0.48(1년 전 $0.15) · Core FFO $2.10(1년 전 $1.89) · 신규 계약 연 임대료 역대 최대(지분 100% 기준 $855M, 회사 몫 $627M) — 다음 날 주가 −1.2%', 'q3', 'Digital Realty 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 10월 6일 장 마감 뒤 — 유로 채권 €10억 발행', '2026-10-07',
     '2036년 만기 €10억 채권(이자 5.125%) 가격 확정 — 다음 날 주가 −2.3%', 'eur', 'Digital Realty 보도자료 (SEC 8-K)'),
    ('green', '2026년 7월 23일 장 마감 뒤 — Q2 2026 실적', '2026-07-24',
     '희석 EPS $1.21(펀드 성과보수 포함, 1년 전 $2.94는 매각 이익) · Core FFO $2.65(성과보수 제외 Core FFO $2.13) — 다음 날 주가 +11.0%', 'q2', 'Digital Realty 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 23일 장 마감 뒤 — Q1 2026 실적', '2026-04-24',
     '희석 EPS $0.46(1년 전 $0.27) · Core FFO $2.04(1년 전 $1.77) — 다음 날 주가 0.0%', 'q1', 'Digital Realty 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 5일 장 마감 뒤 — 2025년 연간 실적', '2026-02-06',
     '4분기 희석 EPS $0.24(손상 $79M) · Core FFO $1.86 — 다음 날 주가 +4.2%', 'q4', 'Digital Realty 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Strong Buy', 'n': 34, 'nt': 28, 'mean': 224.54, 'median': 225, 'low': 197, 'high': 250, 'sb': 24, 'b': 5, 'h': 5, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-21'


INCOMPLETE_SHORT = '성과보수 등 일회성 이익이 큼'
INCOMPLETE_WHY = '최근 4분기 EPS($2.39)에 회사가 FFO·Core FFO·성과보수 제외 Core FFO를 낼 때 빼는 이익(2분기 펀드 성과보수 $188M, 기타 비핵심 수익 $95M, 부동산 매각 이익 $59M 등 $391M)이 비용보다 훨씬 커서, 매 분기 반복되는 거래·통합·퇴직 비용을 뺀 순 일회성이 보통주 순이익의 약 32%다 — 배수 판정이 왜곡돼 보류한다. 분기마다 다시 센다'
POST = [r"""
import re as _re0
_w = '최근 4분기 EPS($2.39)에 회사가 FFO·Core FFO·성과보수 제외 Core FFO를 낼 때 빼는 이익(2분기 펀드 성과보수 $188M, 기타 비핵심 수익 $95M, 부동산 매각 이익 $59M 등 $391M)이 비용보다 훨씬 커서, 매 분기 반복되는 거래·통합·퇴직 비용을 뺀 순 일회성이 보통주 순이익의 약 32%다 — 배수 판정이 왜곡돼 보류한다. 분기마다 다시 센다'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — 성과보수 등 일회성 이익이 큼 · 매 분기 재검토</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — 성과보수 등 일회성 이익이 큼. 미완성 카드 규칙에 따라 종합 판정과 함께 현금흐름 내재가치도 보류했다.')
h = _re0.sub(r'(id="dlrFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)
h = _re0.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re0.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")
h = _re0.sub(r'(<div class="verdict-summary-head">[^<]*)<span class="tag">[^<]*</span>', r'\1<span class="tag">성과보수 등 일회성 이익이 큼</span>', h, count=1)
h = _re0.sub(r'<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
h = _re0.sub(r'<div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
"""]
# 배당 칸 — 보통주 배당 태그가 2020년에 멈춰 "없음", 전체 배당·분배 지급액이 우선주 배당으로 표시됐다(Fable·Codex r1)
POST.append(r"""
h = h.replace('<span class="zone-label">우선주 배당 (연초~9/30, 39주)</span>\n          <span class="zone-val">$1.8B</span>', '<span class="zone-label">배당·분배 지급 (연초~9/30, 39주 — 보통주·OP 유닛·우선주 합계, 우선주는 $31M)</span>\n          <span class="zone-val">$1.8B</span>', 1)
h = h.replace('>보통주 배당 없음</span>\n            <span class="zone-val">—</span>', '>분기 배당</span>\n            <span class="zone-val">$1.22</span>', 1)
""")


AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "srt:ProductOrServiceAxis",
 "extra": {},
 "members": {"dlr:RentalAndOtherServicesMember": ["임대·기타 서비스", "#1f3a5f"], "dlr:FeeIncomeAndOtherMember": ["수수료·기타", "#00a3e0"]},
 "ignore": []
}
