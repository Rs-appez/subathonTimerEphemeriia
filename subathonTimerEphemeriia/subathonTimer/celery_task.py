from redis.connection import ConnectionPool
import json

from celery import shared_task
from utils.redis import Channels
from redis.client import Redis
from django.conf import settings


redis_pool = ConnectionPool.from_url(settings.CELERY_BROKER_URL)

def redis_client() -> Redis:
    return Redis(connection_pool=redis_pool)

@shared_task
def send_update(data):
    client = redis_client()
    payload = json.dumps(data) if isinstance(data, dict) else str(data)
    client.publish(Channels.UPDATES.value, payload)


@shared_task
def send_start_event(data):
    client = redis_client()
    payload = json.dumps(data) if isinstance(data, dict) else str(data)
    client.publish(Channels.START_EVENT.value, payload)
