#!/bin/bash

# Script unificado para iniciar SCAIE
echo "🚀 SCAIE - Sistema Agente Conversacional"
echo "========================================"

# Verificar ubicación
if [ ! -f ".env" ]; then
    echo "❌ Error: Ejecuta este script desde la raíz del proyecto scaie_crm/"
    exit 1
fi

# Activar entorno virtual
if [ ! -d "venv" ]; then
    echo "⚙️  Creando entorno virtual..."
    python3 -m venv venv
fi

source venv/bin/activate
echo "✅ Entorno virtual activado"

# Instalar dependencias si es necesario
if [ ! -f "venv/.deps_installed" ]; then
    echo "📦 Instalando dependencias..."
    pip install --upgrade pip
    pip install -r core/backend/requirements.txt
    pip install dashscope "python-jose[cryptography]" bcrypt
    touch venv/.deps_installed
    echo "✅ Dependencias instaladas"
fi

# Verificar base de datos
echo "🗄️  Verificando base de datos..."
cd core/backend/src/scaie
python init_db.py
cd ../../../..

# Mostrar información
echo "======================================"
echo "🌐 Backend: http://localhost:8003"
echo "📖 API Docs: http://localhost:8003/docs"
echo "🗄️  Base de datos: ./data/scaie.db"
echo "📋 Logs: ./data/logs/"
echo "🛑 Para detener: Ctrl+C"
echo "======================================"

# Iniciar backend
cd core/backend/src/scaie
python app/main.py
