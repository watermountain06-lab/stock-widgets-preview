# 수익률 없는 재봉인 점검(2026-10-26, 낡은 재무상태표 수정) — 입력·판정만 본다. 수익률·평가일 뒤 가격·결과 파일은 읽지 않는다.
# 사용: python3 check.py 옛패널.json 새패널.json   (옛 = 10-11 봉인 패널, 새 = 이번 재생성)
import sys, json, copy, collections
R = "/Users/watermountain/Workspace/stock-widgets-preview/v2/research"
sys.path.insert(0, R)
import verdict_replay as vr
L = lambda p: (lambda d: d["rows"] if isinstance(d, dict) else d)(json.load(open(p)))
OLD, NEW = L(sys.argv[1]), L(sys.argv[2])
mem = json.load(open(f"{R}/gate_membership.json"))["tickers"]
def prep(rows):
    rows = copy.deepcopy(rows)
    for r in rows:
        if "px_then" in r: r["_px"], r["px"] = r["px"], r["px_then"]
    vr.peer_scores(rows); vr.assign(rows)
    return rows
O, N = prep(OLD), prep(NEW)
ko = {(r["t"], r["m"]): r for r in O}
has = lambda r, *p: any(str(x).startswith(p) for x in (r.get("dq") or []))
bad_old = lambda r: has(r, "debt_suspect", "shares_missing")            # 바꾸기 전 필터
bad_new = lambda r: has(r, "debt_suspect", "shares_missing", "dcf_hold")  # 2026-10-26 필터
ev = lambda rs: [r for r in rs if mem.get(r["t"], {}).get("status") != "ambiguous"]
print("## 1. dq 필터 통과 행 (구성 불명 제외)")
print("옛 패널·옛 필터", sum(not bad_old(r) for r in ev(O)), "/", len(ev(O)))
print("새 패널·옛 필터", sum(not bad_old(r) for r in ev(N)), "/", len(ev(N)))
print("새 패널·새 필터", sum(not bad_new(r) for r in ev(N)), "/", len(ev(N)))
H = [r for r in ev(N) if has(r, "dcf_hold")]
print("dcf_hold 행", len(H), "종목", len({r["t"] for r in H}), "| 다른 필터 표식 없이 새로 빠짐", sum(not bad_old(r) for r in H))
items = collections.Counter(x.split(":", 1)[1] for r in H for x in r["dq"] if x.startswith("dcf_hold:"))
print("보류 항목", dict(items.most_common()))
print("종목별", dict(collections.Counter(r["t"] for r in H).most_common()))
print("## 2. 새 표식 (새 필터 통과 행 기준)")
c = collections.Counter()
for r in ev(N):
    if not bad_new(r):
        for p in {str(x).split(":")[0] for x in r["dq"]}: c[p] += 1
print(dict(c.most_common()))
print("## 3. 연 단위 dcf_ok%·옛 필터 제외%·새 필터 제외%·판정% (옛 -> 새)")
for y in sorted({r["m"][:4] for r in N}):
    a = [r for r in O if r["m"].startswith(y)]; b = [r for r in N if r["m"].startswith(y)]
    f = lambda rs, bad: (round(100*sum(r["dcf_ok"] for r in rs)/len(rs), 1), round(100*sum(bad(r) for r in rs)/len(rs), 1), round(100*sum(1 for r in rs if r["g_V0"])/len(rs), 1))
    print(y, len(b), f(a, bad_old), "->", f(b, bad_old), "| 새 필터 제외%", round(100*sum(bad_new(r) for r in b)/len(b), 1))
print("## 4. 월별 새 필터 제외% (옛 필터 -> 새 필터)")
for m in sorted({r["m"] for r in N}):
    g = [r for r in N if r["m"] == m]
    print(m, len(g), round(100*sum(bad_old(r) for r in g)/len(g), 1), "->", round(100*sum(bad_new(r) for r in g)/len(g), 1))
print("## 5. 칸별 표 분포 (옛 -> 새)")
for f in ("self_vote", "peer_vote", "lv_V0", "g_V0"):
    print(f, dict(sorted(collections.Counter(str(r.get(f)) for r in O).items())), "->", dict(sorted(collections.Counter(str(r.get(f)) for r in N).items())))
print("## 6. 바뀐 행 수 (옛 -> 새)")
for f in ("base", "dcf_ok", "self_vote", "peer_vote", "lv_V0", "g_V0"):
    ch = [(r["t"], r["m"]) for r in N if ko[(r["t"], r["m"])].get(f) != r.get(f)]
    print(f, len(ch), "종목", len({t for t, _ in ch}))
print("## 7. 배수 이상값 (자기 이력 원값이 아니라 동종업 배수 > 1,000)")
big = lambda rs: sum(1 for r in rs for v in (r.get("peer") or {}).values() if isinstance(v, (int, float)) and abs(v) > 1000)
print("옛", big(O), "-> 새", big(N))
print("## 8. 기본 내재가치 3배 넘게 바뀐 행 (둘 다 양수)")
x3 = [(r["t"], r["m"], round(ko[(r["t"], r["m"])]["base"], 1), round(r["base"], 1)) for r in N
      if r.get("base") and ko[(r["t"], r["m"])].get("base") and r["base"] > 0 and ko[(r["t"], r["m"])]["base"] > 0
      and max(r["base"] / ko[(r["t"], r["m"])]["base"], ko[(r["t"], r["m"])]["base"] / r["base"]) > 3]
print(len(x3), "종목", sorted({t for t, *_ in x3}))
for row in x3[:40]: print("  ", row)
print("## 9. 부호가 바뀐 기본 내재가치")
sg = [(r["t"], r["m"]) for r in N if r.get("base") is not None and ko[(r["t"], r["m"])].get("base") is not None and (r["base"] > 0) != (ko[(r["t"], r["m"])]["base"] > 0)]
print(len(sg), dict(collections.Counter(t for t, _ in sg).most_common()))
