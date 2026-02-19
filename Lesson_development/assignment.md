# UC01 — Dashboard for Monitoring Published 4TU Datasets

## Goal

Build a minimal dashboard that monitors published datasets in 4TU.ResearchData
and allows filtering by affiliation (group) and publication date.

The dashboard must:

- Retrieve published datasets from the production API
- Map datasets to affiliations (groups)
- Provide filtering options
- Display results in a simple dashboard
- Allow exporting filtered results as CSV

Production base URL:
https://data.4tu.nl

---

## Learning Objectives

After this assignment you can:

- Use curl to interact with the 4TU API
- Authenticate (optionally) using an API token
- Retrieve published datasets via `/v2/articles`
- Retrieve group metadata via `/v3/groups`
- Extract affiliation information from dataset metadata
- Build a minimal monitoring dashboard using Streamlit

---

## Technical Stack

- curl
- Python 3.10+
- requests
- pandas
- streamlit

---

## Part 1 — Explore the API with curl

### Step 1 — List recent published datasets

Retrieve published datasets from 2025 onwards.

Endpoint:
GET /v2/articles

Required parameters:
- item_type=3   (dataset)
- published_since=2025-01-01
- limit=50
- offset=0

Save the JSON response.

Questions:
- How many results are returned?
- Which fields identify publication date?
- Is group_id present?

---

### Step 2 — Retrieve group information

Call:
GET /v3/groups

Questions:
- What is the structure of a group object?
- How can you map group_id → group name?

---

### Step 3 — Inspect one dataset in detail

Call:
GET /v2/articles/{id}

Questions:
- Where are affiliations stored?
- Is there a custom_fields section?
- Does it contain “organizations” or similar?

---

## Part 2 — Implement the Monitoring Logic in Python

Create a Python module that:

1. Fetches published datasets (paged)
2. Maps group_id to group name
3. Extracts:
   - id
   - title
   - published_date
   - group_name
   - DOI
4. Returns a pandas DataFrame

---

## Part 3 — Build the Dashboard (Streamlit)

Your dashboard must provide:

Sidebar filters:
- Group (affiliation)
- Publication date range
- Keyword search (title)

Main view:
- Table of filtered datasets
- Count of results
- CSV download button

---

## Deliverable

You should be able to run:

streamlit run streamlit_app.py

And obtain a working monitoring dashboard for published datasets.

---

## Extension (Optional)

- Add caching
- Add download statistics if available
- Add automatic refresh
