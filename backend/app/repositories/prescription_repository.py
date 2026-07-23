from bson import ObjectId
from app.database.database import db

class PrescriptionRepository:

    @staticmethod
    async def create(data):
        result = await db.prescriptions.insert_one(data)
        return result.inserted_id

    @staticmethod
    async def get_by_patient(patient_id):
        return await db.prescriptions.find(
            {
                "patient_id": patient_id
            }
        ).to_list(None)

    @staticmethod
    async def get_by_id(prescription_id):
        return await db.prescriptions.find_one(
            {
                "_id": ObjectId(prescription_id)
            }
        )
    
    @staticmethod
    async def get_by_medical_record(medical_record_id):
        return await db.prescriptions.find_one(
            {
                "medical_record_id": medical_record_id
            }
        )