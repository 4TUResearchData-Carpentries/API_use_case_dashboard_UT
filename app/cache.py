from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional


def cache_dir() -> Path:
    d = Path("data/output/uc01_cache")
    d.mkdir(parents=True, exist_ok=True)
    return d


def load_json(name: str) -> Optional[Any]:
    path = cache_dir() / name
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(name: str, data: Any) -> None:
    path = cache_dir() / name
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
