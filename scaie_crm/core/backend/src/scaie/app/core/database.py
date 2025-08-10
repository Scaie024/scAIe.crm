import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Cargar variables de entorno desde la raíz del proyecto
env_path = os.path.join(os.path.dirname(__file__), '../../../../../.env')
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    load_dotenv()

# Configuración de la base de datos
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./scaie.db")

# Normalizar ruta SQLite relativa a un path absoluto estable (backend/src/scaie)
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    try:
        # Extraer la parte del path después de 'sqlite://'
        prefix = "sqlite:///"
        if SQLALCHEMY_DATABASE_URL.startswith("sqlite:////"):
            # Ya es absoluta, no modificar
            pass
        elif SQLALCHEMY_DATABASE_URL.startswith(prefix):
            rel_path = SQLALCHEMY_DATABASE_URL[len(prefix):]
            # Si el path no es absoluto, convertirlo respecto al directorio raíz del proyecto
            if not os.path.isabs(rel_path):
                # Subir desde core/backend/src/scaie/app/core hasta la raíz del proyecto scaie_crm
                base_dir = Path(__file__).resolve().parents[6]  # .../scaie_crm
                abs_path = (base_dir / rel_path).resolve()
                # Asegurar que el path sea correcto incluso con espacios en el path
                SQLALCHEMY_DATABASE_URL = f"sqlite:///{abs_path.as_posix()}"
    except Exception as e:
        # En caso de cualquier error, mantener la URL original y registrar el error
        print(f"Error al procesar la URL de la base de datos: {str(e)}")
        pass

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {},
    echo=False  # Cambiar a True para ver las consultas SQL en la consola
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependency to get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize the database, creating all tables."""
    # Importar todos los modelos aquí para que se creen en la base de datos
    from ..models.contact import Contact
    from ..models.conversation import Conversation, Message
    from ..models.agent_action import AgentAction, AgentTask
    from .. import models  # Import relationships
    
    Base.metadata.create_all(bind=engine)