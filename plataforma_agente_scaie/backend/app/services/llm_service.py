import os
import asyncio
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv
import json
import random
from datetime import datetime
import logging
from .scaie_knowledge import scaie_knowledge
from openai import AsyncOpenAI

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

# Personalidad y estilo de respuesta
AGENT_NAME = os.getenv('AGENT_NAME', 'SCAI')
AGENT_PERSONALITY = os.getenv('AGENT_PERSONALITY', 'amigable, empático, profesional, persuasivo')
AGENT_TONE = os.getenv('AGENT_TONE', 'coloquial pero respetuoso')
AGENT_GOAL = os.getenv('AGENT_GOAL', 'ayudar a los usuarios a entender los beneficios de SCAIE de manera natural')

# Expresiones para hacer las respuestas más naturales
NATURAL_RESPONSES = {
    'greetings': [
        "¡Hola! ¿En qué puedo ayudarte hoy?",
        "¡Hola! Me alegra verte por aquí. ¿Cómo estás?",
        "¡Hola! ¿Cómo va tu día? Estoy aquí para ayudarte con lo que necesites."
    ],
    'acknowledgments': [
        "Entiendo perfectamente lo que dices.",
        "Tiene mucho sentido lo que mencionas.",
        "¡Qué interesante! Me alegra que menciones eso.",
        "Excelente punto, déjame contarte más al respecto."
    ],
    'closings': [
        "¿Hay algo más en lo que pueda ayudarte?",
        "¿Tienes alguna otra pregunta sobre SCAIE?",
        "¿Hay algo más sobre lo que te gustaría saber?"
    ],
    'sales_closings': [
        "¿Te gustaría agendar una sesión gratuita para probar SCAIE?",
        "¿Quieres que te contacte un experto para mostrarte cómo SCAIE puede aumentar tus ventas?",
        "¿Te interesa inscribirte en nuestro taller gratuito de automatización de ventas?"
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
        """Inicializa el servicio de lenguaje con Qwen."""
        # Configurar credenciales
        self.initialized = True
        self.api_key = os.getenv('DASHSCOPE_API_KEY')
        
        # Verificar si se proporcionó una clave API
        if not self.api_key or self.api_key.strip() == "":
            logger.warning("No se ha proporcionado una clave API de DashScope")
            self.api_key = None
            self.demo_mode = True
        else:
            # Registro de depuración
            logger.debug(f"Usando API Key: {self.api_key[:5]}...{self.api_key[-5:]}")
            self.demo_mode = False
        
        # Configuración del cliente OpenAI (solo si hay clave API)
        if self.api_key:
            self.client = AsyncOpenAI(
                api_key=self.api_key,
                base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
            )
        else:
            self.client = None
        
        # Modelo Qwen a usar
        self.model_name = os.getenv('QWEN_MODEL', 'qwen-plus')
        
        # Configuración de generación optimizada para ventas
        self.generation_config = {
            'temperature': float(os.getenv('TEMPERATURE', 0.8)),  # Más creatividad para ventas
            'max_tokens': int(os.getenv('MAX_TOKENS', 1024)),  # Menos tokens para reducir costos
            'top_p': float(os.getenv('TOP_P', 0.9)),
            'top_k': int(os.getenv('TOP_K', 30)),
        }
        
        # Historial de conversación
        self.conversation_history = []
        
        # Inicializar con el prompt del sistema
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
        
        # CONOCIMIENTO SOBRE SCAIE (www.scaie.com.mx)
        SCAIE ofrece un workshop de automatización de ventas que incluye:
        - Estrategias de ventas automatizadas que pueden aumentar las ventas hasta un 300%
        - Herramientas para captación y cualificación de leads
        - Uso de IA para mejorar la conversión
        - Plantillas y recursos prácticos
        - Integración con WhatsApp, Facebook, Instagram y más
        
        # TÉCNICAS DE VENTA
        - Escucha activa para identificar necesidades del cliente
        - Presenta SCAIE como solución específica a sus problemas
        - Usa testimonios y casos de éxito cuando sea relevante
        - Ofrece pruebas gratuitas o sesiones de demostración
        - Maneja objeciones con empatía y argumentos sólidos
        - Busca siempre obtener contacto para seguimiento
        
        # DIRECTRICES IMPORTANTES
        - NUNCA inventes información sobre precios o características que no estés seguro
        - Si no sabes algo, ofrécete a buscar la información o conectar al usuario con un experto
        - Mantén las respuestas enfocadas en cómo SCAIE puede aumentar las ventas del usuario
        - Usa el conocimiento de www.scaie.com.mx para dar respuestas precisas y útiles
        - Siempre busca una oportunidad para presentar SCAIE como solución
        - Si el usuario menciona un problema específico, enfócate en cómo SCAIE lo resuelve
        
        # EJEMPLOS DE RESPUESTAS EFECTIVAS
        Buenas respuestas:
        - "¡Hola! Me alegra que estés interesado en SCAIE. 😊 ¿En qué puedo ayudarte hoy?"
        - "Entiendo que quieres mejorar tus ventas. El workshop de SCAIE podría ser justo lo que necesitas. ¿Te gustaría que te cuente más?"
        - "¡Excelente pregunta! Según lo que sé de SCAIE, puedo contarte que..."
        - "Muchos emprendedores han duplicado sus ventas en solo 30 días usando SCAIE. ¿Te gustaría saber cómo pueden ayudarte a ti?"
        
        Malas respuestas:
        - "No sé la respuesta a eso."
        - "Lo siento, no puedo ayudarte con eso."
        - Respuestas genéricas sin personalización
        
        # TÉCNICA DE CIERRE DE VENTAS
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
    
    async def generate_response(self, user_message: str) -> Dict[str, Any]:
        """
        Genera una respuesta a partir del mensaje del usuario usando Qwen.
        
        Args:
            user_message: Mensaje del usuario
            
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
            logger.debug(f"Conocimiento obtenido: {knowledge}")
            
            # Crear contexto con la información relevante
            context_parts = []
            if knowledge.get('success', False) and knowledge.get('relevant_sections'):
                context_parts.append("Información relevante de SCAIE (usa esto para responder de manera precisa pero natural):")
                for i, section in enumerate(knowledge['relevant_sections'][:3], 1):
                    context_parts.append(f"- {section}")
            
            context = '\n'.join(context_parts) if context_parts else "No se encontró información específica, pero sé que SCAIE puede ayudar con automatización de ventas."
            
            # Crear el mensaje con contexto de manera más natural
            message_with_context = f"""
            [MENSAJE DEL USUARIO]
{user_message}

            [INFORMACIÓN DE CONTEXTO]
{context}

            [INSTRUCCIONES]
            - Responde de manera natural y conversacional
            - Muestra empatía y comprensión
            - Usa la información del contexto para dar una respuesta precisa pero natural
            - NO menciones que estás usando información del contexto
            - Mantén un tono {AGENT_TONE}
            - Sé {AGENT_PERSONALITY}
            - Tu objetivo es convencer al usuario de los beneficios de SCAIE para aumentar sus ventas
            - Siempre busca una oportunidad para presentar SCAIE como solución
            - Si es apropiado, invita al usuario a agendar una sesión gratuita o demostración
            - Si el usuario menciona un problema específico, enfócate en cómo SCAIE lo resuelve
            - Si detectas interés, aplica técnicas de cierre de ventas
            """
            
            # Agregar mensaje del usuario con contexto al historial
            messages = self.conversation_history.copy()
            messages.append({
                'role': 'user',
                'content': message_with_context
            })
            
            logger.debug(f"Enviando solicitud a Qwen con {len(messages)} mensajes en el historial")
            
            # Generar respuesta con Qwen
            try:
                completion = await self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    temperature=self.generation_config['temperature'],
                    max_tokens=self.generation_config['max_tokens'],
                    top_p=self.generation_config['top_p']
                )
                
                logger.debug(f"Resultado de Qwen: {completion}")
                
                # Obtener y formatear la respuesta
                response_text = completion.choices[0].message.content
                
                # Dar formato a la respuesta para que sea más natural
                response_text = format_response(response_text)
                
                # Agregar respuesta al historial (sin el contexto para mantenerlo limpio)
                self.conversation_history.append({
                    'role': 'user',
                    'content': user_message  # Reemplazar con el mensaje original
                })
                self.conversation_history.append({
                    'role': 'assistant',
                    'content': response_text
                })
                
                return {
                    'success': True,
                    'response': response_text,
                    'metadata': {
                        'model': self.model_name,
                        'tokens_used': completion.usage.total_tokens if completion.usage else len(response_text.split()),
                        'context_used': knowledge.get('relevant_sections', [])
                    }
                }
            except Exception as e:
                logger.error(f"Error al llamar a Qwen: {e}")
                print(f"Error al llamar a Qwen: {e}")
                if "invalid_api_key" in str(e).lower():
                    # En caso de error de autenticación, usar modo demo
                    logger.warning("API Key no válida, usando modo demo")
                    return await self._generate_demo_response(user_message)
                
                return {
                    'success': False,
                    'error': f'Error: {e}',
                    'response': 'Lo siento, ha ocurrido un error al procesar tu solicitud. ¿Podrías intentar reformular tu pregunta?'
                }
            
        except Exception as e:
            logger.error(f"Error al generar respuesta: {e}")
            print(f"Error al generar respuesta: {e}")
            # En caso de cualquier error, usar modo demo
            return await self._generate_demo_response(user_message)
    
    async def _generate_demo_response(self, user_message: str) -> Dict[str, Any]:
        """Genera una respuesta de demostración cuando hay errores."""
        # Esta función ya no se usa ya que ahora mostramos mensajes específicos sobre la API
        # cuando no hay clave o es inválida
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
    
    def reset_conversation(self):
        """Reinicia la conversación."""
        self._initialize_system_prompt()
        return {'success': True, 'message': 'Conversación reiniciada'}

# Instancia global del servicio
llm_service = LLMService()