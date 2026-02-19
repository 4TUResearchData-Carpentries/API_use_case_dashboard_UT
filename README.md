# Dasboard monitoring datasets in 4TU.ResearchData

Welcome to the workshop **Building a minimal dashboard to monitor datasets using 4TU.ResearchData API**! for data support staff from University of Twente, on March 10th, 2026.  



## 🚀 Workshop Overview

### What we will build

By the end of the workshop, you will be able to:

- Apply the API data flow: request → JSON → DataFrame → Streamlit UI

- Retrieve results from an API in multiple batches by using the limit (how many records per request) and offset (where to start in the result list) parameters

- Use .env configuration (BASE_URL, TOKEN, TIMEOUT)

- Add filters and CSV download functionality

- Optionally implement caching and diagnostics

We will live-code everything in a single script.



## 🛠 Workshop Setup

Before the workshop, please:

### Step 1 — Clone the repository

```bash
git clone git@github.com:4TUResearchData-Carpentries/API_use_case_dashboard_UT.git
cd API_use_case_dashboard_UT
```
### Step 2 — Create and activate virtual environment

Mac/Linux:

```bash

python -m venv .venv
source .venv/bin/activate

```

Windows (PowerShell):

```bash

python -m venv .venv
.venv\Scripts\activate

```



### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Create .env file

Create a `.env` file in the project root with the following content:

```

# Production public base URL
FOURTU_BASE_URL=https://data.4tu.nl

# Request tuning
FOURTU_TIMEOUT=30

# Dashboard defaults
UC01_PUBLISHED_SINCE=2025-01-01
UC01_PAGE_SIZE=100
UC01_MAX_PAGES=3

# Optional: only needed if you encounter import errors when running from the repo root 
PYTHONPATH=.

# Optional : If you already have a 4TU API token, you may add:

FOURTU_TOKEN=your_token_here

```

- Production base URL: https://data.4tu.nl
- Authentication is optional for public monitoring.




## 🛠 Prerequisites

Before attending the workshop, please ensure you have:

### Required Knowledge

This is not a beginner Python workshop. You should be comfortable with:

- Basic Python syntax (functions, dictionaries, loops)

- Running Python from the command line

- Installing packages with pip

- Basic familiarity with pandas

- Basic understanding of HTTP concepts (GET requests, JSON)

If you have never used requests or streamlit before, that is fine, we will cover those from scratch.


### Required Software

Please ensure the following are installed:

✅ Python : Python 3.10 or newer

Verify with: `python --version` 


✅ Git 

Verify with: `git --version`

✅ Code Editor

Recommended:

- VS Code

-Any editor where you can run a terminal

## 📖 Workshop Materials

- Laptop with charger

- Admin rights to install packages (if needed)

- Stable internet connection

## 🔗 Resources

- 4TU.ResearchData API documentation: https://djehuty.4tu.nl/

## 💡 License
This workshop material is licensed under **GNU AFFERO GENERAL PUBLIC LICENSE Version 3**. Feel free to share and modify the lesson according your needs.

## 🙌 Acknowledgments


---


Happy coding! 🎉
