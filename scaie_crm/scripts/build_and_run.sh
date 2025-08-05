#!/bin/bash

# Script to build and run the improved SCAIE application

set -e  # Exit immediately if a command exits with a non-zero status

echo "========================================="
echo "  SCAIE - Sistema Agente Conversacional  "
echo "========================================="
echo "Building and running the improved version"
echo ""

# Directory setup
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$BASE_DIR"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r backend/requirements.txt
else
    echo "✅ Virtual environment already exists"
    source venv/bin/activate
fi

# Install/upgrade frontend dependencies
echo "🔧 Installing/upgrading frontend dependencies..."
cd frontend
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
else
    echo "Frontend dependencies already installed"
fi

# Build frontend
echo "🔧 Building frontend..."
npm run build

echo "✅ Frontend built successfully"

# Go back to backend directory
cd ../backend

# Check if database exists
if [ ! -f "scaie.db" ]; then
    echo "✅ Database will be created automatically when the application starts"
fi

# Kill any existing processes on port 8001
echo "🔍 Checking for processes on port 8001..."
if lsof -i :8001 > /dev/null 2>&1; then
    echo "⚠️  Process found on port 8001. Terminating..."
    lsof -t -i :8001 | xargs kill -9
    echo "✅ Process terminated"
fi

echo ""
echo "========================================="
echo "  Starting the improved SCAIE server     "
echo "========================================="
echo "Port: 8001"
echo "API: http://localhost:8001/api"
echo "Docs: http://localhost:8001/docs"
echo "Frontend: http://localhost:8001/"
echo ""
echo "To stop the server: Ctrl+C"
echo ""

# Start the server
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload