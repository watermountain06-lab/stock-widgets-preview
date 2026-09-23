# Stage 4 — the news layer

Status: **specced, not started.** Gated on the in-ticker valuation automation (stage 2B) finishing
first. Written 2026-09-23.

The daily refresh today runs prices → macro → build/validate → card price layer → commit if changed →
Pages build → health check, on three retry crons (22:00, 09:00, 13:00 UTC), and commits nothing when
nothing changed. This adds a fourth stage.

## Design principles carried over, not to be revisited

Values are generated at build time and never typed in. Structured JSON is the source of truth. A card
is edited **only between explicit markers** — whole-card regeneration is banned, because it corrupted
cards before. The v2 NVDA card already follows this: a script writes `const NVDA_XXX = {…}` between
`/* XXX:BEGIN */` and `/* XXX:END */`, and the page's JS draws from that constant
(`v2/build_peer_score.py --card`, `v2/build_activity_score.py`). See `v2/PRICE_CASCADE.md`.

The `#news` tab, in order: the interpretation card, then the `<!-- TODAY_NEWS_ANCHOR … -->` comment,
then the legend row, then the timeline card with its `.tl-item` list. The anchor comment and the start
of the legend row are the insertion region's two markers. A timeline item's reaction chip
(`<span class="tl-reaction" data-react="YYYY-MM-DD">`) is computed by JS from `NVDA_DAILY` against the
prior close — **never write a reaction % by hand.**

## Decisions to confirm before starting

1. **Where the automatic boundary sits.** Recommended: the "오늘의 뉴스" card publishes daily and
   automatically from primary sources only, while new timeline events and any interpretive sentence go
   out as a weekly draft PR for approval. Adding new timeline events is a judgment point already
   reserved to a person, and date, causation and source errors have recurred.
2. **Who writes the sentences.** Recommended: the daily portion is a deterministic template (title,
   date, link, reaction %), and sentence-level summary happens only in the weekly PR step. Running an
   LLM inside Actions would need an API key and cost.
3. **Scope.** v2 cards first (NVDA is the only one). The 50 root cards come later, with the v2 rollout.

## Goals

**A — daily, automatic.** Per ticker, accumulate the last N days (default 7) of primary-source events
into `site_data/news/{T}.json`, and render them into the card's `TODAY_NEWS_ANCHOR` region as a
`NVDA_TODAY_NEWS` block plus its card.

**B — weekly, approved.** Timeline candidates from the past 7 days that clear the bar, raised as a PR
with the verification notes.

## Sources, in priority order

1. **SEC EDGAR** — the CIK's 8-K/6-K filings (filing date, item codes, source link) via the
   data.sec.gov submissions API. User-Agent is required; reuse the existing `.sec_cache` rules and
   429 backoff.
2. **Company press / IR** RSS — nvidianews.nvidia.com, investor.nvidia.com, blogs.nvidia.com.
3. **Price trigger** — any day where `|change|` ≥ 5% from `NVDA_DAILY`. State the large move as a
   fact and say nothing about its cause.

Press coverage is evidence for a **B** candidate only. It never appears in **A**.

## Hard rules, each one a mistake that already shipped

- Announcement date and reaction date are different. An after-hours announcement reacts the next
  session; a weekend announcement reacts the next trading day. The reaction always comes from
  `NVDA_DAILY`.
- No forward references. Only what was public on that date, never backfilled from a later report's
  comparison figures.
- No unverifiable framing. "Beat consensus" or "fell on concerns about X" only when the source says
  so. A guidance comparison is checkable in the company release, so cite that instead.
- The link must match the event by date and subject. A 200 response proves nothing.
- Labels like "52-week low" are computed, never asserted. An intraday low was once written up as a
  52-week low.
- Dedupe one event's 8-K and press release into a single item, keyed on date plus title similarity.
- On source failure, keep yesterday's value and mark it stale. Yesterday's value with a label beats a
  strange new one.
- Edit only between the markers. If the marker pair is not exactly one pair, write nothing and record
  the failure in `card_status.json` so `health_check.py` reads it.

## Implementation

- **`pipeline/fetch_news.py`** — collect, normalise, dedupe → `site_data/news/{T}.json`, shaped
  `{"ticker", "asOf", "items": [{"date", "type": "8-K|press|price-move", "title", "url", "source",
  "itemCodes"?, "reactDate"?}], "stale": bool}`.
- **Card rendering** — either a `--card` option in the v2 style or a news layer inside
  `update_cards.py`. Replace the `TODAY_NEWS_ANCHOR` region and preserve the legend row.
- **`daily_refresh.yml`** — a "Fetch news" step after "Update cards", `site_data/news` and the v2 cards
  added to the `git add` list, `news.log` in the run summary.
- **A weekly workflow** (separate yml, e.g. Monday 13:00 UTC) — generate the candidate draft, and do
  not open a second PR while one is already open (at most one open PR). The body gives each candidate
  its source link, its date evidence, its `NVDA_DAILY` reaction, and the reason anything was excluded.
- **`pipeline/test_pipeline.py`** — offline tests on fixed fixtures covering collection, rendering and
  marker verification, with no network.

## Done means

- Offline tests pass, one manual `workflow_dispatch` run succeeds, and a no-change run commits nothing.
- The NVDA v2 card renders "오늘의 뉴스" from primary-source links only, and the existing timeline,
  interpretation card and legend are byte-for-byte unchanged — the before/after diff touches the
  marker region and nothing else.
- Browser check over a local server (`python3 -m http.server`) with zero console errors.
- `codex review --uncommitted` findings addressed, then summarised for the user.
- Commit and push only after the user approves, and `git fetch` before committing, since the pipeline
  commits to `main` directly.

## Out of scope

- Auto-publishing new timeline events or interpretive sentences, unless decision 1 changes.
- Anything in redesign (the live domain). Promotion stays approval-gated.
- Applying this to all 50 root cards at once. That rides with the v2 rollout.
