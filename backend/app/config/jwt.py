import jwt
from datetime import datetime, timedelta, timezone
import uuid
from fastapi import HTTPException, status

from app.config.settings import settings


def create_token(
        user_uid: str,
        expires_delta: timedelta | None = None,
        token_type: str = "access"
):
    now = datetime.now(timezone.utc)

    if expires_delta is None:

        if token_type == "access":
            expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        elif token_type == "refresh":
            expires_delta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="invalid token type"
            )
        
    expire = now + expires_delta

    payload = {
        "sub": user_uid,
        "type": token_type,
        "iat": now,
        "exp": expire,
        "jti": str(uuid.uuid4())
    }

    return jwt.encode(
        payload=payload,
        key=settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )


def decode_token(token: str) -> dict:

    try:
        payload = jwt.decode(
            jwt=token,
            key=settings.JWT_SECRET,
            algorithms=settings.JWT_ALGORITHM
        )

        return payload
    
    except jwt.ExpiredSignatureError:
        raise ValueError("Token Expired")
    
    except jwt.InvalidTokenError:
        raise ValueError("Invalid Token")
