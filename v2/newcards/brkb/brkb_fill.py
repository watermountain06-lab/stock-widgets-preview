#!/usr/bin/env python3
"""BRKB(버크셔 해서웨이) 카드 생성기 — 분기마다 바뀌는 숫자와 문장을 원문에서 다시 쓴다(2026-10-12 사용자 결정).

버크셔는 보험지주라 일반 생성기(auto_card)의 매출·영업이익률 틀이 맞지 않아, 은행 카드처럼 전용 생성기를 둔다.
카드 HTML 자체를 틀로 쓰고, 분기마다 바뀌는 자리만 정해진 꼴로 다시 쓴다(같은 꼴이라 몇 번 돌려도 같다).

- 숫자: adapters/brkb_quarter.py(10-Q/10-K 인라인 XBRL + MD&A 세후 사업별 표·플로트·상위 5종목 문장),
        adapters/brkb_pillars.py(두 기둥 참고값 — 사전 등록 계산 그대로, 판정에는 넣지 않는다)
- 문장: 규칙 문장(숫자를 넣는 정해진 틀). 원인·전망은 쓰지 않는다.
- 뉴스: 실적 발표 항목은 이 스크립트가 만든다. 손으로 넣은 다른 사건(인수·경영진)은 15개월 동안 남긴다.
- 기준 시점: 카드의 마지막 종가일 하루 전까지 접수된 공시만(그날 장중에 나온 공시를 미리 쓰지 않게).
- 못 읽으면(문장 꼴이 바뀜, 표 합이 안 맞음, 자리를 못 찾음) 멈춘다 — 카드는 그대로 두고 실패로 알린다.
- 매일 돈다(daily_price.py HAND 단계). 숫자 칸(자기 이력·밴드·밸류 문장)은 그다음 hand_refresh.py가 쓴다.

    python3 v2/newcards/brkb/brkb_fill.py            # v2/BRKB_full_widget.html을 고친다
    python3 v2/newcards/brkb/brkb_fill.py --dry      # 쓰지 않고 바뀔 자리만 센다
"""
import datetime as dt
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NC = os.path.dirname(HERE)
V2 = os.path.dirname(NC)
sys.path.insert(0, os.path.join(V2, "adapters"))
sys.path.insert(0, NC)
import brkb_quarter as bq  # noqa: E402
import brkb_pillars as bp  # noqa: E402

T, CIK = "BRKB", "0001067983"
CARD = os.path.join(V2, f"{T}_full_widget.html")
DRY = "--dry" in sys.argv
h = open(CARD, encoding="utf-8").read()
_n = {"subs": 0}


def sub(pat, new, flags=re.S, count=1):
    """정확히 한 자리(또는 count자리)를 바꾼다 — 못 찾으면 멈춘다(카드 틀이 바뀐 것)."""
    global h
    h2, n = re.subn(pat, new if callable(new) else (lambda m: m.expand(new) if "\\" in new else new), h, flags=flags)
    if n != count:
        raise SystemExit(f"BRKB 채우기: 자리 {n}곳(기대 {count}) — {pat[:80]}")
    h = h2
    _n["subs"] += 1


# ── 기준 시점·가격 ───────────────────────────────────────────────────────
D = json.loads(re.search(r"const BRKB_DAILY = (\[.*?\]);", h, re.S).group(1))
SESSION, PX = D[-1][0], D[-1][4]
import auto_card as ac  # noqa: E402
import news_auto as na  # noqa: E402
SUB = ac._submissions(CIK)
ROWS = list(zip(SUB["form"], SUB["filingDate"], SUB["accessionNumber"], SUB["primaryDocument"], SUB["items"]))


def first_session_after(accepted_utc):
    """공시 접수 뒤 첫 종가 세션(동부 16:00 이후면 다음 거래일) — daily_price.first_session_after와 같은 규칙."""
    from zoneinfo import ZoneInfo
    t_ = dt.datetime.strptime(accepted_utc[:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=dt.timezone.utc).astimezone(ZoneInfo("America/New_York"))
    day = t_.date() if t_.hour < 16 else t_.date() + dt.timedelta(days=1)
    while day.weekday() >= 5:
        day += dt.timedelta(days=1)
    return day.isoformat()


# 기준 시점: 접수 뒤 첫 종가가 카드의 마지막 종가 이전인 10-Q·10-K까지(장 마감 뒤 공시는 다음 종가부터, Codex).
# 숫자 칸(brkb_multiples: 접수일 ≤ 거래일)과는 장 마감 뒤 접수된 날 하루만 다를 수 있다.
_ok = [SUB["filingDate"][i] for i, f in enumerate(SUB["form"]) if f in ("10-Q", "10-K", "10-Q/A", "10-K/A")
       and first_session_after(SUB["acceptanceDateTime"][i]) <= SESSION]
ASOF = os.environ.get("BRKB_ASOF") or max(_ok)   # BRKB_ASOF: 지난 분기로 되돌려 시험할 때만
L = bq.last_end(ASOF)
Q = bq.quarter(L, ASOF)
P = bp.pillars(ASOF)
if P.get("abstain") or P.get("L") != L:
    raise SystemExit(f"BRKB 채우기: 두 기둥 계산이 {L} 분기와 맞지 않는다 ({P.get('L')}, {P.get('abstain')})")
d = dt.date.fromisoformat
y, qn = int(L[:4]), {"03": 1, "06": 2, "09": 3, "12": 4}[L[5:7]]
qlab = lambda e: "Q%d %s" % ({"03": 1, "06": 2, "09": 3, "12": 4}[e[5:7]], e[:4])
QL, YL, PL = qlab(L), qlab(bq.year_ago(L)), qlab(bq.prev_q(L))
QK = f"{qn}분기" if qn < 4 else "4분기"
dot = lambda e: e.replace("-", ".")
NEXT_END = {"03-31": f"{y}-06-30", "06-30": f"{y}-09-30", "09-30": f"{y}-12-31", "12-31": f"{y + 1}-03-31"}[L[5:]]
NL = qlab(NEXT_END)
NA = bq.year_ago(NEXT_END)   # 다음 분기의 1년 전 분기 — 체크포인트 비교 기준
NAL = qlab(NA)
FORM = "10-K" if L.endswith("12-31") else "10-Q"


def B(v, nd=None):
    """$B — 100억 달러 넘으면 소수 한 자리, 아니면 두 자리(카드 관례: $177.5B, $1.73B)."""
    if v is None:
        return "—"
    from decimal import Decimal, ROUND_HALF_UP   # 13,485 → $13.49B(이진 소수 반올림은 $13.48B, Fable)
    a = Decimal(repr(abs(float(v)))) / Decimal(10 ** 9)
    nd = nd if nd is not None else (1 if a >= 10 else 2)
    return ("−" if v < 0 else "") + f"${a.quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP):,.{nd}f}B"


def pc(a, b):
    if a is None or b is None or b <= 0:
        return None
    return (a / b - 1) * 100


def pct(x, nd=1):
    return "—" if x is None else f"{x:+.{nd}f}%".replace("-", "−")


def vs(a, b):
    """증감 표기 — 1년 전 값이 0 이하(적자)면 비율 대신 그 값을 적는다(Fable)."""
    return pct(pc(a, b)) if b is not None and b > 0 else f"1년 전 {B(b * 1e6, 2)}"


# ── SEC 제출 목록: 10-Q 주소, 실적 보도자료(8-K 2.02), 발표일(토요일) ──
def doc_url(doc):
    r = next((x for x in ROWS if x[3] == doc and x[0] in ("10-Q", "10-K")), None)
    return f"https://www.sec.gov/Archives/edgar/data/{int(CIK)}/{r[2].replace('-', '')}/{doc}" if r else None


def release_day(filed):
    """버크셔는 토요일에 실적을 내고 월요일(드물게 화요일)에 10-Q/10-K를 낸다 — 접수일 바로 전 토요일."""
    f = d(filed)
    return f - dt.timedelta(days=(f.weekday() - 5) % 7 or 7)


def press(end):
    """그 분기 실적 보도자료 주소 — 발표 토요일부터 12일 안의 8-K 2.02항 EX-99. 못 찾으면 None."""
    try:
        filed = bq.doc_for(end)[2]
    except bq.BrkbParseError:
        return None
    rd = release_day(filed)
    for form, fd, acc, prim, items in sorted(ROWS, key=lambda x: x[1]):
        if form == "8-K" and "2.02" in (items or "").split(",") and 0 <= (d(fd) - rd).days <= 12:
            pth = os.path.join(ac.SUBS, f"exhibit_{acc}.json")
            if os.path.exists(pth) and json.load(open(pth)).get("url"):
                return json.load(open(pth))["url"]
            try:
                u, hd = na.exhibit(CIK, acc, prim)
            except Exception:
                return None
            json.dump({"url": u, "head": hd[:400]}, open(pth, "w"))
            return u
    return None


TENQ = doc_url(Q["doc"]) or f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={CIK}&type=10-Q"
PRESS = press(L)
SRC = (f'<a href="{PRESS}" target="_blank" rel="noopener">Berkshire {QL} 실적 보도자료 (SEC 8-K) →</a>' if PRESS
       else f'<a href="{TENQ}" target="_blank" rel="noopener">Berkshire {QL} {FORM} (SEC) →</a>')
REL = release_day(Q["filed"])
try:
    _ra = release_day(bq.doc_for(NA)[2])   # 작년 같은 분기 발표(토요일) — 같은 달 같은 번째 토요일(11월 첫 토요일 등, Fable)
    _nth, _yy = (_ra.day - 1) // 7, _ra.year + 1
    _d1 = dt.date(_yy, _ra.month, 1)
    NEXT_DAY = _d1 + dt.timedelta(days=(5 - _d1.weekday()) % 7 + 7 * _nth)
    if NEXT_DAY.month != _ra.month:   # 다섯째 토요일이 없는 달
        NEXT_DAY -= dt.timedelta(days=7)
except bq.BrkbParseError:
    NEXT_DAY = REL + dt.timedelta(days=91)
WD = "월화수목금토일"
NEXT_TXT = f"{NEXT_DAY.month}월 {NEXT_DAY.day}일({WD[NEXT_DAY.weekday()]}) 무렵"
CHECK_WHEN = f"{NEXT_DAY.year}년 {NEXT_DAY.month}월 {NEXT_DAY.day}일 무렵 (예상) · {NL}"

# ── 분기 값 ──────────────────────────────────────────────────────────────
FX = bq.fx_of(Q["doc"], qn)   # 기타에 든 외화 차입금 환산 손익(세후 $M, 이번·1년 전) — 못 읽으면 None
# 세후 사업별 표는 $M 그대로 쓴다(B6로 적는다)
S, SY = bq.seg_quarter(L, ASOF)
SP = bq.seg_quarter(bq.prev_q(L), ASOF)[0]
NONINS = lambda s: s["rail"] + s["energy"] + s["msr"] + sum(v for k, v in s.items() if k.startswith("x:"))   # 보험 밖 사업 — '기타'(외화 차입금 환산손익·모회사 이자)는 뺀다
cash_io = Q["cash_io"] + Q["tbills"]
cash_all = cash_io + Q["cash_rue"]
debt = Q["debt_io"] + Q["debt_rue"]
sharesB = P["sharesB"]
assets = bq.bal("Assets", [], L, ASOF)

# 8분기 차트
ends = [L]
while len(ends) < 8:
    ends.insert(0, bq.prev_q(ends[0]))
rev8, ni8, opm8 = [], [], []
for e in ends:
    r_ = bq.flow_q("Revenues", bq.IO, e, ASOF) + bq.flow_q("Revenues", bq.RUE, e, ASOF)
    n_ = bq.flow_q("NetIncomeLoss", [], e, ASOF)
    o_ = bq.seg_quarter(e, ASOF)[0]["oper"] * 1e6
    rev8.append(round(r_ / 1e9, 1)); ni8.append(round(n_ / 1e9, 1)); opm8.append(round(o_ / r_ * 100, 1))
L8 = [qlab(e) for e in ends]

# ── 1. 헤더 · 두 기둥 ─────────────────────────────────────────────────────
p1ps, e2ps, iv = P["p1"] / sharesB, P["e2"] / bp.RATE / sharesB, P["iv"]
sub(r'(<span class="meta-value" id="brkbPillarRef"[^>]*title=")[^"]*(">)[^<]*',
    lambda m: m.group(1) + f"투자 기둥 ${p1ps:.0f} + 영업 기둥 ${e2ps:.0f}(주당). 보험지주라 현금흐름 모델 대신 쓰지만 사전 등록한 데이터 정확성 관문을 통과하지 못해 판정에 넣지 않는다. 내재가치 탭 참고." + m.group(2) + f"${iv:.0f}")
sub(r'<div class="card-title">두 기둥 참고값 — [^<]*</div>', f'<div class="card-title">두 기둥 참고값 — {QL} {FORM} 기준</div>')
TB = f'''        <tr>
          <td class="scn-name">투자</td>
          <td>{B(P["p1"], 1)}</td><td class="big">${p1ps:.2f}</td>
          <td class="story">보험·기타 부문의 현금 {B(P["cash"], 1)}, 국채 {B(P["tbills"], 1)}, 채권 {B(P["bonds"], 1)}, 상장주식 {B(P["eq_fv"], 1)}를 더하고 국채 매입 미지급금 {B(P["payable"], 1)}와 주식 평가이익에 물릴 세금 {bp.TAX * 100:.0f}%를 뺐다.</td>
        </tr>
        <tr>
          <td class="scn-name">영업</td>
          <td>{B(P["e2"], 1)} ÷ {bp.RATE * 100:.0f}%</td><td class="big">${e2ps:.2f}</td>
          <td class="story">최근 4분기 정상화 영업이익 {B(P["op_norm"], 1)}에서 보험 투자수익과 인수이익(세후)을 뺀 사업 이익이다. 철도·에너지·제조 등에서 나온다.</td>
        </tr>
        <tr>
          <td class="scn-name scn-base">합계</td>
          <td></td><td class="big scn-base">${iv:.2f}</td>
          <td class="story">B주 환산 {sharesB / 1e9:.3f}B주 기준. 지금 가격(${PX:.2f})은 이 값의 {PX / iv:.2f}배다.</td>
        </tr>
'''
sub(r'(<thead><tr><th>기둥</th><th>금액</th><th>주당</th><th class="story">무엇인가</th></tr></thead>\n      <tbody>\n).*?(      </tbody>)',
    lambda m: m.group(1) + TB + m.group(2))
sub(r'<div class="note">요구수익률을 9%로[^<]*</div>',
    f'<div class="note">요구수익률을 9%로 낮추면 ${P["iv_9"]:.2f}, 11%로 높이면 ${P["iv_11"]:.2f}다. 사업 이익이 최근 5년 중 가장 낮았던 해 수준이면 ${P["iv_low"]:.2f}다.</div>')
sub(r'<div class="note">보험 플로트\(\$[\d.,]+B\)가',
    f'<div class="note">보험 플로트({B(Q["float"], 1)})가')

# ── 2. 기본적 분석: 차트·박스 ──────────────────────────────────────────────
sub(r'분기 매출 / 순이익 / 세후 영업이익률 \([^)]*\)', f'분기 매출 / 순이익 / 세후 영업이익률 ({L8[0]}~{L8[-1]})')
sub(r"const revenue=\[[^\]]*\];", f"const revenue={json.dumps(rev8).replace(' ', '')};")
sub(r"const netIncome=\[[^\]]*\];", f"const netIncome={json.dumps(ni8).replace(' ', '')};")
sub(r"const opm=\[[^\]]*\];", f"const opm={json.dumps(opm8).replace(' ', '')};")
sub(r"(const opm=\[[^\]]*\];.*?labels:)\[[^\]]*\]", lambda m: m.group(1) + "[" + ",".join(f"'{x}'" for x in L8) + "]")
sub(r'<div class="stat-label">FCF \([^)]*\)</div>\n      <div class="stat-value">[^<]*</div>',
    f'<div class="stat-label">FCF ({QL})</div>\n      <div class="stat-value">{B(Q["fcf"], 1)}</div>')
sub(r'<div class="stat-label">Capex \([^)]*\)</div>\n      <div class="stat-value">[^<]*</div>',
    f'<div class="stat-label">Capex ({QL})</div>\n      <div class="stat-value">{B(Q["capex"], 1)}</div>')
if Q["float_ytd_change"] is not None:
    FL_NOTE = f"연초 대비 {'+' if Q['float_ytd_change'] >= 0 else '−'}${abs(Q['float_ytd_change']) / 1e9:.1f}B"
else:
    try:
        _pf = bq.float_of(bq.doc_for(bq.prev_q(L), ASOF)[3])[0]
        FL_NOTE = f"직전 분기 ${_pf:.1f}B"
    except bq.BrkbParseError:
        FL_NOTE = "회사 공시 근사값"
sub(r'<div class="stat-label">보험 플로트 \([^)]*\)</div>\n      <div class="stat-value">[^<]*</div>\n      <div class="stat-sub">[^<]*</div>',
    f'<div class="stat-label">보험 플로트 ({dot(L)})</div>\n      <div class="stat-value">{B(Q["float"], 1)}</div>\n      <div class="stat-sub">{FL_NOTE}</div>')
sub(r'<div class="stat-label">다음 실적</div>\n      <div class="stat-value">[^<]*</div>\n      <div class="stat-sub">[^<]*</div>',
    f'<div class="stat-label">다음 실적</div>\n      <div class="stat-value">{NEXT_DAY.month}월 {NEXT_DAY.day}일 무렵 예상</div>\n      <div class="stat-sub">일정 · {NL} (작년과 같은 달 같은 번째 토요일로 추정)</div>')

# ── 3. 재무 건전성 ────────────────────────────────────────────────────────
sub(r'재무 건전성 — 안정성·활동성 \([^)]*\)', f'재무 건전성 — 안정성·활동성 ({QL} · {dot(L)} 기준)')
fy_e = f"{y if L.endswith('12-31') else y - 1}-12-31"
a1, a0 = bq.bal("Assets", [], fy_e, ASOF), bq.bal("Assets", [], f"{int(fy_e[:4]) - 1}-12-31", ASOF)
eq = bq.bal("StockholdersEquity", [], L, ASOF)
liab = bq.bal("Liabilities", [], L, ASOF)
dd_ = debt / assets * 100 if assets else None
de_ = liab / eq * 100 if liab and eq else None
sub(r'(<span class="diag-label">차입금의존도</span><span class="diag-value">)[^<]*', lambda m: m.group(1) + (f"{dd_:.1f}%" if dd_ else "—"))
sub(r'(<span class="diag-label">부채비율</span><span class="diag-value">)[^<]*', lambda m: m.group(1) + (f"{de_:.1f}%" if de_ else "—"))
if a1 and a0:
    sub(r'(<span class="diag-label">총자산증가율</span><span class="diag-value">)[^<]*(</span><span class="diag-note">)[^<]*',
        lambda m: m.group(1) + pct(pc(a1, a0)) + m.group(2) + f"FY{fy_e[2:4]} {B(a1, 1)}(전기 {B(a0, 1)}) · 연간 지표, FY{int(fy_e[2:4]) + 1:02d} 마감 전까지 동일")
nc = cash_all - debt
sub(r'(id="fundNetCashPs">)[^<]*(</span><span class="diag-note" id="fundNetCashNote">)[^<]*',
    lambda m: m.group(1) + f"${nc / sharesB:.2f}" + m.group(2)
    + f"순현금 {B(nc, 1)} ÷ {sharesB / 1e9:.2f}B주 · 현금·국채 {B(cash_all, 1)}(철도·에너지 현금 포함) − 차입금 {B(debt, 1)} · 리스부채 제외")
sub(r'(<span class="diag-label">현금·국채 \(보험·기타\)</span><span class="diag-value">)[^<]*(</span><span class="diag-note">)현금 [^·]*·',
    lambda m: m.group(1) + B(cash_io, 1) + m.group(2) + f"현금 {B(Q['cash_io'], 1)} + 단기 국채 {B(Q['tbills'], 1)}(미지급금 {B(P['payable'], 1)} 차감 전) ·")
sub(r'(<span class="diag-label">보험 플로트</span><span class="diag-value">)[^<]*(</span><span class="diag-note">)[^·<]*·',
    lambda m: m.group(1) + B(Q["float"], 1) + m.group(2) + f"{FL_NOTE} ·")
KO = {"Alphabet Inc.": "알파벳", "American Express Company": "아메리칸 익스프레스", "Apple Inc.": "애플",
      "Bank of America Corporation": "뱅크오브아메리카", "The Coca-Cola Company": "코카콜라", "Chevron Corporation": "셰브론",
      "Occidental Petroleum Corporation": "옥시덴탈", "The Kraft Heinz Company": "크래프트하인즈", "Moody’s Corporation": "무디스",
      "Moody's Corporation": "무디스", "Chubb Limited": "처브", "Mitsubishi Corporation": "미쓰비시상사"}
top5 = "·".join(KO.get(x, x) for x in Q["top5"])
sub(r'(<span class="diag-label">상장주식 공정가치</span><span class="diag-value">)[^<]*(</span><span class="diag-note">)[^<]*',
    lambda m: m.group(1) + B(Q["eq_fv"], 1) + m.group(2) + (f"상위 5종목({top5})이 {Q['top5_pct']}%" if top5 else f"상위 5종목이 {Q['top5_pct']}%"))
_mult = cash_io / debt
_rue_sh = Q["debt_rue"] / debt * 100
sub(r'현금과 단기 국채만 \$[\d.,]+B로 차입금 \$[\d.,]+B의 [^,]*, 차입금의 [^<]*자회사 몫이다\.',
    f'현금과 단기 국채만 {B(cash_io, 1)}로 차입금 {B(debt, 1)}의 {_mult:.1f}배이고, 차입금의 {_rue_sh:.0f}%는 철도·유틸리티·에너지 자회사 몫이다.')

# FUNDAMENTAL 블록(보험지주 — 점수 없이 값만): 기준일·접수일, 차입금의존도·부채비율·매출 CAGR
F = json.loads(re.search(r"const BRKB_FUNDAMENTAL = (\{.*?\});\n", h, re.S).group(1))
F["asOf"], F["filedAt"] = L, Q["filed"]
_tmp = os.path.join(V2, ".sec_cache", "_work", "BRKB_fund.json")
os.makedirs(os.path.dirname(_tmp), exist_ok=True)
_r = subprocess.run([sys.executable, os.path.join(V2, "build_fundamental_score.py"), T, "--json", _tmp], capture_output=True, text=True)
_bf = json.load(open(_tmp)) if _r.returncode == 0 and os.path.exists(_tmp) else None
_bf_rows = {r_["metric"]: r_ for ax in (_bf or {}).get("axes", {}).values() for r_ in ax.get("rows", [])}
for ax in F["axes"].values():
    for r_ in ax["rows"]:
        if r_["metric"] == "debtDependency":
            r_["value"] = dd_
        elif r_["metric"] == "debtToEquity":
            r_["value"] = de_
        elif r_["metric"] == "revenueCagr" and _bf and _bf.get("asOf") == L:
            r_["value"] = _bf_rows.get("revenueCagr", {}).get("value", r_["value"])
sub(r"const BRKB_FUNDAMENTAL = \{.*?\};\n", lambda m: "const BRKB_FUNDAMENTAL = " + json.dumps(F, ensure_ascii=False) + ";\n")

# ── 4. 최신 분기 핵심 재무 YoY/QoQ ──────────────────────────────────────────
def cmp_block(key, cl, cs, ce, vals_c):
    cur = [Q["rev"], S["oper"] * 1e6, Q["ni"], Q["fcf"]]
    dl = [pct(pc(a, b)) if b and b > 0 and a is not None else ("적자 전환" if b and b > 0 and a < 0 else "—") for a, b in zip(cur, vals_c)]
    fn = (f"기준일: {dot(L)}({QL}) vs {dot(ce)}({cl}) · 매출·순이익(지배주주)은 GAAP · FCF는 영업현금흐름 − 설비투자(비GAAP) · "
          f"영업이익은 회사 정의 세후(투자 평가손익·영업권 손상 제외) · " + SRC.replace("'", "\\'"))
    r1 = lambda v: round(v / 1e9, 1)
    return (f"  {key}: {{\n    curLabel: '{QL}', cmpLabel: '{cl}',\n    titleSuffix: '{cs} ({QL} vs {cl})',\n"
            f"    chart: {{ cur: {json.dumps([r1(v) for v in cur])}, cmp: {json.dumps([r1(v) for v in vals_c])} }},\n"
            f"    deltas: {json.dumps(dl, ensure_ascii=False)},\n    footnote: '{fn}'\n  }}")


FC = ("const FUND_COMPARE = {\n" + cmp_block("yoy", YL, "YoY", bq.year_ago(L), [Q["rev_yo"], SY["oper"] * 1e6, Q["ni_yo"], Q["fcf_yo"]]) + ",\n"
      + cmp_block("qoq", PL, "QoQ", bq.prev_q(L), [Q["rev_prev"], SP["oper"] * 1e6, Q["ni_prev"], Q["fcf_prev"]]) + "\n};")
sub(r"const FUND_COMPARE = \{.*?\n\};", lambda m: FC)
sub(r'(<span id="fundPeriodTitle">)YoY \([^)]*\)', lambda m: m.group(1) + f"YoY ({QL} vs {YL})")

# ── 5. 영업이익 구성 도넛 ─────────────────────────────────────────────────
SEGS = [("보험 인수", "uw", "#7c6ad6"), ("보험 투자수익", "invinc", "#7c6ad6"), ("BNSF", "rail", "#3b82f6"),
        ("BHE", "energy", "#1abc9c"), ("제조·서비스·소매", "msr", "#d4a017"), ("기타", "other", "#94a3b8")]
sv = {k: S[k] for _, k, _ in SEGS}
sv["other"] += sum(v for k, v in S.items() if k.startswith("x:"))   # 표에만 있는 사업 행(2024 Pilot 등)은 기타에
tot = sum(sv.values())
leg = "".join(f'          <div style="display:flex;align-items:center;gap:7px;font-size:11px;color:var(--text2);white-space:nowrap;"><span style="width:8px;height:8px;border-radius:50%;background:{c};display:inline-block;flex-shrink:0;"></span>{lab} <strong style="color:var(--text);">{B(sv[k] * 1e6, 2)} · {sv[k] / tot * 100:.1f}%</strong></div>\n'
              for lab, k, c in SEGS)
sub(r'영업이익 구성 — 사업별 세후 \([^)]*\)', f'영업이익 구성 — 사업별 세후 ({QL} · {dot(L)} 기준)')
sub(r'(<div style="display:flex;flex-direction:column;gap:9px;">\n)(?:\s*<div style="display:flex;align-items:center;gap:7px;font-size:11px;[^\n]*\n)+',
    lambda m: m.group(1) + leg)
_neg = [lab for lab, k, _ in SEGS if sv[k] < 0]
sub(r'<div class="yoy-footnote" style="margin-top:14px;">출처: .*?</div>',
    f'<div class="yoy-footnote" style="margin-top:14px;">출처: {SRC} · 회사 정의 세후 영업이익 {B(tot * 1e6, 2)}(투자 평가손익·손상 제외)'
    + (f' · {"·".join(_neg)}는 손실이라 도넛에서 0으로 그렸다' if _neg else '')
    + (f' · 기타에는 외화 차입금 환산 손익(세후) {"+" if FX[0] >= 0 else "−"}${abs(FX[0]):,.0f}M(1년 전 {"+" if FX[1] >= 0 else "−"}${abs(FX[1]):,.0f}M)이 들어 있다' if FX else '') + '</div>')
sub(r"// ─── 영업이익 구성 도넛 차트 \([^)]*\) ───", f"// ─── 영업이익 구성 도넛 차트 ({QL} {FORM}, 세후 $M) ───")
sub(r"(function renderSegmentChart\(\) \{.*?const total = )-?\d+;", lambda m: m.group(1) + f"{round(sum(max(v, 0) for v in sv.values()))};")
sub(r"(labels:\[\"보험 인수\"[^\]]*\],\n      datasets:\[\{\n        data:)\[[^\]]*\]",
    lambda m: m.group(1) + json.dumps([round(max(sv[k], 0)) for _, k, _ in SEGS]))

# ── 6. 자본배분 ───────────────────────────────────────────────────────────
md = f"{d(L).month}/{d(L).day}"
ZL = f'''        <div class="zone-item">
          <span class="zone-label">자사주 매입 ({QL})</span>
          <div style="display:flex;align-items:center;gap:8px;">
            <span class="zone-tag" style="background:rgba(212,160,23,0.18);color:var(--gold);">연초~{md} {B(Q["buyback_ytd"], 1) if Q["buyback_ytd"] else "없음"}</span>
            <span class="zone-val">{B(Q["buyback"], 1) if Q["buyback"] else "없음"}</span>
          </div>
        </div>
        <div class="zone-item">
          <span class="zone-label">사업 인수 (연초~{md}, 현금)</span>
          <span class="zone-val">{B(Q["acq_ytd"], 1) if Q["acq_ytd"] else "없음"}</span>
        </div>
        <div class="zone-item">
          <span class="zone-label">현금·국채 (보험·기타)</span>
          <span class="zone-val">{B(cash_io, 1)}</span>
        </div>
        <div class="zone-item">
          <span class="zone-label">배당</span>
          <span class="zone-val">없음 (1967년 이후)</span>
        </div>
'''
sub(r'(<div class="card-title">)자본배분 · 주주환원 \([^)]*\)(</div>\n      <div class="zone-list">\n).*?(      </div>\n      <div class="yoy-footnote" style="margin-top:10px;">)',
    lambda m: m.group(1) + f"자본배분 · 주주환원 ({QL} · {dot(L)} 기준)" + m.group(2) + ZL + m.group(3))
sub(r'(<div class="yoy-footnote" style="margin-top:10px;">자사주는 CEO가 회장과 협의해 내재가치보다 싸다고 볼 때만 산다\(한도 없음\)\. 1967년 이후 현금배당이 없다\. 출처: ).*?(</div>)',
    lambda m: m.group(1) + (f'<a href="{PRESS}" target="_blank" rel="noopener">{QL} 보도자료</a> · ' if PRESS else "")
    + f'<a href="{TENQ}" target="_blank" rel="noopener">{QL} {FORM}</a> · 자사주는 자본변동표의 취득 원가(현금흐름표 지급액과 다를 수 있다) · 사업 인수는 현금흐름표의 인수 지출(취득 현금 차감, 소규모 인수 포함)' + m.group(2))

# ── 7. 다음 실적 체크포인트 ─────────────────────────────────────────────────
try:
    NS = bq.seg_quarter(NA, ASOF)[0]
except bq.BrkbParseError:
    NS = None
B6 = lambda v: B(v * 1e6, 2)
_ytd_txt = "" if qn == 1 else f", 연초~{md} {B(Q['buyback_ytd'], 1) if Q['buyback_ytd'] else '없음'}"
ck = [f"자사주 매입이 이어지는지 ({QK} {B(Q['buyback'], 1)}{_ytd_txt})" if Q["buyback"]
      else f"자사주 매입을 다시 시작하는지 ({QK} 없음{_ytd_txt})"]
if NS:
    ck += [f"보험 인수이익이 {NAL} {B6(NS['uw'])}를 넘는지 (직전 분기 {B6(S['uw'])})",
           f"보험 투자수익이 {NAL} {B6(NS['invinc'])}를 넘는지 (직전 분기 {B6(S['invinc'])})",
           f"회사 영업이익(세후)이 {NAL} {B6(NS['oper'])}를 넘는지 (직전 분기 {B6(S['oper'])})"]
CK = "\n".join(f'      <div{" style=\"margin-bottom:8px;\"" if i < len(ck) - 1 else ""}><strong style="color:var(--accent2);">{"①②③④"[i]}</strong> {t_}</div>' for i, t_ in enumerate(ck))
sub(r'(<div class="card-title">다음 실적 체크포인트 <span[^>]*>)[^<]*(</span></div>\n    <div style="font-size:12px;color:var\(--text2\);line-height:1.8;">\n).*?(\n    </div>)',
    lambda m: m.group(1) + CHECK_WHEN + m.group(2) + CK + m.group(3))

# ── 8. 밸류에이션 탭 · 투자의견 · DCF 참고값 ─────────────────────────────────
sub(r'두 기둥 참고값 <strong>\$[\d,]+</strong> · 현재가는 그 [\d.]+배', f'두 기둥 참고값 <strong>${iv:.0f}</strong> · 현재가는 그 {PX / iv:.2f}배')
oper_ttm = sum(bq.seg_quarter(e, ASOF)[0]["oper"] for e in ends[-4:]) * 1e6
_gap = (P["op_norm"] / oper_ttm - 1) * 100
_ii = pc(S["invinc"], SY["invinc"])
sub(r'<div class="verdict-summary-risk">⚠️ 정상화 PER의 이익은.*?</div>',
    f'<div class="verdict-summary-risk">⚠️ 정상화 PER의 이익은 순이익에서 투자·파생 손익을 빼고 손상을 되돌린 우리 정의로, 회사가 밝힌 영업이익과 최근 4분기 {abs(_gap):.1f}% 차이다. '
    + (f'{QK} 보험 투자수익({B6(S["invinc"])})은 1년 전보다 {abs(_ii):.1f}% {"줄었고" if _ii < 0 else "늘었고"}, ' if _ii is not None else '')
    + '보험 투자수익이 줄면 같은 주가에서도 PER이 올라간다.</div>')
sub(r'(<span class="op-label">다음 실적</span>\n        <span class="op-val">)[^<]*<span class="op-sub">[^<]*</span>',
    lambda m: m.group(1) + f'{NEXT_DAY.month}월 {NEXT_DAY.day}일 무렵 <span class="op-sub">{NL} 예상</span>')
DCF = json.loads(re.search(r"const BRKB_DCF = (\{.*?\});", h, re.S).group(1))
DCF["unavailable"] = f"보험지주라 현금흐름 모델 미적용, 두 기둥 참고값 ${iv:.0f}은 판정 미반영"
DCF["asOf"] = SESSION
DCF["reference"].update({"value": round(iv, 2), "invest": round(p1ps, 2), "operating": round(e2ps, 2), "at9": round(P["iv_9"], 2),
                         "at11": round(P["iv_11"], 2), "low": round(P["iv_low"], 2), "quarter": L})
sub(r"const BRKB_DCF = \{.*?\};", lambda m: "const BRKB_DCF = " + json.dumps(DCF, ensure_ascii=False) + ";")

# ── 9. 뉴스 타임라인 · 종합 해석 ───────────────────────────────────────────
days = [r_[0] for r_ in D]
first_session = lambda day: next((x for x in days if x >= day), None)


def tl_item(dot_, date, react, title, href, src, auto=False):
    rx = f'<span class="tl-reaction flat" data-react="{react}">0.0%</span>' if react else ""
    return (f'      <div class="tl-item"{" data-auto=\"earn\"" if auto else ""}>\n        <div class="{("tl-dot " + dot_).strip()}"></div>\n'
            f'        <div class="tl-date">{date}{rx}</div>\n        <div class="tl-title">{title}</div>\n'
            f'        <a class="tl-source" href="{href}" target="_blank" rel="noopener">{src} →</a>\n      </div>')


tl_m = re.search(r'    <div class="timeline" id="newsTimeline">\n(.*?)\n    </div>\n    <div class="tl-pager"', h, re.S)
old_items = re.findall(r'      <div class="tl-item".*?\n      </div>', tl_m.group(1), re.S)
KD = lambda s_: (lambda m: dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else None)(re.search(r"(\d{4})년 (\d+)월 (\d+)일", s_))
keep = []
for it in old_items:
    if 'data-auto="earn"' in it or re.search(r"— Q[1-4] \d{4} 실적", it):   # 실적 항목은 아래에서 다시 만든다
        continue
    dd = KD(it)
    if dd and (d(SESSION) - dd).days <= 460:
        keep.append((dd, it))
earn = []
for e in reversed(ends[-4:]):
    try:
        fe = bq.doc_for(e, ASOF)[2]
    except bq.BrkbParseError:
        continue
    rd = release_day(fe)
    rx = first_session((rd + dt.timedelta(days=1)).isoformat())
    if rx is None:
        continue
    cs, cy = bq.seg_quarter(e, ASOF)
    qq = bq.quarter(e, ASOF) if e == L else None
    t_ = f"회사 영업이익 {B6(cs['oper'])}({pct(pc(cs['oper'], cy['oper']))}) · 보험 인수이익 {B6(cs['uw'])}(1년 전 {B6(cy['uw'])})"
    if qq:
        t_ += f" · 플로트 {B(qq['float'], 1)}" + (f" · 자사주 {B(qq['buyback'], 1)} 매입" if qq["buyback"] else "")
    pu = press(e)
    rxd = d(rx)
    earn.append((rd, tl_item("", f"{rd.year}년 {rd.month}월 {rd.day}일({WD[rd.weekday()]}) 발표 · {rxd.month}월 {rxd.day}일 반응 — {qlab(e)} 실적",
                             rx, t_, pu or doc_url(bq.doc_for(e, ASOF)[3]) or TENQ, "Berkshire 실적 보도자료 (SEC 8-K)" if pu else f"Berkshire {qlab(e)} (SEC)", auto=True)))
items = sorted(earn + keep, key=lambda x: x[0], reverse=True)
sub(r'(    <div class="timeline" id="newsTimeline">\n).*?(\n    </div>\n    <div class="tl-pager")',
    lambda m: m.group(1) + "\n".join(it for _, it in items) + m.group(2))
_ds = [x[0] for x in items]
sub(r'<div class="section-title">시계열 주요 뉴스 \([^)]*\)</div>',
    f'<div class="section-title">시계열 주요 뉴스 ({min(_ds).year}.{min(_ds).month:02d} ~ {max(_ds).year}.{max(_ds).month:02d})</div>')

oy = pc(S["oper"], SY["oper"])
ni_ins, ni_ins_y = NONINS(S), NONINS(SY)
_bb = (f"자사주를 {QK}에 {B(Q['buyback'], 1)}" + ("" if qn == 1 else f"(연초부터 {B(Q['buyback_ytd'], 1)})") + " 샀" if Q["buyback"]
       else f"{QK}에는 자사주를 사지 않았" + (f"(연초부터 {B(Q['buyback_ytd'], 1)})" if Q["buyback_ytd"] else ""))
bul = [f"보험 밖 사업(BNSF·BHE·제조·서비스·소매) 세후 이익은 {B6(ni_ins)}({vs(ni_ins, ni_ins_y)}), 보험 인수이익은 {B6(S['uw'])}({vs(S['uw'], SY['uw'])}), 보험 투자수익은 {B6(S['invinc'])}({vs(S['invinc'], SY['invinc'])})였다.",
       _bb + (f"고, 사업 인수에는 연초부터 현금 {B(Q['acq_ytd'], 1)}를 썼다." if Q["acq_ytd"] else "다."),
       f"현금·국채(보험·기타)는 {B(cash_io, 1)}, 보험 플로트는 {B(Q['float'], 1)}({FL_NOTE})다."]
if FX:   # 기타의 외화 환산 손익을 빼면 — 헤드라인 증가율의 상당 부분이 이 손익일 수 있다(Fable)
    _ex, _exy = S["oper"] - FX[0], SY["oper"] - FX[1]
    bul.insert(1, f"기타에 든 외화 차입금 환산 손익(세후 {'+' if FX[0] >= 0 else '−'}${abs(FX[0]):,.0f}M, 1년 전 {'+' if FX[1] >= 0 else '−'}${abs(FX[1]):,.0f}M)을 빼면 회사 영업이익은 {B6(_ex)}({vs(_ex, _exy)})다.")
_neg_c = sorted([(pc(S[k], SY[k]), n_) for k, n_ in (("uw", "보험 인수이익"), ("invinc", "보험 투자수익"), ("msr", "제조·서비스·소매"), ("rail", "BNSF"), ("energy", "BHE"))
                 if pc(S[k], SY[k]) is not None and pc(S[k], SY[k]) < -5])
CTR = ("⚠️ 1년 전 대비 " + ", ".join(f"{n_} {pct(v)}" for v, n_ in _neg_c[:2]) + f". 순이익에는 투자 평가손익(세후 {B6(S['gains'])})이 들어 있어 분기마다 크게 흔들린다."
       if _neg_c else f"⚠️ 순이익에는 투자 평가손익(세후 {B6(S['gains'])})이 들어 있어 분기마다 크게 흔들린다. 현금·국채 {B(cash_io, 1)}는 자본의 {cash_io / eq * 100:.0f}%다.")
_tag = ("영업이익 증가" if oy is not None and oy > 2 else "영업이익 감소" if oy is not None and oy < -2 else "영업이익 보합") + " · 판정 보류"
SUM = (f'<div class="verdict-summary-head">지배적 내러티브 · {QL} 회사 영업이익 {B6(S["oper"])}({pct(oy)}), 순이익 {B(Q["ni"], 1)}<span class="tag">{_tag}</span></div>\n'
       '    <ol class="news-list">\n' + "\n".join(f"      <li>{x}</li>" for x in bul) + "\n    </ol>\n"
       f'    <div class="verdict-summary-counter">{CTR}</div>\n'
       f'    <div class="verdict-summary-next">🔍 다음 확인 포인트 · {CHECK_WHEN} 실적 발표.</div>')
sub(r'<div class="verdict-summary-head">지배적 내러티브.*?<div class="verdict-summary-next">.*?</div>', lambda m: SUM)

# ── 10. 핵심 투자 포인트(규칙 후보 → 강세·약세 셋씩) ─────────────────────────
cand = []
cand.append(("현금", 1.0 if cash_io >= 100e9 else 0.0, f"현금·국채(보험·기타) {B(cash_io, 1)}로 차입금 {B(debt, 1)}의 {_mult:.1f}배다."))
_gi = pc(ni_ins, ni_ins_y)
if _gi is not None and abs(_gi) >= 5:   # 보험 밖 사업은 한 줄로(BNSF·BHE·제조가 각각 셋 자리를 다투지 않게, Fable)
    cand.append(("보험 밖 사업", 0.85 * (1 if _gi > 0 else -1),
                 f"{QK} 세후 이익 {B6(ni_ins)}({pct(_gi)}) — BNSF {vs(S['rail'], SY['rail'])}, BHE {vs(S['energy'], SY['energy'])}, 제조·서비스·소매 {vs(S['msr'], SY['msr'])}."))
for k, head in (("uw", "보험 인수"), ("invinc", "보험 투자수익")):
    g = pc(S[k], SY[k])
    if g is not None and abs(g) >= 5:
        cand.append((head, 0.9 * (1 if g > 0 else -1), f"{QK} {'보험 인수이익' if k == 'uw' else '보험 투자수익'} {B6(S[k])}, 1년 전 {B6(SY[k])}보다 {abs(g):.1f}% {'늘었다' if g > 0 else '줄었다'}."))
if Q["buyback"]:
    cand.append(("자사주", 0.8, f"{QK}에 {B(Q['buyback'], 1)}를 샀다" + ("" if qn == 1 else f"(연초부터 {B(Q['buyback_ytd'], 1)})") + ". 회사는 내재가치보다 쌀 때만 산다고 밝혀 왔다."))
if Q["float_ytd_change"]:
    cand.append(("플로트", 0.5 if Q["float_ytd_change"] > 0 else -0.5, f"보험 플로트 {B(Q['float'], 1)}, {FL_NOTE}."))
if Q["top5_pct"] >= 60:
    cand.append(("집중", -0.5, f"상장주식 {B(Q['eq_fv'], 1)}의 {Q['top5_pct']}%가 5종목에 몰려 있다."))
seen = set()
cand = [c_ for c_ in sorted(cand, key=lambda c_: -abs(c_[1])) if c_[1] != 0 and not (c_[0] in seen or seen.add(c_[0]))]
bull = [c_ for c_ in cand if c_[1] > 0][:3] or [("—", 1, "기준을 넘는 강세 지표가 없다.")]
bear = [c_ for c_ in cand if c_[1] < 0][:3] or [("—", -1, "기준을 넘는 약세 지표가 없다.")]
row = lambda k, head, t_: f'      <div class="bb-row {k}"><span class="bb-icon">{"▲" if k == "bull" else "▼"}</span><span class="bb-head">{head}</span><span class="bb-text">{t_}</span></div>\n'
sub(r'(<div class="bb-title bb-bull">🐂 Bull 요인</div>\n)(?:\s*<div class="bb-row bull">.*?</div>\n)+', lambda m: m.group(1) + "".join(row("bull", a, t_) for a, _, t_ in bull))
sub(r'(<div class="bb-title bb-bear">🐻 Bear 요인</div>\n)(?:\s*<div class="bb-row bear">.*?</div>\n)+', lambda m: m.group(1) + "".join(row("bear", a, t_) for a, _, t_ in bear))

if DRY:
    print(f"BRKB 채우기(시험): {QL}({Q['doc']}, 접수 {Q['filed']}) · 바꾼 자리 {_n['subs']}곳 · 쓰지 않음")
else:
    open(CARD, "w", encoding="utf-8").write(h)
    print(f"BRKB 채우기: {QL}({Q['doc']}, 접수 {Q['filed']}) · 두 기둥 ${iv:.2f} · 다음 실적 {NEXT_TXT} · 바꾼 자리 {_n['subs']}곳")
