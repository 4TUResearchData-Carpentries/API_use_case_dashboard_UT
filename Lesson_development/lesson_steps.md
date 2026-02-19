
## Learning outcomes

By the end, participants can:

* explain the **request → JSON → DataFrame → UI** pipeline
* paginate an API endpoint with **limit/offset**
* use `.env` configuration (BASE_URL, TOKEN, TIMEOUT)
* add **filters + download**
* optionally add **caching + diagnostics**

---

## Timeboxed agenda (2h30)

### 0:00–0:10 — Orientation + “What we’re building”

* Show final dashboard briefly (your MVP).
* Explain the “thin client + transformations + UI” structure.
* Confirm everyone can run:

  * `source .venv/bin/activate`
  * `streamlit run lesson_code.py`

Deliverable: participants see a Streamlit page (even if blank).

---

### 0:10–0:25 — Step 1: Minimal Streamlit app (no API yet)

**Goal:** a Streamlit page with a sidebar and a placeholder table.

Build:

* `st.set_page_config`, `st.title`, `st.sidebar`
* A dummy `pd.DataFrame` and `st.dataframe(df)`



Deliverable: app runs; participants understand Streamlit layout basics.

```python

import streamlit as st

st.set_page_config(page_title="4TU Monitoring", layout="wide")
st.title("4TU Monitoring Dashboard")


with st.sidebar:
    st.header("Query")

```

---

### 0:25–0:45 — Step 2: First API call (GET groups)

**Goal:** introduce the API + `requests.get`.

Build:

* `load_dotenv()`
* `BASE_URL`, `TIMEOUT`, `TOKEN`
* `headers()` function
* `get_groups()` function
* Show groups count + first 5 groups in the app

Talking points:

* `raise_for_status()` (fail fast)
* `timeout` (avoid hanging)
* “defensive JSON parsing” (list vs dict)

Deliverable: sidebar shows “Groups loaded: N”.

---

### 0:45–1:10 — Step 3: Articles page (one page only)

**Goal:** fetch datasets/software from `/v2/articles` with query params.

Build:

* sidebar controls:

  * item type select: Dataset (3) / Software (9)
  * published_since
  * page_size
* `get_articles_page(...)`
* Display raw JSON in an expander (`st.json(...)`) for understanding the structure

Deliverable: participants see live data from the API.

---

### 1:10–1:30 — Step 4: Pagination loop (limit/offset)

**Goal:** fetch multiple pages safely.

Build:

* `get_recent_articles(..., max_pages)`
* explain stop condition: `len(batch) < page_size`
* show “Loaded N articles” metric

Deliverable: they can tune page_size/max_pages and see effect.

---

### 1:30–1:50 — Step 5: Transform JSON → DataFrame + group names

**Goal:** make dashboard-friendly tabular data.

Build:

* `build_group_map(groups)`
* `to_dataframe(articles, group_map)`
* parse `published_date` to datetime
* show dataframe with key columns:

  * title, group_name, published_date, doi

Deliverable: clean table appears.

---

### 1:50–2:10 — Step 6: Filters + CSV download

**Goal:** make it “a dashboard” not just a table.

Build:

* group filter (selectbox)
* date range filter (date_input) based on min/max
* keyword filter on title
* download button CSV

Deliverable: participants can explore and export.

---

### 2:10–2:25 — Step 7: Caching + refresh + diagnostics

**Goal:** introduce performance + reproducibility.

Build:

* `@st.cache_data`
* `use_cache` checkbox and `refresh` button to clear
* diagnostics expander: rows + columns

Deliverable: dashboard becomes responsive and stable.

---

### 2:25–2:30 — Branching ideas (“make it yours”)

Give them 3–5 concrete extensions they can implement immediately:

* Add a column: e.g., `url` / `authors` / `license` if present
* Add a “Top groups by count” bar chart (`value_counts()`)
* Add a “DOI present?” filter
* Add a “Published per month” aggregation

---

## Teaching version: “progressive build” in one file

Below is the **skeleton** you can live-code through. You’ll gradually replace `TODO` blocks as you go. This is designed so the file remains runnable at each step.

```python
from __future__ import annotations

import os
from typing import Any, Dict, List

import pandas as pd
import requests
import streamlit as st
from dotenv import load_dotenv


# ============================================================
# Step 0 — Config
# ============================================================
load_dotenv()

BASE_URL = os.getenv("FOURTU_BASE_URL", "https://data.4tu.nl").rstrip("/")
TIMEOUT = int(os.getenv("FOURTU_TIMEOUT", "30"))
TOKEN = os.getenv("FOURTU_TOKEN", "").strip()

DEFAULT_PUBLISHED_SINCE = os.getenv("UC01_PUBLISHED_SINCE", "2025-01-01")
DEFAULT_PAGE_SIZE = int(os.getenv("UC01_PAGE_SIZE", "100"))
DEFAULT_MAX_PAGES = int(os.getenv("UC01_MAX_PAGES", "3"))


def headers() -> Dict[str, str]:
    """Build HTTP headers (add auth only if TOKEN is set)."""
    h = {"Accept": "application/json"}
    if TOKEN:
        h["Authorization"] = f"token {TOKEN}"
    return h


# ============================================================
# Step 1 — Client functions (API calls)
# ============================================================
def get_groups() -> List[Dict[str, Any]]:
    """GET /v3/groups"""
    url = f"{BASE_URL}/v3/groups"
    r = requests.get(url, headers=headers(), timeout=TIMEOUT)
    r.raise_for_status()
    data = r.json()
    return data if isinstance(data, list) else []


def get_articles_page(
    *,
    item_type: int,
    published_since: str,
    limit: int,
    offset: int,
) -> List[Dict[str, Any]]:
    """GET /v2/articles (one page)."""
    url = f"{BASE_URL}/v2/articles"
    params = {
        "item_type": item_type,
        "published_since": published_since,
        "limit": limit,
        "offset": offset,
    }
    r = requests.get(url, headers=headers(), params=params, timeout=TIMEOUT)
    r.raise_for_status()
    data = r.json()
    return data if isinstance(data, list) else []


def get_recent_articles(
    *,
    item_type: int,
    published_since: str,
    page_size: int,
    max_pages: int,
) -> List[Dict[str, Any]]:
    """Fetch multiple pages via limit/offset."""
    all_items: List[Dict[str, Any]] = []
    for page in range(max_pages):
        offset = page * page_size
        batch = get_articles_page(
            item_type=item_type,
            published_since=published_since,
            limit=page_size,
            offset=offset,
        )
        all_items.extend(batch)
        if len(batch) < page_size:
            break
    return all_items


# ============================================================
# Step 2 — Transformations (JSON -> DataFrame)
# ============================================================
def build_group_map(groups: List[Dict[str, Any]]) -> Dict[int, str]:
    """Map group_id -> group_name."""
    out: Dict[int, str] = {}
    for g in groups:
        gid = g.get("id")
        name = g.get("name")
        if isinstance(gid, int) and isinstance(name, str):
            out[gid] = name
    return out


def to_dataframe(articles: List[Dict[str, Any]], group_map: Dict[int, str]) -> pd.DataFrame:
    """Keep only columns we want in the dashboard."""
    rows = []
    for a in articles:
        gid = a.get("group_id")
        rows.append(
            {
                "id": a.get("id"),
                "title": a.get("title"),
                "published_date": a.get("published_date"),
                "group_name": group_map.get(gid, "Unknown"),
                "doi": a.get("doi"),
            }
        )

    df = pd.DataFrame(rows)
    if "published_date" in df.columns:
        df["published_date"] = pd.to_datetime(df["published_date"], errors="coerce")
    return df


# ============================================================
# Step 3 — Streamlit UI
# ============================================================
st.set_page_config(page_title="4TU Monitoring (Workshop Build)", layout="wide")
st.title("4TU Monitoring Dashboard — built live")
st.caption(f"Source: {BASE_URL}")

with st.sidebar:
    st.header("Query")

    item_type_label = st.selectbox("Item type", ["Dataset (3)", "Software (9)"], index=0)
    item_type = 3 if item_type_label.startswith("Dataset") else 9

    published_since = st.text_input("published_since (YYYY-MM-DD)", value=DEFAULT_PUBLISHED_SINCE)
    page_size = st.number_input("page_size", min_value=10, max_value=1000, value=DEFAULT_PAGE_SIZE, step=10)
    max_pages = st.number_input("max_pages", min_value=1, max_value=50, value=DEFAULT_MAX_PAGES, step=1)

    st.divider()
    st.header("Performance")
    use_cache = st.checkbox("Use Streamlit cache", value=True)
    refresh = st.button("Refresh now")


@st.cache_data(show_spinner=True)
def load_data_cached(item_type: int, published_since: str, page_size: int, max_pages: int) -> pd.DataFrame:
    groups = get_groups()
    group_map = build_group_map(groups)
    articles = get_recent_articles(
        item_type=item_type,
        published_since=published_since,
        page_size=page_size,
        max_pages=max_pages,
    )
    return to_dataframe(articles, group_map)


if refresh:
    load_data_cached.clear()

if use_cache:
    df = load_data_cached(item_type, published_since, int(page_size), int(max_pages))
else:
    groups = get_groups()
    group_map = build_group_map(groups)
    articles = get_recent_articles(
        item_type=item_type,
        published_since=published_since,
        page_size=int(page_size),
        max_pages=int(max_pages),
    )
    df = to_dataframe(articles, group_map)

if df.empty:
    st.warning("No results. Try earlier published_since or increase max_pages.")
    st.stop()


# ============================================================
# Step 4 — Filters
# ============================================================
with st.sidebar:
    st.header("Filters")
    group_options = sorted(df["group_name"].dropna().unique().tolist())
    group_choice = st.selectbox("Group", ["All"] + group_options)
    keyword = st.text_input("Keyword in title", value="").strip()

filtered = df.copy()
if group_choice != "All":
    filtered = filtered[filtered["group_name"] == group_choice]
if keyword:
    filtered = filtered[filtered["title"].fillna("").str.contains(keyword, case=False, na=False)]


# ============================================================
# Step 5 — Output
# ============================================================
col1, col2 = st.columns([1, 3])
with col1:
    st.metric("Results", len(filtered))
    st.download_button(
        "Download CSV",
        data=filtered.to_csv(index=False),
        file_name=f"4tu_monitoring_{item_type}.csv",
        mime="text/csv",
    )

with col2:
    st.dataframe(filtered, use_container_width=True, hide_index=True)

with st.expander("Diagnostics"):
    st.write("Rows loaded:", len(df))
    st.write("Columns:", list(df.columns))
```



## How to run (for your workshop slide / instructions)

* install environment : `bash scripts/setup_env.sh`
* Activate env: `source .venv/bin/activate`
* Start app: `streamlit run lesson_code.py`

