from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import os
import tempfile

from ...core.database import get_db
from ...services.contact_service import contact_service
from ...schemas.contact import Contact, ContactCreate, ContactUpdate, ContactList, ImportResponse, ExportResponse

router = APIRouter(prefix="/contacts", tags=["contacts"])

@router.get("/", response_model=ContactList)
def list_contacts(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = Query(None, description="Search in name, phone, email or company"),
    db: Session = Depends(get_db)
):
    """
    List contacts with optional search and pagination.
    """
    return contact_service.get_contacts(db, skip=skip, limit=limit, search=search)

@router.post("/", response_model=Contact)
def create_contact(
    contact: ContactCreate,
    db: Session = Depends(get_db)
):
    """
    Create new contact.
    """
    # Check if contact with this phone already exists
    if contact.phone:
        existing_contact = contact_service.get_contact_by_phone(db, contact.phone)
        if existing_contact:
            raise HTTPException(status_code=400, detail="Contact with this phone number already exists")
    
    db_contact = contact_service.create_contact(db, contact)
    return Contact(**db_contact.to_dict())

@router.get("/stats")
def get_contact_stats(
    db: Session = Depends(get_db)
):
    """
    Get contact statistics.
    """
    return contact_service.get_contact_stats(db)

@router.get("/{contact_id}", response_model=Contact)
def get_contact(
    contact_id: int,
    db: Session = Depends(get_db)
):
    """
    Get contact by ID.
    """
    contact = contact_service.get_contact(db, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@router.put("/{contact_id}", response_model=Contact)
def update_contact(
    contact_id: int,
    contact: ContactUpdate,
    db: Session = Depends(get_db)
):
    """
    Update contact.
    """
    db_contact = contact_service.update_contact(db, contact_id, contact)
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return Contact(**db_contact.to_dict())

@router.delete("/{contact_id}")
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete contact.
    """
    success = contact_service.delete_contact(db, contact_id)
    if not success:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"message": "Contact deleted successfully"}

@router.post("/import", response_model=ImportResponse)
async def import_contacts(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Import contacts from CSV or JSON file.
    """
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(await file.read())
        tmp_file_path = tmp_file.name
    
    try:
        # Determine file type
        file_type = ""
        if file.filename and "." in file.filename:
            file_type = file.filename.split(".")[-1].lower()
        
        if file_type not in ["csv", "json"]:
            raise HTTPException(status_code=400, detail="Unsupported file type. Use CSV or JSON.")
        
        # Import contacts
        result = contact_service.import_contacts_from_file(db, tmp_file_path, file_type)
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["message"])
            
        return result
    finally:
        # Clean up temporary file
        if os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)

@router.get("/export/{file_type}")
def export_contacts(
    file_type: str,
    db: Session = Depends(get_db)
):
    """
    Export contacts to CSV or JSON file.
    """
    if file_type not in ["csv", "json"]:
        raise HTTPException(status_code=400, detail="Unsupported file type. Use CSV or JSON.")
    
    try:
        if file_type == 'csv':
            content = contact_service.export_contacts_to_csv(db)
            media_type = "text/csv"
            filename = f"contacts_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        else:  # json
            content = contact_service.export_contacts_to_json(db)
            media_type = "application/json"
            filename = f"contacts_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        from fastapi.responses import Response
        return Response(
            content=content,
            media_type=media_type,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error exporting contacts: {str(e)}")