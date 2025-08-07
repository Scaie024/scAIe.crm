import os
import asyncio
import logging
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv
import json
import random
from datetime import datetime
from .scaie_knowledge import scaie_knowledge
from .workshop_knowledge import workshop_knowledge_instance
from ..core.database import get_db, SessionLocal
from ..models.conversation import Message, Conversation
from ..models.contact import Contact, InterestLevel
from ..services.contact_service import contact_service
from openai import AsyncOpenAI, OpenAI, APIError, RateLimitError

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

# Personalidad y estilo de respuesta alineados con la visión
AGENT_NAME = os.getenv('AGENT_NAME', 'SCAI')
AGENT_PERSONALITY = os.getenv('AGENT_PERSONALITY', 'experto en ventas de workshops, profesional, directo, conversacional, natural')
AGENT_TONE = os.getenv('AGENT_TONE', 'profesional y directo')
AGENT_GOAL = os.getenv('AGENT_GOAL', 'vender el workshop "Sé más eficiente con IA" y posicionar a SCAIE como consultor experto en IA')

# Initialize OpenAI client
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
api_key = DASHSCOPE_API_KEY
base_url = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"

if api_key:
    client = AsyncOpenAI(
        api_key=api_key,
        base_url=base_url
    )
else:
    logger.warning("DASHSCOPE_API_KEY not found in environment variables")
    client = None

def format_response(text):
    """Da formato a la respuesta para que parezca más natural"""
    # Eliminar espacios extra al inicio y final
    text = text.strip()
    
    # Eliminar asteriscos que pueden haberse generado en la respuesta
    text = text.replace('*', '')
    
    return text

class LLMService:
    def __init__(self):
        self.client = client
        self.agent_name = AGENT_NAME
        self.agent_personality = AGENT_PERSONALITY
        self.agent_tone = AGENT_TONE
        self.agent_goal = AGENT_GOAL
        self.workshop_knowledge = workshop_knowledge_instance

    async def generate_response(self, message: str, contact: Optional[Contact] = None) -> Dict[str, Any]:
        """
        Generate AI response for incoming message.
        
        Args:
            message: Incoming message text
            contact: Contact object (optional)
            
        Returns:
            Dict with response and metadata
        """
        try:
            # Check for specific keywords that require predefined responses
            response = self._check_predefined_responses(message)
            if response:
                return {
                    'success': True,
                    'response': response,
                    'contact_id': contact.id if contact else None
                }
            
            # Generate response using LLM
            system_prompt = self._create_system_prompt()
            user_prompt = self._create_user_prompt(message, contact)
            
            if not self.client:
                return {
                    'success': False,
                    'error': 'OpenAI client not initialized',
                    'response': 'Lo siento, el servicio de IA no está disponible en este momento. Por favor, comunícate al 5535913417 para obtener asistencia.'
                }
            
            response = await self.client.chat.completions.create(
                model=os.getenv('QWEN_MODEL', 'qwen-plus'),
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=float(os.getenv('TEMPERATURE', '0.9')),  # Más creativo/natural
                max_tokens=int(os.getenv('MAX_TOKENS', '512'))       # Respuestas más cortas
            )
            
            ai_response = response.choices[0].message.content
            
            # Format response
            formatted_response = format_response(ai_response)
            
            return {
                'success': True,
                'response': formatted_response,
                'contact_id': contact.id if contact else None
            }
            
        except APIError as e:
            logger.error(f"OpenAI API error: {e}")
            return {
                'success': False,
                'error': str(e),
                'response': 'Lo siento, estoy experimentando dificultades técnicas. Por favor, inténtalo de nuevo más tarde o comunícate al 5535913417.'
            }
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return {
                'success': False,
                'error': str(e),
                'response': 'Lo siento, ha ocurrido un error inesperado. Por favor, comunícate al 5535913417 para obtener asistencia.'
            }
    
    def _check_predefined_responses(self, message: str) -> Optional[str]:
        """
        Check for keywords that require predefined responses.
        
        Args:
            message: Incoming message text
            
        Returns:
            Predefined response or None
        """
        message_lower = message.lower()
        
        # Contact information keywords
        contact_keywords = [
            "humano", "persona", "asesor", "cotizacion", "cotización", 
            "precio específico", "precio personalizado", "hablar con alguien"
        ]
        
        if any(keyword in message_lower for keyword in contact_keywords):
            return f"Claro, para una cotización personalizada puedes llamar al {self.workshop_knowledge['detalles_contacto']['telefono']}. ¿Qué tipo de procesos te gustaría automatizar?"
        
        # Scheduling keywords
        schedule_keywords = [
            "agendar", "cita", "llamada", "reunión", "consultoría", 
            "sesión", "entrevista", "conversar"
        ]
        
        if any(keyword in message_lower for keyword in schedule_keywords):
            return f"Perfecto, puedes agendar una llamada aquí: {self.workshop_knowledge['detalles_contacto']['calendly']}. Es gratis y dura 15 minutos."
        
        # Website keywords
        website_keywords = [
            "más información", "detalles", "sitio web", "página web", 
            "información adicional", "ver más"
        ]
        
        if any(keyword in message_lower for keyword in website_keywords):
            return f"Aquí tienes más info: {self.workshop_knowledge['detalles_contacto']['sitio_web']}. ¿Hay algo específico que te interese saber?"
        
        return None
    
    def _create_system_prompt(self) -> str:
        """Create system prompt for the AI agent."""
        return f"""
        Eres {self.agent_name}, un consultor especializado en automatización con IA.

        PERSONALIDAD: Natural, conversacional, amigable pero profesional
        ESTILO: Respuestas CORTAS (1-2 oraciones máximo), como hablaría un humano real
        OBJETIVO: Ayudar a empresas a ser más eficientes con IA

        INFORMACIÓN DEL WORKSHOP:
        - Nombre: "{self.workshop_knowledge['titulo']}"
        - Duración: 2-4 horas según necesidades  
        - Modalidad: Online o presencial
        - Precio: Desde $1,499 MXN
        
        BENEFICIOS CLAVE:
        - Sin programación, herramientas que cualquiera puede usar
        - Resultados inmediatos desde la primera sesión
        - Para todos los departamentos (ventas, admin, gerencia)
        - Empezamos con herramientas gratuitas

        REGLAS IMPORTANTES:
        1. RESPUESTAS MUY CORTAS: Máximo 1-2 oraciones por respuesta
        2. HABLA NATURAL: Como lo haría una persona real, sin formalidades
        3. SIN EMOJIS: Solo texto, conversación profesional pero cercana
        4. Ve AL GRANO: Di solo lo esencial sin rodeos
        5. HAZ PREGUNTAS: Termina con una pregunta simple para seguir la conversación

        CONTACTOS:
        - Teléfono: {self.workshop_knowledge['detalles_contacto']['telefono']}
        - Agendar llamada: {self.workshop_knowledge['detalles_contacto']['calendly']}

        CONTEXTO:
        Hablas con alguien que podría estar interesado en automatizar procesos con IA. 
        Sé directo, amigable y enfócate en cómo puedes ayudarlos específicamente.
        """

    def _create_user_prompt(self, message: str, contact: Optional[Contact] = None) -> str:
        """Create user prompt with context."""
        contact_info = ""
        if contact:
            contact_info = f"""
            Información del contacto:
            - Nombre: {contact.name}
            - Empresa: {contact.company or 'No especificada'}
            - Canal: {contact.platform or 'No especificado'}
            """
        
        return f"""
        MENSAJE DEL USUARIO: {message}
        
        {contact_info}
        
        Por favor, responde de manera profesional y amigable, siguiendo las instrucciones proporcionadas.
        """

    def process_sandbox_message(self, message: str, reset_context: bool = False) -> Dict[str, Any]:
        """
        Process message in sandbox mode for testing.
        
        Args:
            message: Message to process
            reset_context: Whether to reset conversation context
            
        Returns:
            Dict with response and metadata
        """
        try:
            # Simple echo response for sandbox
            response = f"[SANDBOX] {self.agent_name} dice: {message}"
            
            return {
                'success': True,
                'response': response,
                'sandbox': True
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'response': 'Error en modo sandbox'
            }

# Create singleton instance
llm_service = LLMService()