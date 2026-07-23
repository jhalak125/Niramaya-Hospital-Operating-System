import os
import aiosmtplib

from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT"))

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


async def send_email(
    receiver: str,
    subject: str,
    body: str
):
    message = EmailMessage()

    message["From"] = f"Niramaya <{EMAIL_ADDRESS}>"
    message["To"] = receiver
    message["Subject"] = subject

    message.set_content(body)

    await aiosmtplib.send(
        message,
        hostname=SMTP_HOST,
        port=SMTP_PORT,
        username=EMAIL_ADDRESS,
        password=EMAIL_PASSWORD,
        start_tls=True
    )