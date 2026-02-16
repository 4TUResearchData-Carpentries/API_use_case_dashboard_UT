# Lesson Plan (1 Full Day)

## Audience: Data stewards & support staff
## Goal: Build a working monitoring dashboard.

## Shedule: 

Morning Session 

-  09:00 – 09:30 : Understanding the API (3 hours)


    Context

    What is monitoring?

    Why use the API instead of manual browsing?

    Public vs authenticated endpoints

-  09:30 – 10:30 : Hands-on with curl

    Hands-on with curl

    

    - Practice GET endpoint /v2/articles

    - Filter by `published_since` , `item_type` and `limit`

    - Call /v3/groups

    - Inspect dataset metadata structure "/v2/articles/{uuid}"

- 10:30 – 10:45: Break

- 10:45 – 12:00: Python API Client

    We implement a simple Python client to wrap the API calls.

    - requests wrapper

    - parameter handling

    JSON inspection

    - convert to pandas

    By lunch they must have: A DataFrame printed in terminal. That is the first Minimal Viable Product (MVP) milestone.

- 12:00 – 13:00: Lunch

- 13:00 – 13:45  Building the Dashboard (3 hours)


    - Minimal Streamlit intro

    - st.title

    - st.sidebar

    - st.dataframe

    - st.download_button

13:45 – 14:45: Build filtering logic

    - Group selectbox

    - Date filter

    - Keyword filter

Second MVP milestone: Filtering works.

14:45 – 15:00 : Break

15:00 – 16:00 : Stabilization


    - Error handling

    - Optional caching

    - Performance discussion

    - What not to do (full harvesting)

16:00 – 16:30 : Discussion & Wrap-up

Topics:

Scaling monitoring workflows


## At the end of the day:

Participants must have:

- A working Streamlit dashboard

- Pulling real production data

- Filtering by affiliation and date

- Exporting CSV

