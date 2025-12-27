from utils.redis import RedisBroadcaster, Channels
import asyncio

from django.http import StreamingHttpResponse

HEARTBEAT_INTERVAL = 30  # seconds


broadcaster = RedisBroadcaster()


async def sse_stream(event_to_subscribe: str) -> StreamingHttpResponse:
    # Create a local queue for this specific user
    queue: asyncio.Queue[str] = asyncio.Queue()

    # Register this user's queue with the global broadcaster
    await broadcaster.add_subscriber(event_to_subscribe, queue)

    async def event_stream():
        async def send_heartbeats():
            try:
                while True:
                    await asyncio.sleep(HEARTBEAT_INTERVAL)
                    await queue.put(": heartbeat\n\n")
            except asyncio.CancelledError:
                pass

        heartbeat_task = asyncio.create_task(send_heartbeats())

        try:
            while True:
                yield await queue.get()
        except asyncio.CancelledError:
            pass
        finally:
            heartbeat_task.cancel()
            await broadcaster.remove_subscriber(event_to_subscribe, queue)

    response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    response["Cache-Control"] = "no-cache"
    response["X-Accel-Buffering"] = "no"
    response["Connection"] = "keep-alive"
    return response


async def sse_start_event_stream(_request) -> StreamingHttpResponse:
    return await sse_stream(Channels.START_EVENT.value)


async def sse_updates_stream(_request) -> StreamingHttpResponse:
    return await sse_stream(Channels.UPDATES.value)
