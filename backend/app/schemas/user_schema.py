from pydantic import BaseModel, EmailStr, field_validator
from typing import Literal
import re


class UserRegister(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    phone: str
    role: Literal[
        "admin",
        "doctor",
        "patient",
        "receptionist",
        "nurse",
        "lab_technician",
        "pharmacist"
    ]

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        clean_email = v.strip()
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, clean_email):
            raise ValueError("Please provide a valid email address (e.g., user@example.com).")
        return clean_email

    @field_validator("phone")
    @classmethod
    def validate_phone_10_digits(cls, v: str) -> str:
        digits = re.sub(r"\D", "", str(v or ""))
        if len(digits) != 10:
            raise ValueError("Phone number must contain exactly 10 digits.")
        return digits


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        clean_email = v.strip()
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, clean_email):
            raise ValueError("Please provide a valid email address.")
        return clean_email