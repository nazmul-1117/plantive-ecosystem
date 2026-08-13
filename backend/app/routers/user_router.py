from fastapi import APIRouter, status

from app.schemas.user_schema import UserUpdateResponse, UserReadResponse, UserDeleteResponse

from app.controllers.user_controllers import (
    get_me,
    update_profile,
    delete_me
)

user_router = APIRouter()
admin_user_router = APIRouter()

# user
user_router.get(
    path="/me",
    status_code=status.HTTP_200_OK,
    response_model=UserReadResponse,
    summary="Get current user's profile"
)(get_me)


user_router.patch(
    path="/me",
    status_code=status.HTTP_200_OK,
    response_model=UserUpdateResponse,
    summary="Update current user's profile"
)(update_profile)


user_router.delete(
    path="/me",
    status_code=status.HTTP_200_OK,
    response_model=UserDeleteResponse,
    summary="Delete current user's account"
)(delete_me)