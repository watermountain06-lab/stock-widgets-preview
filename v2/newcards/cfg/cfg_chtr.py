CIK = '0001091667'
BUILD = {'no_dcf': '미완성 — Cox 합병 직후·프랜차이즈 손상', 'cover_shares': True}   # 2026-11-07 사용자 결정(미완성 카드). 표지 주식 수 태그가 2016년에 멈춤 — 클래스별 표지 합산
# CHTR(차터 커뮤니케이션즈) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 12월 31일. 미국 케이블(Spectrum) — 초고속 인터넷·모바일·유료 방송·유선 전화, 기업 고객, 광고.
# 출처: SEC XBRL, Q3 2026 10-Q(2026-11-06 12:01 UTC = 07:01 동부 장 전 접수 → 첫 세션 11-06, 카드 기준일 11-06 종가 — 예외 없음),
#        실적 보도자료(8-K 2.02항 — 모두 장 전 07:00 동부 → 그날), Cox·Liberty Broadband 종결 8-K(2026-08-20 17:16 동부 → 다음 날), CFO 교체 8-K(2026-08-31 16:29 동부 → 다음 날).
# 엔진 입력(2026-11-07): 이자비용 InterestIncomeExpenseNonoperatingNet("Interest expense, net" — InterestExpense는 2015-03에 멈춤, fetch_financials CONCEPTS_BY_CIK),
#   주식 수 = 표지 Class A 114,454,220주(+ Class B·C 각 1주 — cover_shares; dei 합계 태그는 2016년에 멈춤). 비지배지분 $18,837M(A/N·Cox 지분 단위 — 2025-12 $4,465M),
#   차입금 = LongTermDebt $107,052M(1년 안 $1,990M 포함) + 기타 단기 $1,180M = $108,232M. EIP 금융 $1,696M(재무상태표 별도 줄, 회사 고유 태그)은 빠짐 — 문장에 밝힘(Codex r1).
#   리스 = 운용리스 $1,442M(2025-12) + 금융리스 $64M(2021-12 낡은 값) — 10-K에만 태깅, 미완성이라 둔다. 부채비율은 총부채 태그가 없어 자산 − 비지배지분 포함 총자본(totalEquity, 2026-11-07 엔진 수정)으로 계산.
#   4분기 EPS는 보도자료 희석 EPS(Q4_EPS_OVERRIDE 2020~2025).
# 일회성(E54 — 미완성이라 판정에 쓰지 않음): Q3 2026 프랜차이즈 손상 $6,326M(세전, 주가 하락이 계기), 채무 교환 이익(보도자료 약 $1.4B, 9개월 소멸 이익 $1,630M).
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 1, 0), '판정 보류'
CO = 'Charter Communications'
S_ = 'https://www.sec.gov/Archives/edgar/data/1091667/'
SEC = S_
TENQ = S_ + '000109166726000073/chtr-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000109166726000072/chtrex991earningsrelease93.htm', 'q2': S_ + '000109166726000051/chtrex991earningsrelease63.htm',
      'q1': S_ + '000109166726000027/chtrex991earningsrelease33.htm', 'q4': S_ + '000109166726000016/chtrex991earningsrelease12.htm',
      'cox': S_ + '000114036126033909/ef20080687_8k.htm', 'cfo': S_ + '000114036126035084/ef20081340_ex99-1.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="chtrFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(Cox 합병 직후 — 최근 4분기 재무가 합병 전후 회사를 섞은 값이고 3분기 프랜차이즈 손상 $6.3B가 이익을 크게 낮춘다)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (-30, 40)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('미완성 카드다. 2026년 8월 19일 Cox Communications의 케이블 사업 인수와 Liberty Broadband 합병을 끝냈다 — Cox에 현금 약 $4.2B($3.5B + $0.72B), 자회사 Charter Holdings의 전환우선 지분 단위(청산우선액 $6.0B, 연 6.875%)와 보통 지분 단위 약 3,360만 단위를 줬고, Liberty Broadband 주주는 1주당 Charter 0.236주를 받았다. '
              '그래서 3분기에는 Cox 실적이 약 6주만 들어 있고 최근 4분기 매출·이익은 합병 전후 회사를 섞은 값이다(회사가 낸 3분기 합병 기준 매출은 $16.5B로 1년 전보다 1.5% 줄었다). 카드의 증가율(매출 +9.1%, 기업 고객 +22.6% 등)은 Cox 몫(종결 뒤 약 6주 $1.4B)을 포함한 보고 기준이라, 기업 고객에서 Cox 기업 매출 $397M을 빼면 +0.9%다. '
              '3분기에 주가 하락을 계기로 한 손상 검사에서 프랜차이즈 손상 $6.3B(세전)를 잡아 영업이익이 −$3.5B, 희석 EPS가 −$20.50이었고, 같은 분기 채무 교환 이익(약 $1.4B)도 있다. 손상을 피한 다른 프랜차이즈 단위도 공정가치가 장부가보다 약 8% 높을 뿐이라 주가가 더 떨어지면 추가 손상이 날 수 있다. GAAP 그대로 둔 최근 4분기 EPS는 손상 때문에 크게 낮아 PER이 높게, EBITDA도 낮게 잡혀 EV/EBITDA가 높게 나온다. '
              'Cox와 Advance/Newhouse는 Charter 주식 대신 Charter Holdings 지분 단위를 갖는다(종결 뒤 재무보고상 보통지분율 Cox 약 21%·A/N 약 9% — 전환우선 지분 전환 전 Charter 몫은 약 70%) — 시가총액은 Class A 주식(약 1.14억 주)만으로 계산하고, 이들 몫은 비지배지분 장부가(3분기 말 $18.8B, 연초 $4.5B — Cox 전환우선 지분 단위 포함)로 EV에 더한다. PSR·PCR은 Class A 시가총액을 연결 매출·연결 FCF 전체로 나눠 그만큼 낮게 나온다. '
              '3분기 자사주 매입은 $19M으로 사실상 멈췄고(1~2분기 $1.8B), Cox는 9월 28일 비례 매입 참여를 중단했다. 차입금은 장부상 약 $108B(장기 $107.1B + 단기 $1.2B)이고, 별도 줄인 단말기 할부채권 담보 차입(EIP 금융, $1.7B)은 회사 고유 태그라 빠져 있다. EV의 리스는 최신 태그 값인 운용리스 $1.44B(2025년 말)와 금융리스 $0.06B(2021년 말)이고, Cox에서 넘어온 리스는 아직 들어 있지 않다. 카드의 FCF는 영업현금흐름 − 설비투자라 회사가 발표하는 FCF(설비투자 미지급금 변동까지 뺌, 3분기 $674M)와 다르다. 합병 뒤 4분기가 쌓이는 2027년 3분기 실적 뒤 정식 판정으로 다시 본다.')
PH = ['CMCSA', 'T', 'VZ', 'TMUS', 'DIS', 'GOOGL']
PEER_FILE = 'peer_universe/communication_services.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '통신·케이블·미디어 6곳 PER 비교 (점수는 S&P500 커뮤니케이션 기준)', 'pbr': '통신·케이블·미디어 PBR 비교', 'psr': '통신·케이블·미디어 PSR 비교',
                'pcr': '통신·케이블·미디어 PCR(FCF) 비교', 'evebitda': '통신·케이블·미디어 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 커뮤니케이션 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 커뮤니케이션 대비 배수 순위 (v2/peer_universe/communication_services.json)'
PEER_TIP = ('S&P500 커뮤니케이션(CHTR 제외)와 배수 순위를 매긴 값이다.',
            '통신·케이블·미디어·인터넷 플랫폼이 섞여 있다. 차트에는 통신·케이블·미디어 6곳만 보인다.')
# 매출(Q3 2026 10-Q 주석 11 상품별): 인터넷 6,395 + 모바일 1,134 + 유료 방송 3,292 + 유선 전화 340 + 기업 고객 2,249 + 광고 460 + 기타 1,052 = 14,922.
SEG = [('인터넷', 6395.0, '#0099d8'), ('모바일', 1134.0, '#1a2a5a'), ('유료 방송', 3292.0, '#7fc8ec'), ('유선 전화', 340.0, '#9aa5c4'),
       ('기업 고객', 2249.0, '#f2a900'), ('광고', 460.0, '#c9c9c9'), ('기타', 1052.0, '#e5e5e5')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 상품별'
# 손 뉴스: 실적 4건 + Cox 종결 + CFO 교체. Q3 2026 실적은 손상·합병이 함께 나와 손 항목으로 쓴다(news_auto 자동 항목은 빠진다 — README 안건 E32).
# 반응일: 실적 8-K 모두 장 전 07:00 동부 → 그날. Cox 종결 8-K 08-20 17:16 동부 → 08-21. CFO 8-K 08-31 16:29 동부 → 09-01.
NEWS_RANGE = '2026.01 ~ 2026.11'
NEWS = [
    ('red', '2026년 11월 6일 장 전 — Q3 2026 실적', '2026-11-06',
     '매출 $14.92B(+9.1%, Cox 약 6주 포함 — 합병 기준 $16.5B로 −1.5%) · 순손실 $2.40B · 희석 EPS −$20.50(1년 전 $8.34) — 프랜차이즈 손상 $6.3B · 합병 기준 인터넷 가입자 23.3만 감소 · 18개월에 걸친 연환산 $2B 비용 절감 계획(Cox 시너지 $1B+와 별도) — 그날 주가 −6.2%', 'q3', 'Charter 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 8월 31일 장 마감 뒤 — CFO 교체', '2026-09-01',
     'Jessica Fischer CFO가 10월 15일 물러나고 회계 책임자 Kevin Howard가 임시 CFO — 다음 날 주가 −4.1%', 'cfo', 'Charter 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 8월 20일 장 마감 뒤 공시 — Cox 케이블 인수·Liberty Broadband 합병 완료(8월 19일)', '2026-08-21',
     'Cox에 현금 약 $4.2B·전환우선 지분 단위 $6.0B·보통 지분 단위 약 33.6M · Liberty Broadband 1주당 Charter 0.236주 — 다음 날 주가 +1.6%', 'cox', 'Charter 공시 (SEC 8-K)'),
    ('red', '2026년 7월 24일 장 전 — Q2 2026 실적', '2026-07-24',
     '매출 $13.53B(−1.7%) · 순이익 $1.29B · 희석 EPS $10.66(1년 전 $9.18) · 인터넷 가입자 17.2만 감소 — 그날 주가 −2.5%', 'q2', 'Charter 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 4월 24일 장 전 — Q1 2026 실적', '2026-04-24',
     '매출 $13.60B(−1.0%) · 순이익 $1.16B · 희석 EPS $9.17(1년 전 $8.42) · 인터넷 가입자 12.0만 감소 — 그날 주가 −25.5%', 'q1', 'Charter 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 1월 30일 장 전 — Q4 2025 실적', '2026-01-30',
     '매출 $13.60B(−2.3%) · 순이익 $1.33B · 희석 EPS $10.34(1년 전 $10.10) · 인터넷 가입자 11.9만 감소 — 그날 주가 +7.6%', 'q4', 'Charter 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 21, 'nt': 14, 'mean': 153.64, 'median': 140, 'low': 101, 'high': 380, 'sb': 5, 'b': 0, 'h': 10, 's': 2, 'ss': 4}
ANALYST_ASOF = '2026-11-07'

# 미완성 카드 표시(2026-11-07 사용자 결정, D·SRE 방식).
INCOMPLETE_SHORT = 'Cox 합병 직후·프랜차이즈 손상'
INCOMPLETE_WHY = '2026년 8월 Cox 케이블 사업을 인수해 최근 4분기 재무가 합병 전후 회사를 섞은 값이고(3분기에 Cox 약 6주), 3분기 프랜차이즈 손상 $6.3B가 GAAP 이익을 크게 낮춰 배수 판정이 왜곡된다. 합병 뒤 4분기가 쌓이는 2027년 3분기 실적 뒤 다시 본다'
POST = [r"""
import re as _re0
_w = '2026년 8월 Cox 케이블 사업을 인수해 최근 4분기 재무가 합병 전후 회사를 섞은 값이고(3분기에 Cox 약 6주), 3분기 프랜차이즈 손상 $6.3B가 GAAP 이익을 크게 낮춰 배수 판정이 왜곡된다. 합병 뒤 4분기가 쌓이는 2027년 3분기 실적 뒤 다시 본다'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — Cox 합병 직후·프랜차이즈 손상</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — Cox 합병 직후·프랜차이즈 손상. 최근 4분기 재무가 합병 전후를 섞어 현금흐름 내재가치를 계산하지 않았다.')
h = _re0.sub(r'(id="chtrFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)
h = _re0.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re0.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")
h = _re0.sub(r'(<div class="verdict-summary-head">[^<]*)<span class="tag">[^<]*</span>', r'\1<span class="tag">Cox 합병 직후·프랜차이즈 손상</span>', h, count=1)
h = _re0.sub(r'<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
h = _re0.sub(r'<div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
"""]


# ── 자동 카드 — 상품별 매출 지도(seg_map_propose 전부 맞음). 원문 대조: Q3 2026 10-Q 주석 11 — 7개 합 14,922(2026-11-07).
#    소계(연결성·주거)와 기업 고객 하위(중소·대기업·Cox 기업)는 겹치므로 뺀다 ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "srt:ProductOrServiceAxis",
 "extra": {},
 "members": {"chtr:ResidentialInternetProductLineMember": ["인터넷", "#0099d8"], "chtr:MobileServiceMember": ["모바일", "#1a2a5a"],
             "chtr:ResidentialVideoProductLineMember": ["유료 방송", "#7fc8ec"], "chtr:ResidentialVoiceProductLineMember": ["유선 전화", "#9aa5c4"],
             "chtr:CommercialProductLineMember": ["기업 고객", "#f2a900"], "chtr:AdvertisingsalesMember": ["광고", "#c9c9c9"], "chtr:OtherServicesMember": ["기타", "#e5e5e5"]},
 "ignore": ["chtr:ConnectivityMember", "chtr:ResidentialProductLineMember", "chtr:CommercialSmallandMediumBusinessProductLineMember",
            "chtr:CommercialEnterpriseProductLineMember", "chtr:CoxCommunicationsBusinessMember"]
}
