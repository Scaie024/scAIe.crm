from typing import List, Optional, Dict, Any
from pydantic import BaseModel, ConfigDict

class Message(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    role: str
    content: str

class ContactInfo(BaseModel):
    phone: Optional[str] = None
    name: Optional[str] = None
    company: Optional[str] = None

class ChatRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    message: str
    contact_info: Optional[ContactInfo] = None

class ChatResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    response: str
    contact_id: Optional[int] = None
    message_id: Optional[int] = None

class SandboxRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    message: str
    agent_prompt: Optional[str] = None
    history: Optional[List[Message]] = []

class SandboxResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    response: str
    usage: Optional[Dict[str, Any]] = None