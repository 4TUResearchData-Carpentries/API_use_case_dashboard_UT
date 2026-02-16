from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import Mock

from api.client import FourTUClient

FIXTURES = Path("fixtures")

#These tests do not call the network. They patch requests.Session.get inside your client.
def _load_fixture(name: str):
    path = FIXTURES / name
    assert path.exists(), f"Missing fixture: {path}"
    return json.loads(path.read_text(encoding="utf-8"))


def _mock_response(payload, status_code=200):
    r = Mock()
    r.status_code = status_code
    r.json.return_value = payload
    r.raise_for_status.return_value = None
    return r


def test_client_get_groups_offline(monkeypatch):
    payload = _load_fixture("groups.json")

    client = FourTUClient(base_url="https://data.4tu.nl", token="", timeout=1)

    def fake_get(*args, **kwargs):
        return _mock_response(payload)

    monkeypatch.setattr(client.session, "get", fake_get)

    out = client.get_groups()
    assert isinstance(out, list)
    assert len(out) >= 1
    assert "id" in out[0]
    assert "name" in out[0]


def test_client_get_articles_offline_item_type_3(monkeypatch):
    payload = _load_fixture("articles_item_type_3.json")

    client = FourTUClient(base_url="https://data.4tu.nl", token="", timeout=1)

    def fake_get(*args, **kwargs):
        # ensure the call includes the expected params
        params = kwargs.get("params", {})
        assert params.get("item_type") == 3
        return _mock_response(payload)

    monkeypatch.setattr(client.session, "get", fake_get)

    out = client.get_articles(item_type=3, published_since="2025-01-01", limit=2, offset=0)
    assert isinstance(out, list)
    assert len(out) == len(payload)


def test_client_get_articles_offline_item_type_9(monkeypatch):
    payload = _load_fixture("articles_item_type_9.json")

    client = FourTUClient(base_url="https://data.4tu.nl", token="", timeout=1)

    def fake_get(*args, **kwargs):
        params = kwargs.get("params", {})
        assert params.get("item_type") == 9
        return _mock_response(payload)

    monkeypatch.setattr(client.session, "get", fake_get)

    out = client.get_articles(item_type=9, published_since="2025-01-01", limit=2, offset=0)
    assert isinstance(out, list)
    assert len(out) == len(payload)
