#!/usr/bin/env python3
"""
Top-level entry point to verify all numbers from Review-3 presentation slides 10 & 11.
"""
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parent
venv_python = root / ".venv" / "bin" / "python"
script = root / "PROJECT" / "verify_all_numbers.py"

python_bin = str(venv_python) if venv_python.exists() else sys.executable
res = subprocess.run([python_bin, str(script)])
sys.exit(res.returncode)
