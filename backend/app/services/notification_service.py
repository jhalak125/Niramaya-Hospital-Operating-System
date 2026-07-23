from datetime import datetime
from fastapi import HTTPException

from app.repositories.notification_repository import NotificationRepository
from app.services.audit_log_service import create_audit_log



async def create_notification(data):

    notification = data.dict()

    notification["created_at"] = datetime.utcnow()

    notification_id = await NotificationRepository.create(
        notification
    )

    await create_audit_log(
    user_id=data.user_id,
    action="CREATE_NOTIFICATION",
    module="Notification",
    module_id=str(notification_id),
    description="Notification created"
)

    return {
        "message": "Notification created successfully",
        "notification_id": str(notification_id)
    }



async def get_user_notifications(user_id):

    notifications = await NotificationRepository.get_by_user(
        user_id
    )

    for notification in notifications:
        notification["_id"] = str(
            notification["_id"]
        )

    return notifications



async def mark_notification_read(notification_id):

    await NotificationRepository.mark_as_read(
        notification_id
    )

    return {
        "message": "Notification marked as read"
    }



async def delete_notification(notification_id):

    await NotificationRepository.delete(
        notification_id
    )

    await create_audit_log(
    user_id="SYSTEM",
    action="DELETE_NOTIFICATION",
    module="Notification",
    module_id=notification_id,
    description="Notification deleted"
)

    return {
        "message": "Notification deleted successfully"
    }