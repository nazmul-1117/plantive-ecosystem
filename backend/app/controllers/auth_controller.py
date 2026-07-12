from typing import Annotated
from sqlmodel.ext.asyncio.session import AsyncSession
from redis.asyncio import Redis
from fastapi import Depends, HTTPException, status

from app.models.auth_model import User
from app.core.database import get_session
from app.dependencies.redis_dependency import get_redis
from app.schemas.auth_schema import UserCreate, LoginRequest, LoginResponse
from app.schemas.token_schema import AccessTokenResponse
from app.dependencies.auth_dependency import get_refresh_token_payload, get_access_token_payload

from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.services.token_service import TokenService
from app.services.role_service import RoleService


user_service = UserService()
auth_service = AuthService()
token_service = TokenService()
role_service = RoleService()

async def register_user(
        user_data: UserCreate,
        session: AsyncSession = Depends(get_session)
) -> dict:
    
    # suggestion:
    #     try:
    #         user = await auth_service.create_user(...)
    #     except EmailAlreadyExists:
    #         raise HTTPException(
    #             status_code=409,
    #             detail="Email already exists"
    #         )
    
    try:
        
        user: User = await user_service.register_user(user_data, session)

        return {
            "status": status.HTTP_201_CREATED,
            "details": "User created successfully",
            "data": user
        }
    
    except:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user not created"
        )


async def login_user(
        login_data: LoginRequest,
        session: AsyncSession = Depends(get_session)
) -> LoginResponse:
    
    return await auth_service.login(
        login_credentials=login_data,
        session=session
    )


async def refresh_access_token(
        token_payload: Annotated[dict, Depends(get_refresh_token_payload)],
        session: Annotated[AsyncSession, Depends(get_session)]
 ) -> AccessTokenResponse:
    
    try:
        return await auth_service.refresh_access_token(
            token_payload=token_payload,
            session=session
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="access token create failed"
        )


async def logout_user(
    token_payload: Annotated[dict, Depends(get_access_token_payload)],
    redis: Annotated[Redis, Depends(get_redis)]  
):
    try:
        return await auth_service.logout(
            token_payload=token_payload,
            redis=redis
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user do not logged out"
        )

