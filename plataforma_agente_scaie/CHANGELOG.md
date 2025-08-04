# Registro de Cambios - SCAIE

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

[1.0.0]: https://github.com/usuario/scalie/releases/tag/v1.0.0