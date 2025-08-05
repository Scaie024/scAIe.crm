# scAIe - Sistema Agente

Sistema de agente de inteligencia artificial para automatización de ventas con integración multiplataforma.

## Descripción

scAIe (Sistema Conversacional de Agente de Inteligencia Artificial) es una plataforma avanzada de ventas automatizadas que utiliza inteligencia artificial para interactuar con clientes potenciales a través de múltiples canales de comunicación. El sistema está diseñado para identificar el nivel de interés de los contactos, proporcionar información relevante sobre productos/servicios y automatizar el proceso de calificación de leads.

## Arquitectura del Sistema

### Tecnologías Principales
- **Backend**: Python/FastAPI
- **Base de Datos**: SQLite con SQLAlchemy ORM
- **Frontend**: Vue.js 3 con Vite
- **IA**: Integración con Qwen API (Alibaba Cloud)
- **Mensajería**: Telegram Bot API, Facebook Graph API (WhatsApp)
- **Despliegue**: Docker, Nginx

### Estructura del Proyecto
```
scaie_crm/
├── backend/                 # Aplicación FastAPI
│   ├── src/scaie/app/       # Código fuente principal
│   │   ├── api/             # Endpoints de la API
│   │   ├── core/            # Configuración del núcleo
│   │   ├── models/          # Modelos de base de datos
│   │   ├── schemas/         # Esquemas Pydantic
│   │   ├── services/        # Lógica de negocio y servicios
│   │   └── static/          # Archivos estáticos (build del frontend)
├── frontend/                # Aplicación Vue.js
│   ├── src/                 # Código fuente del frontend
│   │   ├── components/      # Componentes Vue
│   │   ├── pages/           # Páginas principales
│   │   ├── router/          # Configuración de rutas
│   │   ├── services/        # Clientes API
│   │   └── utils/           # Funciones utilitarias
├── docs/                    # Documentación
├── scripts/                 # Scripts de utilidad
└── config/                  # Archivos de configuración
```

Para información más detallada sobre la estructura del proyecto, consulte [PROJECT_STRUCTURE.md](scaie_crm/docs/development/PROJECT_STRUCTURE.md).

## Características Principales

1. **Agente de IA Omnipotente**: Capaz de mantener conversaciones naturales con clientes potenciales
2. **Gestión de Contactos**: Base de datos completa de contactos con seguimiento de interés
3. **Multiplataforma**: Integración con Telegram y WhatsApp
4. **Dashboard Interactivo**: Panel de control con estadísticas en tiempo real
5. **Sistema de Interés**: Clasificación de contactos de 1-5 estrellas basado en interacciones
6. **Personalización**: Configuración del agente para diferentes contextos de negocio

## Requisitos del Sistema

- Python 3.8+
- Node.js 14+
- npm o yarn
- Acceso a API de Qwen (Alibaba Cloud)
- Cuentas de Telegram y/o WhatsApp Business (para integración completa)

## Instalación y Configuración

1. Clonar el repositorio
2. Configurar variables de entorno (`.env` files)
3. Ejecutar script de inicialización: `./scripts/init_project.sh`
4. Iniciar la aplicación: `./scripts/run_with_ngrok.sh`

## Documentación

La documentación completa se encuentra en el directorio [docs/](scaie_crm/docs/), incluyendo:
- [Guía de Desarrollo](scaie_crm/docs/development/)
- [Documentación de Despliegue](scaie_crm/docs/deployment/)
- [Documentación Técnica](scaie_crm/docs/development/TECHNICAL_DOCS.md)

## Contribuciones

Este proyecto está en constante evolución. Para contribuir, por favor revise la documentación de desarrollo y siga las mejores prácticas establecidas.