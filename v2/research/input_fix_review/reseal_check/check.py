# 수익률 없는 점검 마무리 — 입력·판정만 본다. 수익률·평가일 뒤 가격·결과 파일은 읽지 않는다.
import sys, json, copy, collections
R = "/Users/watermountain/Workspace/stock-widgets-preview/v2/research"
sys.path.insert(0, R)
import verdict_replay as vr
OLD = json.load(open("/Users/watermountain/Workspace/stock-widgets-preview/.regress_20261010/panels/gate_test_stored_20261008.json"))["rows"]  # 옛 시험 패널(10-08)
NEW = json.load(open(sys.argv[1]))["rows"]
mem = json.load(open(f"{R}/gate_membership.json"))["tickers"]
def prep(rows):
    rows = copy.deepcopy(rows)
    for r in rows:
        if "px_then" in r: r["_px"], r["px"] = r["px"], r["px_then"]
    vr.peer_scores(rows); vr.assign(rows)
    return rows
O, N = prep(OLD), prep(NEW)
ko = {(r["t"], r["m"]): r for r in O}
bad = lambda r: any(str(x).startswith(("debt_suspect", "shares_missing")) for x in (r.get("dq") or []))
print("## 1. 10-09 예외 16행")
EXC = {"UDR": [f"2022-{m:02d}" for m in range(4, 13)] + ["2023-01"], "ETN": ["2022-02", "2022-03"], "VRT": ["2024-02", "2024-03"], "VTRS": ["2024-02", "2024-03"]}
for r in N:
    if r["m"] in EXC.get(r["t"], []):
        o = ko[(r["t"], r["m"])]
        print(r["t"], r["m"], "dcf_ok", o["dcf_ok"], "->", r["dcf_ok"], "base", o.get("base"), "->", r.get("base"), "lv", o.get("lv_V0"), "->", r.get("lv_V0"))
print("## 2. 리츠·태그 전환 종목: 기본 내재가치 음수 행·V0 분포 (전 -> 후)")
for t in ["UDR", "AMT", "CCI", "ESS", "EXR", "CPT", "SBAC", "IRM", "DOC", "INVH", "URI", "DVN", "GD"]:
    a = [r for r in O if r["t"] == t]; b = [r for r in N if r["t"] == t]
    neg = lambda rs: sum(1 for r in rs if r["dcf_ok"] and (r.get("base") or 0) <= 0)
    dist = lambda rs: dict(collections.Counter(r["lv_V0"] for r in rs if r["lv_V0"]).most_common())
    print(t, len(a), "dcf_ok", sum(r["dcf_ok"] for r in a), "->", sum(r["dcf_ok"] for r in b), "| base<=0", neg(a), "->", neg(b), "|", dist(a), "->", dist(b))
print("## 3. 부분 차입금 12종목: debt_total_fallback 행 / debt_suspect 행 (전 -> 후)")
for t in ["A", "ADI", "DRI", "EQIX", "KLAC", "LIN", "OMC", "PTC", "RMD", "TRMB", "TTWO", "VTR"]:
    a = [r for r in O if r["t"] == t]; b = [r for r in N if r["t"] == t]
    c = lambda rs, p: sum(1 for r in rs if any(str(x).startswith(p) for x in (r.get("dq") or [])))
    print(t, "fallback", c(b, "debt_total_fallback"), "| suspect", c(a, "debt_suspect"), "->", c(b, "debt_suspect"))
print("## 4. dq 필터 범위 — 필터(debt_suspect·shares_missing)를 통과해 평가 행에 남는 표식")
def scope(rows, tag):
    ev = [r for r in rows if not bad(r) and mem.get(r["t"], {}).get("status") != "ambiguous"]
    c = collections.Counter()
    for r in ev:
        for p in {str(x).split(":")[0] for x in (r.get("dq") or [])}: c[p] += 1
    print(tag, "필터 통과", len(ev), dict(c.most_common()))
scope(O, "전"); scope(N, "후")
print("## 5. 구성 불명(ambiguous) 종목 행")
for t, v in mem.items():
    if v["status"] == "ambiguous":
        print(t, sum(1 for r in N if r["t"] == t), v["note"])
print("## 6. S1 민감도 — 자기 이력에서 PER을 뺀 판정 (새 패널)")
P = copy.deepcopy(N)
for r in P: r["self"] = {k: v for k, v in r["self"].items() if k != "PER"}
vr.assign(P)
sv = sum(1 for a, b in zip(N, P) if a["self_vote"] != b["self_vote"])
gv = sum(1 for a, b in zip(N, P) if a["g_V0"] != b["g_V0"])
print("행", len(N), "self_vote 바뀜", sv, "g_V0 바뀜", gv)
print("## 7. 월별 dcf_ok·판정률 (전 -> 후, 연 단위 요약)")
for y in ["2021", "2022", "2023", "2024"]:
    a = [r for r in O if r["m"].startswith(y)]; b = [r for r in N if r["m"].startswith(y)]
    f = lambda rs: (round(100 * sum(r["dcf_ok"] for r in rs) / len(rs), 1), round(100 * sum(1 for r in rs if r["g_V0"]) / len(rs), 1))
    print(y, len(a), "dcf_ok%·판정%", f(a), "->", f(b))
print("## 8. 칸별 표 분포 (전 -> 후)")
for f in ("self_vote", "peer_vote", "lv_V0", "g_V0"):
    print(f, dict(sorted(collections.Counter(str(r.get(f)) for r in O).items())), "->", dict(sorted(collections.Counter(str(r.get(f)) for r in N).items())))
print("## 9. 월별 dcf_ok%·dq필터 제외%·판정% (전 -> 후)")
for m in sorted({r["m"] for r in N}):
    g = [r for r in N if r["m"] == m]; go = [r for r in O if r["m"] == m]
    f = lambda rs: (round(100*sum(r["dcf_ok"] for r in rs)/len(rs),1), round(100*sum(bad(r) for r in rs)/len(rs),1), round(100*sum(1 for r in rs if r["g_V0"])/len(rs),1))
    print(m, len(g), f(go), "->", f(g))
print("## 10. 종합 판정 변화")
ch = [(r["t"], r["m"]) for r in N if ko[(r["t"], r["m"])]["g_V0"] != r["g_V0"]]
print("g_V0 바뀜", len(ch), "종목", len({t for t, _ in ch}))
print("## 11. IRM 옛 양수 행", [(r["m"], round(r["base"], 1)) for r in O if r["t"] == "IRM" and (r.get("base") or 0) > 0])
