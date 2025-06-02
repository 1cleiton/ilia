import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

app = Celery("app")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


app.conf.beat_schedule = {
    "Importação de produtos de forma recorrente": {
        "task": "orders.tasks.import_products",
        "schedule": crontab(hour="*/6"),
    }
}
