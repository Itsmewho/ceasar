from pydantic import BaseModel
from typing import Optional


class InviteModel(BaseModel):
    sender_name: str
    sender_surname: str
    sender_phone: str
    recipient_name: str
    recipient_surname: str
    recipient_phone: str
    message: str
    status: Optional[str] = "unread"  # Default to 'unread'

    class Config:
        from_attributes = True
