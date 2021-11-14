# Celery communicates via messages, usually using a broker to mediate between clients and workers. Worker is the function that executes the task. The django passes the defined task to the celery workers and  broker is the task queue that stores the task.

import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')    # main = <project_name>

app = Celery('main')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'crypto_data_10s': {
        'task': 'crypto.tasks.crypto_data',
        'schedule': 10.0    # refresh time 10 secs
    }
}

app.autodiscover_tasks()