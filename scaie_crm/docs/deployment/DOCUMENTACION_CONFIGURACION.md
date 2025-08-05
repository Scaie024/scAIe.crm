# Documentación de Configuración - SCAIE

## Problemas Resueltos

### 1. Configuración de Rutas Estáticas

**Problema:** La aplicación cargaba una página en blanco porque los recursos estáticos (JS/CSS) no se cargaban correctamente.

**Solución implementada:**
- Se corrigió la configuración de Vite para generar rutas absolutas en los recursos estáticos.
- Se actualizó el archivo `index.html` para usar rutas relativas a los recursos.
- Se ajustó la configuración de FastAPI para servir correctamente los archivos estáticos.

### 2. Configuración de Vite para Producción

**Problema:** El proceso de construcción fallaba con errores relacionados con rutas de archivos.

**Solución implementada:**
- Se simplificó la configuración de Vite en `vite.config.js`.
- Se eliminaron configuraciones redundantes que causaban conflictos.
- Se aseguró que los archivos generados se guarden en la ubicación correcta (`backend/static/`).

## Configuración Actual

### Estructura de Archivos

```
plataforma_agente_scaie/
├── backend/
│   └── static/
│       ├── assets/
│       │   ├── index.[hash].css
│       │   └── index.[hash].js
│       └── index.html
└── frontend/
    ├── src/
    ├── public/
    ├── index.html
    └── vite.config.js
```

### Archivos de Configuración Clave

#### vite.config.js

```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000
  },
  base: '/',
  root: __dirname,
  publicDir: 'public',
  build: {
    outDir: resolve(__dirname, '../backend/static'),
    emptyOutDir: true,
    assetsDir: 'assets',
    rollupOptions: {
      output: {
        entryFileNames: 'assets/[name].[hash].js',
        chunkFileNames: 'assets/[name].[hash].js',
        assetFileNames: 'assets/[name].[hash][extname]'
      }
    }
  },
  resolve: {
    alias: {
      '@': resolve(__dirname, './src')
    }
  }
})
```

#### main.py (FastAPI)

```python
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directorio de archivos estáticos
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

# Montar directorios estáticos
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Ruta para archivos estáticos
@app.get("/assets/{file_path:path}")
async def serve_assets(file_path: str):
    return FileResponse(os.path.join(STATIC_DIR, "assets", file_path))

# Ruta para manejar SPA (Single Page Application)
@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    # Si la ruta comienza con api, static o assets, devolver 404
    if full_path.startswith(('api/', 'static/', 'assets/')):
        return {"detail": "Not Found"}, 404
    # Devolver el index.html para cualquier otra ruta
    return FileResponse(os.path.join(STATIC_DIR, "index"))

# Ruta de salud
@app.get("/health")
async def health_check():
    return {"status": "ok"}
```

## Comandos Útiles

### Desarrollo

```bash
# Iniciar servidor de desarrollo de frontend
cd frontend
npm run dev

# Iniciar servidor de backend (en otra terminal)
cd backend
uvicorn app.main:app --reload
```

### Producción

```bash
# Construir frontend para producción
cd frontend
npm run build

# Iniciar servidor de producción
cd ../backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Notas Adicionales

- Asegúrate de que el directorio `backend/static` exista antes de construir el frontend.
- El frontend se construye directamente en `backend/static` para simplificar el despliegue.
- La aplicación está configurada para funcionar como una SPA (Single Page Application).

## Solución de Problemas

### Página en blanco
- Verifica la consola del navegador para ver errores de carga de recursos.
- Asegúrate de que el backend esté sirviendo correctamente los archivos estáticos.

### Errores de construcción
- Si hay problemas con las rutas, verifica la configuración de `base` en `vite.config.js`.
- Asegúrate de que las rutas en `index.html` sean relativas (comiencen con `./` o sean absolutas desde la raíz).
