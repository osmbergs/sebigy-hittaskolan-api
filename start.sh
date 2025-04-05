#!/bin/bash

echo "=== Starting backend ==="
echo "Environment: $FASTAPI_ENV"

export PYTHONPATH=$PWD

echo "==== Starting db upgrade ==="
alembic upgrade head
echo "==== Finished db upgrade ==="

echo "==== Starting server... ==="

uvicorn app.main:app --host 0.0.0.0 --port 80

# End of script
