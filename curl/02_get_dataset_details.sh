#!/usr/bin/env bash
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: bash 02_get_dataset_details.sh <ARTICLE_ID>"
  exit 1
fi

BASE_URL="${FOURTU_BASE_URL:-https://data.4tu.nl}"
ARTICLE_ID="$1"

curl -s "${BASE_URL}/v2/articles/${ARTICLE_ID}" | jq .
