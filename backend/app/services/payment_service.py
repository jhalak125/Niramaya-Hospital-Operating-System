import os
import shutil
from uuid import uuid4
from datetime import datetime

from fastapi import UploadFile, File, Form, HTTPException

from app.repositories.notification_repository import NotificationRepository

from app.repositories.billing_repository import BillingRepository
from app.repositories.payment_repository import PaymentRepository
from app.services.audit_log_service import create_audit_log
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv("BASE_URL")

UPLOAD_DIR = "uploads/payments"


async def upload_payment(
    bill_id: str,
    transaction_id: str,
    screenshot: UploadFile
):

    # Check if bill exists
    bill = await BillingRepository.get_by_id(bill_id)

    if bill is None:
        raise HTTPException(
            status_code=404,
            detail="Bill not found"
        )

    # Generate unique filename
    extension = screenshot.filename.split(".")[-1]

    filename = f"{uuid4()}.{extension}"

    filepath = os.path.join(
        UPLOAD_DIR,
        filename
    )

    # Save screenshot
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(
            screenshot.file,
            buffer
        )

    payment = {
        "bill_id": bill_id,
        "amount": bill["total_amount"],
        "transaction_id": transaction_id,
        "payment_method": "UPI",
        "status": "Verification Pending",
        "screenshot": filename,
        "created_at": datetime.utcnow()
    }

    payment_id = await PaymentRepository.create(
        payment
    )

    await create_audit_log(
    user_id=bill["patient_id"],
    action="UPLOAD_PAYMENT",
    module="Payment",
    module_id=str(payment_id),
    description="Payment uploaded"
)

    return {
        "message": "Payment uploaded successfully",
        "payment_id": str(payment_id)
    }

async def verify_payment(payment_id: str):

    payment = await PaymentRepository.get_by_id(
        payment_id
    )

    if payment is None:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    await PaymentRepository.verify(
        payment_id
    )

    await BillingRepository.mark_paid(
        payment["bill_id"]
    )

    await create_audit_log(
    user_id=bill["patient_id"],
    action="VERIFY_PAYMENT",
    module="Payment",
    module_id=payment_id,
    description="Payment verified"
)

    bill = await BillingRepository.get_by_id(
        payment["bill_id"]
    )

    notification = {

        "user_id": bill["patient_id"],

        "title": "Payment Verified",

        "message": (
            f"Your payment of ₹{payment['amount']} "
            "has been verified successfully."
        ),

        "notification_type": "payment",

        "is_read": False,

        "created_at": datetime.utcnow()
    }

    await NotificationRepository.create(
        notification
    )

    return {
        "message": "Payment verified successfully"
    }

async def get_payment_by_bill(
    bill_id: str
):

    payment = await PaymentRepository.get_by_bill(
        bill_id
    )

    if payment is None:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    payment["_id"] = str(payment["_id"])

    payment["screenshot_url"] = (
    f"{BASE_URL}/uploads/payments/{payment['screenshot']}"
)

    return payment