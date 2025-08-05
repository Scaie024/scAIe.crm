from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from ...core.database import get_db
from ...services.omnipotent_agent import omnipotent_agent
from ...models.conversation import Message, Conversation
from ...models.contact import Contact, InterestLevel
from ...schemas.chat import ChatRequest, ChatResponse, SandboxRequest, SandboxResponse
from ...schemas.contact import ContactCreate, ContactUpdate

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Chat with the AI agent specialized in selling the "Sé más eficiente con IA" workshop.
    """
    try:
        # Process the chat message with the omnipotent agent
        response_data = await omnipotent_agent.process_incoming_message(
            message=request.message,
            platform="web",  # Default platform for web chat
            contact_info={
                "name": request.contact_info.name if request.contact_info else "Usuario Web",
                "phone": request.contact_info.phone if request.contact_info else None,
                "email": request.contact_info.email if request.contact_info else None,
                "company": request.contact_info.company if request.contact_info else None,
                "platform_user_id": None  # Not applicable for web chat
            }
        )
        
        return ChatResponse(
            response=response_data["response"],
            contact_id=response_data["contact_id"],
            message_id=response_data["message_id"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sandbox", response_model=SandboxResponse)
async def sandbox_endpoint(request: SandboxRequest):
    """
    Sandbox endpoint for testing prompts and agent behavior.
    """
    try:
        response_data = llm_service.process_sandbox_message(
            message=request.message,
            reset_context=request.reset_context
        )
        
        return SandboxResponse(
            response=response_data["response"],
            metadata=response_data.get("metadata", {})
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))