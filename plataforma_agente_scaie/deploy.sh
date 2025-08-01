#!/bin/bash

# SCAIE - Production Deployment Script
# Script for deploying SCAIE in production environments

set -e  # Exit immediately if a command exits with a non-zero status

echo "========================================="
echo "  SCAIE - Sistema Agente v1.0           "
echo "  Production Deployment Script          "
echo "========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}!${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if running as root (optional)
if [ "$EUID" -eq 0 ]; then
    print_warning "Running as root. This is not recommended for production."
fi

# Base directory
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$BASE_DIR"

# Check if we're in the right directory
if [ ! -f "start.sh" ]; then
    print_error "This script must be run from the plataforma_agente_scaie directory"
    exit 1
fi

# Check for Docker
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check for Docker Compose
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

print_status "Docker and Docker Compose found"

# Check for environment variables
if [ -z "$DASHSCOPE_API_KEY" ]; then
    print_warning "DASHSCOPE_API_KEY environment variable not set"
    echo "Please set it with: export DASHSCOPE_API_KEY=your_api_key"
    echo "Or create a .env file with the variable"
fi

if [ -z "$SECRET_KEY" ]; then
    print_warning "SECRET_KEY environment variable not set"
    echo "Please set it with: export SECRET_KEY=your_secret_key"
    echo "Or create a .env file with the variable"
fi

# Build and deploy with Docker Compose
print_status "Building and deploying with Docker Compose"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    print_status "Creating .env file"
    cat > .env << EOF
DASHSCOPE_API_KEY=${DASHSCOPE_API_KEY:-your_dashscope_api_key_here}
SECRET_KEY=${SECRET_KEY:-scaie_secret_key_for_production_please_change_this}
EOF
    print_warning "Please update the .env file with your actual API keys and secrets"
fi

# Build and start services
print_status "Starting services with Docker Compose"
docker-compose -f docker-compose.prod.yml up -d --build

# Wait for services to start
print_status "Waiting for services to start..."
sleep 10

# Check if services are running
if docker-compose -f docker-compose.prod.yml ps | grep -q "Up"; then
    print_status "Services are running successfully!"
    
    echo ""
    echo "========================================="
    echo "  Deployment Complete!                  "
    echo "========================================="
    echo "Frontend: http://localhost/"
    echo "API: http://localhost/api"
    echo "Documentation: http://localhost/docs"
    echo ""
    echo "To stop the services, run:"
    echo "  docker-compose -f docker-compose.prod.yml down"
    echo ""
else
    print_error "Services failed to start. Check the logs with:"
    echo "  docker-compose -f docker-compose.prod.yml logs"
    exit 1
fi