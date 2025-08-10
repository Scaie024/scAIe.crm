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
    # Ejemplos concretos de tareas diarias donde el taller ayuda
    "tareas_diarias_ejemplos": [
        "Resumir correos y redactar respuestas en 1 clic",
        "Generar reportes en Excel/Sheets a partir de datos crudos",
        "Crear minutas y to‑dos automáticos después de reuniones",
        "Redactar propuestas y cotizaciones con plantillas inteligentes",
        "Clasificar y priorizar tickets o solicitudes repetitivas",
        "Generar contenido para marketing (posts, copies, imágenes)"
    ],
    # Casos de uso por rol/área para mensajes más persuasivos
    "casos_uso_por_rol": {
        "ventas": [
            "Redactar correos de seguimiento personalizados",
            "Priorizar leads y preparar propuestas en minutos",
            "Resumir llamadas y extraer próximos pasos"
        ],
        "administracion": [
            "Automatizar conciliación básica y controles en Excel",
            "Generar reportes mensuales a partir de datos",
            "Estandarizar respuestas a proveedores y clientes"
        ],
        "gerencia": [
            "Obtener resúmenes ejecutivos y tableros",
            "Detectar cuellos de botella en procesos",
            "Alinear equipos con plantillas y flujos claros"
        ],
        "marketing": [
            "Crear calendarios de contenido",
            "Generar copies y piezas visuales",
            "Analizar rendimiento de campañas"
        ],
        "operaciones": [
            "Estandarizar SOPs y checklists inteligentes",
            "Reducir tiempos de respuesta en tickets",
            "Automatizar asignaciones y notificaciones"
        ],
        "rrhh": [
            "Filtrar CVs con criterios objetivos",
            "Redactar descripciones de puestos",
            "Documentar onboarding con plantillas"
        ]
    },
    # Respuestas breves a objeciones frecuentes
    "objecciones": {
        "no_tengo_tiempo": {
            "keywords": ["no tengo tiempo", "sin tiempo", "muy ocupado"],
            "respuesta": "Justo por eso: en 2 horas sales con 2‑3 automatizaciones listas que te ahorran tiempo desde mañana. ¿Prefieres 2h o 4h?"
        },
        "no_se_programar": {
            "keywords": ["no se programar", "no s\u00E9 programar", "no programo", "sin programar"],
            "respuesta": "No necesitas programar. Usamos herramientas sin código con pasos guiados. ¿En qué tarea te gustaría empezar?"
        },
        "precio": {
            "keywords": ["precio", "costo", "cuanto", "cu\u00E1nto"],
            "respuesta": "Desde $1,499 MXN. Incluye ejemplos aplicados a tu equipo y una sesión de seguimiento. ¿Cuántas personas serían?"
        },
        "ya_uso_ia": {
            "keywords": ["ya uso ia", "ya usamos ia", "ya usamos chatgpt"],
            "respuesta": "Excelente. El valor está en estandarizar y escalar: plantillas, flujos y medición. ¿Qué proceso quisieras formalizar primero?"
        },
        "privacidad": {
            "keywords": ["privacidad", "datos", "confidencial"],
            "respuesta": "Trabajamos con buenas prácticas y datos de muestra; nada sensible. Si lo requieres, cubrimos opciones privadas. ¿Qué dato te preocupa?"
        }
    },
    "beneficios": [
        "Aumenta productividad del equipo 30-50%",
        "Elimina brecha entre perfiles jr y sr",
        "Reduce tiempo en tareas repetitivas 70%",
        "Empodera a los empleados con herramientas de IA",
        "Mejora la eficiencia general de la empresa"
    ],
    # Herramientas gratuitas o freemium recomendadas (no-code / low-code)
    "herramientas_gratuitas": {
        "texto": ["ChatGPT (free)", "Gemini", "Perplexity"],
        "automatizacion": ["Make/Zapier (free tier)", "IFTTT"],
        "datos": ["Google Sheets", "Excel + complementos"],
        "imagenes": ["Canva", "Ideogram"],
        "notas": ["Notion", "Obsidian"]
    },
    # Consejos de prompting sencillos y accionables
    "consejos_prompts": [
        "Da contexto y objetivo en 1 frase",
        "Muestra 1 ejemplo del resultado que esperas",
        "Pide pasos y formato de salida (viñetas, tabla)",
        "Limita tiempo/palabras para enfocarlo",
        "Itera: mejora el resultado con tus comentarios"
    ],
    # Temas de tendencia resumidos en lenguaje simple
    "temas_tendencia": {
        "agentes": "Bots que ejecutan pasos por ti (buscar, resumir, escribir) con objetivos simples",
        "rag": "Conectar tus documentos a la IA para respuestas con citas y contexto",
        "vision": "Analizar imágenes o PDFs para extraer datos y describir contenido"
    },
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