import os
import sys
import logging
from dotenv import load_dotenv
import asyncio
from typing import Dict, Any, Optional, List

# Load environment variables from .env file (no secret printing)
env_path = os.path.join(os.path.dirname(__file__), "../../../../../.env")
if os.path.exists(env_path):
    load_dotenv(env_path)

# Dashscope imports
try:
    import dashscope
    from dashscope import Generation
    DASHSCOPE_AVAILABLE = True
except ImportError:
    DASHSCOPE_AVAILABLE = False
    print("DashScope not available. Using fallback responses.")

# Import RAG service
try:
    from .rag_service import rag_service
    RAG_AVAILABLE = True
except ImportError:
    RAG_AVAILABLE = False
    print("RAG service not available. Using basic knowledge base.")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
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

# Initialize OpenAI client (DashScope-compatible)
DISABLE_LLM = os.getenv("DISABLE_LLM", "false").lower() in ("1", "true", "yes")
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
api_key = DASHSCOPE_API_KEY
base_url = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"

# Set api_key to None if not found
if not DASHSCOPE_API_KEY:
    logger.warning("DASHSCOPE_API_KEY not found in environment variables; LLM responses will be disabled")
    client = None

try:
    if api_key and not DISABLE_LLM:
        client = AsyncOpenAI(
            api_key=api_key,
            base_url=base_url
        )
        logger.info("LLM client initialized successfully")
    else:
        if DISABLE_LLM:
            logger.warning("LLM is disabled via DISABLE_LLM env var; using fallback responses")
        else:
            logger.error("DASHSCOPE_API_KEY not found in environment variables; LLM responses will be disabled")
        client = None
except Exception as e:
    logger.error(f"Error initializing LLM client: {str(e)}", exc_info=True)  # Added exc_info for detailed traceback
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
            response = self._check_predefined_responses(message, contact)
            if response:
                return {
                    'success': True,
                    'response': response,
                    'contact_id': contact.id if contact else None
                }
        
            # Generate response using LLM
            system_prompt = self._create_system_prompt(contact)
            user_prompt = self._create_user_prompt(message, contact)
            
            if not self.client:
                logger.warning("LLM client not initialized - using fallback response")
                return {
                    'success': False,
                    'error': 'LLM client not initialized',
                    'response': 'Lo siento, el servicio de IA no está disponible en este momento. Por favor, comunícate al 5535913417 para obtener asistencia.'
                }
            
            # Call with a modest timeout to avoid hanging during local runs
            try:
                response = await self.client.chat.completions.create(
                    model=os.getenv('QWEN_MODEL', 'qwen-plus'),
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=float(os.getenv('TEMPERATURE', '0.9')),  # Más creativo/natural
                    max_tokens=int(os.getenv('MAX_TOKENS', '512'))       # Respuestas más cortas
                )
            except Exception as e:
                # Specific handling for HTTP 501 error
                if getattr(e, 'status_code', None) == 501:
                    logger.error(f"HTTP 501 error calling LLM API: {str(e)}", exc_info=True)
                    return {
                        'success': False,
                        'error': 'HTTP 501 error',
                        'response': 'Lo siento, estamos experimentando problemas temporales con nuestro servicio de IA. Por favor, inténtalo de nuevo más tarde.'
                    }
                else:
                    logger.error(f"Error calling LLM API: {str(e)}", exc_info=True)  # Added exc_info for detailed traceback
                    raise
            
            ai_response = response.choices[0].message.content
            
            # Format response
            formatted_response = format_response(ai_response)
            
            return {
                'success': True,
                'response': formatted_response,
                'contact_id': contact.id if contact else None
            }
            
        except RateLimitError as e:
            logger.error(f"Rate limit error: {e}")
            return {
                'success': False,
                'error': str(e),
                'response': 'Demasiadas solicitudes. Por favor, inténtalo de nuevo en unos momentos.'
            }
        except APIError as e:
            logger.error(f"OpenAI API error: {e}")
            return {
                'success': False,
                'error': str(e),
                'response': 'Lo siento, estoy experimentando dificultades técnicas. Por favor, inténtalo de nuevo más tarde o comunícate al 5535913417.'
            }
        except Exception as e:
            logger.error(f"Unexpected error generating response: {e}", exc_info=True)
            return {
                'success': False,
                'error': str(e),
                'response': 'Lo siento, ha ocurrido un error inesperado. Por favor, comunícate al 5535913417 para obtener asistencia.'
            }
    
    def _check_predefined_responses(self, message: str, contact: Optional[Contact] = None) -> Optional[str]:
        """
        Check for keywords that require predefined responses.
        
        Args:
            message: Incoming message text
            contact: Contact object (optional)
            
        Returns:
            Predefined response or None
        """
        message_lower = message.lower()

        # Friendly greeting for first-contact style
        greeting_keywords = [
            "hola", "buenas", "buen dia", "buen día", "que tal", "qué tal", "hey", "hi", "saludos"
        ]
        if any(gk in message_lower for gk in greeting_keywords):
            return "¡Hola! 👋 Soy SCAI, tu asistente de IA. ¿Quieres que tu equipo trabaje más eficiente? Te ayudo a automatizar tareas en minutos. ¿De qué área es tu equipo?"
        
        # Contact information keywords
        contact_keywords = [
            "humano", "persona", "asesor", "cotizacion", "cotización", 
            "precio específico", "precio personalizado", "hablar con alguien"
        ]
        
        if any(keyword in message_lower for keyword in contact_keywords):
            return f"Perfecto, te conecto con un experto. 📞 Llama al {self.workshop_knowledge['detalles_contacto']['telefono']} o agenda una llamada gratuita aquí: {self.workshop_knowledge['detalles_contacto']['calendly']}"
        
        # Scheduling keywords
        schedule_keywords = [
            "agendar", "cita", "llamada", "reunión", "consultoría", 
            "sesión", "entrevista", "conversar"
        ]
        
        if any(keyword in message_lower for keyword in schedule_keywords):
            return f"¡Genial! 📅 Agenda tu llamada gratuita de 15 minutos aquí: {self.workshop_knowledge['detalles_contacto']['calendly']}. ¿A qué hora te viene mejor?"
        
        # Website keywords
        website_keywords = [
            "más información", "detalles", "sitio web", "página web", 
            "información adicional", "ver más"
        ]
        
        if any(keyword in message_lower for keyword in website_keywords):
            return f"Te dejo más info en: {self.workshop_knowledge['detalles_contacto']['sitio_web']}. ¿Hay algo específico que te interese saber?"
        
        # Objection handling (concise)
        objs = self.workshop_knowledge.get("objecciones", {})
        for key, cfg in objs.items():
            if any(k in message_lower for k in cfg.get("keywords", [])):
                return cfg.get("respuesta")

        # Role-based quick value hints
        roles = self.workshop_knowledge.get("casos_uso_por_rol", {})
        for role, ideas in roles.items():
            if role in message_lower:
                top = ", ".join(ideas[:2])
                return f"Para {role}: {top}. ¿Cuál te ayudaría más esta semana?"

        # Daily tasks examples when user asks "para qué" or similar
        if any(k in message_lower for k in ["para que", "para qué", "como me ayuda", "tareas", "diario", "cotidianas"]):
            tareas = self.workshop_knowledge.get("tareas_diarias_ejemplos", [])
            if tareas:
                return f"Ejemplos rápidos: {tareas[0]}, {tareas[1]}. ¿Cuál haces más seguido?"

        # Free tools recommendations
        if any(k in message_lower for k in ["gratis", "free", "herramientas", "empiezo", "comenzar"]):
            tools = self.workshop_knowledge.get('herramientas_gratuitas', {})
            texto = ", ".join(tools.get('texto', [])[:2]) if isinstance(tools.get('texto', []), list) else "ChatGPT o Claude"
            auto = ", ".join(tools.get('automatizacion', [])[:1]) if isinstance(tools.get('automatizacion', []), list) else "Make/Zapier"
            return f"Empieza con {texto} y {auto}. En 2h te dejo 2–3 flujos listos. ¿Texto o automatizar primero?"

        # Models guidance
        if any(k in message_lower for k in ["modelos", "chatgpt", "claude", "mistral", "gemini"]):
            return "Todos sirven; lo importante es tu flujo. Vemos tu caso y elegimos el modelo. ¿Qué tarea quieres resolver primero?"

        # Trends: RAG, vision
        if any(k in message_lower for k in ["rag", "documentos", "pdf", "visión", "vision", "imagenes", "imágenes", "ocr"]):
            t = self.workshop_knowledge.get('temas_tendencia', {})
            rag = t.get('rag', 'conectar tus documentos a la IA (RAG)')
            vis = t.get('vision', 'analizar imágenes y PDFs')
            return f"Hacemos {rag} y {vis} con plantillas simples. ¿Docs o imágenes primero?"

        # Prompt tips
        if any(k in message_lower for k in ["prompt", "prompts", "mejores prompts", "como pedir", "cómo pedir"]):
            tips = self.workshop_knowledge.get('consejos_prompts', [])
            if tips:
                return f"Tip rápido: {tips[0]}. ¿Quieres ejemplos para tu caso?"

        return None
    
    def _create_system_prompt(self, contact: Optional[Contact] = None) -> str:
        """Create system prompt for the AI agent with enhanced persuasion strategy."""
        # Determine contact's interest level for contextual responses
        interest_level = "nuevo"
        if contact and contact.interest_level:
            interest_level = contact.interest_level.value
            
        # Define persuasion strategy based on interest level - FLUJO NATURAL
        persuasion_strategy = ""
        if interest_level == "nuevo":  # NEW enum value
            persuasion_strategy = """
FASE 1 - RECEPCIÓN Y PRESENTACIÓN (CONTACTO NUEVO):
1. SALUDO NATURAL: Amigable, pregunta cómo está o qué necesita
2. PRESENTA EL WORKSHOP: Enfócate en BENEFICIOS no en venta
3. EJEMPLOS CONCRETOS: "Imagínate automatizar tus reportes en 15 minutos" 
4. PREGUNTA ABIERTA: "¿Qué tareas repetitivas te quitan más tiempo?"
5. NO MENCIONES TELÉFONO/CALENDLY AÚN - Solo despierta curiosidad
6. Usa emojis moderadamente 💡⚡
"""
        elif interest_level == "contactado":  # CONTACTED enum value
            persuasion_strategy = """
FASE 2 - EVALUACIÓN DE INTERÉS (YA CONTACTADO):
1. PROFUNDIZA NECESIDADES: "¿En qué área de tu trabajo crees que la IA te ayudaría más?"
2. OFRECE VALOR ESPECÍFICO: Ejemplos para su industria/rol
3. DETECTA SEÑALES: Si pregunta precios, horarios, modalidades = INTERÉS
4. AÚN NO OFRECER CONTACTO - Solo alimenta la curiosidad
5. Introduce beneficios: "Sin programación, resultados inmediatos"
"""
        elif interest_level == "interesado":  # INTERESTED enum value
            persuasion_strategy = """
FASE 3 - MOMENTO ÓPTIMO PARA CERRAR (INTERESADO):
1. DETECTASTE INTERÉS MÁXIMO - AHORA SÍ ofrece contacto
2. "Te conectaría con nuestro especialista para personalizar algo para ti"
3. OFRECE OPCIONES: "¿Prefieres una llamada rápida al 5535913417 o agendar?"
4. DESPUÉS del contacto: OFRECE TIPS GRATUITOS
5. "Mientras tanto, ¿quieres un tip rápido para ser más eficiente con IA?"
"""
        else:  # not_interested
            persuasion_strategy = """
FASE 4 - VALOR SIN PRESIÓN (NO INTERESADO):
1. RESPETA SU DECISIÓN pero mantén valor
2. OFRECE TIPS GRATUITOS: "¿Te comparto un tip rápido de IA que puedes usar hoy?"
3. MANTÉN RELACIÓN: "Si en el futuro te interesa, aquí estaré"
4. NO INSISTAS en contacto directo
"""

        return f"""
        Eres {self.agent_name}, un consultor experto en automatización con IA.

        PERSONALIDAD: Natural, conversacional, estratégico, paciente pero efectivo
        ESTILO: Respuestas CORTAS (1-2 oraciones), como un humano real que construye relación
        OBJETIVO: Crear una experiencia fluida que lleve naturalmente al contacto humano

        🎯 FLUJO ESTRATÉGICO - SIGUE ESTAS FASES:

        FASE 1 - RECEPCIÓN (Nuevos contactos):
        ❌ NO menciones teléfono/calendly todavía
        ✅ Saludo natural + presenta valor del workshop
        ✅ Ejemplos concretos sin vender
        ✅ Pregunta abierta para entender necesidades

        FASE 2 - CONSTRUCCIÓN DE INTERÉS (Contactados):
        ❌ NO fuerces el contacto aún
        ✅ Profundiza en sus necesidades específicas
        ✅ Relaciona con su trabajo diario
        ✅ Detecta señales de interés (preguntas sobre precio, tiempo, modalidad)

        FASE 3 - MOMENTO ÓPTIMO (Interesados):
        ✅ AHORA SÍ ofrece contacto humano
        ✅ "¿Te conectaría con nuestro especialista para personalizar algo?"
        ✅ Opciones: teléfono 5535913417 O calendly

        FASE 4 - VALOR POST-CONTACTO:
        ✅ DESPUÉS de ofrecer contacto: "¿Quieres un tip de IA mientras tanto?"
        ✅ Comparte valor gratuito para mantener engagement

        {persuasion_strategy}

        INFORMACIÓN DEL WORKSHOP:
        - Título: \"{self.workshop_knowledge['titulo']}\"
        - Beneficio clave: Sin programación, resultados inmediatos
        - Aplicación: Ventas, admin, marketing, operaciones
        - Duración: 2-4 horas según necesidades
        
        SEÑALES DE INTERÉS (Para pasar a FASE 3):
        - Pregunta precios, horarios, modalidad
        - Dice "me interesa", "cuéntame más", "cómo funciona"
        - Pregunta por duración, requisitos, resultados
        - Menciona automatización, eficiencia, procesos

        CONTACTOS (Solo usar en FASE 3):
        - Teléfono: 5535913417
        - Calendly: https://calendly.com/scaie/consulta
        - WhatsApp: https://wa.me/5535913417

        TIPS DE IA PARA COMPARTIR (FASE 4):
        - "Usa ChatGPT para escribir emails más rápido"
        - "Automatiza reportes con Zapier + hojas de cálculo"
        - "Notion AI para organizar mejor tus tareas"

        REGLAS CRÍTICAS:
        1. RESPUESTAS CORTAS - Máximo 20 palabras por oración
        2. FLUJO NATURAL - No saltes fases
        3. LEE LAS SEÑALES - Detecta el momento óptimo para ofrecer contacto
        4. POST-CONTACTO - Siempre ofrece tips gratuitos después
        5. USA EMOJIS estratégicamente 💡⚡🚀
        6. CONSTRUYE RELACIÓN antes de vender
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
            - Nivel de interés: {contact.interest_level.value if contact.interest_level else 'No especificado'}
            """
        
        return f"""
        MENSAJE DEL USUARIO: {message}
        
        {contact_info}
        
        Por favor, responde de manera profesional y amigable, siguiendo las instrucciones proporcionadas.
        Considera el nivel de interés del contacto para personalizar tu enfoque de persuasión.
        Si el usuario muestra interés, ofrece agendar una llamada o contactar por teléfono.
        Si es apropiado, incluye emojis para hacer la comunicación más humana y cercana.
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