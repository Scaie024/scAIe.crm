from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
import enum

class InterestLevel(str, enum.Enum):
    NEW = "nuevo"
    CONTACTED = "contactado"
    INTERESTED = "interesado"
    CONFIRMED = "confirmado"
    NOT_INTERESTED = "no_interesado"

class ContactBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    phone: str
    email: Optional[str] = None
    company: Optional[str] = None
    notes: Optional[str] = None
    interest_level: Optional[InterestLevel] = InterestLevel.NEW

class ContactCreate(ContactBase):
    model_config = ConfigDict(from_attributes=True)

class ContactUpdate(ContactBase):
    model_config = ConfigDict(from_attributes=True)
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    company: Optional[str] = None
    notes: Optional[str] = None
    interest_level: Optional[InterestLevel] = None

class Contact(ContactBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime

class ContactList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    contacts: List[Contact]
    total: int
    page: int
    size: int

class ImportResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    success: bool
    message: str
    imported_count: int

class ExportResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    success: bool
    message: str
    file_path: str

class ContactInteractionBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    contact_id: int
    interaction_type: str
    details: Optional[str] = None

class ContactInteractionCreate(ContactInteractionBase):
    model_config = ConfigDict(from_attributes=True)
    pass

class ContactInteraction(ContactInteractionBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    date: datetime