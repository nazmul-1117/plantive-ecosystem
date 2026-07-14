from fastapi import Depends
from typing import Annotated

from app.dependencies.auth_dependency import get_refresh_token_payload, get_access_token_payload
from app.dependencies.service_dependency import get_auth_service, get_user_service

from app.services.auth_service import AuthService
from app.services.user_service import UserService

from app.models.auth_model import User

from app.schemas.auth_schema import UserCreate, LoginRequest, LoginResponse, UserResponse, UserRead, LogoutResponse
from app.schemas.token_schema import AccessTokenResponse, TokenPayload


async def register_user(
        user_data: UserCreate,
        user_service: Annotated[UserService, Depends(get_user_service)]
) -> UserResponse:
    
    user: User = await user_service.register_user(user_data)

    return UserResponse(
        success=True,
        message="User created successfully",
        data=UserRead.model_validate(user)
    )


async def login_user(
        login_data: LoginRequest,
        auth_service: Annotated[AuthService, Depends(get_auth_service)]
) -> LoginResponse:
    
    return await auth_service.login(
        login_credentials=login_data,
    )


async def refresh_access_token(
        token_payload: Annotated[TokenPayload, Depends(get_refresh_token_payload)],
        auth_service: Annotated[AuthService, Depends(get_auth_service)]
 ) -> AccessTokenResponse:
    
    return await auth_service.refresh_access_token(
        token_payload=token_payload,
    )


async def logout_user(
    token_payload: Annotated[TokenPayload, Depends(get_access_token_payload)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
) -> LogoutResponse:
    
    return await auth_service.logout(
        token_payload=token_payload,
    )
