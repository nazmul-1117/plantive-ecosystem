
import logging
import time

from fastapi import Request

logger = logging.getLogger(__name__)

async def logging_middleware(request: Request, call_next):

    start_time: float =  time.perf_counter()

    method: str = request.method
    path: str = request.url.path

    response = await call_next(request)

    elapsed_time: float = time.perf_counter()  - start_time
    request_uid: str = request.state.request_uid

    response_code = response.status_code

    logger.info(
        "[%s] %s %s -> %d (%.2f ms)",
        request_uid,
        method,
        path,
        response_code,
        elapsed_time*1000
    )

    return response
