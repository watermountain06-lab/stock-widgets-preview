// preview 전용 기능(2026-10-17). 라이브(stock-widgets-redesign)로 옮기지 않는다 — pipeline/site_ui/UI_DIFF.md.
// index.html은 `preview-only:range` 꼬리표가 붙은 줄로만 이 파일과 연결된다(파일 싣기 2줄, 필터 1줄, 초기화 1줄).
//
// 순위 구간 토글: [전체] [1~100위] [101~200위]. 그날 시총 순위(d.rank)로 행을 거른다. 탭 4개·검색·즐겨찾기와
// 함께 걸리고, 순위 칸 숫자의 기준(전체 등록 종목)은 바꾸지 않는다 — 보이는 행만 줄인다(2026-10-17 dr 합의).
// 고른 구간은 저장하지 않는다(사용자 결정).
window.PreviewOnly = (function () {
  var RANGES = [['all', '전체'], ['1-100', '1~100위'], ['101-200', '101~200위']];
  var range = 'all';

  function filter(d) {
    if (range === 'all') return true;
    var lohi = range.split('-');
    return d.rank >= +lohi[0] && d.rank <= +lohi[1];
  }

  // "분석 대상 N개 종목" 줄을 왼쪽 글자 + 오른쪽 버튼 줄로 바꾼다. index.html의 그 줄은 라이브와 같은 모양 그대로 둔다.
  function init(rerender) {
    var count = document.getElementById('ticker-count');
    if (!count) return;
    var line = count.parentNode;
    var label = document.createElement('span');
    while (line.firstChild) label.appendChild(line.firstChild);
    line.appendChild(label);
    line.classList.add('range-line');

    var bar = document.createElement('div');
    bar.className = 'range-bar';
    bar.setAttribute('role', 'group');
    bar.setAttribute('aria-label', '시총 순위 구간');
    bar.innerHTML = RANGES.map(function (r) {
      return '<button type="button" class="range-btn" data-range="' + r[0] + '" aria-pressed="' + (r[0] === range) + '">' + r[1] + '</button>';
    }).join('');
    line.appendChild(bar);

    bar.addEventListener('click', function (e) {
      var b = e.target.closest('[data-range]');
      if (!b || b.dataset.range === range) return;
      range = b.dataset.range;
      bar.querySelectorAll('[data-range]').forEach(function (x) { x.setAttribute('aria-pressed', x === b); });
      rerender();
    });
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
