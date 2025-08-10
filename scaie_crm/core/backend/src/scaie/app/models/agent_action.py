from sqlalchemy import Column, Integer, String, DateTime, Text, Enum, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.database import Base
import enum

class ActionType(str, enum.Enum):
    SEND_MESSAGE = "send_message"
    CREATE_CONTACT = "create_contact"
    UPDATE_CONTACT = "update_contact"
    SCHEDULE_APPOINTMENT = "schedule_appointment"
    SEND_MATERIAL = "send_material"
    GENERATE_QUOTE = "generate_quote"
    ESCALATE_TO_HUMAN = "escalate_to_human"
    UPDATE_INTEREST_LEVEL = "update_interest_level"
    IMPORT_CONTACTS = "import_contacts"
    EXPORT_CONTACTS = "export_contacts"
    DELETE_CONTACT = "delete_contact"
    SEARCH_CONTACTS = "search_contacts"
    GET_CONTACT_DETAILS = "get_contact_details"
    SEND_EMAIL = "send_email"
    CREATE_TASK = "create_task"
    UPDATE_TASK = "update_task"
    COMPLETE_TASK = "complete_task"

class AgentAction(Base):
    __tablename__ = "agent_actions"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    action_type = Column(Enum(ActionType, native_enum=False), nullable=False)
    parameters = Column(JSON, nullable=True)
    result = Column(JSON, nullable=True)
    status = Column(String(50), default="pending")  # pending, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    executed_at = Column(DateTime, nullable=True)
    
    # Relationships will be defined after all classes are declared
    
    def to_dict(self):
        """Convert agent action to dictionary."""
        return {
            "id": self.id,
            "conversation_id": self.conversation_id,
            "action_type": self.action_type.value if self.action_type else None,
            "parameters": self.parameters,
            "result": self.result,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "executed_at": self.executed_at.isoformat() if self.executed_at else None
        }

class AgentTask(Base):
    __tablename__ = "agent_tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="pending")  # pending, in_progress, completed, failed
    priority = Column(String(50), default="medium")  # low, medium, high
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships will be defined after all classes are declared
    
    def to_dict(self):
        """Convert agent task to dictionary."""
        return {
            "id": self.id,
            "contact_id": self.contact_id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }