from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from ...core.database import get_db
from ...models.contact import Contact, InterestLevel
from ...models.conversation import Conversation, Message

router = APIRouter(prefix="/agent", tags=["agent"])

@router.get("/stats")
async def get_agent_stats(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Get agent statistics.
    """
    # Count total contacts
    total_contacts = db.query(Contact).count()
    
    # Count contacts by interest level
    interest_level_counts = {}
    for level in InterestLevel:
        count = db.query(Contact).filter(Contact.interest_level == level).count()
        interest_level_counts[level.value] = count
    
    # Count total conversations
    total_conversations = db.query(Conversation).count()
    
    # Count total messages
    total_messages = db.query(Message).count()
    
    # Count messages by sender
    user_messages = db.query(Message).filter(Message.sender == "user").count()
    agent_messages = db.query(Message).filter(Message.sender == "agent").count()
    
    return {
        "total_contacts": total_contacts,
        "interest_level_distribution": interest_level_counts,
        "total_conversations": total_conversations,
        "total_messages": total_messages,
        "message_distribution": {
            "user": user_messages,
            "agent": agent_messages
        }
    }