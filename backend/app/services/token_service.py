from redis.asyncio import Redis
from typing import Annotated
from fastapi import status, Depends

# from app.dependencies.redis_dependency import get_redis

class TokenService:

    # def __init__(self, redis: Redis):
    #     self.redis = redis
    
    async def revoke_token(
            self, jti: str,
            ttl: int,
            redis: Redis
        ) -> None:

        await redis.set(
            name=f"jwt:blacklist:{jti}",
            value="1", #1-> key exist, 0-> key doesnot exist
            ex=ttl
        )
    
    async def is_revoked(
            self,
            jti: str,
            redis: Redis
        ) -> bool:
        return await redis.exists(
            f"jwt:blacklist:{jti}"
            ) == 1
