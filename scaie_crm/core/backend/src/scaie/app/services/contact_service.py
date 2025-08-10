import csv
import json
import logging
from datetime import datetime
from typing import List, Optional, Dict, Any, Union
from sqlalchemy.orm import Session
from sqlalchemy import or_, func, desc
from ..models.contact import Contact, InterestLevel
from ..schemas.contact import ContactCreate, ContactUpdate

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContactService:
    # --- helpers ---
    @staticmethod
    def _norm_str(val: Optional[str]) -> Optional[str]:
        if val is None:
            return None
        if isinstance(val, str):
            s = val.strip()
            return s if s != "" else None
        return str(val)

    @staticmethod
    def _merge_missing_fields(target: Contact, source: Dict[str, Any]) -> bool:
        """Fill only missing (None/empty) fields in target from provided source. Returns True if any change was made."""
        changed = False
        for field in ["name", "phone", "email", "company", "notes"]:
            incoming = ContactService._norm_str(source.get(field)) if field in source else None
            if not incoming:
                continue
            current = getattr(target, field)
            if current is None or (isinstance(current, str) and current.strip() == ""):
                setattr(target, field, incoming)
                changed = True
        # interest_level
        if "interest_level" in source and source.get("interest_level") is not None:
            try:
                val = source.get("interest_level")
                if isinstance(val, str):
                    interest_level_map = {
                        "nuevo": InterestLevel.NEW,
                        "contactado": InterestLevel.CONTACTED,
                        "interesado": InterestLevel.INTERESTED,
                        "confirmado": InterestLevel.CONFIRMED,
                        "no_interesado": InterestLevel.NOT_INTERESTED,
                    }
                    val = interest_level_map.get(val, None)
                if val and getattr(target, "interest_level", None) != val:
                    setattr(target, "interest_level", val)
                    changed = True
            except Exception:
                pass
        return changed

    def get_contacts(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        interest: Optional[str] = None,
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
        try:
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
            # Optional interest level filter (string values mapped to enum)
            if interest:
                interest_map = {
                    "nuevo": InterestLevel.NEW,
                    "contactado": InterestLevel.CONTACTED,
                    "interesado": InterestLevel.INTERESTED,
                    "confirmado": InterestLevel.CONFIRMED,
                    "no_interesado": InterestLevel.NOT_INTERESTED,
                }
                enum_val = interest_map.get(interest)
                if enum_val is not None:
                    query = query.filter(Contact.interest_level == enum_val)
            
            total = query.count()
            contacts = query.offset(skip).limit(limit).all()
            
            return {
                "contacts": [contact.to_dict() for contact in contacts],
                "total": total,
                "skip": skip,
                "limit": limit
            }
        except Exception as e:
            logger.error(f"Error getting contacts: {str(e)}")
            raise
    
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
        # Normalize inputs
        name = self._norm_str(contact.name) or "Sin nombre"
        phone = self._norm_str(contact.phone)
        email = self._norm_str(contact.email)
        company = self._norm_str(contact.company)
        notes = self._norm_str(contact.notes)

        # Dedupe by phone or email if provided
        existing: Optional[Contact] = None
        if phone:
            existing = db.query(Contact).filter(Contact.phone == phone).first()
        if not existing and email:
            existing = db.query(Contact).filter(Contact.email == email).first()

        if existing:
            # merge missing fields and return existing
            changed = self._merge_missing_fields(existing, {
                "name": name,
                "phone": phone,
                "email": email,
                "company": company,
                "notes": notes,
                "interest_level": contact.interest_level,
            })
            if changed:
                db.commit()
                db.refresh(existing)
            return existing

        # Create new
        db_contact = Contact(
            name=name,
            phone=phone,
            email=email,
            company=company,
            notes=notes,
            interest_level=contact.interest_level,
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
        # Normalize strings
        for k in ["name", "phone", "email", "company", "notes"]:
            if k in update_data:
                update_data[k] = self._norm_str(update_data[k])
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
            # Prevent UNIQUE(phone) issues: if phone is set, ensure not colliding with other contacts
            if key == "phone" and value:
                other = db.query(Contact).filter(Contact.phone == value, Contact.id != db_contact.id).first()
                if other:
                    # If trying to set to an existing phone, keep current value and skip updating phone
                    logger.warning(f"Attempt to set duplicate phone {value} on contact {db_contact.id}; skipping phone update")
                    continue
            setattr(db_contact, key, value)
            
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
            # naive CSV split can break on commas; use csv module
            reader = csv.reader(lines)
            headers = next(reader)
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
            
            for i, row in enumerate(reader, start=2):  # Start from line 2 (1-indexed)
                try:
                    values = row
                    if len(values) != len(headers):
                        errors.append(f"Line {i}: Column count mismatch")
                        continue
                    
                    # Create contact data
                    contact_data = {}
                    for header, value in zip(headers, values):
                        contact_data[header] = self._norm_str(value)
                    
                    # Create or merge contact (dedupe inside create_contact)
                    try:
                        contact_create = ContactCreate(**contact_data)
                    except Exception as ve:
                        errors.append(f"Line {i}: {str(ve)}")
                        continue
                    created_or_existing = self.create_contact(db, contact_create)
                    imported_count += 1 if created_or_existing else 0
                    
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
                    # Normalize map
                    for k in ["name", "phone", "email", "company", "notes"]:
                        if k in contact_data:
                            contact_data[k] = self._norm_str(contact_data[k])
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

    def import_contacts_from_file(self, db: Session, file_path: str, file_type: str) -> Dict[str, Any]:
        """
        Import contacts from file.
        
        Args:
            db: Database session
            file_path: Path to the file
            file_type: Type of file (csv or json)
            
        Returns:
            Dict with import results
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                file_content = file.read()
            
            if file_type == 'csv':
                return self.import_contacts_from_csv(db, file_content)
            elif file_type == 'json':
                return self.import_contacts_from_json(db, file_content)
            else:
                return {
                    "success": False,
                    "message": f"Unsupported file type: {file_type}",
                    "imported_count": 0
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error reading file: {str(e)}",
                "imported_count": 0
            }
    
    def export_contacts(self, db: Session, file_path: str, file_type: str) -> Dict[str, Any]:
        """
        Export contacts to file.
        
        Args:
            db: Database session
            file_path: Path to save the file
            file_type: Type of file (csv or json)
            
        Returns:
            Dict with export results
        """
        try:
            if file_type == 'csv':
                content = self.export_contacts_to_csv(db)
            elif file_type == 'json':
                content = self.export_contacts_to_json(db)
            else:
                return {
                    "success": False,
                    "message": f"Unsupported file type: {file_type}"
                }
            
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            
            return {
                "success": True,
                "message": f"Contacts exported to {file_path}",
                "file_path": file_path
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error exporting contacts: {str(e)}"
            }

# Create singleton instance
contact_service = ContactService()