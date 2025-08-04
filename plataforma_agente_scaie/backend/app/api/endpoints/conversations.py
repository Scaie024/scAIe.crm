from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List
import re

from ...core.database import get_db
from ...models.conversation import Conversation, Message
from ...models.contact import Contact, InterestLevel
from ...schemas.conversation import Conversation as ConversationSchema, ConversationCreate, MessageCreate
from ...services.llm_service import llm_service

router = APIRouter(prefix="/conversations", tags=["conversations"])

@router.get("/", response_model=List[ConversationSchema])
def list_conversations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List conversations from database.
    """
    conversations = db.query(Conversation).offset(skip).limit(limit).all()
    return [ConversationSchema.from_orm(conv) for conv in conversations]

@router.post("/", response_model=ConversationSchema)
def create_conversation(
    conversation: ConversationCreate,
    db: Session = Depends(get_db)
):
    """
    Create new conversation in database.
    """
    # Check if contact exists
    contact = db.query(Contact).filter(Contact.id == conversation.contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    # Create conversation
    db_conversation = Conversation(
        contact_id=conversation.contact_id,
        platform=conversation.platform
    )
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    
    return ConversationSchema.from_orm(db_conversation)

@router.get("/{conversation_id}", response_model=ConversationSchema)
def get_conversation(
    conversation_id: int,
    db: Session = Depends(get_db)
):
    """
    Get conversation by ID from database.
    """
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return ConversationSchema.from_orm(conversation)

@router.delete("/{conversation_id}")
def delete_conversation(
    conversation_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete conversation by ID.
    """
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    db.delete(conversation)
    db.commit()
    return {"message": "Conversation deleted successfully"}

@router.get("/{conversation_id}/messages")
def get_conversation_messages(
    conversation_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get messages for a conversation.
    """
    # Check if conversation exists
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Get messages
    messages = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(desc(Message.created_at)).offset(skip).limit(limit).all()
    
    return [msg.to_dict() for msg in messages]

@router.post("/{conversation_id}/messages")
async def send_message(
    conversation_id: int,
    message: MessageCreate,
    db: Session = Depends(get_db)
):
    """
    Send a message in a conversation.
    """
    # Check if conversation exists
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Save user message to database
    if message.sender == "user":
        user_message = Message(
            conversation_id=conversation_id,
            sender="user",
            content=message.content
        )
        db.add(user_message)
        db.commit()
        
        # Generate AI response
        ai_response_data = await llm_service.generate_response(message.content)
        ai_response_text = ai_response_data.get("response", "Lo siento, no puedo procesar tu solicitud en este momento.")
        
        # Save AI response to database
        ai_message = Message(
            conversation_id=conversation_id,
            sender="agent",
            content=ai_response_text
        )
        db.add(ai_message)
        db.commit()
        
        return {
            "user_message": user_message.to_dict(),
            "ai_response": ai_message.to_dict()
        }
    
    # Save agent message to database
    elif message.sender == "agent":
        agent_message = Message(
            conversation_id=conversation_id,
            sender="agent",
            content=message.content
        )
        db.add(agent_message)
        db.commit()
        
        return {"message": agent_message.to_dict()}
    
    raise HTTPException(status_code=400, detail="Invalid sender. Must be 'user' or 'agent'")

# Nuevo endpoint para crear conversaciones desde canales externos con registro automático de contactos
@router.post("/from-channel")
async def create_conversation_from_channel(
    platform: str,
    user_phone: str,
    user_name: str = None,
    initial_message: str = None,
    db: Session = Depends(get_db)
):
    """
    Create a conversation from an external channel (WhatsApp, Messenger, Telegram)
    and automatically register the contact if not exists.
    """
    try:
        # Verificar si el contacto ya existe
        contact = db.query(Contact).filter(Contact.phone == user_phone).first()
        
        # Si no existe, crearlo
        if not contact:
            contact = Contact(
                name=user_name or f"Usuario {user_phone}",
                phone=user_phone,
                interest_level=InterestLevel.NEW
            )
            db.add(contact)
            db.commit()
            db.refresh(contact)
        
        # Crear la conversación
        conversation = Conversation(
            contact_id=contact.id,
            platform=platform
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        
        # Si hay un mensaje inicial, guardarlo
        if initial_message:
            message = Message(
                conversation_id=conversation.id,
                sender="user",
                content=initial_message
            )
            db.add(message)
            db.commit()
            
            # Generar respuesta del agente
            ai_response_data = await llm_service.generate_response(initial_message)
            ai_response_text = ai_response_data.get("response", "¡Hola! Estoy aquí para ayudarte. ¿En qué puedo ayudarte hoy?")
            
            # Guardar respuesta del agente
            ai_message = Message(
                conversation_id=conversation.id,
                sender="agent",
                content=ai_response_text
            )
            db.add(ai_message)
            db.commit()
            
            return {
                "contact": contact.to_dict(),
                "conversation": conversation.to_dict(),
                "initial_message": message.to_dict(),
                "agent_response": ai_message.to_dict()
            }
        
        return {
            "contact": contact.to_dict(),
            "conversation": conversation.to_dict()
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating conversation: {str(e)}")