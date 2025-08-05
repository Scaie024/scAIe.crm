#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from app.core.database import get_db
from app.models.contact import Contact

def test_db():
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        # Test querying
        print("Testing query...")
        contact = db.query(Contact).first()
        print(f"Query result: {contact}")
        
        # Test insertion
        print("Testing insertion...")
        new_contact = Contact(
            name="Test Contact",
            phone="999888777"
        )
        db.add(new_contact)
        db.commit()
        print("Insertion successful")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    test_db()