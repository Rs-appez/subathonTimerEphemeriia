from redis.connection import ConnectionPool
import json

from celery import shared_task
from utils.redis import Channels
from redis.client import Redis
from django.conf import settings


redis_pool = ConnectionPool.from_url(settings.CELERY_BROKER_URL)
redis_client = Redis(connection_pool=redis_pool)

@shared_task
def send_update(data):
    payload = json.dumps(data) if isinstance(data, dict) else str(data)
    redis_client.publish(Channels.UPDATES.value, payload)


@shared_task
def send_start_event(data):
    payload = json.dumps(data) if isinstance(data, dict) else str(data)
    redis_client.publish(Channels.START_EVENT.value, payload)
