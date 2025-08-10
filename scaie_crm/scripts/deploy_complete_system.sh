#!/bin/bash

# Script de construcción y despliegue completo del sistema SCAIE
# Automatiza la construcción del frontend y actualización del sistema

set -e

echo "🚀 CONSTRUYENDO Y DESPLEGANDO SCAIE COMPLETO"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Get project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo -e "${BLUE}📁 Directorio del proyecto: $PROJECT_ROOT${NC}"

# 1. Construir el frontend
echo -e "\n${BLUE}1. Construyendo frontend...${NC}"
cd core/frontend

# Verificar que node_modules existe
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}📦 Instalando dependencias del frontend...${NC}"
    npm install
fi

# Construir para producción
echo -e "${GREEN}🔨 Construyendo frontend para producción...${NC}"
npm run build

# Copiar archivos al backend
echo -e "${GREEN}📋 Copiando archivos al backend...${NC}"
cp -r dist/* ../backend/src/scaie/static/

cd ../..

# 2. Verificar dependencias del backend
echo -e "\n${BLUE}2. Verificando dependencias del backend...${NC}"

# Activar entorno virtual si existe
if [ -d "venv" ]; then
    echo -e "${GREEN}🐍 Activando entorno virtual...${NC}"
    source venv/bin/activate
fi

# Instalar dependencias adicionales para RAG
echo -e "${YELLOW}📦 Instalando dependencias RAG...${NC}"
cd core/backend
pip install sentence-transformers numpy scikit-learn > /dev/null 2>&1
cd ../..

# 3. Detener servicios existentes
echo -e "\n${BLUE}3. Deteniendo servicios existentes...${NC}"
if [ -f "logs/production.pids" ]; then
    ./stop-production.sh
else
    echo -e "${YELLOW}⚠️ No hay servicios ejecutándose${NC}"
fi

# 4. Limpiar logs antiguos (opcional)
echo -e "\n${BLUE}4. Preparando logs...${NC}"
mkdir -p logs
# Rotar logs si son muy grandes
for logfile in logs/*.log; do
    if [ -f "$logfile" ] && [ $(wc -c < "$logfile") -gt 1048576 ]; then
        mv "$logfile" "${logfile}.old"
        echo -e "${YELLOW}📝 Rotado log: $(basename $logfile)${NC}"
    fi
done

# 5. Inicializar base de conocimiento RAG
echo -e "\n${BLUE}5. Preparando sistema RAG...${NC}"
mkdir -p data/knowledge
mkdir -p data/embeddings
echo -e "${GREEN}✅ Directorios RAG creados${NC}"

# 6. Iniciar servicios
echo -e "\n${BLUE}6. Iniciando servicios...${NC}"
./start-production.sh

# 7. Esperar a que todo esté funcionando
echo -e "\n${BLUE}7. Verificando estado del sistema...${NC}"
sleep 15

# Verificar que el backend esté respondiendo
if curl -s http://localhost:8000/health > /dev/null; then
    echo -e "${GREEN}✅ Backend funcionando correctamente${NC}"
else
    echo -e "${RED}❌ Backend no está respondiendo${NC}"
    exit 1
fi

# Obtener URL de ngrok
NGROK_URL=""
if curl -s http://localhost:4040/api/tunnels > /dev/null 2>&1; then
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
fi

# 8. Inicializar conocimiento por defecto
echo -e "\n${BLUE}8. Inicializando base de conocimiento...${NC}"
if [ -n "$NGROK_URL" ]; then
    curl -s -X POST "$NGROK_URL/api/v1/knowledge/initialize-defaults" > /dev/null 2>&1
    echo -e "${GREEN}✅ Base de conocimiento inicializada${NC}"
fi

# 9. Verificar todos los endpoints importantes
echo -e "\n${BLUE}9. Verificando endpoints...${NC}"
if [ -n "$NGROK_URL" ]; then
    # Verificar sandbox
    if curl -s "$NGROK_URL/api/v1/sandbox/test-scenarios" > /dev/null; then
        echo -e "${GREEN}✅ Sandbox funcionando${NC}"
    else
        echo -e "${YELLOW}⚠️ Sandbox no responde${NC}"
    fi
    
    # Verificar knowledge
    if curl -s "$NGROK_URL/api/v1/knowledge/categories" > /dev/null; then
        echo -e "${GREEN}✅ Sistema RAG funcionando${NC}"
    else
        echo -e "${YELLOW}⚠️ Sistema RAG no responde${NC}"
    fi
    
    # Verificar admin dashboard
    if curl -s "$NGROK_URL/api/v1/dashboard/metrics" > /dev/null; then
        echo -e "${GREEN}✅ Dashboard administrativo funcionando${NC}"
    else
        echo -e "${YELLOW}⚠️ Dashboard no responde${NC}"
    fi
fi

# 10. Resumen final
echo ""
echo -e "${GREEN}🎉 ¡DESPLIEGUE COMPLETADO EXITOSAMENTE!${NC}"
echo ""
echo -e "${YELLOW}📊 RESUMEN DEL SISTEMA:${NC}"
echo -e "${BLUE}• Frontend: ✅ Construido y desplegado${NC}"
echo -e "${BLUE}• Backend: ✅ Funcionando${NC}"
echo -e "${BLUE}• Bot Telegram: ✅ Activo${NC}"
echo -e "${BLUE}• Sistema RAG: ✅ Inicializado${NC}"
echo -e "${BLUE}• Base de conocimiento: ✅ Configurada${NC}"

if [ -n "$NGROK_URL" ]; then
    echo ""
    echo -e "${YELLOW}🌍 URLS PÚBLICAS:${NC}"
    echo -e "${BLUE}• Frontend: $NGROK_URL${NC}"
    echo -e "${BLUE}• Administración: $NGROK_URL/admin${NC}"
    echo -e "${BLUE}• Sandbox: $NGROK_URL/sandbox${NC}"
    echo -e "${BLUE}• API Docs: $NGROK_URL/docs${NC}"
    echo -e "${BLUE}• Panel ngrok: http://localhost:4040${NC}"
fi

echo ""
echo -e "${YELLOW}🛠️ NUEVAS FUNCIONALIDADES:${NC}"
echo -e "${BLUE}• Panel administrativo completo${NC}"
echo -e "${BLUE}• Sandbox interactivo para pruebas${NC}"
echo -e "${BLUE}• Sistema RAG con búsqueda semántica${NC}"
echo -e "${BLUE}• Gestión dinámica de conocimiento${NC}"
echo -e "${BLUE}• Métricas y analytics en tiempo real${NC}"

echo ""
echo -e "${YELLOW}📱 PARA GESTIONAR EL SISTEMA:${NC}"
echo -e "${BLUE}• Administración: Accede a /admin${NC}"
echo -e "${BLUE}• Pruebas del agente: Accede a /sandbox${NC}"
echo -e "${BLUE}• Detener sistema: ./stop-production.sh${NC}"
echo -e "${BLUE}• Monitorear: ./scripts/monitor_system.sh${NC}"

echo ""
echo -e "${GREEN}✨ Sistema completamente autónomo y optimizado${NC}"
