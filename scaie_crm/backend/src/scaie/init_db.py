#!/usr/bin/env python3
"""
Script para inicializar la base de datos de SCAIE.
"""

import os
import sys
from sqlalchemy import create_engine, inspect, MetaData, Table
from sqlalchemy.orm import sessionmaker

# Añadir el directorio backend al path para poder importar los módulos
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from app.core.database import Base, engine
from app.models import contact, conversation, agent_action

def init_db():
    """Inicializa la base de datos creando todas las tablas."""
    print("Creando tablas en la base de datos...")
    try:
        Base.metadata.create_all(bind=engine)
        print("Todas las tablas creadas exitosamente.")
    except Exception as e:
        print(f"Error al crear las tablas: {e}")
        sys.exit(1)

def check_and_update_tables():
    """Verifica si las tablas existen y crea las que falten o actualiza las existentes."""
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()

    required_tables = [
        'contacts',
        'conversations',
        'messages',
        'agent_actions',
        'agent_tasks'
    ]

    missing_tables = [table for table in required_tables if table not in existing_tables]

    if missing_tables:
        print(f"Creando tablas faltantes: {missing_tables}")
        tables_to_create = []
        if 'contacts' in missing_tables:
            tables_to_create.append(contact.Contact.__table__)
        if 'conversations' in missing_tables:
            tables_to_create.append(conversation.Conversation.__table__)
        if 'messages' in missing_tables:
            tables_to_create.append(conversation.Message.__table__)
        if 'agent_actions' in missing_tables:
            tables_to_create.append(agent_action.AgentAction.__table__)
        if 'agent_tasks' in missing_tables:
            tables_to_create.append(agent_action.AgentTask.__table__)

        Base.metadata.create_all(bind=engine, tables=tables_to_create)
        print("Tablas faltantes creadas exitosamente.")
    else:
        print("Todas las tablas requeridas ya existen.")
        # Verificar si la tabla contacts necesita actualizarse
        check_contacts_table_update(inspector)

def check_contacts_table_update(inspector):
    """Verifica si la tabla contacts necesita actualizarse con nuevas columnas."""
    columns = [col['name'] for col in inspector.get_columns('contacts')]
    
    # Verificar si las columnas telegram_user_id y platform_user_id existen
    missing_columns = []
    if 'telegram_user_id' not in columns:
        missing_columns.append('telegram_user_id')
    if 'platform_user_id' not in columns:
        missing_columns.append('platform_user_id')
    
    if missing_columns:
        print(f"Actualizando tabla contacts: agregando columnas {missing_columns}")
        # En una implementación real, aquí se ejecutarían las sentencias ALTER TABLE
        # Por ahora, solo mostramos el mensaje
        print("NOTA: En una base de datos de producción, necesitarías ejecutar sentencias ALTER TABLE para agregar estas columnas")
        print("Ejemplo:")
        for col in missing_columns:
            print(f"  ALTER TABLE contacts ADD COLUMN {col} VARCHAR(255);")
    else:
        print("Tabla contacts actualizada.")

def update_contacts_table():
    """Actualiza la tabla contacts con las nuevas columnas."""
    print("Actualizando tabla contacts...")
    try:
        # Para SQLite, necesitamos recrear la tabla con las nuevas columnas
        # Primero respaldamos los datos existentes
        print("Este proceso recreará la tabla contacts. Asegúrate de tener un respaldo.")
        
        # En una implementación real, aquí se manejaría la migración de datos
        # Por ahora, solo mostramos información sobre cómo hacerlo
        
        print("Para actualizar la tabla contacts manualmente en SQLite:")
        print("1. Crear una nueva tabla con las columnas actualizadas")
        print("2. Copiar los datos existentes")
        print("3. Eliminar la tabla vieja")
        print("4. Renombrar la nueva tabla")
        
    except Exception as e:
        print(f"Error al actualizar la tabla contacts: {e}")

if __name__ == "__main__":
    db_path = os.path.join(os.path.dirname(__file__), 'scaie.db')
    
    if os.path.exists(db_path):
        print("El archivo de la base de datos ya existe.")
        check_and_update_tables()
    else:
        print("El archivo de la base de datos no existe. Creando una nueva base de datos.")
        init_db()