#!/bin/bash

# Script para iniciar el servidor SCAIE de forma confiable

echo "========================================"
echo "  SCAIE - Sistema Agente Conversacional"
echo "========================================"

# Directorio base
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "📁 Directorio actual: $(pwd)"

# Verificar directorio backend
if [ ! -d "backend" ]; then
    echo "❌ Error: No se encuentra el directorio 'backend'"
    exit 1
fi

# Verificar entorno virtual
if [ ! -d "venv" ]; then
    echo "❌ Error: No se encuentra el entorno virtual 'venv'"
    exit 1
fi

echo "✅ Entorno virtual encontrado"

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Verificar dependencias
echo "🔍 Verificando dependencias..."
if ! python -c "import fastapi" 2>/dev/null; then
    echo "❌ FastAPI no está instalado"
    exit 1
fi

if ! python -c "import uvicorn" 2>/dev/null; then
    echo "❌ Uvicorn no está instalado"
    exit 1
fi

echo "✅ Dependencias verificadas"

# Verificar que la aplicación se puede importar
echo "🔍 Verificando aplicación principal..."
if ! python -c "from backend.app.main import app" 2>/dev/null; then
    echo "❌ No se puede importar la aplicación principal"
    exit 1
fi

echo "✅ Aplicación principal verificada"

# Cambiar al directorio backend
cd backend

# Verificar archivo de base de datos
if [ ! -f "scaie.db" ]; then
    echo "🆕 Creando base de datos SQLite..."
    touch scaie.db
fi

echo "🔧 Verificando archivo .env..."
if [ ! -f ".env" ]; then
    echo "⚠️  Creando archivo .env con configuración por defecto..."
    cat > .env << EOF
# Configuración de base de datos
DATABASE_URL=sqlite:///./scaie.db

# Configuración de Qwen AI (requerido)
DASHSCOPE_API_KEY=sk-1ded1e3aa4d04a7593afc74a484cd4c1
QWEN_MODEL=qwen-plus

# Configuración de autenticación
SECRET_KEY=scaie_secret_key_for_development
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Configuración del agente
AGENT_NAME=SCAI
AGENT_PERSONALITY=amigable, empático, profesional, persuasivo
AGENT_TONE=coloquial pero respetuoso
AGENT_GOAL=ayudar a los usuarios a entender los beneficios de SCAIE de manera natural

# Saltar autenticación (solo para desarrollo)
SKIP_AUTH=true
EOF
fi

# Puerto y host
PORT=8001
HOST="127.0.0.1"

echo ""
echo "========================================"
echo "  Iniciando servidor SCAIE"
echo "========================================"
echo "🌐 Host: $HOST"
echo "📍 Puerto: $PORT"
echo "📂 Directorio: $(pwd)"
echo ""
echo "Accede a:"
echo "  API Principal: http://$HOST:$PORT/"
echo "  Documentación: http://$HOST:$PORT/docs"
echo "  Interfaz Web:  http://$HOST:$PORT/static/index.html"
echo ""
echo "Para detener el servidor: Ctrl+C"
echo ""

# Iniciar el servidor
python -m uvicorn app.main:app --host $HOST --port $PORT --reload