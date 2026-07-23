from fastapi import APIRouter, Depends
from typing import Optional

from app.schemas.lab_test_schema import LabTestCreate
from app.services.lab_test_service import (
    create_lab_test,
    get_patient_lab_tests,
    search_lab_tests
)
from app.dependencies.role_dependency import require_roles

router = APIRouter(
    prefix="/lab-tests",
    tags=["Lab Tests"]
)


@router.post("/")
async def create(
    lab_test: LabTestCreate,
    current_user=Depends(require_roles("doctor"))
):
    return await create_lab_test(lab_test)


@router.get("/patient/{patient_id}")
async def get_patient_history(
    patient_id: str,
    current_user=Depends(require_roles("doctor", "admin"))
):
    return await get_patient_lab_tests(patient_id)

@router.get("/search")
async def search(
    patient_id: Optional[str] = None,
    doctor_id: Optional[str] = None,
    status: Optional[str] = None,
    test_name: Optional[str] = None,
    page: int = 1,
    limit: int = 10,
    sort_by: Optional[str] = None,
    order: str = "asc",
    current_user=Depends(require_roles("doctor", "admin"))
):
    return await search_lab_tests(
        patient_id,
        doctor_id,
        status,
        test_name,
        page,
        limit,
        sort_by,
        order
    )