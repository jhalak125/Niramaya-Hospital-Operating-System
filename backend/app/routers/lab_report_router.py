from fastapi import APIRouter, Depends, UploadFile, File, Form

from app.schemas.lab_report_schema import LabReportCreate
from app.services.lab_report_service import (
    create_lab_report,
    get_patient_reports
)
from app.dependencies.role_dependency import require_roles


router = APIRouter(
    prefix="/lab-reports",
    tags=["Lab Reports"]
)


@router.post("")
@router.post("/")
async def create(
    lab_test_id: str = Form(...),
    result: str = Form(...),
    notes: str = Form(...),
    file: UploadFile = File(None),
    current_user=Depends(require_roles("doctor"))
):

    report = LabReportCreate(
        lab_test_id=lab_test_id,
        result=result,
        notes=notes
    )

    return await create_lab_report(
        report,
        file
    )


@router.get("/patient/{patient_id}")
async def get_patient_history(
    patient_id: str,
    current_user=Depends(require_roles("patient", "doctor", "admin"))
):

    return await get_patient_reports(
        patient_id
    )