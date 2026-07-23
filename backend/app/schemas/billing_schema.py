from pydantic import BaseModel
from typing import Optional


class BillCreate(BaseModel):
    patient_id: str
    appointment_id: str

    consultation_fee: float
    medicine_cost: float = 0
    test_cost: float = 0
    other_charges: float = 0


class BillResponse(BaseModel):
    message: str
    bill_id: str