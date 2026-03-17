from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.notification import Notification
from app.schemas.notification import NotificationCreate, NotificationResponse
from app.tasks.notification_tasks import send_notification

router = APIRouter()

@router.post("/", response_model=NotificationResponse, status_code=202)
def create_notification(
    data: NotificationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    notif = Notification(
        user_id=current_user.id,
        channel=data.channel,
        recipient=data.recipient,
        subject=data.subject,
        body=data.body,
        status="pending",
    )
    db.add(notif)
    db.commit()
    db.refresh(notif)

    # Envia para a fila — não bloqueia a resposta
    send_notification.delay(str(notif.id))

    return notif

@router.get("/", response_model=List[NotificationResponse])
def list_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(Notification).filter(
        Notification.user_id == current_user.id
    ).order_by(Notification.created_at.desc()).all()