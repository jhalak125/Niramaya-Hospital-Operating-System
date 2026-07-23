from app.database.database import db
from bson import ObjectId


class DoctorRepository:

    @staticmethod
    async def create(data):
        result = await db.doctors.insert_one(data)
        return result.inserted_id

    @staticmethod
    async def get_by_user(user_id):
        return await db.doctors.find_one({"user_id": str(user_id)})

    @staticmethod
    async def get_all():
        return await db.doctors.find().to_list(None)

    @staticmethod
    async def search(filters, skip, limit, sort_field=None, sort_order=1):
        cursor = db.doctors.find(filters)
        if sort_field:
            cursor = cursor.sort(sort_field, sort_order)
        cursor = cursor.skip(skip).limit(limit)
        return await cursor.to_list(length=limit)

    @staticmethod
    async def get_by_department(department: str):
        cursor = db.doctors.find({"department": department, "status": "available"})
        return await cursor.to_list(None)

    @staticmethod
    async def get_by_id(doctor_id):
        if not doctor_id:
            return None
        if ObjectId.is_valid(str(doctor_id)):
            res = await db.doctors.find_one({"_id": ObjectId(doctor_id)})
            if res:
                return res
        return await db.doctors.find_one({"$or": [{"_id": str(doctor_id)}, {"user_id": str(doctor_id)}]})

    @staticmethod
    async def update(doctor_id, data):
        if ObjectId.is_valid(str(doctor_id)):
            return await db.doctors.update_one({"_id": ObjectId(doctor_id)}, {"$set": data})
        return await db.doctors.update_one({"$or": [{"_id": str(doctor_id)}, {"user_id": str(doctor_id)}]}, {"$set": data})

    @staticmethod
    async def delete(doctor_id):
        if ObjectId.is_valid(str(doctor_id)):
            return await db.doctors.delete_one({"_id": ObjectId(doctor_id)})
        return await db.doctors.delete_one({"$or": [{"_id": str(doctor_id)}, {"user_id": str(doctor_id)}]})