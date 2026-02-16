from __future__ import annotations

import os
from typing import Any, Dict, List

import pandas as pd

from api.client import FourTUClient  # Relative import from the api module
from app.cache import load_json, save_json


def _get_env_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except ValueError:
        return default


def build_group_map(groups: List[Dict[str, Any]]) -> Dict[int, str]:
    """
    groups: list of objects with keys like {"id": <int>, "name": <str>}
    """
    out: Dict[int, str] = {}
    for g in groups:
        gid = g.get("id")
        name = g.get("name")
        if isinstance(gid, int) and isinstance(name, str):
            out[gid] = name
    return out


def normalize_articles_to_df(articles: List[Dict[str, Any]], group_map: Dict[int, str]) -> pd.DataFrame:
    rows = []
    for a in articles:
        gid = a.get("group_id")
        rows.append(
            {
                "id": a.get("id"),
                "title": a.get("title"),
                "published_date": a.get("published_date"),
                "group_id": gid,
                "group_name": group_map.get(gid, "Unknown"),
                "doi": a.get("doi"),
            }
        )
    df = pd.DataFrame(rows)
    return df


def fetch_recent_articles_paged(client: FourTUClient, item_type: int) -> List[Dict[str, Any]]:
    """
    Pull N pages of recent articles using limit+offset (MVP).
    This keeps load bounded and workshop-friendly.
    """
    published_since = os.getenv("UC01_PUBLISHED_SINCE", "2025-01-01")
    page_size = _get_env_int("UC01_PAGE_SIZE", 100)
    max_pages = _get_env_int("UC01_MAX_PAGES", 3)


    all_articles: List[Dict[str, Any]] = []
    for page in range(max_pages):
        offset = page * page_size
        batch = client.get_articles(
            item_type=item_type,
            published_since=published_since,
            limit=page_size,
            offset=offset,
        )
        if not isinstance(batch, list):
            # Some APIs return an object, but for our workshop we expect a list.
            # If this happens, participants learn to inspect the response.
            break

        all_articles.extend(batch)
        if len(batch) < page_size:
            break

    return all_articles


def load_or_fetch_groups(client: FourTUClient, use_cache: bool = True) -> List[Dict[str, Any]]:
    if use_cache:
        cached = load_json("groups.json")
        if isinstance(cached, list):
            return cached
    groups = client.get_groups()
    if isinstance(groups, list) and use_cache:
        save_json("groups.json", groups)
    return groups if isinstance(groups, list) else []


def load_or_fetch_articles(client: FourTUClient, item_type: int , use_cache: bool = True) -> List[Dict[str, Any]]:
    cache_name = f"articles_recent_item_type_{item_type}.json"
    if use_cache:
        cached = load_json(cache_name)
        if isinstance(cached, list):
            return cached
    articles = fetch_recent_articles_paged(client,item_type=item_type)
    if use_cache:
        save_json(cache_name, articles)
    return articles


def build_monitoring_dataframe(item_type: int = 3, use_cache: bool = True) -> pd.DataFrame:
    client = FourTUClient()

    groups = load_or_fetch_groups(client, use_cache=use_cache)
    group_map = build_group_map(groups)

    articles = load_or_fetch_articles(client, item_type=item_type, use_cache=use_cache)
    df = normalize_articles_to_df(articles, group_map)

    # Normalize date column for filtering
    if "published_date" in df.columns:
        df["published_date"] = pd.to_datetime(df["published_date"], errors="coerce")

    return df
