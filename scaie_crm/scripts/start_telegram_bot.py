#!/usr/bin/env python3

import asyncio
import sys
import os
import signal
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add backend to path
sys.path.append('backend')

from backend.app.services.telegram_service import telegram_service

# Variable global para controlar la ejecución
running = True

def signal_handler(signum, frame):
    """Manejador de señales para detener el bot limpiamente"""
    global running
    print('\n🛑 Recibida señal de detención...')
    running = False

async def start_telegram_bot():
    """Inicia el bot de Telegram"""
    global running
    
    print("Inicializando bot de Telegram...")
    
    # Registrar manejadores de señales
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        success = await telegram_service.initialize()
        if success:
            print('✅ Bot de Telegram inicializado correctamente')
            print('Iniciando bot de Telegram...')
            
            started = await telegram_service.start()
            if started:
                print('✅ Bot de Telegram iniciado correctamente')
                print('Bot está en ejecución. Presiona Ctrl+C para detener.')
                
                # Mantener el bot en ejecución
                while running:
                    await asyncio.sleep(1)
                
                # Detener el bot limpiamente
                print("Deteniendo bot de Telegram...")
                await telegram_service.stop()
                print("✅ Bot de Telegram detenido correctamente")
            else:
                print('❌ Error al iniciar el bot de Telegram')
                return False
        else:
            print('❌ Error al inicializar el bot de Telegram')
            return False
            
    except Exception as e:
        print(f'❌ Error inesperado: {e}')
        return False
    
    return True

if __name__ == '__main__':
    try:
        result = asyncio.run(start_telegram_bot())
        if not result:
            sys.exit(1)
    except KeyboardInterrupt:
        print('\n🛑 Interrupción por teclado recibida...')
    except Exception as e:
        print(f'\n❌ Error no manejado: {e}')
        sys.exit(1)
    finally:
        print("👋 ¡Hasta luego!")