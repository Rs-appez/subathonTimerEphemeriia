from enum import Enum
from redis.client import Redis, ConnectionPool
import asyncio
from collections import defaultdict
from django.conf import settings


redis_pool = ConnectionPool.from_url(settings.CELERY_BROKER_URL)

def redis_client() -> Redis:
    return Redis(connection_pool=redis_pool)


class Channels(Enum):
    START_EVENT = "start_event"
    UPDATES = "updates"


class RedisBroadcaster:
    """
    Singleton that maintains ONE Redis connection for ALL users.
    """

    def __init__(self):
        self._queues = defaultdict(set)
        self._task = None
        self._lock = asyncio.Lock()

    async def add_subscriber(self, channel: str, queue: asyncio.Queue):
        async with self._lock:
            self._queues[channel].add(queue)
            print("Added subscriber to channel:", channel)
            if self._task is None:
                self._task = asyncio.create_task(self._listen_to_redis())

    async def remove_subscriber(self, channel: str, queue: asyncio.Queue):
        async with self._lock:
            self._queues[channel].discard(queue)
            # Optional: Cancel task if no subscribers left, but keeping it open is cheaper
            # than constantly re-subscribing/unsubscribing in Upstash.

    async def _listen_to_redis(self):
        client = redis_client()
        pubsub = client.pubsub()
        # Subscribe to all known channels at once to save commands
        print("Starting Redis listener task...")
        await pubsub.subscribe(*[ch.value for ch in Channels])

        try:
            async for message in pubsub.listen():
                print("message : ", message)
                if message["type"] == "message":
                    channel = message["channel"].decode()
                    data = message["data"].decode()
                    # Fan-out: Send to all queues listening to this channel
                    for q in list(self._queues.get(channel, [])):
                        await q.put(f"data: {data}\n\n")
        except Exception as e:
            print(f"Redis listener error: {e}")
            self._task = None  # Allow restart on next request
        finally:
            await client.aclose()
