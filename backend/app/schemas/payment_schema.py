from pydantic import BaseModel


class PaymentResponse(BaseModel):
    message: str
    payment_id: str