from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import logging
import io
import json

from ...core.database import get_db
from ...services.rag_service import rag_service

# Create logger
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/knowledge", tags=["knowledge"])

class KnowledgeCreate(BaseModel):
    title: str
    content: str
    category: str = "general"
    metadata: Optional[Dict[str, Any]] = None

class KnowledgeUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class KnowledgeSearch(BaseModel):
    query: str
    top_k: int = 5
    category: Optional[str] = None

@router.post("/add")
async def add_knowledge(knowledge: KnowledgeCreate):
    """
    Agregar nueva entrada de conocimiento a la base de datos RAG.
    """
    try:
        knowledge_id = rag_service.add_knowledge(
            title=knowledge.title,
            content=knowledge.content,
            category=knowledge.category,
            metadata=knowledge.metadata or {}
        )
        
        return {
            "message": "Conocimiento agregado exitosamente",
            "knowledge_id": knowledge_id
        }
        
    except Exception as e:
        logger.error(f"Error agregando conocimiento: {str(e)}")
        raise HTTPException(status_code=500, detail="Error agregando conocimiento")

@router.get("/list")
async def list_knowledge(category: Optional[str] = None):
    """
    Listar todas las entradas de conocimiento.
    """
    try:
        knowledge_list = rag_service.list_knowledge(category=category)
        return {"knowledge": knowledge_list}
        
    except Exception as e:
        logger.error(f"Error listando conocimiento: {str(e)}")
        raise HTTPException(status_code=500, detail="Error listando conocimiento")

@router.get("/categories")
async def get_categories():
    """
    Obtener todas las categorías disponibles.
    """
    try:
        categories = rag_service.get_categories()
        return {"categories": categories}
        
    except Exception as e:
        logger.error(f"Error obteniendo categorías: {str(e)}")
        raise HTTPException(status_code=500, detail="Error obteniendo categorías")

@router.post("/search")
async def search_knowledge(search_request: KnowledgeSearch):
    """
    Buscar conocimiento relevante usando búsqueda semántica.
    """
    try:
        results = rag_service.search_knowledge(
            query=search_request.query,
            top_k=search_request.top_k,
            category=search_request.category
        )
        
        return {"results": results}
        
    except Exception as e:
        logger.error(f"Error buscando conocimiento: {str(e)}")
        raise HTTPException(status_code=500, detail="Error buscando conocimiento")

@router.get("/context/{query}")
async def get_context(query: str, max_length: int = 1000):
    """
    Obtener contexto relevante formateado para el LLM.
    """
    try:
        context = rag_service.get_relevant_context(
            query=query,
            max_context_length=max_length
        )
        
        return {
            "query": query,
            "context": context,
            "context_length": len(context)
        }
        
    except Exception as e:
        logger.error(f"Error obteniendo contexto: {str(e)}")
        raise HTTPException(status_code=500, detail="Error obteniendo contexto")

@router.put("/{knowledge_id}")
async def update_knowledge(knowledge_id: str, update_data: KnowledgeUpdate):
    """
    Actualizar entrada de conocimiento existente.
    """
    try:
        success = rag_service.update_knowledge(
            knowledge_id=knowledge_id,
            content=update_data.content,
            title=update_data.title,
            metadata=update_data.metadata
        )
        
        if not success:
            raise HTTPException(status_code=404, detail="Conocimiento no encontrado")
        
        return {"message": "Conocimiento actualizado exitosamente"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error actualizando conocimiento: {str(e)}")
        raise HTTPException(status_code=500, detail="Error actualizando conocimiento")

@router.delete("/{knowledge_id}")
async def delete_knowledge(knowledge_id: str):
    """
    Eliminar entrada de conocimiento.
    """
    try:
        success = rag_service.delete_knowledge(knowledge_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Conocimiento no encontrado")
        
        return {"message": "Conocimiento eliminado exitosamente"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error eliminando conocimiento: {str(e)}")
        raise HTTPException(status_code=500, detail="Error eliminando conocimiento")

@router.post("/upload-document")
async def upload_document(
    title: str,
    category: str = "general",
    file: UploadFile = File(...)
):
    """
    Subir documento y extraer conocimiento automáticamente.
    """
    try:
        # Verificar tipo de archivo
        allowed_types = ["text/plain", "application/json"]
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400, 
                detail="Tipo de archivo no soportado. Use .txt o .json"
            )
        
        # Leer contenido del archivo
        content = await file.read()
        
        if file.content_type == "application/json":
            # Procesar archivo JSON
            try:
                json_data = json.loads(content.decode('utf-8'))
                content_text = json.dumps(json_data, indent=2, ensure_ascii=False)
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Archivo JSON inválido")
        else:
            # Procesar archivo de texto
            content_text = content.decode('utf-8')
        
        # Agregar a la base de conocimiento
        knowledge_id = rag_service.add_knowledge(
            title=title,
            content=content_text,
            category=category,
            metadata={
                "source": "uploaded_file",
                "filename": file.filename,
                "content_type": file.content_type
            }
        )
        
        return {
            "message": "Documento subido y procesado exitosamente",
            "knowledge_id": knowledge_id,
            "filename": file.filename
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error subiendo documento: {str(e)}")
        raise HTTPException(status_code=500, detail="Error procesando documento")

@router.post("/initialize-defaults")
async def initialize_default_knowledge():
    """
    Inicializar la base de conocimiento con datos por defecto.
    """
    try:
        rag_service.initialize_default_knowledge()
        
        return {
            "message": "Base de conocimiento inicializada con datos por defecto",
            "knowledge_count": len(rag_service.knowledge_base)
        }
        
    except Exception as e:
        logger.error(f"Error inicializando conocimiento por defecto: {str(e)}")
        raise HTTPException(status_code=500, detail="Error inicializando conocimiento")

@router.get("/stats")
async def get_knowledge_stats():
    """
    Obtener estadísticas de la base de conocimiento.
    """
    try:
        knowledge_list = rag_service.list_knowledge()
        categories = rag_service.get_categories()
        
        # Calcular estadísticas
        total_entries = len(knowledge_list)
        total_chunks = sum(entry["chunks_count"] for entry in knowledge_list)
        total_content_length = sum(entry["content_length"] for entry in knowledge_list)
        
        category_stats = {}
        for category in categories:
            category_entries = [entry for entry in knowledge_list if entry["category"] == category]
            category_stats[category] = {
                "entries": len(category_entries),
                "chunks": sum(entry["chunks_count"] for entry in category_entries)
            }
        
        return {
            "total_entries": total_entries,
            "total_chunks": total_chunks,
            "total_content_length": total_content_length,
            "categories": len(categories),
            "category_stats": category_stats,
            "embeddings_cached": len(rag_service.embeddings_cache)
        }
        
    except Exception as e:
        logger.error(f"Error obteniendo estadísticas: {str(e)}")
        raise HTTPException(status_code=500, detail="Error obteniendo estadísticas")
