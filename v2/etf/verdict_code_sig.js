// 카드 판정 코드 서명 — ETF 판정(etf-v1)이 받는 카드 판정 코드인지 확인하는 해시(v2/research/etf_verdict_prereg.md 5번).
// extract_card_verdicts.js가 실행하는 것과 같은 범위(dcfLevel·bankLevel·rimLevel 함수 + "종합 평가 자동 판정" IIFE)를
// 잘라, 티커 접두어(NVDA_ 등)를 T_로 바꾼 텍스트의 sha256 앞 12자. 문턱(30·70)·표 사전(DV)·합산식이 모두 IIFE 안에 있어,
// 오늘 어느 카드도 새 분기를 타지 않아도 코드가 바뀌면 해시가 바뀐다. 카드 파일은 읽기만 한다.
//   node v2/etf/verdict_code_sig.js > out.json
const fs = require('fs'), path = require('path'), crypto = require('crypto');
const V2 = path.join(__dirname, '..');
function block(src, start) {            // extract_card_verdicts.js의 block()과 같은 짝 맞추기
  let depth = 0, i = start, q = null;
  for (; i < src.length; i++) {
    const c = src[i];
    if (q) { if (c === '\\') { i++; continue; } if (c === q) q = null; continue; }
    if (c === '"' || c === "'" || c === '`') { q = c; continue; }
    if (c === '/' && src[i + 1] === '/') { i = src.indexOf('\n', i); continue; }
    if (c === '/' && src[i + 1] === '*') { i = src.indexOf('*/', i) + 1; continue; }
    if (c === '{' || c === '(' || c === '[') depth++;
    if (c === '}' || c === ')' || c === ']') { depth--; if (depth === 0) return i + 1; }
  }
  return -1;
}
const out = {};
for (const f of fs.readdirSync(V2).filter(f => f.endsWith('_full_widget.html')).sort()) {
  const T = f.replace('_full_widget.html', '');
  const html = fs.readFileSync(path.join(V2, f), 'utf8');
  try {
    let code = '';
    for (const fn of ['dcfLevel', 'bankLevel', 'rimLevel']) {
      const m = html.indexOf(`function ${fn}(`);
      if (m >= 0) code += html.slice(m, block(html, html.indexOf('{', m)));
    }
    const anchor = html.indexOf('종합 평가 자동 판정');
    if (anchor < 0) throw new Error('판정 IIFE 없음');
    const st = html.indexOf('(function(){', anchor);
    code += html.slice(st, block(html, st));
    code = code.split(T + '_').join('T_');
    out[T] = crypto.createHash('sha256').update(code).digest('hex').slice(0, 12);
  } catch (e) { out[T] = { error: String(e).slice(0, 120) }; }
}
console.log(JSON.stringify(out));
