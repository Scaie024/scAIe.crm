#!/bin/bash

# Script de monitoreo del sistema SCAIE
# Muestra el estado actual de todos los servicios

echo "📊 ESTADO DEL SISTEMA SCAIE"
echo "============================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo -e "${BLUE}📁 Directorio: $PROJECT_ROOT${NC}"
echo -e "${BLUE}⏰ Fecha: $(date)${NC}"
echo ""

# 1. Estado del Backend
echo -e "${BLUE}🔧 BACKEND (Puerto 8000):${NC}"
if curl -s http://localhost:8000/health >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Backend funcionando correctamente${NC}"
    BACKEND_PID=$(lsof -t -i:8000 2>/dev/null)
    if [ -n "$BACKEND_PID" ]; then
        echo -e "${BLUE}   PID: $BACKEND_PID${NC}"
    fi
else
    echo -e "${RED}❌ Backend no responde${NC}"
fi

# 2. Estado de ngrok
echo -e "\n${BLUE}🌐 NGROK:${NC}"
if curl -s http://localhost:4040/api/tunnels >/dev/null 2>&1; then
    NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    if 'tunnels' in data and len(data['tunnels']) > 0:
        tunnel = data['tunnels'][0]['public_url']
        print(tunnel)
    else:
        print('')
except:
    print('')
")
    if [ -n "$NGROK_URL" ]; then
        echo -e "${GREEN}✅ Túnel activo: $NGROK_URL${NC}"
        
        # Verificar conectividad pública
        if curl -s "$NGROK_URL/health" >/dev/null 2>&1; then
            echo -e "${GREEN}✅ API pública accesible${NC}"
        else
            echo -e "${YELLOW}⚠️ API pública no accesible${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️ ngrok corriendo pero sin túneles${NC}"
    fi
    
    NGROK_PID=$(pgrep ngrok 2>/dev/null)
    if [ -n "$NGROK_PID" ]; then
        echo -e "${BLUE}   PID: $NGROK_PID${NC}"
    fi
else
    echo -e "${RED}❌ ngrok no está corriendo${NC}"
fi

# 3. Estado del Bot de Telegram
echo -e "\n${BLUE}🤖 BOT DE TELEGRAM:${NC}"
TELEGRAM_PID=$(pgrep -f "scai_telegram_bot.py" 2>/dev/null)
if [ -n "$TELEGRAM_PID" ]; then
    echo -e "${GREEN}✅ Bot de Telegram activo${NC}"
    echo -e "${BLUE}   PID: $TELEGRAM_PID${NC}"
else
    echo -e "${RED}❌ Bot de Telegram no está corriendo${NC}"
fi

# 4. Estado de la Base de Datos
echo -e "\n${BLUE}💾 BASE DE DATOS:${NC}"
if [ -f "data/scaie.db" ]; then
    DB_SIZE=$(du -h data/scaie.db | cut -f1)
    echo -e "${GREEN}✅ Base de datos disponible (${DB_SIZE})${NC}"
else
    echo -e "${RED}❌ Base de datos no encontrada${NC}"
fi

# 5. Logs recientes
echo -e "\n${BLUE}📝 LOGS RECIENTES:${NC}"
if [ -f "logs/backend.log" ]; then
    BACKEND_LINES=$(wc -l < logs/backend.log)
    echo -e "${BLUE}• Backend: $BACKEND_LINES líneas${NC}"
    if [ $BACKEND_LINES -gt 0 ]; then
        echo -e "${YELLOW}  Última línea: $(tail -1 logs/backend.log)${NC}"
    fi
else
    echo -e "${YELLOW}• Backend: Sin logs${NC}"
fi

if [ -f "logs/telegram.log" ]; then
    TELEGRAM_LINES=$(wc -l < logs/telegram.log)
    echo -e "${BLUE}• Telegram: $TELEGRAM_LINES líneas${NC}"
    if [ $TELEGRAM_LINES -gt 0 ]; then
        echo -e "${YELLOW}  Última línea: $(tail -1 logs/telegram.log)${NC}"
    fi
else
    echo -e "${YELLOW}• Telegram: Sin logs${NC}"
fi

if [ -f "logs/ngrok.log" ]; then
    NGROK_LINES=$(wc -l < logs/ngrok.log)
    echo -e "${BLUE}• ngrok: $NGROK_LINES líneas${NC}"
else
    echo -e "${YELLOW}• ngrok: Sin logs${NC}"
fi

# 6. Uso de recursos
echo -e "\n${BLUE}⚡ USO DE RECURSOS:${NC}"
if [ -n "$BACKEND_PID" ]; then
    CPU_USAGE=$(ps -p $BACKEND_PID -o %cpu= 2>/dev/null | xargs)
    MEM_USAGE=$(ps -p $BACKEND_PID -o %mem= 2>/dev/null | xargs)
    echo -e "${BLUE}• Backend CPU: ${CPU_USAGE}% | RAM: ${MEM_USAGE}%${NC}"
fi

if [ -n "$TELEGRAM_PID" ]; then
    CPU_USAGE=$(ps -p $TELEGRAM_PID -o %cpu= 2>/dev/null | xargs)
    MEM_USAGE=$(ps -p $TELEGRAM_PID -o %mem= 2>/dev/null | xargs)
    echo -e "${BLUE}• Telegram CPU: ${CPU_USAGE}% | RAM: ${MEM_USAGE}%${NC}"
fi

if [ -n "$NGROK_PID" ]; then
    CPU_USAGE=$(ps -p $NGROK_PID -o %cpu= 2>/dev/null | xargs)
    MEM_USAGE=$(ps -p $NGROK_PID -o %mem= 2>/dev/null | xargs)
    echo -e "${BLUE}• ngrok CPU: ${CPU_USAGE}% | RAM: ${MEM_USAGE}%${NC}"
fi

# 7. Enlaces útiles
echo -e "\n${BLUE}🔗 ENLACES RÁPIDOS:${NC}"
echo -e "${BLUE}• Panel ngrok: http://localhost:4040${NC}"
echo -e "${BLUE}• API local: http://localhost:8000/docs${NC}"
if [ -n "$NGROK_URL" ]; then
    echo -e "${BLUE}• API pública: $NGROK_URL/docs${NC}"
    echo -e "${BLUE}• Frontend: $NGROK_URL${NC}"
fi

# 8. Comandos útiles
echo -e "\n${BLUE}🛠️ COMANDOS ÚTILES:${NC}"
echo -e "${BLUE}• Ver logs backend: tail -f logs/backend.log${NC}"
echo -e "${BLUE}• Ver logs telegram: tail -f logs/telegram.log${NC}"
echo -e "${BLUE}• Reiniciar sistema: ./stop-production.sh && ./start-production.sh${NC}"
echo -e "${BLUE}• Verificar sistema: ./scripts/verify_system.sh${NC}"

echo ""
echo -e "${GREEN}✨ Monitoreo completado${NC}"
