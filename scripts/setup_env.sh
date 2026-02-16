#!/usr/bin/env bash
set -euo pipefail

rm -rf .venv
python -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate

pip install -r requirements.txt

echo "✅ Environment ready."
echo "Activate with: source .venv/bin/activate"

