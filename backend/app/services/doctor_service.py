from datetime import datetime
from fastapi import HTTPException
from bson import ObjectId
from app.database.database import db

from app.repositories.user_repository import UserRepository
from app.repositories.doctor_repository import DoctorRepository
from app.auth.security import hash_password


async def create_doctor(data):
    user_id_str = data.user_id
    user = None
    if user_id_str:
        user = await UserRepository.get_by_id(user_id_str)
        if not user:
            try:
                user = await db.users.find_one({"$or": [{"_id": ObjectId(user_id_str) if ObjectId.is_valid(user_id_str) else None}, {"email": user_id_str}]})
            except Exception:
                user = None

    if user is None:
        # Create a new user profile for doctor automatically
        doc_email = f"doc_{int(datetime.utcnow().timestamp())}@niramaya.org" if not user_id_str or '@' not in str(user_id_str) else user_id_str
        doc_name = data.doctor_name or f"Dr. {data.specialization}"
        user_data = {
            "email": doc_email,
            "password": hash_password("password123"),
            "full_name": doc_name,
            "role": "doctor",
            "phone": "+91 9876543210",
            "is_active": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        res = await db.users.insert_one(user_data)
        user_id_str = str(res.inserted_id)
        data.user_id = user_id_str
        user_data["_id"] = user_id_str
        user = user_data
    else:
        user_id_str = str(user["_id"])
        data.user_id = user_id_str

    doctor = data.dict()
    doctor["user_id"] = user_id_str
    doctor["doctor_name"] = data.doctor_name or user.get("full_name") or "Dr. Specialist"
    doctor["created_at"] = datetime.utcnow()
    doctor["updated_at"] = datetime.utcnow()

    doctor_id = await DoctorRepository.create(doctor)

    return {
        "message": "Doctor profile created successfully",
        "doctor_id": str(doctor_id)
    }


async def search_doctors(
    department=None,
    specialization=None,
    status=None,
    min_experience=None,
    page=1,
    limit=10,
    sort_by=None,
    order="asc"
):
    filters = {}
    if department:
        filters["department"] = department
    if specialization:
        filters["specialization"] = specialization
    if status:
        filters["status"] = status
    if min_experience is not None:
        filters["experience"] = {"$gte": min_experience}

    skip = (page - 1) * limit
    sort_order = 1 if order == "asc" else -1

    doctors = await DoctorRepository.search(
        filters,
        skip,
        limit,
        sort_by,
        sort_order
    )
    return doctors


async def get_department_doctors(department):
    try:
        doctors = await DoctorRepository.get_by_department(department)
    except Exception:
        doctors = []

    if not doctors:
        dept_fallbacks = [
            d for d in DEFAULT_DOCTORS_DATA
            if d.get("department", "").lower() == department.lower()
        ]
        return [
            {
                "doctor_name": d["doctor_name"],
                "specialization": d["specialization"],
                "experience": f'{d["experience"]} Years',
                "consultation_fee": d["consultation_fee"],
                "available_time": f'{d.get("start_time", "09:00 AM")} - {d.get("end_time", "05:00 PM")}',
                "working_days": d.get("working_days", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]),
                "department": d["department"]
            }
            for d in dept_fallbacks
        ]

    result = []
    for doctor in doctors:
        user = None
        try:
            user = await UserRepository.get_by_id(doctor.get("user_id"))
        except Exception:
            pass
        result.append({
            "doctor_name": user["full_name"] if user else doctor.get("doctor_name", "Dr. Specialist"),
            "specialization": doctor["specialization"],
            "experience": f'{doctor["experience"]} Years',
            "consultation_fee": doctor["consultation_fee"],
            "available_time": f'{doctor.get("start_time", "09:00 AM")} - {doctor.get("end_time", "05:00 PM")}',
            "working_days": doctor.get("working_days", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]),
            "department": doctor["department"]
        })
    return result


async def get_doctor(doctor_id: str):
    doctor = await DoctorRepository.get_by_id(doctor_id)
    if doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    user = None
    try:
        user = await UserRepository.get_by_id(doctor["user_id"])
    except Exception:
        pass
    doctor["_id"] = str(doctor["_id"])
    doctor["doctor_name"] = (
        (user["full_name"] if user else None)
        or doctor.get("doctor_name")
        or f"Dr. {doctor.get('specialization', 'Specialist')}"
    )
    return doctor


async def update_doctor(doctor_id, data):
    doctor = await DoctorRepository.get_by_id(doctor_id)
    if doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    update_data = data.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    await DoctorRepository.update(doctor_id, update_data)
    return {"message": "Doctor updated successfully"}


async def delete_doctor(doctor_id):
    doctor = await DoctorRepository.get_by_id(doctor_id)
    if doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    await DoctorRepository.delete(doctor_id)
    return {"message": "Doctor deleted successfully"}


DEFAULT_DOCTORS_DATA = [
    {
        "_id": "doc_cardio_01",
        "user_id": "user_cardio_01",
        "doctor_name": "Dr. Priya Sharma",
        "department": "Cardiology",
        "specialization": "Interventional Cardiologist",
        "qualification": "MBBS, MD, DM (Cardiology)",
        "experience": 12,
        "consultation_fee": 1500.0,
        "working_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "start_time": "09:00 AM",
        "end_time": "05:00 PM",
        "status": "available",
    },
    {
        "_id": "doc_neuro_02",
        "user_id": "user_neuro_02",
        "doctor_name": "Dr. Rahul Mehta",
        "department": "Neurology",
        "specialization": "Neurologist",
        "qualification": "MBBS, MD, DM (Neurology)",
        "experience": 10,
        "consultation_fee": 1800.0,
        "working_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "start_time": "10:00 AM",
        "end_time": "06:00 PM",
        "status": "available",
    },
    {
        "_id": "doc_pedia_03",
        "user_id": "user_pedia_03",
        "doctor_name": "Dr. Ananya Krishnan",
        "department": "Pediatrics",
        "specialization": "Pediatrician",
        "qualification": "MBBS, MD (Pediatrics)",
        "experience": 8,
        "consultation_fee": 1000.0,
        "working_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Saturday"],
        "start_time": "09:00 AM",
        "end_time": "04:00 PM",
        "status": "available",
    },
    {
        "_id": "doc_ortho_04",
        "user_id": "user_ortho_04",
        "doctor_name": "Dr. Vikram Singh",
        "department": "Orthopedics",
        "specialization": "Orthopedic Surgeon",
        "qualification": "MBBS, MS (Orthopedics)",
        "experience": 15,
        "consultation_fee": 2000.0,
        "working_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "start_time": "08:00 AM",
        "end_time": "04:00 PM",
        "status": "available",
    },
    {
        "_id": "doc_derma_05",
        "user_id": "user_derma_05",
        "doctor_name": "Dr. Neha Gupta",
        "department": "Dermatology",
        "specialization": "Dermatologist",
        "qualification": "MBBS, MD (Dermatology)",
        "experience": 7,
        "consultation_fee": 1200.0,
        "working_days": ["Monday", "Wednesday", "Friday", "Saturday"],
        "start_time": "10:00 AM",
        "end_time": "05:00 PM",
        "status": "available",
    },
    {
        "_id": "doc_genmed_06",
        "user_id": "user_genmed_06",
        "doctor_name": "Dr. Arjun Patel",
        "department": "General Medicine",
        "specialization": "General Physician",
        "qualification": "MBBS, MD (General Medicine)",
        "experience": 9,
        "consultation_fee": 800.0,
        "working_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
        "start_time": "09:00 AM",
        "end_time": "07:00 PM",
        "status": "available",
    },
    {
        "_id": "doc_gyn_07",
        "user_id": "user_gyn_07",
        "doctor_name": "Dr. Sunita Rao",
        "department": "Gynecology",
        "specialization": "Gynecologist & Obstetrician",
        "qualification": "MBBS, MS (OBG)",
        "experience": 11,
        "consultation_fee": 1500.0,
        "working_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "start_time": "09:00 AM",
        "end_time": "05:00 PM",
        "status": "available",
    },
    {
        "_id": "doc_psych_08",
        "user_id": "user_psych_08",
        "doctor_name": "Dr. Karthik Nair",
        "department": "Psychiatry",
        "specialization": "Psychiatrist",
        "qualification": "MBBS, MD (Psychiatry)",
        "experience": 6,
        "consultation_fee": 2000.0,
        "working_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "start_time": "10:00 AM",
        "end_time": "06:00 PM",
        "status": "available",
    },
]


async def get_all_doctors():
    try:
        doctors = await DoctorRepository.get_all()
    except Exception as e:
        print(f"Database error in get_all_doctors: {e}")
        doctors = []

    if not doctors:
        return DEFAULT_DOCTORS_DATA

    result = []
    for doctor in doctors:
        user = None
        try:
            user = await UserRepository.get_by_id(doctor.get("user_id"))
        except Exception:
            pass
        doctor["_id"] = str(doctor["_id"])
        doctor["doctor_name"] = (
            (user["full_name"] if user else None)
            or doctor.get("doctor_name")
            or f"Dr. {doctor.get('specialization', 'Specialist')}"
        )
        result.append(doctor)
    return result if result else DEFAULT_DOCTORS_DATA