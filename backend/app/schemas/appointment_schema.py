from pydantic import BaseModel
from datetime import date, datetime
from typing import Literal, Optional


class AppointmentCreate(BaseModel):

    patient_id: str

    doctor_id: str

    appointment_date: date

    time_slot: str

    reason: str

    notes: Optional[str] = None

class AppointmentUpdate(BaseModel):

    appointment_date: Optional[date] = None

    time_slot: Optional[str] = None

    reason: Optional[str] = None

    notes: Optional[str] = None

    status: Optional[
        Literal[
            "scheduled",
            "completed",
            "cancelled"
        ]
    ] = None