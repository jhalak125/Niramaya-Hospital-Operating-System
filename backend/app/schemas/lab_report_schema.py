from pydantic import BaseModel
from typing import Optional


class LabReportCreate(BaseModel):
    lab_test_id: str
    result: str
    notes: str
    report_file: Optional[str] = None