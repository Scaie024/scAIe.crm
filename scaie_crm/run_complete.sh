#!/bin/bash

# SCAIE - Sistema Agente Conversacional Inteligente Empresarial
# Complete System Run Script
# This script builds and runs the entire SCAIE system with all components

set -e  # Exit immediately if a command exits with a non-zero status

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

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if a process is running on a port
is_port_in_use() {
    lsof -i :"$1" >/dev/null 2>&1
}

# Function to kill processes on a port
kill_port_processes() {
    if is_port_in_use "$1"; then
        print_warning "Killing processes on port $1..."
        lsof -t -i :"$1" | xargs kill -9 2>/dev/null || true
        sleep 2
    fi
}

# Print banner
echo -e "${GREEN}"
echo "=============================================="
echo "  SCAIE - Sistema Agente Conversacional       "
echo "  Complete System Startup Script              "
echo "=============================================="
echo -e "${NC}"

# Check if we're in the right directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    print_error "This script must be run from the root of the SCAIE project directory"
    print_error "Please navigate to the scaie_crm directory and try again"
    exit 1
fi

# Check system requirements
print_status "Checking system requirements..."

# Check Python
if ! command_exists python3; then
    print_error "Python 3 is required but not found"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
print_success "Python version: $PYTHON_VERSION"

# Check Node.js
if ! command_exists node; then
    print_error "Node.js is required but not found"
    exit 1
fi

NODE_VERSION=$(node --version)
print_success "Node.js version: $NODE_VERSION"

# Check npm
if ! command_exists npm; then
    print_error "npm is required but not found"
    exit 1
fi

print_success "npm found"

# Create virtual environment if it doesn't exist
print_status "Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_success "Virtual environment already exists"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate
print_success "Virtual environment activated"

# Install/upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip >/dev/null 2>&1
print_success "Pip upgraded"

# Install backend dependencies
print_status "Installing backend dependencies..."
cd backend
if [ ! -f "requirements.txt" ]; then
    print_error "requirements.txt not found in backend directory"
    exit 1
fi

pip install -r requirements.txt >/dev/null 2>&1
print_success "Backend dependencies installed"

# Go back to project root
cd ..

# Install frontend dependencies
print_status "Installing frontend dependencies..."
cd frontend
if [ ! -f "package.json" ]; then
    print_error "package.json not found in frontend directory"
    exit 1
fi

if [ ! -d "node_modules" ]; then
    npm install >/dev/null 2>&1
    print_success "Frontend dependencies installed"
else
    print_status "Frontend dependencies already installed"
fi

# Build frontend
print_status "Building frontend..."
npm run build >/dev/null 2>&1
print_success "Frontend built successfully"

# Go back to project root
cd ..

# Check environment variables
print_status "Checking environment configuration..."
cd backend

if [ ! -f ".env" ]; then
    print_warning ".env file not found, creating with default values..."
    cat > .env << EOF
# Database Configuration
DATABASE_URL=sqlite:///./scaie.db

# Security Configuration
SECRET_KEY=scaie_secret_key_for_development
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# DashScope API Configuration (Qwen)
# Get your key at: https://dashscope.aliyuncs.com/
DASHSCOPE_API_KEY=your_dashscope_api_key_here

# Qwen Model Configuration
QWEN_MODEL=qwen-plus

# Text Generation Configuration
TEMPERATURE=0.8
MAX_TOKENS=1024
TOP_P=0.9
TOP_K=30

# Agent Configuration
AGENT_NAME=SCAI
AGENT_PERSONALITY=amigable, empático, profesional, persuasivo
AGENT_TONE=coloquial pero respetuoso
AGENT_GOAL=ayudar a los usuarios a entender los beneficios de SCAIE de manera natural

# Development Settings
SKIP_AUTH=true
EOF
    print_success ".env file created with default values"
    print_warning "Please update DASHSCOPE_API_KEY with your actual API key"
else
    print_success ".env file found"
fi

# Check database
print_status "Checking database..."
if [ ! -f "scaie.db" ]; then
    print_warning "Database not found, it will be created automatically on first run"
else
    print_success "Database found"
fi

# Kill any existing processes on port 8003
print_status "Checking for processes on port 8003..."
kill_port_processes 8003

# Go to the directory with main.py
cd src/scaie

# Final instructions
echo ""
echo "=============================================="
echo "  SCAIE is ready to run!                      "
echo "=============================================="
echo ""
print_success "Starting the application..."
print_success "The application will be available at:"
echo "    Web Interface: http://localhost:8003"
echo "    API Documentation: http://localhost:8003/docs"
echo "    Health Check: http://localhost:8003/health"
echo ""
print_warning "Press Ctrl+C to stop the application"
echo ""

# Start the application
trap 'print_status "Shutting down..."; exit 0' INT TERM
python3 -m app.main