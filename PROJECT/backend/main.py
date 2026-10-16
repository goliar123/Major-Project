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
    import os

    # Render/Heroku-style platforms inject $PORT; default keeps local behavior.
    port = int(os.environ.get("PORT", "8000"))
    debug = os.environ.get("ENVIRONMENT", "development") == "development"
    print(f"Starting Failure Attribution Backend from {BACKEND_ROOT} on port {port}...")
    uvicorn.run("api.main:app", host="0.0.0.0", port=port, reload=debug)
