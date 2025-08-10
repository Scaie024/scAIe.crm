import os
import logging
from typing import List, Dict, Any, Optional
import json
import asyncio
from datetime import datetime
import hashlib

# Vector database - using simple file-based storage for now
# In production, consider using ChromaDB, FAISS, or Pinecone
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self):
        self.model = None
        self.knowledge_base = {}
        self.embeddings_cache = {}
        self.knowledge_path = "data/knowledge"
        self.embeddings_path = "data/embeddings"
        self.model_name = "all-MiniLM-L6-v2"  # Lightweight embedding model
        
        # Create directories if they don't exist
        os.makedirs(self.knowledge_path, exist_ok=True)
        os.makedirs(self.embeddings_path, exist_ok=True)
        
        # Initialize model
        self._initialize_model()
        
        # Load existing knowledge base
        self._load_knowledge_base()
    
    def _initialize_model(self):
        """Initialize the sentence transformer model for embeddings."""
        try:
            self.model = SentenceTransformer(self.model_name)
            logger.info(f"Initialized embedding model: {self.model_name}")
        except Exception as e:
            logger.error(f"Error initializing embedding model: {str(e)}")
            self.model = None
    
    def _load_knowledge_base(self):
        """Load the knowledge base from disk."""
        try:
            knowledge_file = os.path.join(self.knowledge_path, "knowledge_base.json")
            if os.path.exists(knowledge_file):
                with open(knowledge_file, 'r', encoding='utf-8') as f:
                    self.knowledge_base = json.load(f)
                logger.info(f"Loaded {len(self.knowledge_base)} knowledge entries")
            
            # Load embeddings cache
            embeddings_file = os.path.join(self.embeddings_path, "embeddings_cache.pkl")
            if os.path.exists(embeddings_file):
                with open(embeddings_file, 'rb') as f:
                    self.embeddings_cache = pickle.load(f)
                logger.info(f"Loaded {len(self.embeddings_cache)} cached embeddings")
                
        except Exception as e:
            logger.error(f"Error loading knowledge base: {str(e)}")
    
    def _save_knowledge_base(self):
        """Save the knowledge base to disk."""
        try:
            knowledge_file = os.path.join(self.knowledge_path, "knowledge_base.json")
            with open(knowledge_file, 'w', encoding='utf-8') as f:
                json.dump(self.knowledge_base, f, ensure_ascii=False, indent=2)
            
            # Save embeddings cache
            embeddings_file = os.path.join(self.embeddings_path, "embeddings_cache.pkl")
            with open(embeddings_file, 'wb') as f:
                pickle.dump(self.embeddings_cache, f)
                
            logger.info("Knowledge base and embeddings saved")
        except Exception as e:
            logger.error(f"Error saving knowledge base: {str(e)}")
    
    def _get_text_hash(self, text: str) -> str:
        """Generate a hash for text to use as cache key."""
        return hashlib.md5(text.encode()).hexdigest()
    
    def _get_embedding(self, text: str) -> Optional[np.ndarray]:
        """Get embedding for text, using cache if available."""
        if not self.model:
            return None
            
        text_hash = self._get_text_hash(text)
        
        # Check cache first
        if text_hash in self.embeddings_cache:
            return np.array(self.embeddings_cache[text_hash])
        
        try:
            # Generate new embedding
            embedding = self.model.encode(text, convert_to_numpy=True)
            
            # Cache the embedding
            self.embeddings_cache[text_hash] = embedding.tolist()
            
            return embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            return None
    
    def add_knowledge(self, title: str, content: str, category: str = "general", metadata: Dict[str, Any] = None) -> str:
        """Add new knowledge to the knowledge base."""
        knowledge_id = f"{category}_{self._get_text_hash(content)[:8]}"
        
        # Split content into chunks for better retrieval
        chunks = self._chunk_text(content)
        
        knowledge_entry = {
            "id": knowledge_id,
            "title": title,
            "content": content,
            "chunks": chunks,
            "category": category,
            "metadata": metadata or {},
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        self.knowledge_base[knowledge_id] = knowledge_entry
        
        # Generate embeddings for chunks
        for i, chunk in enumerate(chunks):
            chunk_id = f"{knowledge_id}_chunk_{i}"
            embedding = self._get_embedding(chunk)
            if embedding is not None:
                self.embeddings_cache[self._get_text_hash(chunk)] = embedding.tolist()
        
        self._save_knowledge_base()
        logger.info(f"Added knowledge: {title} ({len(chunks)} chunks)")
        
        return knowledge_id
    
    def _chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """Split text into overlapping chunks for better retrieval."""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            if chunk.strip():
                chunks.append(chunk.strip())
        
        return chunks
    
    def search_knowledge(self, query: str, top_k: int = 5, category: str = None) -> List[Dict[str, Any]]:
        """Search for relevant knowledge based on query."""
        if not self.model or not self.knowledge_base:
            return []
        
        try:
            # Get query embedding
            query_embedding = self._get_embedding(query)
            if query_embedding is None:
                return []
            
            candidates = []
            
            # Search through all knowledge entries
            for knowledge_id, knowledge in self.knowledge_base.items():
                if category and knowledge.get("category") != category:
                    continue
                
                # Search through chunks
                for i, chunk in enumerate(knowledge.get("chunks", [])):
                    chunk_embedding = self._get_embedding(chunk)
                    if chunk_embedding is not None:
                        # Calculate cosine similarity
                        similarity = np.dot(query_embedding, chunk_embedding) / (
                            np.linalg.norm(query_embedding) * np.linalg.norm(chunk_embedding)
                        )
                        
                        candidates.append({
                            "knowledge_id": knowledge_id,
                            "chunk_index": i,
                            "chunk": chunk,
                            "title": knowledge.get("title", ""),
                            "category": knowledge.get("category", ""),
                            "similarity": float(similarity),
                            "metadata": knowledge.get("metadata", {})
                        })
            
            # Sort by similarity and return top results
            candidates.sort(key=lambda x: x["similarity"], reverse=True)
            return candidates[:top_k]
            
        except Exception as e:
            logger.error(f"Error searching knowledge: {str(e)}")
            return []
    
    def get_relevant_context(self, query: str, max_context_length: int = 1000) -> str:
        """Get relevant context for a query, formatted for LLM input."""
        relevant_chunks = self.search_knowledge(query, top_k=3)
        
        if not relevant_chunks:
            return ""
        
        context_parts = []
        current_length = 0
        
        for chunk_info in relevant_chunks:
            chunk = chunk_info["chunk"]
            title = chunk_info["title"]
            
            # Format the chunk with title
            formatted_chunk = f"**{title}**\n{chunk}\n"
            
            if current_length + len(formatted_chunk) > max_context_length:
                break
            
            context_parts.append(formatted_chunk)
            current_length += len(formatted_chunk)
        
        return "\n".join(context_parts)
    
    def update_knowledge(self, knowledge_id: str, content: str = None, title: str = None, metadata: Dict[str, Any] = None) -> bool:
        """Update existing knowledge entry."""
        if knowledge_id not in self.knowledge_base:
            return False
        
        knowledge = self.knowledge_base[knowledge_id]
        
        if content is not None:
            knowledge["content"] = content
            knowledge["chunks"] = self._chunk_text(content)
            
            # Regenerate embeddings for updated chunks
            for i, chunk in enumerate(knowledge["chunks"]):
                embedding = self._get_embedding(chunk)
                if embedding is not None:
                    self.embeddings_cache[self._get_text_hash(chunk)] = embedding.tolist()
        
        if title is not None:
            knowledge["title"] = title
        
        if metadata is not None:
            knowledge["metadata"].update(metadata)
        
        knowledge["updated_at"] = datetime.now().isoformat()
        
        self._save_knowledge_base()
        logger.info(f"Updated knowledge: {knowledge_id}")
        
        return True
    
    def delete_knowledge(self, knowledge_id: str) -> bool:
        """Delete knowledge entry."""
        if knowledge_id not in self.knowledge_base:
            return False
        
        # Remove embeddings from cache
        knowledge = self.knowledge_base[knowledge_id]
        for chunk in knowledge.get("chunks", []):
            chunk_hash = self._get_text_hash(chunk)
            if chunk_hash in self.embeddings_cache:
                del self.embeddings_cache[chunk_hash]
        
        del self.knowledge_base[knowledge_id]
        self._save_knowledge_base()
        logger.info(f"Deleted knowledge: {knowledge_id}")
        
        return True
    
    def list_knowledge(self, category: str = None) -> List[Dict[str, Any]]:
        """List all knowledge entries."""
        entries = []
        
        for knowledge_id, knowledge in self.knowledge_base.items():
            if category and knowledge.get("category") != category:
                continue
            
            entries.append({
                "id": knowledge_id,
                "title": knowledge.get("title", ""),
                "category": knowledge.get("category", ""),
                "content_length": len(knowledge.get("content", "")),
                "chunks_count": len(knowledge.get("chunks", [])),
                "created_at": knowledge.get("created_at", ""),
                "updated_at": knowledge.get("updated_at", ""),
                "metadata": knowledge.get("metadata", {})
            })
        
        return sorted(entries, key=lambda x: x["updated_at"], reverse=True)
    
    def get_categories(self) -> List[str]:
        """Get all available categories."""
        categories = set()
        for knowledge in self.knowledge_base.values():
            categories.add(knowledge.get("category", "general"))
        return sorted(list(categories))
    
    def initialize_default_knowledge(self):
        """Initialize with default SCAIE knowledge."""
        default_knowledge = [
            {
                "title": "SCAIE - Qué es y qué hace",
                "content": """SCAIE es una empresa especializada en automatización empresarial con inteligencia artificial. 
                Ayudamos a las empresas a implementar IA sin código para mejorar la productividad en todos los departamentos.
                
                Nuestros servicios incluyen:
                - Workshops de capacitación en IA
                - Consultoría en automatización de procesos
                - Implementación de soluciones de IA personalizadas
                - Análisis de datos y visualización
                - Generación de contenido automatizada
                
                SCAIE se enfoca en hacer la IA accesible para todas las empresas, sin importar su tamaño o sector.""",
                "category": "empresa"
            },
            {
                "title": "Workshop: Sé más eficiente con IA",
                "content": """Workshop especializado para equipos que quieren implementar IA sin código.
                
                MODALIDADES:
                - Online en vivo (recomendado)
                - Presencial 
                - Híbrido
                
                PRECIOS:
                - Básico: $1,499 MXN (2 horas, hasta 10 personas)
                - Profesional: $2,999 MXN (4 horas, hasta 20 personas)  
                - Empresarial: $5,000 MXN (contenido específico para la empresa)
                
                INCLUYE:
                - Manual del workshop
                - Grabación de la sesión
                - Sesión de seguimiento (30 minutos)
                - Acceso a herramientas freemium
                
                El workshop cubre automatización de tareas, análisis de datos, generación de contenido y más.""",
                "category": "servicios"
            },
            {
                "title": "Información de Contacto",
                "content": """DATOS DE CONTACTO SCAIE:
                
                Teléfono: 55 3591 3417
                WhatsApp: https://wa.me/525535913417
                Email: info@scaie.com.mx
                Website: www.scaie.com.mx
                
                AGENDA UNA LLAMADA GRATUITA:
                https://calendly.com/scaie-empresa/30min
                
                HORARIOS DE ATENCIÓN:
                Lunes a Viernes: 9:00 AM - 6:00 PM (GMT-6)
                
                OBJETIVO: El agente debe dirigir todas las conversaciones hacia agendar una llamada al 55 3591 3417""",
                "category": "contacto"
            }
        ]
        
        for knowledge in default_knowledge:
            self.add_knowledge(
                title=knowledge["title"],
                content=knowledge["content"],
                category=knowledge["category"]
            )
        
        logger.info("Initialized default knowledge base")

# Create singleton instance
rag_service = RAGService()

# Initialize with default knowledge if empty
if not rag_service.knowledge_base:
    rag_service.initialize_default_knowledge()
