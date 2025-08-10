from fastapi import APIRouter

from .endpoints import (
    agent, 
    auth, 
    chat, 
    contacts, 
    conversations, 
    dashboard,
    omnipotent_agent,
    messaging,  # Endpoint existente
    telegram_webhook,  # Nuevo endpoint para Telegram
    whatsapp_webhook,   # Nuevo endpoint para WhatsApp
    debug,
    sandbox,  # Nuevo endpoint para sandbox
    knowledge  # Nuevo endpoint para gestión de conocimiento
)

api_router = APIRouter()
api_router.include_router(agent.router)
api_router.include_router(auth.router)
api_router.include_router(chat.router)
api_router.include_router(contacts.router)
api_router.include_router(conversations.router)
api_router.include_router(dashboard.router)
api_router.include_router(omnipotent_agent.router)
api_router.include_router(messaging.router)  # Endpoint existente
api_router.include_router(telegram_webhook.telegram_router)  # Nuevo endpoint para Telegram
api_router.include_router(whatsapp_webhook.whatsapp_router)  # Nuevo endpoint para WhatsApp
api_router.include_router(debug.router)  # Debug endpoints
api_router.include_router(sandbox.router)  # Sandbox endpoints
api_router.include_router(knowledge.router)  # Knowledge management endpoints