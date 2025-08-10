from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from pydantic import BaseModel
import logging

from ...core.database import get_db
from ...services.omnipotent_agent import omnipotent_agent
from ...services.llm_service import llm_service

# Create logger
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/sandbox", tags=["sandbox"])

class SandboxMessage(BaseModel):
    message: str
    reset_context: bool = False
    agent_config: Optional[Dict[str, Any]] = None

class SandboxResponse(BaseModel):
    response: str
    context_info: Optional[Dict[str, Any]] = None
    agent_config: Optional[Dict[str, Any]] = None

@router.post("/test-message", response_model=SandboxResponse)
async def test_message(
    request: SandboxMessage,
    db: Session = Depends(get_db)
):
    """
    Endpoint para probar mensajes en el sandbox sin guardar en la base de datos principal.
    """
    try:
        # Configuración temporal del agente para testing
        test_contact_info = {
            "name": "Usuario de Prueba",
            "platform": "sandbox",
            "platform_user_id": "sandbox_test_user"
        }
        
        if request.reset_context:
            # Reiniciar contexto para una conversación nueva
            logger.info("Reiniciando contexto del sandbox")
        
        # Procesar mensaje usando el agente omnipotente
        result = await omnipotent_agent.process_incoming_message(
            message=request.message,
            platform="sandbox",
            contact_info=test_contact_info,
            db=db
        )
        
        # Información adicional del contexto para debugging
        context_info = {
            "model": "qwen-plus",
            "tokens_used": "N/A",  # Se podría calcular
            "context_used": ["Conocimiento base SCAIE", "Historial de conversación"],
            "processing_time": "< 1s"
        }
        
        return SandboxResponse(
            response=result.get("response", "Error generando respuesta"),
            context_info=context_info,
            agent_config=request.agent_config
        )
        
    except Exception as e:
        logger.error(f"Error en sandbox: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error procesando mensaje en sandbox"
        )

@router.get("/agent-config")
async def get_agent_config():
    """
    Obtiene la configuración actual del agente.
    """
    try:
        config = {
            "name": "SCAI",
            "personality": "vendedor experto persuasivo directo orientado a resultados",
            "tone": "profesional y directo",
            "goal": "convertir todas las conversaciones en llamadas al 5535913417",
            "model": "qwen-plus",
            "temperature": 0.8,
            "max_tokens": 1024
        }
        return config
    except Exception as e:
        logger.error(f"Error obteniendo configuración: {str(e)}")
        raise HTTPException(status_code=500, detail="Error obteniendo configuración")

@router.post("/agent-config")
async def update_agent_config(config: Dict[str, Any]):
    """
    Actualiza la configuración del agente (temporal para el sandbox).
    """
    try:
        # En una implementación completa, esto se guardaría en base de datos
        # Por ahora es temporal para testing
        logger.info(f"Configuración temporal actualizada: {config}")
        return {"message": "Configuración actualizada correctamente", "config": config}
    except Exception as e:
        logger.error(f"Error actualizando configuración: {str(e)}")
        raise HTTPException(status_code=500, detail="Error actualizando configuración")

@router.get("/test-scenarios")
async def get_test_scenarios():
    """
    Obtiene escenarios de prueba predefinidos para el sandbox.
    """
    scenarios = [
        {
            "id": 1,
            "name": "Cliente Interesado en Workshop",
            "message": "Hola, me interesa el workshop de IA para mi empresa. ¿Podrían darme más información?",
            "expected_outcome": "Información detallada del workshop y solicitud de contacto"
        },
        {
            "id": 2,
            "name": "Cliente Preguntando Precios",
            "message": "¿Cuánto cuesta el workshop básico? ¿Tienen descuentos para empresas pequeñas?",
            "expected_outcome": "Información de precios y propuesta de llamada"
        },
        {
            "id": 3,
            "name": "Cliente Escéptico",
            "message": "No estoy seguro si la IA realmente puede ayudar a mi negocio. ¿Tienen casos de éxito?",
            "expected_outcome": "Casos de éxito y propuesta de demo gratuita"
        },
        {
            "id": 4,
            "name": "Cliente con Urgencia",
            "message": "Necesito automatizar procesos urgentemente. ¿Pueden ayudarme esta semana?",
            "expected_outcome": "Respuesta inmediata y agendamiento de cita urgente"
        },
        {
            "id": 5,
            "name": "Cliente Comparando Opciones",
            "message": "Estoy evaluando diferentes proveedores de IA. ¿Qué los hace diferentes?",
            "expected_outcome": "Diferenciadores clave y propuesta de comparación"
        }
    ]
    return scenarios

@router.post("/bulk-test")
async def bulk_test_scenarios(
    scenario_ids: list[int],
    db: Session = Depends(get_db)
):
    """
    Ejecuta múltiples escenarios de prueba y devuelve los resultados.
    """
    try:
        scenarios = await get_test_scenarios()
        results = []
        
        for scenario_id in scenario_ids:
            scenario = next((s for s in scenarios if s["id"] == scenario_id), None)
            if not scenario:
                continue
                
            # Procesar mensaje del escenario
            request = SandboxMessage(
                message=scenario["message"],
                reset_context=True
            )
            
            response = await test_message(request, db)
            
            results.append({
                "scenario": scenario,
                "response": response.response,
                "context_info": response.context_info
            })
        
        return {"results": results}
        
    except Exception as e:
        logger.error(f"Error en prueba masiva: {str(e)}")
        raise HTTPException(status_code=500, detail="Error ejecutando pruebas masivas")
