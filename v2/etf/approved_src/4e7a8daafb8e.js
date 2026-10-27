function dcfLevel(price, D) {
  if (!D || price == null || typeof D.base !== 'number' || !isFinite(D.base))
    return { label: '계산 불가', cls: 'mid', color: 'var(--gold)', split: false, ratio: null, range: '' };
  if (D.base <= 0)
    return { label: '매우 비싸다', cls: 'high', color: 'var(--red)', split: false, ratio: null, range: '기본 내재가치가 0 이하다' };
  const r = price / D.base;
  const [cls, label] = r <= 0.7 ? ['', '매우 싸다'] : r <= 0.9 ? ['', '싸다'] : r <= 1.1 ? ['mid', '적정']
                     : r <= 1.5 ? ['high', '비싸다'] : ['high', '매우 비싸다'];
  const color = cls === '' ? '#0ea5e9' : cls === 'mid' ? 'var(--gold)' : 'var(--red)';
  const _sv = [D.low, D.base, D.high].filter(v => typeof v === 'number'), _mn = Math.min(..._sv), _mx = Math.max(..._sv);   // RIM: 보수 없음 제외   // 세 시나리오 최소·최대(카드 한정)
  const split = _mn > 0 && _mn < price && price < _mx;
  const range = _mn > 0
    ? `시나리오 범위: ${(price / _mx).toFixed(2)} ~ ${(price / _mn).toFixed(2)}(세 시나리오 최대·최소 기준)` : '';
  return { label, cls, color, split, ratio: r, range };
}(function(){
  const V = T_VALUATION, D = T_DCF;
  const last = T_DAILY[T_DAILY.length - 1];
  // 기권 규칙(2026-09-25, Fable 지적 · 사용자 결정): 표를 못 던지는 심판은 0표가 아니라 **제외**한다.
  // 0표는 "적정"이라는 주장이라, 적자·신규 상장·표본 부족 종목이 근거 없이 적정 쪽으로 끌려간다.
  // 배수 심판은 유효 배수 3개 이상일 때만 성립한다. 현금흐름이 기권하거나 성립한 심판이 2명 미만이면 판정 보류.
  const valid = side => side && side.score != null
    && (side.metrics || []).filter(m => m.score != null).length >= 3;
  const vote = s => s >= 70 ? 1 : s < 30 ? -1 : 0;
  // '매우 싸다'는 +1만 준다(2026-09-25 사용자 결정) — S&P500 검증에서 내재가치 대비 가장 싼 무리가
  // 오히려 부진했다(가치 함정: 보험·헬스케어·자동차·크루즈). 효과는 중간 구간 순위에서 나왔다.
  const DV = {'매우 싸다': 1, '싸다': 1, '적정': 0, '비싸다': -1, '매우 비싸다': -2};
  const lv = dcfLevel(last[4], D);
  const judges = [
    ['자기 이력', valid(V.self) ? vote(V.self.score) : null, V.self && V.self.score, 1],
    ['동종업', valid(V.peer) ? vote(V.peer.score) : null, V.peer && V.peer.score, 1],
    ['초과이익', lv.label in DV ? DV[lv.label] : null, lv.label, 2],
  ];
  const seated = judges.filter(j => j[1] != null);
  const maxW = seated.reduce((a, j) => a + j[3], 0);
  const total = seated.reduce((a, j) => a + j[1], 0);
  const dcfIn = judges[2][1] != null;
  // 기권이 있으면 최대 가능 표(전원 4표)에 맞춰 늘려 같은 문턱을 쓴다.
  const n = maxW ? total * 4 / maxW : 0;
  T_VERDICT = (!dcfIn || seated.length < 2) ? '판정 보류'
    : n >= 3 ? '저평가' : n >= 1 ? '적정~저평가' : n > -1 ? '적정' : n > -3 ? '적정~고평가' : '고평가';
  const sgn = v => (v > 0 ? '+' : v < 0 ? '−' : '') + Math.abs(v);
  const tip = judges.map(j => `${j[0]} ${typeof j[2] === 'number' ? j[2].toFixed(1) : (j[2] ?? '—')} → `
      + (j[1] == null ? '기권' : sgn(j[1]))).join('\n')
    + `\n심판 ${seated.length}/3 · 합계 ${sgn(total)}` + (maxW && maxW < 4 ? ` (4표 기준 ${(n < 0 ? '−' : n > 0 ? '+' : '') + Math.abs(n).toFixed(1)})` : '')
    + ` → ${T_VERDICT}`
    + '\n(+3 이상 저평가 · +1~+2 적정~저평가 · 0 적정 · −1~−2 적정~고평가 · −3 이하 고평가)'
    + (lv.label === '매우 싸다' ? '\n⚠ 초과이익이 "매우 싸다"여도 +1만 준다 — 가장 싼 무리에는 가치 함정이 많았다. 왜 싼지 확인할 것.' : '');
  document.querySelectorAll('[data-verdict]').forEach(el => { el.textContent = T_VERDICT; el.title = tip; });
  // A7(2026-10-04 사용자 결정 — 표시만, 판정 규칙은 그대로): 자기 이력·동종업 점수가 문턱(30·70) ±2점 안이고 그 칸 표가
  // 한 칸만 바뀌어도 종합 판정이 달라지면 헤더 판정 밑에 작게 적는다.
  const verdictOf = js => { const s = js.filter(j => j[1] != null), w = s.reduce((a, j) => a + j[3], 0), t = s.reduce((a, j) => a + j[1], 0), m = w ? t * 4 / w : 0;
    return (js[2][1] == null || s.length < 2) ? '판정 보류' : m >= 3 ? '저평가' : m >= 1 ? '적정~저평가' : m > -1 ? '적정' : m > -3 ? '적정~고평가' : '고평가'; };
  const edges = [];
  // 카드 규칙과 같은 식으로 다시 낸 판정이 실제 판정과 같을 때만 본다(은행 등 판정 식이 다른 카드는 건너뜀)
  if (verdictOf(judges) === T_VERDICT) judges.slice(0, 2).forEach((j, i) => {
    if (j[1] == null || typeof j[2] !== 'number') return;
    [30, 70].forEach(th => {
      if (Math.abs(j[2] - th) > 2) return;
      const js = judges.map(x => x.slice()); js[i][1] = j[2] >= th ? j[1] - 1 : j[1] + 1;
      const v = verdictOf(js);
      if (v !== T_VERDICT) edges.push(`${j[0]} ${j[2].toFixed(1)}점이 문턱 ${th} 옆이라 그 칸 표가 한 칸 바뀌면 ${v}`);
    });
  });
  document.querySelectorAll('[data-verdict]').forEach(el => {
    if (edges.length) el.title += '\n\n경계: ' + edges.join(' / ');
  });
})