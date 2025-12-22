import json

import redis
from celery import shared_task
from django.conf import settings

redis_pool = redis.ConnectionPool.from_url(settings.CELERY_BROKER_URL)

def get_redis_client():
    return redis.Redis(connection_pool=redis_pool)

@shared_task
def send_update(data):
    client = get_redis_client()
    payload = json.dumps(data) if isinstance(data, dict) else str(data)
    client.publish("updates", payload)


@shared_task
def send_start_event(data):
    client = get_redis_client()
    payload = json.dumps(data) if isinstance(data, dict) else str(data)
    client.publish("start_event", payload)
