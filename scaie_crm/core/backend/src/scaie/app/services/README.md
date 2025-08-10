# Services

Servicios de dominio y utilidades de integración.

- `llm_service.py` – cliente OpenAI-compatible para Qwen/DashScope; expone `llm_service.generate_response(...)`.
- `omnipotent_agent.py` – orquesta contexto y decide respuesta; usa `llm_service`.
- `scaie_knowledge.py`, `workshop_knowledge.py` – bloques de conocimiento.

Tips:
- `DISABLE_LLM=true` para operar sin llamadas externas (respuestas mínimas/plantillas).
- Configuración de modelo por `QWEN_MODEL` en `.env`.
