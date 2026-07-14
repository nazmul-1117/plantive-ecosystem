# file: app.dependencies.permission_dependency.py

from typing import Annotated
from fastapi import Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.dependencies.auth_dependency import get_current_active_user
from app.models.auth_model import User
from app.core.database import get_session

from app.services.role_service import RoleService

from app.exceptions.auth_exception import PermissionDenied
from app.dependencies.service_dependency import get_role_service


def require_roles(
        *required_roles: str
):
    
    async def checker(
            current_user: Annotated[User, Depends(get_current_active_user)],
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

async def require_permissions(*permissions):
    pass
