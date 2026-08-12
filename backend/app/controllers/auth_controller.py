from fastapi import Depends, Query, BackgroundTasks
from typing import Annotated

from app.dependencies.auth_dependency import get_refresh_token_payload, get_access_token_payload, get_current_active_user
from app.dependencies.service_dependency import get_auth_service, get_user_service, get_email_service, get_token_service

from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.services.email_service import EmailService

from app.models.auth_model import User

from app.schemas.token_schema import AccessTokenResponse, TokenPayload
from app.schemas.auth_schema import UserCreate, LoginRequest, LoginResponse, UserResponse, UserRead, LogoutResponse, EmailVerificationResponse, ChangePasswordRequest, ChangePasswordResponse
from app.schemas.password_reset_schema import ResetPasswordRequestSchema, ForgotPasswordRequestSchema, ForgotPasswordResponseSchema, ResetPasswordResponseSchema

import logging
logger = logging.getLogger(__name__)


async def register_user(
        background_task: BackgroundTasks,
        user_data: UserCreate,
        user_service: Annotated[UserService, Depends(get_user_service)],
        email_service: Annotated[EmailService, Depends(get_email_service)],
) -> UserResponse:
    
    user, verification_url = await user_service.register_user(user_data)

    background_task.add_task(
        email_service.send_verification_email,
        email=user.email,
        verification_url=verification_url
    )
    
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

async def verify_email(
        user_service: Annotated[UserService, Depends(get_user_service)],
        token: str = Query(..., description="The raw verification token from the email link"),
) -> EmailVerificationResponse:
    
    user: User = await user_service.verify_email(token)
    
    return EmailVerificationResponse(
        message="Email Verified Successfully",
        email=user.email
    )

async def forgot_password(
        background_task: BackgroundTasks,
        user_service: Annotated[UserService, Depends(get_user_service)],
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        email_service: Annotated[EmailService, Depends(get_email_service)],
        forgot_data: ForgotPasswordRequestSchema,
) -> ForgotPasswordResponseSchema:
    
    email: str = forgot_data.email
    user: User = await user_service.get_by_email(email)

    response, reset_url = await auth_service.forgot_password(user)

    background_task.add_task(
        email_service.send_password_reset_email,
        email=email,
        reset_url=reset_url
    )

    return response

async def reset_password(
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        reset_data: ResetPasswordRequestSchema,
        token: str = Query(..., description="Raw password reset token from the email link"),
) -> ResetPasswordResponseSchema:
    
    return await auth_service.reset_password(
        reset_data=reset_data,
        raw_token=token
    )

async def change_password(
        password_data: ChangePasswordRequest,
        user_service: Annotated[UserService, Depends(get_user_service)],
        token_payload: Annotated[TokenPayload, Depends(get_access_token_payload)],
) -> ChangePasswordResponse:

    return await user_service.change_password(
        password_data = password_data,
        user_uid = token_payload.sub,
    )
    
async def get_me(
        current_user: Annotated[User, Depends(get_current_active_user)],
) -> UserRead:

    return UserRead.model_validate(current_user)