#!/usr/bin/env bash
# Start React/Vite Frontend Web Client (Port 5173)
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "================================================================="
echo " Starting Failure Attribution Frontend (Vite / React)..."
echo "================================================================="

cd "$DIR/frontend"
npm run dev -- --host
