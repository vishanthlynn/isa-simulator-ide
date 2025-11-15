#!/bin/bash
# Quick start script for frontend

cd "$(dirname "$0")/frontend"

if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

echo "Starting frontend development server..."
npm start

