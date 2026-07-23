from bson import ObjectId
from app.database.database import db


class UserRepository:

    @staticmethod
    async def get_by_id(user_id):
        if not user_id:
            return None
        if ObjectId.is_valid(str(user_id)):
            res = await db.users.find_one({"_id": ObjectId(user_id)})
            if res:
                return res
        return await db.users.find_one({"$or": [{"_id": str(user_id)}, {"email": str(user_id)}]})

    @staticmethod
    async def get_by_email(email):
        if not email:
            return None
        clean_email = email.strip()
        return await db.users.find_one({"email": {"$regex": f"^{clean_email}$", "$options": "i"}})

    @staticmethod
    async def create_google_user(email, name):
        user = {
            "name": name,
            "email": email.strip().lower(),
            "password": None,
            "provider": "google",
            "role": "patient"
        }
        result = await db.users.insert_one(user)
        user["_id"] = result.inserted_id
        return user