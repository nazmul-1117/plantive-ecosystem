
# controllers/admin/user_controller.py -> admin controller

from uuid import UUID
from typing import Annotated

from fastapi import Depends

from app.services.role_service import RoleService
from app.services.admin.user_service import AdminUserService
from app.services.admin.user_role_service import AdminUserRoleService

from app.models.auth_model import User

from app.schemas.admin.user_schema import (
    AdminUserReadResponse,
    AdminUserUpdateRequest,
    AdminUserDeleteResponse,
    AdminUserListResponse,
    AdminUserListParams,
    AdminRoleResponse,
    AdminUserPasswordResetResponse,
    AdminUserPasswordResetRequest,
    AdminUserActivateResponse,
)
from app.schemas.admin.role_schema import AdminRoleReadResponse

from app.schemas.admin.user_role_schema import (
    AdminAssignUserRolesRequest
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

async def get_user_roles(
        user_uid: UUID,
        admin_user_role_service: Annotated[AdminUserRoleService, Depends(get_admin_user_role_service)],
        _: Annotated[User, Depends(require_roles(RoleConstant.ADMIN, RoleConstant.MODERATOR))],
) -> list[AdminRoleResponse]:
    
    return await admin_user_role_service.get_roles_by_uid(
        user_uid=user_uid
    )

async def assign_user_roles(
        user_uid: UUID,
        request: AdminAssignUserRolesRequest,
        admin_user_role_service: Annotated[AdminUserRoleService, Depends(get_admin_user_role_service)],
        _: Annotated[User, Depends(require_roles(RoleConstant.ADMIN, RoleConstant.MODERATOR))],
) -> list[AdminRoleResponse]:
    
    return await admin_user_role_service.assign_roles(
        user_uid=user_uid,
        role_uids=request.role_uids,
    )

async def get_roles(
        role_service: Annotated[RoleService, Depends(get_role_service)],
        _: Annotated[User, Depends(require_roles(RoleConstant.ADMIN, RoleConstant.MODERATOR))],
) -> list[AdminRoleReadResponse]:
    
    return await role_service.get_roles()

async def remove_user_role(
        user_uid: UUID,
        role_uid: UUID,
        admin_user_role_service: Annotated[AdminUserRoleService, Depends(get_admin_user_role_service)],
        _: Annotated[User, Depends(require_roles(RoleConstant.ADMIN))],
) -> None:

    await admin_user_role_service.remove_role(
        user_uid=user_uid,
        role_uid=role_uid,
    )

async def reset_user_password(
        user_uid: UUID,
        password_data: AdminUserPasswordResetRequest,
        admin_user_service: Annotated[AdminUserService, Depends(get_admin_user_service)],
        _: Annotated[User, Depends(require_roles(RoleConstant.ADMIN))],
) -> AdminUserPasswordResetResponse:
    
    return await admin_user_service.reset_user_password(
        user_uid=user_uid,
        password_data=password_data,
    )

async def activate_user(
        user_uid: UUID,
        admin_user_service: Annotated[AdminUserService, Depends(get_admin_user_service)],
        _: Annotated[User, Depends(require_roles(RoleConstant.ADMIN))],
) -> AdminUserActivateResponse:

    return await admin_user_service.activate_user(
        user_uid=user_uid
    )

async def deactivate_user(
        user_uid: UUID,
        admin_user_service: Annotated[AdminUserService, Depends(get_admin_user_service)],
        _: Annotated[User, Depends(require_roles(RoleConstant.ADMIN))],
) -> AdminUserActivateResponse:

    return await admin_user_service.deactivate_user(
        user_uid=user_uid
    )