from datetime import datetime
from app.repositories.notification_repository import NotificationRepository


async def send_appointment_notification(
    patient_id,
    doctor_id,
    appointment_date,
    time_slot
):
    patient_notification = {
        "user_id": str(patient_id),
        "title": "Appointment Confirmed",
        "message": f"Your consultation is scheduled on {appointment_date} at {time_slot}.",
        "notification_type": "appointment",
        "is_read": False,
        "created_at": datetime.utcnow()
    }
    await NotificationRepository.create(patient_notification)

    doctor_notification = {
        "user_id": str(doctor_id),
        "title": "New Consultation Scheduled",
        "message": f"A new patient appointment has been booked for {appointment_date} at {time_slot}.",
        "notification_type": "appointment",
        "is_read": False,
        "created_at": datetime.utcnow()
    }
    await NotificationRepository.create(doctor_notification)