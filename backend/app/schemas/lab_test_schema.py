from pydantic import BaseModel
from typing import List


class LabTestCreate(BaseModel):
    appointment_id: str
    tests: List[str]
    notes: str = ""