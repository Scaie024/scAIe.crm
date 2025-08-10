"""
Endpoint de WhatsApp (Cloud API) para integrar webhooks vía ngrok o producción.
"""

from fastapi import APIRouter, Request, HTTPException, Query
from typing import Dict, Any
import logging
import os

from ...services.whatsapp_service import whatsapp_service
from ...services.omnipotent_agent import omnipotent_agent

logger = logging.getLogger(__name__)

whatsapp_router = APIRouter(prefix="/webhook/whatsapp", tags=["whatsapp"])


@whatsapp_router.get("")
async def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
):
    """
    Verificación del webhook de WhatsApp (GET) requerida por Meta.
    """
    try:
        result = await whatsapp_service.verify_webhook(hub_challenge, hub_mode, hub_verify_token)
        if result.get("success"):
            # Responder con el challenge en texto/plain
            return int(result["challenge"]) if result.get("challenge") else ""
        raise HTTPException(status_code=403, detail=result.get("error", "Verification failed"))
    except Exception as e:
        logger.error(f"WhatsApp webhook verification error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@whatsapp_router.post("")
async def receive_message(payload: Dict[str, Any]):
    """
    Recepción de mensajes entrantes de WhatsApp (POST).
    """
    try:
        # Estructura estándar de WhatsApp Cloud API
        # payload['entry'][0]['changes'][0]['value']['messages'][0]
        entry = (payload or {}).get("entry", [])
        if not entry:
            return {"status": "ignored"}

        changes = entry[0].get("changes", []) if entry else []
        if not changes:
            return {"status": "ignored"}

        value = changes[0].get("value", {})
        messages = value.get("messages", [])
        contacts = value.get("contacts", [])
        if not messages:
            return {"status": "ignored"}

        msg = messages[0]
        from_id = msg.get("from")  # WhatsApp user ID (phone)
        text = (msg.get("text") or {}).get("body") or ""
        contact_name = contacts[0].get("profile", {}).get("name") if contacts else None

        # Procesar con agente
        response = await omnipotent_agent.process_incoming_message(
            message=text,
            platform="whatsapp",
            contact_info={
                "name": contact_name or "Usuario WhatsApp",
                "phone": from_id,
                "platform_user_id": from_id,
            },
        )

        # Enviar respuesta
        await whatsapp_service.send_message(response.get("response", ""), from_id)

        return {"status": "ok"}
    except Exception as e:
        logger.error(f"WhatsApp webhook processing error: {e}")
        # WhatsApp requiere 200 OK; devolver error en cuerpo si es necesario
        return {"status": "error", "detail": str(e)}
