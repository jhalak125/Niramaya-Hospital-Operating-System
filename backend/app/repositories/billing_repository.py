from app.database.database import bills_collection
from bson import ObjectId


class BillingRepository:

    @staticmethod
    async def create(data):
        result = await bills_collection.bills.insert_one(data)
        return result.inserted_id

    @staticmethod
    async def get_by_patient(patient_id):
        cursor = bills_collection.bills.find({"patient_id": str(patient_id)})
        return await cursor.to_list(None)

    @staticmethod
    async def get_by_id(bill_id):
        if not bill_id:
            return None
        if ObjectId.is_valid(str(bill_id)):
            res = await bills_collection.bills.find_one({"_id": ObjectId(bill_id)})
            if res:
                return res
        return await bills_collection.bills.find_one({"$or": [{"_id": str(bill_id)}, {"bill_id": str(bill_id)}]})

    @staticmethod
    async def get_all():
        cursor = bills_collection.bills.find({})
        bills = await cursor.to_list(None)
        for b in bills:
            b["_id"] = str(b["_id"])
        return bills

    @staticmethod
    async def mark_paid(bill_id):
        if ObjectId.is_valid(str(bill_id)):
            await bills_collection.bills.update_one({"_id": ObjectId(bill_id)}, {"$set": {"payment_status": "Paid"}})
        else:
            await bills_collection.bills.update_one({"$or": [{"_id": str(bill_id)}, {"bill_id": str(bill_id)}]}, {"$set": {"payment_status": "Paid"}})