from __future__ import annotations

from datetime import date

import polars as pl

from app.services import market_overview_builder as builder


class _FakeSvc:
    def __init__(self, repo):
        self.repo = repo

    def latest_date(self):
        return date(2026, 6, 29)

    def _load_enriched_for_date(self, as_of):
        return pl.DataFrame()


class _FakeRepo:
    def __init__(self, data_dir):
        self.store = type("Store", (), {"data_dir": data_dir})()


class _FakeQuoteService:
    def status(self):
        return {"enabled": True, "running": True, "quote_age_ms": 100, "is_trading_hours": True}


def test_default_overview_keeps_indices_realtime_when_no_date_selected(monkeypatch, tmp_path):
    seen = {}

    def fake_index_quotes(repo, quote_service, as_of=None):
        seen["as_of"] = as_of
        return []

    monkeypatch.setattr(builder, "ScreenerService", _FakeSvc)
    monkeypatch.setattr(builder, "_index_quotes", fake_index_quotes)

    builder.build_market_overview(_FakeRepo(tmp_path), quote_service=_FakeQuoteService(), as_of=None)

    assert seen["as_of"] is None
