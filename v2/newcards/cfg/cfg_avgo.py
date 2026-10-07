# AVGO(브로드컴) v2 카드 설정 — fill.py AVGO. 회계연도 10월 말~11월 초 일요일(Q3 FY26 = 2026-05-04~08-02).
# 틀 시절 카드(2026-09 루트 카드에서 손으로 옮긴 것)를 생성기로 다시 만들기 위해 지금 카드의 내용을 옮겼다(2026-10-05, 틀 통일 G2).
# 출처: SEC XBRL(무형자산 상각 2020~2025는 adapters/avgo_amort.py — 엔진이 읽는다), Q3 FY26 10-Q(2026-09-10), 실적 발표(Q4 FY25~Q3 FY26),
# 8-K(CFO 4/2, Google 4/6, Apple 7/6), StockAnalysis(2026-09-25).
# 순이익: NetIncomeLoss 태그가 FY2024에서 멈춰 연결 순이익(ProfitLoss, 비지배지분 없음)을 쓴다.
# 재현 모드: python3 v2/newcards/build.py AVGO --from-card (일봉·이동평균·백테스트는 지금 카드에서, 마지막 종가 2026-09-24).
CIK = '0001730168'
CUR, YO, QO = '2026-08-02', '2025-08-03', '2026-05-03'
QLABEL, YL, QQL = 'Q3 FY26', 'Q3 FY25', 'Q2 FY26'
L8 = ['Q4 FY24', 'Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26']
NI_TAGS = ['ProfitLoss']
RELEASE = {'rev': 29591, 'op': 15955, 'ni': 13088}   # Q3 FY26 10-Q 손익계산서(백만 달러, 부문 합 29,591과 같다)
VOTES, VERDICT = (0, 0, -2), '적정~고평가'
CO = 'Broadcom'
S_ = 'https://www.sec.gov/Archives/edgar/data/1730168/'
SEC = S_
PR = {'q3': S_ + '000173016826000076/avgo-08022026x8kxex99.htm', 'q2': S_ + '000173016826000051/avgo-05032026x8kxex99.htm',
      'q1': S_ + '000173016826000011/avgo-02012026x8kxex99.htm', 'q4': S_ + '000173016825000116/avgo-11022025x8kxex99.htm'}
PR_CUR = 'q3'
TENQ = S_ + '000173016826000080/avgo-20260802.htm'; TENQ_NAME = 'Q3 FY26 10-Q'
LINKS = {'tenq': TENQ, 'apple': S_ + '000119312526295589/d84378d8k.htm', 'google': S_ + '000119312526144028/d87999d8k.htm',
         'cfo': S_ + '000119312526140574/d109450d8k.htm'}
FAIRBAND_TITLE = 'id="avgoFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 3년 +{pct(HIST[\'growth_3y\'])})</span>'
OPM_RANGE, Y2 = (25, 60), (25, 60)
FCF_SUB = '현금창출력'
CAPEX_SUB = '미래 재투자'
STAT3 = ('R&amp;D (Q3 FY26)', '$2.9B', '기술 경쟁력 투자')
NEXT = ('12월 중순 예상', '일정 · Q4 FY26'); NEXT_OP = ('12월 중순', 'Q4 FY26 예상')
FY_ENDS, FY_LABEL = ('2025-11-02', '2024-11-03'), 'FY2025'
HEALTH_NOTE = ('유동비율 250%·당좌비율 229%로 단기 지급 여력은 넉넉하고, 이자보상배율은 20.5배다. 차입금은 2023년 VMware 인수 때 크게 늘었고, '
               '이번 분기에도 공개매수와 상환으로 회사채 $5.6B를 줄여 총차입금이 $65.1B(FY25 말)에서 $59.4B가 됐다. 현금 $24.0B보다 차입금이 많아 순차입금이 남아 있다.')
ACT_REASON = ''
YOY_EXTRA = ''
SEG = [('AI 반도체', 16700, '#f63a5f'), ('기타 반도체', 4139, '#f97316'), ('인프라 소프트웨어', 8752, '#3498db')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'
SEG_NOTE = ('반도체 부문 $20.8B 가운데 AI 반도체가 $16.7B(전년 대비 +221%)다. 기타 반도체는 부문 매출에서 AI 반도체를 뺀 값이다 · 출처: '
            '<a href="{PR[\'q3\']}" target="_blank" rel="noopener">Broadcom Q3 FY26 실적 발표 (SEC 8-K) →</a>')
CAPITAL = [('자사주 매입 (FY26 1~3분기 누계)', '$8.45B'), ('잔여 바이백 승인 한도 (2026.08.02 기준)', '$10.1B'), ('배당 (Q3 FY26, 주당 $0.65)', '', '$3.1B')]   # 자리 채움 — 옛 카드의 네 줄은 POST
CAPITAL4 = [('배당 (Q3 FY26, 주당 $0.65)', '$3.1B'), ('자사주 매입 (FY26 1~3분기 누계)', '$8.45B'),
            ('잔여 바이백 승인 한도 (2026.08.02 기준)', '$10.1B'), ('회사채 공개매수·상환 (Q3 FY26)', '$5.6B')]
CAPITAL_NOTE = ('자사주 매입은 1분기 $7.85B, 2분기 $0.6B였고 3분기에는 없었다. 분기 배당은 FY26부터 $0.59에서 $0.65로 10% 올랐다 · 출처: '
                '<a href="{TENQ}" target="_blank" rel="noopener">Broadcom Q3 FY26 10-Q →</a>')
CHECK_WHEN = '2026년 12월 중순 (예상) · Q4 FY26'
CHECK = ['매출 가이던스 $34.8B(전년 대비 +93%)와 비GAAP 영업이익률 66%를 지키는지',
         'AI 반도체 매출이 전망대로 $21.7B(전년 대비 +236%)에 닿는지',
         'AI XPV 플랫폼의 리스 보증(최대 약 $29B)과 고객 전환사채 한도($42B)가 실제로 쓰이기 시작하는지',
         '인프라 소프트웨어 성장(Q3 +29%)이 고객이 해지할 수 없는 계약에서 추가로 인식한 라이선스 매출 덕인지, 다음 분기에도 이어지는지']
NONOP_WHAT = '지분·장기투자'
PH = ['NVDA', 'TSM', 'ASML', 'QCOM', 'MU']
PEER_FILE = None
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '반도체 대형주 PER 비교', 'pbr': '반도체 대형주 PBR 비교', 'psr': '반도체 대형주 PSR 비교',
                'pcr': '반도체 대형주 PCR(FCF) 비교', 'evebitda': '반도체 대형주 EV/EBITDA 비교'}
PEER_NAME_TITLE = '같은 IT 섹터 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'GICS Information Technology 23~27종목 대비 배수 순위'
FUND_ASOF_NOTE = 'Q3 FY26 10-Q (2026-09-10 공시)'
PREMISE = ('자기 5년 이력과 동종업 안에서는 둘 다 중간 자리지만, <strong>현금흐름 내재가치(기본 시나리오)는 현재가의 {DCF[\'base\'] / px * 100:.0f}%에 그친다.</strong> '
           'VMware 인수로 생긴 영업권·무형자산이 투하자본에 들어가 평균 매출/자본이 0.66으로 낮게 잡히는 영향이 크다.')
RISK = ('현재가가 정당하려면 5년간 매출이 매년 <strong data-vs="req">{pct(DCF[\'requiredGrowth\'])}</strong>씩 커야 한다. '
        '최근 5년 실제 성장은 연 {pct(HIST[\'growth_5y\'])}였고, 4분기 가이던스는 전년 대비 93% 성장이다.')
FUND_TIP = '순이익률은 연결 순이익을 썼다. 지배주주 순이익 태그가 FY2024에서 멈췄고, 비지배지분은 없다.'
SELF_TIP = '다섯 배수 모두 5년 중 가운데 부근(하위 {int(min(SM[k][\'percentile\'] for k in (\'PER\', \'PSR\', \'PBR\', \'PCR\', \'EV/EBITDA\')) + 0.5)}~{int(max(SM[k][\'percentile\'] for k in (\'PER\', \'PSR\', \'PBR\', \'PCR\', \'EV/EBITDA\')) + 0.5)}%)이다. EV/EBITDA는 2020~2025년 무형자산 상각을 공시 원문에서 채워 계산했다.'
PEER_TIP = ('같은 GICS 섹터(Information Technology) 안에서 배수 순위를 매긴 값이다.',
            '회계 기준이 다른 종목(IFRS)과 사업모델이 다른 종목(파운드리)이 섞여 있다.')
STORIES = ['지난 5년 성장 속도의 절반에서 출발해 점점 식고, 영업이익률은 지난 5년 중앙값({pct(HIST[\'margin_5y\'])})으로 내려온다. 매출 $1을 늘리는 데 $1.52를 투자한다(과거 평균 — 최근 1년($0.14)보다 자본이 더 드는 쪽).',
           '지난 5년의 성장 속도로 출발해 점점 식고, 영업이익률은 최근 2년 중앙값({pct(HIST[\'margin_2y\'])})으로 서서히 내려온다. 매출 $1당 투자는 최근 1년 $0.14에서 5년에 걸쳐 과거 평균 $1.52로 돌아온다. 최근 1년 값은 순투자에서 인수 무형자산 상각(연 $8.0B)까지 빼서 작게 잡힌 것이라, 이 시나리오 가치를 높이는 쪽으로 기운다.',
           '최근 3년의 성장 속도로 출발해 점점 식고, 지금 영업이익률({pct(HIST[\'margin_now\'])})이 그대로 간다. 매출 $1당 투자는 과거 평균 $1.52다. 과거 평균에는 VMware 인수로 생긴 영업권·무형자산이 들어 있어, 인수 없이 자라는 동안에는 이보다 적게 들 수 있다.']
DCF_NOTE = ''
NEWS_RANGE = '2025.12 ~ 2026.09'
NEWS = [
    ('neutral', '2026년 9월 10일 공시 · 9월 10일 반응 — 10-Q · 고객 리스 보증', '2026-09-10',
     '6월 출범한 AI XPV 플랫폼(1차 $35B)에서 고객의 5년 리스 의무를 보증 · 최대 노출 약 $29B · 고객 전환사채 인수 한도 $42B', 'tenq', 'Broadcom 10-Q (SEC)'),
    ('', '2026년 9월 2일 발표 · 9월 3일 반응 — Q3 FY26 실적', '2026-09-03',
     '매출 $29.6B(+86%)로 가이던스 $29.4B 상회 · AI 반도체 $16.7B(+221%) · 4분기 가이던스 $34.8B', 'q3', 'Broadcom 실적 발표 (SEC 8-K)'),
    ('green', '2026년 7월 6일 — Apple 장기 계약', '2026-07-06',
     'Apple 여러 세대 제품에 들어갈 맞춤형 ASIC을 개발·공급하는 장기 계약 · 협력 기간 2031년까지 연장', 'apple', 'Broadcom 공시 (SEC 8-K)'),
    ('', '2026년 6월 3일 발표 · 6월 4일 반응 — Q2 FY26 실적', '2026-06-04',
     '매출 $22.2B(+48%)로 가이던스 $22.0B 상회 · AI 반도체 $10.8B(+143%) · 3분기 가이던스 $29.4B', 'q2', 'Broadcom 실적 발표 (SEC 8-K)'),
    ('green', '2026년 4월 6일 공시 · 4월 7일 반응 — Google TPU 장기 계약', '2026-04-07',
     'Google 차세대 TPU 개발·공급 장기 계약 · AI 랙용 네트워킹 부품 공급 보장 계약(2031년까지) · Anthropic이 2027년부터 Broadcom을 통해 약 3.5GW의 TPU 연산 사용', 'google', 'Broadcom 공시 (SEC 8-K)'),
    ('neutral', '2026년 4월 2일 공시 · 4월 6일 반응 — CFO 교체', '2026-04-06',
     'Kirsten Spears CFO가 6월 12일 은퇴 · 후임은 Amie Thuener(전 Alphabet 최고회계책임자)', 'cfo', 'Broadcom 공시 (SEC 8-K)'),
    ('', '2026년 3월 4일 발표 · 3월 5일 반응 — Q1 FY26 실적', '2026-03-05',
     '매출 $19.3B(+29%)로 가이던스 $19.1B 상회 · AI 반도체 $8.4B(+106%) · 자사주 매입 $10B 추가 승인', 'q1', 'Broadcom 실적 발표 (SEC 8-K)'),
    ('', '2025년 12월 11일 발표 · 12월 12일 반응 — Q4 FY25 실적', '2025-12-12',
     '매출 $18.0B(+28%)로 가이던스 $17.4B 상회 · 분기 배당 10% 인상($0.65) · 1분기 가이던스 $19.1B', 'q4', 'Broadcom 실적 발표 (SEC 8-K)'),
]
SUMMARY = ('맞춤형 AI 칩 수요가 매 분기 가이던스를 넘긴다', '우호적·밸류 부담',
           ['네 분기 연속 매출이 직전 가이던스를 넘었다. $18.0B에서 $29.6B까지 늘었고, AI 반도체 성장률은 전년 대비 74% → 106% → 143% → 221%로 빨라졌다.',
            'Google(TPU, 네트워킹 공급은 2031년까지)·Apple(맞춤형 ASIC, 2031년까지)과 장기 계약을 맺었다. 확정 계약 잔액은 $179.2B이고, 그중 약 25%가 12개월 안에 매출이 된다.',
            '4분기 가이던스는 매출 $34.8B, AI 반도체 $21.7B다.'],
           '고객의 자금 조달까지 떠안기 시작했다(리스 보증 최대 약 $29B, 고객 전환사채 인수 한도 $42B). 상위 5개 최종 고객이 최근 분기 매출의 약 55%(9개월 누계 50%)이고, 실적 발표 다음날 주가가 오른 것은 네 번 중 한 번(Q1 FY26)뿐이다.',
           'Q4 FY26 실적(12월 중순 예상)에서 $34.8B 가이던스와 AI 반도체 $21.7B를 넘는지, 보증 노출이 얼마나 쌓였는지.')
BULL = [('수요', 'AI 반도체 매출이 전년 대비 221% 늘었고, 4분기 전망은 $21.7B(+236%)다.'),
        ('계약 잔액', '확정 계약 잔액이 $179.2B이고, Google(TPU)·Apple(맞춤형 ASIC)과 장기 계약을 맺었다.'),
        ('현금창출', '3분기 잉여현금흐름이 $13.7B로 매출의 46%이고, 설비투자는 매출의 2%에 못 미친다.')]
BEAR = [('밸류', '현재가가 기본 내재가치의 약 {ratio:.1f}배이고, 현재가를 정당화하려면 매출이 5년간 매년 {pct(DCF[\'requiredGrowth\'])}씩 커야 한다.'),
        ('고객 집중', '상위 5개 최종 고객이 최근 분기 매출의 약 55%이고, 한 고객의 리스 의무를 최대 약 $29B까지 보증한다.'),
        ('차입금', '현금 $24.0B보다 차입금이 $59.4B로 많아, 리스를 더한 순차입금이 약 $37B이다.')]
ANALYST = {'rating': 'Strong Buy', 'n': 50, 'nt': 29, 'mean': 519.07, 'median': 520, 'low': 350, 'high': 630, 'sb': 40, 'b': 7, 'h': 3, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-06'

# 카드 한정 패치(fill.py 끝에서 exec) — 틀 시절 카드에 있던 내용을 같은 자리에 되살린다.
POST = [r'''
# 역산 문장: 성장 모드는 틀이 빈칸(—)으로 둔다 — 옛 카드의 문장 틀(값은 카드 JS가 data-dcf-* 칸에 채운다)
one('<div class="reverse">—</div>', '<div class="reverse">지금 가격(<span data-dcf-price>$' + f'{px:.2f}' + '</span>)이 정당하려면 5년간 매출이 매년 <b data-dcf-req>' + pct(DCF['requiredGrowth']) + '</b>씩 커야 한다. 기본 시나리오(<span data-dcf-basev>$' + f"{DCF['base']:.0f}" + '</span>)를 같은 방식으로 환산하면 연 <span data-dcf-baseeq>' + pct(DCF['baseEquivGrowth']) + '</span>다.</div>')
# 자본배분: 옛 카드는 네 줄(배당·누계 매입·잔여 한도·회사채 상환)과 출처 각주
_z = ''.join(f'\n        <div class="zone-item">\n          <span class="zone-label">{l_}</span>\n          <span class="zone-val">{v_}</span>\n        </div>' for l_, v_ in C.CAPITAL4)
sub(r'(<div class="card-title">자본배분 · 주주환원 \([^)]*\)</div>\n      <div class="zone-list">).*?(\n      </div>)(\n    </div>)',
    lambda m: m.group(1) + _z + m.group(2) + '\n      <div class="yoy-footnote" style="margin-top:14px;">' + F(C.CAPITAL_NOTE) + '</div>' + m.group(3))
# 각주 링크 이름(옛 카드: 실적발표 원문)
assert h.count(f'{C.CO} {QL} 실적 보도자료 (SEC 8-K)') == 2
h = h.replace(f'{C.CO} {QL} 실적 보도자료 (SEC 8-K)', f'{C.CO} {QL} 실적발표 원문 (SEC 8-K)')
# 총자산증가율 메모(옛 카드 표기)
one(f'<span class="diag-note">{C.FY_LABEL} 말 ${a1 / 1000:.1f}B(전년 ${a0 / 1000:.1f}B) · 연간 지표</span>', f'<span class="diag-note">FY25 ${a1 / 1000:.1f}B(전기 ${a0 / 1000:.1f}B) · 연간 지표, FY26 마감 전까지 동일</span>')
''']
