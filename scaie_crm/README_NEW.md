# SCAIE CRM - Sistema Agente Conversacional

> **🎯 Sistema CRM con Inteligencia Artificial para automatización de ventas**

SCAIE CRM es una plataforma completa que combina un CRM tradicional con un agente conversacional inteligente powered by AI, capaz de interactuar con clientes potenciales a través de múltiples canales.

## 🚀 Inicio Rápido

```bash
# Clonar e iniciar el sistema
cd scaie_crm
./start.sh
```

El sistema estará disponible en: **http://localhost:8003**

## 🏗️ Arquitectura

```
┌─────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│   Frontend      │    │   Backend API    │    │   Database       │
│   (Vue 3)       │◄──►│   (FastAPI)      │◄──►│   (SQLite)       │
└─────────────────┘    └──────────────────┘    └──────────────────┘
                                │
                                ▼
┌─────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│   Telegram Bot  │    │   AI Agent       │    │   Logs & Data    │
│                 │◄──►│   (Qwen LLM)     │◄──►│                  │
└─────────────────┘    └──────────────────┘    └──────────────────┘
```

## 📁 Estructura del Proyecto

```
scaie_crm/
├── 📁 core/                    # Core del sistema
│   ├── backend/               # API FastAPI + servicios
│   └── frontend/              # Interfaz Vue.js
├── 📁 integrations/           # Integraciones externas
│   └── telegram/              # Bot de Telegram
├── 📁 data/                   # Base de datos y logs
│   ├── scaie.db              # Base de datos principal
│   └── logs/                 # Archivos de log
├── 📁 scripts/               # Scripts de utilidad
├── 📁 tests/                 # Tests del sistema
├── 📁 docs/                  # Documentación
├── start.sh                  # Script principal de inicio
└── .env                      # Configuración
```

## ⚙️ Configuración (.env)

```ini
# Base de datos
DATABASE_URL=sqlite:///./data/scaie.db

# IA - DashScope/Qwen
DASHSCOPE_API_KEY=tu_api_key_aqui
QWEN_MODEL=qwen-plus

# Telegram
TELEGRAM_BOT_TOKEN=tu_token_aqui

# Seguridad
SECRET_KEY=tu_secret_key_aqui
```

## 🤖 Características Principales

### Agente Conversacional IA
- **LLM Qwen** para conversaciones naturales
- **Contexto persistente** de conversaciones
- **Acciones automáticas** (agendar, enviar materiales, etc.)

### Gestión CRM Completa
- **Gestión de contactos** con niveles de interés
- **Historial de conversaciones** completo
- **Dashboard** con métricas en tiempo real
- **Tareas automáticas** basadas en interacciones

### Integraciones Multi-canal
- **Telegram Bot** nativo
- **WhatsApp** (próximamente)
- **Web Chat** integrado
- **API REST** completa

## 📚 API Endpoints

### Agente Principal
- `POST /api/v1/omnipotent-agent/process-message` - Procesar mensaje
- `GET /api/v1/omnipotent-agent/contact/{id}/summary` - Resumen de contacto

### Gestión de Contactos
- `GET /api/v1/contacts` - Listar contactos
- `POST /api/v1/contacts` - Crear contacto
- `PUT /api/v1/contacts/{id}` - Actualizar contacto

### Documentación Completa
- **Swagger UI**: http://localhost:8003/docs
- **ReDoc**: http://localhost:8003/redoc

## 🧪 Tests

```bash
# Ejecutar todos los tests
cd tests
python -m pytest

# Test específico
python test_all_components.py
```

## 🛠️ Desarrollo

### Iniciar solo Backend
```bash
cd core/backend/src/scaie
python app/main.py
```

### Iniciar solo Frontend
```bash
cd core/frontend
npm run dev
```

### Iniciar Bot Telegram
```bash
cd integrations/telegram
python scai_telegram_bot.py
```

## 📖 Documentación Adicional

- [Documentación Técnica](docs/development/)
- [Guía de Deploy](docs/deployment/)
- [Funcionalidad del Agente](docs/AGENT_FUNCTIONALITY.md)

## 🤝 Soporte

Para reportar issues o solicitar features, crear un issue en el repositorio.

---

**⚡ scAIe CRM - Automatización inteligente para ventas**
