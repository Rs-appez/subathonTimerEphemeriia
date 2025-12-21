from celery import shared_task
import redis


@shared_task
def send_update(data):
    r = redis.Redis()
    r.publish("updates", data)

