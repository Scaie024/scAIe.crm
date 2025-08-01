import re
from typing import Dict, List, Any

# SCAIE Knowledge Base

# Información básica sobre SCAIE
scaie_knowledge = {
    "descripcion": "SCAIE es una plataforma avanzada de agente conversacional para ventas, impulsada por inteligencia artificial.",
    "caracteristicas": [
        "Chat Interactivo con IA avanzada",
        "Integración con WhatsApp y Messenger",
        "Panel de Administración completo",
        "Gestión de Contactos y Conversaciones",
        "Importación/Exportación de Datos (CSV, JSON)",
        "WebSockets para actualizaciones en tiempo real",
        "Diseño Responsive",
        "Seguridad con autenticación JWT",
        "API RESTful documentada"
    ],
    "beneficios": [
        "Automatiza la interacción con clientes potenciales",
        "Mejora la eficiencia en ventas mediante IA conversacional avanzada",
        "Ofrece una interfaz intuitiva y herramientas de análisis",
        "Reduce el tiempo de atención al cliente",
        "Permite escalar la atención personalizada a través de chatbots"
    ],
    "tecnologias": {
        "backend": ["Python", "FastAPI", "SQLite/MySQL"],
        "frontend": ["Vue 3", "Vite", "TailwindCSS"],
        "ai": ["Qwen (Aliyun Dashscope)"],
        "comunicacion": ["API REST", "WebSockets"]
    },
    "precios": {
        "basico": {
            "nombre": "Básico",
            "precio": "$99/mes",
            "caracteristicas": [
                "Hasta 1,000 conversaciones/mes",
                "Integración con WhatsApp",
                "Panel de administración básico",
                "Soporte por correo"
            ]
        },
        "profesional": {
            "nombre": "Profesional",
            "precio": "$299/mes",
            "caracteristicas": [
                "Hasta 10,000 conversaciones/mes",
                "Integración con WhatsApp y Messenger",
                "Panel de administración avanzado",
                "API REST completa",
                "Soporte prioritario 24/7"
            ]
        },
        "empresarial": {
            "nombre": "Empresarial",
            "precio": "Personalizado",
            "caracteristicas": [
                "Conversaciones ilimitadas",
                "Integraciones personalizadas",
                "Panel de administración completo",
                "API REST completa",
                "Soporte 24/7 dedicado",
                "Personalización avanzada"
            ]
        }
    }
}

class SCAIEKnowledge:
    def __init__(self):
        self.knowledge_base = scaie_knowledge
    
    def get_knowledge(self, query: str) -> Dict[str, Any]:
        """
        Get relevant knowledge based on the user query.
        
        Args:
            query: User query string
            
        Returns:
            Dict with relevant knowledge sections
        """
        # Simple keyword-based matching for now
        relevant_sections = []
        
        # Convert query to lowercase for matching
        query_lower = query.lower()
        
        # Check for keywords in the query
        if any(keyword in query_lower for keyword in ['precio', 'costo', 'plan', 'suscripción']):
            relevant_sections.append("Planes y precios:")
            for plan_key, plan_data in self.knowledge_base["precios"].items():
                relevant_sections.append(f"- {plan_data['nombre']}: {plan_data['precio']}")
                
        if any(keyword in query_lower for keyword in ['característica', 'función', 'funcionalidad']):
            relevant_sections.append("Características principales:")
            for feature in self.knowledge_base["caracteristicas"]:
                relevant_sections.append(f"- {feature}")
                
        if any(keyword in query_lower for keyword in ['beneficio', 'ventaja']):
            relevant_sections.append("Beneficios:")
            for benefit in self.knowledge_base["beneficios"]:
                relevant_sections.append(f"- {benefit}")
                
        if any(keyword in query_lower for keyword in ['tecnología', 'tecnología', 'lenguaje']):
            relevant_sections.append("Tecnologías utilizadas:")
            for tech_category, tech_list in self.knowledge_base["tecnologias"].items():
                relevant_sections.append(f"- {tech_category.title()}: {', '.join(tech_list)}")
        
        # If no specific matches, provide general description
        if not relevant_sections:
            relevant_sections.append(self.knowledge_base["descripcion"])
            relevant_sections.append("Características principales:")
            for feature in self.knowledge_base["caracteristicas"][:3]:  # First 3 features
                relevant_sections.append(f"- {feature}")
        
        return {
            "success": True,
            "relevant_sections": relevant_sections
        }

# Create global instance
scaie_knowledge = SCAIEKnowledge()

# Función para obtener conocimiento sobre SCAIE
def get_scaie_knowledge():
    return scaie_knowledge