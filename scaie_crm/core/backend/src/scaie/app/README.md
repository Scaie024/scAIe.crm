# App (FastAPI application)

Código de la aplicación FastAPI del backend.

- `main.py` – Punto de entrada de la API (puerto 8003), monta routers y estáticos.
- `api/` – Endpoints agrupados por dominio (omnipotent_agent, contacts, chat, telegram_webhook, etc.).
- `core/` – Infra base (DB, configuración).
- `models/` – ORM SQLAlchemy.
- `schemas/` – Modelos Pydantic (validación/IO).
- `services/` – Lógica de negocio: LLM, agente y conocimiento.

Uso rápido:
```bash
cd backend/src/scaie
python app/main.py  # http://127.0.0.1:8003
```
