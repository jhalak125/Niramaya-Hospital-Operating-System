from fastapi import APIRouter

from app.services.email_service import send_email

router = APIRouter(
    prefix="/test",
    tags=["Testing"]
)


@router.get("/email")
async def test_email():

    await send_email(
        receiver="jhalakmverma.15@gmail.com",
        subject="Niramaya",
        body="""
Hello!

This is a test email from Niramaya - Healthcare Management Platform.

Congratulations! Your email service is working.

Regards,
Niramaya
"""
    )

    return {
        "message": "Email sent successfully"
    }