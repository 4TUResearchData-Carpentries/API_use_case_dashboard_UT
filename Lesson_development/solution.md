# UC01 — Solution

## Architecture (MVP)

We implement a simple 3-layer structure:

1. API Layer (requests)
2. Transformation Layer (pandas)
3. Presentation Layer (Streamlit)

---

## Step 1 — API Client

```python
import os
import requests

BASE_URL = os.getenv("FOURTU_BASE_URL", "https://data.4tu.nl")
TOKEN = os.getenv("FOURTU_TOKEN")

def get_headers():
    headers = {"Accept": "application/json"}
    if TOKEN:
        headers["Authorization"] = f"token {TOKEN}"
    return headers

def get_recent_datasets(published_since="2025-01-01", limit=100):
    url = f"{BASE_URL}/v2/articles"
    params = {
        "item_type": 3,
        "published_since": published_since,
        "limit": limit,
        "offset": 0,
    }
    r = requests.get(url, headers=get_headers(), params=params)
    r.raise_for_status()
    return r.json()

def get_groups():
    url = f"{BASE_URL}/v3/groups"
    r = requests.get(url, headers=get_headers())
    r.raise_for_status()
    return r.json()
```
---

## Step 2 — Transform to DataFrame

```python
import pandas as pd

def build_dataframe():
    datasets = get_recent_datasets()
    groups = get_groups()

    group_map = {g["id"]: g["name"] for g in groups}

    rows = []
    for ds in datasets:
        rows.append({
            "id": ds["id"],
            "title": ds["title"],
            "published_date": ds["published_date"],
            "group": group_map.get(ds.get("group_id"), "Unknown"),
            "doi": ds.get("doi")
        })

    return pd.DataFrame(rows)
```
---

## Step 3 — Streamlit Dashboard

```python
import streamlit as st

st.title("4TU Dataset Monitoring Dashboard")

df = build_dataframe()

groups = sorted(df["group"].dropna().unique())
selected_group = st.sidebar.selectbox("Affiliation", ["All"] + groups)

date_min = pd.to_datetime(df["published_date"]).min()
date_max = pd.to_datetime(df["published_date"]).max()
date_range = st.sidebar.date_input("Publication range", [date_min, date_max])

keyword = st.sidebar.text_input("Keyword")

filtered = df.copy()

if selected_group != "All":
    filtered = filtered[filtered["group"] == selected_group]

filtered["published_date"] = pd.to_datetime(filtered["published_date"])
filtered = filtered[
    (filtered["published_date"] >= pd.to_datetime(date_range[0])) &
    (filtered["published_date"] <= pd.to_datetime(date_range[1]))
]

if keyword:
    filtered = filtered[filtered["title"].str.contains(keyword, case=False)]

st.write(f"Results: {len(filtered)}")
st.dataframe(filtered)

st.download_button(
    "Download CSV",
    filtered.to_csv(index=False),
    file_name="filtered_datasets.csv"
)
```
---

## MVP Characteristics

- Single page
- No background jobs
- No full repository harvesting
- Limited to a recent time window
- Optional authentication
