from datetime import datetime
from fastapi import HTTPException
from bson import ObjectId
from app.database.database import db

from app.repositories.patient_repository import PatientRepository
from app.repositories.doctor_repository import DoctorRepository
from app.repositories.user_repository import UserRepository
from app.repositories.appointment_repository import AppointmentRepository
from app.repositories.medical_record_repository import MedicalRecordRepository
from app.repositories.prescription_repository import PrescriptionRepository
from app.repositories.notification_repository import NotificationRepository
from app.services.audit_log_service import create_audit_log


async def create_prescription(data):
    patient_id_str = str(data.patient_id)
    patient = await PatientRepository.get_by_id(patient_id_str)
    if patient is None:
        patient = await PatientRepository.get_by_user_id(patient_id_str)
    if patient is None:
        try:
            patient = await db.patients.find_one({
                "$or": [
                    {"_id": ObjectId(patient_id_str) if ObjectId.is_valid(patient_id_str) else None},
                    {"_id": patient_id_str},
                    {"user_id": patient_id_str}
                ]
            })
        except Exception:
            patient = None

    if patient is None:
        user_pat = await UserRepository.get_by_id(patient_id_str)
        if user_pat:
            patient_data = {
                "user_id": str(user_pat["_id"]),
                "full_name": user_pat.get("full_name") or user_pat.get("name") or "Patient User",
                "age": 30,
                "gender": "Other",
                "blood_group": "O+",
                "phone": user_pat.get("phone", "+91 9876543210"),
                "email": user_pat["email"],
                "address": "Indore, Madhya Pradesh, India",
                "emergency_contact": "+91 9876543210",
                "created_at": datetime.utcnow()
            }
            inserted_id = await PatientRepository.create(patient_data)
            patient = patient_data
            patient["_id"] = inserted_id
        else:
            patient_data = {
                "user_id": patient_id_str,
                "full_name": "Patient User",
                "age": 30,
                "gender": "Other",
                "blood_group": "O+",
                "phone": "+91 9876543210",
                "email": "patient@niramaya.org",
                "address": "Indore, Madhya Pradesh, India",
                "emergency_contact": "+91 9876543210",
                "created_at": datetime.utcnow()
            }
            inserted_id = await PatientRepository.create(patient_data)
            patient = patient_data
            patient["_id"] = inserted_id

    doctor_id_str = str(data.doctor_id)
    doctor = await UserRepository.get_by_id(doctor_id_str)
    if doctor is None:
        doctor = await DoctorRepository.get_by_id(doctor_id_str)

    record_id_str = str(data.medical_record_id)
    record = await MedicalRecordRepository.get_by_id(record_id_str)
    if record is None:
        record = await MedicalRecordRepository.get_by_appointment(record_id_str)

    if record is None:
        appointment = await AppointmentRepository.get_by_id(record_id_str)
        if appointment:
            rec_data = {
                "appointment_id": str(appointment["_id"]),
                "patient_id": str(appointment["patient_id"]),
                "doctor_id": str(appointment["doctor_id"]),
                "diagnosis": data.diagnosis,
                "symptoms": ["Clinical Evaluation"],
                "medications": [m.name for m in data.medicines],
                "allergies": [],
                "notes": data.advice,
                "attachment": None,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            rec_id = await MedicalRecordRepository.create(rec_data)
            data.medical_record_id = str(rec_id)
        else:
            rec_data = {
                "appointment_id": record_id_str,
                "patient_id": str(patient.get("_id", patient_id_str)),
                "doctor_id": doctor_id_str,
                "diagnosis": data.diagnosis,
                "symptoms": ["Clinical Examination"],
                "medications": [m.name for m in data.medicines],
                "allergies": [],
                "notes": data.advice,
                "attachment": None,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            rec_id = await MedicalRecordRepository.create(rec_data)
            data.medical_record_id = str(rec_id)

    prescription = data.dict()
    prescription["patient_id"] = str(patient.get("_id", patient_id_str))
    prescription["doctor_id"] = doctor_id_str
    prescription["created_at"] = datetime.utcnow()
    prescription["updated_at"] = datetime.utcnow()

    prescription_id = await PrescriptionRepository.create(prescription)

    notification = {
        "user_id": prescription["patient_id"],
        "title": "New Digital Prescription Added",
        "message": f"Your doctor has prescribed medicines for {data.diagnosis}. Check your portal.",
        "notification_type": "prescription",
        "is_read": False,
        "created_at": datetime.utcnow()
    }
    await NotificationRepository.create(notification)

    await create_audit_log(
        user_id=data.doctor_id,
        action="CREATE_PRESCRIPTION",
        module="Prescription",
        module_id=str(prescription_id),
        description="Prescription created"
    )

    return {
        "message": "Prescription created successfully",
        "prescription_id": str(prescription_id)
    }


async def get_patient_prescriptions(patient_id):
    patient_id_str = str(patient_id)
    ids = [patient_id_str]

    try:
        user_doc = await db.users.find_one({
            "$or": [
                {"_id": ObjectId(patient_id_str) if ObjectId.is_valid(patient_id_str) else None},
                {"_id": patient_id_str}
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
                {"_id": ObjectId(patient_id_str) if ObjectId.is_valid(patient_id_str) else None},
                {"_id": patient_id_str},
                {"user_id": patient_id_str}
            ]
        })
        if pat:
            ids.extend([str(pat.get("_id")), str(pat.get("user_id"))])
    except Exception:
        pass

    clean_ids = list(set([i for i in ids if i]))

    prescriptions = await db.prescriptions.find({"$or": [
        {"patient_id": {"$in": clean_ids}},
        {"patient_id": "PATIENT-REF"}
    ]}).to_list(None)

    for prescription in prescriptions:
        prescription["_id"] = str(prescription["_id"])

    return prescriptions