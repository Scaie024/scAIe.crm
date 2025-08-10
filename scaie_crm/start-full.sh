#!/bin/bash

# Script para iniciar SCAIE completo: Backend + Bot Telegram
echo "🚀 SCAIE - Sistema Completo"
echo "============================"

# Verificar ubicación
if [ ! -f ".env" ]; then
    echo "❌ Error: Ejecuta desde la raíz del proyecto scaie_crm/"
    exit 1
fi

# Función para cleanup
cleanup() {
    echo ""
    echo "🛑 Deteniendo servicios..."
    pkill -f "python.*main.py" 2>/dev/null
    pkill -f "python.*scai_telegram_bot.py" 2>/dev/null
    echo "✅ Servicios detenidos"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Activar entorno virtual
source venv/bin/activate

# Verificar que el bot token está configurado
if ! grep -q "TELEGRAM_BOT_TOKEN=" .env || grep -q "TELEGRAM_BOT_TOKEN=$" .env; then
    echo "⚠️  TELEGRAM_BOT_TOKEN no configurado - solo backend será iniciado"
    TELEGRAM_ENABLED=false
else
    TELEGRAM_ENABLED=true
fi

# Iniciar backend
echo "🌐 Iniciando Backend..."
cd core/backend/src/scaie
python app/main.py &
BACKEND_PID=$!

sleep 3

# Iniciar bot solo si está configurado
if [ "$TELEGRAM_ENABLED" = true ]; then
    echo "🤖 Iniciando Bot de Telegram..."
    cd ../../../../integrations/telegram
    python scai_telegram_bot.py &
    BOT_PID=$!
    BOT_STATUS="✅ Activo"
else
    BOT_STATUS="⚠️  Token no configurado"
fi

echo ""
echo "✅ SCAIE Sistema Iniciado"
echo "========================="
echo "🌐 Backend:    http://localhost:8003"
echo "📖 API Docs:   http://localhost:8003/docs"
echo "🤖 Telegram:   $BOT_STATUS"
echo "🗄️  Database:   ./data/scaie.db"
echo "========================="
echo "🛑 Presiona Ctrl+C para detener"
echo ""

# Mantener corriendo
wait
