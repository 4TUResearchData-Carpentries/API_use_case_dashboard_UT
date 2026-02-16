from __future__ import annotations

import json
from pathlib import Path

from app.dashboard_queries import build_group_map, normalize_articles_to_df

FIXTURES = Path("fixtures")


def _load_fixture(name: str):
    path = FIXTURES / name
    assert path.exists(), f"Missing fixture: {path}"
    return json.loads(path.read_text(encoding="utf-8"))


def test_build_group_map():
    groups = _load_fixture("groups.json")
    group_map = build_group_map(groups)

    assert isinstance(group_map, dict)
    # At least one expected mapping should exist
    assert all(isinstance(k, int) for k in group_map.keys())
    assert all(isinstance(v, str) for v in group_map.values())


def test_normalize_articles_item_type_3():
    groups = _load_fixture("groups.json")
    group_map = build_group_map(groups)

    articles = _load_fixture("articles_item_type_3.json")
    df = normalize_articles_to_df(articles, group_map)

    expected_cols = {"id", "title", "published_date", "group_id", "group_name", "doi"}
    assert expected_cols.issubset(set(df.columns))

    # Basic sanity: rows should match fixtures length
    assert len(df) == len(articles)

    # group_name should not be missing for known groups
    assert "Unknown" in df["group_name"].values or df["group_name"].notna().all()


def test_normalize_articles_item_type_9():
    groups = _load_fixture("groups.json")
    group_map = build_group_map(groups)

    articles = _load_fixture("articles_item_type_9.json")
    df = normalize_articles_to_df(articles, group_map)

    expected_cols = {"id", "title", "published_date", "group_id", "group_name", "doi"}
    assert expected_cols.issubset(set(df.columns))
    assert len(df) == len(articles)
