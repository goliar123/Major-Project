#!/usr/bin/env bash
# Start Automated Failure Attribution Engine Backend (FastAPI / Uvicorn)
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PYTHON="$DIR/../.venv/bin/python"

if [ ! -f "$VENV_PYTHON" ]; then
  VENV_PYTHON="python3"
fi

echo "================================================================="
echo " Starting Failure Attribution Backend (Port 8000)..."
echo "================================================================="

cd "$DIR/backend"
"$VENV_PYTHON" -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
