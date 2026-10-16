#!/usr/bin/env bash
# Execute Full ICML 2025 Who&When Benchmark Across All 184 Traces
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PYTHON="$DIR/../.venv/bin/python"

if [ ! -f "$VENV_PYTHON" ]; then
  VENV_PYTHON="python3"
fi

echo "================================================================="
echo " Running Full ICML 2025 Who&When Benchmark Evaluation Suite"
echo " Evaluating 184 Traces (58 Hand-Crafted + 126 Algorithm-Generated)"
echo "================================================================="

cd "$DIR/backend"
"$VENV_PYTHON" run_who_and_when_benchmark.py "$@"
