from fastapi import APIRouter, Depends

from app.schemas.prescription_schema import PrescriptionCreate
from app.services.prescription_service import (
    create_prescription,
    get_patient_prescriptions
)
from app.dependencies.role_dependency import require_roles

router = APIRouter(
    prefix="/prescriptions",
    tags=["Prescriptions"]
)


@router.post("")
@router.post("/")
async def create(
    prescription: PrescriptionCreate,
    current_user=Depends(require_roles("doctor"))
):
    return await create_prescription(prescription)


@router.get("/patient/{patient_id}")
async def get_patient_history(
    patient_id: str,
    current_user=Depends(require_roles("patient", "doctor", "admin"))
):
    return await get_patient_prescriptions(patient_id)