CIK = '0001032208'
BUILD = {'no_dcf': '미완성 — SI Partners 지분 매각 종결 대기',   # 2026-11-03 사용자 결정(보류 C군 → 미완성 카드), 2026-11-07 제작
         'overlay': True,   # companyfacts가 Q2·Q3 2026 10-Q를 아직 싣지 않았다(2026-11-07 확인 — 최신 2026-03-31)
         # EV/EBITDA는 뺀다: 매각 예정 부채 안 SI Partners 차입 $9.7B는 EV에서 빠지는데 SI Partners 이익·비지배지분은 남아 있고, 과거 EV는 Series C 우선주 $889M(2021-10~2025)을
         # 담지 못한다(preferred 태그 2018 멈춤). 지분법 투자(Oncor $20.0B)도 빼지 않는다 — 방향이 엇갈려 참고값으로도 쓸 수 없다(Codex r1 필수 2건, Fable r1, 2026-11-07)
         'drop_multiples': ['evebitda']}
# SRE(셈프라) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 12월 31일.
# 사업: Sempra California(SDGE 전력·가스, SoCalGas 가스 — 연결), Sempra Texas(Oncor 지분 80.25% — 지분법, 매출 없음), Sempra Infrastructure(SI Partners 70% — LNG·멕시코, 매각 예정 자산).
# 출처: SEC XBRL(보충 자료 overlay), Q3 2026 10-Q(2026-11-05 16:09 동부 장 마감 뒤), 실적 보도자료(8-K 2.02항 2026-11-05 — 회사 발표는 장 전, 당일 반응),
#        SI Partners 매각 계약 8-K(2025-09-23).
# 미완성 사유: 2025-09-22 SI Partners Class A 지분 45%와 GP 지분을 KKR·CPP Investments에 기본가 $9.99B에 매각 계약(종결 때 현금 $4.65B, 나머지는 2027년 말·7년 뒤 받을 증서·어음).
#   종결되면 Sempra 지분이 70% → 25%가 되어 SI Partners가 연결에서 빠지고 지분법으로 바뀐다 — 매출(Q3 2026 Infrastructure $474M)·매각 예정 자산 $33.6B·부채 $13.1B·비지배지분이 연결에서 사라진다.
#   회사는 Q3 실적(11-05)에서 "앞으로 2주 안" 종결을 예상했고, 매각 이익 $2.0~2.4B(세후, 사후 조정 전)을 추정한다. 지금 재무로 낸 배수가 종결 뒤 회사와 이어지지 않아 판정을 보류한다.
# 엔진 입력(2026-11-07): 매출 RegulatedAndUnregulatedOperatingRevenue, 영업이익은 줄이 없어 합성(DERIVED_OPINC — 세전·지분법 전 이익 + 이자비용 − 이자수익 − 기타 수익 − 매각 이익,
#   Q3 2026 451). 지분법 이익(Q3 2026 $668M = Oncor $462M + SI Partners 몫 Cameron LNG 등 $206M)은 영업이익에 들어가지 않는다. EV/EBITDA는 drop_multiples로 뺐다.
#   차입금 $37,474M = 단기 4,438 + 1년 안 장기·금융리스 1,528 + 장기·금융리스 31,508(SI Partners 차입은 매각 예정 부채 안). 비지배 7,457 + 상환가능 비지배 3,392.
#   총부채는 태그가 없어 overlay_feed SUM(유동 + 장기차입 + 기타 비유동 = 73,848)으로.
# 일회성(E54): 규제 불인정(2026 Q3 −$149M 세후)·SI Partners 매각 예정 세금(2025 Q3 −$514M)·Ecogas 매각 이익(+$97M)·멕시코 환율 등 — 판정 보류라 GAAP 그대로 둔다.
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, 0, 0), '판정 보류'
CO = 'Sempra'
S_ = 'https://www.sec.gov/Archives/edgar/data/1032208/'
SEC = S_
TENQ = S_ + '000103220826000054/sre-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000103220826000051/ex99_1x20260930xearningsta.htm', 'q2': S_ + '000103220826000043/ex99_1x20260630xearningsta.htm',
      'q1': S_ + '000103220826000027/ex99_1x20260331xearningsta.htm', 'q4': S_ + '000103220826000008/ex99_1x20251231xearningsta.htm',
      'q3y': S_ + '000103220825000062/ex99_1x20250930xearningsta.htm', 'oncor': S_ + '000103220826000020/sempra-20260417.htm',
      'deal': S_ + '000103220825000055/sempra-20250922.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="sreFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(SI Partners 지분 매각 종결 대기)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 40)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('미완성 카드다. 2025년 9월 LNG·멕시코 사업을 담은 Sempra Infrastructure Partners(SI Partners) 지분 45%를 KKR·캐나다 연금(CPP Investments)에 기본가 $9.99B(조정 대상)에 팔기로 했다(종결 때 현금 $4.65B, 나머지는 2027년 말 만기 증서와 종결 7년 91일 뒤 만기 어음으로 받는다). '
              '종결되면 Sempra 지분이 70%에서 25%로 줄어 SI Partners가 연결 재무에서 빠지고 지분법 투자로 바뀐다 — 매출·자산·부채·비지배지분이 크게 달라져 지금 재무로 낸 판정이 이어지지 않으므로 판정을 보류한다(자기 이력·동종업 점수는 참고값). '
              '회사는 11월 5일 실적 발표에서 "앞으로 2주 안" 종결을 예상했고, 매각 이익을 세후 $2.0~2.4B(종결 뒤 조정 대상)로, 이와 별도로 거래 부대비용을 세후 $3.25~4.0억으로 추정했다. '
              '이익의 큰 몫은 텍사스 송배전 회사 Oncor(지분 80.25%)에서 지분법 이익으로 들어온다(2026년 3분기 지분법 이익 $668M 중 Oncor $462M, 나머지 $206M은 SI Partners의 Cameron LNG 등). '
              '손익계산서에 영업이익 줄이 없어 세전·지분법 전 이익에 이자비용을 더하고 이자수익·기타 수익·매각 이익을 뺀 합성 값을 쓰는데, 지분법 이익은 여기에 들어가지 않는다. '
              'EV/EBITDA는 이 카드에서 뺐다 — 매각 예정 부채에 묶인 SI Partners 차입($9.7B)이 EV에서 빠지고 지분 투자도 빼지 않아 숫자가 어느 쪽으로 틀렸는지 가릴 수 없다. '
              '유동비율·당좌비율은 SI Partners 매각 예정 자산($33.6B)과 부채($13.1B)가 유동 항목에 들어가 부풀었다 — 둘을 빼면 유동비율은 약 37%다. '
              '현금($34M)도 SI Partners 현금이 매각 예정 자산에 묶여 작게 보이고, 음수인 FCF는 종결 뒤 연결에서 빠질 Sempra Infrastructure 설비투자(2026년 9개월 $4.2B — LNG 건설 등)가 키운 것이다. 차입금($37.5B)·차입금의존도(31.8%)·주당 순현금도 매각 예정 부채에 묶인 SI Partners 차입 $9.7B를 담지 않는다 — 넣으면 차입금의존도는 약 40%다(점수 구간은 같다).')
PH = ['NEE', 'DUK', 'SO', 'AEP', 'XEL', 'PEG']
PEER_FILE = 'peer_universe/utilities.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '유틸리티 6곳 PER 비교 (점수는 S&P500 유틸리티 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 유틸리티 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 유틸리티 대비 배수 순위 (v2/peer_universe/utilities.json)'
PEER_TIP = ('S&P500 유틸리티(SRE 제외)와 배수 순위를 매긴 값이다.',
            '규제 전력·가스, 독립 발전사, 수도가 섞여 있다. 차트에는 규제 전력·가스 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문): Sempra California 2,733 + Sempra Infrastructure 474 − 본사·부문 간 상계 16 = 3,191. Sempra Texas(Oncor)는 지분법이라 매출이 없다.
SEG = [('Sempra California(SDGE·SoCalGas)', 2733.0, '#0d5ba7'), ('Sempra Infrastructure(LNG·멕시코 — 매각 예정)', 474.0, '#e87722')]
SEG_ADJ = -16
SEG_ADJ_LABEL = '본사·부문 간 상계'
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 매각 계약·Oncor 요금 명령 + 실적 5건(GAAP 희석 EPS, 보도자료 직접값). news_auto는 이 카드 매출 태그를 찾지 못해 빈 본문을 냈다(Fable r1) — 모두 손으로.
# 반응일: 실적 보도자료는 장 전 → 같은 날, Oncor 8-K는 2026-04-17 16:18 장 마감 뒤 → 04-20.
NEWS_RANGE = '2025.09 ~ 2026.11'
NEWS = [
    ('red', '2026년 11월 5일 — Q3 2026 실적', '2026-11-05',
     '매출 $3.19B(+1.3%) · 보통주 귀속 이익 $877M · 희석 EPS $1.34(1년 전 $0.12 — 매각 예정 분류 세금 $514M 반영, 조정 EPS는 $1.40 대 $1.11) · CPUC 결정안에 따른 규제 불인정 세후 $149M · 8월 20일 멕시코 가스 배급사 Ecogas 매각 종결(세후·비지배 차감 뒤 이익 $97M) · Oncor 2027~31 투자 계획 약 20% 증액 예고 · 2026 조정 EPS 전망 상단($4.80~5.30) — 당일 주가 −3.7%', 'q3', 'Sempra 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 8월 6일 — Q2 2026 실적', '2026-08-06',
     '매출 $3.00B(−0.1%) · 보통주 귀속 이익 $796M · 희석 EPS $1.21(1년 전 $0.71) — 당일 주가 −0.4%', 'q2', 'Sempra 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 5월 7일 — Q1 2026 실적', '2026-05-07',
     '매출 $3.66B(−3.9%) · 보통주 귀속 이익 $1.04B · 희석 EPS $1.58(1년 전 $1.39) — 당일 주가 −2.2%', 'q1', 'Sempra 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 17일 장 마감 뒤 — Oncor 요금 심사 최종 명령', '2026-04-20',
     '텍사스 규제위원회(PUCT)가 합의안 승인 · 연 수익요구액 약 $6.97B(+$560M, +8.7%) · 자기자본이익률 9.75%(종전 9.70%) · 자본 비율 43.5%(종전 42.5%) — 다음 거래일 주가 −0.7%', 'oncor', 'Sempra 공시 (SEC 8-K)'),
    ('neutral', '2026년 2월 26일 — Q4 2025 실적', '2026-02-26',
     '매출 $3.75B(−0.2%) · 보통주 귀속 이익 $352M · 희석 EPS $0.54 · 2025년 연간 GAAP EPS $2.75(조정 $4.69) — 당일 주가 +0.7%', 'q4', 'Sempra 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 11월 5일 — Q3 2025 실적', '2025-11-05',
     '매출 $3.15B(+13.5%) · 보통주 귀속 이익 $77M · 희석 EPS $0.12(1년 전 $1.00 — SI Partners 매각 예정 분류 세금 $514M, 조정 EPS $1.11) — 당일 주가 −0.1%', 'q3y', 'Sempra 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 9월 23일 — SI Partners 지분 45% KKR 매각 계약', '2025-09-23',
     '기본가 $9.99B(조정 대상, 종결 때 현금 $4.65B) · 매각 뒤 Sempra 지분 25% · 텍사스·캘리포니아 유틸리티 투자 자금 — 당일 주가 +4.5%', 'deal', 'Sempra 공시 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 21, 'nt': 15, 'mean': 99.03, 'median': 99, 'low': 83, 'high': 118, 'sb': 13, 'b': 4, 'h': 4, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-08'


# 미완성 카드 표시(2026-11-03 사용자 결정, AWK·AES 방식 — 대형 지분 매각 종결 대기).
INCOMPLETE_SHORT = 'SI Partners 지분 매각 종결 대기'
INCOMPLETE_WHY = '2025년 9월 LNG·멕시코 사업(SI Partners) 지분 45%를 KKR 등에 팔기로 했다(2026년 11월 종결 예상) — 종결되면 SI Partners가 연결에서 빠져 매출·부채·비지배지분이 크게 바뀌고 지금 재무로 낸 판정이 이어지지 않는다. 종결 뒤 분기가 쌓이면 다시 본다'
POST = [r"""
import re as _re0
_w = '2025년 9월 LNG·멕시코 사업(SI Partners) 지분 45%를 KKR 등에 팔기로 했다(2026년 11월 종결 예상) — 종결되면 SI Partners가 연결에서 빠져 매출·부채·비지배지분이 크게 바뀌고 지금 재무로 낸 판정이 이어지지 않는다. 종결 뒤 분기가 쌓이면 다시 본다'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — SI Partners 지분 매각 종결 대기</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — SI Partners 지분 매각 종결 대기. 매각 뒤 재무가 크게 바뀌어 현금흐름 내재가치를 계산하지 않았다.')
h = _re0.sub(r'(id="sreFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)
h = _re0.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re0.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")
h = _re0.sub(r'(<div class="verdict-summary-head">[^<]*)<span class="tag">[^<]*</span>', r'\1<span class="tag">SI Partners 지분 매각 종결 대기</span>', h, count=1)
h = _re0.sub(r'<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
h = h.replace('합성 영업이익률(세전이익 기준)', '합성 영업이익률(세전이익 − 영업외 손익)').replace('합성 영업이익(세전이익 기준)', '합성 영업이익(세전이익 − 영업외 손익)')
h = _re0.sub(r'(<div class="verdict-summary-head">[^<]*?), 영업이익률 ', r'\1, 합성 영업이익률 ', h, count=1)
h = h.replace("label:'OPM(%)'", "label:'합성 OPM(%)'", 1)
h = _re0.sub(r'<div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
"""]


# ── 자동 카드 — 부문 지도(손 작성). 원문 대조: Q3 2026 10-Q California 2,733 + Infrastructure 474 − 본사·상계 16 = 3,191(2026-11-07) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RegulatedAndUnregulatedOperatingRevenue"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"sre:SempraCaliforniaMember": ["Sempra California(SDGE·SoCalGas)", "#0d5ba7"],
             "sre:SempraInfrastructureMember": ["Sempra Infrastructure(LNG·멕시코 — 매각 예정)", "#e87722"]},
 "ignore": []
}
