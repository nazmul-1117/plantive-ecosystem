import logging

from fastapi.requests import Request

logger = logging.getLogger(__name__)

async def exception_logging_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    
    except Exception:
        logger.exception(
            "[%s] %s %s -> Unhandled Exception",
            request.state.request_uid,
            request.method,
            request.url.path
        )
