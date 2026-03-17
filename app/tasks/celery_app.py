from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "notifica",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="America/Sao_Paulo",
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    task_always_eager=True,   # ← adiciona essa linha
)