import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

import re
import logging
from typing import Dict, List, Any, Optional, cast
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel

from ..core.database import get_db
from ..models.contact import Contact, InterestLevel, PlatformType
from ..models.conversation import Conversation, Message
from ..models.agent_action import AgentAction, AgentTask
from ..services.llm_service import llm_service
from ..services.scaie_knowledge import scaie_knowledge
from ..services.workshop_knowledge import workshop_knowledge_instance
from ..api.endpoints.contacts import ContactCreate

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class OmnipotentAgent:
    def __init__(self):
        self.llm_service = llm_service
        self.scaie_knowledge = scaie_knowledge
        self.workshop_knowledge = workshop_knowledge_instance
        
    async def process_incoming_message(self, message: str, platform: str, contact_info: Dict[str, Any], db: Optional[Session] = None) -> Dict[str, Any]:
        """
        Process an incoming message and determine appropriate actions.
        """
        created_session = False
        if db is None:
            db_gen = get_db()
            db = next(db_gen)
            created_session = True
        
        user_message = None
        ai_message = None
        
        try:
            # Get or create contact
            contact = self._get_or_create_contact(db, contact_info, platform)
            logger.info(f"Contact created/retrieved: ID {contact.id}")
            
            # Create or get conversation
            conversation = self._get_or_create_conversation(db, contact.id, platform)  # type: ignore[arg-type]
            logger.info(f"Conversation created/retrieved: ID {conversation.id}")
            
            # Save user message
            try:
                user_message = self._save_message(db, conversation.id, contact.id, "user", message)  # type: ignore[arg-type]
                logger.info(f"User message saved: ID {user_message.id}")
            except SQLAlchemyError as e:
                logger.error(f"Database error saving user message: {str(e)}")
                db.rollback()
                # Continue anyway since we can still generate a response
            
            # Generate response using LLM
            try:
                response_text = await self._generate_response(db, message, contact, conversation)
            except Exception as e:
                logger.error(f"Error generating response: {str(e)}", exc_info=True)
                response_text = "Lo siento, estoy teniendo dificultades técnicas. Por favor, inténtalo de nuevo más tarde."
                
            # Save agent (AI) response
            try:
                # Use consistent sender label 'agent' across the codebase
                ai_message = self._save_message(db, conversation.id, contact.id, "agent", response_text)  # type: ignore[arg-type]
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
            if created_session:
                try:
                    db.close()
                except:
                    pass
            raise
        finally:
            if created_session:
                try:
                    db.close()
                except:
                    pass
    
    def _get_or_create_contact(self, db: Session, contact_info: Dict[str, Any], platform: str) -> Contact:
        """
        Get existing contact or create a new one based on platform-specific identifiers.
        Normaliza cadenas vacías a None para no violar UNIQUE(phone) con ''.
        """
        def _norm(v: Any) -> Optional[str]:
            if v is None:
                return None
            s = str(v).strip()
            return s if s else None

        # Normalize inputs
        name = _norm(contact_info.get("name")) or "Usuario desconocido"
        phone = _norm(contact_info.get("phone"))
        email = _norm(contact_info.get("email"))
        company = _norm(contact_info.get("company"))
        platform_user_id = _norm(contact_info.get("platform_user_id"))

        # Try platform-specific lookup first
        contact: Optional[Contact] = None
        if platform == "telegram" and platform_user_id:
            contact = db.query(Contact).filter(Contact.telegram_user_id == platform_user_id).first()
        elif platform == "whatsapp" and platform_user_id:
            contact = db.query(Contact).filter(Contact.whatsapp_user_id == platform_user_id).first()
        elif platform == "facebook_messenger" and platform_user_id:
            contact = db.query(Contact).filter(Contact.facebook_messenger_user_id == platform_user_id).first()
        elif platform == "instagram" and platform_user_id:
            contact = db.query(Contact).filter(Contact.instagram_user_id == platform_user_id).first()

        # Fallback lookup by phone/email
        if not contact and (phone or email):
            contact = (
                db.query(Contact)
                .filter(or_(Contact.phone == phone, Contact.email == email))
                .first()
            )

        # Create if not exists
        if not contact:
            platform_type_map = {
                "web": PlatformType.WEB,
                "telegram": PlatformType.TELEGRAM,
                "whatsapp": PlatformType.WHATSAPP,
                "facebook_messenger": PlatformType.FACEBOOK_MESSENGER,
                "instagram": PlatformType.INSTAGRAM,
            }
            contact = Contact(
                name=name,
                phone=phone,
                email=email,
                company=company,
                platform=platform_type_map.get(platform, PlatformType.WEB),
            )
            # Set platform-specific IDs
            if platform == "telegram" and platform_user_id:
                contact.telegram_user_id = platform_user_id
            elif platform == "whatsapp" and platform_user_id:
                contact.whatsapp_user_id = platform_user_id
            elif platform == "facebook_messenger" and platform_user_id:
                contact.facebook_messenger_user_id = platform_user_id
            elif platform == "instagram" and platform_user_id:
                contact.instagram_user_id = platform_user_id

            db.add(contact)
            try:
                db.commit()
            except Exception:
                db.rollback()
                # Handle UNIQUE(phone/email) gracefully
                if phone:
                    existing = db.query(Contact).filter(Contact.phone == phone).first()
                    if existing:
                        contact = existing
                if not contact and email:
                    existing = db.query(Contact).filter(Contact.email == email).first()
                    if existing:
                        contact = existing
                if not contact:
                    # Re-raise if not duplicate on normalized keys
                    raise
            else:
                db.refresh(contact)
        else:
            # Update with new info if empty
            if name and contact.name == "Usuario desconocido":
                contact.name = name
            if phone and not contact.phone:
                contact.phone = phone
            if email and not contact.email:
                contact.email = email
            if company and not contact.company:
                contact.company = company
            # Fill platform-specific IDs if missing
            if platform == "telegram" and platform_user_id and not contact.telegram_user_id:
                contact.telegram_user_id = platform_user_id
            elif platform == "whatsapp" and platform_user_id and not contact.whatsapp_user_id:
                contact.whatsapp_user_id = platform_user_id
            elif platform == "facebook_messenger" and platform_user_id and not contact.facebook_messenger_user_id:
                contact.facebook_messenger_user_id = platform_user_id
            elif platform == "instagram" and platform_user_id and not contact.instagram_user_id:
                contact.instagram_user_id = platform_user_id
            db.commit()

        return cast(Contact, contact)
    
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
        if not llm_service.client:
            logger.error("LLM client not initialized - using fallback response")
            return "Lo siento, el servicio de IA no está disponible en este momento. Por favor, comunícate al 5535913417 para obtener asistencia."

        try:
            response_data = await llm_service.generate_response(message, contact)
            
            if response_data.get("success"):
                return response_data["response"]
            else:
                logger.error(f"LLM service error: {response_data.get('error')}")
                return "Lo siento, estoy teniendo dificultades técnicas. Por favor, inténtalo de nuevo más tarde o comunícate al 5535913417."
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return "Disculpa, estoy teniendo dificultades técnicas. Por favor, inténtalo de nuevo más tarde."
    
    def _update_contact_interest(self, db: Session, contact: Contact, user_message: str, ai_response: str):
        """
        Update contact interest level based on conversation content with enhanced persuasion logic.
        """
        # Enhanced interest detection with more sophisticated patterns
        user_message_lower = user_message.lower()
        
        # Strong interest signals - user explicitly shows interest
        strong_interest_keywords = [
            "interesado", "interesada", "quiero", "necesito", "me gusta", 
            "agendar", "cita", "llamada", "información", "detalles",
            "precio", "costo", "cuanto", "cuánto", "presupuesto",
            "cotización", "cotizacion", "contactar", "asesor",
            "demo", "demostración", "prueba", "muestra", "más info",
            "más información", "hablar", "charlar", "platica", "platicar"
        ]
        
        # Medium interest signals - user shows curiosity or asks specific questions
        medium_interest_keywords = [
            "como funciona", "cómo funciona", "que incluye", "qué incluye",
            "duracion", "duración", "tiempo", "cuanto tiempo", "cuánto tiempo",
            "modalidad", "online", "presencial", "híbrido", "híbrida",
            "equipo", "personas", "participantes", "empresa",
            "resultados", "beneficios", "ventajas", "ayuda",
            "automatizar", "procesos", "tareas", "eficiente"
        ]
        
        # Negative signals - user shows disinterest
        negative_keywords = [
            "no", "no gracias", "no estoy interesado", "no me interesa",
            "ocupado", "después", "otro momento", "no ahora",
            "caro", "muy caro", "costoso", "muy costoso",
            "no puedo", "no es posible", "no tengo"
        ]
        
        # Calendly click or phone number request signals
        calendly_requested = "calendly" in ai_response.lower() or "agendar" in ai_response.lower()
        phone_requested = any(keyword in user_message_lower for keyword in ["teléfono", "telefono", "número", "numero", "whatsapp"])
        
        # Check for explicit interest signals
        has_strong_interest = any(keyword in user_message_lower for keyword in strong_interest_keywords)
        has_medium_interest = any(keyword in user_message_lower for keyword in medium_interest_keywords)
        has_negative_signal = any(keyword in user_message_lower for keyword in negative_keywords)
        
        # Update interest level based on detected signals
        if has_negative_signal and not (has_strong_interest or has_medium_interest):
            contact.interest_level = InterestLevel.NOT_INTERESTED
        elif has_strong_interest or calendly_requested or phone_requested:
            # Strong interest or user requested contact info
            contact.interest_level = InterestLevel.INTERESTED
        elif has_medium_interest:
            # Medium interest - user is curious
            if contact.interest_level == InterestLevel.NEW:
                contact.interest_level = InterestLevel.CONTACTED
            elif contact.interest_level == InterestLevel.CONTACTED:
                # If already contacted and showing continued interest, move to interested
                contact.interest_level = InterestLevel.INTERESTED
        
        # Additional logic for persuasion - if user has been contacted and shows continued interest
        if (contact.interest_level == InterestLevel.CONTACTED and 
            (has_strong_interest or has_medium_interest)):
            # Move to interested if they continue showing interest
            contact.interest_level = InterestLevel.INTERESTED
            
        try:
            db.commit()
        except Exception as e:
            logger.error(f"Error updating contact interest: {str(e)}")
            db.rollback()

    # ---- Simple helper endpoints used by API ----
    def execute_pending_actions(self, conversation_id: int, db: Optional[Session] = None) -> List[Dict[str, Any]]:
        """Stub that returns an empty list for pending actions execution."""
        # In a full implementation, this would fetch AgentAction rows and execute them.
        return []

    def get_contact_summary(self, contact_id: int, db: Optional[Session] = None) -> Dict[str, Any]:
        """Return a minimal contact summary for the API contract."""
        created_session = False
        if db is None:
            db_gen = get_db()
            db = next(db_gen)
            created_session = True
        try:
            contact = db.query(Contact).filter(Contact.id == contact_id).first()
            if not contact:
                return {"error": "Contacto no encontrado"}
            conversations_count = db.query(Conversation).filter(Conversation.contact_id == contact_id).count()
            # For simplicity, tasks and actions not implemented here
            return {
                "contact": contact.to_dict(),
                "conversations_count": conversations_count,
                "tasks": [],
                "recent_actions": [],
            }
        finally:
            if created_session:
                try:
                    db.close()
                except:
                    pass

    def search_contacts(self, query: str, db: Optional[Session] = None) -> List[Dict[str, Any]]:
        """Basic contact search by name, phone, email, or company."""
        created_session = False
        if db is None:
            db_gen = get_db()
            db = next(db_gen)
            created_session = True
        try:
            q = f"%{query}%"
            results = (
                db.query(Contact)
                .filter(
                    or_(
                        Contact.name.ilike(q),
                        Contact.phone.ilike(q),
                        Contact.email.ilike(q),
                        Contact.company.ilike(q),
                    )
                )
                .all()
            )
            return [c.to_dict() for c in results]
        finally:
            if created_session:
                try:
                    db.close()
                except:
                    pass

# Create singleton instance
omnipotent_agent = OmnipotentAgent()


async def process_message(
    db: Session,
    message_text: str,
    contact_info: Optional[Any] = None,
    conversation_id: Optional[int] = None
) -> Dict[str, Any]:
    """
    Process incoming message from any channel.
    
    Args:
        db: Database session
        message_text: Message text from user
        contact_info: Optional contact information (can be ContactCreate or dict)
        conversation_id: Optional conversation ID
    """
    try:
        # Convert contact_info to ContactCreate if it's a dict
        if contact_info and isinstance(contact_info, dict):
            # Map fields from ContactInfo (message schema) to ContactCreate (contact schema)
            contact_dict = {
                "name": contact_info.get("name", "Usuario desconocido"),
                "phone": contact_info.get("phone"),
                "email": contact_info.get("email"),
                "company": contact_info.get("company"),
                "interest_level": contact_info.get("interest_level", "nuevo"),
                "platform": contact_info.get("platform", "web"),
                "telegram_user_id": contact_info.get("telegram_user_id"),
                "whatsapp_user_id": contact_info.get("whatsapp_user_id"),
                "facebook_messenger_user_id": contact_info.get("facebook_messenger_user_id"),
                "instagram_user_id": contact_info.get("instagram_user_id"),
                "platform_user_id": contact_info.get("platform_user_id"),
            }
            from ..schemas.contact import ContactCreate
            contact_info = ContactCreate(**contact_dict)
        
        # Create or get contact
        contact = await _create_or_get_contact(db, contact_info)
        
        # Create or get conversation
        conversation = await _create_or_get_conversation(db, contact.id, conversation_id)
        
        # Save user message
        user_message = await _save_message(db, conversation.id, contact.id, "user", message_text)
        
        # Generate response using LLM
        response_text = await _generate_response(db, message_text, contact, conversation)
        
        # Save agent (AI) response
        ai_message = await _save_message(db, conversation.id, contact.id, "agent", response_text)
        
        # Update contact interest level based on conversation
        await _update_contact_interest(db, contact, message_text, response_text)
        
        return {
            "response": response_text,
            "contact_id": contact.id,
            "message_id": ai_message.id if ai_message else None
        }
        
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        raise


async def _create_or_get_contact(
    db: Session,
    contact_info: Optional[ContactCreate] = None
) -> Contact:
    """
    Create or get contact based on contact information.
    
    Args:
        db: Database session
        contact_info: Contact information
    Returns:
        Contact object
    """
    if not contact_info:
        raise ValueError("Se requiere información de contacto")

    # Validate platform type
    if contact_info.platform not in [pt.value for pt in PlatformType]:
        logger.warning(f"Tipo de plataforma no válida: {contact_info.platform}")
        contact_info.platform = "web"
    
    # Normalize inputs
    name = contact_info.name or "Usuario desconocido"
    phone = contact_info.phone
    email = contact_info.email
    company = contact_info.company
    platform_user_id = contact_info.platform_user_id

    # Try platform-specific lookup first
    contact: Optional[Contact] = None
    if contact_info.platform == "telegram" and platform_user_id:
        contact = db.query(Contact).filter(Contact.telegram_user_id == platform_user_id).first()
    elif contact_info.platform == "whatsapp" and platform_user_id:
        contact = db.query(Contact).filter(Contact.whatsapp_user_id == platform_user_id).first()
    elif contact_info.platform == "facebook_messenger" and platform_user_id:
        contact = db.query(Contact).filter(Contact.facebook_messenger_user_id == platform_user_id).first()
    elif contact_info.platform == "instagram" and platform_user_id:
        contact = db.query(Contact).filter(Contact.instagram_user_id == platform_user_id).first()

    # Fallback lookup by phone/email
    if not contact and (phone or email):
        contact = (
            db.query(Contact)
            .filter(or_(Contact.phone == phone, Contact.email == email))
            .first()
        )

    # Create if not exists
    if not contact:
        platform_type_map = {
            "web": PlatformType.WEB,
            "telegram": PlatformType.TELEGRAM,
            "whatsapp": PlatformType.WHATSAPP,
            "facebook_messenger": PlatformType.FACEBOOK_MESSENGER,
            "instagram": PlatformType.INSTAGRAM,
        }
        contact = Contact(
            name=name,
            phone=phone,
            email=email,
            company=company,
            platform=platform_type_map.get(contact_info.platform, PlatformType.WEB),
        )
        # Set platform-specific IDs
        if contact_info.platform == "telegram" and platform_user_id:
            contact.telegram_user_id = platform_user_id
        elif contact_info.platform == "whatsapp" and platform_user_id:
            contact.whatsapp_user_id = platform_user_id
        elif contact_info.platform == "facebook_messenger" and platform_user_id:
            contact.facebook_messenger_user_id = platform_user_id
        elif contact_info.platform == "instagram" and platform_user_id:
            contact.instagram_user_id = platform_user_id

        db.add(contact)
        try:
            db.commit()
        except Exception:
            db.rollback()
            # Handle UNIQUE(phone/email) gracefully
            if phone:
                existing = db.query(Contact).filter(Contact.phone == phone).first()
                if existing:
                    contact = existing
            if not contact and email:
                existing = db.query(Contact).filter(Contact.email == email).first()
                if existing:
                    contact = existing
            if not contact:
                # Re-raise if not duplicate on normalized keys
                raise
        else:
            db.refresh(contact)
    else:
        # Update with new info if empty
        if name and contact.name == "Usuario desconocido":
            contact.name = name
        if phone and not contact.phone:
            contact.phone = phone
        if email and not contact.email:
            contact.email = email
        if company and not contact.company:
            contact.company = company
        # Fill platform-specific IDs if missing
        if contact_info.platform == "telegram" and platform_user_id and not contact.telegram_user_id:
            contact.telegram_user_id = platform_user_id
        elif contact_info.platform == "whatsapp" and platform_user_id and not contact.whatsapp_user_id:
            contact.whatsapp_user_id = platform_user_id
        elif contact_info.platform == "facebook_messenger" and platform_user_id and not contact.facebook_messenger_user_id:
            contact.facebook_messenger_user_id = platform_user_id
        elif contact_info.platform == "instagram" and platform_user_id and not contact.instagram_user_id:
            contact.instagram_user_id = platform_user_id
        db.commit()

    return cast(Contact, contact)


async def _create_or_get_conversation(db: Session, contact_id: int, conversation_id: Optional[int]) -> Conversation:
    """
    Create or get conversation based on provided information.
    """
    if conversation_id:
        conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if conversation:
            return conversation
    
    conversation = Conversation(
        contact_id=contact_id,
        platform=PlatformType.WEB  # Default platform type
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    
    return conversation


async def _save_message(db: Session, conversation_id: int, contact_id: int, role: str, content: str) -> Message:
    """
    Save a message to the database.
    """
    message = Message(
        conversation_id=conversation_id,
        contact_id=contact_id,
        sender=role,
        content=content
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


async def _generate_response(db: Session, message: str, contact: Contact, conversation: Conversation) -> str:
    """
    Genera una respuesta utilizando el servicio LLM basado en el contexto del contacto y la conversación.
    """
    try:
        # Preparar contexto para el LLM
        context = {
            "contact": contact,
            "conversation": conversation,
            "message": message,
            "interest_level": contact.interest_level.value if contact.interest_level else "nuevo",
            "platform": conversation.platform
        }
        
        # Usar el conocimiento específico según el tipo de mensaje
        if "workshop" in message.lower() or "taller" in message.lower():
            knowledge_base = workshop_knowledge_instance
        else:
            knowledge_base = scaie_knowledge
        
        # Generar respuesta usando Qwen
        response_text = await llm_service.generate_response(
            message=message,
            knowledge_base=knowledge_base,
            context=context
        )
        
        return response_text or "Disculpa, estoy teniendo dificultades técnicas. Por favor, inténtalo de nuevo más tarde."
        
    except Exception as e:
        logger.error(f"Error generando respuesta: {str(e)}")
        return "Disculpa, estoy teniendo dificultades técnicas. Por favor, inténtalo de nuevo más tarde."


async def _update_contact_interest(db: Session, contact: Contact, user_message: str, ai_response: str):
    """
    Update contact interest level based on conversation content with enhanced persuasion logic.
    """
    # Enhanced interest detection with more sophisticated patterns
    user_message_lower = user_message.lower()
    
    # Strong interest signals - user explicitly shows interest
    strong_interest_keywords = [
        "interesado", "interesada", "quiero", "necesito", "me gusta", 
        "agendar", "cita", "llamada", "información", "detalles",
        "precio", "costo", "cuanto", "cuánto", "presupuesto",
        "cotización", "cotizacion", "contactar", "asesor",
        "demo", "demostración", "prueba", "muestra", "más info",
        "más información", "hablar", "charlar", "platica", "platicar"
    ]
    
    # Medium interest signals - user shows curiosity or asks specific questions
    medium_interest_keywords = [
        "como funciona", "cómo funciona", "que incluye", "qué incluye",
        "duracion", "duración", "tiempo", "cuanto tiempo", "cuánto tiempo",
        "modalidad", "online", "presencial", "híbrido", "híbrida",
        "equipo", "personas", "participantes", "empresa",
        "resultados", "beneficios", "ventajas", "ayuda",
        "automatizar", "procesos", "tareas", "eficiente"
    ]
    
    # Negative signals - user shows disinterest
    negative_keywords = [
        "no", "no gracias", "no estoy interesado", "no me interesa",
        "ocupado", "después", "otro momento", "no ahora",
        "caro", "muy caro", "costoso", "muy costoso",
        "no puedo", "no es posible", "no tengo"
    ]
    
    # Calendly click or phone number request signals
    calendly_requested = "calendly" in ai_response.lower() or "agendar" in ai_response.lower()
    phone_requested = any(keyword in user_message_lower for keyword in ["teléfono", "telefono", "número", "numero", "whatsapp"])
    
    # Check for explicit interest signals
    has_strong_interest = any(keyword in user_message_lower for keyword in strong_interest_keywords)
    has_medium_interest = any(keyword in user_message_lower for keyword in medium_interest_keywords)
    has_negative_signal = any(keyword in user_message_lower for keyword in negative_keywords)
    
    # Update interest level based on detected signals
    if has_negative_signal and not (has_strong_interest or has_medium_interest):
        contact.interest_level = InterestLevel.NOT_INTERESTED
    elif has_strong_interest or calendly_requested or phone_requested:
        # Strong interest or user requested contact info
        contact.interest_level = InterestLevel.INTERESTED
    elif has_medium_interest:
        # Medium interest - user is curious
        if contact.interest_level == InterestLevel.NEW:
            contact.interest_level = InterestLevel.CONTACTED
        elif contact.interest_level == InterestLevel.CONTACTED:
            # If already contacted and showing continued interest, move to interested
            contact.interest_level = InterestLevel.INTERESTED
    
    # Additional logic for persuasion - if user has been contacted and shows continued interest
    if (contact.interest_level == InterestLevel.CONTACTED and 
        (has_strong_interest or has_medium_interest)):
        # Move to interested if they continue showing interest
        contact.interest_level = InterestLevel.INTERESTED
        
    try:
        db.commit()
    except Exception as e:
        logger.error(f"Error updating contact interest: {str(e)}")
        db.rollback()