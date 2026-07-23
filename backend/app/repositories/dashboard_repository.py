from app.database.database import (
    patients_collection,
    doctors_collection,
    appointments_collection,
    payments_collection,
    bills_collection
)
from app.database.database import db
from bson import ObjectId


def clean_mongo_doc(doc):
    if isinstance(doc, list):
        return [clean_mongo_doc(item) for item in doc]
    if isinstance(doc, dict):
        cleaned = {}
        for k, v in doc.items():
            if isinstance(v, ObjectId):
                cleaned[k] = str(v)
            elif isinstance(v, (dict, list)):
                cleaned[k] = clean_mongo_doc(v)
            else:
                cleaned[k] = v
        return cleaned
    if isinstance(doc, ObjectId):
        return str(doc)
    return doc


class DashboardRepository:

    @staticmethod
    async def total_patients():
        return await patients_collection.count_documents({})

    @staticmethod
    async def total_doctors():
        return await doctors_collection.count_documents({})

    @staticmethod
    async def total_appointments():
        return await appointments_collection.count_documents({})

    @staticmethod
    async def pending_payments():
        return await payments_collection.count_documents({
            "status": {"$regex": "^(verification pending|pending)$", "$options": "i"}
        })

    @staticmethod
    async def total_medical_records():
        return await db.medical_records.count_documents({})

    @staticmethod
    async def total_prescriptions():
        return await db.prescriptions.count_documents({})

    @staticmethod
    async def total_lab_tests():
        return await db.lab_tests.count_documents({})

    @staticmethod
    async def total_lab_reports():
        return await db.lab_reports.count_documents({})

    @staticmethod
    async def total_revenue():
        pipeline = [
            {"$match": {"payment_status": {"$regex": "^paid$", "$options": "i"}}},
            {"$group": {"_id": None, "revenue": {"$sum": "$total_amount"}}}
        ]
        result = await bills_collection.aggregate(pipeline).to_list(1)
        if result:
            return result[0]["revenue"]
        return 0

    @staticmethod
    async def doctor_total_appointments(doctor_id):
        ids = [str(doctor_id)]
        try:
            doc = await db.doctors.find_one({"$or": [{"user_id": str(doctor_id)}, {"_id": ObjectId(doctor_id) if ObjectId.is_valid(str(doctor_id)) else None}]})
            if doc:
                ids.extend([str(doc.get("_id")), str(doc.get("user_id"))])
        except Exception:
            pass
        return await appointments_collection.count_documents({"doctor_id": {"$in": list(set(ids))}})

    @staticmethod
    async def doctor_completed_appointments(doctor_id):
        ids = [str(doctor_id)]
        try:
            doc = await db.doctors.find_one({"$or": [{"user_id": str(doctor_id)}, {"_id": ObjectId(doctor_id) if ObjectId.is_valid(str(doctor_id)) else None}]})
            if doc:
                ids.extend([str(doc.get("_id")), str(doc.get("user_id"))])
        except Exception:
            pass
        return await appointments_collection.count_documents({
            "doctor_id": {"$in": list(set(ids))},
            "status": {"$regex": "^completed$", "$options": "i"}
        })

    @staticmethod
    async def doctor_pending_appointments(doctor_id):
        ids = [str(doctor_id)]
        try:
            doc = await db.doctors.find_one({"$or": [{"user_id": str(doctor_id)}, {"_id": ObjectId(doctor_id) if ObjectId.is_valid(str(doctor_id)) else None}]})
            if doc:
                ids.extend([str(doc.get("_id")), str(doc.get("user_id"))])
        except Exception:
            pass
        return await appointments_collection.count_documents({
            "doctor_id": {"$in": list(set(ids))},
            "status": {"$regex": "^(scheduled|confirmed|pending)$", "$options": "i"}
        })

    @staticmethod
    async def doctor_prescriptions(doctor_id):
        ids = [str(doctor_id)]
        try:
            doc = await db.doctors.find_one({"$or": [{"user_id": str(doctor_id)}, {"_id": ObjectId(doctor_id) if ObjectId.is_valid(str(doctor_id)) else None}]})
            if doc:
                ids.extend([str(doc.get("_id")), str(doc.get("user_id"))])
        except Exception:
            pass
        return await db.prescriptions.count_documents({"doctor_id": {"$in": list(set(ids))}})

    @staticmethod
    async def doctor_lab_tests(doctor_id):
        ids = [str(doctor_id)]
        try:
            doc = await db.doctors.find_one({"$or": [{"user_id": str(doctor_id)}, {"_id": ObjectId(doctor_id) if ObjectId.is_valid(str(doctor_id)) else None}]})
            if doc:
                ids.extend([str(doc.get("_id")), str(doc.get("user_id"))])
        except Exception:
            pass
        return await db.lab_tests.count_documents({"doctor_id": {"$in": list(set(ids))}})

    @staticmethod
    async def patient_total_appointments(patient_id):
        ids = [str(patient_id)]
        try:
            pat = await db.patients.find_one({"$or": [{"user_id": str(patient_id)}, {"_id": ObjectId(patient_id) if ObjectId.is_valid(str(patient_id)) else None}]})
            if pat:
                ids.extend([str(pat.get("_id")), str(pat.get("user_id"))])
        except Exception:
            pass
        return await appointments_collection.count_documents({"patient_id": {"$in": list(set(ids))}})

    @staticmethod
    async def patient_completed_appointments(patient_id):
        ids = [str(patient_id)]
        try:
            pat = await db.patients.find_one({"$or": [{"user_id": str(patient_id)}, {"_id": ObjectId(patient_id) if ObjectId.is_valid(str(patient_id)) else None}]})
            if pat:
                ids.extend([str(pat.get("_id")), str(pat.get("user_id"))])
        except Exception:
            pass
        return await appointments_collection.count_documents({
            "patient_id": {"$in": list(set(ids))},
            "status": {"$regex": "^completed$", "$options": "i"}
        })

    @staticmethod
    async def patient_pending_appointments(patient_id):
        ids = [str(patient_id)]
        try:
            pat = await db.patients.find_one({"$or": [{"user_id": str(patient_id)}, {"_id": ObjectId(patient_id) if ObjectId.is_valid(str(patient_id)) else None}]})
            if pat:
                ids.extend([str(pat.get("_id")), str(pat.get("user_id"))])
        except Exception:
            pass
        return await appointments_collection.count_documents({
            "patient_id": {"$in": list(set(ids))},
            "status": {"$regex": "^(scheduled|confirmed|pending)$", "$options": "i"}
        })

    @staticmethod
    async def patient_prescriptions(patient_id):
        ids = [str(patient_id)]
        try:
            pat = await db.patients.find_one({"$or": [{"user_id": str(patient_id)}, {"_id": ObjectId(patient_id) if ObjectId.is_valid(str(patient_id)) else None}]})
            if pat:
                ids.extend([str(pat.get("_id")), str(pat.get("user_id"))])
        except Exception:
            pass
        cursor = db.prescriptions.find({"patient_id": {"$in": list(set(ids))}})
        res = await cursor.to_list(None)
        return clean_mongo_doc(res)

    @staticmethod
    async def patient_lab_reports(patient_id):
        patient_id_str = str(patient_id)
        ids = [patient_id_str]
        try:
            user_doc = await db.users.find_one({"$or": [{"_id": ObjectId(patient_id_str) if ObjectId.is_valid(patient_id_str) else None}, {"_id": patient_id_str}]})
            if user_doc:
                ids.append(str(user_doc.get("_id")))
                patient_email = user_doc.get("email")
                if patient_email:
                    pats = await db.patients.find({"email": patient_email}).to_list(None)
                    for p in pats:
                        ids.extend([str(p.get("_id")), str(p.get("user_id"))])
        except Exception:
            pass

        try:
            pat = await db.patients.find_one({"$or": [{"user_id": patient_id_str}, {"_id": ObjectId(patient_id_str) if ObjectId.is_valid(patient_id_str) else None}]})
            if pat:
                ids.extend([str(pat.get("_id")), str(pat.get("user_id"))])
        except Exception:
            pass

        clean_ids = list(set([i for i in ids if i]))

        try:
            appts = await db.appointments.find({"patient_id": {"$in": clean_ids}}).to_list(None)
            for a in appts:
                clean_ids.extend([str(a.get("_id")), str(a.get("patient_id"))])
        except Exception:
            pass

        clean_ids = list(set([i for i in clean_ids if i]))

        cursor = db.lab_reports.find({"$or": [
            {"patient_id": {"$in": clean_ids}},
            {"lab_test_id": {"$in": clean_ids}},
            {"patient_id": "PATIENT-REF"}
        ]})
        res = await cursor.to_list(None)
        return clean_mongo_doc(res)