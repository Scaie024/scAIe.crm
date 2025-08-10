import os
import sys
import logging
from dotenv import load_dotenv

# Load environment variables from .env file (no secret printing)
env_path = os.path.join(os.path.dirname(__file__), "../../../../.env")
if os.path.exists(env_path):
    load_dotenv(env_path)

from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add backend directory to path for imports
backend_path = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, backend_path)

# Import models before creating tables
from app.models import contact, conversation, agent_action
from app.core.database import engine, Base

# Create database tables
# Base.metadata.create_all(bind=engine)  # Commented out to avoid conflicts

app = FastAPI(title="SCAIE - Sistema Agente", 
              description="Sistema de gestión de clientes con inteligencia artificial",
              version="1.1.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
from app.api.api import api_router
# Primary versioned API
app.include_router(api_router, prefix="/api/v1")
# Backward-compatible unversioned prefix to support older clients/bots
app.include_router(api_router, prefix="/api")

# Serve frontend static files (within the backend package)
# __file__ -> .../backend/src/scaie/app/main.py
# static lives at .../backend/src/scaie/static
static_dir = os.path.join(os.path.dirname(__file__), "../static")
if os.path.exists(static_dir):
    # Mount assets folder specifically for CSS/JS files
    assets_dir = os.path.join(static_dir, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")
        print(f"Serving assets from {os.path.abspath(assets_dir)}")
    
    # Mount main static directory for other files
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    print(f"Serving static files from {os.path.abspath(static_dir)}")
else:
    msg = f"Static directory not found: {os.path.abspath(static_dir)}"
    print(msg)
    # Raise an exception to stop the server if static directory is not found
    raise Exception(msg)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Servir el archivo index.html para cualquier ruta no manejada
@app.get("/", response_class=HTMLResponse)
async def read_root():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return HTMLResponse(content="<h1>SCAIE CRM</h1><p>Frontend files not found</p>")

# Manejar rutas del frontend para SPA (Single Page Application)
@app.get("/{full_path:path}")
async def catch_all(full_path: str, request: Request):
    # Si la ruta comienza con api/, static/, o assets/, devolver 404
    if full_path.startswith(("api/", "static/", "assets/")):
        raise HTTPException(status_code=404, detail="Not Found")
    # Devolver el index.html para cualquier otra ruta
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return HTMLResponse(content="<h1>SCAIE CRM</h1><p>Frontend files not found</p>")

if __name__ == "__main__":
    # Log startup information
    logger.info("Starting the server...")
    logger.info(f"Static directory: {static_dir}")
    
    # Iniciar el servidor
    # Use port 8000 to match production script and ngrok configuration
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
