from fastapi import APIRouter, status
from app.schemas.token_schema import AccessTokenResponse
from app.schemas.auth_schema import LoginResponse, LogoutResponse, UserResponse, EmailVerificationResponse
from app.schemas.password_reset_schema import ForgotPasswordResponseSchema, ResetPasswordResponseSchema

from app.controllers.auth_controller import (
    register_user,
    login_user,
    refresh_access_token,
    logout_user,
    verify_email,
    forgot_password,
    reset_password
)

auth_router = APIRouter()

auth_router.post(
    path="/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
    summary="Create new account"
)(register_user)


auth_router.post(
    path="/login",
    status_code=status.HTTP_200_OK,
    response_model=LoginResponse,
    summary="Input login credential and login"
)(login_user)


auth_router.post(
    path="/refresh-token",
    status_code=status.HTTP_200_OK,
    response_model=AccessTokenResponse,
    summary="generate new access token through refresh token"
)(refresh_access_token)


auth_router.post(
    path="/logout",
    status_code=status.HTTP_200_OK,
    response_model=LogoutResponse,
    summary="endpoint for logged out"
)(logout_user)


auth_router.get(
    path="/verify-email",
    status_code=status.HTTP_200_OK,
    response_model=EmailVerificationResponse,
    summary="Verify account email address"
)(verify_email)


auth_router.post(
    path="/forgot-password",
    status_code=status.HTTP_200_OK,
    response_model=ForgotPasswordResponseSchema,
    summary="Forgot password"
)(forgot_password)


auth_router.post(
    path="/reset-password",
    status_code=status.HTTP_200_OK,
    response_model=ResetPasswordResponseSchema,
    summary="take token and reset password",
)(reset_password)