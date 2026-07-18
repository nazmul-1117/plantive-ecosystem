from uuid import uuid4
from fastapi import Request


async def request_uid_middleware(request: Request, call_next):
    
    request_uid: str = str(uuid4())

    request.state.request_uid = request_uid
    response = await call_next(request)

    response.headers["X-Request-UID"] = request_uid

    return response