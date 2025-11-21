import os
from celery import Celery

# Get Redis URL from environment or use default
redis_url = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')

app = Celery('gitta_trader', broker=redis_url, backend=redis_url)

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

if __name__ == '__main__':
    app.start()
