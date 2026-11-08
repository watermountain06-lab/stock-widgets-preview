CIK = '0000827052'
BUILD = {'no_dcf': '미완성 — Eaton 산불 손실 추정 불가'}   # 2026-11-07 사용자 결정(D군 → 미완성 카드: 추정 불가한 산불 책임)
# EIX(에디슨 인터내셔널) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 12월 31일. 남부 캘리포니아 규제 전력(SCE) + 지주회사.
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-29 16:08 동부 장 마감 뒤 → 첫 세션 10-30, 카드 기준일 11-06 종가), 실적 보도자료(8-K 2.02항 — 모두 장 마감 뒤 16:0x 동부 → 다음 날).
# 엔진 입력(2026-11-07): 차입금 $41,596M, 비지배지분 = SCE 우선주 $1,564M(MinorityInterestAmountRepresentedByPreferredStock — EV_TAGS_BY_CIK, 없으면 0),
#   EIX 우선주 Series B $83M(preferred), 단기투자는 2010년 낡은 값이라 뺐다. 4분기 EPS는 역산 그대로 — 보도자료 주당 이익은 기본 EPS(Q4 2025 $4.80·Q4 2024 $0.88)라 희석 역산(4.78·0.89 — 보도자료 각주 희석 4.79·0.87과 1센트 차)과 기준이 다르다.
# 일회성: 최근 4분기 기본 EPS 9.45(4.80 + 1.38 + 1.39 + 1.88) 대 회사 핵심 EPS 6.75(1.87 + 1.42 + 1.54 + 1.92) — 비핵심 2.70, 대부분 Q4 2025(Woolsey 합의 비용 회수 등 2.93).
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, 1, 0), '판정 보류'
CO = 'Edison International'
S_ = 'https://www.sec.gov/Archives/edgar/data/827052/'
SEC = S_
TENQ = S_ + '000082705226000073/eix-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000082705226000072/eix-2026x0930exx991.htm', 'q2': S_ + '000082705226000058/eix-2026x0730exx991.htm',
      'q1': S_ + '000082705226000041/eix-2026x0428exx991.htm', 'q4': S_ + '000082705226000010/eix-2026x02x18exx991.htm',
      'deck': S_ + '000082705226000075/a10eixoctober2026busines.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="eixFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(Eaton 산불 손실을 추정할 수 없고, 최근 4분기 이익에 큰 일회성 회수 이익이 들어 있다)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 60)
ACT_REASON = '유틸리티라 재고·매출채권 회전으로 보는 활동성이 잘 맞지 않는다'
NONOP_WHAT = '투자'
MODEL_NOTE = ('미완성 카드다. 2025년 1월 로스앤젤레스 카운티 Eaton 산불에 대해 2026년 8월 LA 카운티 소방국·CAL FIRE 보고서가 SCE의 전기를 끊고 놀리던 송전 설비에서 생긴 아크가 발화 원인이라고 결론 냈고, 회사도 자사 설비가 관련됐을 가능성이 높다고 본다. '
              '10-Q는 추가로 중대한 손실이 생길 가능성이 높지만 그 규모는 아직 추정할 수 없다고 적었다(2026년 10월 소송 약 2,000건·개인 원고 약 3만 8천 명, 대표 배심 재판 2027년 1·5·9월 예정). '
              '2026년 9월까지 피해자 보상 프로그램 등 합의 손실 $1.8B를 계상했고 대부분을 고객 부담으로 조성한 자가보험($917M)·캘리포니아 산불기금($859M)·FERC 관할 전력요금($70M)으로 회수할 것으로 봐 세후 순비용은 $9M이다. '
              '자가보험 $1.0B는 2026년 2월 소진됐고, 이후 적격 피해 보상은 산불기금이 대신 낸다(기금 관리자는 Eaton 산불에 최소 $21B를 쓸 수 있다고 밝힘). 규제당국이 비용을 부당하다고 판정하면 SCE가 기금에 갚아야 하는데, 안전 인증이 있어 고의·중과실이 아니면 상한이 약 $4.3B다. '
              '벌금·과징금은 보험·기금·요금으로 회수할 수 없고, LA 카운티 지방검사의 형사 수사도 진행 중이다. '
              '최근 4분기 GAAP 이익에는 2025년 4분기 Woolsey 산불 합의 비용 회수 같은 일회성 이익이 커서, 보도자료 기준 최근 4분기 기본 EPS 합계(약 $9.45)가 회사 핵심 EPS 합계(약 $6.75)보다 약 $2.70 높다 — 카드 PER은 희석 EPS(약 $9.40)로 계산해 핵심 이익 기준보다 낮게 보이고, 2025년 4분기의 높은 영업이익률도 이 회수 효과 때문이다. 회사는 2026년 핵심 EPS 전망 $5.90~6.20을 유지했다. '
              '자기 이력·동종업 점수는 참고값이고 판정은 보류한다. SCE 우선주($1.6B)는 비지배지분으로 EV에 더한다. 손실 규모가 추정되거나 소송이 정리되면 정식 판정으로 다시 본다.')
PH = ['PCG', 'SRE', 'XEL', 'AEP', 'DUK', 'PNW']
PEER_FILE = 'peer_universe/utilities.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '유틸리티 6곳 PER 비교 (점수는 S&P500 유틸리티 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 유틸리티 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 유틸리티 대비 배수 순위 (v2/peer_universe/utilities.json)'
PEER_TIP = ('S&P500 유틸리티(EIX 제외)와 배수 순위를 매긴 값이다.',
            '전력·가스·수도 회사가 섞여 있다. 차트에는 서부·대형 전력 6곳만 보인다.')
SEG = [('SCE(남부 캘리포니아 전력)', 4887.0, '#00664f')]
SEG_ADJ = -1
SEG_ADJ_LABEL = '지주회사·연결 조정'
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 실적 3건. 최신 Q3 2026(10-29 장 마감 뒤)은 news_auto가 붙인다. 반응일: 실적 8-K 장 마감 뒤 16:0x 동부 → 다음 날.
NEWS_RANGE = '2026.02 ~ 2026.10'
NEWS = [
    ('red', '2026년 8월 31일 — 주가 급락', '2026-08-31',
     '그날 주가 −23.1%(직전 거래일 8월 28일에도 −4.8%) — 회사 8-K는 없다. 같은 8월 LA 카운티 소방국·CAL FIRE의 Eaton 산불 조사 보고서가 SCE 설비를 발화 원인으로 결론 냈고, 캘리포니아 의회 정기 회기가 산불 책임 제도 개혁 없이 끝났다(10월 회사 설명 자료)', 'deck', 'Edison International 10-Q·설명 자료 (SEC)'),
    ('neutral', '2026년 7월 30일 장 마감 뒤 — Q2 2026 실적', '2026-07-31',
     '순이익 $534M · 주당 $1.39(1년 전 $0.89) · 핵심 EPS $1.54(1년 전 $0.97) — 실적은 1년 전보다 좋았지만 다음 날 주가 −6.8%', 'q2', 'Edison International 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 28일 장 마감 뒤 — Q1 2026 실적', '2026-04-29',
     '순이익 $531M · 주당 $1.38(1년 전 $3.73) · 핵심 EPS $1.42(1년 전 $1.37) — 다음 날 주가 +0.0%', 'q1', 'Edison International 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 18일 장 마감 뒤 — Q4 2025 실적', '2026-02-19',
     '순이익 $1,848M · 주당 $4.80(1년 전 $0.88, Woolsey 합의 비용 회수 등 일회성 이익 포함) · 핵심 EPS $1.87(1년 전 $1.05) — 다음 날 주가 +4.2%', 'q4', 'Edison International 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 17, 'nt': 12, 'mean': 58.67, 'median': 62, 'low': 42, 'high': 67, 'sb': 2, 'b': 1, 'h': 10, 's': 0, 'ss': 4}
ANALYST_ASOF = '2026-11-08'

# 미완성 카드 표시(2026-11-07 사용자 결정, D·SRE 방식).
INCOMPLETE_SHORT = 'Eaton 산불 손실 추정 불가'
INCOMPLETE_WHY = '회사는 2025년 1월 Eaton 산불에 자사 설비가 관련됐을 가능성이 높다고 보고 있고, 추가로 중대한 손실이 생길 가능성이 높지만 규모를 추정할 수 없다(10-Q) — 최근 4분기 이익에도 큰 일회성 회수 이익이 들어 있어 배수 판정이 의미를 갖기 어렵다. 손실 규모가 추정되거나 합의가 마무리되면 다시 본다'
POST = [r"""
import re as _re0
_w = '회사는 2025년 1월 Eaton 산불에 자사 설비가 관련됐을 가능성이 높다고 보고 있고, 추가로 중대한 손실이 생길 가능성이 높지만 규모를 추정할 수 없다(10-Q) — 최근 4분기 이익에도 큰 일회성 회수 이익이 들어 있어 배수 판정이 의미를 갖기 어렵다. 손실 규모가 추정되거나 합의가 마무리되면 다시 본다'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — Eaton 산불 손실 추정 불가</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — Eaton 산불 손실 추정 불가. 산불 책임 규모를 몰라 현금흐름 내재가치를 계산하지 않았다.')
h = _re0.sub(r'(id="eixFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)
h = _re0.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re0.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")
h = _re0.sub(r'(<div class="verdict-summary-head">[^<]*)<span class="tag">[^<]*</span>', r'\1<span class="tag">Eaton 산불 손실 추정 불가</span>', h, count=1)
h = _re0.sub(r'<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
h = _re0.sub(r'<div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
"""]


# ── 자동 카드 — 부문 지도(seg_map_propose 전부 맞음 — 법인 축 SCE 하나, 지주회사 매출은 거의 없다). 원문 대조: Q3 2026 SCE 매출 4,887 − 연결 조정 1 = 연결 4,886(Codex r1, 2026-11-07) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "dei:LegalEntityAxis",
 "extra": {},
 "members": {"eix:SouthernCaliforniaEdisonCompanyMember": ["SCE(남부 캘리포니아 전력)", "#00664f"]},
 "ignore": []
}
