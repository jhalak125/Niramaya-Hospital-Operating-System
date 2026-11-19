import asyncio
import os
import sys
from datetime import datetime
from pathlib import Path

# Load .env from the same directory as this script
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env")

from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext

MONGODB_URL = os.getenv("MONGODB_URL") or "mongodb://localhost:27017"
DATABASE_NAME = os.getenv("DATABASE_NAME") or "hospital_db"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

DOCTORS_SEED = [
    {
        "user": {"full_name": "Dr. Priya Sharma", "email": "dr.priya.sharma@niramaya.org", "role": "doctor", "phone": "+91 9876500001"},
        "doctor": {"department": "Cardiology", "specialization": "Interventional Cardiologist", "qualification": "MBBS, MD, DM (Cardiology)", "experience": 12, "consultation_fee": 1500.0, "working_days": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "start_time": "09:00 AM", "end_time": "05:00 PM", "status": "available"}
    },
    {
        "user": {"full_name": "Dr. Rahul Mehta", "email": "dr.rahul.mehta@niramaya.org", "role": "doctor", "phone": "+91 9876500002"},
        "doctor": {"department": "Neurology", "specialization": "Neurologist", "qualification": "MBBS, MD, DM (Neurology)", "experience": 10, "consultation_fee": 1800.0, "working_days": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "start_time": "10:00 AM", "end_time": "06:00 PM", "status": "available"}
    },
    {
        "user": {"full_name": "Dr. Ananya Krishnan", "email": "dr.ananya.krishnan@niramaya.org", "role": "doctor", "phone": "+91 9876500003"},
        "doctor": {"department": "Pediatrics", "specialization": "Pediatrician", "qualification": "MBBS, MD (Pediatrics)", "experience": 8, "consultation_fee": 1000.0, "working_days": ["Monday","Tuesday","Wednesday","Thursday","Saturday"], "start_time": "09:00 AM", "end_time": "04:00 PM", "status": "available"}
    },
    {
        "user": {"full_name": "Dr. Vikram Singh", "email": "dr.vikram.singh@niramaya.org", "role": "doctor", "phone": "+91 9876500004"},
        "doctor": {"department": "Orthopedics", "specialization": "Orthopedic Surgeon", "qualification": "MBBS, MS (Orthopedics)", "experience": 15, "consultation_fee": 2000.0, "working_days": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "start_time": "08:00 AM", "end_time": "04:00 PM", "status": "available"}
    },
    {
        "user": {"full_name": "Dr. Neha Gupta", "email": "dr.neha.gupta@niramaya.org", "role": "doctor", "phone": "+91 9876500005"},
        "doctor": {"department": "Dermatology", "specialization": "Dermatologist", "qualification": "MBBS, MD (Dermatology)", "experience": 7, "consultation_fee": 1200.0, "working_days": ["Monday","Wednesday","Friday","Saturday"], "start_time": "10:00 AM", "end_time": "05:00 PM", "status": "available"}
    },
    {
        "user": {"full_name": "Dr. Arjun Patel", "email": "dr.arjun.patel@niramaya.org", "role": "doctor", "phone": "+91 9876500006"},
        "doctor": {"department": "General Medicine", "specialization": "General Physician", "qualification": "MBBS, MD (General Medicine)", "experience": 9, "consultation_fee": 800.0, "working_days": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"], "start_time": "09:00 AM", "end_time": "07:00 PM", "status": "available"}
    },
    {
        "user": {"full_name": "Dr. Sunita Rao", "email": "dr.sunita.rao@niramaya.org", "role": "doctor", "phone": "+91 9876500007"},
        "doctor": {"department": "Gynecology", "specialization": "Gynecologist & Obstetrician", "qualification": "MBBS, MS (OBG)", "experience": 11, "consultation_fee": 1500.0, "working_days": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "start_time": "09:00 AM", "end_time": "05:00 PM", "status": "available"}
    },
    {
        "user": {"full_name": "Dr. Karthik Nair", "email": "dr.karthik.nair@niramaya.org", "role": "doctor", "phone": "+91 9876500008"},
        "doctor": {"department": "Psychiatry", "specialization": "Psychiatrist", "qualification": "MBBS, MD (Psychiatry)", "experience": 6, "consultation_fee": 2000.0, "working_days": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "start_time": "10:00 AM", "end_time": "06:00 PM", "status": "available"}
    },
]


async def seed():
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]

    # --- Check if doctors already seeded ---
    existing_count = await db.doctors.count_documents({})
    if existing_count >= 8:
        print(f"✅ Doctors already seeded ({existing_count} doctors found in DB). Skipping doctor seed.")
    else:
        seeded = 0
        for entry in DOCTORS_SEED:
            u = entry["user"]
            d = entry["doctor"]

            # Skip if user already exists (by email)
            existing_user = await db.users.find_one({"email": u["email"]})
            if existing_user:
                user_id_str = str(existing_user["_id"])
                # Ensure doctor record is linked
                existing_doc = await db.doctors.find_one({"user_id": user_id_str})
                if not existing_doc:
                    doctor_doc = {
                        **d,
                        "user_id": user_id_str,
                        "doctor_name": u["full_name"],
                        "created_at": datetime.utcnow(),
                        "updated_at": datetime.utcnow(),
                    }
                    await db.doctors.insert_one(doctor_doc)
                    seeded += 1
                    print(f"✅ Seeded: {u['full_name']} ({d['department']}) [doctor record linked to existing user]")
                else:
                    print(f"⚠️  Already exists: {u['full_name']} ({d['department']}) — skipped")
                continue

            # Insert user
            now = datetime.utcnow()
            user_doc = {
                "email": u["email"],
                "password": pwd_context.hash("doctor123"),
                "full_name": u["full_name"],
                "role": u["role"],
                "phone": u["phone"],
                "is_active": True,
                "created_at": now,
                "updated_at": now,
            }
            user_result = await db.users.insert_one(user_doc)
            user_id_str = str(user_result.inserted_id)

            # Insert doctor document linked to user
            doctor_doc = {
                **d,
                "user_id": user_id_str,
                "doctor_name": u["full_name"],
                "created_at": now,
                "updated_at": now,
            }
            await db.doctors.insert_one(doctor_doc)
            seeded += 1
            print(f"✅ Seeded: {u['full_name']} ({d['department']})")

        print(f"\n🏥 Doctor seeding complete. {seeded} new doctor(s) inserted.")

    # --- Seed admin user ---
    admin_exists = await db.users.find_one({"email": "admin@niramaya.org"})
    if admin_exists:
        print("⚠️  Admin user already exists — skipped")
    else:
        now = datetime.utcnow()
        await db.users.insert_one({
            "email": "admin@niramaya.org",
            "password": pwd_context.hash("admin123"),
            "full_name": "Hospital Admin",
            "role": "admin",
            "phone": "+91 9876500000",
            "is_active": True,
            "created_at": now,
            "updated_at": now,
        })
        print("✅ Seeded: Hospital Admin (admin@niramaya.org / admin123)")

    # --- Seed patient user ---
    patient_exists = await db.users.find_one({"email": "patient@niramaya.org"})
    if patient_exists:
        print("⚠️  Demo patient user already exists — skipped")
    else:
        now = datetime.utcnow()
        await db.users.insert_one({
            "email": "patient@niramaya.org",
            "password": pwd_context.hash("patient123"),
            "full_name": "Demo Patient",
            "role": "patient",
            "phone": "+91 9876500099",
            "is_active": True,
            "created_at": now,
            "updated_at": now,
        })
        print("✅ Seeded: Demo Patient (patient@niramaya.org / patient123)")

    client.close()
    print("\n✅ Seed script completed successfully.")


if __name__ == "__main__":
    asyncio.run(seed())
