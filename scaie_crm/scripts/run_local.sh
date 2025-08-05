#!/bin/bash

# Script para ejecutar la aplicación SCAIE localmente

# Verificar si el entorno virtual existe, si no, crearlo
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r backend/requirements.txt
else
    echo "Activando entorno virtual..."
    source venv/bin/activate
fi

# Verificar si el archivo .env existe, si no, crearlo con valores por defecto
if [ ! -f ".env" ]; then
    echo "Creando archivo .env..."
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

# Iniciar la aplicación
echo "Iniciando la aplicación SCAIE..."
python3 backend/app/main.py
