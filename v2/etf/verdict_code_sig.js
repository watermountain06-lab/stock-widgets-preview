// 카드 판정 코드 서명 — ETF 판정(etf-v1)이 받는 카드 판정 코드인지 확인하는 해시(v2/research/etf_verdict_prereg.md 5번).
// extract_card_verdicts.js가 실행하는 것과 같은 범위(dcfLevel·bankLevel·rimLevel 함수 + "종합 평가 자동 판정" IIFE)를
// 잘라, 티커 접두어(NVDA_ 등)를 T_로 바꾼 텍스트의 sha256 앞 12자. 문턱(30·70)·표 사전(DV)·합산식이 모두 IIFE 안에 있어,
// 오늘 어느 카드도 새 분기를 타지 않아도 코드가 바뀌면 해시가 바뀐다. 카드 파일은 읽기만 한다.
//   node v2/etf/verdict_code_sig.js            → {티커: 해시 | {error}}
//   node v2/etf/verdict_code_sig.js --text     → {티커: {hash, text} | {error}}   (승인 원문 저장·diff용, 2026-10-20)
// 잘라낸 조각(함수 선언 각각, IIFE)은 하나씩 vm.Script로 컴파일해 본다 — 정규식·템플릿 리터럴 속 괄호 때문에 범위가 일찍
// 잘리면 괄호가 안 맞아 컴파일이 실패하고 그 카드는 오류(잘린 범위로 해시해 변경을 놓치지 않게). 범위가 넘쳐 잡히는 쪽은
// 컴파일될 수 있으나 해시에 코드가 더 들어가 거짓 보류가 될 뿐이다(사람이 diff에서 본다).
const fs = require('fs'), path = require('path'), crypto = require('crypto'), vm = require('vm');
const V2 = path.join(__dirname, '..');
const WITH_TEXT = process.argv.includes('--text');
function block(src, start) {            // extract_card_verdicts.js의 block()과 같은 짝 맞추기
  let depth = 0, i = start, q = null;
  for (; i < src.length; i++) {
    const c = src[i];
    if (q) { if (c === '\\') { i++; continue; } if (c === q) q = null; continue; }
    if (c === '"' || c === "'" || c === '`') { q = c; continue; }
    // 주석 끝을 못 찾으면 -1 — 예전엔 indexOf의 -1로 처음부터 다시 훑어 끝나지 않았다(2026-10-20 dr)
    if (c === '/' && src[i + 1] === '/') { const e = src.indexOf('\n', i); if (e < 0) return -1; i = e; continue; }
    if (c === '/' && src[i + 1] === '*') { const e = src.indexOf('*/', i); if (e < 0) return -1; i = e + 1; continue; }
    if (c === '{' || c === '(' || c === '[') depth++;
    if (c === '}' || c === ')' || c === ']') { depth--; if (depth === 0) return i + 1; }
  }
  return -1;
}
function piece(html, from, open, what) {   // from부터 open 위치의 괄호 짝까지 잘라 혼자 컴파일되는지 본다. 못 하면 오류.
  if (from < 0 || open < 0) throw new Error(`${what} 시작 없음`);
  const end = block(html, open);
  if (end < 0) throw new Error(`${what} 끝 없음`);
  const text = html.slice(from, end);
  try { new vm.Script('(' + text + ')'); } catch (e) { throw new Error(`${what} 조각이 컴파일되지 않음`); }
  return text;
}
const out = {};
for (const f of fs.readdirSync(V2).filter(f => f.endsWith('_full_widget.html')).sort()) {
  const T = f.replace('_full_widget.html', '');
  const html = fs.readFileSync(path.join(V2, f), 'utf8');
  try {
    let code = '';
    for (const fn of ['dcfLevel', 'bankLevel', 'rimLevel']) {
      const m = html.indexOf(`function ${fn}(`);
      if (m >= 0) code += piece(html, m, html.indexOf('{', m), fn);
    }
    const anchor = html.indexOf('종합 평가 자동 판정');
    if (anchor < 0) throw new Error('판정 IIFE 없음');
    const st = html.indexOf('(function(){', anchor);
    code += piece(html, st, st, '판정 IIFE');
    code = code.split(T + '_').join('T_');
    const hash = crypto.createHash('sha256').update(code).digest('hex').slice(0, 12);
    out[T] = WITH_TEXT ? { hash, text: code } : hash;
  } catch (e) { out[T] = { error: String(e).slice(0, 120) }; }
}
console.log(JSON.stringify(out));
