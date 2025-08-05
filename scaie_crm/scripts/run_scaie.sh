#!/bin/bash

# Script to initialize, build and run the SCAIE application

set -e  # Exit immediately if a command exits with a non-zero status

echo "========================================="
echo "  SCAIE - Sistema Agente Conversacional  "
echo "========================================="
echo "Initializing, building and running the application"
echo ""

# Directory setup
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$BASE_DIR"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "Please create a .env file with the following variables:"
    echo "DASHSCOPE_API_KEY=your_api_key_here"
    echo "TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here"
    echo "DATABASE_URL=sqlite:///./backend/scaie.db"
    echo ""
    echo "Example .env file content:"
    echo "DASHSCOPE_API_KEY=sk-ff40b02e0b454d379ea51160cfbadfa9"
    echo "TELEGRAM_BOT_TOKEN=1234567890:ABCdefGhIJKlmNoPQRsTUVwxyZ"
    echo "DATABASE_URL=sqlite:///./backend/scaie.db"
    echo ""
    exit 1
fi

# Load environment variables
source .env

# Check if required environment variables are set
if [ -z "$DASHSCOPE_API_KEY" ]; then
    echo "❌ DASHSCOPE_API_KEY is not set in .env file"
    exit 1
fi

echo "✅ Environment variables loaded"

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
    
    # Check if requirements need to be updated
    echo "🔍 Checking for updated requirements..."
    pip install -r backend/requirements.txt > /dev/null 2>&1
fi

# Install/upgrade frontend dependencies
echo "🔧 Installing/upgrading frontend dependencies..."
cd frontend
if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
else
    echo "📦 Updating frontend dependencies..."
    npm install
fi

# Build frontend
echo "🔧 Building frontend..."
npm run build

echo "✅ Frontend built successfully"

# Go back to base directory
cd ..

# Check if database exists and initialize if needed
echo "🔍 Checking database..."
cd backend

if [ ! -f "scaie.db" ]; then
    echo "🆕 Creating and initializing database..."
    python3 init_db.py
    echo "✅ Database created and initialized"
else
    # Check if all tables exist
    echo "🔍 Checking database tables..."
    TABLES=$(sqlite3 scaie.db ".tables" 2>/dev/null || echo "")
    if [ -z "$TABLES" ]; then
        echo "🔧 Initializing database tables..."
        python3 init_db.py
        echo "✅ Database tables initialized"
    else
        echo "✅ Database and tables already exist"
    fi
fi

# Kill any existing processes on port 8001
echo "🔍 Checking for processes on port 8001..."
if lsof -i :8001 > /dev/null 2>&1; then
    echo "⚠️  Process found on port 8001. Terminating..."
    lsof -t -i :8001 | xargs kill -9
    echo "✅ Process terminated"
else
    echo "✅ No processes found on port 8001"
fi

echo ""
echo "========================================="
echo "  Starting SCAIE server                  "
echo "========================================="
echo "Port: 8001"
echo "API: http://localhost:8001/api"
echo "Docs: http://localhost:8001/docs"
echo "Frontend: http://localhost:8001/"
echo ""
echo "To stop the server: Ctrl+C"
echo ""

# Copy frontend build to static directory
echo "📦 Copying frontend build to static directory..."
cp -r ../frontend/dist/* ./static/ 2>/dev/null || echo "✅ Static files already up to date"

# Start the server in background
echo "🚀 Starting SCAIE server..."
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload &
SERVER_PID=$!

# Wait a moment for server to start
sleep 5

# Start Telegram bot if token is provided
if [ -n "$TELEGRAM_BOT_TOKEN" ]; then
    echo "🤖 Starting Telegram bot..."
    # Start Telegram bot in background
    python3 ../start_telegram_bot.py &
    TELEGRAM_PID=$!
    echo "✅ Telegram bot started with PID $TELEGRAM_PID"
else
    echo "ℹ️  Telegram bot token not provided, skipping Telegram bot start"
fi

# Show server status
echo ""
echo "========================================="
echo "  SCAIE is now running                   "
echo "========================================="
echo "🌐 Web interface: http://localhost:8001/"
echo "📚 API documentation: http://localhost:8001/docs"
if [ -n "$TELEGRAM_BOT_TOKEN" ]; then
    echo "🤖 Telegram bot: @scAIebot (or your custom bot name)"
fi
echo ""
echo "To stop the server, press Ctrl+C"
echo ""

# Function to clean up processes on exit
cleanup() {
    echo ""
    echo "🛑 Stopping SCAIE server..."
    if [ -n "$SERVER_PID" ]; then
        kill $SERVER_PID 2>/dev/null || true
    fi
    
    if [ -n "$TELEGRAM_PID" ]; then
        echo "🛑 Stopping Telegram bot..."
        kill $TELEGRAM_PID 2>/dev/null || true
    fi
    
    echo "👋 SCAIE stopped."
    exit 0
}

# Trap exit signals to clean up
trap cleanup EXIT INT TERM

# Wait for both processes
if [ -n "$SERVER_PID" ] && [ -n "$TELEGRAM_PID" ]; then
    echo "⏳ Waiting for both processes to complete..."
    wait $SERVER_PID $TELEGRAM_PID
elif [ -n "$SERVER_PID" ]; then
    echo "⏳ Waiting for server process to complete..."
    wait $SERVER_PID
fi