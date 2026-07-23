from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    Depends
)
from app.dependencies.auth_dependency import (
    require_patient,
    require_admin,
    get_current_user
)
from app.services.payment_service import (
    upload_payment,
    verify_payment,
    get_payment_by_bill
)

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


@router.post("/")
async def upload_payment_proof(
    bill_id: str = Form(...),
    transaction_id: str = Form(...),
    screenshot: UploadFile = File(...),
    current_user=Depends(require_patient)
):
    return await upload_payment(
        bill_id,
        transaction_id,
        screenshot
    )

@router.put("/verify/{payment_id}")
async def verify_uploaded_payment(
    payment_id: str,
    current_user=Depends(require_admin)
):
    return await verify_payment(payment_id)

@router.get("/bill/{bill_id}")
async def payment_details(
    bill_id: str,
    current_user=Depends(get_current_user)
):
    return await get_payment_by_bill(
        bill_id
    )