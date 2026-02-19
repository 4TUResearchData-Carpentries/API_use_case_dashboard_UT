import streamlit as st
import requests
from datetime import datetime, date

BASE_URL = "https://data.4tu.nl"

st.set_page_config(page_title="Dataset Monitoring Dashboard", layout="wide")
st.title("Dataset Monitoring Dashboard")
st.sidebar.header("Filters")

# -----------------------------
# 1) Date range widget (IMPORTANT: give a sensible default)
# -----------------------------
st.sidebar.subheader("Date Range")
default_start = date(2025, 1, 1)
default_end = date.today()
start_date, end_date = st.sidebar.date_input(
    "Publication date range",
    value=(default_start, default_end),
)

# Convert to strings for display / comparisons
start_date_str = start_date.isoformat()
end_date_str = end_date.isoformat()

# -----------------------------
# 2) Fetch groups and build maps
# -----------------------------
groups_resp = requests.get(f"{BASE_URL}/v3/groups", timeout=30)
groups_resp.raise_for_status()
groups = groups_resp.json()  # list[dict]

# Build both mappings for easy use
group_id_to_name = {g["id"]: g["name"] for g in groups if "id" in g and "name" in g}
group_name_to_id = {g["name"]: g["id"] for g in groups if "id" in g and "name" in g}

# Sidebar affiliation selectbox (dynamic)
st.sidebar.subheader("Affiliation")
affiliation_name = st.sidebar.selectbox(
    "Select Affiliation",
    ["All"] + sorted(group_name_to_id.keys())
)

selected_group_id = None if affiliation_name == "All" else group_name_to_id.get(affiliation_name)

# -----------------------------
# 3) Fetch articles (keep it simple: use published_since + limit)
#    Note: /v2/articles supports published_since, limit, offset, item_type, etc. :contentReference[oaicite:1]{index=1}
# -----------------------------
params = {
    "published_since": start_date_str,  # server-side filter for the start
    "limit": 100,
    "offset": 0,
    # "item_type": 3,  # optionally: dataset only
}
articles_resp = requests.get(f"{BASE_URL}/v2/articles", params=params, timeout=30)
articles_resp.raise_for_status()
articles = articles_resp.json()  # list[dict]

# -----------------------------
# 4) Local filtering for end_date + affiliation
# -----------------------------
def parse_pub_date(a: dict) -> date | None:
    # published_date often looks like "2024-07-26 T10:39:57" (space before time). :contentReference[oaicite:2]{index=2}
    s = a.get("published_date")
    if not s:
        return None
    # Take first 10 chars => YYYY-MM-DD
    try:
        return datetime.fromisoformat(s[:10]).date()
    except ValueError:
        return None

filtered = []
for a in articles:
    pub_d = parse_pub_date(a)
    if pub_d is None:
        continue

    # End-date filter (since the API gives us "since", we do "until" locally)
    if pub_d > end_date:
        continue

    # Affiliation filter (articles have group_id)
    if selected_group_id is not None and a.get("group_id") != selected_group_id:
        continue

    filtered.append(a)

# -----------------------------
# 5) Display
# -----------------------------
st.subheader("Results")
st.write(f"Retrieved from API: {len(articles)} (first page)")
st.write(f"After filters: {len(filtered)}")

for a in filtered[:20]:
    gid = a.get("group_id")
    gname = group_id_to_name.get(gid, "Unknown")
    st.markdown(f"**{a.get('title', '(no title)')}**")
    st.caption(f"Published: {a.get('published_date')} • Affiliation: {gname}")
    st.divider()
