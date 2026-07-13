from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

import jwt

from app.core.config import settings
from app.core.jwt import decode_token

from app.services.user_service import UserService
from app.services.token_service import TokenService
from app.schemas.token_schema import TokenPayload

from app.models.auth_model import User

from app.exceptions.auth_exception import (
    ExpiredAccessToken,
    InvalidAccessToken,
    AccessTokenRequired,
    RefreshTokenRequired,
    RevokedAccessToken
)
from app.exceptions.user_exception import(
    UserNotFound,
    UserInactive
)

from app.dependencies.service_dependency import (
    get_user_service,
    get_token_service
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f'/api/{settings.API_VERSION}/auth/login')


async def verify_token(
        token: Annotated[str, Depends(oauth2_scheme)],
        token_service: Annotated[TokenService, Depends(get_token_service)]
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

    except jwt.ExpiredSignatureError:
        raise ExpiredAccessToken()
    
    except jwt.InvalidSignatureError:
        raise InvalidAccessToken()
    
    except jwt.InvalidTokenError:
        raise InvalidAccessToken()

    if await token_service.is_revoked(token_payload.jti):
        raise RevokedAccessToken()
    
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
        payload: Annotated[TokenPayload, Depends(get_access_token_payload)],
        user_service: Annotated[UserService, Depends(get_user_service)]
) -> User:
    
    """
    Return: Authenticate the current requrest and return current user
    
    Raise: if something wrong, raise a value exception
    """

    user_uid: str = payload.sub
    user: User | None = await user_service.get_by_uid(user_uid)

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
