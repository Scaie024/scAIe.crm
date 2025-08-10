# Plan de análisis y documentación — versión 3.0.1

Este plan guía el análisis técnico y la documentación para publicar la versión funcional (frontend + admin + sandbox con RAG) expuesta vía ngrok.

## Objetivos
- Publicar una versión funcional accesible públicamente (ngrok) con: UI, administración de contactos, sandbox de agente y RAG.
- Consolidar documentación canónica y un proceso de release repetible.

## Alcance del análisis
- Backend (FastAPI)
  - Rutas: salud, CRUD de contactos, conversaciones, agente, sandbox, knowledge/RAG, webhooks.
  - Servido de SPA y assets estáticos (evitar colisiones con catch-all).
  - DB (SQLite) y logs.
- Frontend (Vue 3 + Vite)
  - Build de producción (dist/), rutas SPA, carga de assets (/assets/*).
- RAG
  - Embeddings, indexación/carga de conocimiento, endpoints de recuperación.
- Integraciones
  - Bot de Telegram (tokens, webhook/polling; pruebas básicas de envío/recepción).
- DevOps
  - Scripts de arranque/paro, túnel ngrok, logging y estructura de carpetas.

## Validaciones mínimas (smoke tests)
- GET /health → 200 OK.
- Assets SPA (p.ej., /assets/index.css, /assets/index.js) → 200 y content-type correcto.
- Admin de contactos: listar, crear, editar, eliminar, y estadísticas.
- Sandbox: flujo de conversación y ejecución de acciones mínimas.
- RAG: carga de conocimiento y recuperación básica con contexto.
- (Opcional) Telegram: comando simple que responda correctamente.

## Documentación a producir/actualizar
- README (raíz) como fuente única de verdad: instalación, ejecución, estructura, endpoints clave y troubleshooting.
- CHANGELOG.md (listo) con cambios notables por versión.
- RELEASE.md (listo) con checklist de publicación y post-release.
- Guías específicas (si aplican):
  - docs/sandbox.md → uso del sandbox y ajuste del agente.
  - docs/rag.md → cómo cargar fuentes y verificar recuperación.
  - docs/telegram.md → variables de entorno y prueba rápida.
  - docs/deployment/ngrok.md → exponer el frontend y API con ngrok.
- Unificar README duplicados dentro de scaie_crm/ para que apunten al README raíz.
- .gitignore endurecido para evitar venv/node_modules/dist/*.db/logs (listo).

## Checklist de publicación
1) Limpiar índice de git (eliminar venv/node_modules/dist/.db/logs del historial si estaban rastreados).
2) Asegurar que SPA sirve assets y rutas correctamente (hecho en 3.0.1).
3) Versionado y notas (README + CHANGELOG) y etiqueta semántica (vX.Y.Z).
4) Commit, tag y push a main + tags.
5) Crear GitHub Release con notas desde CHANGELOG.md.
6) Validar enlace público de ngrok y flujos clave.

## Estado actual (3.0.1)
- Fix de SPA/assets en backend: DONE.
- .gitignore endurecido: DONE.
- README raíz actualizado con nota de la corrección: DONE.
- CHANGELOG.md y RELEASE.md creados: DONE.
- Tag v3.0.1 y push a origin: DONE.

## Próximos pasos sugeridos
- Consolidar README duplicados bajo README del raíz (añadir enlace/nota en scaie_crm/README*).
- Añadir guías específicas (sandbox, RAG, Telegram) si se requieren para onboarding externo.
- (Opcional) .env.example con variables esperadas y comentarios.
- (Opcional) CI básico para pruebas rápidas (lint/build/backend health).

## Notas
- Mantener el repositorio limpio: no versionar venv, node_modules, dist, bases de datos ni logs.
- Para releases posteriores, seguir el checklist en RELEASE.md.
