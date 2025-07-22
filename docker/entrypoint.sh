#!/usr/bin/env bash
set -e

# Wait for Postgres if we're using it
if [[ "$DATABASE_URL" == postgresql* ]]; then
  echo "Waiting for Postgres..."
  # crude wait loop
  for i in {1..30}; do
    python - <<'PY' && break || sleep 1
import os, sys
import sqlalchemy
from sqlalchemy import create_engine
url = os.environ["DATABASE_URL"]
try:
    create_engine(url).connect()
except Exception as e:
    sys.exit(1)
PY
  done
fi

echo "Initializing DB schema (safe if already exists)..."
python -m backend.init_db

if [[ "${SCRAPE_ON_START:-1}" == "1" ]]; then
  echo "Running initial scrape..."
  python -m tasks.fetch_and_store || echo "Scrape failed (continuing)."
fi

echo "Starting Uvicorn..."
exec uvicorn backend.main:app --host 0.0.0.0 --port 8000
