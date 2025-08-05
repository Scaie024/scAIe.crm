#!/bin/bash

# Simple run script for SCAIE - Sistema Agente Conversacional Inteligente Empresarial

echo "=============================================="
echo "  SCAIE - Sistema Agente Conversacional       "
echo "  Script de Ejecución Simple                  "
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

print_status "Starting SCAIE application..."

# Activate virtual environment
print_status "Activating virtual environment..."
if [ -d "venv" ]; then
    source venv/bin/activate
    print_success "Virtual environment activated"
else
    print_warning "Virtual environment not found, using system Python"
fi

# Step 1: Check .env file
print_status "Checking environment configuration..."
cd backend
if [ ! -f ".env" ]; then
    print_warning ".env file not found"
    print_warning "Please create a .env file with your DashScope API key"
    print_warning "Example content:"
    echo "DASHSCOPE_API_KEY=your_dashscope_api_key_here"
    echo "DATABASE_URL=sqlite:///./scaie.db"
    echo ""
else
    print_success ".env file found"
fi

# Step 2: Check database
print_status "Checking database..."
if [ ! -f "scaie.db" ]; then
    print_warning "Database not found"
    print_warning "The application will create it automatically on first run"
else
    print_success "Database found"
fi

# Step 3: Kill any existing processes on port 8003
print_status "Checking for processes on port 8003..."
if lsof -i :8003 > /dev/null 2>&1; then
    print_warning "Process found on port 8003. Terminating..."
    lsof -t -i :8003 | xargs kill -9
    print_success "Process terminated"
else
    print_success "No processes found on port 8003"
fi

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
python3 -m app.main