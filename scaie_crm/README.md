# SCAI# 🎯 SCAIE - Sistema Conversacional con Agente Inteligente Empresarial

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.0+-green.svg)](https://vuejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-red.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Sistema completo de automatización de ventas con agente conversacional especializado en el Workshop "Sé más eficiente con IA"**

## 📋 Descripción

**SCAIE** es un sistema completo de CRM con agente conversacional inteligente, diseñado específicamente para automatizar y optimizar la venta del workshop **"Sé más eficiente con IA"**. El sistema combina tecnologías de inteligencia artificial de última generación con una interfaz web moderna y un potente backend API.

### 🎯 Workshop "Sé más eficiente con IA"

El agente está especializado en promocionar y vender este workshop intensivo diseñado para equipos que buscan implementar IA en sus procesos:

- **🎯 Básico**: $1,499 MXN (2 horas, hasta 10 personas)
- **💼 Profesional**: $2,999 MXN (4 horas, hasta 20 personas) 
- **🏢 Empresarial**: Precio personalizado para grandes equipos

### 🤖 Características Principales

- **Agente Conversacional Inteligente**: Powered by Qwen (Alibaba Cloud)
- **CRM Completo**: Gestión avanzada de contactos y leads
- **Dashboard Analytics**: Métricas de ventas en tiempo real
- **Chat de Pruebas**: Interfaz para interactuar con el agente
- **Multi-canal**: Soporte para WhatsApp, Telegram, Facebook y Web
- **API REST Completa**: Documentación automática con Swagger/OpenAPI

## 🚀 Inicio Rápido

### Opción 1: Ejecución Automática (Recomendada)

```bash
# 1. Clona el repositorio
git clone <repository-url>
cd scaie_crm

# 2. Ejecuta el script de inicio completo
./run_complete.sh
```

### Opción 2: Configuración Manual

```bash
# 1. Configurar Python
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt

# 2. Configurar Node.js
cd frontend
npm install
npm run build
cd ..

# 3. Configurar variables de entorno
cp backend/.env.example backend/.env
# Editar backend/.env con tu configuración

# 4. Ejecutar aplicación
cd backend/src/scaie
python3 -m app.main
```

## 📱 Acceso a la Aplicación

Una vez iniciado el sistema:

- **🌐 Aplicación Web**: http://localhost:8003
- **📚 API Documentación**: http://localhost:8003/docs
- **❤️ Health Check**: http://localhost:8003/health

### 🧭 Navegación en la Aplicación

1. **📊 Dashboard**: Métricas y KPIs de ventas
2. **💬 Chat**: Interacción directa con el agente IA
3. **👥 Base de Datos**: Gestión completa de contactos
4. **🤖 Agente**: Configuración del comportamiento del bot
5. **🧪 Sandbox**: Pruebas y experimentación

## 🛠️ Tecnologías

### Backend
- **FastAPI**: Framework web moderno para Python
- **SQLAlchemy**: ORM para base de datos
- **SQLite**: Base de datos ligera
- **Pydantic**: Validación de datos
- **Qwen API**: Modelo de lenguaje de Alibaba Cloud

### Frontend
- **Vue.js 3**: Framework progresivo de JavaScript
- **Vite**: Build tool rápido
- **TailwindCSS**: Framework de utilidades CSS
- **Vue Router**: Enrutamiento SPA

### Inteligencia Artificial
- **DashScope API**: Plataforma de IA de Alibaba Cloud
- **Qwen Models**: Modelos de lenguaje multimodal

## ⚙️ Configuración

### Variables de Entorno Principales

```bash
# API de IA (Obligatorio)
DASHSCOPE_API_KEY=your_api_key_here

# Base de Datos
DATABASE_URL=sqlite:///./scaie.db

# Configuración del Agente
AGENT_NAME=SCAI
QWEN_MODEL=qwen-plus
TEMPERATURE=0.8

# Workshop
WORKSHOP_CONTACT_PHONE=5535913417
WORKSHOP_CONTACT_EMAIL=info@scaie.com.mx
```

### 🔑 Obtener API Key de DashScope

1. Visita [DashScope Console](https://dashscope.aliyuncs.com/)
2. Crea una cuenta gratuita
3. Genera tu API key
4. Actualiza `DASHSCOPE_API_KEY` en `.env`

## 📊 Estructura del Proyecto

```
scaie_crm/
├── 📁 backend/                 # Servidor FastAPI
│   ├── 📁 src/scaie/          # Código fuente principal
│   │   ├── 📁 app/           # Aplicación FastAPI
│   │   │   ├── main.py       # Punto de entrada
│   │   │   ├── 📁 api/       # Endpoints REST
│   │   │   ├── 📁 models/    # Modelos SQLAlchemy
│   │   │   ├── 📁 schemas/   # Schemas Pydantic
│   │   │   └── 📁 services/  # Lógica de negocio
│   │   └── 📁 scripts/       # Scripts de utilidad
│   ├── requirements.txt       # Dependencias Python
│   └── .env                  # Variables de entorno
├── 📁 frontend/               # Aplicación Vue.js
│   ├── 📁 src/               # Código fuente
│   │   ├── 📁 components/    # Componentes Vue
│   │   ├── 📁 pages/        # Páginas principales
│   │   ├── 📁 services/     # Servicios API
│   │   └── 📁 utils/        # Composables Vue
│   ├── package.json          # Dependencias Node.js
│   └── vite.config.js        # Configuración Vite
├── 📁 scripts/               # Scripts de automatización
├── 📁 docs/                  # Documentación
└── run_complete.sh           # Script de inicio
```

## 🎯 Funcionalidades del Agente

### Personalidad y Comportamiento
- **Tono**: Amigable, empático, profesional
- **Estilo**: Coloquial pero respetuoso
- **Objetivo**: Convertir leads en ventas del workshop

### Capacidades Principales
- ✅ Respuesta a consultas sobre el workshop
- ✅ Calificación automática de leads
- ✅ Gestión de niveles de interés (1-5)
- ✅ Actualización automática de base de datos
- ✅ Generación de reportes de conversaciones
- ✅ Integración multi-canal

### Tipos de Conversación
1. **Consultas Generales**: Información sobre el workshop
2. **Interés en Contratación**: Procesamiento de leads calificados
3. **Objeciones**: Manejo de dudas y preocupaciones
4. **Seguimiento**: Nurturing de prospectos

## 📈 Dashboard y Analytics

### Métricas Principales
- **Contactos Totales**: Contador de leads
- **Nivel de Interés Promedio**: KPI de calidad
- **Conversiones**: Tasa de cierre
- **Actividad Reciente**: Timeline de interacciones

### Filtros y Búsqueda
- Búsqueda por nombre, email, teléfono
- Filtros por nivel de interés
- Ordenamiento por fecha de creación
- Exportación de datos

## 🔧 API Endpoints

### Contactos
```http
GET    /api/contacts/          # Listar contactos
POST   /api/contacts/          # Crear contacto
GET    /api/contacts/{id}      # Obtener contacto
PUT    /api/contacts/{id}      # Actualizar contacto
DELETE /api/contacts/{id}      # Eliminar contacto
```

### Chat
```http
POST   /api/chat/message       # Enviar mensaje al agente
GET    /api/chat/history/{contact_id}  # Historial de chat
```

### Estadísticas
```http
GET    /api/stats/overview     # Estadísticas generales
GET    /api/stats/contacts     # Métricas de contactos
```

### Agente
```http
GET    /api/agent/config       # Configuración del agente
PUT    /api/agent/config       # Actualizar configuración
POST   /api/agent/test         # Probar respuesta del agente
```

## 🧪 Testing y Desarrollo

### Ejecutar Tests
```bash
# Tests del backend
cd backend
python -m pytest tests/

# Tests del frontend
cd frontend
npm run test
```

### Modo Desarrollo
```bash
# Backend con recarga automática
cd backend/src/scaie
uvicorn app.main:app --reload --port 8003

# Frontend con recarga automática
cd frontend
npm run dev
```

## 🚀 Despliegue

### Usando Docker
```bash
# Construir imagen
docker build -t scaie:latest .

# Ejecutar contenedor
docker run -p 8003:8003 --env-file .env scaie:latest
```

### Usando Docker Compose
```bash
# Producción
docker-compose -f config/docker-compose.prod.yml up -d
```

## 🤝 Integraciones

### WhatsApp Business API
```bash
# Variables de entorno necesarias
WHATSAPP_PHONE_NUMBER_ID=your_phone_id
WHATSAPP_ACCESS_TOKEN=your_access_token
```

### Telegram Bot
```bash
# Variable de entorno necesaria
TELEGRAM_BOT_TOKEN=your_bot_token
```

### Facebook Messenger
```bash
# Variable de entorno necesaria
FACEBOOK_PAGE_ACCESS_TOKEN=your_page_token
```

## 🛠️ Troubleshooting

### Problemas Comunes

**Error: Puerto 8003 en uso**
```bash
# Matar procesos en el puerto
lsof -ti:8003 | xargs kill -9
```

**Error: API Key no válida**
```bash
# Verificar configuración
grep DASHSCOPE_API_KEY backend/.env
```

**Error: Base de datos**
```bash
# Recrear base de datos
rm backend/scaie.db
cd backend/src/scaie
python -c "from app.models import create_tables; create_tables()"
```

**Error: Dependencias faltantes**
```bash
# Reinstalar backend
pip install -r backend/requirements.txt

# Reinstalar frontend
cd frontend && npm install
```

### Logs y Debugging

```bash
# Ver logs del servidor
tail -f backend/server.log

# Debug mode
export DEBUG=true
python -m app.main
```

## 📞 Soporte y Contacto

- **📧 Email**: info@scaie.com.mx
- **📱 Teléfono**: 55 3591 3417
- **🌐 Website**: https://scaie.com.mx

## 📄 Licencia

Este proyecto está licenciado bajo la [Licencia MIT](LICENSE).

---

<div align="center">

**🤖 Desarrollado con IA para optimizar ventas con IA 🤖**

*SCAIE - Donde la inteligencia artificial impulsa tu crecimiento empresarial*

</div> - Sistema Agente Conversacional para Ventas con IA

<p align="center">
  <img src="docs/assets/scaie-logo.png" alt="SCAIE Logo" width="200"/>
</p>

SCAIE (Sistema Conversacional con Agente Inteligente Empresarial) es una plataforma avanzada de agentes conversacionales basada en inteligencia artificial que ayuda a las empresas a automatizar ventas, mejorar la atención al cliente y optimizar procesos mediante la automatización inteligente.

## Características Principales

### 🤖 Agente Conversacional Inteligente Especializado en Ventas de Workshops

El agente de SCAIE está especialmente entrenado para vender el workshop **"Sé más eficiente con IA"**, una solución práctica para que los equipos aprendan a usar inteligencia artificial en sus procesos diarios.

**Capacidades del Agente:**
- **Ventas Consultivas**: Técnicas avanzadas de descubrimiento, manejo de objeciones y cierre
- **Personalización**: Adaptación de mensajes según el perfil del cliente
- **Contexto**: Mantenimiento de conversaciones coherentes a través de múltiples interacciones
- **Multi-Canal**: Funciona en WhatsApp, Facebook Messenger, Web Chat y Telegram

### 📊 Panel de Administración Completo

- Dashboard con KPIs de ventas y métricas de agentes
- Gestión de contactos con niveles de interés (Nuevo, Contactado, Interesado, Confirmado, No Interesado)
- Visualización de conversaciones en tiempo real
- Gestión de tareas y seguimiento de leads
- Importación/Exportación de datos (CSV, JSON)

### 🔧 Tecnología de Vanguardia

- Backend en Python/FastAPI con SQLite
- Frontend en Vue 3 con Vite y TailwindCSS
- Integración con Qwen (Aliyun Dashscope) para procesamiento de lenguaje natural
- Arquitectura modular y escalable

## Workshop "Sé más eficiente con IA"

### ¿De qué trata?

Un workshop intensivo diseñado para equipos que quieren empezar a usar inteligencia artificial en su trabajo diario. A través de ejercicios prácticos, casos reales y herramientas específicas, los participantes aprenden a automatizar tareas, analizar información y generar contenido con IA, sin necesidad de conocimientos técnicos previos.

### Resultados Esperados

- Al menos 3 herramientas de IA activas y funcionando
- Un proceso de trabajo automatizado
- Plantillas y prompts personalizados para el equipo
- Plan de implementación de IA en la organización

### Modalidades

- **Básico** ($1,499 MXN): 2 horas, online en vivo, hasta 10 personas
- **Profesional** ($2,999 MXN): 4 horas, online o presencial, hasta 20 personas
- **Empresarial** (Precio personalizado): Implementación completa con múltiples sesiones

## Requisitos del Sistema

- Python 3.8+
- Node.js 14+
- npm 6+
- SQLite (incluido) o MySQL

## Instalación y Configuración

### Método 1: Ejecución Directa (Recomendado para desarrollo)

1. Clonar el repositorio:
```bash
git clone https://github.com/Scaie024/scAIe.crm.git
cd scAIe.crm
```

2. Ejecutar el script de configuración:
```bash
chmod +x setup.sh
./setup.sh
```

3. Configurar las variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus credenciales de API
```

4. Ejecutar la aplicación:
```bash
chmod +x run_app.sh
./run_app.sh
```

### Método 2: Ejecución Completa (Recomendado para producción)

```bash
chmod +x run_complete.sh
./run_complete.sh
```

Este script realiza todas las tareas necesarias:
- Configuración del entorno virtual
- Instalación de dependencias backend y frontend
- Construcción del frontend
- Inicio del servidor backend en el puerto 8003

### Manual Setup

If you prefer to set up the system manually:

1. **Clone or download the repository**
   ```bash
   git clone https://github.com/Scaie024/scAIe.crm.git
   ```

2. **Navigate to the project directory**
   ```bash
   cd scaie_crm
   ```

3. **Set up Python virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install backend dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   cd ..
   ```

5. **Install frontend dependencies**
   ```bash
   cd frontend
   npm install
   npm run build
   cd ..
   ```

6. **Configure environment variables**
   Create a `.env` file in the `backend` directory with your configuration:
   ```env
   # Database Configuration
   DATABASE_URL=sqlite:///./scaie.db

   # Security Configuration
   SECRET_KEY=your_secret_key_here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30

   # DashScope API Configuration (Qwen)
   # Get your key at: https://dashscope.aliyuncs.com/
   DASHSCOPE_API_KEY=your_dashscope_api_key_here

   # Qwen Model Configuration
   QWEN_MODEL=qwen-plus
   ```

7. **Run the application**
   ```bash
   cd backend/src/scaie
   python3 -m app.main
   ```

## Uso

Una vez iniciado el servidor:

1. Accede a la interfaz web: http://localhost:8003
2. Usa la sección de chat para probar el agente
3. Explora el dashboard para ver métricas y contactos
4. Configura integraciones con WhatsApp/Facebook según necesites

## Endpoints de la API

- Documentación de la API: http://localhost:8003/docs
- Health check: http://localhost:8003/health
- Chat endpoint: http://localhost:8003/api/chat/
- Endpoint del agente omnipotente: http://localhost:8003/api/omnipotent-agent/

## Arquitectura del Sistema

```
scaie_crm/
├── backend/
│   ├── src/scaie/
│   │   ├── app/
│   │   │   ├── api/          # Endpoints de la API
│   │   │   ├── core/         # Configuración del núcleo
│   │   │   ├── models/       # Modelos de datos
│   │   │   ├── schemas/      # Esquemas de Pydantic
│   │   │   ├── services/     # Servicios de negocio
│   │   │   └── main.py       # Punto de entrada de la aplicación
│   │   └── static/           # Archivos estáticos (frontend compilado)
│   └── requirements.txt      # Dependencias de Python
├── frontend/
│   ├── src/
│   │   ├── assets/           # Recursos estáticos
│   │   ├── components/       # Componentes de Vue
│   │   ├── layouts/          # Diseños de página
│   │   ├── pages/            # Páginas de la aplicación
│   │   ├── router/           # Configuración de rutas
│   │   ├── services/         # Servicios de API
│   │   ├── stores/           # Stores de Pinia
│   │   └── utils/            # Utilidades
│   └── package.json          # Dependencias de Node.js
├── docs/                     # Documentación
├── scripts/                  # Scripts de utilidad
├── setup.sh                  # Script de configuración
├── run_app.sh                # Script de ejecución
└── run_complete.sh           # Script de ejecución completa
```

## Agentes y Funcionalidades

### Agente Especializado en Ventas del Workshop

El agente está entrenado específicamente para:
1. **Descubrir Necesidades**: Hacer preguntas abiertas para entender los desafíos del cliente
2. **Posicionar Valor**: Conectar los problemas del cliente con soluciones de IA
3. **Manejar Objeciones**: Responder con empatía a preocupaciones comunes
4. **Cerrar Ventas**: Guiar al cliente hacia agendar una sesión o solicitar información

### Integraciones

- WhatsApp Business API
- Facebook Messenger
- Telegram Bot
- Web Chat

## Desarrollo

### Estructura del Backend

El backend está construido con FastAPI y sigue una arquitectura limpia:
- **API Endpoints**: Rutas REST bien definidas
- **Modelos**: SQLAlchemy ORM para interacción con la base de datos
- **Servicios**: Lógica de negocio encapsulada
- **Esquemas**: Validación de datos con Pydantic

### Estructura del Frontend

El frontend utiliza Vue 3 con Composition API:
- **Componentes Reutilizables**: Diseño modular
- **Estado Global**: Gestión con Pinia
- **Enrutamiento**: Vue Router para navegación
- **Estilos**: TailwindCSS para diseño responsivo

## 🔧 Configuration

### Environment Variables

The system requires several environment variables to be set in the `backend/.env` file:

- `DASHSCOPE_API_KEY`: Your DashScope API key for Qwen access
- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: Secret key for JWT token generation
- `QWEN_MODEL`: The Qwen model to use (default: qwen-plus)

### Agent Configuration

The agent can be configured with:
- `AGENT_NAME`: The name of the agent
- `AGENT_PERSONALITY`: Personality traits of the agent
- `AGENT_TONE`: Communication tone
- `AGENT_GOAL`: Primary goal of the agent

## Contribución

1. Haz un fork del repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Realiza tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Haz push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## Contacto

Para más información, visita [www.scaie.com.mx](https://www.scaie.com.mx) o contacta con el equipo de desarrollo.

## Estado del Proyecto

Versión actual: v1.0.0 - Producción

El sistema está listo para ser usado en entornos de producción con todas las funcionalidades implementadas y probadas.

## 📞 Support

For support, please open an issue on the GitHub repository or contact the development team.