import os

from django.conf import settings

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fantasy.settings")

app = Celery("fantasy")

app.config_from_object("django.conf.settings", namespace="CELERY")

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
