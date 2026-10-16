#!/usr/bin/env bash
# Start Both Backend (FastAPI :8000) and Frontend (Vite :5173) Concurrently
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

trap 'echo "Stopping all services..."; kill $(jobs -p) 2>/dev/null || true' EXIT

echo "================================================================="
echo " Launching Automated Failure Attribution Platform (Batch B12)"
echo "================================================================="

# Start Backend
"$DIR/start_backend.sh" &
BACKEND_PID=$!
echo "Backend running on PID $BACKEND_PID (http://localhost:8000)"

# Wait for backend to initialize
sleep 2

# Start Frontend
"$DIR/start_frontend.sh" &
FRONTEND_PID=$!
echo "Frontend running on PID $FRONTEND_PID (http://localhost:5173)"

echo "-----------------------------------------------------------------"
echo " Platform Active:"
echo " • Web Frontend: http://localhost:5173"
echo " • API Docs:     http://localhost:8000/docs"
echo " • Health Check: http://localhost:8000/api/v1/health"
echo " Press Ctrl+C to terminate both servers."
echo "-----------------------------------------------------------------"

wait
