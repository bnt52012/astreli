#!/bin/bash
# AdGenAI — Local Development Runner
set -e

echo "========================================="
echo "  AdGenAI Pipeline — Local Dev"
echo "========================================="

# Check .env
if [ ! -f .env ]; then
  echo "⚠ No .env file found. Copy .env.example to .env and fill in your API keys."
  exit 1
fi

# Backend
echo ""
echo "[1/2] Starting FastAPI backend on :8000..."
cd "$(dirname "$0")"
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Frontend
echo "[2/2] Starting Next.js frontend on :3000..."
cd frontend
npm run dev &
FRONTEND_PID=$!

echo ""
echo "✓ Backend:  http://localhost:8000"
echo "✓ Frontend: http://localhost:3000"
echo "✓ API docs: http://localhost:8000/docs"
echo ""

# Trap exit to kill both processes
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM
wait
