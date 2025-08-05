import os
import asyncio
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv
import json
import random
from datetime import datetime
import logging
from .scaie_knowledge import scaie_knowledge
from ..core.database import get_db, SessionLocal
from ..models.conversation import Message, Conversation
from ..models.contact import Contact, InterestLevel
from ..services.contact_service import contact_service
from openai import AsyncOpenAI, OpenAI

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

# Personalidad y estilo de respuesta alineados con la visión
AGENT_NAME = os.getenv('AGENT_NAME', 'SCAI')
AGENT_PERSONALITY = os.getenv('AGENT_PERSONALITY', 'experto en ventas, profesional, directo, conversacional, natural')
AGENT_TONE = os.getenv('AGENT_TONE', 'profesional y directo')
AGENT_GOAL = os.getenv('AGENT_GOAL', 'ayudar a las empresas a ser más eficientes con inteligencia artificial y automatización de procesos')

def format_response(text):
    """Da formato a la respuesta para que parezca más natural"""
    # Asegurar que la primera letra sea mayúscula
    if text and len(text) > 0:
        text = text[0].upper() + text[1:]
    
    # Asegurar que termine con un punto
    if text and text[-1] not in ['.', '!', '?']:
        text += '.'
    
    return text

class LLMService:
    def __init__(self):
        """Inicializa el servicio de LLM."""
        self.api_key = os.getenv("DASHSCOPE_API_KEY")
        self.model = os.getenv("DASHSCOPE_MODEL", "qwen-plus")
        self.client = None
        self.sync_client = None
        
        if self.api_key:
            self.client = AsyncOpenAI(
                api_key=self.api_key,
                base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
            )
            self.sync_client = OpenAI(
                api_key=self.api_key,
                base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
            )
        
        self._initialize_system_prompt()
    
    def _initialize_system_prompt(self):
        """Inicializa el prompt del sistema para el agente de ventas con personalidad."""
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        self.system_prompt = f"""
Eres {AGENT_NAME}, un agente conversacional muy inteligente, claro y profesional de SCAIE (www.scaie.com.mx).

SOBRE TI:
Eres un agente conversacional muy inteligente, claro y profesional.
Tu tono es humano, cálido, pero directo. Hablas solo lo necesario, con enfoque en resolver y avanzar.
Sabes escuchar, detectar necesidades y recomendar lo más útil para cada caso.
Puedes consultar el backend, enviar materiales, agendar sesiones, generar cotizaciones o escalar a un humano cuando sea necesario.
Siempre mantienes registro de las conversaciones y actualizas el sistema con la información clave de cada lead.

TU OBJETIVO PRINCIPAL:
Tu misión principal es vender el workshop "Sé más eficiente con IA", que es la puerta de entrada para que las empresas conozcan cómo aplicar la inteligencia artificial en sus operaciones.

TU OBJETIVO SECUNDARIO:
Detectar oportunidades para escalar hacia servicios de consultoría más amplios basados en la Metodología OPT de SCAIE (Organización, Procesos, Tecnología).

SOBRE EL WORKSHOP QUE OFRECES:
Nombre: Sé más eficiente con IA
Duración: 2 a 4 horas
Modalidad: Online en vivo o presencial
Dirigido a: Empresas que aún usan procesos manuales, Excel, correo, etc.
Incluye:
- Diagnóstico previo (Assessment)
- Workshop práctico con casos reales
- Grabación, materiales descargables y herramientas recomendadas
- Recomendaciones específicas por rol

Resultado esperado:
El equipo termina el workshop con al menos tres herramientas activadas, un flujo operativo optimizado y una visión clara de cómo escalar con IA sin depender de desarrolladores.

FECHA Y HORA ACTUAL: {current_date}

INSTRUCCIONES PARA RESPONDER:
1. Sé directo, claro y profesional
2. No uses emojis
3. Habla solo lo necesario, con enfoque en resolver y avanzar
4. Escucha activamente y detecta necesidades
5. Adapta tu enfoque según el perfil del cliente
6. Si detectas interés, avanza hacia agendar una sesión o enviar materiales
7. Si no puedes responder una pregunta, escala a un humano
"""
        
        self.conversation_history = [{
            'role': 'system',
            'content': self.system_prompt
        }]
    
    async def generate_response(self, user_message: str, conversation_id: Optional[int] = None, 
                              contact_info: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Genera una respuesta a partir del mensaje del usuario usando Qwen.
        
        Args:
            user_message: Mensaje del usuario
            conversation_id: ID de la conversación (opcional)
            contact_info: Información del contacto (opcional)
            
        Returns:
            Dict con la respuesta generada y metadatos
        """
        logger.info(f"Generando respuesta para el mensaje: {user_message}")
        
        # Si no hay clave API, devolver un mensaje indicando que se necesita configurar
        if not self.api_key:
            logger.warning("No hay clave API, mostrando mensaje de configuración")
            response_text = "Para utilizar el agente de inteligencia artificial, necesitas configurar una clave API válida de DashScope. Por favor, visita https://dashscope.console.aliyuncs.com/ para obtener una clave y configúrala en el archivo .env."
            
            # Agregar respuesta al historial
            self.conversation_history.append({
                'role': 'user',
                'content': user_message
            })
            self.conversation_history.append({
                'role': 'assistant',
                'content': response_text
            })
            
            return {
                'success': True,
                'response': response_text,
                'metadata': {
                    'model': 'no-api-key',
                    'tokens_used': 0,
                    'context_used': []
                }
            }
        
        try:
            # Añadir el mensaje del usuario al historial
            self.conversation_history.append({
                'role': 'user',
                'content': user_message
            })
            
            # Generar respuesta usando el modelo
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                temperature=float(os.getenv('MODEL_TEMPERATURE', 0.7)),
                max_tokens=int(os.getenv('MODEL_MAX_TOKENS', 256))  # Reducido para respuestas más concisas
            )
            
            # Extraer la respuesta del modelo
            response_text = response.choices[0].message.content
            tokens_used = response.usage.total_tokens if response.usage else 0
            
            logger.info(f"Respuesta del modelo: {response_text}")
            
            # Formatear la respuesta para que parezca más natural
            formatted_response = format_response(response_text)
            
            # Añadir la respuesta al historial
            self.conversation_history.append({
                'role': 'assistant',
                'content': formatted_response
            })
            
            # Limitar el historial a las últimas 10 interacciones para evitar context overflow
            if len(self.conversation_history) > 10:
                # Mantener el mensaje del sistema y las últimas 9 interacciones
                self.conversation_history = [self.conversation_history[0]] + self.conversation_history[-9:]
            
            return {
                'success': True,
                'response': formatted_response,
                'metadata': {
                    'model': self.model,
                    'tokens_used': tokens_used,
                    'context_used': [msg['content'] for msg in self.conversation_history]
                }
            }
            
        except Exception as e:
            logger.error(f"Error al generar respuesta: {e}")
            return {
                'success': False,
                'response': "Lo siento, estoy teniendo dificultades técnicas en este momento. ¿Podrías intentar de nuevo más tarde?",
                'error': str(e)
            }
    
    def reset_conversation(self):
        """Reinicia la conversación."""
        self._initialize_system_prompt()
        return {'success': True, 'message': 'Conversación reiniciada'}

    def process_chat_message(self, message: str, phone: str, name: Optional[str] = None, db=None):
        """
        Process a chat message and return the response.
        """
        # If no database session provided, create one
        if db is None:
            db = SessionLocal()
            
        try:
            # Get or create contact
            contact = db.query(Contact).filter(Contact.phone == phone).first()
            if not contact:
                contact = Contact(
                    name=name or "Cliente",
                    phone=phone,
                    interest_level=InterestLevel.NEW
                )
                db.add(contact)
                db.commit()
                db.refresh(contact)
            
            # Create or get conversation
            conversation = db.query(Conversation).filter(Conversation.contact_id == contact.id).first()
            if not conversation:
                conversation = Conversation(contact_id=contact.id)
                db.add(conversation)
                db.commit()
                db.refresh(conversation)
            
            # Add user message to conversation
            user_message = Message(
                conversation_id=conversation.id,
                sender="user",
                content=message
            )
            db.add(user_message)
            db.commit()
            
            # Get conversation history
            messages = db.query(Message).filter(
                Message.conversation_id == conversation.id
            ).order_by(Message.created_at).all()
            
            # Convert to the format expected by the LLM
            formatted_messages = [
                {"role": "system", "content": self.system_prompt}
            ]
            
            # Add conversation history (limit to last 10 messages to prevent context overflow)
            for msg in messages[-10:]:
                formatted_messages.append({
                    "role": "user" if msg.sender == "user" else "assistant",
                    "content": msg.content
                })
            
            # Get response from LLM using the real API
            try:
                # Use actual LLM API for generating response
                response = self._get_llm_response(formatted_messages)
                
                # Save assistant response to database
                assistant_message = Message(
                    conversation_id=conversation.id,
                    sender="agent",
                    content=response
                )
                db.add(assistant_message)
                db.commit()
                
                return {
                    "response": response,
                    "contact_id": contact.id,
                    "message_id": assistant_message.id
                }
            except Exception as e:
                logger.error(f"Error al obtener respuesta de LLM: {e}")
                # Fallback response
                response = "Gracias por tu mensaje. Estoy aquí para ayudarte con cualquier pregunta sobre nuestros servicios."
                
                # Save assistant response to database
                assistant_message = Message(
                    conversation_id=conversation.id,
                    sender="agent",
                    content=response
                )
                db.add(assistant_message)
                db.commit()
                
                return {
                    "response": response,
                    "contact_id": contact.id,
                    "message_id": assistant_message.id
                }
                
        except Exception as e:
            db.rollback()
            logger.error(f"Error al procesar mensaje de chat: {e}")
            raise e
        finally:
            if db is SessionLocal():
                db.close()
    
    def _get_llm_response(self, messages: List[Dict[str, str]]) -> str:
        """
        Get response from LLM using the real API.
        This is a synchronous version for use in non-async contexts.
        """
        try:
            # Get response from LLM
            response = self.sync_client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=float(os.getenv('MODEL_TEMPERATURE', 0.7)),
                max_tokens=int(os.getenv('MODEL_MAX_TOKENS', 256))  # Reducido para respuestas más concisas
            )
            
            # Extract response text
            response_text = response.choices[0].message.content
            
            # Format response to make it more natural
            formatted_response = format_response(response_text)
            
            return formatted_response
            
        except Exception as e:
            logger.error(f"Error al obtener respuesta de LLM: {e}")
            # Return a fallback response
            return "Gracias por tu mensaje. ¿Podrías proporcionar más detalles sobre tu consulta para poder ayudarte mejor?"

# Instancia global del servicio
llm_service = LLMService()