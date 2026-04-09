#!/bin/sh
set -e

# Start FastAPI backend
uvicorn backend.main:app --host 0.0.0.0 --port 8000 &

# Start Next.js frontend
cd frontend && node server.js &

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?
