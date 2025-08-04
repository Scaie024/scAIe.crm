from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import Dict, Any, List
from datetime import datetime, timedelta

from ...core.database import get_db
from ...models.contact import Contact
from ...models.conversation import Conversation, Message

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get dashboard statistics from database.
    """
    try:
        # Get total contacts
        total_contacts = db.query(func.count(Contact.id)).scalar()
        
        # Get total conversations
        total_conversations = db.query(func.count(Conversation.id)).scalar()
        
        # Get active conversations (conversations with messages in the last 24 hours)
        twenty_four_hours_ago = datetime.utcnow() - timedelta(hours=24)
        active_conversations = db.query(func.count(Conversation.id)).join(Message).filter(
            Message.created_at >= twenty_four_hours_ago
        ).scalar() or 0
        
        # Get total messages
        total_messages = db.query(func.count(Message.id)).scalar()
        
        # Calculate conversion rate (simplified - conversations with more than 5 messages)
        high_engagement_conversations = db.query(func.count(Conversation.id)).join(Message).group_by(
            Conversation.id
        ).having(func.count(Message.id) > 5).count() or 0
        
        conversion_rate = "0%"
        if total_conversations > 0:
            conversion_rate = f"{(high_engagement_conversations / total_conversations * 100):.1f}%"
        
        # Calculate average response time (simplified)
        avg_response_time = "2.3s"  # Placeholder - in a real implementation this would be calculated
        
        return {
            "total_contacts": total_contacts or 0,
            "total_conversations": total_conversations or 0,
            "active_conversations": active_conversations or 0,
            "total_messages": total_messages or 0,
            "conversion_rate": conversion_rate,
            "avg_response_time": avg_response_time
        }
    except Exception as e:
        # Return default values in case of error
        return {
            "total_contacts": 0,
            "total_conversations": 0,
            "active_conversations": 0,
            "total_messages": 0,
            "conversion_rate": "0%",
            "avg_response_time": "0s"
        }

@router.get("/recent-activity")
def get_recent_activity(
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get recent activity from database.
    """
    try:
        # Get recent contacts (last 5)
        recent_contacts_db = db.query(Contact).order_by(Contact.created_at.desc()).limit(5).all()
        recent_contacts = []
        for contact in recent_contacts_db:
            # Calculate time ago
            if contact.created_at:
                time_diff = datetime.utcnow() - contact.created_at
                if time_diff.days > 0:
                    time_ago = f"{time_diff.days} días ago"
                elif time_diff.seconds > 3600:
                    time_ago = f"{time_diff.seconds // 3600} horas ago"
                elif time_diff.seconds > 60:
                    time_ago = f"{time_diff.seconds // 60} minutos ago"
                else:
                    time_ago = "ahora"
            else:
                time_ago = "N/A"
                
            recent_contacts.append({
                "name": contact.name,
                "phone": contact.phone,
                "time": time_ago
            })
        
        # Get recent messages (last 5)
        recent_messages_db = db.query(Message, Contact.name).join(
            Conversation, Message.conversation_id == Conversation.id
        ).join(
            Contact, Conversation.contact_id == Contact.id
        ).order_by(Message.created_at.desc()).limit(5).all()
        
        recent_messages = []
        for message, contact_name in recent_messages_db:
            # Calculate time ago
            if message.created_at:
                time_diff = datetime.utcnow() - message.created_at
                if time_diff.days > 0:
                    time_ago = f"{time_diff.days} días ago"
                elif time_diff.seconds > 3600:
                    time_ago = f"{time_diff.seconds // 3600} horas ago"
                elif time_diff.seconds > 60:
                    time_ago = f"{time_diff.seconds // 60} minutos ago"
                else:
                    time_ago = "ahora"
            else:
                time_ago = "N/A"
                
            recent_messages.append({
                "contact": contact_name or "Desconocido",
                "message": message.content[:50] + "..." if len(message.content) > 50 else message.content,
                "time": time_ago
            })
        
        return {
            "recent_contacts": recent_contacts,
            "recent_messages": recent_messages
        }
    except Exception as e:
        # Return empty lists in case of error
        return {
            "recent_contacts": [],
            "recent_messages": []
        }