from pydantic import BaseModel
from typing import Optional, Literal


class DoctorCreate(BaseModel):
    user_id: Optional[str] = None
    doctor_name: Optional[str] = "Dr. Specialist"
    department: str = "General Medicine"
    specialization: str = "Senior Physician"
    qualification: Optional[str] = "MBBS, MD"
    experience: int = 5
    consultation_fee: float = 1000.0
    working_days: Optional[list[str]] = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    start_time: Optional[str] = "09:00 AM"
    end_time: Optional[str] = "05:00 PM"
    status: Optional[str] = "available"


class DoctorUpdate(BaseModel):
    department: Optional[str] = None
    specialization: Optional[str] = None
    qualification: Optional[str] = None
    experience: Optional[int] = None
    consultation_fee: Optional[float] = None
    working_days: Optional[list[str]] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    status: Optional[Literal["available", "unavailable"]] = None