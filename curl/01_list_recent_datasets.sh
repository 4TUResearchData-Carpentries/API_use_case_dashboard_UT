#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${FOURTU_BASE_URL:-https://data.4tu.nl}"
PUBLISHED_SINCE="${PUBLISHED_SINCE:-2025-01-01}"
LIMIT="${LIMIT:-50}"
OFFSET="${OFFSET:-0}"
ITEM_TYPE="${ITEM_TYPE:-3}"

# item_type=3 is "dataset" in your workshop notes
curl -s "${BASE_URL}/v2/articles?item_type=${ITEM_TYPE}&limit=${LIMIT}&offset=${OFFSET}&published_since=${PUBLISHED_SINCE}" | jq .
