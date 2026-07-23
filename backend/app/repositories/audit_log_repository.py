from datetime import datetime
from app.database.database import db


class AuditLogRepository:

    @staticmethod
    async def create(data):

        data["created_at"] = datetime.utcnow()

        result = await db.audit_logs.insert_one(data)

        return result.inserted_id


    @staticmethod
    async def get_all():

        return await db.audit_logs.find().sort(
            "created_at",
            -1
        ).to_list(None)