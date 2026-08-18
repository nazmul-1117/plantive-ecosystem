
# controllers/admin/user_controller.py -> admin controller

from uuid import UUID
from typing import Annotated

from fastapi import Depends, Query

from app.services.user_service import UserService
from app.services.role_service import RoleService
from app.services.admin.user_service import AdminUserService
from app.services.admin.user_role_service import AdminUserRoleService

from app.models.auth_model import User, Role, UserRole
from app.schemas.admin.user_schema import (
    AdminUserReadResponse,
    AdminUserUpdateRequest,
    AdminUserDeleteResponse,
    AdminUserListResponse,
    AdminUserListParams,
    AdminRoleResponse
)

from app.dependencies.service_dependency import (
    get_admin_user_service,
    get_admin_user_role_service,
    get_role_service
)
from app.dependencies.permission_dependency import require_roles

from app.constants.roles_constant import RoleConstant

async def get_users(
        params: Annotated[AdminUserListParams, Depends()],
        admin_user_service: Annotated[AdminUserService, Depends(get_admin_user_service)],
        _: Annotated[User, Depends(require_roles(RoleConstant.ADMIN, RoleConstant.MODERATOR))],
) -> AdminUserListResponse:

    return await admin_user_service.list_users(
        params=params
    )

async def get_user_by_uid(
        user_uid: UUID,
        admin_user_service: Annotated[AdminUserService, Depends(get_admin_user_service)],
        _: Annotated[User, Depends(require_roles(RoleConstant.ADMIN, RoleConstant.MODERATOR))],
) -> AdminUserReadResponse:

    return await admin_user_service.get_user_by_uid(
        user_uid=user_uid
    )

async def update_user(
        user_uid: UUID,
        update_data: AdminUserUpdateRequest,
        admin_user_service: Annotated[AdminUserService, Depends(get_admin_user_service)],
        _: Annotated[User, Depends(require_roles(RoleConstant.ADMIN, RoleConstant.MODERATOR))],
) -> AdminUserReadResponse:

    user: User = await admin_user_service.get_user_by_uid(user_uid)

    return await admin_user_service.update_user(
        user = user,
        update_data = update_data
    )

async def delete_user(
        user_uid: UUID,
        admin_user_service: Annotated[AdminUserService, Depends(get_admin_user_service)],
        _: Annotated[User, Depends(require_roles(RoleConstant.ADMIN))],
) -> AdminUserDeleteResponse:

    user: User = await admin_user_service.get_user_by_uid(user_uid)

    return await admin_user_service.delete_user(
        user=user
    )


async def get_roles(
        user_uid: UUID,
        admin_user_role_service: Annotated[AdminUserRoleService, Depends(get_admin_user_role_service)],
        _: Annotated[User, Depends(require_roles(RoleConstant.ADMIN))],
) -> list[AdminRoleResponse]:
    
    return await admin_user_role_service.get_roles_by_uid(
        user_uid=user_uid
    )

