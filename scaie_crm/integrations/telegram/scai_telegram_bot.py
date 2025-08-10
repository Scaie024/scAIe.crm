#!/usr/bin/env python3
"""
Bot de Telegram SCAI simplificado y funcional
Bot: @scAIebot (t.me/scAIebot)
"""

import os
import sys
import logging
import asyncio
import httpx
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Cargar variables de entorno desde la raíz del proyecto
load_dotenv('../../.env')

# Token del bot y URL del backend
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
BACKEND_URL = os.getenv('BACKEND_URL', 'http://127.0.0.1:8000')

if not TELEGRAM_BOT_TOKEN:
    print("❌ Error: TELEGRAM_BOT_TOKEN no encontrado en .env")
    sys.exit(1)

# Añadir el path del backend para importar servicios
sys.path.append('../../core/backend/src/scaie')

# Respuestas predefinidas para el agente
WORKSHOP_INFO = """
🎯 **Workshop: "Sé más eficiente con IA"**

💡 Capacita a tu equipo para usar IA sin código y mejora la productividad en todos los departamentos.

📅 **Modalidades:**
• Online en vivo (recomendado)
• Presencial 
• Híbrido

💰 **Precios:**
• Básico: $1,499 MXN (2 horas, hasta 10 personas)
• Profesional: $2,999 MXN (4 horas, hasta 20 personas)
• Empresarial: $5,000 MXN (contenido específico)

🎁 **Incluye:**
• Manual del workshop
• Grabación de la sesión
• Sesión de seguimiento (30 minutos)
• Acceso a herramientas freemium

📞 **Contacto:** 55 3591 3417
🌐 **Web:** www.scaie.com.mx
📅 **Agendar:** https://calendly.com/scaie-empresa/30min
"""

class ScaiBot:
    def __init__(self):
        # TELEGRAM_BOT_TOKEN ya fue validado arriba
        self.token = TELEGRAM_BOT_TOKEN
        self.application = Application.builder().token(str(self.token)).build()

        # Registrar handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("workshop", self.workshop_command))
        self.application.add_handler(CommandHandler("contacto", self.contact_command))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start"""
        user = update.effective_user
        if not user or not update.message:
            return
        welcome_message = f"""
👋 ¡Hola {user.first_name}! Soy SCAI, tu asistente de IA especializado en automatización empresarial.

🎯 ¿Quieres que tu equipo trabaje un 50-300% más eficiente? 

Descubre cómo puedes:
✅ Automatizar tareas repetitivas en minutos
✅ Tomar decisiones basadas en datos
✅ Generar contenido profesional al instante
✅ Romper la brecha de conocimiento en tu equipo

💡 Solo dime... ¿En qué área te gustaría mejorar primero?

Puedes consultarme sobre:
• Automatización de procesos
• Análisis de datos
• Generación de contenido
• Y mucho más...

📌 Usa /workshop para ver nuestro programa completo
📌 Usa /contacto para hablar con un experto
        """
        if update.message:
            await update.message.reply_text(welcome_message)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /help"""
        help_message = """
🆘 **GUÍA DE USO - SCAI**

🧠 Estoy diseñado para ayudarte con todo relacionado con inteligencia artificial y automatización empresarial. Puedes:

📌 Comandos principales:
/start - Reiniciar conversación
/workshop - Conocer nuestro programa de capacitación
/contacto - Datos de contacto
/help - Mostrar esta guía

💡 Pregúntame sobre:
• Cómo implementar IA en tu negocio
• Soluciones específicas para tu industria
• Casos prácticos de éxito
• Automatización de tareas repetitivas
• Análisis y visualización de datos

✨ Consejo: Cuanto más específico seas sobre tus necesidades, mejor podré ayudarte.

📞 ¿Prefieres hablar con un humano? 
Usa /contacto para conectarte con nuestro equipo de expertos.

        """
        if update.message:
            await update.message.reply_text(help_message)
    
    async def workshop_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /workshop"""
        if update.message:
            await update.message.reply_text(WORKSHOP_INFO)
    
    async def contact_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /contacto"""
        contact_message = """
📞 **CONTACTO - SCAI**

📱 **Teléfono:** 55 3591 3417
🌐 **Website:** www.scaie.com.mx
📅 **Agenda una llamada gratuita:** https://calendly.com/scaie-empresa/30min

💬 **¿Prefieres otra opción?**
📧 Email: info@scaie.com.mx
📱 WhatsApp: [Enviar mensaje](https://wa.me/525535913417)

🕒 **Horarios de atención:**
Lunes a Viernes: 9:00 AM - 6:00 PM (GMT-6)

🎯 **Oferta especial:** Esta semana tenemos cupo limitado para sesiones personalizadas. ¿Te gustaría agendar una llamada gratuita de 15 minutos para ver cómo podemos ayudar a tu empresa?
        """
        if update.message:
            await update.message.reply_text(contact_message)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Manejar mensajes de texto"""
        user = update.effective_user
        if not user or not update.message or not update.effective_chat:
            return
        
        message_text = update.message.text or ""

        logger.info(
            f"Mensaje de @{getattr(user, 'username', None) or getattr(user, 'first_name', 'usuario')}: {message_text}"
        )

        # Enviar al backend para una respuesta coherente via LLM
        try:
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

            # Obtener respuesta del backend
            response_text = await self.ask_backend(message_text, user)
            
            # Enviar respuesta al usuario
            await update.message.reply_text(response_text)
            
        except Exception as e:
            logger.error(f"Error procesando mensaje: {str(e)}")
            error_message = """
⚠️ Lo siento, estoy experimentando algunas dificultades técnicas en este momento.

🔧 Mientras resolvemos el problema, puedes contactarnos directamente:

📱 WhatsApp: [55 3591 3417](https://wa.me/525535913417)
🌐 Agenda una llamada: https://calendly.com/scaie-empresa/30min
📧 Email: info@scaie.com.mx

⏳ Vuelve en unos minutos para probar el servicio nuevamente. ¡Agradecemos tu paciencia!
            """
            await update.message.reply_text(error_message)

    async def ask_backend(self, message_text: str, user) -> str:
        """Envía el mensaje al backend (omnipotent-agent) y devuelve la respuesta del LLM."""
        # Usar el endpoint versionado y el esquema esperado por el backend (MessageRequest)
        url = f"{BACKEND_URL.rstrip('/')}/api/v1/omnipotent-agent/process-message"
        payload = {
            "message": message_text,
            "contact": {
                "name": getattr(user, 'first_name', None) or getattr(user, 'username', 'Usuario'),
                "phone": None,  # Opcional, podríamos pedirlo si es necesario
                "email": None,   # Opcional, podríamos pedirlo si es necesario
                "platform": "telegram",
                "platform_user_id": str(getattr(user, 'id', ''))
            }
        }
        timeout = httpx.Timeout(15.0, connect=5.0)
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.post(url, json=payload)
            resp.raise_for_status()
            data = resp.json()
            return data.get("response", "") or "Disculpa, no pude generar respuesta en este momento."

def main():
    """Función principal"""
    print("🤖 SCAI - Bot de Telegram")
    print("=" * 40)
    print("Bot: @scAIebot")
    print("URL: https://t.me/scAIebot")
    print("=" * 40)
    
    bot = ScaiBot()
    # run_polling es bloqueante y maneja init/start/stop internamente en PTB v20+
    bot.application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()