# SCAIE – Guía de Desarrollo

Este documento reúne la información extensa para desarrollo (antes en varios README duplicados).

## Índice
- Entorno y requisitos
- Instalación y ejecución (dev)
- Estructura del proyecto
- API y endpoints
- Telegram bot
- Build del frontend
- Despliegue

## Entorno y requisitos
- Python 3.9+
- Node 16+ (solo si reconstruyes frontend)
- SQLite 3

## Instalación y ejecución (dev)
- Ver README canónico en la raíz para comandos rápidos.
- Backend: `cd scaie_crm && ./run_scaie.sh`
- Sistema completo: `cd scaie_crm && ./run_complete_system.sh`

## Estructura del proyecto
- backend/src/scaie/app: FastAPI, modelos, esquemas, servicios
- frontend: Vue 3 + Vite (build servido por backend)
- scripts de ejecución en `scaie_crm/`

## API
Principales endpoints:
- `GET /api/contacts/`
- `POST /api/contacts/`
- `POST /api/omnipotent-agent/process-message`
- `GET /api/omnipotent-agent/search-contacts`
- `GET /api/omnipotent-agent/contact/{id}/summary`

## Telegram bot
- Archivo: `scaie_crm/scai_telegram_bot.py`
- Usa polling y llama al backend para obtener respuestas del agente.

## Build del frontend
- `cd scaie_crm/frontend && npm install && npm run build`
- Asegúrate que genere `frontend/dist/` para que el backend sirva los estáticos.

## Despliegue
- Docker y compose disponibles en `scaie_crm/config/`
- Variables de entorno en `.env` en `scaie_crm/`.
