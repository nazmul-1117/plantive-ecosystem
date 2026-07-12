from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel.ext.asyncio.session import AsyncSession
from redis.asyncio import Redis

import jwt

from app.core.config import settings
from app.core.database import get_session
from app.core.jwt import decode_token

from app.services.user_service import UserService
from app.services.token_service import TokenService
from app.schemas.token_schema import TokenPayload

from app.models.auth_model import User
from app.services.token_service import TokenService
from app.dependencies.redis_dependency import get_redis

from app.exceptions.auth_exception import (
    ExpiredAccessToken,
    InvalidAccessToken,
    AccessTokenRequired,
    RefreshTokenRequired
)
from app.exceptions.user_exception import(
    UserNotFound,
    UserInactive
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f'/api/{settings.API_VERSION}/auth/login')
user_service = UserService()
token_service = TokenService()



async def verify_token(
        token: Annotated[str, Depends(oauth2_scheme)],
        redis: Annotated[Redis, Depends(get_redis)]
) -> TokenPayload:
    
    """
    Verify Token data and return Payload

    :param token: Dependecy -> token from request header
    :param redis: Dependecy -> get redis from redis library
    :return: dict: Token payload 
    :raise: unauthorized error
    """
    
    try: 
        token_payload: TokenPayload = decode_token(token)
    
    except jwt.InvalidSignatureError:
        raise ExpiredAccessToken()
    
    except jwt.InvalidTokenError:
        raise InvalidAccessToken()

    if await token_service.is_revoked(
        jti=token_payload.jti,
        redis=redis
    ):
        raise ExpiredAccessToken()
    
    return token_payload


async def get_access_token_payload(
        payload: Annotated[TokenPayload, Depends(verify_token)]
) -> TokenPayload:
    
    """
    Validate that provider JWT is a valid access token
    and return it's payload
    """

    if payload.type != "access":
        raise AccessTokenRequired()
    
    return payload


async def get_refresh_token_payload(
        payload: Annotated[TokenPayload, Depends(verify_token)]
) -> TokenPayload:
    
    """
    Validate that provider JWT is a valid refresh token
    and return it's payload
    """

    if payload.type != "refresh":
        raise RefreshTokenRequired()
    
    return payload


async def get_current_user(
        session: Annotated[AsyncSession, Depends(get_session)],
        payload: Annotated[TokenPayload, Depends(get_access_token_payload)]
) -> User:
    
    """
    Return: Authenticate the current requrest and return current user
    
    Raise: if something wrong, raise a value exception
    """

    user_uid: str = payload.sub
    user: User = await user_service.get_by_uid(user_uid, session)

    if user is None:
        raise UserNotFound()
    
    return user
    

async def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    
    """
    Ensure authenticate user is active
    """

    if not current_user.is_active:
        raise UserInactive()
    
    return current_user
