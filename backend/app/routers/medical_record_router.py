from fastapi import APIRouter, Depends, UploadFile, File, Form
from typing import Optional

from app.schemas.medical_record_schema import MedicalRecordCreate
from app.services.medical_record_service import (
    create_medical_record,
    get_patient_records,
    get_doctor_records,
    get_record,
    delete_record,
    search_medical_records
)
from app.dependencies.role_dependency import require_roles


router = APIRouter(
    prefix="/medical-records",
    tags=["Medical Records"]
)


@router.post("/")
async def add_record(
    appointment_id: str = Form(...),
    diagnosis: str = Form(...),
    symptoms: Optional[str] = Form(""),
    medications: Optional[str] = Form(""),
    allergies: Optional[str] = Form(""),
    notes: Optional[str] = Form(""),
    file: UploadFile = File(None),
    current_user=Depends(require_roles("doctor"))
):
    symp_list = [s.strip() for s in symptoms.split(",") if s.strip()] if symptoms else []
    meds_list = [m.strip() for m in medications.split(",") if m.strip()] if medications else []
    allg_list = [a.strip() for a in allergies.split(",") if a.strip()] if allergies else []

    record = MedicalRecordCreate(
        appointment_id=appointment_id,
        diagnosis=diagnosis,
        symptoms=symp_list,
        medications=meds_list,
        allergies=allg_list,
        notes=notes or ""
    )

    return await create_medical_record(
        record,
        current_user["sub"],
        file
    )


@router.get("/patient/{patient_id}")
async def patient_records(
    patient_id: str,
    current_user=Depends(require_roles("doctor", "admin"))
):
    return await get_patient_records(patient_id)


@router.get("/doctor/my")
async def doctor_records(
    current_user=Depends(require_roles("doctor"))
):
    return await get_doctor_records(current_user["sub"])


@router.get("/search")
async def search_records(
    patient_id: Optional[str] = None,
    doctor_id: Optional[str] = None,
    diagnosis: Optional[str] = None,
    page: int = 1,
    limit: int = 10,
    sort_by: Optional[str] = None,
    order: str = "asc",
    current_user=Depends(require_roles("doctor", "admin"))
):
    return await search_medical_records(
        patient_id,
        doctor_id,
        diagnosis,
        page,
        limit,
        sort_by,
        order
    )


@router.get("/{record_id}")
async def record_details(
    record_id: str,
    current_user=Depends(require_roles("doctor", "admin"))
):
    return await get_record(record_id)


@router.delete("/{record_id}")
async def remove_record(
    record_id: str,
    current_user=Depends(require_roles("admin"))
):
    return await delete_record(record_id)