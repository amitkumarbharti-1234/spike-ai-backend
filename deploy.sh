#!/bin/bash

set -e

echo "========================================"
echo " Spike AI Backend Deployment Starting "
echo "========================================"

# Check Python
if ! command -v python &> /dev/null; then
  echo "Python not found"
  exit 1
fi

echo "Python found"

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Start FastAPI server
echo "Starting FastAPI server on port 8080..."
nohup uvicorn app.main:app --host 0.0.0.0 --port 8080 > server.log 2>&1 &

# Wait for server startup
sleep 3

# Health check
if lsof -i:8080 > /dev/null; then
  echo "Server started successfully on port 8080"
else
  echo "Server failed to start"
  exit 1
fi

echo "========================================"
echo " Deployment Completed Successfully "
echo "========================================"
