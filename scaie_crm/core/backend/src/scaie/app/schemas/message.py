from pydantic import BaseModel, Field
from typing import Optional

class ContactInfo(BaseModel):
    """
    Información básica de contacto para identificar al remitente del mensaje
    """
    name: str = Field(..., description="Nombre completo del contacto")
    phone: Optional[str] = Field(None, description="Número de teléfono del contacto")
    email: Optional[str] = Field(None, description="Correo electrónico del contacto")
    company: Optional[str] = Field(None, description="Empresa donde trabaja el contacto")
    notes: Optional[str] = Field(None, description="Notas adicionales sobre el contacto")
    interest_level: str = Field("nuevo", description="Nivel de interés del contacto")
    platform: str = Field("web", description="Plataforma de origen del mensaje")
    telegram_user_id: Optional[str] = Field(None, description="ID único de Telegram")
    whatsapp_user_id: Optional[str] = Field(None, description="ID único de WhatsApp")
    facebook_messenger_user_id: Optional[str] = Field(None, description="ID único de Facebook Messenger")
    instagram_user_id: Optional[str] = Field(None, description="ID único de Instagram")
    platform_user_id: Optional[str] = Field(None, description="ID único genérico de la plataforma")


class MessageRequest(BaseModel):
    """
    Modelo para validar las solicitudes de procesamiento de mensajes
    """
    message: str = Field(..., description="Contenido del mensaje a procesar")
    conversation_id: Optional[int] = Field(None, description="ID de conversación existente")
    contact: Optional[ContactInfo] = Field(None, description="Información del contacto")