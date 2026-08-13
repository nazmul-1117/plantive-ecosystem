from typing import Annotated

from fastapi import Depends

from app.dependencies.auth_dependency import get_current_active_user
from app.services.user_service import UserService

from app.models.auth_model import User
from app.schemas.user_schema import UserReadResponse, UserUpdateRequest, UserUpdateResponse, UserDeleteRequest, UserDeleteResponse

from app.dependencies.auth_dependency import get_current_active_user
from app.dependencies.service_dependency import get_user_service


async def get_me(
        current_user: Annotated[User, Depends(get_current_active_user)],
) -> UserReadResponse:

    return UserReadResponse.model_validate(current_user)

async def update_profile(
        update_data: UserUpdateRequest,
        current_user: Annotated[User, Depends(get_current_active_user)],
        user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserUpdateResponse:

    user: User = await user_service.update_profile(
        user = current_user,
        update_data = update_data
    )

    return UserUpdateResponse(
        user=UserReadResponse.model_validate(user)
    )

async def delete_me(
        delete_data: UserDeleteRequest,
        current_user: Annotated[User, Depends(get_current_active_user)],
        user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserDeleteResponse:

    return await user_service.delete_account(
        user=current_user,
        delete_data=delete_data
    )