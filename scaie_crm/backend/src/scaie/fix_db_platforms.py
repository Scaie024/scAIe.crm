import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy import create_engine, text
from app.core.database import engine

def fix_db_platforms():
    # Create a new engine for raw SQL execution
    raw_engine = create_engine(engine.url)
    
    # Mapping of old string values to new enum values
    platform_updates = [
        ("'web'", "'WEB'"),
        ("'whatsapp'", "'WHATSAPP'"),
        ("'telegram'", "'TELEGRAM'"),
        ("'facebook_messenger'", "'FACEBOOK_MESSENGER'"),
        ("'instagram'", "'INSTAGRAM'"),
        ("NULL", "'WEB'")  # Default to WEB for NULL values
    ]
    
    with raw_engine.connect() as conn:
        for old_value, new_value in platform_updates:
            try:
                # Update platform values
                update_sql = text(f"UPDATE contacts SET platform = {new_value} WHERE platform = {old_value} OR platform IS NULL")
                result = conn.execute(update_sql)
                print(f"Updated {result.rowcount} contacts with platform {old_value} to {new_value}")
            except Exception as e:
                print(f"Error updating platform from {old_value} to {new_value}: {e}")
        
        conn.commit()
    
    print("Database platform values updated successfully")

if __name__ == "__main__":
    fix_db_platforms()