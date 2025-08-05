#!/bin/bash

# Script to completely initialize the SCAIE project

set -e  # Exit immediately if a command exits with a non-zero status

echo "========================================="
echo "  SCAIE - Project Initialization Script  "
echo "========================================="
echo "Initializing the complete SCAIE project"
echo ""

# Directory setup
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$BASE_DIR"

echo "🔧 Setting up project structure..."

# Create necessary directories
mkdir -p backend/static
mkdir -p logs

echo "✅ Project structure created"

# Check if .env file exists, create from example if not
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from example..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
    else
        cat > .env << EOF
# SCAIE Environment Configuration

# Qwen API Key (required)
DASHSCOPE_API_KEY=your_dashscope_api_key_here

# Database Configuration
DATABASE_URL=sqlite:///./backend/scaie.db

# Server Configuration
HOST=0.0.0.0
PORT=8001

# Logging Configuration
LOG_LEVEL=INFO
EOF
    fi
    echo "✅ .env file created"
    echo "⚠️  Please update the DASHSCOPE_API_KEY in the .env file with your actual API key"
else
    echo "✅ .env file already exists"
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
else
    echo "✅ Virtual environment already exists"
    source venv/bin/activate
fi

# Install backend dependencies
echo "📦 Installing backend dependencies..."
pip install -r backend/requirements.txt

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend
npm install

echo "✅ All dependencies installed"

# Go back to base directory
cd ..

# Initialize database
echo "🔧 Initializing database..."
cd backend

if [ ! -f "scaie.db" ]; then
    echo "🆕 Creating and initializing database..."
    python3 init_db.py
    echo "✅ Database created and initialized"
else
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

cd ..

echo ""
echo "========================================="
echo "  SCAIE Project Initialization Complete  "
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Update the DASHSCOPE_API_KEY in the .env file"
echo "2. Run './run_scaie.sh' to start the application"
echo ""
echo "For more information, check the README.md file"