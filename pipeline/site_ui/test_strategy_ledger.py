#!/usr/bin/env python3
"""Tests for build_strategy_ledger.py (2026-10-19). Run: python3 pipeline/site_ui/test_strategy_ledger.py"""
import json
import shutil
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_strategy_ledger as b  # noqa: E402

ET = b.fetch_prices.ET
NOW = datetime(2026, 10, 20, 11, 0, tzinfo=ET)   # the morning after session 10-19, when v2 cards finish


def chart(bars, splits=()):
    """A Yahoo daily chart: bars [(date, close)], splits [(date, num, den)]."""
    ts = [int(datetime.fromisoformat(d).replace(hour=9, minute=30, tzinfo=ET).timestamp()) for d, _ in bars]
    ev = {str(t): {"date": t, "numerator": n, "denominator": m}
          for t, n, m in ((int(datetime.fromisoformat(d).replace(hour=9, minute=30, tzinfo=ET).timestamp()), n, m)
                          for d, n, m in splits)}
    res = {"timestamp": ts, "indicators": {"quote": [{"close": [c for _, c in bars], "volume": [1000] * len(bars)}]}}
    if ev:
        res["events"] = {"splits": ev}
    return {"chart": {"result": [res]}}


class LedgerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        (self.tmp / "site_data").mkdir()
        (self.tmp / "v2").mkdir()
        (self.tmp / "pipeline").mkdir()
        (self.tmp / "pipeline" / "sync_v2_home.py").write_text('RULE = "v2-verdict"\n')
        self.fx = self.tmp / "fixtures"
        self.fx.mkdir()
        self._repo, self._ledger = b.REPO, b.LEDGER
        b.REPO, b.LEDGER = self.tmp, self.tmp / "site_data" / "strategy_ledger"
        self.stocks(session="2026-10-19")
        self.status(session="2026-10-19")
        bars = [("2026-10-16", 100.0), ("2026-10-19", 101.0)]
        for t in ["AAA", "BBB", "SPY", "RSP", "QQQ", "OLD", "BRK-B"]:
            self.fixture(t, chart(bars))

    def tearDown(self):
        b.REPO, b.LEDGER = self._repo, self._ledger
        shutil.rmtree(self.tmp)

    def stocks(self, session, tickers=None):
        tickers = tickers or [
            {"ticker": "AAA", "cardAsOf": session, "price": {"close": 50.0, "session": session, "status": "fresh"},
             "tier": {"value": "적정", "status": "valid"}},
            {"ticker": "BBB", "cardAsOf": session, "price": {"close": 20.0, "session": session, "status": "fresh"},
             "tier": {"value": None, "status": "missing"}},
        ]
        (self.tmp / "site_data" / "stocks.json").write_text(json.dumps(
            {"priceSession": session, "scoreVersion": "v2", "tickers": tickers}))

    def status(self, session, finished=True, cards=None):
        d = {"session": session, "full": True, "failed": [], "cards": cards or {}}
        if finished:
            d["finished"] = "2026-10-20T15:00:00+0000"
        (self.tmp / "v2" / "daily_status.json").write_text(json.dumps(d))

    def fixture(self, sym, data):
        (self.fx / f"{sym}.json").write_text(json.dumps(data))

    def run_build(self):
        return b.build(NOW, str(self.fx), lookup_publish=False)

    def read(self, session):
        return json.loads((b.LEDGER / f"{session}.json").read_text())

    def test_skips_until_verdicts_finish(self):
        self.status(session="2026-10-16")
        self.assertIsNone(self.run_build()[0])
        self.status(session="2026-10-19", finished=False)
        self.assertIsNone(self.run_build()[0])
        self.assertFalse(b.LEDGER.exists())

    def test_writes_once_and_never_rewrites(self):
        out, _ = self.run_build()
        first = out.read_bytes()
        self.stocks(session="2026-10-19", tickers=[
            {"ticker": "AAA", "cardAsOf": "2026-10-19", "price": {"close": 999.0, "session": "2026-10-19", "status": "fresh"},
             "tier": {"value": "고평가", "status": "valid"}}])
        self.assertIsNone(self.run_build()[0])
        self.assertEqual(out.read_bytes(), first)
        self.assertEqual(json.loads((b.LEDGER / "index.json").read_text())["sessions"], ["2026-10-19"])

    def test_card_fields_and_fixed_etfs(self):
        self.run_build()
        r = self.read("2026-10-19")
        self.assertEqual(r["cards"]["AAA"], {"tier": "적정", "tierStatus": "valid", "close": 50.0,
                                             "verdictAsOf": "2026-10-19", "priceStale": False})
        self.assertIsNone(r["cards"]["BBB"]["tier"])          # missing verdict stays empty
        self.assertEqual(r["prices"], {"QQQ": 101.0, "RSP": 101.0, "SPY": 101.0})
        self.assertEqual(r["ruleVersion"], "v2-verdict")

    def test_stale_price_and_failed_card(self):
        self.stocks(session="2026-10-19", tickers=[
            {"ticker": "AAA", "cardAsOf": "2026-10-16", "price": {"close": 49.0, "session": "2026-10-16", "status": "fresh"},
             "tier": {"value": "적정", "status": "valid"}},
            {"ticker": "BBB", "cardAsOf": "2026-10-19", "price": {"close": 20.0, "session": "2026-10-19", "status": "fresh"},
             "tier": {"value": "저평가", "status": "valid"}}])
        self.status(session="2026-10-19", cards={"BBB": {"status": "failed"}})
        self.run_build()
        r = self.read("2026-10-19")
        self.assertIsNone(r["cards"]["AAA"]["close"])
        self.assertTrue(r["cards"]["AAA"]["priceStale"])
        self.assertIn("AAA", r["missing"])
        self.assertTrue(r["cards"]["BBB"]["priceStale"])      # v2 card run failed -> verdict not fresh

    def test_dropped_card_keeps_a_price_and_its_symbol(self):
        b.LEDGER.mkdir(parents=True)
        (b.LEDGER / "2026-10-16.json").write_text(json.dumps(
            {"session": "2026-10-16", "cards": {"OLD": {"tier": "적정"}, "BRKB": {"tier": None, "yahooSymbol": "BRK-B"}},
             "splits": []}))
        self.run_build()
        r = self.read("2026-10-19")
        self.assertEqual(r["prices"]["OLD"], 101.0)
        self.assertEqual(r["prices"]["BRKB"], 101.0)          # fetched as BRK-B
        self.assertEqual(r["prevSession"], "2026-10-16")
        self.assertEqual(json.loads((b.LEDGER / "index.json").read_text())["sessions"], ["2026-10-16", "2026-10-19"])

    def test_extra_ticker_without_bar_is_missing(self):
        (self.fx / "RSP.json").unlink()
        self.fixture("QQQ", chart([("2026-10-16", 100.0)]))   # no bar for the session
        self.run_build()
        r = self.read("2026-10-19")
        self.assertIn("RSP", r["missing"])
        self.assertIn("QQQ", r["missing"])
        self.assertNotIn("QQQ", r["prices"])

    def test_splits_carry_late_skip_seen_and_future(self):
        b.LEDGER.mkdir(parents=True)
        (b.LEDGER / "2026-10-15.json").write_text(json.dumps(
            {"session": "2026-10-15", "cards": {}, "splits": [{"id": "BBB:2026-10-14"}]}))
        bars = [("2026-10-14", 10.0), ("2026-10-16", 5.0), ("2026-10-19", 5.1)]
        self.fixture("AAA", chart(bars, splits=[("2026-10-16", 2, 1), ("2026-10-21", 3, 1)]))   # late one + a future one
        self.fixture("BBB", chart(bars, splits=[("2026-10-14", 2, 1)]))                         # already recorded
        self.run_build()
        r = self.read("2026-10-19")
        self.assertEqual(r["splits"], [{"id": "AAA:2026-10-16", "ticker": "AAA", "effectiveDate": "2026-10-16", "ratio": 2.0}])

    def test_published_at_uses_push_not_commit(self):
        calls = []

        class R:
            def __init__(self, out="", code=0):
                self.stdout, self.returncode = out, code

        def fake(cmd, **kw):
            calls.append(cmd)
            if cmd[:2] == ["git", "log"]:
                return R("c0ffee\n")
            if cmd[:2] == ["gh", "api"]:
                return R("2026-10-20T15:05:00Z\taaa\tbbb\n2026-10-20T16:00:00Z\tbbb\tccc\n")
            if cmd[:2] == ["git", "merge-base"]:
                return R(code=0 if cmd[-1] in ("bbb", "ccc") else 1)
            raise AssertionError(cmd)
        b.LEDGER.mkdir(parents=True)
        f = b.LEDGER / "2026-10-16.json"
        f.write_text("{}")
        self.assertEqual(b.published_at(f, run=fake), "2026-10-20T15:05:00Z")


if __name__ == "__main__":
    unittest.main(verbosity=1)
