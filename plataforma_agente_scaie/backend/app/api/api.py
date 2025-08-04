from fastapi import APIRouter

from .endpoints import chat, contacts, conversations, dashboard, agent

api_router = APIRouter()
api_router.include_router(chat.router)
api_router.include_router(contacts.router)
api_router.include_router(conversations.router)
api_router.include_router(dashboard.router)
api_router.include_router(agent.router)