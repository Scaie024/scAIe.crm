#!/bin/bash

# SCAIE - Sistema Agente Startup Script
# Script mejorado para iniciar el sistema fácilmente

set -e  # Salir inmediatamente si un comando falla

echo "========================================="
echo "  SCAIE - Sistema Agente Conversacional  "
echo "========================================="

# Directorio base
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$BASE_DIR"

# Verificar si estamos en el directorio correcto
if [ ! -d "backend" ]; then
    echo "❌ Error: No se encuentra el directorio 'backend'"
    echo "Por favor ejecuta este script desde el directorio raíz del proyecto"
    exit 1
fi

# Detectar sistema operativo
echo "🔍 Detectando sistema operativo..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "   Sistema detectado: macOS"
    PYTHON_CMD="python3"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "   Sistema detectado: Linux"
    PYTHON_CMD="python3"
else
    echo "   Sistema detectado: Otro (usando python3)"
    PYTHON_CMD="python3"
fi

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "🔧 Creando entorno virtual..."
    $PYTHON_CMD -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Error al crear el entorno virtual"
        exit 1
    fi
else
    echo "✅ Entorno virtual ya existe"
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Verificar si las dependencias están instaladas
echo "🔍 Verificando dependencias..."
if [ ! -f "backend/requirements.txt" ]; then
    echo "❌ No se encuentra el archivo de requerimientos"
    exit 1
fi

# Instalar/actualizar dependencias
echo "🔧 Instalando dependencias..."
pip install -r backend/requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Error al instalar dependencias"
    exit 1
fi

# Navegar al directorio frontend
cd frontend

# Verificar si node_modules existe
if [ ! -d "node_modules" ]; then
    echo "🔧 Instalando dependencias del frontend..."
    npm install
    if [ $? -ne 0 ]; then
        echo "❌ Error al instalar dependencias del frontend"
        exit 1
    fi
else
    echo "✅ Dependencias del frontend ya instaladas"
fi

# Construir el frontend
echo "🔧 Construyendo el frontend..."
npm run build
if [ $? -ne 0 ]; then
    echo "❌ Error al construir el frontend"
    exit 1
fi

echo "✅ Frontend construido exitosamente"

# Navegar al directorio backend
cd ../backend

# Debug: Verificar si app.main:app es importable
echo "🔍 Verificando si 'app.main:app' es importable..."
python -c "from app.main import app" && echo "✅ 'app.main:app' es importable" || (echo "❌ Error al importar 'app.main:app'" && exit 1)

# Debug: Listar procesos en el puerto 8001
echo "🔍 Listando procesos en el puerto 8001..."
lsof -i :8001

# Si hay procesos en el puerto 8001, terminarlos
if lsof -i :8001 > /dev/null; then
    echo "⚠️  Proceso encontrado en el puerto 8001. Terminando..."
    lsof -t -i :8001 | xargs kill -9
    echo "✅ Proceso terminado"
fi

# Crear archivo .env si no existe
if [ ! -f ".env" ]; then
    echo "🔧 Creando archivo .env con configuración por defecto..."
    cat > .env << EOF
# Configuración de base de datos
DATABASE_URL=sqlite:///./scaie.db

# Configuración de Qwen AI (requerido)
# Obtén tu clave en: https://dashscope.aliyuncs.com/
DASHSCOPE_API_KEY=sk-1ded1e3aa4d04a7593afc74a484cd4c1

# Modelo Qwen a utilizar
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
    echo "✅ Archivo .env creado"
else
    echo "✅ Archivo .env ya existe"
fi

# Crear base de datos si no existe
echo "🔧 Verificando base de datos..."
if [ ! -f "scaie.db" ]; then
    echo "✅ Base de datos SQLite creada automáticamente al iniciar la aplicación"
else
    echo "✅ Base de datos ya existe"
fi

# Verificar clave de API
if grep -q "DASHSCOPE_API_KEY=sk-1ded1e3aa4d04a7593afc74a484cd4c1" .env; then
    echo "⚠️  Usando clave de API de ejemplo. Para producción, actualiza con tu propia clave."
fi

echo ""
echo "========================================="
echo "  ¡Sistema listo para iniciar!           "
echo "========================================="
echo "Puerto: 8001"
echo "API: http://localhost:8001"
echo "Docs: http://localhost:8001/docs"
echo "Frontend: http://localhost:8001/"
echo ""
echo "Para detener el servidor: Ctrl+C"
echo ""
echo "Iniciando servidor con información de depuración..."

# Iniciar el servidor con información de depuración
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001