import re
from typing import Dict, List, Any

# Workshop Knowledge Base - "Sé más eficiente con IA"

workshop_knowledge = {
    "titulo": "Sé más eficiente con IA",
    "descripcion_corta": "Capacita a tu equipo para usar IA sin código y mejora la productividad en todos los departamentos.",
    "descripcion_larga": """Un workshop práctico para que tu equipo aprenda a usar inteligencia artificial en sus procesos diarios. 
    Aumenta la productividad, elimina la brecha entre perfiles jr y sr, y empodera a todos con herramientas de IA sin necesidad de programar.""",
    "duracion": {
        "corta": "2 horas",
        "larga": "4 horas",
        "flexible": "Adaptable a necesidades"
    },
    "modalidades": [
        "Online en vivo (recomendado)",
        "Presencial",
        "Híbrido"
    ],
    "publico_objetivo": [
        "Equipos de ventas",
        "Personal administrativo",
        "Gerentes y supervisores",
        "Emprendedores",
        "Cualquier persona interesada en mejorar su eficiencia"
    ],
    "temario": [
        "Introducción a la IA generativa",
        "Herramientas sin código para automatizar tareas",
        "Análisis de datos con IA",
        "Creación de contenido con IA",
        "Identificación de oportunidades de automatización"
    ],
    "resultados": [
        "3 herramientas de IA activas en 2 horas",
        "Proceso automatizado en tu área",
        "Plantillas y prompts personalizados",
        "Plan de implementación de IA"
    ],
    "inclusiones": [
        "Diagnóstico previo del equipo",
        "Manual del workshop",
        "Acceso a herramientas freemium",
        "Grabación de la sesión",
        "Sesión de seguimiento (30 minutos)"
    ],
    "beneficios": [
        "Aumenta productividad del equipo 30-50%",
        "Elimina brecha entre perfiles jr y sr",
        "Reduce tiempo en tareas repetitivas 70%",
        "Empodera al equipo con nuevas habilidades"
    ],
    "precios": {
        "basico": {
            "nombre": "Básico",
            "precio": "$1,499 MXN",
            "descripcion": "Workshop estándar para hasta 10 personas",
            "caracteristicas": [
                "Duración: 2 horas",
                "Modalidad: Online en vivo",
                "Manual del workshop",
                "Grabación de la sesión"
            ]
        },
        "profesional": {
            "nombre": "Profesional",
            "precio": "$2,999 MXN",
            "descripcion": "Workshop completo con personalización para hasta 20 personas",
            "caracteristicas": [
                "Duración: 4 horas",
                "Modalidad: Online en vivo o presencial",
                "Diagnóstico previo del equipo",
                "Manual del workshop personalizado",
                "Grabación de la sesión",
                "Sesión de seguimiento (30 minutos)"
            ]
        },
        "empresarial": {
            "nombre": "Empresarial",
            "precio": "Precio personalizado",
            "descripcion": "Implementación completa con múltiples sesiones",
            "caracteristicas": [
                "Múltiples sesiones personalizadas",
                "Diagnóstico detallado de procesos",
                "Implementación guiada de soluciones",
                "Soporte post-workshop por 30 días",
                "Reporte de impacto"
            ]
        }
    },
    "testimonios": [
        {
            "empresa": "Tecnosoluciones SA de CV",
            "testimonial": "Nuestro equipo de ventas redujo 3 horas semanales en reportes. Ahora usan ese tiempo para prospectar nuevos clientes.",
            "impacto": "3 horas semanales recuperadas por vendedor"
        },
        {
            "empresa": "Distribuidora Mérida",
            "testimonial": "Implementamos 5 automatizaciones en el primer mes. El gerente dice que el workshop pagó su inversión en la primera semana.",
            "impacto": "5 automatizaciones implementadas en el primer mes"
        }
    ],
    "objeciones_comunes": {
        "costo": {
            "objecion": "Es muy caro",
            "respuesta": "La inversión se recupera en la primera semana al automatizar tareas que toman horas cada semana."
        },
        "tiempo": {
            "objecion": "No tenemos tiempo para esto",
            "respuesta": "Precisamente por eso es importante. El workshop te da herramientas para recuperar horas cada semana."
        },
        "utilidad": {
            "objecion": "No sé si nos sirva",
            "respuesta": "Empezamos con un diagnóstico gratuito de 15 minutos para identificar qué tareas podrían automatizarse en tu negocio."
        },
        "complejidad": {
            "objecion": "Suena muy complicado",
            "respuesta": "El workshop está diseñado para personas sin conocimiento técnico. Terminas con herramientas funcionando en tu computadora."
        }
    }
}

class WorkshopKnowledge:
    def __init__(self):
        self.knowledge_base = workshop_knowledge
    
    def get_workshop_overview(self) -> str:
        """Get a concise overview of the workshop"""
        return f"""
Workshop: {self.knowledge_base['titulo']}
Duración: {self.knowledge_base['duracion']['corta']} - {self.knowledge_base['duracion']['larga']}
Descripción: {self.knowledge_base['descripcion_corta']}
Resultados: {'; '.join(self.knowledge_base['resultados'][:2])}
        """.strip()
    
    def get_detailed_info(self, section: str) -> Dict[str, Any]:
        """Get detailed information about a specific section of the workshop"""
        if section in self.knowledge_base:
            return {
                "success": True,
                "section": section,
                "data": self.knowledge_base[section]
            }
        return {
            "success": False,
            "error": f"Section '{section}' not found"
        }
    
    def get_pricing_info(self) -> Dict[str, Any]:
        """Get pricing information"""
        return self.get_detailed_info("precios")
    
    def get_objection_response(self, objection_key: str) -> Dict[str, Any]:
        """Get a prepared response to a common objection"""
        if objection_key in self.knowledge_base["objeciones_comunes"]:
            return {
                "success": True,
                "objection": self.knowledge_base["objeciones_comunes"][objection_key]["objecion"],
                "response": self.knowledge_base["objeciones_comunes"][objection_key]["respuesta"]
            }
        return {
            "success": False,
            "error": f"Objection '{objection_key}' not found"
        }
    
    def get_testimonials(self) -> List[Dict[str, str]]:
        """Get workshop testimonials"""
        return self.knowledge_base["testimonios"]

# Create global instance
workshop_knowledge_instance = WorkshopKnowledge()