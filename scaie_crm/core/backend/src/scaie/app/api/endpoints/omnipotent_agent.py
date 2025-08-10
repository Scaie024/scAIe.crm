from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import logging

from ...core.database import get_db
from ...services.omnipotent_agent import omnipotent_agent
from ...models.contact import Contact
from ...models.conversation import Conversation
from ...models.agent_action import AgentTask, AgentAction
from ...schemas.message import MessageRequest  # Added missing import

# Create logger
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/omnipotent-agent", tags=["omnipotent-agent"])

class IncomingMessage(BaseModel):
    message: str
    platform: str = "web"
    contact_info: Dict[str, Any]

class ContactInfo(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    company: Optional[str] = None

class AgentResponse(BaseModel):
    response: str
    contact_id: int
    message_id: int
    actions: List[Dict[str, Any]] = []
    executed_actions: List[Dict[str, Any]] = []

class TaskCreate(BaseModel):
    contact_id: int
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    due_date: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[str] = None

class TaskResponse(BaseModel):
    id: int
    contact_id: int
    title: str
    description: Optional[str] = None
    status: str
    priority: str
    due_date: Optional[str] = None
    created_at: str
    completed_at: Optional[str] = None

class ContactSummaryResponse(BaseModel):
    contact: Dict[str, Any]
    conversations_count: int
    tasks: List[Dict[str, Any]]
    recent_actions: List[Dict[str, Any]]

@router.get("/test")
def test_endpoint():
    return {"message": "Test endpoint is working"}

@router.post("/process-message")
async def process_message_endpoint(
    request: MessageRequest,
    db: Session = Depends(get_db)
):
    """
    Endpoint para procesar mensajes desde cualquier canal (web, Telegram, WhatsApp, etc.)
    
    Args:
        request: Objeto de solicitud con información del mensaje y contacto
        db: Sesión de base de datos
    Returns:
        Dict with response and metadata
    """
    try:
        # Procesar mensaje usando el servicio del agente
        result = await omnipotent_agent.process_incoming_message(
            message=request.message,
            platform=request.contact.platform if request.contact else "web",
            contact_info=request.contact.dict() if request.contact else {},
            db=db
        )
        
        return result
        
    except HTTPException as e:
        # Re-raise HTTPException to maintain original status code and detail
        raise e
    except Exception as e:
        # Log detailed error information
        logger.error(f"Error processing message: {str(e)}", exc_info=True)
        # Provide more specific error message
        raise HTTPException(
            status_code=500,
            detail="Error al procesar el mensaje. Por favor, inténtalo de nuevo más tarde."
        )

@router.post("/execute-pending-actions/{conversation_id}")
async def execute_pending_actions(
    conversation_id: int,
    db: Session = Depends(get_db)
):
    """
    Ejecuta todas las acciones pendientes para una conversación.
    """
    try:
        results = omnipotent_agent.execute_pending_actions(conversation_id, db=db)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/contact/{contact_id}/summary", response_model=ContactSummaryResponse)
async def get_contact_summary(
    contact_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene un resumen completo de un contacto.
    """
    try:
        summary = omnipotent_agent.get_contact_summary(contact_id, db=db)
        if "error" in summary:
            raise HTTPException(status_code=404, detail=summary["error"])
        return ContactSummaryResponse(**summary)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search-contacts")
async def search_contacts(
    query: str,
    db: Session = Depends(get_db)
):
    """
    Busca contactos por nombre, teléfono, email o empresa.
    """
    try:
        results = omnipotent_agent.search_contacts(query, db=db)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tasks", response_model=TaskResponse)
async def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
):
    """
    Crea una nueva tarea para un contacto.
    """
    try:
        # Verificar que el contacto exista
        contact = db.query(Contact).filter(Contact.id == task.contact_id).first()
        if not contact:
            raise HTTPException(status_code=404, detail="Contacto no encontrado")
        
        # Crear la tarea
        db_task = AgentTask(
            contact_id=task.contact_id,
            title=task.title,
            description=task.description,
            priority=task.priority,
            due_date=task.due_date
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        
        return TaskResponse(**db_task.to_dict())
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualiza una tarea existente.
    """
    try:
        # Obtener la tarea
        db_task = db.query(AgentTask).filter(AgentTask.id == task_id).first()
        if not db_task:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        
        # Actualizar los campos proporcionados
        if task_update.title is not None:
            db_task.title = task_update.title
        if task_update.description is not None:
            db_task.description = task_update.description
        if task_update.status is not None:
            db_task.status = task_update.status
        if task_update.priority is not None:
            db_task.priority = task_update.priority
        if task_update.due_date is not None:
            db_task.due_date = task_update.due_date
            
        db.commit()
        db.refresh(db_task)
        
        return TaskResponse(**db_task.to_dict())
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/tasks/{task_id}")
async def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    """
    Elimina una tarea.
    """
    try:
        # Obtener la tarea
        db_task = db.query(AgentTask).filter(AgentTask.id == task_id).first()
        if not db_task:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        
        db.delete(db_task)
        db.commit()
        
        return {"message": "Tarea eliminada exitosamente"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tasks", response_model=List[TaskResponse])
async def list_tasks(
    contact_id: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Lista todas las tareas, opcionalmente filtradas por contacto o estado.
    """
    try:
        query = db.query(AgentTask)
        
        if contact_id is not None:
            query = query.filter(AgentTask.contact_id == contact_id)
            
        if status is not None:
            query = query.filter(AgentTask.status == status)
            
        tasks = query.all()
        
        return [TaskResponse(**task.to_dict()) for task in tasks]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))