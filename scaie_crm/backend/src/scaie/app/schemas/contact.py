from typing import Optional, List
from pydantic import BaseModel, ConfigDict

from ..models.contact import InterestLevel

class ContactBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: str
    phone: str
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

class ContactSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    phone: str
    interest_level: InterestLevel
    created_at: str
    updated_at: str

class ContactList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    contacts: List[Contact]
    total: int

class ImportResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    success: bool
    message: str
    imported_count: int

class ExportResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    success: bool
    message: str
    exported_count: int