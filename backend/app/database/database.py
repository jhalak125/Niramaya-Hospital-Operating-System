from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings


client = AsyncIOMotorClient(
    settings.MONGODB_URL
)


db = client[
    settings.DATABASE_NAME
]


users_collection = db["users"]

patients_collection = db["patients"]

doctors_collection = db["doctors"]

appointments_collection = db["appointments"]

bills_collection = db["bills"]

payments_collection = db["payments"]

medical_records_collection = db["medical_records"]

lab_tests_collection = db["lab_tests"]

lab_reports_collection = db["lab_reports"]

notifications_collection = db["notifications"]