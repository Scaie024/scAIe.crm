from sqlalchemy import Column, Integer, String, DateTime, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.database import Base
import enum

# Definir InterestLevel antes de usarlo
class InterestLevel(str, enum.Enum):
    NEW = "nuevo"
    CONTACTED = "contactado"
    INTERESTED = "interesado"
    CONFIRMED = "confirmado"
    NOT_INTERESTED = "no_interesado"

class Contact(Base):
    __tablename__ = "contacts"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    phone = Column(String(20), unique=True, index=True)
    email = Column(String(255), nullable=True)
    company = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    interest_level = Column(Enum(InterestLevel, native_enum=False), default=InterestLevel.NEW)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with conversations
    conversations = relationship("Conversation", back_populates="contact", cascade="all, delete-orphan")
    
    def to_dict(self):
        """Convert contact to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "company": self.company,
            "notes": self.notes,
            "interest_level": self.interest_level.value if self.interest_level else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

class ContactInteraction(Base):
    __tablename__ = "contact_interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=False)
    interaction_type = Column(String(50), nullable=False)  # message_sent, message_received, call_made, etc.
    date = Column(DateTime, default=datetime.utcnow)
    details = Column(Text, nullable=True)