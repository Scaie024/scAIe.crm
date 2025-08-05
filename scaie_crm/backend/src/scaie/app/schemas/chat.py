from typing import List, Optional, Dict, Any
from pydantic import BaseModel, ConfigDict

class Message(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    role: str
    content: str

class ChatRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    message: str
    history: Optional[List[Message]] = []
    contact_name: Optional[str] = None

class ChatResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    response: str

class SandboxRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    message: str
    agent_prompt: Optional[str] = None
    history: Optional[List[Message]] = []

class SandboxResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    response: str
    usage: Optional[Dict[str, Any]] = None