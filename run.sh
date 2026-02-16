#!/usr/bin/env bash
set -euo pipefail

# shellcheck disable=SC1091
if [ -f ".env" ]; then
  set -a
  source .env
  set +a
fi

streamlit run use_cases/uc01_dashboard_monitoring/app/streamlit_app.py
