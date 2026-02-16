from __future__ import annotations

import pandas as pd
import streamlit as st

from app.dashboard_queries import build_monitoring_dataframe


st.set_page_config(page_title="4TU Dataset Monitoring", layout="wide")
st.title("4TU Dataset Monitoring Dashboard (UC01)")

with st.sidebar:
    st.header("Filters")
    use_cache = st.checkbox("Use local cache", value=True)

    item_type_label = st.selectbox(
        "Item type",
        options=["Dataset (3)", "Software (9)"],
        index=0,
    )

    item_type = 3 if item_type_label.startswith("Dataset") else 9


@st.cache_data(show_spinner=True)
def load_df_cached(use_cache_flag: bool, item_type: int) -> pd.DataFrame:
    return build_monitoring_dataframe(item_type=item_type, use_cache=use_cache_flag)

df = load_df_cached(use_cache,item_type=item_type)

if df.empty:
    st.warning("No data returned. Try disabling cache or adjusting UC01_* environment variables.")
    st.stop()

# Prepare filter options
group_options = sorted([g for g in df["group_name"].dropna().unique().tolist() if isinstance(g, str)])
group_choice = st.sidebar.selectbox("Affiliation (group)", ["All"] + group_options)

# Date range
date_series = df["published_date"].dropna()
if date_series.empty:
    st.sidebar.info("No published_date values found to filter on.")
    date_start = None
    date_end = None
else:
    min_date = date_series.min().date()
    max_date = date_series.max().date()
    date_start, date_end = st.sidebar.date_input("Publication date range", value=(min_date, max_date))

keyword = st.sidebar.text_input("Keyword in title", value="").strip()

filtered = df.copy()

if group_choice != "All":
    filtered = filtered[filtered["group_name"] == group_choice]

if date_series is not None and not date_series.empty:
    filtered = filtered[
        (filtered["published_date"].dt.date >= date_start) &
        (filtered["published_date"].dt.date <= date_end)
    ]

if keyword:
    filtered = filtered[filtered["title"].fillna("").str.contains(keyword, case=False, na=False)]

# Output
col1, col2 = st.columns([1, 3])
with col1:
    st.metric("Results", int(len(filtered)))
    st.download_button(
        label="Download CSV",
        data=filtered.drop(columns=["group_id"], errors="ignore").to_csv(index=False),
        file_name="uc01_filtered_datasets.csv",
        mime="text/csv",
    )

with col2:
    st.dataframe(
        filtered.drop(columns=["group_id"], errors="ignore"),
        use_container_width=True,
        hide_index=True,
    )
