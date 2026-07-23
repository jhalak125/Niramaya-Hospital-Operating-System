from bson import ObjectId
from app.database.database import db


class LabReportRepository:

    @staticmethod
    async def create(data):
        result = await db.lab_reports.insert_one(data)
        return result.inserted_id

    @staticmethod
    async def get_by_id(report_id):
        return await db.lab_reports.find_one(
            {
                "_id": ObjectId(report_id)
            }
        )

    @staticmethod
    async def get_by_lab_test(lab_test_id):
        return await db.lab_reports.find_one(
            {
                "lab_test_id": lab_test_id
            }
        )

    @staticmethod
    async def get_by_patient(patient_id):
        return await db.lab_reports.find(
            {
                "patient_id": patient_id
            }
        ).to_list(None)