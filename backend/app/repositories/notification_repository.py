from app.database.database import db
from bson import ObjectId


class NotificationRepository:

    @staticmethod
    async def create(data):
        result = await db.notifications.insert_one(data)
        return result.inserted_id

    @staticmethod
    async def get_by_user(user_id):
        ids = [str(user_id)]
        try:
            is_valid_obj = ObjectId.is_valid(str(user_id))
            query_filter = {"$or": [{"user_id": str(user_id)}]}
            if is_valid_obj:
                query_filter["$or"].append({"_id": ObjectId(user_id)})

            patient = await db.patients.find_one(query_filter)
            if patient:
                ids.extend([str(patient.get("_id")), str(patient.get("user_id"))])

            doctor = await db.doctors.find_one(query_filter)
            if doctor:
                ids.extend([str(doctor.get("_id")), str(doctor.get("user_id"))])
        except Exception:
            pass

        clean_ids = list(set([i for i in ids if i]))
        return await db.notifications.find({"user_id": {"$in": clean_ids}}).sort("created_at", -1).to_list(None)

    @staticmethod
    async def mark_as_read(notification_id):
        if ObjectId.is_valid(str(notification_id)):
            await db.notifications.update_one({"_id": ObjectId(notification_id)}, {"$set": {"is_read": True}})
        else:
            await db.notifications.update_one({"_id": str(notification_id)}, {"$set": {"is_read": True}})

    @staticmethod
    async def delete(notification_id):
        if ObjectId.is_valid(str(notification_id)):
            await db.notifications.delete_one({"_id": ObjectId(notification_id)})
        else:
            await db.notifications.delete_one({"_id": str(notification_id)})