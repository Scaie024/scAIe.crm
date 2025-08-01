# SCAIE - Sistema Agente Conversacional de Ventas

## 📋 Versión 1.0 - Listo para Producción

Este proyecto ahora incluye documentación completa para despliegue en producción. Para información detallada sobre cómo desplegar y configurar SCAIE v1.0 en un entorno de producción, por favor consulte:

📁 [`plataforma_agente_scaie/README.md`](file:///Users/arturopinzon/Desktop/scAIe%20-%20Sistema%20Agente/plataforma_agente_scaie/README.md)

## 🚀 Descripción General

SCAIE (Sistema Conversacional de Atención e Inteligencia Empresarial) es una plataforma avanzada de agente conversacional para ventas automatizadas, impulsada por inteligencia artificial. Combina un backend en Python (FastAPI + SQLite/MySQL) con un frontend en Vue 3 para ofrecer una solución completa de gestión de conversaciones y automatización de ventas.

### ¿Qué hace SCAIE?

SCAIE automatiza la interacción con clientes potenciales a través de conversaciones inteligentes, mejorando la eficiencia de ventas y ofreciendo una experiencia personalizada a cada cliente. El sistema puede integrarse con WhatsApp y otras plataformas de mensajería para interactuar con clientes de forma natural y efectiva.

## 📦 Características Principales

- 🤖 **Chat Conversacional con IA** - Agente inteligente basado en Qwen AI
- 📱 **Integración con WhatsApp** - Conecta con tus clientes donde ya están
- 👥 **Gestión de Contactos** - CRUD completo con búsqueda y paginación
- 💬 **Gestión de Conversaciones** - Historial completo de interacciones
- 📊 **Panel de Administración** - Estadísticas y métricas del sistema
- 📥 **Importación/Exportación** - Manejo de datos en CSV y JSON
- 🔐 **Seguridad JWT** - Autenticación segura basada en tokens
- 📚 **API RESTful Documentada** - Integración fácil con otros sistemas
- 🖥️ **Interfaz Web Moderna** - Frontend en Vue 3 con Tailwind CSS

## 🛠️ Tecnologías Utilizadas

### Backend
- **Framework**: FastAPI
- **Lenguaje**: Python 3.10+
- **Base de Datos**: SQLite/MySQL
- **ORM**: SQLAlchemy
- **Documentación API**: Swagger UI / ReDoc

### Frontend
- **Framework**: Vue 3 (Composition API)
- **Build Tool**: Vite
- **Estilos**: TailwindCSS
- **Rutas**: Vue Router

## 🚀 Inicio Rápido

### Ejecutar el Sistema

```bash
cd plataforma_agente_scaie
chmod +x start.sh
./start.sh
```

El sistema estará disponible en:
- Frontend: http://localhost:8001/
- API: http://localhost:8001/api
- Documentación interactiva: http://localhost:8001/docs

## 📖 Documentación Completa

Para documentación detallada de producción, incluyendo:
- Despliegue con Docker
- Configuración de variables de entorno
- Consideraciones de seguridad
- Monitoreo y mantenimiento

Por favor consulte: 📁 [`plataforma_agente_scaie/README.md`](file:///Users/arturopinzon/Desktop/scAIe%20-%20Sistema%20Agente/plataforma_agente_scaie/README.md)

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](file:///Users/arturopinzon/Desktop/scAIe%20-%20Sistema%20Agente/plataforma_agente_scaie/LICENSE) para más detalles.

<div align="center">
  <p>Desarrollado con ❤️ por el equipo de SCAIE</p>
  <p>🚀 Potenciado por Qwen AI</p>
</div>