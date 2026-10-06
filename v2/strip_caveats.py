#!/usr/bin/env python3
"""값 옆·밑에 작은 글씨로 붙은 "왜 그런지" 설명을 화면에서 빼고 툴팁으로 옮긴다(2026-10-06 사용자 결정, 103장 전체).

카드를 다 만든 뒤 마지막에 돈다(build.py·은행 rebuild 스크립트가 부른다) — 같은 카드에 여러 번 돌려도 결과가 같다.
  1. 헤더 "밴드 적중률 (PER 해당 없음 — …)"처럼 해당 없음 사유가 붙은 칸 이름 → "밴드 적중률", 사유는 칸 이름 툴팁.
     적중률 숫자가 있을 때의 "(407/680일, …)"은 사유가 아니라 값의 근거라 그대로 둔다.
  2. 내재가치 칸 "계산 불가 · 사유" → "계산 불가", 사유는 칸 툴팁.
  3. 헤더 판정 밑 "경계 — …" 글 → 없앤다. 같은 내용은 판정 툴팁의 "경계:" 줄에 이미 있다.
  4. BRKB "(판정 미반영)" 표기 → 없앤다("참고값"이라는 말이 판정과 무관하다는 뜻을 담는다).

    python3 v2/strip_caveats.py NVDA BRKB SPCX      # 또는 --all
"""
import glob
import os
import re
import sys

V2 = os.path.dirname(os.path.abspath(__file__))
WHY = r"(?:PER 해당 없음|백테스트 없음|해당 없음|끝난 체크포인트)"


def strip(h):
    # 1. 칸 이름의 해당 없음 사유(JS) — 작은따옴표 꼴과 템플릿 꼴
    #    "if (label) …" 한 문장이 두 문장이 되므로 중괄호로 묶는다(label이 없으면 title도 건너뛴다)
    h = re.sub(r"(if \(label\) )?label\.textContent = '밴드 적중률 \((" + WHY + r"[^']*)\)';",
               lambda m: (m.group(1) or "") + "{ label.textContent = '밴드 적중률'; label.title = '" + m.group(2) + "'; }", h)
    h = re.sub(r"(if \(label\) )?label\.textContent = `밴드 적중률 \((" + WHY + r".*)\)`;$",
               lambda m: (m.group(1) or "") + "{ label.textContent = '밴드 적중률'; label.title = `" + m.group(2) + "`; }", h, flags=re.M)
    #    앞판(2026-10-06 첫 실행)에서 중괄호 없이 바꾼 것
    h = re.sub(r"if \(label\) label\.textContent = '밴드 적중률'; label\.title = (.*?);$",
               r"if (label) { label.textContent = '밴드 적중률'; label.title = \1; }", h, flags=re.M)
    #    정적 대체값
    h = re.sub(r'(id="\w+ConfidenceLabel")( title="[^"]*")?>밴드 적중률 \((' + WHY + r'[^)<]*)\)',
               lambda m: f'{m.group(1)}{m.group(2) or " title=" + chr(34) + m.group(3) + chr(34)}>밴드 적중률', h)
    # 2. 내재가치 칸 사유(JS·정적)
    h = h.replace("if (box) box.innerHTML = '계산 불가<span class=\"logic-denom\"> · ' + why + '</span>';",
                  "if (box) { box.textContent = '계산 불가'; box.title = why; }")
    h = re.sub(r'(id="\w+DcfBox")>계산 불가<span class="logic-denom"> · ([^<]*)</span>',
               lambda m: f'{m.group(1)} title="{m.group(2)}">계산 불가', h)
    # 3. 판정 밑 "경계 —" 글(툴팁 줄은 남긴다)
    h = re.sub(r"\n    if \(!el\.classList\.contains\('meta-value'\)\) return;   // 헤더 판정 밑에만 글을 단다\n.*?e\.textContent = '경계 — ' \+ edges\[0\]; el\.after\(e\);",
               "", h, flags=re.S)
    h = re.sub(r'<span class="verdict-edge"[^>]*>.*?</span>', "", h)
    # 4. BRKB "(판정 미반영)"
    h = h.replace("두 기둥 참고값 (판정 미반영)", "두 기둥 참고값").replace("<strong>$408</strong>(판정 미반영)", "<strong>$408</strong>")
    h = re.sub(r"(두 기둥 참고값 <strong>\$[\d,.]+</strong>)\(판정 미반영\)", r"\1", h)
    return h


def main():
    args = sys.argv[1:]
    paths = sorted(glob.glob(os.path.join(V2, "*_full_widget.html"))) if args == ["--all"] else \
        [a if a.endswith(".html") else os.path.join(V2, f"{a.upper()}_full_widget.html") for a in args]
    for p in paths:
        h = open(p, encoding="utf-8").read()
        n = strip(h)
        if n != h:
            open(p, "w", encoding="utf-8").write(n)
            print("고침", os.path.relpath(p, V2))


if __name__ == "__main__":
    main()
