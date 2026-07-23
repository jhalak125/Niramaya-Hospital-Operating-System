from fastapi import APIRouter, Depends

from app.schemas.billing_schema import BillCreate
from app.services.billing_service import (
    create_bill,
    get_patient_bills,
    get_all_bills
)
from app.dependencies.auth_dependency import (
    require_admin_or_doctor
)

router = APIRouter(
    prefix="/billing",
    tags=["Billing"]
)


@router.post("/")
async def generate_bill(
    bill: BillCreate,
    current_user=Depends(require_admin_or_doctor)
):
    return await create_bill(bill)


@router.get("/")
async def get_all_bills_route(
    current_user=Depends(require_admin_or_doctor)
):
    return await get_all_bills()


@router.get("/{patient_id}")
async def get_bills(
    patient_id: str,
    current_user=Depends(require_admin_or_doctor)
):
    return await get_patient_bills(patient_id)