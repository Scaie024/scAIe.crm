from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ContactBase(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None
    company: Optional[str] = None
    notes: Optional[str] = None

class ContactCreate(ContactBase):
    pass

class ContactUpdate(ContactBase):
    name: Optional[str] = None
    phone: Optional[str] = None

class Contact(ContactBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

class ContactList(BaseModel):
    contacts: List[Contact]
    total: int
    page: int
    size: int

class ImportResponse(BaseModel):
    success: bool
    message: str
    imported_count: int

class ExportResponse(BaseModel):
    success: bool
    message: str
    file_path: str