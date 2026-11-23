CIK = '0001751788'
BUILD = {'overlay': True, 'no_dcf': '미완성 — 최근 4분기 GAAP가 적자(영업권 손상·연금 정산·Sadara 보증 충당·구조조정 등 특별 항목)'}   # 2026-11-07·08 사용자 규칙(GAAP 적자면 미완성)
# DOW(다우) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 12월 말. 포장·특수 플라스틱(폴리에틸렌), 산업 중간재·인프라, 성능 소재·코팅(실리콘·아크릴).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-23 접수, 카드 기준일 11-17 종가), 실적 보도자료(8-K 2.02항 — 모두 장 전 06~07시 동부 → 그날), CEO 교체 8-K(2026-04-14 장 전 → 그날).
# 엔진 입력(2026-11-18): 영업이익 = 세전이익 + 이자비용 − 이자수익(DERIVED_OPINC — 영업이익 줄 없음), 차입금 = 1년 안 + 장기(DEBT_TOTAL_TAG), 설비투자 새 태그(EXTRA_TAGS — 2026년 2분기부터), Q4 2025 EPS −2.15(보도자료).
# 일회성(E54): 최근 4분기 GAAP 희석 EPS −1.28(−2.15 − 0.74 + 0.99 + 0.62) — 적자라 미완성. 회사 운영 EPS 1.67(−0.34 − 0.14 + 1.44 + 0.71).
#   회사 특별 항목(세후 주당): Q4 2025 1.81(영업권 손상 0.93·자산 손상 0.42·연금 정산 0.36·구조조정 0.10), Q1 0.60(Sadara 보증 충당 0.31·세금 0.21·Transform to Outperform 0.09 등), Q2 0.45(Transform to Outperform 0.58·구조조정 0.09 − 세금 환입 0.21 등), Q3 0.09.
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 1, 0), '판정 보류'
CO = 'Dow'
NI_TAGS = ['NetIncomeLossAvailableToCommonStockholdersBasic']   # 분기 순이익: NetIncomeLoss 태그는 4분기(10-K) 값이 비어 차트가 멈췄다 — 보통주 귀속(Q3 2026 454, Q4 2025 −1,534)
S_ = 'https://www.sec.gov/Archives/edgar/data/1751788/'
SEC = S_
TENQ = S_ + '000175178826000160/dow-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000175178826000155/exhibit991enrschedules3q26.htm', 'q2': S_ + '000175178826000144/exhibit991enrschedules2q26.htm',
      'q1': S_ + '000175178826000131/exhibit991enrschedules1q26.htm', 'q4': S_ + '000175178826000011/exhibit991enrschedules4q25.htm',
      'ceo': S_ + '000119312526153769/d103960d8k.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="dowFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(최근 4분기 GAAP가 적자다)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (미완성 — 현금흐름 보류)</span>'
Y2 = (-30, 30)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('미완성 카드다. 이 카드는 최근 4분기 GAAP 이익이 적자이거나 일회성이 30% 이상이면 판정을 보류하는데, DOW는 최근 4분기 GAAP 희석 EPS가 −$1.28로 적자다. 회사가 조정에서 빼는 특별 항목이 주당 $2.95로 크다 — 2025년 4분기 폴리우레탄·건설화학 영업권 손상($690M)·자산 손상·연금 정산, 2026년 1분기 Sadara(사우디 합작) 보증 충당($292M), 2분기 비용 절감 계획 Transform to Outperform($526M) 등이다. 회사 운영 EPS로는 최근 4분기 $1.67이다. '
              '분기마다 GAAP 흑자 여부와 특별 항목 비중을 다시 센다. 2027년 1월 말(예상) 실적에서는 손상이 든 2025년 4분기가 빠지고(그 분기 GAAP EPS가 −$0.87보다 높으면 최근 4분기 흑자), 4월 말에는 Sadara 충당이 든 1분기가, 7월 말에는 구조조정 비용이 큰 2분기가 빠진다. 4월 창에서는 1분기 세금 비용과 같은 건(Nova 판결금)의 2분기 세금 환입만 남아 순액이 낮아 보일 수 있다. 30% 아래가 되는지는 새 분기 실적과 새 특별 항목에 달렸다(구조조정 계획은 2027년 말까지). '
              '이익은 업황에 크게 기대 있다 — 2025년 가격 하락으로 적자였다가 2026년 중동 분쟁에 따른 공급 차질로 폴리에틸렌 가격이 오르며 2분기 운영 EPS $1.44로 회복했고 3분기에는 $0.71로 반쯤 낮아졌다. 회사도 가격 상승이 이어진다고 보장하지 않아 2026년 마진을 평소 수준으로 보면 안 된다. 2026년 1분기부터 Sadara(사우디 합작) 지분법 손실 인식을 멈춰(장부상 의무가 한도에 닿음) 그만큼 2026년 이익이 좋아 보이지만, Sadara 관련 현금 지출은 계속된다. 최근 4분기 FCF($2.2B)에는 3월에 받은 Nova Chemicals 판결금(캐나다달러 $1.4B)이 들어 있다. 7월 1일 Karen S. Carter가 CEO에 올랐고 Jim Fitterling은 Executive Chair(이사회 의장)로 남았다. '
              '손익계산서에 영업이익 줄이 없어 카드는 세전이익에 이자비용을 더하고 이자수익을 빼서 영업이익으로 쓴다(지분법·기타 손익 포함 — 회사 운영 EBIT와 다르다). 설비투자는 2026년 2분기부터 새 태그로만 공시돼 그 태그로 이었다. 순현금에는 시장성 증권 $558M이 빠져 있다(요약 자료에 단독 태그가 없다). 순이익 칸은 참가증권 배분 뒤 보통주 몫이라 손익계산서 귀속 순이익과 몇백만 달러 다를 수 있다.')
PH = ['LYB', 'DD', 'LIN', 'APD', 'PPG', 'ECL']
PEER_FILE = 'peer_universe/materials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '화학 6곳 PER 비교 (점수는 S&P500 소재 기준)', 'pbr': '화학 PBR 비교', 'psr': '화학 PSR 비교',
                'pcr': '화학 PCR(FCF) 비교', 'evebitda': '화학 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 소재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 소재 대비 배수 순위 (v2/peer_universe/materials.json)'
PEER_TIP = ('S&P500 소재(DOW 제외)와 배수 순위를 매긴 값이다.',
            '화학·산업용 가스·금속·건자재·포장재가 섞여 있다. 차트에는 화학 회사 6곳만 보인다.')
# 매출(Q3 2026 보도자료 부문): 포장·특수 플라스틱 5,778 + 산업 중간재·인프라 3,058 + 성능 소재·코팅 2,250 + 본사 181 = 11,267.
SEG = [('포장·특수 플라스틱(폴리에틸렌)', 5778, '#e80033'), ('산업 중간재·인프라', 3058, '#2b2b2b'), ('성능 소재·코팅(실리콘·아크릴)', 2250, '#f28aa0')]
SEG_ADJ = 181
SEG_ADJ_LABEL = '본사·기타'
SEG_TITLE = '매출 구성 — 사업 부문별'
# 손 뉴스: 실적 4건 + CEO 교체. 반응일: 모두 장 전 → 그날.
NEWS_RANGE = '2026.01 ~ 2026.10'
NEWS = [
    ('green', '2026년 10월 22일 장 전 — Q3 2026 실적', '2026-10-22',
     'GAAP 희석 EPS $0.62 · 운영 EPS $0.71(1년 전 −$0.19) · FCF $1.1B — 그날 주가 +4.7%', 'q3', 'Dow 보도자료 (SEC 8-K)'),
    ('green', '2026년 7월 23일 장 전 — Q2 2026 실적', '2026-07-23',
     'GAAP 희석 EPS $0.99(Transform to Outperform 비용 $526M 포함) · 운영 EPS $1.44(1년 전 −$0.42) — 그날 주가 −1.1%', 'q2', 'Dow 보도자료 (SEC 8-K)'),
    ('red', '2026년 4월 23일 장 전 — Q1 2026 실적', '2026-04-23',
     'GAAP 주당 손실 $0.74(Sadara 보증 충당 $292M) · 운영 EPS −$0.14 — 그날 주가 −0.7%', 'q1', 'Dow 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 14일 장 전 — CEO 교체 발표', '2026-04-14',
     'Karen S. Carter를 7월 1일자 CEO로 선임, Jim Fitterling은 이사회 의장으로 — 그날 주가 −2.4%', 'ceo', 'Dow 8-K'),
    ('red', '2026년 1월 29일 장 전 — 2025년 연간 실적', '2026-01-29',
     '4분기 GAAP 주당 손실 $2.15(폴리우레탄·건설화학 영업권 손상 $690M·연금 정산 등) · 운영 EPS −$0.34 — 그날 주가 −2.2%', 'q4', 'Dow 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 20, 'nt': 13, 'mean': 34.31, 'median': 33, 'low': 30, 'high': 40, 'sb': 4, 'b': 1, 'h': 14, 's': 1, 'ss': 0}
ANALYST_ASOF = '2026-11-23'

ONEOFF_QUARTERS = {'2025-12-31': '1.81 — 영업권 손상 0.93 · 자산 손상 0.42 · 연금 정산 0.36 · 2025 구조조정 0.10',
                   '2026-03-31': '0.60 — Sadara 보증 충당 0.31 · 세금 항목 0.21 · Transform to Outperform 0.09 · 구조조정 0.02 · 소송 −0.03',
                   '2026-06-30': '0.45 — Transform to Outperform 0.58 · 구조조정 0.09 · 세금 항목 −0.21 · 기타 −0.01',
                   '2026-09-30': '0.09 — Transform to Outperform 0.08 · 구조조정 0.03 · 채무 조기 상환 0.06 · 소송 −0.08'}

INCOMPLETE_SHORT = 'GAAP 적자·특별 항목이 큼'
INCOMPLETE_WHY = '최근 4분기 GAAP EPS가 적자(−$1.28)이고 회사가 조정에서 빼는 특별 항목(영업권 손상·연금 정산·Sadara 보증 충당·구조조정 등)이 주당 $2.95라 배수 판정이 왜곡돼 보류한다. 분기마다 다시 세고, 주요 재검토는 2027년 1월 말·4월 말·7월 말(예상) 실적 — 손상·충당·구조조정이 든 분기가 차례로 빠질 때'
POST = [r"""
import re as _re0
_w = '최근 4분기 GAAP EPS가 적자(−$1.28)이고 회사가 조정에서 빼는 특별 항목(영업권 손상·연금 정산·Sadara 보증 충당·구조조정 등)이 주당 $2.95라 배수 판정이 왜곡돼 보류한다. 분기마다 다시 세고, 주요 재검토는 2027년 1월 말·4월 말·7월 말(예상) 실적 — 손상·충당·구조조정이 든 분기가 차례로 빠질 때'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — GAAP 적자·특별 항목이 큼 · 매 분기 재검토, 주요 확인 2027년 1월 말부터</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — GAAP 적자·특별 항목이 큼. 미완성 카드 규칙에 따라 종합 판정과 함께 현금흐름 내재가치도 보류했다.')
h = _re0.sub(r'(id="dowFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)
h = _re0.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re0.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")
h = _re0.sub(r'(<div class="verdict-summary-head">[^<]*)<span class="tag">[^<]*</span>', r'\1<span class="tag">GAAP 적자·특별 항목이 큼</span>', h, count=1)
h = _re0.sub(r'<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
h = _re0.sub(r'<div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
# Fable r1: 약세 줄의 합성 영업이익에는 특별 항목(세전 약 $2.5B)이 들어 있다
h = _re0.sub(r'(<span class="bb-head">마진</span><span class="bb-text">최근 4분기[^<]*?)\.?(</span>)', lambda m: m.group(1) + ' — 손상·충당 등 특별 항목(세전 약 $2.5B) 포함, 회사 운영 EBIT로는 약 6.4%.' + m.group(2), h, count=1)
h = _re0.sub(r'(<span class="bb-head">부채</span><span class="bb-text">순차입금[^<]*?)\.?(</span>)', lambda m: m.group(1) + ' — 특별 항목 때문에 영업이익이 작게 잡힌 값이다(회사 운영 EBIT로는 약 5배).' + m.group(2), h, count=1)
"""]

AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"dow:PackagingSpecialtyPlasticsMember": ["포장·특수 플라스틱(폴리에틸렌)", "#e80033"], "dow:IndustrialIntermediatesInfrastructureMember": ["산업 중간재·인프라", "#2b2b2b"], "dow:PerformanceMaterialsCoatingsMember": ["성능 소재·코팅(실리콘·아크릴)", "#f28aa0"]},
 "ignore": ["us-gaap:CorporateMember"]
}
