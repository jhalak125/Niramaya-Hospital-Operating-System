from pydantic import BaseModel
from typing import List,Optional


class MedicalRecordCreate(BaseModel):
    appointment_id: str

    diagnosis: str

    symptoms: List[str]

    medications: List[str]

    allergies: List[str]

    notes: str

    follow_up_required: bool = False