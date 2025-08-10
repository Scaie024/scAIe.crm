import re
from typing import Dict, List, Any

# SCAIE Knowledge Base

# Información básica sobre SCAIE basada en www.scaie.com.mx
scaie_knowledge_data = {
    "descripcion": "SCAIE es una consultoría tecnológica especializada en inteligencia artificial que ayuda a las empresas a mejorar su eficiencia mediante la automatización de procesos y optimización de ventas.",
    "caracteristicas": [
        "Consultoría en inteligencia artificial y automatización",
        "Metodología OPT (Organización, Procesos y Tecnología)",
        "Automatización de ventas mediante agentes conversacionales",
        "Optimización de procesos empresariales",
        "Soluciones personalizadas basadas en IA",
        "Integración con WhatsApp, Facebook Messenger y otros canales",
        "Panel de Administración completo",
        "Gestión de Contactos y Conversaciones",
        "Importación/Exportación de Datos (CSV, JSON)"
    ],
    "beneficios": [
        "Aumenta las ventas mediante automatización inteligente",
        "Reduce costos operativos al automatizar tareas repetitivas",
        "Mejora la atención al cliente con respuestas 24/7",
        "Obtén insights valiosos de las interacciones con clientes",
        "Escala tu negocio sin aumentar proporcionalmente el personal",
        "Mantén una presencia constante en múltiples canales de comunicación"
    ],
    "metodologia": {
        "nombre": "OPT - Organización, Procesos y Tecnología",
        "descripcion": "Nuestro enfoque integral para transformar tu negocio",
        "componentes": [
            "Organización: Optimización de estructuras y roles",
            "Procesos: Mejora y automatización de flujos de trabajo",
            "Tecnología: Implementación de soluciones de vanguardia"
        ]
    },
    "tecnologias": {
        "backend": ["Python", "FastAPI", "SQLite/MySQL"],
        "frontend": ["Vue 3", "Vite", "TailwindCSS"],
        "ai": ["Qwen (Aliyun Dashscope)"],
        "comunicacion": ["API REST", "WebSockets"]
    },
    "servicios": [
        "Agentes conversacionales para ventas automatizadas",
        "Consultoría en inteligencia artificial",
        "Automatización de procesos empresariales",
        "Optimización de ventas mediante IA",
        "Integración multicanal (WhatsApp, Facebook, etc.)",
        "Análisis de datos y generación de insights"
    ],
    "contacto": {
        "telefono_humano": "5535913417",
        "nombre_asesor": "Asesor SCAIE",
        "calendly_url": "https://calendly.com/scaie/consulta",
        "horario": "Lunes a Viernes 9:00 AM - 6:00 PM",
        "whatsapp": "https://wa.me/5535913417"
    },
    "frases_persuasivas": [
        "¿Te gustaría ver esto funcionando en tu empresa?",
        "Tenemos casos de éxito similares al tuyo",
        "El retorno de inversión se ve en las primeras semanas",
        "¿Cuándo podrías dedicar 30 min para ver una demo?",
        "Otros clientes han aumentado ventas 40% el primer mes"
    ],
    "call_to_actions": [
        "Agenda una llamada estratégica gratuita",
        "Habla directo con nuestro especialista al 5535913417", 
        "Reserva tu consultoría sin costo",
        "Solicita una demo personalizada"
    ],
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
        self.knowledge_base = scaie_knowledge_data
    
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
        if any(keyword in query_lower for keyword in ['precio', 'costo', 'plan', 'suscripción', 'cuanto', 'cuesta']):
            relevant_sections.append("Planes y precios:")
            for plan_key, plan_data in self.knowledge_base["precios"].items():
                relevant_sections.append(f"- {plan_data['nombre']}: {plan_data['precio']}")
                
        if any(keyword in query_lower for keyword in ['característica', 'función', 'funcionalidad', 'que hace', 'que puedes']):
            relevant_sections.append("Características principales:")
            for feature in self.knowledge_base["caracteristicas"]:
                relevant_sections.append(f"- {feature}")
                
        if any(keyword in query_lower for keyword in ['beneficio', 'ventaja', 'ayuda', 'para que']):
            relevant_sections.append("Beneficios:")
            for benefit in self.knowledge_base["beneficios"]:
                relevant_sections.append(f"- {benefit}")
                
        if any(keyword in query_lower for keyword in ['tecnología', 'tecnología', 'lenguaje']):
            relevant_sections.append("Tecnologías utilizadas:")
            for tech_category, tech_list in self.knowledge_base["tecnologias"].items():
                relevant_sections.append(f"- {tech_category.title()}: {', '.join(tech_list)}")
                
        if any(keyword in query_lower for keyword in ['servicio', 'que ofrecen', 'que hacen']):
            relevant_sections.append("Servicios que ofrecemos:")
            for service in self.knowledge_base["servicios"]:
                relevant_sections.append(f"- {service}")
                
        if any(keyword in query_lower for keyword in ['metodología', 'metodo', 'opt']):
            relevant_sections.append("Nuestra metodología OPT:")
            relevant_sections.append(self.knowledge_base["metodologia"]["descripcion"])
            for component in self.knowledge_base["metodologia"]["componentes"]:
                relevant_sections.append(f"- {component}")
        
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