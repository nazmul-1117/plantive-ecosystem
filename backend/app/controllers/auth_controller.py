from typing import Annotated
import time

from sqlmodel.ext.asyncio.session import AsyncSession
from redis.asyncio import Redis
from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app.core.database import get_session
from app.dependencies.redis_dependency import get_redis
from app.schemas.auth_schema import UserCreate, UserRead, UserUpdate, LoginRequest
from app.services.auth_service import UserService
from app.services.token_service import TokenService
from app.core.security import verity_hashed_password
from app.models.auth_model import User
from app.core.jwt import create_token, decode_token
from app.dependencies.auth_dependency import verify_token


user_service = UserService()
token_service = TokenService()

async def create_user(
        user_data: UserCreate,
        session: AsyncSession = Depends(get_session)
):
    exist_user: User | None = await user_service.get_by_email_or_username(
        session=session,
        email=user_data.email,
        username=user_data.username
    )

    if exist_user is None:
        user: User | None = await user_service.create_user(user_data, session)

        if user is not None:
            return {
                "status": status.HTTP_201_CREATED,
                "details": "User created successfully",
                "data": user
            }

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="username or email already exist"
    )

async def login_user(
        login_data: LoginRequest,
        session: AsyncSession = Depends(get_session)
    ):
    
    user: User | None = await user_service.get_by_email_or_username(
        session=session,
        email="hey",
        username=login_data.username
    )

    if user is None or not verity_hashed_password(
        password=login_data.password,
        hashed_password=user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    access_token = create_token(
        user_uid= str(user.user_uid)
    )

    refresh_token = create_token(
        user_uid= str(user.user_uid),
        token_type="refresh"
    )

    return JSONResponse(
        content={
            "message": "login successfull :)",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": {
                "user_uid": str(user.user_uid),
                "username": user.username,
                "email": user.email
            }
        }
    )


async def create_new_access_token(
        token_payload: Annotated[dict, Depends(verify_token)],
        session: Annotated[AsyncSession, Depends(get_session)]
 ) -> dict:
    
    if token_payload.get('type') != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh Token Required"
        )
    
    user: User | None = await user_service.get_by_uid(
        user_uid=token_payload['sub'],
        session=session
    )

    if token_payload.get('type') != "refresh" or user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User Not Found"
        )
    
    new_access_token: str =  create_token(
        user_uid=str(user.user_uid)
    )
    
    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }


async def revoke_token(
    token_payload: Annotated[dict, Depends(verify_token)],
    redis: Annotated[Redis, Depends(get_redis)]  
):
    
    jti: str = token_payload['jti']
    ttl: int = max(1, token_payload['exp'] - int(time.time()))
    
    await token_service.revoke_token(
        jti=jti,
        ttl=ttl,
        redis=redis
    )

    return{
        "message": "logged out successfully"
    }


