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
print("# 표본 기준: 1·2절은 구성 불명 종목(WBD) 제외 평가 행, 3~11절은 패널 전체 행. '옛' 판정은 봉인 패널 입력에 지금 판정 코드(peer_scores·assign)를 다시 돌린 값 — 패널에 판정이 저장돼 있지 않다")
print("## 1. dq 필터 통과 행 (구성 불명 제외)")
print("옛 패널·옛 필터", sum(not bad_old(r) for r in ev(O)), "/", len(ev(O)))
print("새 패널·옛 필터", sum(not bad_old(r) for r in ev(N)), "/", len(ev(N)))
print("새 패널·새 필터", sum(not bad_new(r) for r in ev(N)), "/", len(ev(N)))
H = [r for r in ev(N) if has(r, "dcf_hold")]
print("dcf_hold 행", len(H), "종목", len({r["t"] for r in H}), "| 다른 필터 표식 없이 새로 빠짐", sum(not bad_old(r) for r in H))
items = collections.Counter(x.split(":", 1)[1] for r in H for x in r["dq"] if x.startswith("dcf_hold:"))
print("보류 항목", dict(items.most_common()))
print("종목별", dict(collections.Counter(r["t"] for r in H).most_common()))
print("shares_missing 행(전체 패널)", sum(has(r, "shares_missing") for r in N))
print("## 2. 새 표식 (새 필터 통과 행 기준)")
c = collections.Counter()
for r in ev(N):
    if not bad_new(r):
        for p in {str(x).split(":")[0].split("@")[0] for x in r["dq"]}: c[p] += 1
print(dict(c.most_common()))
print("## 3. 연 단위 (dcf_ok%, 옛 필터 제외%, 판정%) 옛 -> 새 | 새 필터 제외%")
for y in sorted({r["m"][:4] for r in N}):
    a = [r for r in O if r["m"].startswith(y)]; b = [r for r in N if r["m"].startswith(y)]
    f = lambda rs, bad: (round(100*sum(r["dcf_ok"] for r in rs)/len(rs), 1), round(100*sum(bad(r) for r in rs)/len(rs), 1), round(100*sum(1 for r in rs if r["g_V0"])/len(rs), 1))
    print(y, len(b), f(a, bad_old), "->", f(b, bad_old), "| 새 필터 제외%", round(100*sum(bad_new(r) for r in b)/len(b), 1))
print("## 3b. 월별 dcf_ok%·판정% (옛 패널 -> 새 패널, 분모 = 그 달 행 수)")
for m in sorted({r["m"] for r in N}):
    a = [r for r in O if r["m"] == m]; b = [r for r in N if r["m"] == m]
    q = lambda rs: (round(100*sum(r["dcf_ok"] for r in rs)/len(rs), 1), round(100*sum(1 for r in rs if r["g_V0"])/len(rs), 1))
    print(m, len(b), q(a), "->", q(b))
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
print("## 7. 배수 이상값 — 동종업 비교용 배수 절댓값 > 1,000인 값 개수(행 수 아님), 새로 생긴 것·없어진 것")
big = lambda rs: {(r["t"], r["m"], k) for r in rs for k, v in (r.get("peer") or {}).items() if isinstance(v, (int, float)) and abs(v) > 1000}
bo, bn = big(O), big(N)
print("옛", len(bo), "-> 새", len(bn), "| 새로 생김", sorted(bn - bo), "| 없어짐", sorted(bo - bn))
print("## 8. 기본 내재가치 3배 넘게 바뀐 행 (둘 다 양수)")
x3 = [(r["t"], r["m"], round(ko[(r["t"], r["m"])]["base"], 2), round(r["base"], 2)) for r in N
      if r.get("base") and ko[(r["t"], r["m"])].get("base") and r["base"] > 0 and ko[(r["t"], r["m"])]["base"] > 0
      and max(r["base"] / ko[(r["t"], r["m"])]["base"], ko[(r["t"], r["m"])]["base"] / r["base"]) > 3]
print(len(x3), "종목", sorted({t for t, *_ in x3}))
for row in x3: print("  ", row)
print("## 9. 기본 내재가치 양수 <-> 0 이하 전환")
sg = [(r["t"], r["m"]) for r in N if r.get("base") is not None and ko[(r["t"], r["m"])].get("base") is not None and (r["base"] > 0) != (ko[(r["t"], r["m"])]["base"] > 0)]
print(len(sg), dict(collections.Counter(t for t, _ in sg).most_common()))
print("## 10. 보류 종목표 (새 패널 — 달 수, 기간, 낡은 항목=값@마지막 결산일)")
HT = collections.defaultdict(list)
for r in N:
    if has(r, "dcf_hold"):
        HT[r["t"]].append((r["m"], ";".join(sorted(str(x) for x in r["dq"] if str(x).startswith("bs_stale:")))))
for t, v in sorted(HT.items(), key=lambda x: -len(x[1])):
    print("  ", t, len(v), v[0][0], "~", v[-1][0], sorted({x for _, x in v}))
print("## 11. 보류로만 빠지는 행과 남는 행의 판정 분포 (새 패널 전체 행 — WBD 포함, %; 보류 행 판정은 낡은 항목을 0으로 넣고 계산한 값)")
A = [r for r in N if has(r, "dcf_hold") and not bad_old(r)]; B = [r for r in N if not bad_new(r)]
for f in ("lv_V0", "g_V0"):
    g = lambda rs: {k: round(100*v/len(rs), 1) for k, v in sorted(collections.Counter(str(r.get(f)) for r in rs).items())}
    print(f, "보류만", len(A), g(A)); print(f, "남는 행", len(B), g(B))
