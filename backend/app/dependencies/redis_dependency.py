from collections.abc import AsyncGenerator
from redis.asyncio import Redis
from fastapi import Request

async def get_redis(request: Request) -> AsyncGenerator[Redis, None]:
    yield request.app.state.redis
