#!/usr/bin/env python3
"""
Script para migrar la tabla contacts y agregar las columnas telegram_user_id y platform_user_id.
"""

import os
import sys
import sqlite3

def migrate_contacts_table():
    """Migra la tabla contacts para agregar las nuevas columnas."""
    db_path = os.path.join(os.path.dirname(__file__), 'scaie.db')
    
    if not os.path.exists(db_path):
        print("No se encontró la base de datos.")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar si las columnas ya existen
        cursor.execute("PRAGMA table_info(contacts)")
        columns = [info[1] for info in cursor.fetchall()]
        
        print(f"Columnas actuales en la tabla contacts: {columns}")
        
        # Agregar columna telegram_user_id si no existe
        if 'telegram_user_id' not in columns:
            print("Agregando columna telegram_user_id...")
            cursor.execute("ALTER TABLE contacts ADD COLUMN telegram_user_id VARCHAR(255)")
            print("Columna telegram_user_id agregada.")
        else:
            print("La columna telegram_user_id ya existe.")
        
        # Agregar columna platform_user_id si no existe
        if 'platform_user_id' not in columns:
            print("Agregando columna platform_user_id...")
            cursor.execute("ALTER TABLE contacts ADD COLUMN platform_user_id VARCHAR(255)")
            print("Columna platform_user_id agregada.")
        else:
            print("La columna platform_user_id ya existe.")
        
        conn.commit()
        conn.close()
        
        print("Migración completada exitosamente.")
        return True
        
    except Exception as e:
        print(f"Error durante la migración: {e}")
        return False

if __name__ == "__main__":
    print("Iniciando migración de la tabla contacts...")
    success = migrate_contacts_table()
    if success:
        print("Migración finalizada correctamente.")
    else:
        print("La migración falló.")
        sys.exit(1)