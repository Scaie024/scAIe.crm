from typing import Optional, List
from pydantic import BaseModel, ConfigDict, field_validator

from ..models.contact import InterestLevel

class ContactBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    company: Optional[str] = None
    notes: Optional[str] = None
    interest_level: Optional[InterestLevel] = InterestLevel.NEW

    @staticmethod
    def _empty_to_none(v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        if isinstance(v, str):
            s = v.strip()
            return s if s != "" else None
        return v

    @field_validator("phone", "email", "company", "notes", mode="before")
    @classmethod
    def normalize_optional_strings(cls, v):
        return cls._empty_to_none(v)

    @field_validator("name", mode="before")
    @classmethod
    def normalize_name(cls, v):
        if v is None:
            return "Sin nombre"
        if isinstance(v, str):
            s = v.strip()
            return s if s != "" else "Sin nombre"
        return str(v)

    @field_validator("interest_level", mode="before")
    @classmethod
    def normalize_interest_level(cls, v):
        if v is None:
            return InterestLevel.NEW
        if isinstance(v, InterestLevel):
            return v
        if isinstance(v, str):
            mapping = {
                "nuevo": InterestLevel.NEW,
                "contactado": InterestLevel.CONTACTED,
                "interesado": InterestLevel.INTERESTED,
                "confirmado": InterestLevel.CONFIRMED,
                "no_interesado": InterestLevel.NOT_INTERESTED,
            }
            return mapping.get(v, InterestLevel.NEW)
        return InterestLevel.NEW

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