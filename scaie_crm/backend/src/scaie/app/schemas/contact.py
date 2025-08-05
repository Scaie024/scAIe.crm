from typing import Optional, List
from pydantic import BaseModel, ConfigDict

from ..models.contact import InterestLevel

class ContactBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    company: Optional[str] = None
    notes: Optional[str] = None
    interest_level: Optional[InterestLevel] = InterestLevel.NEW

class ContactCreate(ContactBase):
    pass

class ContactUpdate(ContactBase):
    name: Optional[str] = None
    phone: Optional[str] = None

class ContactInDBBase(ContactBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: str
    updated_at: str

class Contact(ContactInDBBase):
    pass

class ContactList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    contacts: List[Contact]
    total: int
    skip: int
    limit: int

class ImportResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    success: bool
    message: str
    imported_count: Optional[int] = None

class ExportResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    success: bool
    message: str
    file_path: Optional[str] = None