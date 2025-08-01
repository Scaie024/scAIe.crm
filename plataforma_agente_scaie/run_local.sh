#!/bin/bash

# Script simplificado para ejecutar la aplicación localmente

echo "Iniciando SCAIE - Sistema Agente Conversacional..."

# Directorio base
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$BASE_DIR"

# Activar entorno virtual
if [ -d "venv" ]; then
    echo "Activando entorno virtual..."
    source venv/bin/activate
else
    echo "Creando entorno virtual..."
    python3 -m venv venv
    source venv/bin/activate
    echo "Instalando dependencias..."
    pip install -r backend/requirements.txt
fi

# Navegar al directorio backend
cd backend

# Crear archivo .env si no existe
if [ ! -f ".env" ]; then
    echo "Creando archivo .env con configuración por defecto..."
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
fi

echo "Iniciando servidor en el puerto 8001..."
echo "Accede a la aplicación en: http://localhost:8001"
echo "Documentación de la API: http://localhost:8001/docs"
echo "Presiona Ctrl+C para detener el servidor"

# Iniciar el servidor
uvicorn app.main:app --host 0.0.0.0 --port 8001