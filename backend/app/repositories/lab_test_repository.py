from bson import ObjectId
from app.database.database import db


class LabTestRepository:

    @staticmethod
    async def create(data):
        result = await db.lab_tests.insert_one(data)
        return result.inserted_id

    @staticmethod
    async def get_by_id(lab_test_id):
        return await db.lab_tests.find_one(
            {
                "_id": ObjectId(lab_test_id)
            }
        )

    @staticmethod
    async def get_by_appointment(appointment_id):
        return await db.lab_tests.find_one(
            {
                "appointment_id": appointment_id
            }
        )

    @staticmethod
    async def get_by_patient(patient_id):
        return await db.lab_tests.find(
            {
                "patient_id": patient_id
            }
        ).to_list(None)
    
    @staticmethod
    async def update_status(lab_test_id, status):

        await db.lab_tests.update_one(
            {
                "_id": ObjectId(lab_test_id)
            },
            {
                "$set": {
                    "status": status
                }
            }
        )

    @staticmethod
    async def search(
        patient_id=None,
        doctor_id=None,
        status=None,
        test_name=None,
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

        if status:
            query["status"] = status

        if test_name:
            query["test_name"] = {
                "$regex": test_name,
                "$options": "i"
            }

        cursor = db.lab_tests.find(query)

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