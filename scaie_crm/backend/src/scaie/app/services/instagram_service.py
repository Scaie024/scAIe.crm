import os
import json
from typing import Dict, Any
from datetime import datetime
import httpx
from .llm_service import llm_service
from ..models.contact import Contact, PlatformType
from ..models.conversation import Conversation, Message
from ..core.database import get_db
from sqlalchemy.orm import Session

class InstagramService:
    def __init__(self):
        """Initialize Instagram service."""
        self.token = os.getenv('INSTAGRAM_TOKEN')
        self.page_id = os.getenv('INSTAGRAM_PAGE_ID')
        self.base_url = f"https://graph.facebook.com/v17.0"
        self.client = httpx.AsyncClient()
        
    async def process_message(self, message: str, user_id: str, username: str = None) -> Dict[str, Any]:
        """
        Process incoming Instagram message and generate response.
        
        Args:
            message: Incoming message text
            user_id: Instagram user ID
            username: Instagram username (optional)
            
        Returns:
            Dict with response and metadata
        """
        db_gen = get_db()
        db: Session = next(db_gen)
        
        try:
            # Get or create contact
            contact = self._get_or_create_contact(db, user_id, username)
            
            # Create or get conversation
            conversation = self._get_or_create_conversation(db, contact.id)
            
            # Save user message
            self._save_message(db, conversation.id, "user", message)
            
            # Generate response using LLM service
            llm_response = await llm_service.generate_response(message, contact)
            
            # Save AI response
            if llm_response.get('success'):
                self._save_message(db, conversation.id, "ai", llm_response['response'])
                await self.send_message(llm_response['response'], user_id)
            
            return llm_response
        except Exception as e:
            print(f"Error processing Instagram message: {e}")
            error_response = {
                'success': False,
                'error': str(e),
                'response': 'Lo siento, ha ocurrido un error al procesar tu mensaje. Por favor, inténtalo de nuevo más tarde o comunícate al 5535913417.'
            }
            
            # Save error response
            try:
                conversation = self._get_or_create_conversation(db, contact.id) if 'contact' in locals() else None
                if conversation:
                    self._save_message(db, conversation.id, "ai", error_response['response'])
            except:
                pass
                
            return error_response
        finally:
            db.close()
    
    def _get_or_create_contact(self, db: Session, user_id: str, username: str = None) -> Contact:
        """Get existing contact or create new one."""
        # Try to find contact by Instagram user ID
        contact = db.query(Contact).filter(Contact.instagram_user_id == user_id).first()
        
        if not contact:
            # Create new contact
            contact = Contact(
                name=username if username else f"Usuario Instagram {user_id[:10]}",
                instagram_user_id=user_id,
                platform=PlatformType.INSTAGRAM
            )
            db.add(contact)
            db.commit()
            db.refresh(contact)
        elif not contact.instagram_user_id:
            # Update existing contact with Instagram ID
            contact.instagram_user_id = user_id
            contact.platform = PlatformType.INSTAGRAM
            db.commit()
            
        return contact
    
    def _get_or_create_conversation(self, db: Session, contact_id: int) -> Conversation:
        """Get existing conversation or create new one."""
        conversation = db.query(Conversation).filter(
            Conversation.contact_id == contact_id,
            Conversation.platform == PlatformType.INSTAGRAM
        ).first()
        
        if not conversation:
            conversation = Conversation(
                contact_id=contact_id,
                platform=PlatformType.INSTAGRAM
            )
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
            
        return conversation
    
    def _save_message(self, db: Session, conversation_id: int, role: str, content: str) -> Message:
        """Save message to database."""
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        return message
    
    async def send_message(self, message: str, recipient_id: str) -> bool:
        """
        Send message via Instagram API.
        
        Args:
            message: Message to send
            recipient_id: Instagram recipient ID
            
        Returns:
            Boolean indicating success
        """
        try:
            url = f"{self.base_url}/me/messages"
            
            payload = {
                "recipient": {"id": recipient_id},
                "message": {"text": message}
            }
            
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }
            
            response = await self.client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"Error sending Instagram message: {e}")
            return False
    
    async def verify_webhook(self, request: Dict[str, Any]) -> bool:
        """
        Verify Instagram webhook.
        
        Args:
            request: Webhook request data
            
        Returns:
            Boolean indicating verification success
        """
        try:
            mode = request.get("hub.mode")
            token = request.get("hub.verify_token")
            challenge = request.get("hub.challenge")
            
            verify_token = os.getenv('INSTAGRAM_VERIFY_TOKEN')
            
            if mode and token:
                if mode == 'subscribe' and token == verify_token:
                    print("Instagram webhook verified successfully")
                    return True
        
            return False
        except Exception as e:
            print(f"Error verifying Instagram webhook: {e}")
            return False