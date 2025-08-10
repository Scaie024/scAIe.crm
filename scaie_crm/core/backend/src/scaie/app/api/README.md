# API (Routers)

Routers de FastAPI agrupados por dominio.

- `omnipotent_agent.py` – núcleo de interacción con el agente/LLM (process-message, tasks, contacts).
- `telegram_webhook.py` – compatibilidad webhook para Telegram (opcional si no usas polling).
- `chat.py`, `contacts.py`, `conversations.py`, `dashboard.py`, `auth.py`, `messaging.py`, `debug.py` – endpoints auxiliares.

Import central: `app/api/api.py` (incluye todos los routers). Se monta en `/api/v1` y `/api`.
