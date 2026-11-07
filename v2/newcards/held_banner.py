"""카드 갱신 보류 띠(안건 E71, 2026-11-07 사용자 결정 B).

카드별 증권 표(v2/share_claims.json)에 새 결산일 짝 금액 행이 없으면 배수 엔진이 ClaimHold로 멈춰 그 카드 빌드가 실패한다.
일일 파이프라인(daily_price.attempt)은 카드를 전날 상태로 되돌리는데, 화면에는 낡았다는 표시가 없었다(BLK 2026-11-03~06).
이 모듈은 되돌린 카드 맨 위에 '새 분기 자료 확인 대기 — 숫자는 이전 빌드 기준' 띠를 붙인다. 다음에 빌드가 성공하면
카드를 틀에서 다시 만들므로 띠는 저절로 사라진다. 띠가 이미 있으면 문구만 바꾼다(첫 보류일은 유지).

    python3 v2/newcards/held_banner.py BLK "BLK BLK-hps-subco-units: equity 관측 결산일 2026-09-30에 짝 금액 ce_add 행 없음"
"""
import html
import os
import re
import sys
from datetime import date

V2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
START, END = "<!-- held-banner:start -->", "<!-- held-banner:end -->"


def reason_text(why):
    """ClaimHold 메시지에서 결산일을 뽑아 사람이 읽을 문장으로."""
    m = re.search(r"(\d{4}-\d{2}-\d{2})", why or "")
    q = f"{m.group(1)} 분기" if m else "새 분기"
    return f"{q} 보고서의 전환·교환 증권 금액을 카드별 표에 아직 넣지 않아 이 카드 갱신을 멈췄다"


def mark(ticker, why, today=None, path=None):
    """카드 HTML에 보류 띠를 넣는다(있으면 문구만 갱신). 바꿨으면 True."""
    path = path or os.path.join(V2, f"{ticker}_full_widget.html")
    if not os.path.exists(path):
        return False
    h = open(path, encoding="utf-8").read()
    today = today or date.today().isoformat()
    since = today
    old = re.search(re.escape(START) + r".*?" + re.escape(END), h, re.S)
    if old:
        m = re.search(r'data-held-since="(\d{4}-\d{2}-\d{2})"', old.group(0))
        since = m.group(1) if m else today
    text = (f"새 분기 자료 확인 대기 — {reason_text(why)}. 아래 숫자·판정은 {since} 전 마지막 빌드 기준이다"
            f" (보류 {since}부터, 확인 {today}).")
    div = (f'{START}<div id="heldBanner" data-held-since="{since}" role="status" '
           f'style="margin:0 0 12px;padding:10px 14px;border:1px solid var(--red);border-radius:var(--radius, 8px);'
           f'background:var(--bg2);color:var(--text);font-size:13px;line-height:1.5;" '
           f'title="{html.escape(why or "", quote=True)}">⚠ {html.escape(text)}</div>{END}')
    if old:
        h2 = h[:old.start()] + div + h[old.end():]
    else:
        m = re.search(r"<body[^>]*>", h)
        if not m:
            return False
        h2 = h[:m.end()] + "\n" + div + h[m.end():]
    if h2 == h:
        return False
    open(path, "w", encoding="utf-8").write(h2)
    return True


if __name__ == "__main__":
    print(mark(sys.argv[1].upper(), sys.argv[2] if len(sys.argv) > 2 else ""))
