import os
import logging
from typing import Dict, Any, Optional
import asyncio
import json
from telegram import Update, Message as TelegramMessage
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.error import TelegramError, Conflict

from .omnipotent_agent import omnipotent_agent
from ..core.database import get_db
from ..models.contact import Contact
from ..models.conversation import Conversation, Message

# Configurar logger
logger = logging.getLogger(__name__)

class TelegramService:
    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.app: Optional[Application] = None
        self.is_running = False
        
    async def initialize(self):
        """Initialize the Telegram bot application"""
        if not self.token:
            logger.error("TELEGRAM_BOT_TOKEN not found in environment variables")
            return False
            
        try:
            # Create the Application instance
            self.app = Application.builder().token(self.token).build()
            
            # Add handlers
            self.app.add_handler(CommandHandler("start", self.start_command))
            self.app.add_handler(CommandHandler("help", self.help_command))
            self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
            
            logger.info("Telegram bot initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Error initializing Telegram bot: {e}")
            return False
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        try:
            welcome_message = (
                "¡Bienvenido al agente de ventas de SCAIE!\n\n"
                "Soy SCAI, tu asistente especializado en transformación digital con inteligencia artificial. "
                "Puedo ayudarte a conocer cómo aplicar IA en tu empresa para automatizar procesos y aumentar la productividad.\n\n"
                "¿En qué industria trabajas y qué procesos te gustaría optimizar?"
            )
            await update.message.reply_text(welcome_message)
        except Exception as e:
            logger.error(f"Error in start_command: {e}")
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        try:
            help_text = (
                "Soy SCAI, el agente de ventas de SCAIE.\n\n"
                "Puedo ayudarte con:\n"
                "• Información sobre nuestros servicios de IA\n"
                "• Detalles del workshop 'Sé más eficiente con IA'\n"
                "• Precios y planes de nuestros servicios\n"
                "• Agendamiento de consultas\n\n"
                "Solo tienes que escribirme cualquier pregunta y haré lo posible por ayudarte."
            )
            await update.message.reply_text(help_text)
        except Exception as e:
            logger.error(f"Error in help_command: {e}")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming messages"""
        try:
            # Get message details
            user_id = update.effective_user.id
            username = update.effective_user.username or update.effective_user.full_name
            first_name = update.effective_user.first_name or ""
            last_name = update.effective_user.last_name or ""
            full_name = f"{first_name} {last_name}".strip() or username or "Usuario Telegram"
            text = update.message.text
            
            logger.info(f"Received message from {full_name} (@{username}): {text}")
            
            # Process with omnipotent agent
            contact_info = {
                "name": full_name,
                "phone": None,
                "email": None,
                "platform_user_id": str(user_id),
                "username": username
            }
            
            # Process the message with the omnipotent agent
            try:
                response_data = omnipotent_agent.process_incoming_message(
                    message=text,
                    platform="telegram",
                    contact_info=contact_info
                )
                
                # Send response back to user
                await update.message.reply_text(response_data["response"])
                
                # Execute any immediate actions
                for action in response_data.get("executed_actions", []):
                    await self.handle_action_result(action, update)
            except Exception as agent_error:
                logger.error(f"Error processing message with omnipotent agent: {agent_error}")
                await update.message.reply_text(
                    "Lo siento, estoy teniendo dificultades para procesar tu solicitud en este momento. "
                    "Por favor, inténtalo de nuevo más tarde."
                )
                
        except Exception as e:
            logger.error(f"Error handling Telegram message: {e}")
            try:
                await update.message.reply_text(
                    "Lo siento, ha ocurrido un error al procesar tu mensaje. "
                    "Por favor, inténtalo de nuevo más tarde."
                )
            except Exception as reply_error:
                logger.error(f"Error sending error message to user: {reply_error}")
    
    async def handle_action_result(self, action: Dict[str, Any], update: Update):
        """Handle action results that need to send additional messages"""
        try:
            action_type = action.get("action_type")
            result = action.get("result", {})
            
            if action_type == "escalate_to_human":
                await update.message.reply_text(
                    "Un agente humano se pondrá en contacto contigo pronto. "
                    "Gracias por tu paciencia."
                )
            elif action_type == "send_material":
                # In a real implementation, this would send actual materials
                material_type = action.get("parameters", {}).get("material_type")
                if material_type == "workshop_brochure":
                    await update.message.reply_text(
                        "Te enviaría el folleto del workshop, pero esta función "
                        "se implementará en una actualización futura."
                    )
        except Exception as e:
            logger.error(f"Error handling action result: {e}")
    
    async def send_message(self, user_id: str, message: str) -> bool:
        """Send a message to a specific user"""
        try:
            if not self.app:
                logger.error("Telegram bot not initialized")
                return False
                
            await self.app.bot.send_message(chat_id=int(user_id), text=message)
            return True
        except TelegramError as e:
            logger.error(f"Telegram error sending message: {e}")
            return False
        except Exception as e:
            logger.error(f"Error sending Telegram message: {e}")
            return False
    
    async def start(self):
        """Start the Telegram bot"""
        if not self.app:
            logger.error("Telegram bot not initialized")
            return False
            
        try:
            # Start the bot
            await self.app.initialize()
            await self.app.start()
            
            # Limpiar cualquier webhook existente antes de iniciar el polling
            try:
                await self.app.bot.delete_webhook(drop_pending_updates=True)
                logger.info("Webhook eliminado correctamente")
            except Exception as e:
                logger.warning(f"No se pudo eliminar el webhook: {e}")
            
            await self.app.updater.start_polling(
                drop_pending_updates=True,  # Ignorar actualizaciones pendientes
                allowed_updates=Update.ALL_TYPES,
                timeout=30,
                read_timeout=30,
                write_timeout=30,
                pool_timeout=30,
                connect_timeout=30
            )
            
            self.is_running = True
            logger.info("Telegram bot started successfully")
            return True
        except Conflict as e:
            logger.error(f"Conflict error starting Telegram bot: {e}")
            logger.error("Esto puede deberse a que otra instancia del bot está en ejecución.")
            logger.error("Asegúrate de detener todas las demás instancias del bot.")
            return False
        except Exception as e:
            logger.error(f"Error starting Telegram bot: {e}")
            return False
    
    async def stop(self):
        """Stop the Telegram bot"""
        if not self.app or not self.is_running:
            return
            
        try:
            await self.app.updater.stop()
            await self.app.stop()
            await self.app.shutdown()
            self.is_running = False
            logger.info("Telegram bot stopped successfully")
        except Exception as e:
            logger.error(f"Error stopping Telegram bot: {e}")

# Global instance
telegram_service = TelegramService()