#!/bin/bash

# SCAIE Production Deployment Script
# Inicia el sistema completo con ngrok como proxy inverso

set -e  # Exit on any error

echo "🚀 Iniciando SCAIE en modo producción..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

echo -e "${BLUE}📁 Directorio del proyecto: $PROJECT_ROOT${NC}"

# Load environment variables
if [ -f ".env" ]; then
    echo -e "${GREEN}✅ Cargando variables de entorno...${NC}"
    set -o allexport
    source .env
    set +o allexport
else
    echo -e "${RED}❌ Error: Archivo .env no encontrado${NC}"
    exit 1
fi

# Check Python environment
echo -e "${BLUE}🐍 Verificando entorno Python...${NC}"
if [ -d "venv" ]; then
    echo -e "${GREEN}✅ Activando entorno virtual...${NC}"
    source venv/bin/activate
else
    echo -e "${RED}❌ Error: Entorno virtual no encontrado${NC}"
    exit 1
fi

# Check dependencies
echo -e "${BLUE}📦 Verificando dependencias...${NC}"
cd core/backend
pip install -r requirements.txt > /dev/null 2>&1
cd ../..

# Start Backend Server in background
echo -e "${YELLOW}🔧 Iniciando servidor backend...${NC}"
cd core/backend
nohup python -m uvicorn src.scaie.app.main:app --host 0.0.0.0 --port 8000 --reload > ../../logs/backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID" > ../../logs/backend.pid
cd ../..

# Wait for backend to start
echo -e "${BLUE}⏳ Esperando que el backend inicie...${NC}"
for i in {1..30}; do
    if curl -s http://localhost:8000/health > /dev/null; then
        echo -e "${GREEN}✅ Backend iniciado correctamente en puerto 8000${NC}"
        break
    fi
    if [ $i -eq 30 ]; then
        echo -e "${RED}❌ Error: Backend no pudo iniciar después de 30 segundos${NC}"
        echo -e "${RED}Ver logs: tail -f logs/backend.log${NC}"
        exit 1
    fi
    sleep 1
done

# Start Telegram Bot in background
echo -e "${YELLOW}🤖 Iniciando bot de Telegram...${NC}"
cd integrations/telegram
nohup python scai_telegram_bot.py > ../../logs/telegram.log 2>&1 &
TELEGRAM_PID=$!
echo "$TELEGRAM_PID" > ../../logs/telegram.pid
cd ../..

echo -e "${GREEN}✅ Bot de Telegram iniciado (PID: $TELEGRAM_PID)${NC}"

# Start ngrok tunnel
echo -e "${YELLOW}🌐 Iniciando túnel ngrok...${NC}"
nohup ngrok http 8000 --log=stdout > logs/ngrok.log 2>&1 &
NGROK_PID=$!
echo "$NGROK_PID" > logs/ngrok.pid

# Wait for ngrok to start and get URL
echo -e "${BLUE}⏳ Esperando que ngrok genere la URL...${NC}"
sleep 10

# Get ngrok URL
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    tunnel = data['tunnels'][0]['public_url']
    print(tunnel)
except:
    print('')
")

if [ -n "$NGROK_URL" ]; then
    echo -e "${GREEN}✅ Túnel ngrok activo: $NGROK_URL${NC}"
    echo -e "${GREEN}🌍 URL pública del API: $NGROK_URL/docs${NC}"
    echo -e "${GREEN}📱 Webhook URL para Telegram: $NGROK_URL/api/v1/telegram/webhook${NC}"
    echo -e "${GREEN}📱 Webhook URL para WhatsApp: $NGROK_URL/api/v1/whatsapp/webhook${NC}"
    
    # Save URLs to file for reference
    echo "NGROK_PUBLIC_URL=$NGROK_URL" > .env.production
    echo "TELEGRAM_WEBHOOK_URL=$NGROK_URL/api/v1/telegram/webhook" >> .env.production
    echo "WHATSAPP_WEBHOOK_URL=$NGROK_URL/api/v1/whatsapp/webhook" >> .env.production
    
    echo -e "${BLUE}💾 URLs guardadas en .env.production${NC}"
else
    echo -e "${RED}❌ Error: No se pudo obtener la URL de ngrok${NC}"
fi

# Save all PIDs
cat > logs/production.pids << EOF
BACKEND_PID=$BACKEND_PID
TELEGRAM_PID=$TELEGRAM_PID
NGROK_PID=$NGROK_PID
EOF

echo -e "${GREEN}💾 PIDs guardados en logs/production.pids${NC}"

# Show status
echo ""
echo -e "${GREEN}🎉 ¡SISTEMA SCAIE EN PRODUCCIÓN INICIADO!${NC}"
echo ""
echo -e "${YELLOW}📊 RESUMEN DE SERVICIOS:${NC}"
echo -e "${BLUE}• Backend API: http://localhost:8000${NC}"
echo -e "${BLUE}• Telegram Bot: ✅ Activo${NC}"
echo -e "${BLUE}• ngrok Tunnel: $NGROK_URL${NC}"
echo -e "${BLUE}• Panel ngrok: http://localhost:4040${NC}"
echo ""
echo -e "${YELLOW}📱 CONTACTO PARA CITAS:${NC}"
echo -e "${GREEN}• Teléfono: 5535913417${NC}"
echo -e "${GREEN}• WhatsApp: https://wa.me/5535913417${NC}"
echo ""
echo -e "${YELLOW}📁 LOGS:${NC}"
echo -e "${BLUE}• Backend: logs/backend.log${NC}"
echo -e "${BLUE}• Telegram: logs/telegram.log${NC}"
echo -e "${BLUE}• ngrok: logs/ngrok.log${NC}"
echo ""
echo -e "${YELLOW}🛑 Para detener todos los servicios: ./stop-production.sh${NC}"
echo ""
echo -e "${GREEN}🔥 El agente está optimizado para convertir leads en citas al 5535913417${NC}"
