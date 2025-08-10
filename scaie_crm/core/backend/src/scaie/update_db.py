import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker
from app.core.database import Base, engine
from app.models.contact import Contact

def update_database():
    # Create a new engine for raw SQL execution
    raw_engine = create_engine(engine.url)
    
    # List of columns to add
    columns_to_add = [
        ("whatsapp_user_id", "VARCHAR"),
        ("facebook_messenger_user_id", "VARCHAR"),
        ("instagram_user_id", "VARCHAR"),
        ("platform", "VARCHAR(20) DEFAULT 'web'")
    ]
    
    with raw_engine.connect() as conn:
        for column_name, column_type in columns_to_add:
            try:
                # Check if column exists
                check_sql = f"SELECT COUNT(*) FROM pragma_table_info('contacts') WHERE name='{column_name}'"
                result = conn.execute(check_sql)
                exists = result.fetchone()[0] > 0
                
                if not exists:
                    # Add column if it doesn't exist
                    alter_sql = f"ALTER TABLE contacts ADD COLUMN {column_name} {column_type}"
                    conn.execute(alter_sql)
                    print(f"Added column {column_name} to contacts table")
                else:
                    print(f"Column {column_name} already exists")
            except Exception as e:
                print(f"Error adding column {column_name}: {e}")
        
        conn.commit()
    
    print("Database update completed")

if __name__ == "__main__":
    update_database()