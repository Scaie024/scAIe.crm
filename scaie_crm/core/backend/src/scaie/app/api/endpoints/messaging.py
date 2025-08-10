from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session
from typing import Dict, Any
import json

from ...core.database import get_db
from ...services.instagram_service import InstagramService
from ...services.messenger_service import MessengerService

router = APIRouter(prefix="/messaging", tags=["messaging"])

# Initialize services
instagram_service = InstagramService()
messenger_service = MessengerService()

@router.get("/instagram/webhook")
async def verify_instagram_webhook(request: Request):
    """
    Verify Instagram webhook subscription.
    """
    try:
        request_data = dict(request.query_params)
        is_verified = await instagram_service.verify_webhook(request_data)
        
        if is_verified:
            challenge = request_data.get("hub.challenge")
            return Response(content=challenge, media_type="text/plain")
        else:
            raise HTTPException(status_code=403, detail="Verification failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/instagram/webhook")
async def handle_instagram_message(request: Request, db: Session = Depends(get_db)):
    """
    Handle incoming Instagram messages.
    """
    try:
        body = await request.json()
        
        # Process Instagram webhook events
        for entry in body.get("entry", []):
            for messaging_event in entry.get("messaging", []):
                if messaging_event.get("message"):
                    sender_id = messaging_event["sender"]["id"]
                    message_text = messaging_event["message"]["text"]
                    
                    # Process the message
                    await instagram_service.process_message(message_text, sender_id)
        
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/messenger/webhook")
async def verify_messenger_webhook(request: Request):
    """
    Verify Facebook Messenger webhook subscription.
    """
    try:
        request_data = dict(request.query_params)
        is_verified = await messenger_service.verify_webhook(request_data)
        
        if is_verified:
            challenge = request_data.get("hub.challenge")
            return Response(content=challenge, media_type="text/plain")
        else:
            raise HTTPException(status_code=403, detail="Verification failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/messenger/webhook")
async def handle_messenger_message(request: Request, db: Session = Depends(get_db)):
    """
    Handle incoming Facebook Messenger messages.
    """
    try:
        body = await request.json()
        
        # Process Facebook Messenger webhook events
        for entry in body.get("entry", []):
            for messaging_event in entry.get("messaging", []):
                if messaging_event.get("message"):
                    sender_id = messaging_event["sender"]["id"]
                    message_text = messaging_event["message"]["text"]
                    
                    # Process the message
                    await messenger_service.process_message(message_text, sender_id)
        
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))