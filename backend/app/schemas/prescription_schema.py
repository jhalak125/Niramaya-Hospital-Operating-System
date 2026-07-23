from pydantic import BaseModel
from typing import List


class Medicine(BaseModel):
    name: str
    dosage: str
    frequency: str
    duration: str


class PrescriptionCreate(BaseModel):
    patient_id: str
    doctor_id: str
    medical_record_id: str
    diagnosis: str
    medicines: List[Medicine]
    advice: str