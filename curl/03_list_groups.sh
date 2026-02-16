#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${FOURTU_BASE_URL:-https://data.4tu.nl}"

curl -s "${BASE_URL}/v3/groups" | jq .

