// preview 전용 ETF 줄(2026-10-19). 라이브(stock-widgets-redesign)로 옮기지 않는다 — pipeline/site_ui/UI_DIFF.md 1절 etf.
// index.html은 `preview-only:etf` 꼬리표가 붙은 줄 3개(CSS, 데이터, 이 파일)로만 연결된다. 홈 "시장 지표" 접힘 구역 맨 위에
// ETF 선택 칩과 요약 한 줄을 넣는다. 값은 preview-only-etf-data.js(window.ETF_DATA, v2/etf/etf_daily.py가 쓴다)에서 읽는다.
// 규칙(v2/research/etf_verdict_prereg.md): 참고용·매수 기준 아님. builtFor가 홈 세션(StockData.meta.priceSession)과 다르면
// 묵음 — 판정·점수를 지우고 사유만 보인다. 데이터 파일이 없거나 깨져 ETF_DATA가 없으면 "불러오지 못함"을 보인다.
(function () {
  var ORDER = ['SPY'];   // 칩 순서. 새 ETF는 etf_daily.py와 사전 등록에 더한 뒤 여기에.
  var TIERS = ['저평가', '적정~저평가', '적정', '적정~고평가', '고평가', '카드 없음', '판정 보류', '그 밖 제외', '분류 안 됨'];
  var picked = ORDER[0];

  function pct(x, d) { return x == null ? '—' : (x * 100).toFixed(d == null ? 1 : d) + '%'; }
  function sgn(x) { return x == null ? '—' : (x > 0 ? '+' : x < 0 ? '−' : '') + Math.abs(x).toFixed(2); }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]; }); }

  function fin(x) { return typeof x === 'number' && isFinite(x); }
  // 형식 검사 — 어긋나면 "형식 오류" 보류로 그린다(값을 짐작해 채우지 않는다).
  function valid(d) {
    if (!d || typeof d !== 'object' || (d.status !== 'ok' && d.status !== 'held')) return false;
    if (d.status === 'held') return typeof d.reasonText === 'string';
    // 정상 판정은 규칙(v2/research/etf_verdict_prereg.md)이 낼 수 있는 값만 받는다: 점수 [−4, +3], 덮은 비중 [0.70, 1],
    // 막대 9칸이 모두 0~1이고 합 1, 5등급 합 = 덮은 비중, 상위 비중 0~1.
    if (TIERS.slice(0, 5).indexOf(d.verdict) < 0 || !fin(d.nbar) || d.nbar < -4 || d.nbar > 3) return false;
    if (!fin(d.coverage) || d.coverage < 0.7 || d.coverage > 1) return false;
    if (!d.bar || typeof d.bar !== 'object' || Array.isArray(d.bar)) return false;
    if (!TIERS.every(function (k) { return fin(d.bar[k]) && d.bar[k] >= 0 && d.bar[k] <= 1; })) return false;
    var sum = TIERS.reduce(function (a, k) { return a + d.bar[k]; }, 0);
    var five = TIERS.slice(0, 5).reduce(function (a, k) { return a + d.bar[k]; }, 0);
    if (Math.abs(sum - 1) > 1e-6 || Math.abs(five - d.coverage) > 1e-6) return false;
    if (!Array.isArray(d.top) || !d.top.every(function (t) { return t && typeof t.company === 'string' && fin(t.weight) && t.weight >= 0 && t.weight <= 1; })) return false;
    if (d.expense != null && (typeof d.expense !== 'object' || !fin(d.expense.pct))) return false;
    if (d.pending != null && (typeof d.pending !== 'object' || ['issuer_lag', 'home_lag'].indexOf(d.pending.kind) < 0
        || typeof d.pending.P !== 'string')) return false;
    return typeof d.S === 'string';
  }

  function line(d) {
    var session = ((window.StockData || {}).meta || {}).priceSession;
    var link = '<a class="etf-link" href="preview-only-etf-' + picked.toLowerCase() + '.html">카드 보기 ↗</a>';
    if (!d) return '<p class="etf-line etf-held">' + esc(picked) + ' · 판정 보류 · ETF 자료를 불러오지 못함 ' + link + '</p>';
    if (!valid(d)) return '<p class="etf-line etf-held">' + esc(picked) + ' · 판정 보류 · ETF 자료 형식 오류 ' + link + '</p>';
    // 갱신 대기(2026-10-20): ETF 단계가 "날짜만 어긋나 직전 판정을 유지했다"고 적은 경우만 묵음 대신 판정을 보인다.
    // 브라우저는 달력을 다시 계산하지 않고 ETF 단계가 쓴 pending.P만 홈 세션과 비교한다.
    var pd = d.status === 'ok' && d.pending ? d.pending : null;
    var lagIssuer = !!(pd && pd.kind === 'issuer_lag' && pd.P === session);
    var lagHome = !!(pd && pd.kind === 'home_lag' && d.builtFor === session);
    var stale = !d.builtFor || (d.builtFor !== session && !lagIssuer);
    if (stale || d.status !== 'ok') {
      var why = stale ? '묵음(ETF ' + esc(d.builtFor || '—') + ' · 홈 ' + esc(session || '—') + ')' : esc(d.reasonText);
      return '<p class="etf-line etf-held"><b>' + esc(d.etf) + '</b> · 판정 보류 · ' + why + ' ' + link + '</p>';
    }
    var bar = TIERS.map(function (k, i) {
      var w = (d.bar || {})[k];
      return w ? '<span class="etf-seg etf-seg-' + i + '" style="width:' + (w * 100).toFixed(3) + '%" title="' + esc(k) + ' ' + pct(w) + '"></span>' : '';
    }).join('');
    var top = (d.top || []).map(function (t) {
      return '<span class="etf-top">' + esc(t.company) + ' <span class="num">' + pct(t.weight) + '</span></span>';
    }).join('');
    return '<p class="etf-line"><b>' + esc(d.etf) + '</b> <span class="etf-verdict">' + esc(d.verdict) + '</span>'
      + (d.edgeNear ? ' <span class="etf-edge">경계 근처</span>' : '')
      + (lagIssuer ? ' <span class="etf-edge">운용사 파일 갱신 대기 · 판정 기준 ' + esc(d.builtFor) + '</span>' : '')
      + (lagHome ? ' <span class="etf-edge">홈 가격 세션 갱신 대기</span>' : '')
      + ' · 점수 <span class="num">' + sgn(d.nbar) + '</span>'
      + ' · 카드가 덮은 비중 <span class="num">' + pct(d.coverage) + '</span>'
      + (d.expense ? ' · 보수 <span class="num">' + d.expense.pct.toFixed(4) + '%</span>' : '')
      + ' · <span class="etf-ref">참고용 · 매수 기준 아님</span> ' + link + '</p>'
      + '<div class="etf-bar" role="img" aria-label="등급별 보유 비중">' + bar + '</div>'
      + '<p class="etf-tops">' + top + '<span class="etf-asof">보유 기준 ' + esc(d.S) + '</span></p>';
  }

  function render(box) {
    var all = window.ETF_DATA || {};
    box.innerHTML = '<div class="etf-chips" role="group" aria-label="ETF 선택">'
      + ORDER.map(function (t) { return '<button type="button" class="etf-chip" data-etf="' + t + '" aria-pressed="' + (t === picked) + '">' + t + '</button>'; }).join('')
      + '</div>' + safeLine(all[picked]);
  }

  function safeLine(d) {
    try { return line(d); }
    catch (e) { return '<p class="etf-line etf-held">' + esc(picked) + ' · 판정 보류 · ETF 자료 형식 오류</p>'; }
  }

  // 시장 지표의 S&P 500 칸 아래에 지수 카드 링크(2026-10-20, v2/index/index_daily.py가 만드는 preview-only-index-sp500.html).
  function linkIndex() {
    var v = document.getElementById('m-sp500');
    if (!v || !v.parentNode || v.parentNode.querySelector('.etf-index-link')) return;
    var a = document.createElement('a');
    a.className = 'etf-index-link';
    a.href = 'preview-only-index-sp500.html';
    a.textContent = '지수 카드 ↗';
    v.parentNode.appendChild(a);
  }

  function init() {
    linkIndex();
    var details = document.querySelector('details.market-demo');
    if (!details) return;
    var box = document.createElement('div');
    box.className = 'etf-strip';
    var summary = details.querySelector('summary');
    summary.parentNode.insertBefore(box, summary.nextSibling);
    box.addEventListener('click', function (e) {
      var b = e.target.closest('[data-etf]');
      if (b) { picked = b.dataset.etf; render(box); }
    });
    render(box);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
