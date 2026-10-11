#!/usr/bin/env python3
"""손 카드(BRKB·SPCX)의 숫자 칸을 매일 다시 계산해 카드에 넣는다(2026-10-11, 15장 자동화 — 사용자 결정).

두 카드는 구조가 특수해(BRKB 두 기둥 내재가치·보험지주, SPCX 상장 첫 분기) 생성기 카드가 아니고 문장은 손으로 쓴다.
그동안 매일 실행은 가격 배열만 붙여 자기 이력·동종업 점수와 적정주가 밴드가 만든 날에 멈춰 있었다(BRKB 10/5 PER 22.6배 — 10/9 23.11배).
여기서는 어댑터로 숫자만 새로 만들고, 분기 문장은 건드리지 않는다. 새 10-Q가 나오면 토요일 새 공시 점검(new_filings)이 알린다.

    python3 v2/newcards/hand_refresh.py BRKB
    python3 v2/newcards/hand_refresh.py SPCX

- BRKB: adapters/brkb_multiples.py(정상화 PER·PBR, 금융 카드 규칙) → VALUATION.self·SCORES.selfHistory·적정주가 밴드(헤더)
- SPCX: adapters/spcx_ttm.py(TTM 배수) → build_peer_score.py(산업재 + IT) → VALUATION.peer·SCORES.peer. 적자라 PER은 평균에서 뺀다(A3)
판정 칸은 바꾸지 않는다 — 두 카드 모두 현금흐름 칸이 설계상 기권이라 판정은 '판정 보류'다.
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
PY = sys.executable


def _run(args):
    r = subprocess.run([PY] + args, cwd=os.path.dirname(V2), capture_output=True, text=True, timeout=1800)
    if r.returncode:
        raise SystemExit(f"{' '.join(args)} 실패: {r.stderr[-400:]}")
    return r.stdout


def _swap(h, name, obj):
    pat = re.compile(rf"const {name} = \{{.*?\}};\n", re.S)
    assert len(pat.findall(h)) == 1, name
    return pat.sub(lambda _: f"const {name} = " + json.dumps(obj, ensure_ascii=False) + ";\n", h)


def _scores(h, T, **kv):
    m = re.search(rf"const {T}_SCORES = \{{.*?\n\}};", h, re.S)
    s = m.group(0)
    for k, v in kv.items():
        s, n = re.subn(rf"(\n  {k}: )[^,]*,", lambda m_: m_.group(1) + json.dumps(v) + ",", s, count=1)
        assert n == 1, k
    return h[:m.start()] + s + h[m.end():]


def brkb():
    out = os.path.join(V2, "BRKB_multiples.json")
    _run(["v2/adapters/brkb_multiples.py", "--json", out])
    M = json.load(open(out))
    p = os.path.join(V2, "BRKB_full_widget.html")
    h = open(p, encoding="utf-8").read()
    V = json.loads(re.search(r"const BRKB_VALUATION = (\{.*?\});\n", h, re.S).group(1))
    key = {"per": "PER", "pbr": "PBR"}
    mets = []
    for m in V["self"]["metrics"]:
        x = M["multiples"][key[m["metric"]]]
        mets.append({**m, **{k: (round(x[k], 2) if isinstance(x.get(k), float) else x.get(k)) for k in ("score", "percentile", "current", "min", "median", "max", "days", "gapDays")}})
    sc = [m["score"] for m in mets if m.get("score") is not None]
    V["self"].update({"metrics": mets, "window": M["window"], "score": round(sum(sc) / len(sc), 1) if len(sc) == len(mets) else None})
    h = _swap(h, "BRKB_VALUATION", V)
    h = _scores(h, "BRKB", selfHistory=V["self"]["score"], asOf=M["window"][1])
    fb = M.get("fairBand")
    if fb:
        h, n = re.subn(r'(id="brkbFairBand"[^>]*title=")[^"]*(">)[^<]*',
                       lambda m_: m_.group(1) + f'최근 252거래일 정상화 PER의 25~75% 구간({fb["per_p25"]:.1f}~{fb["per_p75"]:.1f}배) × 현재 정상화 이익. 분기 주식 수 태그가 없는 구간을 뺀 {fb["days"]}일로 계산했다($10 단위).' + m_.group(2) + f'${fb["low"]} ~ ${fb["high"]}', h, count=1)
        assert n == 1, "BRKB 밴드"
    # 손 문장 속 숫자(두 배수가 5년 가운데쯤 → 0표). 표 방향이 바뀌면 문장이 틀린다 — 멈추고 문제로 알린다(분기 반영 때 손으로)
    _sc = [m.get("score") for m in mets]
    if any(x is None for x in _sc) or all(x >= 70 for x in _sc) or all(x < 30 for x in _sc):
        raise SystemExit(f"BRKB: 자기 이력 표가 0이 아니다({_sc}) — '가운데쯤이라 0표' 문장을 손으로 고칠 것")
    h, n = re.subn(r"정상화 PER\([\d.]+배\)과 PBR\([\d.]+배\)", f"정상화 PER({mets[0]['current']:.1f}배)과 PBR({mets[1]['current']:.2f}배)", h)
    assert n >= 1, "BRKB 문장"
    open(p, "w", encoding="utf-8").write(h)
    print(f"BRKB: 자기 이력 {V['self']['score']} (PER {mets[0].get('current')}·PBR {mets[1].get('current')}), 밴드 {fb and (fb['low'], fb['high'])}, 창 {M['window']}")


def spcx():
    _run(["v2/adapters/spcx_ttm.py"])
    tmp = os.path.join(V2, ".sec_cache", "_work", "SPCX_peer.json")
    os.makedirs(os.path.dirname(tmp), exist_ok=True)
    _run(["v2/build_peer_score.py", "SPCX", "--self", "v2/SPCX_multiples.json", "--json", tmp])
    r = json.load(open(tmp))
    p = os.path.join(V2, "SPCX_full_widget.html")
    h = open(p, encoding="utf-8").read()
    V = json.loads(re.search(r"const SPCX_VALUATION = (\{.*?\});\n", h, re.S).group(1))
    mets = [{"metric": m["metric"], "score": m["score"], "rank": m["rank"], "peers": m["peers"]} for m in r["metrics"]
            if not (V.get("perNA") and m["metric"] == "per")]   # A3: 적자(순이익률 2% 미만)면 PER은 평균에서 뺀다
    sc = [m["score"] for m in mets if m["score"] is not None]
    score = round(sum(sc) / len(sc), 1) if sc else None
    V["peer"].update({"score": score, "asOf": r["peerAsOf"], "priceSession": r.get("priceSession"), "metrics": mets})
    h = _swap(h, "SPCX_VALUATION", V)
    h = _scores(h, "SPCX", peer=score, asOf=r.get("priceSession") or V["peer"]["priceSession"])
    # 손 문장 속 매출 배수("동종업 중 가장 비싼 쪽이다(매출의 101배, 순손실)") — PSR 순위가 꼴찌가 아니면 문장이 틀린다
    _ps = next((m for m in r["metrics"] if m["metric"] == "psr"), None)
    _own = json.load(open(os.path.join(V2, "SPCX_multiples.json")))["multiples"]["PSR"]["current"]
    if not _ps or _ps["rank"] < _ps["peers"]:
        raise SystemExit(f"SPCX: PSR 순위 {_ps and (_ps['rank'], _ps['peers'])} — '가장 비싼 쪽' 문장을 손으로 고칠 것")
    h, n = re.subn(r"매출의 \d+배", f"매출의 {_own:.0f}배", h)
    assert n >= 1, "SPCX 문장"
    open(p, "w", encoding="utf-8").write(h)
    print(f"SPCX: 동종업 {score} ({', '.join(f'{m['metric']} {m['score']}' for m in mets)})")


NEED = {"BRKB": os.path.join(V2, ".sec_cache", "brk_facts.json"), "SPCX": os.path.join(V2, ".sec_cache", "0001181412_facts.json")}

if __name__ == "__main__":
    for T in sys.argv[1:]:
        if not os.path.exists(NEED[T.upper()]):   # Actions 캐시에 원문 저장본이 없으면 숫자 갱신만 건너뛴다(가격은 그대로 간다)
            print(f"{T}: 경고 — {os.path.basename(NEED[T.upper()])} 캐시 없음, 숫자 칸 갱신 건너뜀")
            continue
        {"BRKB": brkb, "SPCX": spcx}[T.upper()]()
