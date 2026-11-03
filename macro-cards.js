// Home 시장 지표 카드(2026-11-03, /design 시안 B + 지표별 작은 그림).
// 여섯 장을 가운데에 겹쳐 두고 3초마다 한 장씩 넘긴다. 카드마다 그 지표를 대표하는 그림을 넣는다:
//   S&P 500·원/달러 = 최근 1개월 선, VIX = 공포 게이지, 기준금리 = 2년 계단 + 다음 FOMC까지 남은 날,
//   실업률 = 최근 13번 막대, 물가 = 최근 12개월 선 + 연준 목표 2% 점선.
// 값과 기록은 stock-data.js의 meta.macro(preview site_data/macro.json → MACRO)에서 온다. 지표가 fresh가
// 아니면 대시를 보이고, 기록이 없으면 그림 자리에 "기록 쌓는 중"을 둔다. 값을 지어내지 않는다.
(function () {
  var host = document.getElementById('macro-cards');
  if (!host) return;
  var macro = (window.StockData && window.StockData.meta || {}).macro;
  var note = document.getElementById('macro-note');
  var SVG = 'http://www.w3.org/2000/svg';
  var W = 220, H = 64;   // 그림 상자

  function live(ind) { return ind && ind.status === 'fresh' ? ind : null; }
  function num(v, d) { return v.toLocaleString('en-US', { minimumFractionDigits: d, maximumFractionDigits: d }); }
  function md(iso) { var p = iso.split('-'); return Number(p[1]) + '/' + Number(p[2]); }
  function ym(s) { var p = s.split('-'); return p[0].slice(2) + '.' + p[1]; }
  function el(tag, attrs, text) {
    var e = document.createElement(tag);
    for (var k in attrs || {}) e.setAttribute(k, attrs[k]);
    if (text != null) e.textContent = text;
    return e;
  }
  function svg(tag, attrs) { var e = document.createElementNS(SVG, tag); for (var k in attrs) e.setAttribute(k, attrs[k]); return e; }
  function frame(label) { return svg('svg', { viewBox: '0 0 ' + W + ' ' + H, class: 'mc-art', role: 'img', 'aria-label': label }); }
  function scale(vals, pad) {
    var lo = Math.min.apply(null, vals), hi = Math.max.apply(null, vals);
    if (hi === lo) { lo -= 1; hi += 1; }
    var p = (hi - lo) * (pad || 0.12);
    lo -= p; hi += p;
    return function (v) { return H - 14 - (v - lo) / (hi - lo) * (H - 22); };
  }
  function axisText(s, x, y, anchor) { var t = svg('text', { x: x, y: y, 'text-anchor': anchor || 'start', class: 'mc-ax' }); t.textContent = s; return t; }

  // 최근 흐름 선(S&P 500·원/달러). 오르면 up 색, 내리면 down 색 — 사이트 등락 색과 같다.
  function line(hist, label) {
    if (!hist || hist.length < 2) return null;
    var vals = hist.map(function (p) { return p[1]; }), y = scale(vals);
    var step = W / (hist.length - 1);
    var pts = hist.map(function (p, i) { return (i * step).toFixed(1) + ',' + y(p[1]).toFixed(1); });
    var dir = vals[vals.length - 1] >= vals[0] ? 'mc-up' : 'mc-down';
    var s = frame(label + ' 최근 ' + hist.length + '거래일 흐름, ' + md(hist[0][0]) + '부터 ' + md(hist[hist.length - 1][0]) + '까지');
    s.append(svg('polygon', { points: '0,' + (H - 14) + ' ' + pts.join(' ') + ' ' + W + ',' + (H - 14), class: 'mc-area ' + dir }));
    s.append(svg('polyline', { points: pts.join(' '), class: 'mc-line ' + dir }));
    var last = pts[pts.length - 1].split(',');
    s.append(svg('circle', { cx: last[0], cy: last[1], r: 2.6, class: 'mc-dot ' + dir }));
    s.append(axisText(md(hist[0][0]), 0, H - 2), axisText(md(hist[hist.length - 1][0]), W, H - 2, 'end'));
    return s;
  }

  // VIX 공포 게이지: 반원에 네 구간(시장에서 흔히 쓰는 기준), 바늘은 0~40에서 값 위치.
  var VIX_ZONES = [[0, 15, '낮음'], [15, 20, '보통'], [20, 30, '높음'], [30, 40, '매우 높음']];
  function vixZone(v) { for (var i = 0; i < VIX_ZONES.length; i++) if (v < VIX_ZONES[i][1]) return VIX_ZONES[i][2]; return '매우 높음'; }
  function gauge(v) {
    var cx = W / 2, cy = H - 6, r = 46;
    var s = frame('VIX ' + num(v, 2) + ', ' + vixZone(v) + ' 구간(15 미만 낮음, 15–20 보통, 20–30 높음, 30 이상 매우 높음)');
    function at(t, rr) { var a = Math.PI * (1 - t); return [cx + rr * Math.cos(a), cy - rr * Math.sin(a)]; }
    VIX_ZONES.forEach(function (z, i) {
      var a = at(z[0] / 40, r), b = at(z[1] / 40, r);
      s.append(svg('path', { d: 'M' + a[0] + ' ' + a[1] + ' A' + r + ' ' + r + ' 0 0 1 ' + b[0] + ' ' + b[1], class: 'mc-zone mc-z' + i }));
    });
    var t = Math.max(0, Math.min(1, v / 40)), tip = at(t, r - 10);
    s.append(svg('line', { x1: cx, y1: cy, x2: tip[0].toFixed(1), y2: tip[1].toFixed(1), class: 'mc-needle' }));
    s.append(svg('circle', { cx: cx, cy: cy, r: 3.5, class: 'mc-hub' }));
    s.append(axisText('0', cx - r - 4, H - 2, 'end'), axisText('40+', cx + r + 4, H - 2));
    return s;
  }

  // 기준금리 2년 계단(상단 기준선 + 하단 옅은 띠)
  function steps(hist, todayIso) {
    if (!hist || !hist.length) return null;
    var end = todayIso || hist[hist.length - 1][0];
    var t0 = Date.parse(hist[0][0]), t1 = Date.parse(end);
    if (!(t1 > t0)) return null;
    var vals = []; hist.forEach(function (h) { vals.push(h[1], h[2]); });
    var y = scale(vals, 0.25), x = function (d) { return (Date.parse(d) - t0) / (t1 - t0) * W; };
    var s = frame('기준금리 범위 ' + md(hist[0][0]) + ' 이후 변화 ' + (hist.length - 1) + '번');
    var d = '', band = '';
    hist.forEach(function (h, i) {
      var xa = x(h[0]), xb = i + 1 < hist.length ? x(hist[i + 1][0]) : W;
      d += (i ? ' L' : 'M') + xa.toFixed(1) + ' ' + y(h[2]).toFixed(1) + ' L' + xb.toFixed(1) + ' ' + y(h[2]).toFixed(1);
      band += '<rect x="' + xa.toFixed(1) + '" y="' + y(h[2]).toFixed(1) + '" width="' + Math.max(0, xb - xa).toFixed(1) + '" height="' + (y(h[1]) - y(h[2])).toFixed(1) + '"/>';
    });
    var g = svg('g', { class: 'mc-band' }); g.innerHTML = band; s.append(g);
    s.append(svg('path', { d: d, class: 'mc-line mc-flat' }));
    s.append(axisText(ym(hist[0][0]), 0, H - 2), axisText('지금', W, H - 2, 'end'));
    return s;
  }

  // 실업률 막대(월별, 빈 달은 칸만 비운다)
  function months(a, b) { var out = [], y = +a.slice(0, 4), m = +a.slice(5, 7); while (true) { var k = y + '-' + String(m).padStart(2, '0'); out.push(k); if (k === b || out.length > 40) break; m++; if (m > 12) { m = 1; y++; } } return out; }
  function bars(hist, label) {
    if (!hist || hist.length < 2) return null;
    var map = {}; hist.forEach(function (h) { map[h[0]] = h[1]; });
    var ms = months(hist[0][0], hist[hist.length - 1][0]);
    var vals = hist.map(function (h) { return h[1]; });
    var lo = Math.min.apply(null, vals) - 0.3, hi = Math.max.apply(null, vals) + 0.1;
    var bw = W / ms.length, s = frame(label + ' 최근 ' + hist.length + '번 발표, ' + ym(ms[0]) + '부터 ' + ym(ms[ms.length - 1]) + '까지');
    ms.forEach(function (k, i) {
      if (!(k in map)) return;
      var h = (map[k] - lo) / (hi - lo) * (H - 22);
      s.append(svg('rect', { x: (i * bw + bw * 0.18).toFixed(1), y: (H - 14 - h).toFixed(1), width: (bw * 0.64).toFixed(1), height: h.toFixed(1), rx: 1.5, class: i === ms.length - 1 ? 'mc-bar mc-bar-now' : 'mc-bar' }));
    });
    s.append(axisText(ym(ms[0]), 0, H - 2), axisText(ym(ms[ms.length - 1]), W, H - 2, 'end'));
    return s;
  }

  // 물가 12개월 선 + 연준 목표 2% 점선
  function cpiLine(hist) {
    if (!hist || hist.length < 2) return null;
    var map = {}; hist.forEach(function (h) { map[h[0]] = h[1]; });
    var ms = months(hist[0][0], hist[hist.length - 1][0]);
    var vals = hist.map(function (h) { return h[1]; }).concat([2]);
    var y = scale(vals), step = W / (ms.length - 1);
    var s = frame('물가상승률 최근 ' + hist.length + '개월, 연준 목표 2%와 비교');
    s.append(svg('line', { x1: 0, x2: W, y1: y(2).toFixed(1), y2: y(2).toFixed(1), class: 'mc-target' }));
    s.append(axisText('목표 2%', 2, (y(2) - 3).toFixed(1)));
    var d = '', pen = false;
    ms.forEach(function (k, i) {
      if (!(k in map)) { pen = false; return; }
      d += (pen ? ' L' : ' M') + (i * step).toFixed(1) + ' ' + y(map[k]).toFixed(1); pen = true;
    });
    s.append(svg('path', { d: d.trim(), class: 'mc-line mc-flat' }));
    var lastY = y(hist[hist.length - 1][1]);
    s.append(svg('circle', { cx: W, cy: lastY.toFixed(1), r: 2.6, class: 'mc-dot mc-flat' }));
    s.append(axisText(ym(ms[0]), 0, H - 2), axisText(ym(ms[ms.length - 1]), W, H - 2, 'end'));
    return s;
  }

  function chip(v) {
    if (!Number.isFinite(v)) return el('span', { class: 'mc-chip' }, '—');
    return el('span', { class: 'mc-chip ' + (v >= 0 ? 'mc-up' : 'mc-down') }, (v >= 0 ? '+' : '−') + Math.abs(v).toFixed(2) + '%');
  }
  function daysTo(iso) { var t = Date.parse(iso + 'T00:00:00'); var now = new Date(); now.setHours(0, 0, 0, 0); return Math.round((t - now) / 86400000); }

  if (!macro) { if (note) note.textContent = '불러오지 못함'; return; }
  var ind = macro.indicators || {}, hist = macro.history || {};
  var sp = live(ind.sp500), vx = live(ind.vix), fx = live(ind.usdkrw), fed = live(ind.fedTarget), un = live(ind.unemployment), cpi = live(ind.cpiYoy);
  var fomc = macro.nextFomc;
  var specs = [
    { label: 'S&P 500', value: sp ? num(sp.value, 2) : '—', sub: chip(sp && sp.changePct), art: sp && line(hist.sp500, 'S&P 500') },
    { label: 'VIX 변동성', value: vx ? num(vx.value, 2) : '—', sub: vx ? el('span', { class: 'mc-chip mc-flat' }, vixZone(vx.value) + ' · ' + (vx.changePct >= 0 ? '+' : '−') + Math.abs(vx.changePct).toFixed(2) + '%') : chip(NaN), art: vx && gauge(vx.value) },
    { label: '원/달러', value: fx ? '₩' + num(fx.value, 2) : '—', sub: chip(fx && fx.changePct), art: fx && line(hist.usdkrw, '원/달러') },
    { label: '기준금리', value: fed ? fed.lower.toFixed(2) + '–' + fed.upper.toFixed(2) + '%' : '—',
      sub: el('span', { class: 'mc-chip mc-flat' }, fomc && fomc.start ? '다음 FOMC ' + md(fomc.start) + (daysTo(fomc.start) >= 0 ? ' · ' + daysTo(fomc.start) + '일 남음' : '') : '일정 확인 필요'),
      art: fed && steps(hist.fedTarget, macro.priceSession) },
    { label: '실업률', value: un ? un.value.toFixed(1) + '%' : '—', sub: el('span', { class: 'mc-chip mc-flat' }, un ? ym(un.asOf) + ' 발표' : '—'), art: un && bars(hist.unemployment, '실업률') },
    { label: '물가상승률(전년 대비)', value: cpi ? cpi.value.toFixed(1) + '%' : '—', sub: el('span', { class: 'mc-chip mc-flat' }, cpi ? ym(cpi.asOf) + ' 발표' : '—'), art: cpi && cpiLine(hist.cpiYoy) }
  ];

  var stage = el('div', { class: 'mc-stage' });
  var cards = specs.map(function (c, i) {
    var b = el('button', { type: 'button', class: 'mc-card', 'aria-label': c.label + ' ' + c.value });
    b.append(el('span', { class: 'mc-label' }, c.label), el('strong', { class: 'mc-value num' }, c.value), c.sub);
    var art = el('span', { class: 'mc-artbox' });
    if (c.art) art.append(c.art); else art.append(el('span', { class: 'mc-wait' }, '기록 쌓는 중'));
    b.append(art);
    b.addEventListener('click', function () { if (i !== active) go(i); });
    stage.append(b);
    return b;
  });
  var bar = el('div', { class: 'mc-controls' });
  var prev = el('button', { type: 'button', class: 'mc-nav', 'aria-label': '이전 지표' }, '◀');
  var pos = el('span', { class: 'mc-pos' });
  var next = el('button', { type: 'button', class: 'mc-nav', 'aria-label': '다음 지표' }, '▶');
  var track = el('span', { class: 'mc-progress', 'aria-hidden': 'true' }); var fill = el('span'); track.append(fill);
  bar.append(prev, track, pos, next);
  host.replaceChildren(stage, bar);

  var n = cards.length, active = 0, paused = false;
  var narrow = matchMedia('(max-width: 600px)'), reduced = matchMedia('(prefers-reduced-motion: reduce)');
  function render() {
    var near = narrow.matches ? 132 : 190, step = narrow.matches ? 64 : 137;
    cards.forEach(function (c, i) {
      var d = i - active;
      if (d > n / 2) d -= n;
      if (d < -n / 2) d += n;
      var ad = Math.abs(d);
      var x = ad === 0 ? 0 : Math.sign(d) * (near + (ad - 1) * step);
      var sc = ad === 0 ? 1 : Math.max(0.6, 0.86 - (ad - 1) * 0.1);
      c.style.transform = 'translateX(calc(-50% + ' + x + 'px)) scale(' + sc + ')';
      c.style.zIndex = String(20 - ad);
      c.style.opacity = String([1, 0.72, 0.38][ad] != null ? [1, 0.72, 0.38][ad] : 0);
      c.style.filter = 'blur(' + (ad * 1.4) + 'px)';
      c.classList.toggle('is-current', ad === 0);
      c.tabIndex = ad <= 1 ? 0 : -1;
      c.setAttribute('aria-hidden', String(ad > 1));
    });
    pos.textContent = (active + 1) + ' / ' + n;
    fill.style.width = ((active + 1) / n * 100) + '%';
  }
  function go(i) { active = (i + n) % n; render(); }
  prev.addEventListener('click', function () { go(active - 1); });
  next.addEventListener('click', function () { go(active + 1); });
  host.addEventListener('keydown', function (e) {   // 이 상자 안에서만(전역 키 처리 없음)
    if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') { e.preventDefault(); go(active + (e.key === 'ArrowLeft' ? -1 : 1)); }
  });
  host.addEventListener('mouseenter', function () { paused = true; });
  host.addEventListener('mouseleave', function () { paused = false; });
  host.addEventListener('focusin', function () { paused = true; });
  host.addEventListener('focusout', function () { paused = false; });
  var touchX = null;
  host.addEventListener('touchstart', function (e) { touchX = e.touches[0].clientX; paused = true; }, { passive: true });
  host.addEventListener('touchend', function (e) {
    if (touchX !== null) { var dx = e.changedTouches[0].clientX - touchX; if (Math.abs(dx) > 40) go(active + (dx < 0 ? 1 : -1)); }
    touchX = null; paused = false;
  }, { passive: true });
  narrow.addEventListener('change', render);
  // 3초마다 넘김. 화면에 안 보일 때(구역 접힘·ETF 탭·탭 숨김)와 움직임 줄이기 설정에서는 멈춘다.
  setInterval(function () {
    if (paused || reduced.matches || document.hidden || !host.offsetParent) return;
    go(active + 1);
  }, 3000);
  render();

  var asOf = (sp && sp.asOf) || macro.priceSession;
  if (note) note.textContent = asOf ? asOf.replace(/-/g, '.') + ' 기준' : '기준일 미상';
})();
