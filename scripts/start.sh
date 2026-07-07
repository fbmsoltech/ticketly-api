#!/usr/bin/env bash
set -e

alembic upgrade head

python scripts/seed_initial_data.py

uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"
