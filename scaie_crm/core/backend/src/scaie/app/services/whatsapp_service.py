import os
import json
from typing import Dict, Any
from datetime import datetime
import httpx
from .llm_service import llm_service

class WhatsAppService:
    def __init__(self):
        """Initialize WhatsApp service."""
        self.token = os.getenv('WHATSAPP_TOKEN')
        self.phone_number_id = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
        self.base_url = f"https://graph.facebook.com/v17.0/{self.phone_number_id}"
        self.client = httpx.AsyncClient()
        
    async def process_message(self, message: str, user_id: str) -> Dict[str, Any]:
        """
        Process incoming WhatsApp message and generate response.
        
        Args:
            message: Incoming message text
            user_id: WhatsApp user ID
            
        Returns:
            Dict with response and metadata
        """
        try:
            # Generate response using LLM service
            llm_response = await llm_service.generate_response(message)
            
            # Send response back via WhatsApp
            if llm_response.get('success'):
                await self.send_message(llm_response['response'], user_id)
            
            return llm_response
        except Exception as e:
            print(f"Error processing WhatsApp message: {e}")
            return {
                'success': False,
                'error': str(e),
                'response': 'Lo siento, ha ocurrido un error al procesar tu mensaje.'
            }
    
    async def send_message(self, message: str, recipient_id: str) -> bool:
        """
        Send message via WhatsApp API.
        
        Args:
            message: Message to send
            recipient_id: WhatsApp recipient ID
            
        Returns:
            Boolean indicating success
        """
        try:
            if not self.token or not self.phone_number_id:
                print("WhatsApp credentials not configured")
                return False
                
            url = f"{self.base_url}/messages"
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "messaging_product": "whatsapp",
                "to": recipient_id,
                "text": {"body": message}
            }
            
            response = await self.client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"Error sending WhatsApp message: {e}")
            return False
    
    async def verify_webhook(self, challenge: str, mode: str, token: str) -> Dict[str, Any]:
        """
        Verify webhook for WhatsApp integration.
        
        Args:
            challenge: Verification challenge
            mode: Verification mode
            token: Verification token
            
        Returns:
            Dict with verification result
        """
        verify_token = os.getenv('WHATSAPP_VERIFY_TOKEN')
        
        if mode and token:
            if mode == 'subscribe' and token == verify_token:
                return {
                    'success': True,
                    'challenge': challenge
                }
            else:
                return {
                    'success': False,
                    'error': 'Verification failed'
                }
        else:
            return {
                'success': False,
                'error': 'Missing parameters'
            }

# Global instance
whatsapp_service = WhatsAppService()