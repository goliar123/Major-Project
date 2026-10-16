#!/usr/bin/env python3
"""
Root entry point for the Dedicated Command-Line App (`agent-trace`).
Automated Failure Attribution for LLM-Based Multi-Agent Systems.

Usage:
    ./agent_trace.py diagnose PROJECT/backend/tests/sample_trace.json
    ./agent_trace.py benchmark --limit 20
    ./agent_trace.py cache stats
    ./agent_trace.py watch --log-file execution.log --goal "Complete Task"
    ./agent_trace.py serve dashboard
"""
import sys
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parent
backend_dir = root / "PROJECT" / "backend"
cli_main = backend_dir / "cli" / "main.py"
venv_python = root / ".venv" / "bin" / "python"

python_bin = str(venv_python) if venv_python.exists() else sys.executable

env = dict(PYTHONPATH=str(backend_dir))
import os
full_env = {**os.environ, **env}

res = subprocess.run([python_bin, str(cli_main)] + sys.argv[1:], env=full_env)
sys.exit(res.returncode)
