from app.database.database import db


class AnalyticsRepository:

    @staticmethod
    async def dashboard_summary():

        total_patients = await db.patients.count_documents({})

        total_doctors = await db.doctors.count_documents({})

        total_appointments = await db.appointments.count_documents({})

        completed_appointments = await db.appointments.count_documents(
            {
                "status": "Completed"
            }
        )

        pending_appointments = await db.appointments.count_documents(
            {
                "status": "Scheduled"
            }
        )

        completed_lab_tests = await db.lab_tests.count_documents(
            {
                "status": "Completed"
            }
        )

        pending_payments = await db.payments.count_documents(
            {
                "status": "Verification Pending"
            }
        )

        revenue = await db.bills.aggregate(
            [
                {
                    "$match": {
                        "payment_status": "Paid"
                    }
                },
                {
                    "$group": {
                        "_id": None,
                        "total": {
                            "$sum": "$total_amount"
                        }
                    }
                }
            ]
        ).to_list(1)

        total_revenue = (
            revenue[0]["total"]
            if revenue
            else 0
        )

        return {
            "total_patients": total_patients,
            "total_doctors": total_doctors,
            "total_appointments": total_appointments,
            "completed_appointments": completed_appointments,
            "pending_appointments": pending_appointments,
            "completed_lab_tests": completed_lab_tests,
            "pending_payments": pending_payments,
            "total_revenue": total_revenue
        }
    
    @staticmethod
    async def revenue_analytics():

        revenue = await db.bills.aggregate(
            [
                {
                    "$match": {
                        "payment_status": "Paid"
                    }
                },
                {
                    "$group": {
                        "_id": {
                            "$dateToString": {
                                "format": "%Y-%m",
                                "date": "$created_at"
                            }
                        },
                        "revenue": {
                            "$sum": "$total_amount"
                        }
                    }
                },
                {
                    "$sort": {
                        "_id": 1
                    }
                }
            ]
        ).to_list(None)


        result = []

        for item in revenue:

            result.append(
                {
                    "month": item["_id"],
                    "revenue": item["revenue"]
                }
            )

        return result
    
    @staticmethod
    async def top_doctors():

        result = await db.appointments.aggregate(
            [

                # Convert doctor_id string -> ObjectId
                {
                    "$addFields": {
                        "doctor_object_id": {
                            "$toObjectId": "$doctor_id"
                        }
                    }
                },


                # Count appointments
                {
                    "$group": {
                        "_id": "$doctor_object_id",
                        "total_appointments": {
                            "$sum": 1
                        }
                    }
                },


                {
                    "$sort": {
                        "total_appointments": -1
                    }
                },


                {
                    "$limit": 10
                },


                # Join doctors collection
                {
                    "$lookup": {
                        "from": "doctors",
                        "localField": "_id",
                        "foreignField": "_id",
                        "as": "doctor"
                    }
                },


                {
                    "$unwind": "$doctor"
                },


                # Join users collection
                {
                    "$addFields": {
                        "user_object_id": {
                            "$toObjectId": "$doctor.user_id"
                        }
                    }
                },


                {
                    "$lookup": {
                        "from": "users",
                        "localField": "user_object_id",
                        "foreignField": "_id",
                        "as": "user"
                    }
                },


                {
                    "$unwind": "$user"
                },


                {
                    "$project": {
                        "_id": 0,
                        "doctor_name": "$user.full_name",
                        "specialization": "$doctor.specialization",
                        "total_appointments": 1
                    }
                }

            ]
        ).to_list(None)


        return result
    
    @staticmethod
    async def appointment_analytics():

        appointments = await db.appointments.aggregate(
            [
                {
                    "$group": {
                        "_id": "$status",
                        "count": {
                            "$sum": 1
                        }
                    }
                }
            ]
        ).to_list(None)


        result = {}

        for appointment in appointments:

            result[appointment["_id"]] = appointment["count"]


        return result

    
    @staticmethod
    async def lab_test_analytics():

        lab_tests = await db.lab_tests.aggregate(
            [
                {
                    "$group": {
                        "_id": "$status",
                        "count": {
                            "$sum": 1
                        }
                    }
                }
            ]
        ).to_list(None)


        result = {}

        for test in lab_tests:

            result[test["_id"]] = test["count"]


        return result
    
    @staticmethod
    async def payment_analytics():

        payments = await db.payments.aggregate(
            [
                {
                    "$group": {
                        "_id": "$status",
                        "count": {
                            "$sum": 1
                        }
                    }
                }
            ]
        ).to_list(None)


        result = {}

        for payment in payments:

            result[payment["_id"]] = payment["count"]


        return result