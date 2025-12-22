import asyncio
from collections.abc import AsyncGenerator

import redis.asyncio as redis
from django.conf import settings
from django.http import StreamingHttpResponse
from django.http.response import HttpResponseServerError

HEARTBEAT_INTERVAL = 30  # seconds

redis_pool = redis.ConnectionPool.from_url(settings.CELERY_BROKER_URL)

def get_redis_client() -> redis.Redis:
    return redis.Redis(connection_pool=redis_pool)

async def sse_stream(event_to_subscribe: str) -> StreamingHttpResponse:
    try:
        client = get_redis_client()
        await client.ping()
        pubsub = client.pubsub()
        await pubsub.subscribe(event_to_subscribe)

    except redis.ConnectionError:
        return HttpResponseServerError("Could not connect to Redis.")

    async def event_stream() -> AsyncGenerator[str, None]:
        queue: asyncio.Queue[str] = asyncio.Queue()

        async def listen_messages():
            try:
                async for message in pubsub.listen():
                    if message["type"] == "message":
                        await queue.put(f"data: {message['data'].decode()}\n\n")
            except asyncio.CancelledError:
                pass

        async def send_heartbeats():
            try:
                while True:
                    await asyncio.sleep(HEARTBEAT_INTERVAL)
                    await queue.put(": heartbeat\n\n")
            except asyncio.CancelledError:
                pass

        listener_task = asyncio.create_task(listen_messages())
        heartbeat_task = asyncio.create_task(send_heartbeats())

        try:
            while True:
                yield await queue.get()
        except asyncio.CancelledError:
            pass
        finally:
            listener_task.cancel()
            heartbeat_task.cancel()
            await asyncio.gather(listener_task, heartbeat_task, return_exceptions=True)
            await pubsub.unsubscribe(event_to_subscribe)
            await pubsub.aclose()
            await client.aclose()

    response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    response["Cache-Control"] = "no-cache"
    response["X-Accel-Buffering"] = "no"
    response["Connection"] = "keep-alive"
    return response


async def sse_start_event_stream(_request) -> StreamingHttpResponse:
    return await sse_stream("start_event")


async def sse_updates_stream(_request) -> StreamingHttpResponse:
    return await sse_stream("updates")
