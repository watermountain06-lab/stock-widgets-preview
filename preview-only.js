// preview 전용 기능(2026-10-17). 라이브(stock-widgets-redesign)로 옮기지 않는다 — pipeline/site_ui/UI_DIFF.md.
// index.html은 `preview-only:range` 꼬리표가 붙은 줄로만 이 파일과 연결된다(파일 싣기 2줄, 필터 1줄, 초기화 1줄).
//
// 순위 구간 고르기: [전체] [1~100위] … [401~500위](100위 단위, 2026-10-28 500위까지, 같은 날 드롭다운으로 바꿈). 그날 시총 순위(d.rank)로 행을 거른다. 탭 4개·검색·즐겨찾기와
// 함께 걸리고, 순위 칸 숫자의 기준(전체 등록 종목)은 바꾸지 않는다 — 보이는 행만 줄인다(2026-10-17 dr 합의).
// 고른 구간은 저장하지 않는다(사용자 결정).
window.PreviewOnly = (function () {
  // 카드가 아직 없는 구간도 미리 둔다(사용자 결정 2026-10-28 — 카드가 늘어날 것). 500위를 넘으면 여기에 더한다.
  var RANGES = [['all', '전체']];
  for (var lo = 1; lo <= 401; lo += 100) RANGES.push([lo + '-' + (lo + 99), lo + '~' + (lo + 99) + '위']);
  var range = 'all';

  function filter(d) {
    if (range === 'all') return true;
    var lohi = range.split('-');
    return d.rank >= +lohi[0] && d.rank <= +lohi[1];
  }

  // "분석 대상 N개 종목" 줄을 왼쪽 글자 + 오른쪽 드롭다운으로 바꾼다(2026-10-28 사용자가 고른 시안 B — 구간이 늘어도 한 칸).
  // index.html의 그 줄은 라이브와 같은 모양 그대로 둔다. 구간별 종목 수는 페이지의 공개 데이터(window.StockData)에서 센다.
  function counts() {
    var rows = (window.StockData && window.StockData.stocks) || [];
    var out = { all: rows.length };
    RANGES.slice(1).forEach(function (r) {
      var lohi = r[0].split('-');
      out[r[0]] = rows.filter(function (d) { return d.rank >= +lohi[0] && d.rank <= +lohi[1]; }).length;
    });
    return out;
  }

  function init(rerender) {
    var count = document.getElementById('ticker-count');
    if (!count) return;
    var line = count.parentNode;
    var label = document.createElement('span');
    while (line.firstChild) label.appendChild(line.firstChild);
    line.appendChild(label);
    line.classList.add('range-line');

    var n = counts();
    var wrap = document.createElement('div');
    wrap.className = 'range-dd';
    wrap.innerHTML =
      '<button type="button" class="range-dd-btn" aria-haspopup="listbox" aria-expanded="false" aria-controls="range-dd-list">' +
        '<span class="range-dd-key">시총 순위</span><strong class="range-dd-val"></strong><span class="range-dd-n"></span>' +
        '<svg aria-hidden="true" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg>' +
      '</button>' +
      '<div class="range-dd-list" id="range-dd-list" role="listbox" aria-label="시총 순위 구간" hidden>' +
        RANGES.map(function (r) {
          var empty = r[0] !== 'all' && !n[r[0]];
          return '<button type="button" class="range-dd-opt" role="option" data-range="' + r[0] + '"' +
            (empty ? ' aria-disabled="true"' : '') + ' aria-selected="' + (r[0] === range) + '">' +
            '<span>' + r[1] + '</span><span class="range-dd-count">' + (empty ? '카드 없음' : n[r[0]]) + '</span></button>';
        }).join('') +
      '</div>';
    line.appendChild(wrap);

    var btn = wrap.querySelector('.range-dd-btn'), list = wrap.querySelector('.range-dd-list');
    var opts = [].slice.call(list.querySelectorAll('.range-dd-opt'));
    function paint() {
      var cur = RANGES.filter(function (r) { return r[0] === range; })[0];
      btn.querySelector('.range-dd-val').textContent = cur[1];
      btn.querySelector('.range-dd-n').textContent = n[range];
      opts.forEach(function (o) { o.setAttribute('aria-selected', o.dataset.range === range); });
    }
    function open(v) {
      list.hidden = !v;
      btn.setAttribute('aria-expanded', v);
      if (v) (list.querySelector('[aria-selected="true"]') || opts[0]).focus();
    }
    paint();

    btn.addEventListener('click', function () { open(list.hidden); });
    list.addEventListener('click', function (e) {
      var o = e.target.closest('[data-range]');
      if (!o || o.getAttribute('aria-disabled') === 'true') return;
      open(false);
      btn.focus();
      if (o.dataset.range === range) return;
      range = o.dataset.range;
      paint();
      rerender();
    });
    // 키보드: 목록 안에서 ↑↓로 옮기고 Esc로 닫는다(목록에만 단다)
    list.addEventListener('keydown', function (e) {
      var live = opts.filter(function (o) { return o.getAttribute('aria-disabled') !== 'true'; });
      var i = live.indexOf(document.activeElement);
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
        e.preventDefault();
        live[(i + (e.key === 'ArrowDown' ? 1 : live.length - 1)) % live.length].focus();
      } else if (e.key === 'Escape') {
        open(false);
        btn.focus();
      }
    });
    document.addEventListener('click', function (e) { if (!list.hidden && !wrap.contains(e.target)) open(false); });
  }

  return { filter: filter, init: init };
})();

// Portfolio 메뉴(2026-10-19, preview-only:portfolio). 페이지마다 머리 메뉴 줄은 라이브와 같게 두고, 이 파일이 링크를 덧붙인다.
// index.html은 위 range 꼬리표 줄로, today.html·market-news.html은 `preview-only:portfolio` 꼬리표 줄로 이 파일을 싣는다.
(function () {
  function addLink() {
    var nav = document.querySelector('.site-header nav');
    if (!nav || nav.querySelector('[href="preview-only-portfolio.html"]')) return;
    var a = document.createElement('a');
    a.href = 'preview-only-portfolio.html';
    a.textContent = 'Portfolio';
    // 순서: Home · Tracking · Portfolio · 뉴스·영상(2026-10-22 사용자 결정) — 뉴스 링크 앞에 넣고, 없으면 끝에 붙인다
    var news = nav.querySelector('[href="market-news.html"]');
    nav.insertBefore(a, news);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', addLink);
  else addLink();
})();
