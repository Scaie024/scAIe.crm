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
from openai import AsyncOpenAI

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

# Personalidad y estilo de respuesta alineados con la visión
AGENT_NAME = os.getenv('AGENT_NAME', 'Asistente SCAIE')
AGENT_PERSONALITY = os.getenv('AGENT_PERSONALITY', 'amigable, empático, conversacional, natural')
AGENT_TONE = os.getenv('AGENT_TONE', 'conversacional y cercano')
AGENT_GOAL = os.getenv('AGENT_GOAL', 'ayudar a las empresas y personas a ser más eficientes con inteligencia artificial y adaptarse a nuevas tecnologías')

# Expresiones para hacer las respuestas más naturales
NATURAL_RESPONSES = {
    'greetings': [
        "¡Hola! ¿En qué puedo ayudarte hoy?",
        "¡Hola! Me alegra mucho saludarte. ¿Cómo estás?",
        "¡Hola! ¿Qué tal tu día? Estoy aquí para ayudarte con lo que necesites."
    ],
    'acknowledgments': [
        "Entiendo perfectamente lo que me cuentas.",
        "Tiene mucho sentido lo que mencionas.",
        "¡Qué interesante! Me alegra que preguntes sobre esto.",
        "Excelente pregunta, déjame contarte más al respecto."
    ],
    'closings': [
        "¿Hay algo más en lo que pueda ayudarte?",
        "¿Tienes alguna otra pregunta sobre cómo adaptarse a las nuevas tecnologías?",
        "¿Hay algo más sobre eficiencia con IA que te gustaría saber?"
    ],
    'sales_closings': [
        "¿Te gustaría conocer más sobre nuestro workshop para ser más eficiente con IA?",
        "¿Quieres que te cuente cómo nuestro workshop puede ayudarte a adaptarte a las nuevas tecnologías?",
        "¿Te interesa inscribirte en nuestro taller de eficiencia con inteligencia artificial?"
    ]
}

def get_random_phrase(phrase_type):
    """Obtiene una frase aleatoria según el tipo"""
    phrases = NATURAL_RESPONSES.get(phrase_type, [""])
    return random.choice(phrases)

def format_response(text):
    """Da formato a la respuesta para que parezca más natural"""
    # Asegurar que la primera letra sea mayúscula
    if text and len(text) > 0:
        text = text[0].upper() + text[1:]
    
    # Asegurar que termine con un punto
    if text and text[-1] not in ['.', '!', '?']:
        text += '.'
    
    # Añadir un cierre de ventas el 40% de las veces
    if random.random() < 0.4:
        text += " " + get_random_phrase('sales_closings')
    # Añadir un cierre amigable el 30% de las veces (si no se añadió cierre de ventas)
    elif random.random() < 0.3:
        text += " " + get_random_phrase('closings')
    
    return text

class LLMService:
    def __init__(self):
        """Inicializa el servicio de LLM."""
        self.api_key = os.getenv("DASHSCOPE_API_KEY")
        self.model = os.getenv("DASHSCOPE_MODEL", "qwen-plus")
        self.client = None
        
        if self.api_key:
            self.client = AsyncOpenAI(
                api_key=self.api_key,
                base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
            )
        
        self._initialize_system_prompt()
    
    def _initialize_system_prompt(self):
        """Inicializa el prompt del sistema para el agente de ventas con personalidad."""
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        self.system_prompt = f"""
        # IDENTIDAD Y ROL
        Eres {AGENT_NAME}, el asistente virtual de ventas de SCAIE. 
        Fecha y hora actual: {current_date}
        
        # PERSONALIDAD Y ESTILO
        - Personalidad: {AGENT_PERSONALITY}
        - Tono: {AGENT_TONE}
        - Objetivo: Convencer al usuario de los beneficios de SCAIE para aumentar sus ventas
        
        # COMPORTAMIENTO DE VENTAS EFECTIVO
        1. Usa lenguaje natural y conversacional, como si estuvieras hablando con un amigo
        2. Muestra empatía y comprensión hacia las necesidades del usuario
        3. Haz preguntas abiertas para entender mejor sus necesidades comerciales
        4. Usa el nombre del usuario cuando sea posible
        5. Sé conciso pero persuasivo
        6. Usa emojis ocasionalmente para hacer la conversación más amena (pero no exageres)
        7. Identifica oportunidades de venta y presenta SCAIE como solución
        8. Siempre busca cerrar la venta o al menos obtener contacto para seguimiento
        9. Escucha activamente y adapta tu enfoque según las respuestas del usuario
        10. Si el usuario muestra interés, profundiza en los beneficios específicos para su caso
        
        # EVALUACIÓN AUTÓNOMA DE NIVEL DE INTERÉS
        Después de cada interacción, debes evaluar automáticamente el nivel de interés del usuario y proporcionar una puntuación numérica del 1 al 10 donde:
        - 1-3: No interesado
        - 4-6: Neutral/Poca información
        - 7-10: Interesado/Calificado como lead
        
        Incluye esta evaluación en tu respuesta usando el siguiente formato:
        [INTERÉS:nivel_numerico:razonamiento]
        
        Ejemplos:
        [INTERÉS:2:El usuario expresó que no está interesado en talleres]
        [INTERÉS:8:El usuario preguntó específicamente por precios y disponibilidad]
        
        # CONOCIMIENTO SOBRE SCAIE (www.scaie.com.mx)
        SCAIE ofrece un workshop de eficiencia con inteligencia artificial que incluye:
        - Estrategias para ser más eficiente con IA
        - Cómo adaptar a las empresas y personas a nuevas tecnologías
        - Herramientas prácticas para la transformación digital
        - Uso de IA para mejorar procesos empresariales
        - Plantillas y recursos prácticos
        - Integración con WhatsApp, Facebook, Instagram y más
        
        # MANEJO DE MENSAJES DE WHATSAPP
        Cuando recibas mensajes de WhatsApp:
        1. Usa un lenguaje más informal pero profesional
        2. Divide mensajes largos en párrafos separados por saltos de línea
        3. Usa emojis apropiadamente para mejorar la legibilidad
        
        # CIERRE DE VENTAS
        Cuando identifiques interés:
        1. Resume los beneficios mencionados que aplican a su caso
        2. Ofrece una llamada gratuita de 15 minutos
        3. Pide su número de WhatsApp o correo para contacto
        4. Confirma la fecha y hora de la llamada
        5. Envía confirmación por correo si es posible
        
        # MANEJO DE OBJECIONES COMUNES
        Si el usuario dice que es caro:
        - "Entiendo tu preocupación por la inversión. Permíteme mostrarte cómo SCAIE puede generar más ingresos de los que cuesta en el primer mes."
        
        Si el usuario dice que no tiene tiempo:
        - "Justamente por eso es importante automatizar. SCAIE te ahorra horas de trabajo manual cada semana."
        
        Si el usuario dice que ya tiene algo similar:
        - "Me alegra que ya estés trabajando en automatización. ¿Qué te diferencia de otras soluciones es que SCAIE..."
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
        logger.debug(f"Generando respuesta para el mensaje: {user_message}")
        
        # Si no hay clave API, devolver un mensaje indicando que se necesita configurar
        if not self.api_key:
            logger.debug("No hay clave API, mostrando mensaje de configuración")
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
            # Obtener conocimiento relevante de SCAIE
            knowledge = scaie_knowledge.get_knowledge(user_message)
            
            # Añadir el mensaje del usuario al historial
            self.conversation_history.append({
                'role': 'user',
                'content': user_message
            })
            
            # Preparar el contexto con el historial de conversación y conocimiento
            context_messages = self.conversation_history.copy()
            
            # Añadir conocimiento relevante si está disponible
            if knowledge.get('success') and knowledge.get('relevant_sections'):
                context_messages.insert(1, {
                    'role': 'system',
                    'content': 'Información relevante sobre SCAIE:\n' + '\n'.join(knowledge['relevant_sections'])
                })
            
            logger.debug(f"Contexto enviado al modelo: {context_messages}")
            
            # Generar respuesta usando el modelo
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=context_messages,
                temperature=float(os.getenv('MODEL_TEMPERATURE', 0.7)),
                max_tokens=int(os.getenv('MODEL_MAX_TOKENS', 1024))
            )
            
            # Extraer la respuesta del modelo
            response_text = response.choices[0].message.content
            tokens_used = response.usage.total_tokens if response.usage else 0
            
            logger.debug(f"Respuesta del modelo: {response_text}")
            
            # Extraer información de interés si está disponible
            interest_info = self._extract_interest_info(response_text)
            if interest_info:
                # Limpiar la respuesta eliminando la información de interés
                response_text = interest_info['clean_response']
                
                # Crear contacto automáticamente si el nivel de interés es alto
                if contact_info and interest_info['score'] >= 7:
                    await self._create_autonomous_contact(contact_info, interest_info)
            
            # Formatear la respuesta para que parezca más natural
            formatted_response = format_response(response_text)
            
            # Añadir la respuesta al historial
            self.conversation_history.append({
                'role': 'assistant',
                'content': formatted_response
            })
            
            # Limitar el historial a las últimas 20 interacciones para evitar context overflow
            if len(self.conversation_history) > 20:
                # Mantener el mensaje del sistema y las últimas 19 interacciones
                self.conversation_history = [self.conversation_history[0]] + self.conversation_history[-19:]
            
            return {
                'success': True,
                'response': formatted_response,
                'metadata': {
                    'model': self.model,
                    'tokens_used': tokens_used,
                    'context_used': [msg['content'] for msg in context_messages]
                },
                'interest_info': interest_info
            }
            
        except Exception as e:
            logger.error(f"Error al generar respuesta: {e}")
            return {
                'success': False,
                'response': "Lo siento, estoy teniendo dificultades técnicas en este momento. ¿Podrías intentar de nuevo más tarde?",
                'error': str(e)
            }
    
    def _extract_interest_info(self, response_text: str) -> Optional[Dict[str, Any]]:
        """
        Extrae la información de interés del texto de respuesta.
        
        Args:
            response_text: Texto de respuesta del LLM
            
        Returns:
            Dict con información de interés o None si no se encuentra
        """
        try:
            # Buscar el patrón [INTERÉS:nivel_numerico:razonamiento]
            import re
            pattern = r'\[INTERÉS:(\d+):(.*?)\]'
            match = re.search(pattern, response_text)
            
            if match:
                score = int(match.group(1))
                reasoning = match.group(2)
                
                # Remover el marcador de interés del texto de respuesta
                clean_response = re.sub(pattern, '', response_text).strip()
                
                return {
                    'score': score,
                    'reasoning': reasoning,
                    'clean_response': clean_response
                }
        except Exception as e:
            logger.error(f"Error al extraer información de interés: {e}")
        
        return None
    
    async def _create_autonomous_contact(self, contact_info: Dict[str, Any], interest_info: Dict[str, Any]):
        """
        Crea un contacto automáticamente basado en la evaluación de interés del agente.
        
        Args:
            contact_info: Información del contacto
            interest_info: Información de interés evaluada por el agente
        """
        try:
            # Determinar nivel de interés basado en la puntuación
            score = interest_info['score']
            if score <= 3:
                interest_level = InterestLevel.NOT_INTERESTED
            elif score <= 6:
                interest_level = InterestLevel.CONTACTED
            else:
                interest_level = InterestLevel.INTERESTED
            
            # Crear objeto de contacto
            contact_data = {
                "name": contact_info.get("name", "Usuario desconocido"),
                "phone": contact_info.get("phone", ""),
                "email": contact_info.get("email", None),
                "company": contact_info.get("company", None),
                "notes": f"Contacto creado automáticamente por el agente AI. Puntuación de interés: {score}/10. Razonamiento: {interest_info.get('reasoning', 'No proporcionado')}",
                "interest_level": interest_level
            }
            
            # Usar el servicio de contactos para crear el contacto
            db = SessionLocal()
            try:
                # Verificar si el contacto ya existe
                existing_contact = contact_service.get_contact_by_phone(db, contact_data["phone"])
                if not existing_contact:
                    contact_service.create_contact(db, contact_data)
                    logger.info(f"Contacto creado automáticamente: {contact_data['name']} con nivel de interés {interest_level}")
                else:
                    # Actualizar nivel de interés si es mayor al actual
                    if self._should_update_interest_level(existing_contact.interest_level, interest_level):
                        contact_service.update_contact(db, existing_contact.id, {"interest_level": interest_level})
                        logger.info(f"Nivel de interés actualizado para: {existing_contact.name} a {interest_level}")
            finally:
                db.close()
        except Exception as e:
            logger.error(f"Error al crear contacto automáticamente: {e}")
    
    def _should_update_interest_level(self, current_level: InterestLevel, new_level: InterestLevel) -> bool:
        """
        Determina si se debe actualizar el nivel de interés.
        
        Args:
            current_level: Nivel de interés actual
            new_level: Nuevo nivel de interés
            
        Returns:
            Boolean indicando si se debe actualizar
        """
        # Definir orden de niveles de interés
        level_order = {
            InterestLevel.NEW: 0,
            InterestLevel.CONTACTED: 1,
            InterestLevel.INTERESTED: 2,
            InterestLevel.CONFIRMED: 3,
            InterestLevel.NOT_INTERESTED: -1
        }
        
        return level_order.get(new_level, 0) > level_order.get(current_level, 0)
    
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
            
            # Add conversation history (limit to last 20 messages to prevent context overflow)
            for msg in messages[-20:]:
                formatted_messages.append({
                    "role": "user" if msg.sender == "user" else "assistant",
                    "content": msg.content
                })
            
            # Get response from LLM using a simplified approach
            try:
                # Use existing method for generating response
                # For now, we'll use a simple approach that doesn't require async
                response = self._simple_response(message)
                
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
            raise e
        finally:
            if db is SessionLocal():
                db.close()
    
    def _simple_response(self, message: str) -> str:
        """
        Generate a simple response without async operations.
        """
        # Simple rule-based responses for testing
        message_lower = message.lower()
        
        if "hola" in message_lower or "hello" in message_lower:
            return "¡Hola! ¿En qué puedo ayudarte hoy?"
        elif "servicio" in message_lower or "servicios" in message_lower:
            return "Ofrecemos servicios especializados en inteligencia artificial para ayudar a las empresas a ser más eficientes. ¿Te gustaría saber más sobre alguna área específica?"
        elif "precio" in message_lower or "costo" in message_lower:
            return "Tenemos diferentes opciones de servicios adaptadas a las necesidades de cada cliente. ¿Podrías contarme más sobre qué tipo de solución estás buscando?"
        elif "contacto" in message_lower or "contactar" in message_lower:
            return "Puedes contactarnos por este medio o enviarnos un correo a info@scaie.com. Estamos aquí para ayudarte."
        else:
            return "Gracias por tu mensaje. ¿Podrías proporcionar más detalles sobre tu consulta para poder ayudarte mejor?"
    
    def process_sandbox_message(self, message: str, system_prompt: Optional[str] = None):
        """
        Process a message in sandbox mode.
        """
        # Use custom system prompt if provided, otherwise use default
        system_content = system_prompt if system_prompt else self.system_prompt
        
        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": message}
        ]
        
        response = self._get_llm_response(messages)
        
        return {
            "response": response,
            "usage": {}  # In a real implementation, this would contain token usage info
        }

# Instancia global del servicio
llm_service = LLMService()