from pydantic import BaseModel, EmailStr, field_validator
from typing import Literal, Optional
import re


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

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        clean_email = v.strip()
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, clean_email):
            raise ValueError("Please provide a valid email address.")
        return clean_email

    @field_validator("phone", "emergency_contact")
    @classmethod
    def validate_phone_10_digits(cls, v: str) -> str:
        digits = re.sub(r"\D", "", str(v or ""))
        if len(digits) != 10:
            raise ValueError("Phone number must contain exactly 10 digits.")
        return digits


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

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        clean_email = v.strip()
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, clean_email):
            raise ValueError("Please provide a valid email address.")
        return clean_email

    @field_validator("phone", "emergency_contact")
    @classmethod
    def validate_phone_10_digits(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        digits = re.sub(r"\D", "", str(v or ""))
        if len(digits) != 10:
            raise ValueError("Phone number must contain exactly 10 digits.")
        return digits