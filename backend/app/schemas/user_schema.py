from pydantic import BaseModel, EmailStr
from typing import Literal


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

class UserLogin(BaseModel):
    email: EmailStr
    password: str