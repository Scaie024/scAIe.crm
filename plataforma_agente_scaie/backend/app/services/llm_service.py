import os
import httpx
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv
import json
import random
from datetime import datetime
from .scaie_knowledge import scaie_knowledge

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
        self.api_key = os.getenv('DASHSCOPE_API_KEY', 'sk-1ded1e3aa4d04a7593afc74a484cd4c1')
        
        # Configuración del cliente HTTP
        self.client = httpx.AsyncClient(
            base_url="https://dashscope.aliyuncs.com/api/v1",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            timeout=30.0
        )
        
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
        try:
            # Obtener conocimiento relevante de SCAIE
            knowledge = scaie_knowledge.get_knowledge(user_message)
            
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
            """
            
            # Agregar mensaje del usuario con contexto al historial
            messages = self.conversation_history.copy()
            messages.append({
                'role': 'user',
                'content': message_with_context
            })
            
            # Generar respuesta con Qwen
            try:
                response = await self.client.post(
                    "/services/aigc/text-generation/generation",
                    json={
                        "model": self.model_name,
                        "input": {
                            "messages": messages
                        },
                        "parameters": {
                            "temperature": self.generation_config['temperature'],
                            "max_tokens": self.generation_config['max_tokens'],
                            "top_p": self.generation_config['top_p'],
                            "top_k": self.generation_config['top_k'],
                            "seed": 1234
                        }
                    }
                )
                
                response.raise_for_status()
                result = response.json()
                
                # Obtener y formatear la respuesta
                if result.get("output") and result["output"].get("text"):
                    response_text = result["output"]["text"]
                else:
                    response_text = "Lo siento, estoy teniendo dificultades técnicas en este momento. ¿Podrías reformular tu pregunta?"
                
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
                        'tokens_used': len(response_text.split()),  # Estimación
                        'context_used': knowledge.get('relevant_sections', [])
                    }
                }
            except httpx.TimeoutException:
                return {
                    'success': False,
                    'error': 'Timeout al generar la respuesta',
                    'response': 'Lo siento, estoy teniendo problemas para procesar tu solicitud en este momento. ¿Podrías intentar reformular tu pregunta?'
                }
            except httpx.HTTPStatusError as e:
                print(f"Error HTTP al llamar a Qwen: {e}")
                return {
                    'success': False,
                    'error': f'Error HTTP: {e}',
                    'response': 'Lo siento, ha ocurrido un error al procesar tu solicitud. ¿Podrías intentar reformular tu pregunta?'
                }
            
        except Exception as e:
            print(f"Error al generar respuesta: {e}")
            return {
                'success': False,
                'error': str(e),
                'response': 'Lo siento, ha ocurrido un error al procesar tu solicitud. ¿Podrías intentar reformular tu pregunta?'
            }
    
    def reset_conversation(self):
        """Reinicia la conversación."""
        self._initialize_system_prompt()
        return {'success': True, 'message': 'Conversación reiniciada'}

# Instancia global del servicio
llm_service = LLMService()