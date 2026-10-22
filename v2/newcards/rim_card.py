"""보험 RIM 카드의 내재가치 칸 — fill.py 끝에서 부른다(DCF.model == "rim", research/insurer_rim_prereg.md §5, 2026-10-17).

카드는 매번 틀(NVDA)에서 복제되므로 현금흐름 칸의 라벨·탭·헤더 JS를 여기서 RIM으로 바꾼다. 숫자는 모두 DCF 블록
(adapters/insurer_rim.py → build.py)에서 읽고, 판정 문턱은 카드 JS(dcfLevel·DV)와 엔진(SCORE_TABLE)이 같은지 대조한다.
찾는 글이 없으면 멈춘다 — 틀이 바뀌었는데 현금흐름 문구가 조용히 남지 않게."""
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "adapters"))
import insurer_rim  # noqa: E402


def _one(h, o, n):
    c = h.count(o)
    assert c == 1, (c, o[:100])
    return h.replace(o, n)


def check_thresholds(h):
    """카드 JS의 5단계(dcfLevel)와 표(DV)를 읽어 엔진 표(insurer_rim.SCORE_TABLE)와 같은지 — 다르면 빌드를 멈춘다(§5)."""
    m = re.search(r"r <= ([\d.]+) \? \['', '매우 싸다'\] : r <= ([\d.]+) \? \['', '싸다'\] : r <= ([\d.]+) \? \['mid', '적정'\]\s*"
                  r": r <= ([\d.]+) \? \['high', '비싸다'\] : \['high', '매우 비싸다'\]", h)
    dv = re.search(r"const DV = \{'매우 싸다': (-?\d), '싸다': (-?\d), '적정': (-?\d), '비싸다': (-?\d), '매우 비싸다': (-?\d)\};", h)
    assert m and dv, "카드 JS에서 판정 문턱(dcfLevel·DV)을 못 찾음"
    js = tuple(zip((float(x) for x in m.groups()), (int(x) for x in dv.groups()[:4])))
    assert js == insurer_rim.SCORE_TABLE and int(dv.group(5)) == -2, ("판정 문턱이 엔진과 다르다", js, insurer_rim.SCORE_TABLE)


def apply(h, T, D, px):
    t = T.lower()
    check_thresholds(h)
    p1 = lambda v: f"{v * 100:.1f}%"
    # ── 라벨: 현금흐름 → 초과이익 ──
    h = _one(h, '<span class="logic-tag">내재가치 <span class="logic-denom">현금흐름</span></span>',
             '<span class="logic-tag">내재가치 <span class="logic-denom">초과이익</span></span>')
    h = _one(h, '<div class="vs-name" title="회사가 앞으로 벌어들일 현금만으로 계산한 주당 가치(기본 시나리오).">현금흐름 (내재가치)</div>',
             '<div class="vs-name" title="보통주 장부 자본에 앞으로의 초과이익(ROE가 할인율 10%를 넘는 몫)을 더한 주당 가치(기본 시나리오, RIM).">초과이익 (내재가치)</div>')
    h = _one(h, "    ['현금흐름', lv.label in DV ? DV[lv.label] : null, lv.label, 2],", "    ['초과이익', lv.label in DV ? DV[lv.label] : null, lv.label, 2],")
    h = _one(h, "'\\n⚠ 현금흐름이 \"매우 싸다\"여도 +1만 준다", "'\\n⚠ 초과이익이 \"매우 싸다\"여도 +1만 준다")
    h = _one(h, '<div class="section-title">내재가치 (DCF) — 현금흐름이 말하는 가격</div>',
             '<div class="section-title">내재가치 (RIM) — 장부 자본과 초과이익이 말하는 가격</div>')
    lede = ("보통주 장부 자본에 앞으로 5년의 초과이익(ROE − 할인율 10%)과 그 뒤 잔존가치를 더한 주당 가치다. 보험사는 투자수익이 영업과 섞여 현금흐름 모델 대신 이 모델을 쓴다."
            if D.get("base") is not None else f"이번에는 초과이익 내재가치를 계산하지 않았다 — {D.get('unavailable')}.")
    # 기권이면 fill.py가 이미 CB 문구('현금흐름 내재가치를 계산하지 않는다')로 바꿔 둔다 — 둘 중 하나(변이 시험 2026-10-17)
    _l0 = [x for x in ('<div class="lede">회사가 앞으로 벌어들일 현금만으로 계산한 주당 가치다.</div>',
                       '<div class="lede">이 종목은 현금흐름 내재가치를 계산하지 않는다.</div>') if h.count(x) == 1]
    assert len(_l0) == 1, "내재가치 탭 첫 문장 자리를 못 찾음"
    h = h.replace(_l0[0], f'<div class="lede">{lede}</div>')
    # ── 헤더 요구 칸: 요구 성장 → 요구 ROE ──
    anchor = "  if (box)  box.innerHTML = "
    assert h.count(anchor) == 1, "헤더 내재가치 칸 자리를 못 찾음"
    h = h.replace(anchor, "  if (req && d.model === 'rim') {   // 보험 RIM — 5년 일정 ROE(insurer_rim_prereg §3)\n"
                  "    req.textContent = d.requiredRoe != null ? f1(d.requiredRoe) : '해 없음';\n"
                  "    const c_ = req.closest('.meta-item');\n"
                  "    if (c_ && price != null) { const lv = dcfLevel(price, d); req.style.color = lv.color;\n"
                  "      c_.title = (d.requiredRoe != null ? `현재가 $${price.toFixed(2)} 가 정당화되려면 5년 내내 ROE가 ${f1(d.requiredRoe)}여야 한다` : `현재가 $${price.toFixed(2)}에는 0~80% 안의 어떤 일정 ROE로도 닿지 않는다`)\n"
                  "        + `(최근 4분기 ${f1(d.roe0)}, 2년 중앙값 ${f1(d.roe2y)}, 유보율 ${f1(d.b)}).`\n"
                  "        + `\\n현재가 ÷ 초과이익 내재가치 $${Math.round(d.base)} = ${lv.ratio != null ? lv.ratio.toFixed(2) : '—'} → ${lv.label} (${DCF_RULE_TEXT})`; }\n"
                  "  }\n" + anchor, 1)
    # ── 계산 어려움 신호(RIM ①~④) ──
    h = _one(h, "        nosol: () => '어떤 일정 성장률로도 현재가에 닿지 않는다',",
             "        nosol: () => '어떤 일정 성장률로도 현재가에 닿지 않는다',\n"
             "        roe_below_r: () => `기본 ROE(2년 중앙값 ${pct(D.roe2y)}) < 할인율 10% — 초과이익이 음수라 장부보다 낮게 나온다`,\n"
             "        b_zero: () => '유보율 0 — 이익을 모두 돌려줘 장부가 자라지 않는다',\n"
             "        no_required_roe: () => '요구 ROE 해 없음 — 0~80% 안의 어떤 일정 ROE로도 현재가에 닿지 않는다',\n"
             "        signal4: () => `출발 4분기에 최근 8분기 중앙값에서 40% 넘게 벗어난 분기(${(H.signal4 || []).join('·')}) — 그 분기를 중앙값으로 바꾸면 ROE ${pct(H.signal4Roe)}`,")
    assert h.count("${D.hard.length}/5") == 2, "계산 어려움 개수 표기 자리"
    h = h.replace("${D.hard.length}/5", "${D.hard.length}/${D.model === 'rim' ? 4 : 5}")
    # 5년 중앙값이 없으면 보수 칸은 "없음"(부분 표시, §4) — 음수와 구분
    h = _one(h, "el.textContent = v0 > 0 ? '$' + v0.toFixed(2) : '0 이하';", "el.textContent = v0 == null ? '없음' : v0 > 0 ? '$' + v0.toFixed(2) : '0 이하';")
    # ── 역산 문장 ──
    rq = D.get("requiredRoe")
    rev = ("—" if D.get("base") is None else
           f"지금 가격(<span data-dcf-price>${px:.2f}</span>)이 정당하려면 5년 내내 ROE가 <b>{p1(rq)}</b>여야 한다"
           f"(유보율 {p1(D['b'])}·잔존 절반 수렴은 그대로). 최근 4분기 ROE는 {p1(D['roe0'])}, 최근 2년 중앙값 {p1(D['roe2y'])}"
           + (f", 5년 중앙값 {p1(D['roe5y'])}" if D.get("roe5y") is not None else "") + "다."
           if rq is not None else
           f"지금 가격(<span data-dcf-price>${px:.2f}</span>)에는 0~80% 안의 어떤 일정 ROE로도 닿지 않는다.")
    h = _one(h, '<div class="reverse">—</div>', f'<div class="reverse">{rev}</div>')
    # ── 직접 바꿔보기 → 민감도 표(할인율 × 잔존 수렴, 7-10) ──
    m = re.search(r'  <!-- ── 2\. 직접 바꿔보기 ── -->\n  <div class="card">.*?<div class="ruler" id="dcfRuler"></div>\n  </div>\n', h, re.S)
    assert m, "직접 바꿔보기 칸을 못 찾음"
    G = (D.get("rimDetail") or {}).get("grid") or {}
    cell = lambda v: f"${v:.0f}" if v is not None else "—"
    rows = "".join(f'<tr><td>{int(r * 100)}%{" (기본)" if r == 0.10 else ""}</td>' + "".join(
        f'<td{" style=\"font-weight:700\"" if (r, lam) == (0.10, 0.5) else ""}>{cell(G.get(f"{r:.2f}|{lam}"))}</td>' for lam in (0.0, 0.5, 1.0)) + "</tr>"
        for r in (0.08, 0.09, 0.10, 0.11, 0.12))
    card = ('  <!-- ── 2. 민감도 (RIM, 7-10) ── -->\n  <div class="card">\n'
            '    <div class="card-title">민감도 — 할인율 × 잔존 수렴 (기본 시나리오, 주당)</div>\n'
            '    <div class="wrap"><table>\n      <thead><tr><th>할인율</th><th>수렴 없음</th><th>절반 수렴(기본)</th><th>완전 수렴</th></tr></thead>\n'
            f'      <tbody>{rows}</tbody>\n    </table></div>\n'
            '    <div class="note">수렴은 5년 뒤 ROE가 할인율 쪽으로 얼마나 다가가는가다. 수렴 없음은 5년째 ROE가 영원히 이어진다는 뜻이고, 완전 수렴은 그 뒤 초과이익이 없다는 뜻이다. '
            '잔존 성장은 연 2.5%를 넘지 않게 유보율을 낮춘다.</div>\n  </div>\n'
            if D.get("base") is not None else "")
    h = h[:m.start()] + card + h[m.end():]
    # 시나리오 범위: 보수만 없을 때(null) Math.min이 0으로 읽어 범위 표시가 사라지지 않게(dr 구현 r1 Codex 사소)
    h = _one(h, "const _mn = Math.min(D.low, D.base, D.high), _mx = Math.max(D.low, D.base, D.high);",
             "const _sv = [D.low, D.base, D.high].filter(v => typeof v === 'number'), _mn = Math.min(..._sv), _mx = Math.max(..._sv);   // RIM: 보수 없음 제외")
    # 기본적 분석 칸: BVPS·ROE_TTM(§1·§5 — 정의는 회사 발표 ROE와 다를 수 있음)
    if D.get("base") is not None:
        R = D.get("rimDetail") or {}
        q = f"Q{int(R['L'][5:7]) // 3} {R['L'][:4]}"
        h = _one(h, "  <!-- ══════════ 3. 재무 건전성 (구조 유지) ══════════ -->",
                 f'  <div class="note" style="margin-top:10px;">주당 장부가치(BVPS) ${D["bvps"]:.2f}({q} 말 보통주 자본 ÷ 주식 수) · '
                 f'ROE(최근 4분기) {p1(D["roe0"])} — 최근 4분기 순이익 ÷ 1년 전 보통주 자본이라 회사가 발표하는 ROE(평균 자본 기준 등)와 다를 수 있다.</div>\n\n'
                 "  <!-- ══════════ 3. 재무 건전성 (구조 유지) ══════════ -->")
    assert "현금흐름 (내재가치)" not in h and "내재가치 (DCF)" not in h, "현금흐름 라벨이 남았다"
    return h
