from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.database import Base

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=False)
    platform = Column(String(50), default="web")  # web, whatsapp, messenger
    created_at = Column(DateTime, default=datetime.utcnow)
    # Store conversation context/state in the database
    context = Column(JSON, nullable=True)
    
    # Relationship with messages
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
    
    # Relationship with contact
    contact = relationship("Contact", back_populates="conversations")
    
    def to_dict(self):
        """Convert conversation to dictionary."""
        return {
            "id": self.id,
            "contact_id": self.contact_id,
            "platform": self.platform,
            "context": self.context,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    sender = Column(String(50), nullable=False)  # user, agent
    content = Column(Text, nullable=False)
    metadata_ = Column(JSON, nullable=True)  # Renamed from metadata to avoid Python keyword conflict
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship with conversation
    conversation = relationship("Conversation", back_populates="messages")
    
    def to_dict(self):
        """Convert message to dictionary."""
        return {
            "id": self.id,
            "conversation_id": self.conversation_id,
            "sender": self.sender,
            "content": self.content,
            "metadata": self.metadata_,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }