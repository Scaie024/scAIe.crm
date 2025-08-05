import os
import sys
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Añadir el directorio backend al path para resolver importaciones
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Importar modelos antes de crear las tablas
from app.models import contact, conversation
from app.core.database import engine, Base

# Create database tables
# Base.metadata.create_all(bind=engine)  # Commented out to avoid conflicts

app = FastAPI(title="SCAIE - Sistema Agente", 
              description="Plataforma conversacional de inteligencia artificial para ventas automatizadas",
              version="1.0.0")

# Configuración de rutas estáticas
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Incluir rutas de la API
from app.api.api import api_router
app.include_router(api_router, prefix="/api")

# Configuración de archivos estáticos
app.mount("/static", StaticFiles(directory=os.path.join(STATIC_DIR, "assets")), name="static")

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir archivos estáticos
@app.get("/assets/{file_path:path}")
async def serve_static(file_path: str):
    static_file = os.path.join(STATIC_DIR, "assets", file_path)
    if os.path.exists(static_file):
        return FileResponse(static_file)
    return {"detail": "Not Found"}, 404

# Ruta de salud
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Servir el archivo index.html para cualquier ruta no manejada
@app.get("/")
async def read_root():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

# Manejar rutas del frontend para SPA (Single Page Application)
@app.get("/{full_path:path}")
async def catch_all(full_path: str, request: Request):
    # Si la ruta comienza con api/ o static/, devolver 404
    if full_path.startswith(("api/", "static/", "assets/")):
        return {"detail": "Not Found"}, 404
    # Devolver el index.html para cualquier otra ruta
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

if __name__ == "__main__":
    # Asegurarse de que el directorio static exista
    os.makedirs(STATIC_DIR, exist_ok=True)
    
    # Iniciar el servidor
    uvicorn.run("app.main:app", 
               host="0.0.0.0", 
               port=8003,  # Changed to 8003
               reload=True,
               workers=1)