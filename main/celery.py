# Celery communicates via messages, usually using a broker to mediate between clients and workers. To initiate a task the client adds a message to the queue, the broker then delivers that message to a worker.

import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')    # main = <project_name>

app = Celery('main')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()