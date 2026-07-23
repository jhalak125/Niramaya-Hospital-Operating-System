from pydantic import BaseModel
from typing import Literal

class AppointmentStatusUpdate(BaseModel):
    status: Literal[
        "Scheduled",
        "Confirmed",
        "Completed",
        "Cancelled",
        "No Show"
    ]