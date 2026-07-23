from app.database.database import db
from bson import ObjectId
from datetime import datetime

class AppointmentRepository:

    @staticmethod
    async def create(data):
        result = await db.appointments.insert_one(data)
        return result.inserted_id

    @staticmethod
    async def find_existing(doctor_id, appointment_date, time_slot):
        return await db.appointments.find_one(
            {
                "doctor_id": str(doctor_id),
                "appointment_date": appointment_date,
                "time_slot": time_slot,
                "status": "scheduled"
            }
        )

    @staticmethod
    async def get_by_id(appointment_id):
        if not appointment_id:
            return None
        if ObjectId.is_valid(str(appointment_id)):
            res = await db.appointments.find_one({"_id": ObjectId(appointment_id)})
            if res:
                return res
        return await db.appointments.find_one({"_id": str(appointment_id)})

    @staticmethod
    async def get_by_patient(patient_id):
        cursor = db.appointments.find({"patient_id": str(patient_id)}).sort("appointment_date", 1)
        return await cursor.to_list(None)

    @staticmethod
    async def get_by_doctor(doctor_id):
        cursor = db.appointments.find({"doctor_id": str(doctor_id)}).sort("appointment_date", 1)
        return await cursor.to_list(None)

    @staticmethod
    async def update_status(appointment_id, status):
        if ObjectId.is_valid(str(appointment_id)):
            return await db.appointments.update_one({"_id": ObjectId(appointment_id)}, {"$set": {"status": status, "updated_at": datetime.utcnow()}})
        return await db.appointments.update_one({"_id": str(appointment_id)}, {"$set": {"status": status, "updated_at": datetime.utcnow()}})

    @staticmethod
    async def get_all():
        return await db.appointments.find().to_list(None)

    @staticmethod
    async def update(appointment_id, data):
        if ObjectId.is_valid(str(appointment_id)):
            return await db.appointments.update_one({"_id": ObjectId(appointment_id)}, {"$set": data})
        return await db.appointments.update_one({"_id": str(appointment_id)}, {"$set": data})

    @staticmethod
    async def delete(appointment_id):
        if ObjectId.is_valid(str(appointment_id)):
            return await db.appointments.delete_one({"_id": ObjectId(appointment_id)})
        return await db.appointments.delete_one({"_id": str(appointment_id)})