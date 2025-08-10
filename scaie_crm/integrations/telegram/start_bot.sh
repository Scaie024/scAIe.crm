#!/bin/bash

# Script para iniciar el bot de Telegram
echo "🤖 Iniciando Bot de Telegram..."

# Verificar ubicación
if [ ! -f "../../.env" ]; then
    echo "❌ Error: No se encontró .env en la raíz del proyecto"
    exit 1
fi

# Activar entorno virtual
cd ../../
source venv/bin/activate

# Verificar token
if ! grep -q "TELEGRAM_BOT_TOKEN=" .env || grep -q "TELEGRAM_BOT_TOKEN=$" .env; then
    echo "❌ Error: TELEGRAM_BOT_TOKEN no configurado en .env"
    exit 1
fi

echo "✅ Token encontrado"
echo "🚀 Iniciando bot..."

# Iniciar bot
cd integrations/telegram
python scai_telegram_bot.py
