from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from typing import List, Optional, Dict, Any
import enum

from ..core.database import Base

class InterestLevel(str, enum.Enum):
    NEW = "nuevo"
    CONTACTED = "contactado"
    INTERESTED = "interesado"
    CONFIRMED = "confirmado"
    NOT_INTERESTED = "no_interesado"

class PlatformType(str, enum.Enum):
    WEB = "web"
    WHATSAPP = "whatsapp"
    TELEGRAM = "telegram"
    FACEBOOK_MESSENGER = "facebook_messenger"
    INSTAGRAM = "instagram"

class Contact(Base):
    __tablename__ = "contacts"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, unique=True, index=True, nullable=True)
    email = Column(String, nullable=True)
    company = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    interest_level = Column(SQLEnum(InterestLevel, native_enum=False), default="nuevo")
    telegram_user_id = Column(String, nullable=True, index=True)  # Campo para Telegram
    whatsapp_user_id = Column(String, nullable=True, index=True)  # Campo para WhatsApp
    facebook_messenger_user_id = Column(String, nullable=True, index=True)  # Campo para Facebook Messenger
    instagram_user_id = Column(String, nullable=True, index=True)  # Campo para Instagram
    platform_user_id = Column(String, nullable=True)  # Campo genérico para otros platforms
    platform = Column(SQLEnum(PlatformType, native_enum=False), default="web")  # Canal de origen
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    
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
            "telegram_user_id": self.telegram_user_id,
            "whatsapp_user_id": self.whatsapp_user_id,
            "facebook_messenger_user_id": self.facebook_messenger_user_id,
            "instagram_user_id": self.instagram_user_id,
            "platform_user_id": self.platform_user_id,
            "platform": self.platform.value if self.platform else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }