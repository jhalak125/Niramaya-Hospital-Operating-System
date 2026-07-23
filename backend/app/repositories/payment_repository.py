from app.database.database import db
from bson import ObjectId


class PaymentRepository:

    @staticmethod
    async def create(data):
        result = await db.payments.insert_one(data)
        return result.inserted_id

    @staticmethod
    async def get_by_bill(bill_id):
        return await db.payments.find_one({"bill_id": str(bill_id)})

    @staticmethod
    async def get_by_id(payment_id):
        if not payment_id:
            return None
        if ObjectId.is_valid(str(payment_id)):
            res = await db.payments.find_one({"_id": ObjectId(payment_id)})
            if res:
                return res
        return await db.payments.find_one({"$or": [{"_id": str(payment_id)}, {"transaction_id": str(payment_id)}]})

    @staticmethod
    async def verify(payment_id):
        if ObjectId.is_valid(str(payment_id)):
            await db.payments.update_one({"_id": ObjectId(payment_id)}, {"$set": {"status": "Paid"}})
        else:
            await db.payments.update_one({"$or": [{"_id": str(payment_id)}, {"transaction_id": str(payment_id)}]}, {"$set": {"status": "Paid"}})