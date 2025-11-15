#!/bin/bash
cd backend || exit 1
pip install -r requirements.txt || exit 1
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}

