from bson import ObjectId

from app.database.database import db


class MedicalRecordRepository:

    @staticmethod
    async def create(data):
        result = await db.medical_records.insert_one(data)
        return result.inserted_id

    @staticmethod
    async def get_by_patient(patient_id):
        return await db.medical_records.find(
            {
                "patient_id": patient_id
            }
        ).to_list(None)

    @staticmethod
    async def get_by_doctor(doctor_id):
        return await db.medical_records.find(
            {
                "doctor_id": doctor_id
            }
        ).to_list(None)

    @staticmethod
    async def get_by_appointment(appointment_id):
        return await db.medical_records.find_one(
            {
                "appointment_id": appointment_id
            }
        )

    @staticmethod
    async def get_by_id(record_id):
        return await db.medical_records.find_one(
            {
                "_id": ObjectId(record_id)
            }
        )

    @staticmethod
    async def delete(record_id):
        return await db.medical_records.delete_one(
            {
                "_id": ObjectId(record_id)
            }
        )
    
    @staticmethod
    async def search(
        patient_id=None,
        doctor_id=None,
        diagnosis=None,
        page=1,
        limit=10,
        sort_by=None,
        order="asc"
    ):

        query = {}

        if patient_id:
            query["patient_id"] = patient_id

        if doctor_id:
            query["doctor_id"] = doctor_id

        if diagnosis:
            query["diagnosis"] = {
                "$regex": diagnosis,
                "$options": "i"
            }

        cursor = db.medical_records.find(query)

        if sort_by:

            direction = 1 if order == "asc" else -1

            cursor = cursor.sort(
                sort_by,
                direction
            )

        cursor = cursor.skip(
            (page - 1) * limit
        ).limit(limit)

        return await cursor.to_list(limit)