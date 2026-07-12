
import time
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from app.core.database import get_session
from sqlmodel import select, or_
from sqlalchemy.exc import SQLAlchemyError
from redis.asyncio import Redis

import jwt

from app.schemas.auth_schema import UserCreate, LoginRequest, LoginResponse
from app.schemas.token_schema import AccessTokenResponse

from app.models.auth_model import User, Role, UserRole
from app.services.token_service import TokenService

from app.core.jwt import create_token, decode_token
from app.core.security import generate_hash_password, verity_hashed_password

from app.repositories.user_repository import UserRepository
from app.repositories.role_repository import RoleRepository
from app.repositories.user_role_repository import UserRoleRepository

from app.exceptions.user_exception import (
    UserNotFound,
    EmailAlreadyExists,
    UsernameAlreadyExists
)
from app.exceptions.auth_exception import InvalidLoginCredential
from app.exceptions.role_exception import RoleNotFound


"""
AuthService.register()

↓

user_repository.get_by_email()

↓

user_repository.get_by_username()

↓

hash password

↓

User(...)

↓

user_repository.create()

↓

role_repository.get_by_name()

↓

user_role_repository.assign()

↓

commit()

↓

return user
"""

user_repository = UserRepository()
role_repository = RoleRepository()
user_role_repository = UserRoleRepository()
token_service = TokenService()

# AuthService
    # register()
    # login()
    # logout()
    # refresh_token()

class AuthService:
    
    async def login(
            self,
            login_credentials: LoginRequest,
            session: AsyncSession
    ) -> LoginResponse:
        
        user: User | None = await user_repository.get_by_username(
            username=login_credentials.username,
            session=session
        )

        if user is None or not verity_hashed_password(
            password=login_credentials.password,
            hashed_password=user.password_hash
        ):
            raise InvalidLoginCredential()

        access_token: str = create_token(
            user_uid= str(user.user_uid)
        )

        refresh_token: str = create_token(
            user_uid= str(user.user_uid),
            token_type="refresh"
        )

        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer"
        )

    async def logout(
            self,
            token_payload: dict,
            redis: Redis
    ) -> dict:
        
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

    async def refresh_access_token(
            self,
            token_payload: dict,
            session: AsyncSession
    ) -> AccessTokenResponse:
        
        user: User | None = await user_repository.get_by_uid(
            user_uid=token_payload['sub'],
            session=session
        )

        if user is None:
            raise UserNotFound()
        
        new_access_token: str = create_token(
            user_uid=str(user.user_uid)
        )

        return AccessTokenResponse(
            access_token=new_access_token
        )
