from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests

from .endpoints import Endpoints


class FourTUClient:
    """
    Minimal API client for workshop use cases.
    - Optional token authentication (not required for public monitoring)
    - Small, explicit methods (easy to teach + reuse)
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        token: Optional[str] = None,
        timeout: Optional[int] = None,
    ) -> None:
        self.base_url = base_url or os.getenv("FOURTU_BASE_URL", "https://data.4tu.nl")
        self.token = token if token is not None else os.getenv("FOURTU_TOKEN", "")
        self.timeout = timeout or int(os.getenv("FOURTU_TIMEOUT", "30"))

        self.endpoints = Endpoints(self.base_url)

        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})
        if self.token:
            # Matches your existing workshop convention
            self.session.headers.update({"Authorization": f"token {self.token}"})

    def get_articles(
        self,
        *,
        item_type: int = 3,
        published_since: str = "2025-01-01",
        limit: int = 100,
        offset: int = 0,
    ) -> Any:
        params = {
            "item_type": item_type,
            "published_since": published_since,
            "limit": limit,
            "offset": offset,
        }
        r = self.session.get(self.endpoints.articles(), params=params, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def get_groups(self) -> Any:
        r = self.session.get(self.endpoints.groups(), timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def get_article_detail(self, article_id: str) -> Any:
        r = self.session.get(self.endpoints.article_detail(article_id), timeout=self.timeout)
        r.raise_for_status()
        return r.json()
