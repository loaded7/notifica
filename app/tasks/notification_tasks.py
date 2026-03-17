from app.tasks.celery_app import celery_app
from app.core.database import SessionLocal
from app.models.notification import Notification
from datetime import datetime
import uuid

@celery_app.task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,  # retry após 60 segundos
)
def send_notification(self, notification_id: str):
    db = SessionLocal()
    try:
        notif = db.query(Notification).filter(
            Notification.id == uuid.UUID(notification_id)
        ).first()

        if not notif:
            return {"error": "Notificação não encontrada"}

        notif.attempts += 1

        # Simulação de envio por canal
        # Na fase 3 vamos integrar SMTP, Twilio e webhooks reais
        if notif.channel == "email":
            print(f"[EMAIL] Para: {notif.recipient} | Assunto: {notif.subject}")
            print(f"[EMAIL] Corpo: {notif.body}")
        elif notif.channel == "sms":
            print(f"[SMS] Para: {notif.recipient} | Msg: {notif.body}")
        elif notif.channel == "webhook":
            print(f"[WEBHOOK] POST {notif.recipient} | Payload: {notif.body}")
        else:
            raise ValueError(f"Canal inválido: {notif.channel}")

        notif.status = "sent"
        notif.sent_at = datetime.utcnow()
        db.commit()

        return {"status": "sent", "id": notification_id}

    except Exception as exc:
        notif.status = "failed"
        db.commit()
        raise self.retry(exc=exc)
    finally:
        db.close()