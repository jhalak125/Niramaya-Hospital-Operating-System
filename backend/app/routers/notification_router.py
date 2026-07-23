from fastapi import APIRouter, Depends

from app.schemas.notification_schema import NotificationCreate

from app.services.notification_service import (
    create_notification,
    get_user_notifications,
    mark_notification_read,
    delete_notification
)

from app.dependencies.auth_dependency import get_current_user


router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)



@router.post("/")
async def create(
    notification: NotificationCreate,
    current_user=Depends(get_current_user)
):

    return await create_notification(
        notification
    )



@router.get("/my")
async def my_notifications(
    current_user=Depends(get_current_user)
):

    return await get_user_notifications(
        current_user["sub"]
    )



@router.put("/{notification_id}/read")
async def read_notification(
    notification_id: str,
    current_user=Depends(get_current_user)
):

    return await mark_notification_read(
        notification_id
    )



@router.delete("/{notification_id}")
async def remove_notification(
    notification_id: str,
    current_user=Depends(get_current_user)
):

    return await delete_notification(
        notification_id
    )