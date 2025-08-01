from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os

from ...services.llm_service import llm_service

router = APIRouter(prefix="/chat", tags=["chat"])

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    context: Optional[dict] = None

class ChatResponse(BaseModel):
    response: str
    context: Optional[dict] = None

@router.post("/", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    """
    Chat with the AI agent.
    """
    try:
        # Get the last user message
        user_message = None
        for message in reversed(request.messages):
            if message.role == "user":
                user_message = message.content
                break
        
        if not user_message:
            raise HTTPException(status_code=400, detail="No user message found")
        
        # Get response from LLM service
        response_data = await llm_service.generate_response(user_message)
        response_text = response_data.get("response", "Lo siento, no puedo procesar tu solicitud en este momento.")
        
        return ChatResponse(
            response=response_text
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))