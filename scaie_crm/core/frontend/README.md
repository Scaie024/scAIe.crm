# Frontend (Vue 3 + Vite)

Interfaz web del sistema SCAIE CRM. Desarrollada en Vue 3 con Vite.

## Estructura clave

```
frontend/
  package.json
  src/
    main.js
    App.vue
    pages/            # Vistas principales
    components/       # Componentes reutilizables
    router/           # Vue Router
    services/         # Clientes API
    utils/
```

## Desarrollo

```bash
cd scaie_crm/frontend
npm install
npm run dev
```

Dev server: `http://127.0.0.1:5173`

## Pruebas

```bash
npx vitest run
```

## Integración con backend

- API base esperada: `http://127.0.0.1:8003`
- Endpoints usados: `/api/v1/...` (chat, contactos, omnipotent-agent)
