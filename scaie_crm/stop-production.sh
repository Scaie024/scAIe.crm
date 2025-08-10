#!/bin/bash

# SCAIE Production Stop Script
# Detiene todos los servicios de producción

set -e

echo "🛑 Deteniendo servicios de SCAIE..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Get project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

# Read PIDs if available
if [ -f "logs/production.pids" ]; then
    echo -e "${BLUE}📖 Leyendo PIDs de servicios...${NC}"
    source logs/production.pids
    
    # Stop backend
    if [ -n "$BACKEND_PID" ] && kill -0 "$BACKEND_PID" 2>/dev/null; then
        echo -e "${YELLOW}🔧 Deteniendo backend (PID: $BACKEND_PID)...${NC}"
        kill "$BACKEND_PID"
        echo -e "${GREEN}✅ Backend detenido${NC}"
    fi
    
    # Stop Telegram bot
    if [ -n "$TELEGRAM_PID" ] && kill -0 "$TELEGRAM_PID" 2>/dev/null; then
        echo -e "${YELLOW}🤖 Deteniendo bot de Telegram (PID: $TELEGRAM_PID)...${NC}"
        kill "$TELEGRAM_PID"
        echo -e "${GREEN}✅ Bot de Telegram detenido${NC}"
    fi
    
    # Stop ngrok
    if [ -n "$NGROK_PID" ] && kill -0 "$NGROK_PID" 2>/dev/null; then
        echo -e "${YELLOW}🌐 Deteniendo túnel ngrok (PID: $NGROK_PID)...${NC}"
        kill "$NGROK_PID"
        echo -e "${GREEN}✅ Túnel ngrok detenido${NC}"
    fi
    
    # Remove PID file
    rm -f logs/production.pids
else
    echo -e "${YELLOW}⚠️  Archivo de PIDs no encontrado, buscando procesos manualmente...${NC}"
fi

# Fallback: kill any remaining processes
echo -e "${BLUE}🔍 Verificando procesos restantes...${NC}"

# Kill any uvicorn processes on port 8000
UVICORN_PID=$(lsof -t -i:8000 2>/dev/null || true)
if [ -n "$UVICORN_PID" ]; then
    echo -e "${YELLOW}🔧 Matando proceso uvicorn restante (PID: $UVICORN_PID)...${NC}"
    kill -9 "$UVICORN_PID" 2>/dev/null || true
fi

# Kill any ngrok processes
NGROK_PIDS=$(pgrep ngrok 2>/dev/null || true)
if [ -n "$NGROK_PIDS" ]; then
    echo -e "${YELLOW}🌐 Matando procesos ngrok restantes...${NC}"
    pkill ngrok 2>/dev/null || true
fi

# Kill any telegram bot processes
TELEGRAM_PIDS=$(pgrep -f "scai_telegram_bot.py" 2>/dev/null || true)
if [ -n "$TELEGRAM_PIDS" ]; then
    echo -e "${YELLOW}🤖 Matando procesos de telegram bot restantes...${NC}"
    pkill -f "scai_telegram_bot.py" 2>/dev/null || true
fi

# Clean up temporary files
echo -e "${BLUE}🧹 Limpiando archivos temporales...${NC}"
rm -f logs/*.pid
rm -f .env.production

echo ""
echo -e "${GREEN}✅ Todos los servicios de SCAIE han sido detenidos${NC}"
echo -e "${BLUE}📊 Los logs se mantienen en la carpeta logs/${NC}"
echo ""
