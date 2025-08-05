import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base, get_db
from app.services.omnipotent_agent import omnipotent_agent

# Configurar la base de datos de prueba
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear una base de datos de prueba
Base.metadata.create_all(bind=engine)

# Sobrescribir la dependencia de la base de datos
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_process_incoming_message():
    """Test processing an incoming message."""
    response = client.post("/api/omnipotent-agent/process-message", json={
        "message": "Hola, me interesa el workshop de IA",
        "platform": "web",
        "contact_info": {
            "name": "Juan Pérez",
            "phone": "+525512345678",
            "email": "juan.perez@example.com",
            "company": "Empresa de Prueba"
        }
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "contact_id" in data
    assert "message_id" in data

def test_search_contacts():
    """Test searching for contacts."""
    response = client.get("/api/omnipotent-agent/search-contacts?query=Juan")
    
    assert response.status_code == 200
    data = response.json()
    assert "results" in data

def test_contact_summary():
    """Test getting contact summary."""
    # Primero crear un contacto
    response = client.post("/api/omnipotent-agent/process-message", json={
        "message": "Hola, me interesa el workshop",
        "platform": "web",
        "contact_info": {
            "name": "María García",
            "phone": "+525587654321"
        }
    })
    
    assert response.status_code == 200
    data = response.json()
    contact_id = data["contact_id"]
    
    # Obtener el resumen del contacto
    response = client.get(f"/api/omnipotent-agent/contact/{contact_id}/summary")
    
    assert response.status_code == 200
    summary = response.json()
    assert "contact" in summary
    assert "conversations_count" in summary
    assert "tasks" in summary
    assert "recent_actions" in summary

def test_task_management():
    """Test creating, updating, and listing tasks."""
    # Crear un contacto primero
    response = client.post("/api/omnipotent-agent/process-message", json={
        "message": "Hola",
        "platform": "web",
        "contact_info": {
            "name": "Pedro López",
            "phone": "+525511223344"
        }
    })
    
    assert response.status_code == 200
    data = response.json()
    contact_id = data["contact_id"]
    
    # Crear una tarea
    response = client.post("/api/omnipotent-agent/tasks", json={
        "contact_id": contact_id,
        "title": "Seguimiento de interés en workshop",
        "description": "El cliente mostró interés en el workshop de IA",
        "priority": "high"
    })
    
    assert response.status_code == 200
    task_data = response.json()
    task_id = task_data["id"]
    assert task_data["title"] == "Seguimiento de interés en workshop"
    
    # Actualizar la tarea
    response = client.put(f"/api/omnipotent-agent/tasks/{task_id}", json={
        "status": "completed",
        "description": "El cliente asistió al workshop"
    })
    
    assert response.status_code == 200
    updated_task = response.json()
    assert updated_task["status"] == "completed"
    assert updated_task["description"] == "El cliente asistió al workshop"
    
    # Listar tareas
    response = client.get("/api/omnipotent-agent/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) > 0

if __name__ == "__main__":
    pytest.main([__file__])