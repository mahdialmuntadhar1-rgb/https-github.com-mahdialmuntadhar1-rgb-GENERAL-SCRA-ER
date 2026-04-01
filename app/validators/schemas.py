from pydantic import BaseModel, EmailStr, HttpUrl, Field
from typing import Optional, List

class UniversityValidator(BaseModel):
    name_en: str = Field(..., min_length=2)
    name_ar: str = Field(..., min_length=2)
    website: Optional[HttpUrl] = None
    governorate_id: int
    city_id: int
    institution_type: str
    public_private: str

class ContactValidator(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    whatsapp: Optional[str] = None
    contact_type: str

class PostValidator(BaseModel):
    title: str
    content: str
    category: str
    language: str
