#!/bin/bash

# Script para ejecutar SCAIE completo: Backend + Bot de Telegram
echo "🚀 Iniciando SCAIE Sistema Completo..."
echo "====================================="

# Cambiar al directorio del proyecto
cd "$(dirname "$0")/.."

# Verificar entorno virtual
if [ ! -d "venv" ]; then
    echo "❌ Entorno virtual no encontrado. Ejecuta primero: ./run_scaie.sh"
    exit 1
fi

# Función para manejar la terminación
cleanup() {
    echo ""
    echo "🛑 Deteniendo servicios..."
    
    # Matar procesos de SCAIE
    pkill -f "python.*app/main.py" 2>/dev/null
    pkill -f "python.*scai_telegram_bot.py" 2>/dev/null
    
    echo "✅ Servicios detenidos"
    exit 0
}

# Configurar trap para Ctrl+C
trap cleanup SIGINT SIGTERM

# Activar entorno virtual
source venv/bin/activate

echo "🌐 Iniciando Backend..."
cd core/backend/src/scaie
# Habilitar LLM por defecto en modo completo
export DISABLE_LLM=${DISABLE_LLM:-false}
python app/main.py &
BACKEND_PID=$!

# Esperar a que el backend esté listo
sleep 3

echo "🤖 Iniciando Bot de Telegram..."
cd ../../../../integrations/telegram
python scai_telegram_bot.py &
BOT_PID=$!

echo ""
echo "✅ Sistema SCAIE iniciado correctamente"
echo "====================================="
echo "🌐 Backend:   http://localhost:8003"
echo "📖 API Docs:  http://localhost:8003/docs"
echo "🤖 Bot:       @scAIebot (https://t.me/scAIebot)"
echo "====================================="
echo "🛑 Presiona Ctrl+C para detener todos los servicios"
echo ""

# Mantener el script corriendo
wait
