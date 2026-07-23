from datetime import datetime
from app.repositories.patient_repository import PatientRepository
from app.services.audit_log_service import create_audit_log


async def create_patient(patient):

    patient_dict = patient.model_dump()

    patient_dict["status"] = "active"
    patient_dict["created_at"] = datetime.utcnow()
    patient_dict["updated_at"] = datetime.utcnow()

    patient_id = await PatientRepository.create(patient_dict)

    await create_audit_log(
    user_id=patient_dict["user_id"],
    action="CREATE",
    module="PATIENT",
    module_id=str(patient_id),
    description=f"Patient {patient.full_name} created"
)

    return {
        "message": "Patient created successfully",
        "patient_id": str(patient_id)
    }

from bson import ObjectId
from app.database.database import db


async def get_patient(patient_id: str):

    patient = await PatientRepository.get_by_id(patient_id)

    if not patient:
        return {"message": "Patient not found"}

    patient["_id"] = str(patient["_id"])

    return patient

async def get_all_patients():

    patients = await PatientRepository.get_all()

    for patient in patients:
        patient["_id"] = str(patient["_id"])

    return patients

async def update_patient(patient_id: str, patient):

    data = patient.model_dump(exclude_unset=True)

    data["updated_at"] = datetime.utcnow()

    result = await PatientRepository.update(
        ObjectId(patient_id),
        data
    )

    await create_audit_log(
    user_id="SYSTEM",
    action="UPDATE_PATIENT",
    module="Patient",
    module_id=patient_id,
    description="Patient updated"
)

    if result.modified_count == 0:
        return {"message": "Patient not found"}

    return {
        "message": "Patient updated successfully"
    }

async def delete_patient(patient_id: str):

    result = await PatientRepository.delete(
        ObjectId(patient_id)
    )

    await create_audit_log(
    user_id=patient_id,
    action="DELETE",
    module="PATIENT",
    module_id=patient_id,
    description="Patient deleted"
)

    if result.deleted_count == 0:
        return {"message": "Patient not found"}

    return {
        "message": "Patient deleted successfully"
    }