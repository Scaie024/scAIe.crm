import csv
import json
from datetime import datetime
from typing import List, Optional, Dict, Any, Union
from sqlalchemy.orm import Session
from sqlalchemy import or_, func, desc
from ..models.contact import Contact, InterestLevel
from ..schemas.contact import ContactCreate, ContactUpdate

class ContactService:
    def get_contacts(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100, 
        search: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get list of contacts with optional search.
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            search: Search term for name, phone, or email
            
        Returns:
            Dict with contacts and pagination info
        """
        query = db.query(Contact)
        
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                or_(
                    Contact.name.like(search_filter),
                    Contact.phone.like(search_filter),
                    Contact.email.like(search_filter),
                    Contact.company.like(search_filter)
                )
            )
        
        total = query.count()
        contacts = query.offset(skip).limit(limit).all()
        
        return {
            "contacts": [contact.to_dict() for contact in contacts],
            "total": total,
            "skip": skip,
            "limit": limit
        }
    
    def get_contact(self, db: Session, contact_id: int) -> Optional[Contact]:
        """
        Get contact by ID.
        
        Args:
            db: Database session
            contact_id: Contact ID
            
        Returns:
            Contact object or None
        """
        return db.query(Contact).filter(Contact.id == contact_id).first()
    
    def get_contact_by_phone(self, db: Session, phone: str) -> Optional[Contact]:
        """
        Get contact by phone number.
        
        Args:
            db: Database session
            phone: Phone number
            
        Returns:
            Contact object or None
        """
        return db.query(Contact).filter(Contact.phone == phone).first()
    
    def create_contact(self, db: Session, contact: ContactCreate) -> Contact:
        """
        Create new contact.
        
        Args:
            db: Database session
            contact: Contact data
            
        Returns:
            Created contact object
        """
        # Convert interest_level to enum if provided as string
        interest_level = contact.interest_level
        if isinstance(interest_level, str):
            try:
                # Map string values to enum values
                interest_level_map = {
                    "nuevo": InterestLevel.NEW,
                    "contactado": InterestLevel.CONTACTED,
                    "interesado": InterestLevel.INTERESTED,
                    "confirmado": InterestLevel.CONFIRMED,
                    "no_interesado": InterestLevel.NOT_INTERESTED
                }
                interest_level = interest_level_map.get(interest_level, InterestLevel.NEW)
            except Exception:
                interest_level = InterestLevel.NEW
        
        db_contact = Contact(
            name=contact.name,
            phone=contact.phone,
            email=contact.email,
            company=contact.company,
            notes=contact.notes,
            interest_level=interest_level
        )
        db.add(db_contact)
        db.commit()
        db.refresh(db_contact)
        return db_contact
    
    def update_contact(self, db: Session, contact_id: int, contact: ContactUpdate) -> Optional[Contact]:
        """
        Update existing contact.
        
        Args:
            db: Database session
            contact_id: Contact ID
            contact: Updated contact data
            
        Returns:
            Updated contact object or None
        """
        db_contact = self.get_contact(db, contact_id)
        if not db_contact:
            return None
            
        update_data = contact.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            # Handle interest_level conversion
            if key == "interest_level" and isinstance(value, str):
                try:
                    # Map string values to enum values
                    interest_level_map = {
                        "nuevo": InterestLevel.NEW,
                        "contactado": InterestLevel.CONTACTED,
                        "interesado": InterestLevel.INTERESTED,
                        "confirmado": InterestLevel.CONFIRMED,
                        "no_interesado": InterestLevel.NOT_INTERESTED
                    }
                    value = interest_level_map.get(value, InterestLevel.NEW)
                except Exception:
                    continue
            setattr(db_contact, key, value)
            
        db_contact.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_contact)
        return db_contact
    
    def delete_contact(self, db: Session, contact_id: int) -> bool:
        """
        Delete contact by ID.
        
        Args:
            db: Database session
            contact_id: Contact ID
            
        Returns:
            True if deleted, False if not found
        """
        contact = self.get_contact(db, contact_id)
        if not contact:
            return False
            
        db.delete(contact)
        db.commit()
        return True
    
    def get_contact_stats(self, db: Session) -> Dict[str, Any]:
        """
        Get contact statistics.
        
        Args:
            db: Database session
            
        Returns:
            Dict with contact statistics
        """
        # Total contacts
        total = db.query(Contact).count()
        
        # Contacts by interest level
        interest_counts = {}
        for level in InterestLevel:
            count = db.query(Contact).filter(Contact.interest_level == level).count()
            interest_counts[level.value] = count
            
        return {
            "total": total,
            "interest_level_distribution": interest_counts
        }
    
    def import_contacts_from_csv(self, db: Session, file_content: str) -> Dict[str, Any]:
        """
        Import contacts from CSV content.
        
        Args:
            db: Database session
            file_content: CSV file content as string
            
        Returns:
            Dict with import results
        """
        try:
            # Parse CSV content
            lines = file_content.strip().split('\n')
            if not lines:
                return {"success": False, "message": "Empty file", "imported_count": 0}
            
            # Get headers
            headers = lines[0].split(',')
            headers = [h.strip().lower() for h in headers]
            
            # Required fields
            required_fields = ['name', 'phone']
            
            # Check if required fields are present
            missing_fields = [field for field in required_fields if field not in headers]
            if missing_fields:
                return {
                    "success": False, 
                    "message": f"Missing required fields: {', '.join(missing_fields)}", 
                    "imported_count": 0
                }
            
            # Process rows
            imported_count = 0
            errors = []
            
            for i, line in enumerate(lines[1:], start=2):  # Start from line 2 (1-indexed)
                try:
                    values = line.split(',')
                    if len(values) != len(headers):
                        errors.append(f"Line {i}: Column count mismatch")
                        continue
                    
                    # Create contact data
                    contact_data = {}
                    for header, value in zip(headers, values):
                        contact_data[header] = value.strip()
                    
                    # Check if contact already exists
                    if self.get_contact_by_phone(db, contact_data['phone']):
                        errors.append(f"Line {i}: Contact with phone {contact_data['phone']} already exists")
                        continue
                    
                    # Create contact
                    contact_create = ContactCreate(**contact_data)
                    self.create_contact(db, contact_create)
                    imported_count += 1
                    
                except Exception as e:
                    errors.append(f"Line {i}: {str(e)}")
            
            # Prepare result message
            message = f"Imported {imported_count} contacts"
            if errors:
                message += f". Errors: {len(errors)}"
            
            return {
                "success": True,
                "message": message,
                "imported_count": imported_count,
                "errors": errors
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error parsing CSV: {str(e)}",
                "imported_count": 0
            }
    
    def import_contacts_from_json(self, db: Session, file_content: str) -> Dict[str, Any]:
        """
        Import contacts from JSON content.
        
        Args:
            db: Database session
            file_content: JSON file content as string
            
        Returns:
            Dict with import results
        """
        try:
            # Parse JSON content
            data = json.loads(file_content)
            
            # If data is a list, process each item
            if isinstance(data, list):
                contacts_data = data
            # If data is a dict with a contacts key, use that
            elif isinstance(data, dict) and 'contacts' in data:
                contacts_data = data['contacts']
            else:
                return {
                    "success": False,
                    "message": "Invalid JSON format. Expected list of contacts or dict with 'contacts' key",
                    "imported_count": 0
                }
            
            # Process contacts
            imported_count = 0
            errors = []
            
            for i, contact_data in enumerate(contacts_data, start=1):
                try:
                    # Check if contact already exists
                    if 'phone' in contact_data and self.get_contact_by_phone(db, contact_data['phone']):
                        errors.append(f"Item {i}: Contact with phone {contact_data['phone']} already exists")
                        continue
                    
                    # Create contact
                    contact_create = ContactCreate(**contact_data)
                    self.create_contact(db, contact_create)
                    imported_count += 1
                    
                except Exception as e:
                    errors.append(f"Item {i}: {str(e)}")
            
            # Prepare result message
            message = f"Imported {imported_count} contacts"
            if errors:
                message += f". Errors: {len(errors)}"
            
            return {
                "success": True,
                "message": message,
                "imported_count": imported_count,
                "errors": errors
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error parsing JSON: {str(e)}",
                "imported_count": 0
            }
    
    def export_contacts_to_csv(self, db: Session) -> str:
        """
        Export contacts to CSV format.
        
        Args:
            db: Database session
            
        Returns:
            CSV content as string
        """
        # Get all contacts
        contacts = db.query(Contact).all()
        
        # Define headers
        headers = ['id', 'name', 'phone', 'email', 'company', 'notes', 'interest_level', 'created_at', 'updated_at']
        
        # Create CSV content
        lines = [','.join(headers)]
        
        for contact in contacts:
            values = [
                str(contact.id),
                contact.name or '',
                contact.phone or '',
                contact.email or '',
                contact.company or '',
                contact.notes or '',
                contact.interest_level.value if contact.interest_level else '',
                contact.created_at.isoformat() if contact.created_at else '',
                contact.updated_at.isoformat() if contact.updated_at else ''
            ]
            lines.append(','.join(f'"{v}"' if ',' in v or '"' in v else v for v in values))
        
        return '\n'.join(lines)
    
    def export_contacts_to_json(self, db: Session) -> str:
        """
        Export contacts to JSON format.
        
        Args:
            db: Database session
            
        Returns:
            JSON content as string
        """
        # Get all contacts
        contacts = db.query(Contact).all()
        
        # Convert to dict
        contacts_data = [contact.to_dict() for contact in contacts]
        
        # Create JSON content
        return json.dumps({
            "contacts": contacts_data,
            "exported_at": datetime.utcnow().isoformat()
        }, indent=2)

# Create singleton instance
contact_service = ContactService()