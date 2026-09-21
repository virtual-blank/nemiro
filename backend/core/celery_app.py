from celery import Celery
from core.config import get_celery_settings

# URL брокера можно брать из .env
broker_url = get_celery_settings().url

celery_app = Celery(
    "nemiro_worker",
    broker=broker_url,
    include=["src.elements.tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

