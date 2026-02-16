from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Endpoints:
    base_url: str

    def articles(self) -> str:
        return f"{self.base_url.rstrip('/')}/v2/articles"

    def article_detail(self, article_id: str) -> str:
        return f"{self.base_url.rstrip('/')}/v2/articles/{article_id}"

    def groups(self) -> str:
        return f"{self.base_url.rstrip('/')}/v3/groups"
