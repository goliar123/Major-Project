#!/usr/bin/env bash
# Run Pytest Test Suite
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PYTEST="$DIR/../.venv/bin/pytest"

if [ ! -f "$VENV_PYTEST" ]; then
  VENV_PYTEST="pytest"
fi

echo "================================================================="
echo " Running Automated Failure Attribution Test Suite..."
echo "================================================================="

cd "$DIR/backend"
"$VENV_PYTEST" -v
