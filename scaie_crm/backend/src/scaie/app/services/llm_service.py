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
    
    # Eliminar comillas iniciales y finales si existen
    if text.startswith('"') and text.endswith('"'):
        text = text[1:-1]
    
    return text

async def generate_response(message: str, contact: Optional[Dict[str, Any]] = None) -> str:
    """
    Genera una respuesta usando el modelo de lenguaje.
    
    Args:
        message: Mensaje del usuario
        contact: Información del contacto (opcional)
        
    Returns:
        Respuesta generada por el modelo
    """
    if not client:
        logger.error("OpenAI client not initialized - missing API key")
        return "Lo siento, no puedo procesar tu solicitud en este momento debido a problemas de configuración."
    
    try:
        # Construir el contexto de la conversación
        context = f"""
Eres {AGENT_NAME}, un {AGENT_PERSONALITY}.
Tu objetivo es: {AGENT_GOAL}.
Tono de comunicación: {AGENT_TONE}.

Información del contacto:
Nombre: {contact.get('name', 'No proporcionado') if contact else 'No proporcionado'}
Empresa: {contact.get('company', 'No proporcionada') if contact else 'No proporcionada'}
Nivel de interés: {contact.get('interest_level', 'No determinado') if contact else 'No determinado'}

Mensaje del cliente: {message}
"""

        # Generar la respuesta usando el modelo
        logger.info(f"Generando respuesta para el mensaje: {message}")
        
        completion = await client.chat.completions.create(
            model="qwen-plus",
            messages=[
                {
                    "role": "system",
                    "content": context
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            temperature=0.7,
            top_p=0.8
        )
        
        response_text = completion.choices[0].message.content
        formatted_response = format_response(response_text)
        
        logger.info(f"Respuesta del modelo: {formatted_response}")
        return formatted_response
        
    except RateLimitError as e:
        logger.error(f"Rate limit exceeded: {str(e)}")
        return "Estoy recibiendo muchas solicitudes en este momento. Por favor, espera un momento antes de enviar otro mensaje."
        
    except APIError as e:
        logger.error(f"API error: {str(e)}")
        return "Lo siento, estoy teniendo dificultades para conectarme con mis sistemas en este momento. Por favor, inténtalo de nuevo más tarde."
        
    except Exception as e:
        logger.error(f"Error generando respuesta: {str(e)}")
        return "Lo siento, estoy experimentando dificultades técnicas en este momento. Por favor, inténtalo de nuevo más tarde."

# Instancia del servicio
llm_service = type('LLMService', (), {
    'generate_response': staticmethod(generate_response)
})()