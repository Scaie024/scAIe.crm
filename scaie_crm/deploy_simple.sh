#!/bin/bash

# Simple deployment script for SCAIE - Sistema Agente Conversacional Inteligente Empresarial
# This script handles all the necessary steps to run the application

set -e  # Exit immediately if a command exits with a non-zero status

echo "=============================================="
echo "  SCAIE - Sistema Agente Conversacional       "
echo "  Script de Despliegue Simplificado           "
echo "=============================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    print_error "This script must be run from the root of the SCAIE project directory"
    print_error "Please navigate to the scaie_crm directory and try again"
    exit 1
fi

print_status "Starting SCAIE deployment process..."

# Step 1: Check for Python 3
print_status "Checking for Python 3..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi
print_success "Python 3 is installed"

# Step 2: Check for pip
print_status "Checking for pip..."
if ! command -v pip3 &> /dev/null; then
    print_warning "pip3 not found, trying to install..."
    python3 -m ensurepip --upgrade
fi
print_success "pip is available"

# Step 3: Setup virtual environment
print_status "Setting up virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_status "Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate
print_success "Virtual environment activated"

# Step 4: Install backend dependencies
print_status "Installing backend dependencies..."
pip install --upgrade pip
pip install fastapi uvicorn sqlalchemy python-dotenv openai pydantic

# Install any additional requirements if requirements.txt exists
if [ -f "backend/requirements.txt" ]; then
    pip install -r backend/requirements.txt
else
    print_warning "backend/requirements.txt not found, continuing with basic dependencies"
fi
print_success "Backend dependencies installed"

# Step 5: Install frontend dependencies
print_status "Installing frontend dependencies..."
cd frontend
if [ ! -d "node_modules" ]; then
    if command -v npm &> /dev/null; then
        npm install
        print_success "Frontend dependencies installed"
    else
        print_warning "npm not found, skipping frontend dependency installation"
    fi
else
    print_status "Frontend dependencies already installed"
fi

# Step 6: Build frontend
print_status "Building frontend..."
if command -v npm &> /dev/null; then
    npm run build
    print_success "Frontend built successfully"
else
    print_warning "npm not found, skipping frontend build"
fi

# Go back to root directory
cd ..

# Step 7: Copy frontend build to static directory
print_status "Copying frontend build to static directory..."
if [ -d "frontend/dist" ]; then
    mkdir -p backend/static
    cp -r frontend/dist/* backend/static/
    print_success "Frontend files copied to static directory"
else
    print_warning "Frontend build directory not found, skipping copy"
fi

# Step 8: Check database
print_status "Checking database..."
cd backend
if [ ! -f "scaie.db" ]; then
    print_status "Database not found, initializing..."
    if [ -f "src/scaie/init_db.py" ]; then
        python src/scaie/init_db.py
        print_success "Database initialized"
    else
        print_warning "Database initialization script not found"
    fi
else
    print_status "Database already exists"
fi

# Step 9: Check .env file
print_status "Checking environment configuration..."
if [ ! -f ".env" ]; then
    print_warning ".env file not found, creating from example..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        print_success ".env file created from example"
        print_warning "Please update the .env file with your actual API keys and configuration"
    else
        print_warning ".env.example not found, creating minimal .env file"
        cat > .env << EOF
# Database Configuration
DATABASE_URL=sqlite:///./scaie.db

# Qwen API Configuration (required for AI features)
DASHSCOPE_API_KEY=your_dashscope_api_key_here

# Agent Configuration
AGENT_NAME=SCAI
AGENT_PERSONALITY="amigable, profesional, directo, conversacional, natural"
AGENT_TONE="profesional y directo"
AGENT_GOAL="ayudar a las empresas a ser más eficientes con inteligencia artificial y automatización de procesos"

# LLM Parameters
TEMPERATURE=0.8
MAX_TOKENS=1024
TOP_P=0.9
TOP_K=30

# Skip authentication for testing
SKIP_AUTH=true
EOF
        print_warning "Please update the .env file with your actual DashScope API key"
    fi
else
    print_success ".env file found"
fi

# Step 10: Kill any existing processes on port 8003
print_status "Checking for processes on port 8003..."
if lsof -i :8003 > /dev/null 2>&1; then
    print_warning "Process found on port 8003. Terminating..."
    lsof -t -i :8003 | xargs kill -9
    print_success "Process terminated"
else
    print_success "No processes found on port 8003"
fi

# Go back to the directory with main.py
cd src/scaie

# Final instructions
echo ""
echo "=============================================="
echo "  SCAIE is ready to run!                      "
echo "=============================================="
echo ""
print_success "To start the application, run:"
echo "    cd /Users/arturopinzon/Desktop/scAIe\ -\ Sistema\ Agente/scaie_crm/backend/src/scaie"
echo "    python3 -m app.main"
echo ""
print_success "The application will be available at:"
echo "    Web Interface: http://localhost:8003"
echo "    API Documentation: http://localhost:8003/docs"
echo "    Health Check: http://localhost:8003/health"
echo ""
print_warning "Before running, make sure to:"
echo "    1. Update the .env file with your DashScope API key"
echo "    2. Check that port 8003 is available"
echo ""
print_status "Press any key to start the application now, or Ctrl+C to exit..."
read -n 1 -s

# Start the application
print_success "Starting SCAIE application..."
python3 -m app.main