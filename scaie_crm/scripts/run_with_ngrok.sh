#!/bin/bash

# Script para ejecutar la aplicación SCAIE localmente y conectarla a ngrok para pruebas en línea

set -e  # Salir inmediatamente si un comando falla

echo "========================================="
echo "  SCAIE - Sistema Agente Conversacional  "
echo "========================================="
echo "Ejecutando aplicación localmente con ngrok"
echo ""

# Directorio base
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$BASE_DIR"

# Verificar si ngrok está instalado
if ! command -v ngrok &> /dev/null
then
    echo "❌ Error: ngrok no está instalado"
    echo "Por favor instala ngrok siguiendo las instrucciones en: https://ngrok.com/download"
    exit 1
fi

echo "✅ ngrok está instalado"

# Verificar si el entorno virtual existe, si no, crearlo
if [ ! -d "venv" ]; then
    echo "🔧 Creando entorno virtual..."
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r backend/requirements.txt
else
    echo "✅ Entorno virtual ya existe"
    source venv/bin/activate
fi

# Verificar si el archivo .env existe, si no, crearlo con valores por defecto
if [ ! -f ".env" ]; then
    echo "🔧 Creando archivo .env..."
    cat > .env << EOF
# Configuración de la base de datos
DATABASE_URL=sqlite:///./scaie.db

# Configuración de seguridad
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Configuración de la API de DashScope (Qwen)
DASHSCOPE_API_KEY=sk-ff40b02e0b454d379ea51160cfbadfa9

# Configuración del modelo Qwen
QWEN_MODEL=qwen-plus

# Configuración de generación de texto
TEMPERATURE=0.8
MAX_TOKENS=1024
TOP_P=0.9
TOP_K=30
EOF
fi

# Navegar al directorio frontend
cd frontend

# Verificar si node_modules existe
if [ ! -d "node_modules" ]; then
    echo "🔧 Instalando dependencias del frontend..."
    npm install
else
    echo "✅ Dependencias del frontend ya instaladas"
fi

# Construir el frontend
echo "🔧 Construyendo el frontend..."
npm run build

echo "✅ Frontend construido exitosamente"

# Navegar al directorio backend
cd ../backend

# Verificar si la base de datos existe
if [ ! -f "scaie.db" ]; then
    echo "✅ La base de datos se creará automáticamente al iniciar la aplicación"
fi

# Verificar si hay procesos en el puerto 8001
if lsof -i :8001 > /dev/null; then
    echo "⚠️  Proceso encontrado en el puerto 8001. Terminando..."
    lsof -t -i :8001 | xargs kill -9
    echo "✅ Proceso terminado"
fi

echo ""
echo "========================================="
echo "  ¡Iniciando servidor local y ngrok!     "
echo "========================================="
echo "Puerto local: 8001"
echo "API local: http://localhost:8001"
echo "Docs local: http://localhost:8001/docs"
echo "Frontend local: http://localhost:8001/"
echo ""

# Función para limpiar procesos al salir
cleanup() {
    echo "🛑 Deteniendo procesos..."
    if [ ! -z "$UVICORN_PID" ]; then
        kill $UVICORN_PID 2>/dev/null || true
    fi
    if [ ! -z "$NGROK_PID" ]; then
        kill $NGROK_PID 2>/dev/null || true
    fi
    exit 0
}

# Capturar señales para limpiar procesos
trap cleanup SIGINT SIGTERM

# Iniciar el servidor uvicorn en segundo plano
echo "🚀 Iniciando servidor uvicorn..."
uvicorn app.main:app --host 0.0.0.0 --port 8001 &
UVICORN_PID=$!

# Esperar un momento para que el servidor inicie
sleep 3

# Verificar si el servidor se inició correctamente
if lsof -i :8001 > /dev/null; then
    echo "✅ Servidor uvicorn iniciado correctamente"
else
    echo "❌ Error al iniciar el servidor uvicorn"
    cleanup
    exit 1
fi

# Iniciar ngrok en segundo plano
echo "🚀 Iniciando ngrok..."
ngrok http 8001 &
NGROK_PID=$!

echo ""
echo "========================================="
echo "  ¡Servidor y ngrok iniciados!           "
echo "========================================="
echo ""
echo "💡 Instrucciones:"
echo "1. Accede localmente a: http://localhost:8001"
echo "2. Para acceder en línea, revisa la URL que ngrok proporciona en:"
echo "   http://localhost:4040"
echo "3. Presiona Ctrl+C para detener ambos servicios"
echo ""

# Esperar a que ambos procesos terminen
wait $UVICORN_PID $NGROK_PID