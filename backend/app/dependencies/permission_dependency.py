# file: app.dependencies.permission_dependency.py

from typing import Annotated
from fastapi import Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.dependencies.auth_dependency import get_current_verified_user
from app.models.auth_model import User
from app.core.database import get_session

from app.services.role_service import RoleService

from app.exceptions.auth_exception import PermissionDenied
from app.dependencies.service_dependency import get_role_service

from app.constants.roles_constant import RoleConstant


def require_roles(
        *required_roles: RoleConstant
):
    
    async def checker(
            current_user: Annotated[User, Depends(get_current_verified_user)],
            role_service: Annotated[RoleService, Depends(get_role_service)]
    ) -> User:

        has_role = await role_service.has_any_role(
            user_uid=current_user.user_uid,
            required_roles=required_roles,
        )

        if not has_role:
            raise PermissionDenied()
        
        return current_user
    return checker

# async def require_permissions(
#         *required_permissions: PermissionConstant,
# ):
#     async def checker(
#             current_user: Annotated[User, Depends(get_current_verified_user)],
#             permission_service: Annotated[Permissionervice, Depends(get_permission_service)]
#     ) -> User:

#         has_permission = await permission_service.has_any_permission(
#             user_uid=current_user.user_uid,
#             required_permissions=required_permissions,
#         )

#         if not has_permission:
#             raise PermissionDenied()
        
#         return current_user
#     return checker
