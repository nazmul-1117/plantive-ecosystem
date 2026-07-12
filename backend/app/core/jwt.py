import uuid
import time
from typing import Literal
from datetime import timedelta

import jwt

from app.core.config import settings
from app.schemas.token_schema import TokenPayload


def create_token(
        user_uid: str,
        expires_delta: timedelta | None = None,
        token_type: Literal["access", "refresh"] = "access"
) -> str:
    
    if expires_delta is None:

        if token_type == "access":
            expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        elif token_type == "refresh":
            expires_delta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    now = int(time.time())
    expire = now + int(expires_delta.total_seconds())

    payload = {
        "sub": user_uid,
        "type": token_type,
        "iat": now,
        "exp": expire,
        "jti": str(uuid.uuid4()),
        "iss": settings.JWT_ISSUER,
        "aud": settings.JWT_AUDIENCE
    }

    return jwt.encode(
        payload=payload,
        key=settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )


def decode_token(token: str) -> TokenPayload:

    payload = jwt.decode(
            jwt=token,
            key=settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
            issuer= settings.JWT_ISSUER,
            audience=settings.JWT_AUDIENCE
        )
    return TokenPayload.model_validate(payload)
