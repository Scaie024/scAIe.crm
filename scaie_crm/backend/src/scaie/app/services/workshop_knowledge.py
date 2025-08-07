import re
from typing import Dict, List, Any

# Workshop Knowledge Base - "Sé más eficiente con IA"

workshop_knowledge = {
    "titulo": "Sé más eficiente con IA",
    "descripcion_corta": "Capacita a tu equipo para usar IA sin código y mejora la productividad en todos los departamentos.",
    "descripcion_larga": """Un workshop práctico para que tu equipo aprenda a usar inteligencia artificial en sus procesos diarios. 
    Aumenta la productividad, elimina la brecha entre perfiles jr y sr, y empodera a todos con herramientas de IA sin necesidad de programar.
    
    En este taller ayudamos a las empresas a mejorar sus procesos y enseñamos y empoderamos a las personas a usar la inteligencia artificial, 
    romper la brecha de conocimientos, creación de contenidos y aprovechar herramientas gratuitas que ayuden a la eficiencia de los equipos de la empresa.""",
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
        "Identificación de oportunidades de automatización",
        "Romper la brecha de conocimientos en el equipo",
        "Uso de herramientas gratuitas para mejorar la eficiencia"
    ],
    "resultados": [
        "3 herramientas de IA activas en 2 horas",
        "Proceso automatizado en tu área",
        "Plantillas y prompts personalizados",
        "Plan de implementación de IA",
        "Superación de brecha de conocimiento en el equipo"
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
        "Empodera a los empleados con herramientas de IA",
        "Mejora la eficiencia general de la empresa"
    ],
    "precios": {
        "basico": {
            "nombre": "Básico",
            "precio": "$1,499 MXN",
            "descripcion": "2 horas, online en vivo, hasta 10 personas"
        },
        "profesional": {
            "nombre": "Profesional",
            "precio": "$2,999 MXN",
            "descripcion": "4 horas, online o presencial, hasta 20 personas"
        },
        "empresarial": {
            "nombre": "Empresarial",
            "precio": "$5,000 MXN",
            "descripcion": "4 horas, máximo 10 personas, contenido específico para romper la brecha de conocimiento"
        }
    },
    "detalles_contacto": {
        "telefono": "5535913417",
        "sitio_web": "www.scaie.com.mx",
        "calendly": "https://calendly.com/scaie-empresa/30min?month=2025-08"
    },
    "politicas": {
        "reembolsos": "Reembolsos disponibles hasta 48 horas antes del evento",
        "modificaciones": "Cambios de fecha disponibles con 24 horas de anticipación"
    }
}

workshop_knowledge_instance = workshop_knowledge