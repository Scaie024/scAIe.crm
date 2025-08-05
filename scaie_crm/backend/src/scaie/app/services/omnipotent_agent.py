import re
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from ..core.database import get_db
from ..models.contact import Contact, InterestLevel
from ..models.conversation import Conversation, Message
from ..models.agent_action import AgentAction, AgentTask
from ..services.llm_service import llm_service
from ..services.scaie_knowledge import scaie_knowledge

class OmnipotentAgent:
    def __init__(self):
        pass
    
    async def process_incoming_message(self, message: str, platform: str, contact_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process an incoming message and determine appropriate actions.
        """
        db_gen = get_db()
        db = next(db_gen)
        
        try:
            # Get or create contact
            contact = self._get_or_create_contact(db, contact_info, platform)
            
            # Create or get conversation
            conversation = self._get_or_create_conversation(db, contact.id, platform)
            
            # Save user message
            user_message = self._save_message(db, conversation.id, "user", message)
            
            # Generate response using LLM
            response_text = await self._generate_response(db, message, contact, conversation)
            
            # Save agent response
            agent_message = self._save_message(db, conversation.id, "agent", response_text)
            
            # Determine actions based on message content
            actions = self._determine_actions(message, contact)
            
            # Execute immediate actions
            executed_actions = []
            pending_actions = []
            
            for action in actions:
                if action.get("execute_immediately", False):
                    result = self._execute_action(db, action, contact, conversation)
                    executed_actions.append({
                        "action_type": action["type"],
                        "parameters": action["parameters"],
                        "result": result
                    })
                else:
                    # Save pending action
                    self._save_pending_action(db, action, conversation.id)
                    pending_actions.append(action)
            
            # Update contact interest level based on message content
            self._update_interest_level(db, contact, message)
            
            db.commit()
            
            return {
                "response": response_text,
                "contact_id": contact.id,
                "message_id": agent_message.id,
                "actions": pending_actions,
                "executed_actions": executed_actions
            }
            
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    def _get_or_create_contact(self, db: Session, contact_info: Dict[str, Any], platform: str) -> Contact:
        """
        Get existing contact or create a new one.
        """
        contact = None
        
        # Try to find contact by phone first
        if contact_info.get("phone"):
            contact = db.query(Contact).filter(Contact.phone == contact_info["phone"]).first()
        
        # Try to find contact by Telegram user ID
        if not contact and platform == "telegram" and contact_info.get("platform_user_id"):
            contact = db.query(Contact).filter(
                Contact.telegram_user_id == contact_info["platform_user_id"]
            ).first()
        
        # Try to find contact by platform user ID for other platforms
        if not contact and platform != "telegram" and contact_info.get("platform_user_id"):
            contact = db.query(Contact).filter(
                Contact.platform_user_id == contact_info["platform_user_id"]
            ).first()
        
        # If still no contact found, create a new one
        if not contact:
            contact = Contact(
                name=contact_info.get("name", "Usuario Desconocido"),
                phone=contact_info.get("phone"),
                email=contact_info.get("email"),
                company=contact_info.get("company"),
                telegram_user_id=contact_info.get("platform_user_id") if platform == "telegram" else None,
                platform_user_id=contact_info.get("platform_user_id") if platform != "telegram" else None
            )
            db.add(contact)
            db.flush()
        
        return contact
    
    def _get_or_create_conversation(self, db: Session, contact_id: int, platform: str) -> Conversation:
        """
        Get existing conversation or create a new one.
        """
        # Try to get the most recent conversation for this contact and platform
        conversation = db.query(Conversation).filter(
            and_(
                Conversation.contact_id == contact_id,
                Conversation.platform == platform
            )
        ).order_by(Conversation.created_at.desc()).first()
        
        # If no recent conversation or last message was more than 1 day ago, create a new one
        if not conversation:
            conversation = Conversation(
                contact_id=contact_id,
                platform=platform
            )
            db.add(conversation)
            db.flush()
        
        return conversation
    
    def _save_message(self, db: Session, conversation_id: int, sender: str, content: str) -> Message:
        """
        Save a message to the database.
        """
        # Get the conversation to extract the contact_id
        conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if not conversation:
            raise ValueError("Conversation not found")
            
        message = Message(
            conversation_id=conversation_id,
            contact_id=conversation.contact_id,
            sender=sender,
            content=content
        )
        db.add(message)
        db.flush()
        return message
    
    async def _generate_response(self, db: Session, message: str, contact: Contact, conversation: Conversation) -> str:
        """
        Generate a response using the LLM service.
        """
        # Get conversation history
        history = db.query(Message).filter(
            Message.conversation_id == conversation.id
        ).order_by(Message.created_at.desc()).limit(10).all()
        
        # Format history for LLM
        formatted_history = []
        for msg in reversed(history):
            formatted_history.append({
                "role": msg.sender,
                "content": msg.content
            })
        
        # Add current message
        formatted_history.append({
            "role": "user",
            "content": message
        })
        
        # Prepare contact info
        contact_info = {
            "name": contact.name,
            "phone": contact.phone,
            "email": contact.email,
            "company": contact.company
        }
        
        # Generate response
        response = await llm_service.generate_response(
            user_message=message,
            conversation_id=conversation.id,
            contact_info=contact_info
        )
        
        return response.get("response", "Lo siento, no puedo procesar tu solicitud en este momento.")
    
    def _determine_actions(self, message: str, contact: Contact) -> List[Dict[str, Any]]:
        """
        Determine what actions should be taken based on the message content.
        """
        actions = []
        message_lower = message.lower()
        
        # Action: Send material (brochure, etc.)
        if any(keyword in message_lower for keyword in ["folleto", "brochure", "información", "informacion", "detalles", "saber más", "saber mas"]):
            actions.append({
                "type": "send_material",
                "parameters": {
                    "material_type": "workshop_brochure",
                    "recipient": "user"
                },
                "execute_immediately": False,
                "description": "Enviar folleto del workshop"
            })
        
        # Action: Schedule appointment
        if any(keyword in message_lower for keyword in ["agendar", "cita", "reunión", "reunion", "consultoría", "consultoria", "asesoría", "asesoria"]):
            actions.append({
                "type": "schedule_appointment",
                "parameters": {
                    "appointment_type": "workshop_consultation",
                    "duration": 30
                },
                "execute_immediately": False,
                "description": "Agendar consulta para el workshop"
            })
        
        # Action: Generate quote
        if any(keyword in message_lower for keyword in ["precio", "costo", "cuánto", "cuanto", "presupuesto"]):
            actions.append({
                "type": "generate_quote",
                "parameters": {
                    "service_type": "workshop",
                    "contact_id": contact.id
                },
                "execute_immediately": False,
                "description": "Generar cotización para el workshop"
            })
        
        # Action: Escalate to human
        if any(keyword in message_lower for keyword in ["humano", "persona", "asesor", "representante"]):
            actions.append({
                "type": "escalate_to_human",
                "parameters": {
                    "reason": "User requested human assistance",
                    "priority": "normal"
                },
                "execute_immediately": True,
                "description": "Escalar conversación a agente humano"
            })
        
        # If no specific actions identified, but message shows interest, send material
        if not actions and any(keyword in message_lower for keyword in ["interesado", "interés", "interes", "quiero", "necesito", "me sirve"]):
            actions.append({
                "type": "send_material",
                "parameters": {
                    "material_type": "workshop_brochure",
                    "recipient": "user"
                },
                "execute_immediately": False,
                "description": "Enviar folleto del workshop"
            })
        
        # Default action if no other actions identified
        if not actions:
            actions.append({
                "type": "send_material",
                "parameters": {
                    "material_type": "workshop_brochure",
                    "recipient": "user"
                },
                "execute_immediately": False,
                "description": "Enviar folleto del workshop"
            })
        
        return actions
    
    def _execute_action(self, db: Session, action: Dict[str, Any], contact: Contact, conversation: Conversation) -> Dict[str, Any]:
        """
        Execute an immediate action.
        """
        action_type = action["type"]
        parameters = action["parameters"]
        
        if action_type == "update_interest_level":
            new_level = parameters.get("interest_level", "contactado")
            try:
                contact.interest_level = InterestLevel(new_level)
                contact.notes = (contact.notes or "") + f"\nActualizado por agente: {parameters.get('reason', 'Interest level updated')}"
                db.commit()
                return {
                    "status": "success",
                    "message": "Nivel de interés actualizado"
                }
            except Exception as e:
                return {
                    "status": "error",
                    "message": f"Error actualizando nivel de interés: {str(e)}"
                }
        
        elif action_type == "escalate_to_human":
            # Create task for human escalation
            task = AgentTask(
                contact_id=contact.id,
                title="Escalar a agente humano",
                description=parameters.get("reason", "User requested human assistance"),
                status="pending",
                priority=parameters.get("priority", "normal")
            )
            db.add(task)
            db.commit()
            return {
                "status": "success",
                "message": "Tarea de escalado creada",
                "task_id": task.id
            }
        
        # For other actions, return default success
        return {
            "status": "success",
            "message": f"Action {action_type} executed"
        }
    
    def _save_pending_action(self, db: Session, action: Dict[str, Any], conversation_id: int):
        """
        Save a pending action to the database.
        """
        agent_action = AgentAction(
            conversation_id=conversation_id,
            action_type=action["type"],
            parameters=action["parameters"],
            status="pending"
        )
        db.add(agent_action)
        db.flush()
    
    def _update_interest_level(self, db: Session, contact: Contact, message: str):
        """
        Update contact interest level based on message content.
        """
        message_lower = message.lower()
        
        # Update interest level based on keywords
        if any(keyword in message_lower for keyword in ["no estoy interesado", "no me interesa", "no gracias"]):
            contact.interest_level = InterestLevel.NOT_INTERESTED
        elif any(keyword in message_lower for keyword in ["estoy interesado", "me interesa", "quiero saber más", "quiero saber mas", "quiero información", "quiero informacion"]):
            contact.interest_level = InterestLevel.INTERESTED
        elif any(keyword in message_lower for keyword in ["agendar", "cita", "reunión", "reunion"]):
            contact.interest_level = InterestLevel.CONFIRMED
        elif contact.interest_level == InterestLevel.NEW:
            contact.interest_level = InterestLevel.CONTACTED
    
    def execute_pending_actions(self, conversation_id: int) -> List[Dict[str, Any]]:
        """
        Execute all pending actions for a conversation.
        """
        db_gen = get_db()
        db = next(db_gen)
        
        try:
            # Get pending actions
            pending_actions = db.query(AgentAction).filter(
                and_(
                    AgentAction.conversation_id == conversation_id,
                    AgentAction.status == "pending"
                )
            ).all()
            
            results = []
            
            for action in pending_actions:
                # In a real implementation, we would actually execute the actions here
                # For now, we'll just mark them as completed
                action.status = "completed"
                action.executed_at = func.now()
                
                results.append({
                    "action_type": action.action_type,
                    "parameters": action.parameters,
                    "result": action.result
                })
            
            db.commit()
            return results
            
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    def get_contact_summary(self, contact_id: int) -> Dict[str, Any]:
        """
        Get a summary of a contact's interactions.
        """
        db_gen = get_db()
        db = next(db_gen)
        
        try:
            # Get contact
            contact = db.query(Contact).filter(Contact.id == contact_id).first()
            if not contact:
                return {"error": "Contact not found"}
            
            # Get conversations count
            conversations_count = db.query(Conversation).filter(
                Conversation.contact_id == contact_id
            ).count()
            
            # Get recent tasks
            recent_tasks = db.query(AgentTask).filter(
                AgentTask.contact_id == contact_id
            ).order_by(AgentTask.created_at.desc()).limit(5).all()
            
            # Get recent actions
            recent_actions = db.query(AgentAction).join(Conversation).filter(
                Conversation.contact_id == contact_id
            ).order_by(AgentAction.created_at.desc()).limit(5).all()
            
            return {
                "contact": contact.to_dict(),
                "conversations_count": conversations_count,
                "tasks": [task.to_dict() for task in recent_tasks],
                "recent_actions": [action.to_dict() for action in recent_actions]
            }
            
        except Exception as e:
            return {"error": str(e)}
        finally:
            db.close()
    
    def search_contacts(self, query: str) -> List[Dict[str, Any]]:
        """
        Search contacts by name, phone, email or company.
        """
        db_gen = get_db()
        db = next(db_gen)
        
        try:
            # Search contacts
            contacts = db.query(Contact).filter(
                or_(
                    Contact.name.ilike(f"%{query}%"),
                    Contact.phone.ilike(f"%{query}%"),
                    Contact.email.ilike(f"%{query}%"),
                    Contact.company.ilike(f"%{query}%")
                )
            ).all()
            
            return [contact.to_dict() for contact in contacts]
            
        except Exception as e:
            raise e
        finally:
            db.close()
    
    def create_task(self, contact_id: int, title: str, description: Optional[str] = None, 
                   priority: str = "medium", due_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new task for a contact.
        """
        db_gen = get_db()
        db = next(db_gen)
        
        try:
            # Verify contact exists
            contact = db.query(Contact).filter(Contact.id == contact_id).first()
            if not contact:
                raise ValueError("Contact not found")
            
            # Create task
            task = AgentTask(
                contact_id=contact_id,
                title=title,
                description=description,
                status="pending",
                priority=priority,
                due_date=due_date
            )
            db.add(task)
            db.commit()
            db.refresh(task)
            
            return task.to_dict()
            
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    def update_task(self, task_id: int, **kwargs) -> Dict[str, Any]:
        """
        Update a task.
        """
        db_gen = get_db()
        db = next(db_gen)
        
        try:
            # Get task
            task = db.query(AgentTask).filter(AgentTask.id == task_id).first()
            if not task:
                raise ValueError("Task not found")
            
            # Update fields
            for key, value in kwargs.items():
                if hasattr(task, key) and key != "id":
                    setattr(task, key, value)
            
            db.commit()
            db.refresh(task)
            
            return task.to_dict()
            
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
    
    def get_tasks(self) -> List[Dict[str, Any]]:
        """
        Get all tasks.
        """
        db_gen = get_db()
        db = next(db_gen)
        
        try:
            tasks = db.query(AgentTask).all()
            return [task.to_dict() for task in tasks]
            
        except Exception as e:
            raise e
        finally:
            db.close()

# Global instance
omnipotent_agent = OmnipotentAgent()