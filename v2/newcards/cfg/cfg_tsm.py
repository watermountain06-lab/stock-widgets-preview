# TSM(TSMC ADR) v2 카드 설정 — fill.py TSM. 회계연도 12월 31일. 루트 카드 있음.
# 재무는 대만 IFRS 연결재무제표(6-K) — 어댑터(v2/adapters/tsm_ifrs.py)가 대만달러 그대로 companyfacts 모양 캐시를 만든다.
# 빌드: build.py는 SEC를 직접 부르는 EPS·재무 두 단계가 어댑터를 모른다 — tsm_feed.py(eps·financials)로 바꿔 끼우고
#   활동성에 --facts 캐시를 준 래퍼로 돌렸다(2026-10-05 G3, 공통 후보: build.py BUILD['feed']).
# 카드 표시: 분기 차트·YoY/QoQ·FCF·설비투자는 분기 평균 환율(연준 H.10, v2/fx.py)로 달러 환산(옛 카드 규칙) — PRE에서 바꾼다.
# 틀 시절 카드를 생성기로 다시 만들기 위해 지금 카드의 내용을 옮겼다(2026-10-05, 틀 통일 G3).
# 출처: 6-K(Q3 2025~Q2 2026 실적 발표·Q2 2026 연결재무제표 2026-08-14, 이사회 5/12·8/11, VIS 매각 5/15, Sony 합작 8/11), StockAnalysis(2026-09-25).
# 재현 모드: python3 build_ifrs.py <clone> TSM --from-card (일봉·이동평균·백테스트는 지금 카드에서, 마지막 종가 2026-09-23).
BUILD = {'feed': True}   # IFRS·대만달러 — adapters/tsm_feed.py
CIK = '0001046179'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
RELEASE = {'rev': 1270380, 'op': 766603, 'ni': 706562}   # Q2 2026 연결재무제표(백만 대만달러)
VOTES, VERDICT = (-1, 0, -2), '고평가'
CO = 'TSMC'
S_ = 'https://www.sec.gov/Archives/edgar/data/1046179/'
SEC = S_
PR = {'q2': S_ + '000104617926000451/a2q26e_withguidancexfinal.htm', 'q1': S_ + '000104617926000199/',
      'q4': S_ + '000104617926000008/', 'q3': S_ + '000104617925000116/'}
PR_CUR = 'q2'
TENQ = S_ + '000104617926000541/a2026q2consolidatedreport-.htm'; TENQ_NAME = 'Q2 2026 연결재무제표'
LINKS = {'sony': S_ + '000104617926000539/sonysemiconductorsolutions.htm', 'vis': S_ + '000104617926000280/tsmctosell81ofvanguardinte.htm',
         'board5': S_ + '000104617926000274/tsm-boardx20260512.htm', 'board8': S_ + '000104617926000536/tsm-boardx20260811.htm'}
FAIRBAND_TITLE = 'id="tsmFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 3년 +{HIST[\'growth_3y\'] * 100:.1f}%)</span>'
OPM_RANGE, Y2 = (40, 65), (40, 65)
FCF_SUB = '현금창출력'
CAPEX_SUB = '미래 재투자'
STAT3 = ('R&amp;D (Q2 2026)', '$2.3B', '기술 경쟁력 투자')
NEXT = ('10월 중순 예상', '일정 · Q3 2026'); NEXT_OP = ('10월 중순', 'Q3 2026 예상')
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
HEALTH_NOTE = ('유동비율 {FR[\'currentRatio\']:.1f}%·당좌비율 {FR[\'quickRatio\']:.1f}%로 단기 지급 여력이 넉넉하고, 이자보상배율은 {FR[\'interestCoverage\']:.0f}배다. '
               '현금·단기투자가 차입금보다 많아 순현금이 ADR 1주당 약 $15다.')
ACT_REASON = ''
YOY_EXTRA = ''
SEG = [('3·2나노', 33, '#e11d48'), ('5나노', 33, '#f97316'), ('7나노', 11, '#3498db'), ('16나노 이상', 23, '#8a8fa8')]   # 웨이퍼 매출 비중(%)
SEG_ADJ = 0   # PRE에서 (달러 환산 매출 − 100)으로 — 비중(%) 도넛이라 fill.py의 매출 대조를 건너뛰게
SEG_TITLE = '매출 구성 — 공정별 웨이퍼 매출 비중'
SEG_NOTE = ('7나노 이하 첨단 공정이 77%(2나노 3% 포함) · 16나노 이상은 16/20·28·40/45·65·90나노 이하 합계 · '
            '출처: <a href="{PR[\'q2\']}" target="_blank" rel="noopener">TSMC Q2 2026 실적 발표 (SEC 6-K) →</a>')
CAPITAL = [('설비투자 (Q2 2026)', '${cap[cur] / 1e9:.1f}B'),
           ('2026년 설비투자 계획 (1월 제시)', '$52~56B'),
           ('분기 배당 (Q2 2026분, 8월 승인)', '', 'NT$7.0')]
CHECK_WHEN = '2026년 10월 중순 (예상) · Q3 2026'
CHECK = ['매출 $44.6~45.8B 전망을 달성하는지(1달러=32대만달러 가정의 매출총이익률 65~67%, 영업이익률 56~58%)',
         '2나노(Q2 웨이퍼 매출의 3%)의 본격 양산이 매출 비중으로 확인되는지',
         '2026년 연간 매출 성장 전망(7월 "40% 조금 넘게")이 유지되는지',
         'Q2 영업외이익(NT$958억)에 들어간 VIS 지분 매각 차익이 빠진 뒤 순이익률이 어떻게 되는지']
NONOP_WHAT = '지분·장기투자'
PH = ['NVDA', 'AVGO', 'ASML', 'MU']
PEER_FILE = None
MISS_WHY = {('AVGO', 'pcr'): ' 자료 없음'}
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '반도체 대형주 PER 비교', 'pbr': '반도체 대형주 PBR 비교', 'psr': '반도체 대형주 PSR 비교',
                'pcr': '반도체 대형주 PCR(FCF) 비교', 'evebitda': '반도체 대형주 EV/EBITDA 비교'}
PEER_NAME_TITLE = '같은 IT 섹터 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'GICS Information Technology 대비 배수 순위 (ADR 가격 × 그날 환율 ÷ 대만달러 재무)'
FUND_ASOF_NOTE = 'Q2 2026 연결재무제표 6-K (2026-08-14 공시)'
PREMISE = ('동종업 안에서는 중간이지만, <strong>다섯 배수 모두 자기 5년 이력의 비싼 쪽이고 현금흐름 내재가치는 현재가에 한참 못 미친다.</strong> '
           '배수는 ADR 가격 기준이라, 본주보다 비싸게 거래되는 ADR만큼 대만 본주 기준 배수보다 높게 나온다.')
RISK = ('현재가가 정당하려면 5년간 매출이 매년 <strong data-vs="req">{pct(DCF[\'requiredGrowth\'])}</strong>씩 커야 한다. '
        '최근 3년 실제 성장은 연 {pct(HIST[\'growth_3y\'])}(대만달러 기준)였고, 회사가 1월에 제시한 2024~2029년 매출 연평균 성장 전망은 25%에 가깝다.')
FUND_TIP = '대만 IFRS 연결재무제표(6-K)를 분기 평균 환율로 달러 환산한 값이다(v2/adapters/tsm_ifrs.py).'
SELF_TIP = '다섯 배수 모두 5년 중 비싼 쪽(상위 {100 - max(v[\'percentile\'] for v in SM.values()):.0f}~{100 - min(v[\'percentile\'] for v in SM.values()):.0f}%)이다 — PSR·PBR·EV/EBITDA는 상위 {math.ceil(100 - min(SM[\'PSR\'][\'percentile\'], SM[\'PBR\'][\'percentile\'], SM[\'EV/EBITDA\'][\'percentile\']))}% 안쪽.'
PEER_TIP = ('같은 GICS 섹터(Information Technology) 안에서 배수 순위를 매긴 값이다(ADR 가격 기준).',
            '회계 기준이 다른 종목(IFRS)과 사업모델이 다른 종목(파운드리)이 섞여 있다.')
STORIES = ['지난 5년 성장 속도의 절반에서 출발해 점점 식고, 영업이익률은 지난 5년 중앙값({pct(HIST[\'margin_5y\'])})으로 내려온다. 매출 $1을 늘리는 데 $0.84를 투자한다(과거 평균 — 최근 1년($0.78)보다 자본이 더 드는 쪽).',
           '지난 5년의 성장 속도로 출발해 점점 식고, 영업이익률은 최근 2년 중앙값({pct(HIST[\'margin_2y\'])})으로 서서히 내려온다. 매출 $1당 투자는 최근 1년 $0.78에서 5년에 걸쳐 과거 평균 $0.84로 돌아온다.',
           '최근 3년의 성장 속도로 출발해 점점 식고, 지금 영업이익률({pct(HIST[\'margin_now\'])})이 그대로 간다. 매출 $1당 투자는 과거 평균 $0.84다.']
DCF_NOTE = ''
NEWS_RANGE = '2025.10 ~ 2026.09'
NEWS = [
    ('', '2026년 7월 16일 — Q2 2026 실적', '2026-07-16',
     '매출 $40.20B(+33.7%)로 가이던스 상단 $40.2B 도달 · 매출총이익률 67.7%·영업이익률 60.3% · 2026년 매출 성장 전망을 "40% 조금 넘게"로 상향', 'q2', 'TSMC 실적 발표 (SEC 6-K)'),
    ('neutral', '2026년 8월 11일 — Sony와 이미지센서 합작법인 본계약', '2026-08-11',
     '일본 구마모토에 차세대 이미지센서 합작법인 설립 · Sony가 지배주주 · 같은 날 이사회가 분기 배당 NT$7.0 승인', 'sony', 'TSMC·Sony 발표 (SEC 6-K)'),
    ('neutral', '2026년 5월 15일 — VIS 지분 8.1% 매각', '2026-05-15',
     '뱅가드(VIS) 보통주 최대 1억 5,200만 주를 블록딜로 매각 · Q2 영업외이익(NT$958억)을 키운 차익의 출처', 'vis', 'TSMC 공시 (SEC 6-K)'),
    ('neutral', '2026년 5월 12일 — 애리조나 법인 증자 승인', '2026-05-12',
     'TSMC Arizona에 최대 $20B 증자 · 설비투자 예산 약 $31.3B 승인 · 분기 배당 NT$6.0 → NT$7.0 인상(1분기분)', 'board5', 'TSMC 이사회 결의 (SEC 6-K)'),
    ('', '2026년 4월 16일 — Q1 2026 실적', '2026-04-16',
     '매출 $35.90B(+40.6%)로 가이던스 상단 $35.8B 상회 · 매출총이익률 66.2% · 2026년 매출 성장 전망 "30% 이상"', 'q1', 'TSMC 실적 발표 (SEC 6-K)'),
    ('', '2026년 1월 15일 — Q4 2025 실적 · 2026년 계획', '2026-01-15',
     '매출 $33.73B(+25.5%)로 가이던스 상단 $33.4B 상회 · 2026년 설비투자 $52~56B · 2024~2029년 매출 연평균 성장 25%에 가까울 전망', 'q4', 'TSMC 실적 발표 (SEC 6-K)'),
    ('', '2025년 10월 16일 — Q3 2025 실적', '2025-10-16',
     '매출 $33.10B(+40.8%) · 매출총이익률 59.5%·영업이익률 50.6% · 7나노 이하 첨단 공정 74%', 'q3', 'TSMC 실적 발표 (SEC 6-K)'),
]
SUMMARY = ('AI 수요로 첨단 공정 비중과 마진이 함께 오른다', '우호적·밸류 부담',
           ['세 분기 연속 매출이 직전 가이던스 상단 이상이었다. 2026년 매출 성장 전망은 1월 30% 가까이 → 4월 30% 이상 → 7월 40% 조금 넘게로 올라갔다.',
            '영업이익률이 1년 새 49.6%(Q2 2025)에서 60.3%(Q2 2026)로 올랐고, 7나노 이하 첨단 공정이 웨이퍼 매출의 77%다.',
            '설비투자가 커진다. 2026년 계획은 $52~56B이고, 이사회는 5월에 애리조나 법인 최대 $20B 증자를 승인했다.'],
           '다섯 배수 모두 자기 5년 이력의 비싼 쪽이다. 2분기 순이익에는 VIS 지분 매각 차익이 들어 있어(영업외이익 NT$958억) 그만큼은 반복되지 않는다.',
           'Q3 2026 실적(10월 중순 예상)에서 매출 전망 $44.6~45.8B와 매출총이익률 65~67%를 지키는지, 2나노 비중이 얼마나 늘었는지.')
BULL = [('수요', '세 분기 연속 가이던스 상단 이상이었고, 2026년 매출 성장 전망을 40% 넘게로 올렸다.'),
        ('기술', '7나노 이하가 웨이퍼 매출의 77%이고, 2나노 양산이 3분기부터 가파르게 늘어난다고 했다.'),
        ('마진', '영업이익률이 1년 새 49.6%에서 60.3%로 올랐다.')]
BEAR = [('밸류', '다섯 배수 모두 자기 5년 이력의 비싼 쪽이고, 현재가가 기본 내재가치의 약 {px / DCF[\'base\']:.1f}배다.'),
        ('설비투자', '2026년 설비투자 계획이 $52~56B이고, Q2 설비투자는 매출의 39%였다.'),
        ('환율', '마진 가이던스가 1달러=32대만달러 가정이라, 대만달러가 강해지면 마진이 깎인다.')]
ANALYST = {'rating': 'Strong Buy', 'n': 21, 'nt': 7, 'mean': 541.29, 'median': 530, 'low': 440, 'high': 650, 'sb': 14, 'b': 6, 'h': 1, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-06'
PRE = [r'''
FR = {r_['metric']: r_['value'] for ax_ in FUND['axes'].values() for r_ in ax_.get('rows', [])}   # 기본적 분석 지표 값
# 분기 흐름을 분기 평균 환율(연준 H.10)로 달러 환산 — 대만달러 재무(어댑터)를 옛 카드처럼 달러로 보인다(보도자료 대조는 위에서 대만달러로 끝남)
import fx as _fx, datetime as _dt
_, _rr = bmh.pick_tag(CIK, bmh.FLOW_TAGS['revenue'])
_st = {e_['end']: e_.get('start') for e_ in bmh.quarterly_flow(_rr, T)}
_fds, _fvs = _fx._load(_fx.CURRENCY[T])
def _qavg(k):
    s_ = _st.get(k) or (_dt.date.fromisoformat(k) - _dt.timedelta(days=91)).isoformat()
    x_ = [v_ for d_, v_ in zip(_fds, _fvs) if s_ <= d_ <= k]
    return sum(x_) / len(x_)
_seen = set()
for _dd in (rev, op, ni, ni_chart, ni_gaap, ocf, cap, fcf):
    if id(_dd) in _seen:
        continue
    _seen.add(id(_dd))
    for _k in list(_dd):
        _dd[_k] = _dd[_k] / _qavg(_k)
C.SEG_ADJ = rev[cur] / 1e6 - sum(v_ for _, v_, _ in C.SEG)   # 비중(%) 도넛 — 매출 대조 건너뜀
C.CAPITAL = [tuple(F(x_) for x_ in z_) for z_ in C.CAPITAL]
''']
# 카드 한정 패치(fill.py 끝에서 exec) — 틀 시절 카드에 있던 내용을 같은 자리에 되살린다.
POST = [r'''
# 분기 차트 제목·설명(달러 환산)
one('분기 매출 / 순이익 / 영업이익률 (Q3 2024~Q2 2026)', '분기 매출 / 순이익 / 영업이익률 (Q3 2024~Q2 2026 · 달러 환산)')
one('<canvas id="tsmRevChart"></canvas>\n    </div>\n', '<canvas id="tsmRevChart"></canvas>\n    </div>\n'
    '    <div class="yoy-footnote" style="margin-top:8px;">대만달러 실적을 분기 평균 환율(연준 H.10)로 달러 환산했다. 회사가 발표한 달러 매출과 조금 다를 수 있다(Q2 2026은 둘 다 $40.2B).</div>\n')
# YoY·QoQ 각주: IFRS 연결재무제표 달러 환산, 링크는 6-K 연결재무제표
_lk = f'<a href="{PR["q2"]}" target="_blank" rel="noopener">TSMC Q2 2026 실적 보도자료 (SEC 8-K) →</a>'
assert h.count(' · GAAP 기준 · FCF는 영업현금흐름 − 설비투자 · ' + _lk) == 2, h.count(_lk)
h = h.replace(' · GAAP 기준 · FCF는 영업현금흐름 − 설비투자 · ' + _lk,
              ' · 대만 IFRS 연결재무제표를 분기 평균 환율로 달러 환산 · FCF는 영업현금흐름 − 설비투자 · <a href="' + C.TENQ + '" target="_blank" rel="noopener">TSMC Q2 2026 연결재무제표 (SEC 6-K) →</a>')
# 총자산증가율 메모: 대만달러 그대로(옛 카드)
sub(r'(<span class="diag-label">총자산증가율</span><span class="diag-value">[^<]*</span><span class="diag-note">)[^<]*(</span>)',
    lambda m: m.group(1) + f'FY25 NT${a1 / 1e6:.2f}조(전기 NT${a0 / 1e6:.2f}조) · 대만달러 기준 · FY26 마감 전까지 동일' + m.group(2))
# 매출 구성: 비중(%) 도넛 — 범례는 비중만, 제목은 분기만
for n_, v_, c_ in C.SEG:
    sub(r'(</span>' + re.escape(n_) + r' <strong style="color:var\(--text\);">)[^<]*(</strong>)', lambda m: m.group(1) + f'{v_}%' + m.group(2))
one('매출 구성 — 공정별 웨이퍼 매출 비중 (Q2 2026 · 2026.06.30 기준)', '매출 구성 — 공정별 웨이퍼 매출 비중 (Q2 2026)')
# 자본배분: 배당 줄은 태그 없이, 아래 배당 각주(옛 카드)
one('<span class="zone-tag" style="background:rgba(240,192,64,0.18);color:var(--gold);"></span>\n            ', '')
sub(r'(<span class="zone-val">NT\$7\.0</span>\n          </div>\n        </div>\n      </div>\n)',
    lambda m: m.group(1) + '      <div class="yoy-footnote" style="margin-top:14px;">배당은 보통주 1주 기준이라 ADR 1주(보통주 5주)로는 NT$35다. 분기 배당이 NT$6.0에서 1분기분부터 NT$7.0으로 올랐다 · 출처: <a href="' + LINKS['board8'] + '" target="_blank" rel="noopener">TSMC 이사회 결의 (SEC 6-K) →</a></div>\n')
# 역산 문장: 성장 모드(reqMode growth)는 JS가 문장을 쓰지 않고 칸만 채운다 — 틀의 칸 있는 문장을 되살린다(fill.py가 '—'로 비움, MU와 같은 공통 후보)
assert DCF['reqMode'] == 'growth'
one('<div class="reverse">—</div>', F('<div class="reverse">지금 가격(<span data-dcf-price>${px:.2f}</span>)이 정당하려면 5년간 매출이 매년 <b data-dcf-req>{pct(DCF[\'requiredGrowth\'])}</b>씩 커야 한다. '
    '기본 시나리오(<span data-dcf-basev>${DCF[\'base\']:.0f}</span>)를 같은 방식으로 환산하면 연 <span data-dcf-baseeq>{pct(DCF[\'baseEquivGrowth\'])}</span>다.</div>'))
# 기본적 분석 툴팁: 분기 자료는 6-K 연결재무제표(10-Q 아님)
one("분기(Q2 2026, 10-Q), 성장률은", "분기(Q2 2026, 6-K 연결재무제표), 성장률은")
''']
