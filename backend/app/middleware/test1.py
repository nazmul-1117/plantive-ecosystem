import asyncio
from redis.asyncio import Redis

async def main():
    redis = Redis(
        host="localhost",
        port=6379,
        decode_responses=True,
    )

    print(await redis.ping())

# if __name__ == ""
asyncio.run(main())