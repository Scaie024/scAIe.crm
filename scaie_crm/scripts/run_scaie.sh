#!/bin/bash

# Script para ejecutar SCAIE fácilmente
echo "🚀 Iniciando SCAIE - Sistema Agente..."
echo "======================================"

# Cambiar al directorio del proyecto
cd "$(dirname "$0")/.."

# Verificar si el entorno virtual existe
if [ ! -d "venv" ]; then
    echo "❌ Entorno virtual no encontrado. Creando..."
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r core/backend/requirements.txt
    if [ -f "core/backend/dev-requirements.txt" ]; then
        pip install -r core/backend/dev-requirements.txt
    fi
    pip install dashscope "python-jose[cryptography]" bcrypt
    echo "✅ Entorno virtual creado e instalado"
else
    echo "✅ Entorno virtual encontrado"
fi

# Activar entorno virtual
source venv/bin/activate

# Verificar que la base de datos esté inicializada
echo "🗄️  Verificando base de datos..."
cd core/backend/src/scaie
python init_db.py

# Ejecutar la aplicación
# Habilitar LLM por defecto; para desactivar exporta DISABLE_LLM=true antes de correr
export DISABLE_LLM=${DISABLE_LLM:-false}
if [ "$DISABLE_LLM" = "true" ]; then LLM_STATUS="OFF"; else LLM_STATUS="ON"; fi
echo "🌐 Iniciando servidor en http://localhost:8003 (LLM $LLM_STATUS)"
echo "📖 Documentación de API: http://localhost:8003/docs"
echo "🛑 Para detener el servidor: Ctrl+C"
echo "======================================"

python app/main.py
