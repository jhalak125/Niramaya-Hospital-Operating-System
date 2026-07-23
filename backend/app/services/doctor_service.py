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
    doctors = await DoctorRepository.get_by_department(department)
    result = []
    for doctor in doctors:
        user = await UserRepository.get_by_id(doctor["user_id"])
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
    user = await UserRepository.get_by_id(doctor["user_id"])
    doctor["_id"] = str(doctor["_id"])
    doctor["doctor_name"] = user["full_name"] if user else doctor.get("doctor_name", "Dr. Specialist")
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


async def get_all_doctors():
    doctors = await DoctorRepository.get_all()
    result = []
    for doctor in doctors:
        user = await UserRepository.get_by_id(doctor["user_id"])
        doctor["_id"] = str(doctor["_id"])
        doctor["doctor_name"] = user["full_name"] if user else doctor.get("doctor_name", "Dr. Specialist")
        result.append(doctor)
    return result