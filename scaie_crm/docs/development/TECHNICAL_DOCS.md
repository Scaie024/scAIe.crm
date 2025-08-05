# Documentación Técnica de SCAIE

## Índice
1. [Arquitectura General](#arquitectura-general)
2. [Componentes del Sistema](#componentes-del-sistema)
3. [Modelos de Datos](#modelos-de-datos)
4. [API Endpoints](#api-endpoints)
5. [Servicios](#servicios)
6. [Flujos de Trabajo](#flujos-de-trabajo)
7. [Agente Todopoderoso](#agente-todopoderoso)
8. [Integración con IA](#integración-con-ia)
9. [Base de Datos](#base-de-datos)
10. [Scripts del Sistema](#scripts-del-sistema)

## Arquitectura General

SCAIE sigue una arquitectura cliente-servidor moderna con los siguientes componentes principales:

### Backend (FastAPI)
- Framework: FastAPI
- Base de datos: SQLite con SQLAlchemy ORM
- Autenticación: JWT (en desarrollo)
- Integración IA: DashScope (Qwen API)

### Frontend (Vue.js 3)
- Framework: Vue 3 con Composition API
- Bundler: Vite
- Estilos: TailwindCSS
- Estado: Composables de Vue

### Comunicación
- API RESTful entre frontend y backend
- WebSocket (futuro) para actualizaciones en tiempo real
- Integración con servicios externos (Qwen API)

## Componentes del Sistema

### 1. Dashboard
Panel de control con métricas en tiempo real:
- Estadísticas de contactos
- Distribución de niveles de interés
- Actividad reciente

### 2. Gestión de Contactos
Sistema completo para administrar clientes:
- CRUD de contactos
- Importación/exportación de datos
- Búsqueda y filtrado
- Niveles de interés (nuevo, contactado, interesado, confirmado, no_interesado)

### 3. Sistema de Conversaciones
Gestión de interacciones con clientes:
- Historial de conversaciones
- Mensajes entrantes y salientes
- Contexto de conversación persistente

### 4. Agente Conversacional
Motor de inteligencia artificial:
- Integración con Qwen AI
- Personalidad definida
- Detección de intenciones
- Generación de respuestas contextuales

### 5. Agente Todopoderoso
Versión avanzada del agente con capacidades extendidas:
- Acceso completo al sistema
- Ejecución automática de acciones
- Gestión de tareas
- Integración multicanal

## Modelos de Datos

### Contacto
```python
class Contact(Base):
    id: int
    name: str
    phone: str
    email: Optional[str]
    company: Optional[str]
    notes: Optional[str]
    interest_level: InterestLevel
    created_at: datetime
    updated_at: datetime
```

### Conversación
```python
class Conversation(Base):
    id: int
    contact_id: int
    platform: str
    created_at: datetime
    messages: List[Message]
```

### Mensaje
```python
class Message(Base):
    id: int
    conversation_id: int
    sender: str  # "user" or "agent"
    content: str
    created_at: datetime
```

### Acción del Agente
```python
class AgentAction(Base):
    id: int
    conversation_id: int
    action_type: str
    parameters: Dict
    result: Optional[str]
    status: str  # "pending" or "completed"
    created_at: datetime
    executed_at: Optional[datetime]
```

### Tarea del Agente
```python
class AgentTask(Base):
    id: int
    contact_id: int
    title: str
    description: Optional[str]
    status: str  # "pending", "in_progress", "completed"
    priority: str  # "low", "medium", "high"
    due_date: Optional[datetime]
    created_at: datetime
    completed_at: Optional[datetime]
```

## API Endpoints

### Contactos
- `GET /api/contacts/` - Listar contactos
- `POST /api/contacts/` - Crear contacto
- `GET /api/contacts/{id}` - Obtener contacto
- `PUT /api/contacts/{id}` - Actualizar contacto
- `DELETE /api/contacts/{id}` - Eliminar contacto
- `POST /api/contacts/import` - Importar contactos
- `GET /api/contacts/export` - Exportar contactos

### Conversaciones
- `GET /api/conversations/` - Listar conversaciones
- `POST /api/conversations/` - Crear conversación
- `GET /api/conversations/{id}` - Obtener conversación

### Chat
- `POST /api/chat/` - Interactuar con el agente
- `POST /api/chat/sandbox` - Modo sandbox para pruebas

### Agente
- `GET /api/agent/stats` - Estadísticas del agente

### Agente Todopoderoso
- `POST /api/omnipotent-agent/process-message` - Procesar mensaje
- `POST /api/omnipotent-agent/execute-pending-actions/{conversation_id}` - Ejecutar acciones pendientes
- `GET /api/omnipotent-agent/contact/{contact_id}/summary` - Resumen de contacto
- `GET /api/omnipotent-agent/search-contacts` - Buscar contactos
- `POST /api/omnipotent-agent/tasks` - Crear tarea
- `PUT /api/omnipotent-agent/tasks/{task_id}` - Actualizar tarea
- `DELETE /api/omnipotent-agent/tasks/{task_id}` - Eliminar tarea
- `GET /api/omnipotent-agent/tasks` - Listar tareas

## Servicios

### Servicio LLM (llm_service.py)
Gestiona la comunicación con la API de Qwen:
- Generación de respuestas contextuales
- Procesamiento de mensajes del sandbox
- Manejo de errores de la API

### Servicio de Contactos (contact_service.py)
Lógica de negocio para gestión de contactos:
- CRUD de contactos
- Búsqueda y filtrado
- Importación/exportación

### Servicio de Conocimiento SCAIE (scaie_knowledge.py)
Gestiona la base de conocimiento del dominio:
- Información sobre SCAIE y sus servicios
- Workshop "Sé más eficiente con IA"
- Metodología OPT

### Servicio del Agente Todopoderoso (omnipotent_agent.py)
Motor principal del agente avanzado:
- Procesamiento de mensajes entrantes
- Detección de intenciones
- Ejecución de acciones
- Gestión de tareas

## Flujos de Trabajo

### 1. Procesamiento de Mensajes Entrantes
1. Mensaje recibido por cualquier canal
2. Agente todopoderoso procesa el mensaje
3. Se identifica la intención del cliente
4. Se generan acciones apropiadas
5. Se ejecutan acciones inmediatas
6. Se programan acciones pendientes
7. Se genera respuesta para el cliente

### 2. Creación de Contactos
1. Nuevo mensaje de cliente desconocido
2. Extracción de información del contacto
3. Creación de nuevo registro de contacto
4. Asignación de nivel de interés inicial
5. Creación de conversación asociada

### 3. Gestión de Tareas
1. Acción identificada durante procesamiento de mensaje
2. Creación de tarea asociada al contacto
3. Asignación de prioridad y fecha límite
4. Seguimiento de estado de la tarea
5. Actualización automática según acciones del cliente

## Agente Todopoderoso

### Características Clave
1. **Acceso Completo**: Puede realizar cualquier operación en el sistema
2. **Inteligencia Avanzada**: Entiende el contexto completo de cada interacción
3. **Multicanal**: Funciona con WhatsApp, web, Facebook y otros canales
4. **Automatización Total**: Detecta automáticamente qué acciones tomar

### Tipos de Acciones
1. **SEND_MATERIAL**: Enviar materiales (folletos, presentaciones)
2. **SCHEDULE_APPOINTMENT**: Agendar citas para workshops
3. **GENERATE_QUOTE**: Generar cotizaciones personalizadas
4. **UPDATE_INTEREST_LEVEL**: Actualizar nivel de interés del contacto
5. **ESCALATE_TO_HUMAN**: Escalar conversación a agente humano
6. **CREATE_TASK**: Crear tareas de seguimiento

### Detección de Intenciones
El agente puede identificar automáticamente:
- Solicitudes de información sobre servicios
- Interés en el workshop "Sé más eficiente con IA"
- Preguntas sobre precios y planes
- Solicitudes para agendar citas
- Peticiones para hablar con un humano

## Integración con IA

### Qwen API (DashScope)
- Modelo: qwen-plus para respuestas equilibradas
- Contexto: Historial de conversación completo
- Personalidad: Profesional, directa, sin emojis
- Parámetros optimizados para ventas B2B

### Procesamiento de Lenguaje Natural
1. Análisis de sentimiento
2. Extracción de entidades
3. Detección de intenciones
4. Generación de respuestas contextuales

## Base de Datos

### Esquema
La base de datos SQLite contiene las siguientes tablas:
1. `contacts` - Información de contactos
2. `conversations` - Registros de conversaciones
3. `messages` - Mensajes individuales
4. `agent_actions` - Acciones del agente
5. `agent_tasks` - Tareas del agente

### Relaciones
- Contacto 1:N Conversaciones
- Conversación 1:N Mensajes
- Conversación 1:N Acciones del Agente
- Contacto 1:N Tareas del Agente

## Scripts del Sistema

### run_scaie.sh
Script principal de ejecución:
- Verifica variables de entorno
- Inicializa base de datos si es necesario
- Construye frontend
- Inicia servidor backend

### init_project.sh
Script de inicialización completa:
- Crea estructura de directorios
- Genera archivo .env de ejemplo
- Instala dependencias
- Inicializa base de datos

### build_and_run.sh
Script de ejecución original (mantenido para compatibilidad)

### init_db.py
Script de inicialización de base de datos:
- Crea tablas si no existen
- Verifica integridad del esquema