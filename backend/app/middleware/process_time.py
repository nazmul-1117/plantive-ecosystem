import time
import logging

from fastapi import Request

logger = logging.getLogger(__name__)

async def process_time_middleware(request: Request, call_next):
    
    start_time: float = time.perf_counter()

    response = await call_next(request)

    # elapsed_time => otibahito time
    elapsed_time: float = time.perf_counter() - start_time

    request.state.process_time = elapsed_time
    response.headers["X-Process-Time"] = f"{elapsed_time:.5f}"

    logger.info(
        "Request Processed in %.5f seconds",
        elapsed_time
    )

    return response