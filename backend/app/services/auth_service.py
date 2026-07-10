
import time
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from app.core.database import get_session
from sqlmodel import select, or_
from redis.asyncio import Redis

from app.schemas.auth_schema import UserCreate, LoginRequest
from app.schemas.token_schema import AccessTokenResponse
from app.models.auth_model import User, Role, UserRole
from app.services.token_service import TokenService

from app.core.jwt import create_token, decode_token
from app.core.security import generate_hash_password, verity_hashed_password

from app.repositories.user_repository import UserRepository
from app.repositories.role_repository import RoleRepository
from app.repositories.user_role_repository import UserRoleRepository


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
    
    async def register(
            self,
            user_data: UserCreate,
            session: AsyncSession
    ) -> User:
        
        user = await user_repository.get_by_email(
            email=user_data.email,
            session=session
        )
        
        if user is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email ALready Exist"
            )

        user = await user_repository.get_by_username(
            username=user_data.username,
            session=session
        )

        if user is not None:
            raise HTTPException(
                # use custom exceptionn get from exceptionn class
                status_code=status.HTTP_409_CONFLICT,
                detail="Email ALready Exist"
            )
        
        # user_data.password = generate_hash_password(user_data.password)
        user = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            avatar_url=user_data.avatar_url,
            bio=user_data.bio,
            username=user_data.username,
            password_hash=generate_hash_password(user_data.password)
        )

        user_table = await user_repository.create(
            user=user,
            session=session
        )

        role_table = await role_repository.get_by_name(
            role_name="user",
            session=session
        )

        if role_table is None:
            # use custom exceptionn get from exceptionn class
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Role is not in Database"
            )

        await user_role_repository.assign_role(
            user_uid=user_table.user_uid,
            role_uid=role_table.role_uid,
            session=session
        )

        try:
            await session.commit()
            await session.refresh(user_table)
        except:
            await session.rollback()
            raise

        return user_table

    async def login(
            self,
            login_credentials: LoginRequest,
            session: AsyncSession
    ) -> JSONResponse:
        
        user: User | None = await user_repository.get_by_username(
            username=login_credentials.username,
            session=session
        )

        if user is None or not verity_hashed_password(
            password=login_credentials.password,
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
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User Not Found"
            )
        
        new_access_token: str = create_token(
            user_uid=str(user.user_uid)
        )
        
        # return {
        #     "access_token": new_access_token,
        #     "token_type": "bearer"
        # }

        return AccessTokenResponse(
            access_token=new_access_token
        )
