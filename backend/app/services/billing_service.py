from datetime import datetime
from fastapi import HTTPException

from app.repositories.patient_repository import PatientRepository
from app.repositories.appointment_repository import AppointmentRepository
from app.repositories.billing_repository import BillingRepository
from app.services.audit_log_service import create_audit_log


async def create_bill(data):

    # Check patient exists
    patient = await PatientRepository.get_by_id(
        data.patient_id
    )

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    # Check appointment exists
    appointment = await AppointmentRepository.get_by_id(
        data.appointment_id
    )

    if appointment is None:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    # Calculate total amount
    total_amount = (
        data.consultation_fee
        + data.medicine_cost
        + data.test_cost
        + data.other_charges
    )

    bill = data.dict()

    bill["total_amount"] = total_amount
    bill["payment_status"] = "Pending"

    bill["created_at"] = datetime.utcnow()
    bill["updated_at"] = datetime.utcnow()

    bill_id = await BillingRepository.create(bill)

    await create_audit_log(
    user_id=data.patient_id,
    action="GENERATE_BILL",
    module="Bill",
    module_id=str(bill_id),
    description="Bill generated"
)

    return {
        "message": "Bill generated successfully",
        "bill_id": str(bill_id)
    }


async def get_patient_bills(patient_id):

    patient = await PatientRepository.get_by_id(
        patient_id
    )

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return await BillingRepository.get_by_patient(
        patient_id
    )


async def get_all_bills():
    from app.repositories.user_repository import UserRepository
    bills = await BillingRepository.get_all()
    for bill in bills:
        patient_name = "Patient"
        pid = bill.get("patient_id")
        if pid:
            pat = await PatientRepository.get_by_id(pid)
            if pat:
                patient_name = pat.get("full_name") or pat.get("name") or "Patient"
            else:
                user = await UserRepository.get_by_id(pid)
                if user:
                    patient_name = user.get("full_name") or user.get("name") or "Patient"
        bill["patient_name"] = patient_name
    return bills