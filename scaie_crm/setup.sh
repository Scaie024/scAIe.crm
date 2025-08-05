#!/bin/bash

# Setup script for SCAIE - Sistema Agente Conversacional Inteligente Empresarial

echo "=============================================="
echo "  SCAIE - Sistema Agente Conversacional       "
echo "  Script de Configuración                     "
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

print_status "Setting up SCAIE application..."

# Step 1: Setup virtual environment
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

# Step 2: Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip
print_success "pip upgraded"

# Step 3: Install backend dependencies
print_status "Installing backend dependencies..."
if [ -f "backend/requirements.txt" ]; then
    pip install -r backend/requirements.txt
else
    # Install required packages directly
    pip install fastapi uvicorn sqlalchemy python-dotenv openai pydantic python-telegram-bot requests python-multipart
fi
print_success "Backend dependencies installed"

# Step 4: Install frontend dependencies
print_status "Installing frontend dependencies..."
cd frontend
if command -v npm &> /dev/null; then
    if [ ! -d "node_modules" ]; then
        npm install
        print_success "Frontend dependencies installed"
    else
        print_status "Frontend dependencies already installed"
    fi
else
    print_warning "npm not found, skipping frontend dependency installation"
fi

# Go back to root directory
cd ..

echo ""
echo "=============================================="
echo "  SCAIE setup completed successfully!         "
echo "=============================================="
echo ""
print_success "To run the application, execute:"
echo "    ./run_app.sh"
echo ""
print_success "To activate the virtual environment manually, run:"
echo "    source venv/bin/activate"
echo ""