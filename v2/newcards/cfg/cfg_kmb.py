CIK = '0000055785'
BUILD = {'eps_tag': 'IncomeLossFromContinuingOperationsPerDilutedShare,EarningsPerShareDiluted',   # 계속사업 EPS — IFP 사업 지분 51% 매각(2026-07-01) 이익이 중단사업(Q3 주당 $4.18)
         'no_dcf': '미완성 — Kenvue 합병 뒤 첫 보고서 대기'}   # 2026-11-03 사용자 결정(보류 C군 → 미완성 카드), 2026-11-07 제작
# KMB(킴벌리-클라크) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 12월 31일. 기저귀·화장지·위생용품(북미·해외 개인위생) + 2026-11-02부터 Kenvue(타이레놀·리스테린 등).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-11-05 12:05 동부 장중 → 카드 기준일 11-06 종가), 실적 보도자료(8-K 2.02항 — 06~07시 동부 장 전 → 같은 날), Q3 예비 실적(10-15), Kenvue 합병 완료 8-K(11-02 09:10 장 전).
# 미완성 사유: Kenvue 합병 완료(2026-11-02, Kenvue 1주당 0.14625주 + $3.50) — 카드 재무는 합병 전 단독(9월 분기), 주식 수는 표지(합병 전) 기준이라 홈 시가총액도 합병 전 주식 수로 낮게 나온다.
#   통합 프로그램 세전 약 $3.1B(현금 $2.5B, 2029년까지 — 8-K 2.05항). IFP 지분 51% 매각(Suzano 합작, 7/1)은 중단사업 — 계속사업 EPS 최근 4분기 5.24 = FY2025 4.86 − 9개월 3.73 + 9개월 4.10(Q4 보도자료 직접값 1.14, 엔진 역산 1.13).
#   요약 자료의 2025 분기 매출에 IFP 재작성 전·후 값이 섞여 1년 전 비교가 어긋날 수 있다(Q1 2025 4,840 vs 재작성 뒤 약 4,050). 참고 점수 자기 73.2·동종 47.7.
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, 0), '판정 보류'
CO = 'Kimberly-Clark'
S_ = 'https://www.sec.gov/Archives/edgar/data/55785/'
SEC = S_
TENQ = S_ + '000162828026070754/kmb-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000162828026070514/kmbq32026ex-991.htm', 'q2': S_ + '000162828026052113/kmbq22026ex-991.htm',
      'q1': S_ + '000162828026027718/kmbq120268kex-991.htm', 'q4': S_ + '000162828026003514/kmb2025q48kex-991.htm',
      'pre': S_ + '000110465926115960/tm2627599d1_ex99-1.htm', 'close': S_ + '000110465926120990/tm2628636d1_ex99-1.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="kmbFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(Kenvue 합병 뒤 첫 보고서 대기)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 30)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('미완성 카드다. 2026년 11월 2일 Kenvue(타이레놀·리스테린·뉴트로지나 등) 인수가 끝났다(Kenvue 1주당 KMB 0.14625주 + 현금 $3.50). 카드 재무는 합병 전 9월 분기 단독 숫자이고 주식 수도 합병 전 기준이라, 주식 수가 크게 늘어난 지금 회사와 이어지지 않는다 — 합병을 반영한 첫 분기 보고서 뒤 다시 본다. 자기 이력·동종업 점수는 참고값이다. '
              '합병으로 주식은 약 2.81억 주 늘어 약 6.14억 주(지금 주가로 시가총액 약 $66B)가 됐는데, 카드의 시가총액·주당 순현금·PBR·PSR·EV/EBITDA는 모두 합병 전 주식 수와 부채로 계산돼 있다. '
              '7월 국제 화장지·업무용 사업(IFP) 지분 51%를 팔아 생긴 이익은 중단사업이라 PER과 기본적 분석의 순이익률은 계속사업 기준으로 계산했다(차트·핵심 재무 표의 순이익은 중단사업 포함 GAAP). 요약 자료의 2025년 1분기 매출(4.84B)은 IFP 재작성 전 값이라 그 분기 막대가 튄다. 회사는 통합 비용으로 2029년까지 세전 약 $3.1B를 예고했다.')
PH = ['PG', 'CL', 'CHD', 'CLX', 'KO', 'PEP']
PEER_FILE = 'peer_universe/consumer_staples.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '생활용품 등 6곳 PER 비교 (점수는 S&P500 필수소비재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 필수소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 필수소비재 대비 배수 순위 (v2/peer_universe/consumer_staples.json)'
PEER_TIP = ('S&P500 필수소비재(KMB 제외)와 배수 순위를 매긴 값이다.',
            '식품·음료·생활용품·유통이 섞여 있다. 차트에는 생활용품 등 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문): 북미 2,738 + 해외 개인위생(IPC) 1,396 = 4,134(1년 전 2,714 + 1,436 = 4,150).
SEG = [('북미', 2738, '#003da5'), ('해외 개인위생(IPC)', 1396, '#4f7fd6')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 실적 3건 + Q3 예비 실적 + Kenvue 합병 완료. 최신 Q3 2026(11-05 06:30 장 전)은 news_auto. EPS는 보도자료 계속사업 기준(Q4 2025부터 IFP는 중단사업).
NEWS_RANGE = '2026.01 ~ 2026.11'
NEWS = [
    ('neutral', '2026년 11월 2일 장 전 — Kenvue 인수 완료', '2026-11-02',
     'Kenvue 1주당 KMB 0.14625주 + 현금 $3.50 · 연간 시너지 $2.1B 목표 재확인 · 통합 비용 2029년까지 세전 약 $3.1B — 당일 주가 +0.3%', 'close', 'Kimberly-Clark 공시 (SEC 8-K)'),
    ('green', '2026년 10월 15일 장 전 — Q3 2026 예비 실적·연간 전망 유지', '2026-10-15',
     '확정 실적은 11월 5일 발표 · 2026년 전망(조정 영업이익 중간 한 자릿수 증가 등) 유지 — 당일 주가 +4.7%', 'pre', 'Kimberly-Clark 공시 (SEC 8-K)'),
    ('green', '2026년 8월 4일 장 전 — Q2 2026 실적', '2026-08-04',
     '매출 $4.2B(+0.6%) · 계속사업 희석 EPS $1.22(조정 $1.80) — 당일 주가 +3.7%', 'q2', 'Kimberly-Clark 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 28일 장 전 — Q1 2026 실적', '2026-04-28',
     '매출 $4.2B(+2.7%) · 계속사업 희석 EPS $1.70(조정 $1.60) — 당일 주가 +0.2%', 'q1', 'Kimberly-Clark 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 1월 27일 장 전 — Q4 2025 실적', '2026-01-27',
     '매출 $4.1B(−0.6%) · 계속사업 희석 EPS $1.14(조정 $1.43; 중단사업 포함 $1.50·조정 $1.86) — 당일 주가 −0.5%', 'q4', 'Kimberly-Clark 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 16, 'nt': 12, 'mean': 116.17, 'median': 115, 'low': 90, 'high': 162, 'sb': 4, 'b': 3, 'h': 8, 's': 0, 'ss': 1}
ANALYST_ASOF = '2026-11-08'


# 미완성 카드 표시(2026-11-03 사용자 결정, FISV·MLM·NSC·PTC·CHRW·SYY 방식).
INCOMPLETE_SHORT = 'Kenvue 합병 뒤 첫 보고서 대기'
INCOMPLETE_WHY = '2026년 11월 2일 Kenvue 인수가 끝났다(Kenvue 1주당 KMB 0.14625주 + 현금 $3.50) — 카드 재무(9월 분기)는 합병 전 단독 숫자라 주식 수가 크게 늘어난 지금 회사와 이어지지 않는다. 합병을 반영한 첫 분기 보고서 뒤 다시 본다'
POST = [r"""
import re as _re0
_w = '2026년 11월 2일 Kenvue 인수가 끝났다(Kenvue 1주당 KMB 0.14625주 + 현금 $3.50) — 카드 재무(9월 분기)는 합병 전 단독 숫자라 주식 수가 크게 늘어난 지금 회사와 이어지지 않는다. 합병을 반영한 첫 분기 보고서 뒤 다시 본다'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — Kenvue 합병 뒤 첫 보고서 대기</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — Kenvue 합병 뒤 첫 보고서 대기. 인수 뒤 재무가 크게 바뀌어 현금흐름 내재가치를 계산하지 않았다.')
h = _re0.sub(r'(id="kmbFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)   # 미완성 — PER 구간 범위를 보이지 않는다(FISV처럼, Codex·Fable r1)
import re as _re3
h = _re3.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re3.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")

h = _re0.sub(r'(<div class="verdict-summary-head">[^<]*)<span class="tag">[^<]*</span>', r'\1<span class="tag">Kenvue 합병 뒤 첫 보고서 대기</span>', h, count=1)
for _id in ('kmbDcfVerdict', 'kmbDcfBox', 'dcfPickValue'):
    h = h.replace(f'id="{_id}">계산 불가<', f'id="{_id}">보류(미완성)<')

h = _re0.sub(r'<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)   # 참고 점수를 약점으로 올리지 않는다(Fable r1)

h = _re0.sub(r'<div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)   # 참고 점수를 강점으로 올리지 않는다(Codex·Fable r1)


# 합병 기준으로 체크포인트 세 줄을 다시 쓴다 — 합병 전 매출 흐름(Q1 2025 재작성 전 값 섞임)·영업이익률·배당 비교는 Kenvue가 합쳐지면 끊긴다(Codex·Fable r1)
_cp = ('<div style="margin-bottom:8px;"><strong style="color:var(--accent2);">①</strong> Kenvue를 합친 첫 분기 매출과 합병 전 두 회사 합(프로포마)의 차이</div>\n'
       '      <div style="margin-bottom:8px;"><strong style="color:var(--accent2);">②</strong> 통합 비용(2029년까지 세전 약 $3.1B 예고)과 시너지(연 $2.1B 목표)가 분기 이익에 얼마나 잡히는지</div>\n'
       '      <div style="margin-bottom:8px;"><strong style="color:var(--accent2);">③</strong> 합병 뒤 주식 약 6.14억 주 기준 배당(분기 $1.28 × 주식 수)을 FCF가 감당하는지</div>')
h = _re0.sub(r'<div style="margin-bottom:8px;"><strong style="color:var\(--accent2\);">①</strong>.*?③</strong>[^<]*</div>', _cp, h, count=1, flags=_re0.S)
# Bull·Bear의 섞인 성장 줄과 감소 매출 Bull 줄 — 보류 안내로
h = _re0.sub(r'<div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">매출</span>.*?</div>', '<div class="bb-row bull"><span class="bb-icon">·</span><span class="bb-head">보류</span><span class="bb-text">미완성 카드라 강점을 따로 뽑지 않는다 — Kenvue 합병을 반영한 첫 보고서 뒤 다시 본다.</span></div>', h, count=1, flags=_re0.S)
h = _re0.sub(r'\n?\s*<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">성장</span>.*?</div>', '', h, count=1, flags=_re0.S)
h = _re0.sub(r'(?<!계속사업 )희석 EPS', '계속사업 희석 EPS', h)   # 카드 EPS는 계속사업 기준(MLM 방식)

# 핵심 재무 표 각주 — 순이익은 중단사업(IFP 매각 이익) 포함 GAAP라 YoY가 크게 튄다, 링크는 확정 실적 보도자료로(Fable r1)
h = h.replace("· GAAP 기준 · FCF는", "· GAAP 기준(Q3 2026 순이익은 IFP 매각 이익 등 중단사업 $1,395M 포함 — 계속사업은 $398M) · FCF는", 2)
h = h.replace('000110465926115960/tm2627599d1_ex99-1.htm" target="_blank" rel="noopener">Kimberly-Clark Q3 20', '000162828026070514/kmbq32026ex-991.htm" target="_blank" rel="noopener">Kimberly-Clark Q3 20')
"""]


# ── 자동 카드 — 부문 지도(손 작성). 원문 대조: Q3 2026 10-Q 북미 2,738 + IPC 1,396 = 4,134, 1년 전 2,714 + 1,436 = 4,150(2026-11-07) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"kmb:NorthAmericaNAMember": ["북미", "#003da5"], "kmb:InternationalPersonalCareIPCMember": ["해외 개인위생(IPC)", "#4f7fd6"]},
 "ignore": []
}
