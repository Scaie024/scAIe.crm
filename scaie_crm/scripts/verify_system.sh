#!/bin/bash

# Script de verificación del sistema SCAIE
# Verifica que todos los componentes estén funcionando correctamente

set -e

echo "🔍 VERIFICACIÓN DEL SISTEMA SCAIE"
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo -e "${BLUE}📁 Directorio del proyecto: $PROJECT_ROOT${NC}"

# 1. Verificar archivo .env
echo -e "\n${BLUE}1. Verificando archivo .env...${NC}"
if [ -f ".env" ]; then
    echo -e "${GREEN}✅ Archivo .env encontrado${NC}"
    
    # Verificar variables críticas
    if grep -q "TELEGRAM_BOT_TOKEN=" .env && grep -q "DASHSCOPE_API_KEY=" .env; then
        echo -e "${GREEN}✅ Variables críticas configuradas${NC}"
    else
        echo -e "${RED}❌ Variables críticas faltantes en .env${NC}"
        exit 1
    fi
else
    echo -e "${RED}❌ Archivo .env no encontrado${NC}"
    exit 1
fi

# 2. Verificar entorno virtual
echo -e "\n${BLUE}2. Verificando entorno virtual...${NC}"
if [ -d "venv" ]; then
    echo -e "${GREEN}✅ Entorno virtual encontrado${NC}"
    source venv/bin/activate
    echo -e "${GREEN}✅ Entorno virtual activado${NC}"
else
    echo -e "${RED}❌ Entorno virtual no encontrado${NC}"
    exit 1
fi

# 3. Verificar dependencias del backend
echo -e "\n${BLUE}3. Verificando dependencias del backend...${NC}"
cd core/backend
if pip list | grep -q fastapi && pip list | grep -q uvicorn; then
    echo -e "${GREEN}✅ Dependencias principales instaladas${NC}"
else
    echo -e "${YELLOW}⚠️ Instalando dependencias...${NC}"
    pip install -r requirements.txt
    echo -e "${GREEN}✅ Dependencias instaladas${NC}"
fi
cd ../..

# 4. Verificar estructura de archivos críticos
echo -e "\n${BLUE}4. Verificando estructura de archivos...${NC}"
CRITICAL_FILES=(
    "core/backend/src/scaie/app/main.py"
    "integrations/telegram/scai_telegram_bot.py"
    "start-production.sh"
    "stop-production.sh"
)

for file in "${CRITICAL_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✅ $file${NC}"
    else
        echo -e "${RED}❌ $file no encontrado${NC}"
        exit 1
    fi
done

# 5. Verificar base de datos
echo -e "\n${BLUE}5. Verificando base de datos...${NC}"
if [ -f "data/scaie.db" ]; then
    echo -e "${GREEN}✅ Base de datos encontrada${NC}"
else
    echo -e "${YELLOW}⚠️ Creando directorio de datos...${NC}"
    mkdir -p data
    echo -e "${GREEN}✅ Directorio de datos creado${NC}"
fi

# 6. Verificar permisos de scripts
echo -e "\n${BLUE}6. Verificando permisos de scripts...${NC}"
chmod +x start-production.sh stop-production.sh scripts/*.sh
echo -e "${GREEN}✅ Permisos de ejecución configurados${NC}"

# 7. Verificar disponibilidad de puertos
echo -e "\n${BLUE}7. Verificando disponibilidad de puertos...${NC}"

# Puerto 8000 (Backend)
if lsof -i :8000 >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️ Puerto 8000 ocupado${NC}"
    echo "Proceso en puerto 8000:"
    lsof -i :8000
else
    echo -e "${GREEN}✅ Puerto 8000 disponible${NC}"
fi

# Puerto 4040 (ngrok dashboard)
if lsof -i :4040 >/dev/null 2>&1; then
    echo -e "${GREEN}✅ ngrok dashboard activo en puerto 4040${NC}"
else
    echo -e "${YELLOW}⚠️ ngrok dashboard no activo${NC}"
fi

# 8. Verificar conectividad a servicios externos
echo -e "\n${BLUE}8. Verificando conectividad externa...${NC}"

# Verificar API de DashScope
if curl -s --connect-timeout 5 https://dashscope.aliyuncs.com >/dev/null; then
    echo -e "${GREEN}✅ Conexión a DashScope disponible${NC}"
else
    echo -e "${YELLOW}⚠️ No se pudo verificar conexión a DashScope${NC}"
fi

# Verificar API de Telegram
if curl -s --connect-timeout 5 https://api.telegram.org >/dev/null; then
    echo -e "${GREEN}✅ Conexión a Telegram API disponible${NC}"
else
    echo -e "${YELLOW}⚠️ No se pudo verificar conexión a Telegram API${NC}"
fi

# 9. Verificar ngrok
echo -e "\n${BLUE}9. Verificando ngrok...${NC}"
if command -v ngrok >/dev/null 2>&1; then
    echo -e "${GREEN}✅ ngrok instalado${NC}"
    
    # Verificar si hay túneles activos
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
            echo -e "${GREEN}✅ Túnel ngrok activo: $NGROK_URL${NC}"
        else
            echo -e "${YELLOW}⚠️ ngrok está corriendo pero sin túneles activos${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️ ngrok no está corriendo${NC}"
    fi
else
    echo -e "${RED}❌ ngrok no está instalado${NC}"
    echo -e "${YELLOW}📝 Para instalar ngrok: brew install ngrok${NC}"
fi

# 10. Verificar logs
echo -e "\n${BLUE}10. Verificando logs...${NC}"
mkdir -p logs
echo -e "${GREEN}✅ Directorio de logs verificado${NC}"

# Resumen final
echo ""
echo -e "${GREEN}🎉 VERIFICACIÓN COMPLETADA${NC}"
echo ""
echo -e "${YELLOW}📋 PRÓXIMOS PASOS:${NC}"
echo -e "${BLUE}1. Para iniciar el sistema: ./start-production.sh${NC}"
echo -e "${BLUE}2. Para detener el sistema: ./stop-production.sh${NC}"
echo -e "${BLUE}3. Para monitorear logs: tail -f logs/*.log${NC}"
echo ""
echo -e "${YELLOW}🔗 ENLACES ÚTILES:${NC}"
echo -e "${BLUE}• Panel ngrok: http://localhost:4040${NC}"
echo -e "${BLUE}• API Docs: http://localhost:8000/docs${NC}"
if [ -n "$NGROK_URL" ]; then
    echo -e "${BLUE}• URL pública: $NGROK_URL${NC}"
    echo -e "${BLUE}• API pública: $NGROK_URL/docs${NC}"
fi

echo ""
echo -e "${GREEN}✨ Sistema verificado y listo para producción${NC}"
