#!/usr/bin/env bash
# Start Streamlit Diagnostic Dashboard (Port 8501)
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_STREAMLIT="$DIR/../.venv/bin/streamlit"

if [ ! -f "$VENV_STREAMLIT" ]; then
  VENV_STREAMLIT="streamlit"
fi

echo "================================================================="
echo " Starting Streamlit Diagnostic Dashboard (Port 8501)..."
echo "================================================================="

cd "$DIR/backend"
"$VENV_STREAMLIT" run dashboard/app.py --server.port 8501
