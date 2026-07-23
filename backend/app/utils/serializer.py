def doctor_serializer(doctor):
    return {
        "id": str(doctor["_id"]),
        "user_id": doctor["user_id"],
        "department": doctor["department"],
        "specialization": doctor["specialization"],
        "qualification": doctor["qualification"],
        "experience": doctor["experience"],
        "consultation_fee": doctor["consultation_fee"],
        "working_days": doctor["working_days"],
        "start_time": doctor["start_time"],
        "end_time": doctor["end_time"],
        "status": doctor["status"],
        "created_at": doctor["created_at"],
        "updated_at": doctor["updated_at"]
    }


def doctors_serializer(doctors):
    return [doctor_serializer(doc) for doc in doctors]