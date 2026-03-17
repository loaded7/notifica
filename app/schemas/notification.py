from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

class NotificationCreate(BaseModel):
    channel: str        # "email", "sms", "webhook"
    recipient: str      # e-mail, telefone ou URL
    subject: Optional[str] = None
    body: str

class NotificationResponse(BaseModel):
    id: uuid.UUID
    channel: str
    recipient: str
    subject: Optional[str]
    body: str
    status: str
    attempts: int
    created_at: datetime

    class Config:
        from_attributes = True