from fastapi import APIRouter, status

from app.controllers.auth_controller import (
    create_user,
    login_user,
    create_new_access_token,
    revoke_token
)

auth_router = APIRouter()

auth_router.post(
    path="/signup",
    status_code=status.HTTP_201_CREATED
)(create_user)


auth_router.post(
    path="/login",
    status_code=status.HTTP_200_OK
)(login_user)


auth_router.post(
    path="/refresh",
    status_code=status.HTTP_200_OK
)(create_new_access_token)


auth_router.post(
    path="/logout",
    status_code=status.HTTP_200_OK
)(revoke_token)