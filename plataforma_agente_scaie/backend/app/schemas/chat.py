from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime

class ChatRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    message: str
    phone: Optional[str] = None
    name: Optional[str] = None

class ChatResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    response: str
    contact_id: Optional[int] = None
    message_id: Optional[int] = None

class SandboxRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    message: str
    reset_context: bool = False

class SandboxResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    response: str
    context_info: Optional[Dict[str, Any]] = None