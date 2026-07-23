from datetime import datetime
from fastapi import HTTPException, UploadFile
import os
import shutil
from uuid import uuid4

from app.repositories.appointment_repository import AppointmentRepository
from app.repositories.medical_record_repository import MedicalRecordRepository
from app.config import settings

UPLOAD_DIR = "uploads/medical_records"
os.makedirs(UPLOAD_DIR, exist_ok=True)


async def create_medical_record(
    data,
    current_doctor_id,
    file: UploadFile = None
):
    appointment = await AppointmentRepository.get_by_id(data.appointment_id)
    if appointment is None:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    # Automatically set appointment status to 'Completed' when record is created
    await AppointmentRepository.update_status(data.appointment_id, "Completed")

    # Prevent duplicate record
    existing = await MedicalRecordRepository.get_by_appointment(data.appointment_id)
    if existing:
        return {
            "message": "Medical record already logged for this appointment",
            "record_id": str(existing["_id"])
        }

    record = data.dict()
    record["patient_id"] = str(appointment["patient_id"])
    record["doctor_id"] = str(appointment["doctor_id"])

    if file:
        extension = file.filename.split(".")[-1]
        filename = f"{uuid4()}.{extension}"
        filepath = os.path.join(UPLOAD_DIR, filename)
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        record["attachment"] = filename
    else:
        record["attachment"] = None

    record["created_at"] = datetime.utcnow()
    record["updated_at"] = datetime.utcnow()

    record_id = await MedicalRecordRepository.create(record)

    await create_audit_log(
        user_id=current_doctor_id,
        action="CREATE_MEDICAL_RECORD",
        module="MedicalRecord",
        module_id=str(record_id),
        description="Medical record created"
    )

    return {
        "message": "Medical record created successfully",
        "record_id": str(record_id)
    }


def _format_attachment_url(record):
    record["_id"] = str(record["_id"])
    if record.get("attachment"):
        att = record["attachment"]
        if att.startswith("http://") or att.startswith("https://"):
            record["attachment_url"] = att
        else:
            base = settings.BASE_URL.rstrip("/")
            record["attachment_url"] = f"{base}/uploads/medical_records/{att}"
    return record


async def get_patient_records(patient_id):
    records = await MedicalRecordRepository.get_by_patient(patient_id)
    return [_format_attachment_url(r) for r in records]


async def get_doctor_records(doctor_id):
    records = await MedicalRecordRepository.get_by_doctor(doctor_id)
    return [_format_attachment_url(r) for r in records]


async def get_record(record_id):
    record = await MedicalRecordRepository.get_by_id(record_id)
    if record is None:
        raise HTTPException(
            status_code=404,
            detail="Medical record not found"
        )
    return _format_attachment_url(record)


async def delete_record(record_id):
    record = await MedicalRecordRepository.get_by_id(record_id)
    if record is None:
        raise HTTPException(
            status_code=404,
            detail="Medical record not found"
        )
    await MedicalRecordRepository.delete(record_id)
    await create_audit_log(
        user_id=record.get("doctor_id", "SYSTEM"),
        action="DELETE_MEDICAL_RECORD",
        module="MedicalRecord",
        module_id=record_id,
        description="Medical record deleted"
    )
    return {"message": "Medical record deleted successfully"}


async def search_medical_records(
    patient_id=None,
    doctor_id=None,
    diagnosis=None,
    page=1,
    limit=10,
    sort_by=None,
    order="asc"
):
    records = await MedicalRecordRepository.search(
        patient_id,
        doctor_id,
        diagnosis,
        page,
        limit,
        sort_by,
        order
    )
    return [_format_attachment_url(r) for r in records]