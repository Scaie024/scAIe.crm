from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class Message(BaseModel):
    role: str
    content: str

class ContactInfo(BaseModel):
    phone: Optional[str] = None
    name: Optional[str] = None

class ChatRequest(BaseModel):
    message: str
    contact_info: Optional[ContactInfo] = None

class ChatResponse(BaseModel):
    response: str
    contact_id: Optional[int] = None
    message_id: Optional[int] = None

class SandboxRequest(BaseModel):
    message: str
    reset_context: bool = False

class SandboxResponse(BaseModel):
    response: str
    context_info: Dict[str, Any]
# This file makes the directory a Python package
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from ...core.database import get_db
from ...services.llm_service import llm_service
from ...models.conversation import Message
from ...schemas.chat import ChatRequest, ChatResponse, SandboxRequest, SandboxResponse

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Chat with the AI agent.
    """
    try:
        # Process the chat message with the LLM service
        response_data = llm_service.process_chat_message(
            message=request.message,
            phone=request.phone,
            name=request.name,
            db=db
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
            context_info=response_data.get("context_info", {})
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))