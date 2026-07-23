from pydantic import BaseModel
from datetime import datetime


class AuditLogCreate(BaseModel):

    user_id: str

    role: str

    action: str

    module: str

    description: str