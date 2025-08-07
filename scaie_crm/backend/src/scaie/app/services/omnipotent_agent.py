import re
import logging
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from sqlalchemy.exc import SQLAlchemyError

from ..core.database import get_db
from ..models.contact import Contact, InterestLevel, PlatformType
from ..models.conversation import Conversation, Message
from ..models.agent_action import AgentAction, AgentTask
from ..services.llm_service import llm_service
from ..services.scaie_knowledge import scaie_knowledge
from ..services.workshop_knowledge import workshop_knowledge_instance

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class OmnipotentAgent:
    def __init__(self):
        pass
    
    async def process_incoming_message(self, message: str, platform: str, contact_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process an incoming message and determine appropriate actions.
        """
        db_gen = get_db()
        db = next(db_gen)
        
        user_message = None
        ai_message = None
        
        try:
            # Get or create contact
            contact = self._get_or_create_contact(db, contact_info, platform)
            logger.info(f"Contact created/retrieved: ID {contact.id}")
            
            # Create or get conversation
            conversation = self._get_or_create_conversation(db, contact.id, platform)
            logger.info(f"Conversation created/retrieved: ID {conversation.id}")
            
            # Save user message
            try:
                user_message = self._save_message(db, conversation.id, contact.id, "user", message)
                logger.info(f"User message saved: ID {user_message.id}")
            except SQLAlchemyError as e:
                logger.error(f"Database error saving user message: {str(e)}")
                db.rollback()
                # Continue anyway since we can still generate a response
            
            # Generate response using LLM
            try:
                response_text = await self._generate_response(db, message, contact, conversation)
            except Exception as e:
                logger.error(f"Error generating response: {str(e)}")
                response_text = "Lo siento, estoy teniendo dificultades técnicas. Por favor, inténtalo de nuevo más tarde."
            
            # Save AI response
            try:
                ai_message = self._save_message(db, conversation.id, contact.id, "ai", response_text)
                logger.info(f"AI message saved: ID {ai_message.id}")
            except SQLAlchemyError as e:
                logger.error(f"Database error saving AI message: {str(e)}")
                db.rollback()
            
            # Update contact interest level based on conversation
            try:
                self._update_contact_interest(db, contact, message, response_text)
            except Exception as e:
                logger.error(f"Error updating contact interest: {str(e)}")
            
            return {
                "response": response_text,
                "contact_id": contact.id,
                "message_id": ai_message.id if ai_message else None
            }
            
        except Exception as e:
            logger.error(f"Error processing incoming message: {str(e)}")
            # Ensure database session is closed even if an error occurs
            try:
                db.close()
            except:
                pass
            raise
        finally:
            try:
                db.close()
            except:
                pass
    
    def _get_or_create_contact(self, db: Session, contact_info: Dict[str, Any], platform: str) -> Contact:
        """
        Get existing contact or create a new one based on platform-specific identifiers.
        """
        contact = None
        
        # Try to find contact based on platform-specific identifiers
        if platform == "telegram" and contact_info.get("platform_user_id"):
            contact = db.query(Contact).filter(
                Contact.telegram_user_id == contact_info["platform_user_id"]
            ).first()
        elif platform == "whatsapp" and contact_info.get("platform_user_id"):
            contact = db.query(Contact).filter(
                Contact.whatsapp_user_id == contact_info["platform_user_id"]
            ).first()
        elif platform == "facebook_messenger" and contact_info.get("platform_user_id"):
            contact = db.query(Contact).filter(
                Contact.facebook_messenger_user_id == contact_info["platform_user_id"]
            ).first()
        elif platform == "instagram" and contact_info.get("platform_user_id"):
            contact = db.query(Contact).filter(
                Contact.instagram_user_id == contact_info["platform_user_id"]
            ).first()
        
        # If not found by platform ID, try to find by phone or email
        if not contact and (contact_info.get("phone") or contact_info.get("email")):
            contact = db.query(Contact).filter(
                or_(
                    Contact.phone == contact_info.get("phone"),
                    Contact.email == contact_info.get("email")
                )
            ).first()
        
        # Create new contact if not found
        if not contact:
            platform_type_map = {
                "web": PlatformType.WEB,
                "telegram": PlatformType.TELEGRAM,
                "whatsapp": PlatformType.WHATSAPP,
                "facebook_messenger": PlatformType.FACEBOOK_MESSENGER,
                "instagram": PlatformType.INSTAGRAM
            }
            
            contact = Contact(
                name=contact_info.get("name", "Usuario desconocido"),
                phone=contact_info.get("phone"),
                email=contact_info.get("email"),
                company=contact_info.get("company"),
                platform=platform_type_map.get(platform, PlatformType.WEB)
            )
            
            # Set platform-specific user ID
            if platform == "telegram" and contact_info.get("platform_user_id"):
                contact.telegram_user_id = contact_info["platform_user_id"]
            elif platform == "whatsapp" and contact_info.get("platform_user_id"):
                contact.whatsapp_user_id = contact_info["platform_user_id"]
            elif platform == "facebook_messenger" and contact_info.get("platform_user_id"):
                contact.facebook_messenger_user_id = contact_info["platform_user_id"]
            elif platform == "instagram" and contact_info.get("platform_user_id"):
                contact.instagram_user_id = contact_info["platform_user_id"]
            
            db.add(contact)
            db.commit()
            db.refresh(contact)
        else:
            # Update existing contact with new information if provided
            if contact_info.get("name") and contact.name == "Usuario desconocido":
                contact.name = contact_info["name"]
            
            if contact_info.get("phone") and not contact.phone:
                contact.phone = contact_info["phone"]
                
            if contact_info.get("email") and not contact.email:
                contact.email = contact_info["email"]
                
            if contact_info.get("company") and not contact.company:
                contact.company = contact_info["company"]
            
            # Update platform-specific user ID if not set
            if platform == "telegram" and contact_info.get("platform_user_id") and not contact.telegram_user_id:
                contact.telegram_user_id = contact_info["platform_user_id"]
            elif platform == "whatsapp" and contact_info.get("platform_user_id") and not contact.whatsapp_user_id:
                contact.whatsapp_user_id = contact_info["platform_user_id"]
            elif platform == "facebook_messenger" and contact_info.get("platform_user_id") and not contact.facebook_messenger_user_id:
                contact.facebook_messenger_user_id = contact_info["platform_user_id"]
            elif platform == "instagram" and contact_info.get("platform_user_id") and not contact.instagram_user_id:
                contact.instagram_user_id = contact_info["platform_user_id"]
            
            db.commit()
        
        return contact
    
    def _get_or_create_conversation(self, db: Session, contact_id: int, platform: str) -> Conversation:
        """
        Get existing conversation or create a new one.
        """
        platform_type_map = {
            "web": PlatformType.WEB,
            "telegram": PlatformType.TELEGRAM,
            "whatsapp": PlatformType.WHATSAPP,
            "facebook_messenger": PlatformType.FACEBOOK_MESSENGER,
            "instagram": PlatformType.INSTAGRAM
        }
        
        conversation = db.query(Conversation).filter(
            and_(
                Conversation.contact_id == contact_id,
                Conversation.platform == platform_type_map.get(platform, PlatformType.WEB)
            )
        ).first()
        
        if not conversation:
            conversation = Conversation(
                contact_id=contact_id,
                platform=platform_type_map.get(platform, PlatformType.WEB)
            )
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
        
        return conversation
    
    def _save_message(self, db: Session, conversation_id: int, contact_id: int, role: str, content: str) -> Message:
        """
        Save a message to the database.
        """
        message = Message(
            conversation_id=conversation_id,
            contact_id=contact_id,
            sender=role,  # Changed from 'role' to 'sender'
            content=content
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        return message
    
    async def _generate_response(self, db: Session, message: str, contact: Contact, conversation: Conversation) -> str:
        """
        Generate a response using the LLM service.
        """
        response_data = await llm_service.generate_response(message, contact)
        if response_data.get("success"):
            return response_data["response"]
        else:
            logger.error(f"LLM service error: {response_data.get('error')}")
            return "Lo siento, estoy teniendo dificultades técnicas. Por favor, inténtalo de nuevo más tarde o comunícate al 5535913417."
    
    def _update_contact_interest(self, db: Session, contact: Contact, user_message: str, ai_response: str):
        """
        Update contact interest level based on conversation content.
        """
        # This is a simplified implementation. In a real-world scenario,
        # you would use more sophisticated NLP techniques to determine interest level.
        
        positive_keywords = [
            "interesado", "interesada", "quiero", "necesito", "me gusta", 
            "agendar", "cita", "llamada", "información", "detalles"
        ]
        
        negative_keywords = [
            "no", "no gracias", "no estoy interesado", "no me interesa",
            "ocupado", "después", "otro momento"
        ]
        
        user_message_lower = user_message.lower()
        
        # Check for explicit interest signals
        if any(keyword in user_message_lower for keyword in positive_keywords):
            if contact.interest_level == InterestLevel.NEW:
                contact.interest_level = InterestLevel.CONTACTED
            elif contact.interest_level == InterestLevel.CONTACTED:
                contact.interest_level = InterestLevel.INTERESTED
        
        # Check for disinterest signals
        if any(keyword in user_message_lower for keyword in negative_keywords):
            contact.interest_level = InterestLevel.NOT_INTERESTED
        
        try:
            db.commit()
        except Exception as e:
            logger.error(f"Error updating contact interest: {str(e)}")
            db.rollback()

# Create singleton instance
omnipotent_agent = OmnipotentAgent()