#!/usr/bin/env bash
# Isolated landing server — no PROJECT deps, stdlib only
# Usage: ./serve.sh  (serves landing/ on :8081)
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
PORT="${1:-8081}"
echo "Serving landing/ from $DIR on http://localhost:$PORT (Ctrl+C to stop)"
python3 -m http.server "$PORT" --directory "$DIR"
