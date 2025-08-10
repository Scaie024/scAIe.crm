"""
Endpoint de Telegram para integrar en el servidor FastAPI principal
Este archivo debe importarse en main.py para añadir el endpoint webhook
"""

from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from typing import Dict, Any, Optional
import logging
import os
import asyncio
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

logger = logging.getLogger(__name__)

# Crear router para Telegram
telegram_router = APIRouter(prefix="/webhook", tags=["telegram"])

# Configuración de Telegram
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Importar servicios
try:
    # Use absolute import to avoid relative path issues
    from app.services.omnipotent_agent import omnipotent_agent
    AGENT_AVAILABLE = True
except ImportError:
    logger.warning("Agente omnipotente no disponible")
    AGENT_AVAILABLE = False

# Modelos Pydantic para Telegram
class TelegramUser(BaseModel):
    id: int
    first_name: str
    username: Optional[str] = None
    is_bot: bool = False

class TelegramChat(BaseModel):
    id: int
    type: str

class TelegramMessage(BaseModel):
    message_id: int
    date: int
    chat: TelegramChat
    from_: Optional[TelegramUser] = Field(default=None, alias="from")
    text: Optional[str] = None
    
    # Pydantic v2 aliasing
    model_config = ConfigDict(populate_by_name=True)

    # 'from_' will be populated from JSON key 'from'

class TelegramUpdate(BaseModel):
    update_id: int
    message: Optional[TelegramMessage] = None
    edited_message: Optional[TelegramMessage] = None

@telegram_router.post("/{token}")
async def telegram_webhook(token: str, update: TelegramUpdate, request: Request):
    """
    Webhook para recibir actualizaciones de Telegram.
    """
    # Verificar que el token coincida
    if token != TELEGRAM_BOT_TOKEN:
        raise HTTPException(status_code=403, detail="Token inválido")
    
    # Procesar mensaje
    message = update.message or update.edited_message
    if not message or not message.text:
        raise HTTPException(status_code=400, detail="Mensaje inválido")
    
    # Obtener información del contacto
    contact_info = {
        "name": message.from_.first_name,
        "platform_user_id": str(message.from_.id),
        "platform": "telegram"
    }
    
    try:
        # Enviar al servicio del agente
        response_data = await omnipotent_agent.process_incoming_message(
            message=message.text,
            platform="telegram",
            contact_info=contact_info
        )
        
        # Enviar respuesta
        async with httpx.AsyncClient() as client:
            await client.post(
                f"https://api.telegram.org/bot{token}/sendMessage",
                json={
                    "chat_id": message.chat.id,
                    "text": response_data["response"],
                    "reply_to_message_id": message.message_id
                }
            )
        
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Error procesando mensaje de Telegram: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# No hay cambios necesarios en esta función para la implementación del webhook

@telegram_router.get("/telegram/status")
async def telegram_status():
    """
    Verificar el estado del bot de Telegram
    """
    if not TELEGRAM_BOT_TOKEN:
        return {"status": "error", "message": "Token no configurado"}
    
    import httpx
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMe"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            if response.status_code == 200:
                bot_info = response.json()["result"]
                return {
                    "status": "active",
                    "bot": {
                        "id": bot_info["id"],
                        "username": bot_info["username"],
                        "first_name": bot_info["first_name"]
                    },
                    "agent_available": AGENT_AVAILABLE
                }
            else:
                return {"status": "error", "message": "No se pudo conectar con Telegram"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

# Función para configurar webhook (usar solo en producción)
async def setup_telegram_webhook(webhook_url: str):
    """
    Configurar webhook de Telegram
    """
    if not TELEGRAM_BOT_TOKEN:
        logger.error("Token de Telegram no configurado")
        return False
    
    import httpx
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook"
    payload = {"url": webhook_url}
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload)
            if response.status_code == 200:
                logger.info(f"✅ Webhook configurado: {webhook_url}")
                return True
            else:
                logger.error(f"❌ Error configurando webhook: {response.text}")
                return False
        except Exception as e:
            logger.error(f"❌ Error: {e}")
            return False
