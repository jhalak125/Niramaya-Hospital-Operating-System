from pydantic import BaseModel
from typing import Optional


class NotificationCreate(BaseModel):

    user_id: str

    title: str

    message: str

    notification_type: str

    is_read: bool = False