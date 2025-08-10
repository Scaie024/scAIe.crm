from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class MessageBase(BaseModel):
    conversation_id: int
    sender: str
    content: str

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: int
    created_at: datetime
    
    # Pydantic v2 configuration
    model_config = ConfigDict(from_attributes=True)

class ConversationBase(BaseModel):
    contact_id: int
    platform: Optional[str] = "web"

class ConversationCreate(ConversationBase):
    pass

class Conversation(ConversationBase):
    id: int
    created_at: datetime
    messages: List[Message] = []
    
    # Pydantic v2 configuration
    model_config = ConfigDict(from_attributes=True)