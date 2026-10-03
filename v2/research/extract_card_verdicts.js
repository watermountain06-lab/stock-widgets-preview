// 카드 판정 추출 — 각 카드의 종합 판정 IIFE를 node에서 그대로 돌려 칸별 표·판정을 꺼낸다(verdict_replay 6번 보고용).
// 카드 파일은 읽기만 한다.   node v2/research/extract_card_verdicts.js > out.json
const fs = require('fs'), path = require('path'), vm = require('vm');
const V2 = path.join(__dirname, '..');
function block(src, start) {            // start = '{' 또는 '(' 위치부터 짝 맞추기(문자열·주석 무시 근사)
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
    for (const name of ['VALUATION', 'DCF', 'DAILY']) {
      const m = html.indexOf(`const ${T}_${name} =`);
      if (m < 0) continue;
      const s = html.indexOf('=', m) + 1;
      let k = s; while (/\s/.test(html[k])) k++;
      const e = block(html, k);
      code += `var ${T}_${name} = ${html.slice(k, e)};\n`;
    }
    // 판정 IIFE가 쓰는 최상위 함수(dcfLevel 등)
    for (const fn of ['dcfLevel', 'bankLevel', 'rimLevel']) {
      const m = html.indexOf(`function ${fn}(`);
      if (m >= 0) code += html.slice(m, block(html, html.indexOf('{', m))) + '\n';
    }
    const anchor = html.indexOf('종합 평가 자동 판정');
    const st = html.indexOf('(function(){', anchor);
    let iife = html.slice(st, block(html, st));
    iife = iife.replace('const seated = judges.filter', `globalThis.__J = judges; globalThis.__LV = (typeof lv !== 'undefined') ? lv : null; const seated = judges.filter`);
    code += `var ${T}_VERDICT;\n` + iife + '();\n' + `globalThis.__V = ${T}_VERDICT;`;
    const ctx = { document: { querySelectorAll: () => [], querySelector: () => null, getElementById: () => null }, console, Math, isFinite, Number };
    vm.createContext(ctx);
    vm.runInContext(code, ctx, { timeout: 2000 });
    const D = ctx[`${T}_DCF`] || null, daily = ctx[`${T}_DAILY`];
    const last = daily ? daily[daily.length - 1] : null;
    out[T] = { verdict: ctx.__V, judges: ctx.__J, dcfLabel: ctx.__LV && ctx.__LV.label, ratio: ctx.__LV && ctx.__LV.ratio,
               base: D && D.base, price: last && last[4], date: last && last[0] };
  } catch (e) { out[T] = { error: String(e).slice(0, 120) }; }
}
console.log(JSON.stringify(out, null, 1));
