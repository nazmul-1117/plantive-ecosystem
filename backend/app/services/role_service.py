from sqlmodel.ext.asyncio.session import AsyncSession
# from fastapi import Depends, HTTPException, status
from app.core.database import get_session
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

# from app.schemas.auth_schema import UserCreate, UserRead
from app.models.auth_model import Role, UserRole
# from app.core.security import generate_hash_password

# from app.repositories.user_repository import UserRepository
from app.repositories.role_repository import RoleRepository
# from app.repositories.user_role_repository import UserRoleRepository

# RoleService

# assign_role()
# remove_role()
# get_roles()
# has_role()

role_repository = RoleRepository()

class RoleService:
    async def assign_role():
        pass

    async def remove_role():
        pass

    async def get_role(
            self,
            role_uid: str,
            session: AsyncSession
    ) -> Role:
        
        return await role_repository.get_by_uid(
            role_uid=role_uid,
            session=session
        )

    async def has_role(
            self,
            user_uid: str,
            required_roles: tuple[str],
            session: AsyncSession
    ) -> bool:
        
        """
        :return boolean: True if user has at least one of the required roles
        """

        user_roles: list[str] = await role_repository.get_user_role_names(
            user_uid=user_uid,
            session=session
        )

        return bool(
            set(user_roles)
            .intersection(required_roles)
        )
    

    async def has_any_role(
            self,
            user_uid: str,
            required_roles: tuple[str],
            session: AsyncSession
    ) -> bool:
        
        """
        :return boolean: True if user has at least one of the required roles
        """

        return await role_repository.has_any_role(
            user_uid=user_uid,
            required_roles=required_roles,
            session=session
        )

    
    async def get_user_role_names(
            self,
            user_uid: str,
            session: AsyncSession
    ) -> list[str]:
        
        return await role_repository.get_user_role_names(
            user_uid=user_uid,
            session=session
        )
