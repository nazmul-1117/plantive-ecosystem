from fastapi import APIRouter, status
from app.schemas.token_schema import AccessTokenResponse
from app.schemas.auth_schema import LoginResponse, LogoutResponse, UserResponse

from app.controllers.auth_controller import (
    register_user,
    login_user,
    refresh_access_token,
    logout_user
)

auth_router = APIRouter()

auth_router.post(
    path="/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse
)(register_user)


auth_router.post(
    path="/login",
    status_code=status.HTTP_200_OK,
    response_model=LoginResponse
)(login_user)


auth_router.post(
    path="/refresh",
    status_code=status.HTTP_200_OK,
    response_model=AccessTokenResponse
)(refresh_access_token)


auth_router.post(
    path="/logout",
    status_code=status.HTTP_200_OK,
    response_model=LogoutResponse
)(logout_user)