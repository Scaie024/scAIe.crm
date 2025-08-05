# Registro de Cambios - SCAIE

## [2.1.0] - 2025-08-04

### Añadido
- Integración completa con Telegram Bot API
- Servicio de Telegram para manejar comunicaciones con el bot
- Campo `telegram_user_id` en el modelo de contactos
- Soporte para comandos `/start` y `/help` en Telegram
- Inicialización automática del bot de Telegram en el script de ejecución
- Documentación de integración con Telegram en README.md

### Mejorado
- Script de ejecución `run_scaie.sh` para iniciar automáticamente el bot de Telegram
- Modelo de contactos para almacenar IDs de usuarios de diferentes plataformas
- Servicio del agente todopoderoso para manejar identificación de usuarios en múltiples plataformas
- Actualización de dependencias para incluir `python-telegram-bot`

### Cambiado
- Versión actualizada a 2.1.0 para reflejar la integración con Telegram
- README.md actualizado con instrucciones de configuración de Telegram

## [2.0.0] - 2025-08-04

### Añadido
- Script de ejecución mejorado `run_scaie.sh` con verificación de variables de entorno y base de datos
- Sistema de tareas automatizadas para seguimiento de clientes
- Agente todopoderoso con capacidades extendidas
- Nuevos endpoints de API para gestión de tareas y acciones del agente
- Modelos de datos extendidos para agentes, acciones y tareas
- Sistema de inicialización automática de base de datos
- Documentación mejorada en README.md

### Mejorado
- Script de ejecución original `build_and_run.sh` mantenido para compatibilidad
- Sistema de detección de intenciones del agente
- Gestión de contactos con diferentes niveles de interés
- Interfaz de usuario con mejoras en la visualización de datos
- Documentación completa del proyecto

### Cambiado
- Versión actualizada a 2.0.0 para reflejar los cambios significativos
- Estructura del proyecto actualizada en la documentación

## [1.0.0] - 2025-08-04

### Añadido
- Nueva estructura de componentes organizada por dominios funcionales
- Componentes especializados para cada funcionalidad:
  - Dashboard: Panel de control con KPIs y métricas
  - Contactos: Gestión completa de clientes y contactos
  - Chat: Sistema de conversación con el agente AI
  - Agente: Configuración y personalización del agente
- Composables para lógica reutilizable (useContacts, useChat, useAgent)
- Nuevas vistas completamente revisadas:
  - Dashboard.vue: Panel de control con estadísticas en tiempo real
  - Contacts.vue: Gestión de base de datos de clientes
  - Chat.vue: Sistema de chat mejorado con mejor UX
  - Agent.vue: Configuración avanzada del agente
- Sistema de gestión de contactos con importación/exportación
- Integración completa con base de datos SQLite
- Endpoint de estadísticas del agente funcional
- Sistema de conversaciones persistente en base de datos

### Corregido
- Problemas con la base de datos y la columna interest_level
- Endpoints de la API para creación y actualización de contactos
- Conversión de valores de interest_level entre strings y enums
- Manejo de errores en todas las operaciones
- Problemas con el servicio LLM y la persistencia de datos
- Estructura de componentes Vue (eliminación de múltiples elementos template)
- Conexión entre frontend y backend para datos reales
- Funcionalidad de chat con el agente AI

### Mejorado
- Arquitectura frontend con organización por dominios
- Interfaz de usuario con componentes reutilizables
- Sistema de estadísticas en tiempo real
- Gestión de contactos con paginación y búsqueda
- Visualización de métricas y KPIs del sistema
- Sistema de importación de contactos desde CSV/JSON
- Previsualización del agente en tiempo real
- Documentación del proyecto actualizada
- Estructura de navegación simplificada y enfocada

### Eliminado
- Componentes antiguos no utilizados
- Código redundante y duplicado
- Dependencias innecesarias

## [0.1.0] - 2025-07-30

### Añadido
- Versión inicial del proyecto
- Estructura básica del frontend y backend
- Integración con Qwen AI (DashScope)
- Sistema de chat básico
- Base de datos SQLite inicial
- API REST básica

[2.1.0]: https://github.com/usuario/scalie/releases/tag/v2.1.0
[2.0.0]: https://github.com/usuario/scalie/releases/tag/v2.0.0
[1.0.0]: https://github.com/usuario/scalie/releases/tag/v1.0.0