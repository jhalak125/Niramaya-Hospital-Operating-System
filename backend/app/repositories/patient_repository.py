from app.database.database import db
from bson import ObjectId


class PatientRepository:

    @staticmethod
    async def create(patient_data: dict):
        result = await db.patients.insert_one(patient_data)
        return result.inserted_id

    @staticmethod
    async def get_all():
        return await db.patients.find().to_list(length=None)

    @staticmethod
    async def update(patient_id, data):
        if ObjectId.is_valid(str(patient_id)):
            return await db.patients.update_one({"_id": ObjectId(patient_id)}, {"$set": data})
        return await db.patients.update_one({"$or": [{"_id": str(patient_id)}, {"user_id": str(patient_id)}]}, {"$set": data})

    @staticmethod
    async def delete(patient_id):
        if ObjectId.is_valid(str(patient_id)):
            return await db.patients.delete_one({"_id": ObjectId(patient_id)})
        return await db.patients.delete_one({"$or": [{"_id": str(patient_id)}, {"user_id": str(patient_id)}]})

    @staticmethod
    async def get_by_id(patient_id):
        if not patient_id:
            return None
        if ObjectId.is_valid(str(patient_id)):
            res = await db.patients.find_one({"_id": ObjectId(patient_id)})
            if res:
                return res
        return await db.patients.find_one({"$or": [{"_id": str(patient_id)}, {"user_id": str(patient_id)}]})

    @staticmethod
    async def get_by_bill(bill_id):
        return await db.payments.find_one({"bill_id": str(bill_id)})

    @staticmethod
    async def get_by_user_id(user_id):
        return await db.patients.find_one({"user_id": str(user_id)})