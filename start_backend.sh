#!/bin/bash
# Quick start script for backend

cd "$(dirname "$0")/backend"

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Starting backend server..."
uvicorn main:app --reload --host 0.0.0.0 --port 8000

