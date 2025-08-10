# SCAIE – Sistema Agente Conversacional (guía corta y precisa)

Versión actual: 3.0.1 (2025-08-10)

Novedades clave:
- LLM activado por defecto (respuestas coherentes, sin fallback).
- Bot de Telegram integrado al mismo flujo del agente del backend.
- Normalización y deduplicación robusta en contactos (crear/actualizar/importar).
- Frontend SPA servido correctamente desde FastAPI (arreglo de rutas /assets).

## Requisitos
- Python 3.9+
- Node 16+ (solo si vas a reconstruir el frontend)

## Variables de entorno (.env en `scaie_crm/`)
Ejemplo mínimo:

DATABASE_URL=sqlite:///./scaie.db
DASHSCOPE_API_KEY=tu_api_key_de_dashscope
QWEN_MODEL=qwen-plus
TELEGRAM_BOT_TOKEN=tu_token_de_bot
SECRET_KEY=cambia_esta_clave

## Cómo ejecutar
- Sistema completo (web + bot):
	- cd scaie_crm
	- ./run_complete_system.sh

- Solo backend/web:
	- cd scaie_crm
	- ./run_scaie.sh

- Solo bot de Telegram:
	- cd scaie_crm
	- source venv/bin/activate
	- python scai_telegram_bot.py

Accesos rápidos:
- Web: http://localhost:8003
- API Docs: http://localhost:8003/docs
- Bot: https://t.me/scAIebot

## Estructura relevante
- backend/src/scaie/app/  FastAPI (API + estáticos)
- run_complete_system.sh  Inicia web + bot
- run_scaie.sh            Inicia solo web
- scai_telegram_bot.py    Bot de Telegram (polling)

Notas:
- Se eliminaron/centralizaron READMEs duplicados: este es el README canónico.
- Guía para desarrolladores: `scaie_crm/docs/development/DEVELOPMENT_GUIDE.md`.
- El bot usa polling (no se necesita webhook/ngrok).
- Si reconstruyes el frontend, asegúrate de que el build termine en `frontend/dist/`; el backend servirá los estáticos.