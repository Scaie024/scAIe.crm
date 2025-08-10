import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.core.database import SessionLocal
from app.models.contact import Contact, PlatformType

def fix_contacts():
    db = SessionLocal()
    try:
        # Get all contacts
        contacts = db.query(Contact).all()
        print(f"Found {len(contacts)} contacts")
        
        for contact in contacts:
            print(f"Processing contact: {contact.name} (ID: {contact.id})")
            print(f"  Current platform: {contact.platform}")
            
            # Fix platform if it's None or invalid
            if contact.platform is None:
                print(f"  Fixing platform for contact {contact.id}")
                contact.platform = PlatformType.WEB
                db.add(contact)
            
            # Make sure platform is a valid enum value
            elif isinstance(contact.platform, str):
                # Convert string values to enum
                platform_mapping = {
                    'web': PlatformType.WEB,
                    'whatsapp': PlatformType.WHATSAPP,
                    'telegram': PlatformType.TELEGRAM,
                    'facebook_messenger': PlatformType.FACEBOOK_MESSENGER,
                    'instagram': PlatformType.INSTAGRAM
                }
                
                if contact.platform.lower() in platform_mapping:
                    contact.platform = platform_mapping[contact.platform.lower()]
                    db.add(contact)
                    print(f"  Converted platform string to enum for contact {contact.id}")
                else:
                    print(f"  Invalid platform string '{contact.platform}' for contact {contact.id}, setting to WEB")
                    contact.platform = PlatformType.WEB
                    db.add(contact)
        
        # Commit changes
        db.commit()
        print("All contacts fixed successfully")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_contacts()