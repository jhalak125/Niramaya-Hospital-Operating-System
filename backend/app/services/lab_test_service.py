from datetime import datetime
from fastapi import HTTPException

from app.repositories.appointment_repository import AppointmentRepository
from app.repositories.lab_test_repository import LabTestRepository
from app.services.audit_log_service import create_audit_log


async def create_lab_test(data):

    appointment = await AppointmentRepository.get_by_id(
        data.appointment_id
    )

    if appointment is None:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    existing = await LabTestRepository.get_by_appointment(
        data.appointment_id
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Lab test already exists for this appointment"
        )

    lab_test = data.dict()

    lab_test["patient_id"] = appointment["patient_id"]

    lab_test["doctor_id"] = appointment["doctor_id"]

    lab_test["status"] = "Pending"

    lab_test["created_at"] = datetime.utcnow()

    lab_test["updated_at"] = datetime.utcnow()

    lab_test_id = await LabTestRepository.create(
        lab_test
    )

    await create_audit_log(
    user_id=appointment["doctor_id"],
    action="CREATE_LAB_TEST",
    module="LabTest",
    module_id=str(lab_test_id),
    description="Lab test ordered"
)

    return {
        "message": "Lab test created successfully",
        "lab_test_id": str(lab_test_id)
    }


async def get_patient_lab_tests(patient_id):

    lab_tests = await LabTestRepository.get_by_patient(
        patient_id
    )

    for test in lab_tests:
        test["_id"] = str(test["_id"])

    return lab_tests

async def search_lab_tests(
    patient_id=None,
    doctor_id=None,
    status=None,
    test_name=None,
    page=1,
    limit=10,
    sort_by=None,
    order="asc"
):

    lab_tests = await LabTestRepository.search(
        patient_id,
        doctor_id,
        status,
        test_name,
        page,
        limit,
        sort_by,
        order
    )

    for test in lab_tests:

        test["_id"] = str(test["_id"])

    return lab_tests