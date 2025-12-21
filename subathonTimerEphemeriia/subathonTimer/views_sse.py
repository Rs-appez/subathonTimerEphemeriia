import asyncio

import redis.asyncio as redis
from django.http import StreamingHttpResponse
from django.http.response import HttpResponseServerError
from django.conf import settings

HEARTBEAT_INTERVAL = 30  # seconds


async def sse_stream(request):
    print("SSE stream requested")
    try:
        client = redis.from_url(settings.CELERY_BROKER_URL)
        await client.ping()
        pubsub = client.pubsub()
        await pubsub.subscribe("updates")

    except redis.ConnectionError:
        return HttpResponseServerError("Could not connect to Redis.")

    async def event_stream():
        try:
            while True:
                try:
                    message = await asyncio.wait_for(
                        pubsub.get_message(ignore_subscribe_messages=True),
                        timeout=HEARTBEAT_INTERVAL,
                    )
                    if message:
                        yield f"data: {message['data'].decode()}\n\n"
                    else:
                        # Send heartbeat to keep connection alive
                        yield ": heartbeat\n\n"
                except asyncio.TimeoutError:
                    yield ": heartbeat\n\n"
        except asyncio.CancelledError:
            pass
        finally:
            await pubsub.unsubscribe("updates")
            await pubsub.close()
            await client.close()

    response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    response["Cache-Control"] = "no-cache"
    response["X-Accel-Buffering"] = "no"
    return response
