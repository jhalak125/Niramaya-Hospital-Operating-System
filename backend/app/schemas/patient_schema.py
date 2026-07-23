from pydantic import BaseModel, EmailStr
from typing import Literal, Optional
from datetime import datetime

class PatientCreate(BaseModel):
    full_name: str
    age: int
    gender: Literal["Male", "Female", "Other"]
    blood_group: str
    phone: str
    email: EmailStr
    address: str
    emergency_contact: str
    medical_history: Optional[str] = None
    allergies: list[str] = []
    current_medications: list[str] = []
    height: float
    weight: float


class PatientUpdate(BaseModel):
    full_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[Literal["Male", "Female", "Other"]] = None
    blood_group: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    medical_history: Optional[str] = None
    allergies: Optional[list[str]] = None
    current_medications: Optional[list[str]] = None
    height: Optional[float] = None
    weight: Optional[float] = None