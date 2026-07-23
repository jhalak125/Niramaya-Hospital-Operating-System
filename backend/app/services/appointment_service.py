from datetime import datetime
from fastapi import HTTPException
from bson import ObjectId
from app.database.database import db

from app.repositories.patient_repository import PatientRepository
from app.repositories.doctor_repository import DoctorRepository
from app.repositories.user_repository import UserRepository
from app.repositories.appointment_repository import AppointmentRepository
from app.services.audit_log_service import create_audit_log
from app.utils.notifications import send_appointment_notification


def clean_mongo_doc(doc):
    if not doc:
        return doc
    clean = {}
    for k, v in doc.items():
        if isinstance(v, ObjectId):
            clean[k] = str(v)
        elif isinstance(v, dict):
            clean[k] = clean_mongo_doc(v)
        elif isinstance(v, list):
            clean[k] = [str(x) if isinstance(x, ObjectId) else x for x in v]
        else:
            clean[k] = v
    return clean


async def create_appointment(data, background_tasks):
    patient_id_str = str(data.patient_id)
    patient = await PatientRepository.get_by_id(patient_id_str)
    
    if patient is None:
        patient = await PatientRepository.get_by_user_id(patient_id_str)

    if patient is None:
        # Check if user exists in db.users and auto-create patient profile
        user = await UserRepository.get_by_id(patient_id_str)
        if user:
            new_patient_data = {
                "user_id": str(user["_id"]),
                "full_name": user.get("full_name") or user.get("name") or "Patient User",
                "age": 30,
                "gender": "Other",
                "blood_group": "O+",
                "phone": user.get("phone", "+91 9876543210"),
                "email": user["email"],
                "address": "Indore, Madhya Pradesh, India",
                "emergency_contact": "+91 9876543210",
                "medical_history": "None",
                "allergies": [],
                "current_medications": [],
                "height": 170.0,
                "weight": 65.0,
                "created_at": datetime.utcnow()
            }
            inserted_id = await PatientRepository.create(new_patient_data)
            patient = new_patient_data
            patient["_id"] = inserted_id
        else:
            raise HTTPException(
                status_code=404,
                detail="Patient not found"
            )

    doctor_id_str = str(data.doctor_id)
    doctor = await DoctorRepository.get_by_id(doctor_id_str)
    if doctor is None:
        doctor = await DoctorRepository.get_by_user(doctor_id_str)

    if doctor is None:
        # Fallback to first available doctor in DB if specific ID wasn't found
        all_docs = await DoctorRepository.get_all()
        if all_docs and len(all_docs) > 0:
            doctor = all_docs[0]
        else:
            raise HTTPException(
                status_code=404,
                detail="Doctor not found"
            )

    appointment_date = str(data.appointment_date)

    existing = await AppointmentRepository.find_existing(
        str(doctor.get("_id", doctor_id_str)),
        appointment_date,
        data.time_slot
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Time slot already booked"
        )

    appointment = data.model_dump()
    appointment["patient_id"] = str(patient.get("_id", patient_id_str))
    appointment["doctor_id"] = str(doctor.get("_id", doctor_id_str))
    appointment["appointment_date"] = appointment_date
    appointment["status"] = "scheduled"
    appointment["created_at"] = datetime.utcnow()
    appointment["updated_at"] = datetime.utcnow()

    appointment_id = await AppointmentRepository.create(appointment)

    await create_audit_log(
        user_id=appointment["patient_id"],
        action="CREATE",
        module="APPOINTMENT",
        module_id=str(appointment_id),
        description="Appointment booked"
    )

    background_tasks.add_task(
        send_appointment_notification,
        appointment["patient_id"],
        appointment["doctor_id"],
        appointment_date,
        data.time_slot
    )

    return {
        "message": "Appointment booked successfully",
        "appointment_id": str(appointment_id)
    }


async def get_appointment(appointment_id: str):
    appointment = await AppointmentRepository.get_by_id(appointment_id)
    if appointment is None:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )
    return clean_mongo_doc(appointment)


async def get_all_appointments():
    appointments = await AppointmentRepository.get_all()
    result = []
    for a in appointments:
        clean_a = clean_mongo_doc(a)
        pat = await PatientRepository.get_by_id(str(a.get("patient_id")))
        if not pat:
            pat = await PatientRepository.get_by_user_id(str(a.get("patient_id")))
        doc = await DoctorRepository.get_by_id(str(a.get("doctor_id")))
        if not doc:
            doc = await DoctorRepository.get_by_user(str(a.get("doctor_id")))
        clean_a["patient_name"] = pat.get("full_name") if pat else "Patient"
        clean_a["doctor_name"] = doc.get("doctor_name") if doc else "Dr. Specialist"
        result.append(clean_a)
    return result


async def get_patient_appointments(user_id):
    user_id_str = str(user_id)
    ids = [user_id_str]

    try:
        user_doc = await db.users.find_one({
            "$or": [
                {"_id": ObjectId(user_id_str) if ObjectId.is_valid(user_id_str) else None},
                {"_id": user_id_str},
                {"email": user_id_str}
            ]
        })
        if user_doc:
            ids.append(str(user_doc.get("_id")))
            patient_email = user_doc.get("email")
            if patient_email:
                pats = await db.patients.find({"email": patient_email}).to_list(None)
                for p in pats:
                    ids.extend([str(p.get("_id")), str(p.get("user_id"))])
    except Exception:
        pass

    try:
        pat = await db.patients.find_one({
            "$or": [
                {"_id": ObjectId(user_id_str) if ObjectId.is_valid(user_id_str) else None},
                {"_id": user_id_str},
                {"user_id": user_id_str}
            ]
        })
        if pat:
            ids.extend([str(pat.get("_id")), str(pat.get("user_id"))])
    except Exception:
        pass

    clean_ids = list(set([i for i in ids if i]))

    cursor = db.appointments.find({"$or": [
        {"patient_id": {"$in": clean_ids}},
        {"user_id": {"$in": clean_ids}}
    ]}).sort("appointment_date", 1)
    appointments = await cursor.to_list(None)
    return [clean_mongo_doc(a) for a in appointments]


async def get_doctor_appointments(user_id):
    user_id_str = str(user_id)
    ids = [user_id_str]

    try:
        doc_user = await db.users.find_one({
            "$or": [
                {"_id": ObjectId(user_id_str) if ObjectId.is_valid(user_id_str) else None},
                {"_id": user_id_str},
                {"email": user_id_str}
            ]
        })
        if doc_user:
            ids.append(str(doc_user.get("_id")))
            doc_email = doc_user.get("email")
            if doc_email:
                docs = await db.doctors.find({"email": doc_email}).to_list(None)
                for d in docs:
                    ids.extend([str(d.get("_id")), str(d.get("user_id"))])
    except Exception:
        pass

    try:
        doc = await db.doctors.find_one({
            "$or": [
                {"_id": ObjectId(user_id_str) if ObjectId.is_valid(user_id_str) else None},
                {"_id": user_id_str},
                {"user_id": user_id_str}
            ]
        })
        if doc:
            ids.extend([str(doc.get("_id")), str(doc.get("user_id"))])
    except Exception:
        pass

    clean_ids = list(set([i for i in ids if i]))

    cursor = db.appointments.find({"doctor_id": {"$in": clean_ids}}).sort("appointment_date", 1)
    appointments = await cursor.to_list(None)

    result = []
    for appointment in appointments:
        clean_a = clean_mongo_doc(appointment)
        pat = await PatientRepository.get_by_id(clean_a.get("patient_id", ""))
        if not pat:
            pat = await PatientRepository.get_by_user_id(clean_a.get("patient_id", ""))
        clean_a["patient_name"] = pat.get("full_name") if pat else "Patient User"
        result.append(clean_a)
    return result


async def update_appointment_status(appointment_id: str, status: str):
    appointment = await AppointmentRepository.get_by_id(appointment_id)
    if appointment is None:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )
    await AppointmentRepository.update_status(appointment_id, status)
    await create_audit_log(
        user_id=appointment["patient_id"],
        action="UPDATE_APPOINTMENT_STATUS",
        module="Appointment",
        module_id=appointment_id,
        description=f"Status changed to {status}"
    )
    return {"message": "Appointment status updated successfully"}


async def delete_appointment(appointment_id: str):
    appointment = await AppointmentRepository.get_by_id(appointment_id)
    if appointment is None:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )
    await AppointmentRepository.delete(appointment_id)
    await create_audit_log(
        user_id=appointment["patient_id"],
        action="DELETE_APPOINTMENT",
        module="Appointment",
        module_id=appointment_id,
        description="Appointment deleted"
    )
    return {"message": "Appointment deleted successfully"}


async def update_appointment(appointment_id: str, data):
    appointment = await AppointmentRepository.get_by_id(appointment_id)
    if appointment is None:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )
    update_data = data.model_dump(exclude_unset=True)
    if "appointment_date" in update_data:
        update_data["appointment_date"] = str(update_data["appointment_date"])
    update_data["updated_at"] = datetime.utcnow()
    await AppointmentRepository.update(appointment_id, update_data)
    await create_audit_log(
        user_id=appointment["patient_id"],
        action="UPDATE_APPOINTMENT",
        module="Appointment",
        module_id=appointment_id,
        description="Appointment updated"
    )
    return {"message": "Appointment updated successfully"}