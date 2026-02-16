#!/usr/bin/env bash
set -euo pipefail

bash scripts/setup_env.sh
cp .env.example .env
sed -i 's/\r$//' .env


# shellcheck disable=SC1091
if [ -f ".env" ]; then
  set -a
  source .env
  set +a
fi

streamlit run app/streamlit_app.py
