from typing import List, Optional, Dict, Any
from pydantic import BaseModel, ConfigDict, field_validator, model_validator

class Message(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    role: str
    content: str

class ContactInfo(BaseModel):
    phone: Optional[str] = None
    name: Optional[str] = None
    company: Optional[str] = None
    email: Optional[str] = None

    # Normalize empty strings to None
    @field_validator('phone', 'name', 'company', 'email', mode='before')
    def _empty_to_none(cls, v):
        if v is None:
            return None
        try:
            s = str(v).strip()
        except Exception:
            return v
        return s or None

class ChatRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    message: str
    # Preferred
    contact_info: Optional[ContactInfo] = None
    # Legacy support (frontend may still send this)
    customer_info: Optional[ContactInfo] = None

    @model_validator(mode="after")
    def _unify_contact_info(self):
        if not self.contact_info and self.customer_info:
            self.contact_info = self.customer_info
        return self

class ChatResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    response: str
    contact_id: Optional[int] = None
    message_id: Optional[int] = None

class SandboxRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    message: str
    reset_context: Optional[bool] = False

class SandboxResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    response: str
    metadata: Optional[Dict[str, Any]] = None