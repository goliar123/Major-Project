"""
Main Entrypoint for the Automated Failure Attribution Engine Backend.
Runs FastAPI with Uvicorn server on http://0.0.0.0:8000
"""
import sys
from pathlib import Path

# Ensure backend root is on sys.path
BACKEND_ROOT = Path(__file__).resolve().parent
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

import uvicorn
from api.main import app

if __name__ == "__main__":
    print(f"Starting Failure Attribution Backend from {BACKEND_ROOT} on port 8000...")
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
