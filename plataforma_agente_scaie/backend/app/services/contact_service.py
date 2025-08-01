import csv
import json
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_
from ..models.contact import Contact
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
            "page": skip // limit + 1,
            "size": limit
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
        db_contact = Contact(
            name=contact.name,
            phone=contact.phone,
            email=contact.email,
            company=contact.company,
            notes=contact.notes
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
            
        update_data = contact.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_contact, key, value)
            
        db_contact.updated_at = db_contact.__class__.updated_at.default.arg
        db.commit()
        db.refresh(db_contact)
        return db_contact
    
    def delete_contact(self, db: Session, contact_id: int) -> bool:
        """
        Delete contact.
        
        Args:
            db: Database session
            contact_id: Contact ID
            
        Returns:
            Boolean indicating success
        """
        db_contact = self.get_contact(db, contact_id)
        if not db_contact:
            return False
            
        db.delete(db_contact)
        db.commit()
        return True
    
    def import_contacts(self, db: Session, file_path: str, file_type: str) -> Dict[str, Any]:
        """
        Import contacts from file.
        
        Args:
            db: Database session
            file_path: Path to file
            file_type: File type (csv, json)
            
        Returns:
            Dict with import result
        """
        try:
            imported_count = 0
            
            if file_type == "csv":
                with open(file_path, "r", encoding="utf-8") as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        # Check if contact already exists
                        existing_contact = self.get_contact_by_phone(db, row.get("phone"))
                        if not existing_contact:
                            contact_data = ContactCreate(
                                name=row.get("name", ""),
                                phone=row.get("phone", ""),
                                email=row.get("email"),
                                company=row.get("company"),
                                notes=row.get("notes")
                            )
                            self.create_contact(db, contact_data)
                            imported_count += 1
                            
            elif file_type == "json":
                with open(file_path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    for item in data:
                        # Check if contact already exists
                        existing_contact = self.get_contact_by_phone(db, item.get("phone"))
                        if not existing_contact:
                            contact_data = ContactCreate(
                                name=item.get("name", ""),
                                phone=item.get("phone", ""),
                                email=item.get("email"),
                                company=item.get("company"),
                                notes=item.get("notes")
                            )
                            self.create_contact(db, contact_data)
                            imported_count += 1
            
            return {
                "success": True,
                "message": f"Successfully imported {imported_count} contacts",
                "imported_count": imported_count
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error importing contacts: {str(e)}",
                "imported_count": 0
            }
    
    def export_contacts(self, db: Session, file_path: str, file_type: str) -> Dict[str, Any]:
        """
        Export contacts to file.
        
        Args:
            db: Database session
            file_path: Path to file
            file_type: File type (csv, json)
            
        Returns:
            Dict with export result
        """
        try:
            contacts = db.query(Contact).all()
            
            if file_type == "csv":
                with open(file_path, "w", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow(["id", "name", "phone", "email", "company", "notes", "created_at", "updated_at"])
                    for contact in contacts:
                        writer.writerow([
                            contact.id,
                            contact.name,
                            contact.phone,
                            contact.email,
                            contact.company,
                            contact.notes,
                            contact.created_at,
                            contact.updated_at
                        ])
                        
            elif file_type == "json":
                data = [contact.to_dict() for contact in contacts]
                with open(file_path, "w", encoding="utf-8") as file:
                    json.dump(data, file, ensure_ascii=False, indent=2)
            
            return {
                "success": True,
                "message": f"Successfully exported {len(contacts)} contacts",
                "file_path": file_path
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error exporting contacts: {str(e)}",
                "file_path": ""
            }

# Global instance
contact_service = ContactService()