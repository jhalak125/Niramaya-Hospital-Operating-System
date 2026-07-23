from datetime import datetime
from fastapi import HTTPException
import os
import shutil
from uuid import uuid4
from bson import ObjectId
from app.database.database import db

from app.repositories.lab_test_repository import LabTestRepository
from app.repositories.lab_report_repository import LabReportRepository
from app.repositories.appointment_repository import AppointmentRepository
from app.repositories.notification_repository import NotificationRepository
from app.services.audit_log_service import create_audit_log

from app.config import settings

UPLOAD_DIR = "uploads/lab_reports"
os.makedirs(UPLOAD_DIR, exist_ok=True)


async def create_lab_report(data, file):
    lab_test_id_str = str(data.lab_test_id)
    lab_test = await LabTestRepository.get_by_id(lab_test_id_str)
    patient_id_for_report = None

    if lab_test:
        patient_id_for_report = str(lab_test.get("patient_id"))
    else:
        appointment = await AppointmentRepository.get_by_id(lab_test_id_str)
        if appointment:
            patient_id_for_report = str(appointment["patient_id"])
            lt_data = {
                "appointment_id": str(appointment["_id"]),
                "patient_id": patient_id_for_report,
                "doctor_id": str(appointment["doctor_id"]),
                "tests": ["Diagnostic Lab Test"],
                "notes": data.notes or "Diagnostic evaluation",
                "status": "Completed",
                "created_at": datetime.utcnow()
            }
            lt_id = await LabTestRepository.create(lt_data)
            data.lab_test_id = str(lt_id)
        else:
            patient_id_for_report = "PATIENT-REF"

    report_file = None
    if file:
        extension = file.filename.split(".")[-1]
        filename = f"{uuid4()}.{extension}"
        filepath = os.path.join(UPLOAD_DIR, filename)
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        report_file = filename

    report = data.dict()
    report["patient_id"] = patient_id_for_report
    report["doctor_id"] = str(lab_test.get("doctor_id", "DOCTOR-REF")) if lab_test else "DOCTOR-REF"
    report["report_file"] = report_file
    report["created_at"] = datetime.utcnow()
    report["updated_at"] = datetime.utcnow()

    report_id = await LabReportRepository.create(report)

    await create_audit_log(
        user_id=report["doctor_id"],
        action="UPLOAD_LAB_REPORT",
        module="LabReport",
        module_id=str(report_id),
        description="Lab report uploaded"
    )

    await LabTestRepository.update_status(data.lab_test_id, "Completed")

    notification = {
        "user_id": report["patient_id"],
        "title": "Lab Report Uploaded",
        "message": f"Your diagnostic lab report results ({data.result[:40]}...) are ready.",
        "notification_type": "lab_report",
        "is_read": False,
        "created_at": datetime.utcnow()
    }
    await NotificationRepository.create(notification)

    return {
        "message": "Lab report uploaded successfully",
        "report_id": str(report_id)
    }


async def get_patient_reports(patient_id):
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

    try:
        appts = await db.appointments.find({"patient_id": {"$in": clean_ids}}).to_list(None)
        for a in appts:
            clean_ids.extend([str(a.get("_id")), str(a.get("patient_id"))])
    except Exception:
        pass

    clean_ids = list(set([i for i in clean_ids if i]))

    reports = await db.lab_reports.find({"$or": [
        {"patient_id": {"$in": clean_ids}},
        {"lab_test_id": {"$in": clean_ids}},
        {"patient_id": "PATIENT-REF"}
    ]}).to_list(None)

    cleaned_reports = []
    base_domain = settings.BASE_URL.rstrip("/")
    for report in reports:
        report["_id"] = str(report["_id"])
        if report.get("report_file"):
            rf = report["report_file"]
            if rf.startswith("http://") or rf.startswith("https://"):
                report["report_url"] = rf
            else:
                report["report_url"] = f"{base_domain}/uploads/lab_reports/{rf}"
        cleaned_reports.append(report)

    return cleaned_reports