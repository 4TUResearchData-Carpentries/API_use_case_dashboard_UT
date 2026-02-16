from __future__ import annotations

from typing import Any, Dict, List

from app.dashboard_queries import load_or_fetch_articles

# This one ensures you don’t regress to a single cache file like articles_recent.json.
# It patches your load_json/save_json to avoid filesystem dependence.

class DummyClient:
    def __init__(self, payload: List[Dict[str, Any]]):
        self.payload = payload

    def get_articles(self, **kwargs):
        return self.payload


def test_cache_name_includes_item_type(monkeypatch):
    # Arrange: dummy payload
    client = DummyClient(payload=[{"id": "x", "title": "t"}])

    seen_saved_names = []

    def fake_load_json(name: str):
        # no cache available
        return None

    def fake_save_json(name: str, data: Any):
        seen_saved_names.append(name)

    # Patch cache read/write inside module
    monkeypatch.setattr("app.dashboard_queries.load_json", fake_load_json)
    monkeypatch.setattr("app.dashboard_queries.save_json", fake_save_json)

    # Patch fetch_recent_articles_paged to avoid env-based loops
    monkeypatch.setattr("app.dashboard_queries.fetch_recent_articles_paged", lambda c, item_type: c.payload)

    # Act
    _ = load_or_fetch_articles(client, item_type=3, use_cache=True)
    _ = load_or_fetch_articles(client, item_type=9, use_cache=True)

    # Assert: different cache keys per item_type
    assert any("item_type_3" in name for name in seen_saved_names), seen_saved_names
    assert any("item_type_9" in name for name in seen_saved_names), seen_saved_names
