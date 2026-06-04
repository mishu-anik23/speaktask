from celery import Celery
from app.core.config import get_settings

settings = get_settings()

app = Celery(
    "speaktask",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes hard limit
    task_soft_time_limit=25 * 60,  # 25 minutes soft limit
)


@app.task(bind=True, max_retries=2)
def execute_command_task(self, command_id: int):
    """Background task to execute a command."""
    from app.db.session import AsyncSessionLocal
    import asyncio

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(_execute_async(command_id))
    except Exception as exc:
        # Retry with exponential backoff
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)


async def _execute_async(command_id: int):
    """Async wrapper for command execution."""
    from app.db.session import AsyncSessionLocal
    from app.services.command_service import CommandService

    async with AsyncSessionLocal() as db:
        await CommandService.execute_command(db, command_id)
