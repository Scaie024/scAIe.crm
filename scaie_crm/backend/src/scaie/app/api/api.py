from fastapi import APIRouter

from .endpoints import (
    agent, 
    auth, 
    chat, 
    contacts, 
    conversations, 
    dashboard,
    messaging  # Nuevo endpoint
)

api_router = APIRouter()
api_router.include_router(agent.router)
api_router.include_router(auth.router)
api_router.include_router(chat.router)
api_router.include_router(contacts.router)
api_router.include_router(conversations.router)
api_router.include_router(dashboard.router)
api_router.include_router(messaging.router)  # Nuevo endpoint