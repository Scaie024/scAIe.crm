from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class MessageBase(BaseModel):
    content: str
    sender: str

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: int
    conversation_id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

class ConversationBase(BaseModel):
    contact_id: int
    platform: Optional[str] = "web"

class ConversationCreate(ConversationBase):
    pass

class Conversation(ConversationBase):
    id: int
    created_at: datetime
    messages: List[Message] = []
    
    class Config:
        orm_mode = True