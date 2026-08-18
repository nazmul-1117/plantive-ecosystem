# service/admin/user_role_service.py

from uuid import UUID
from sqlalchemy.exc import SQLAlchemyError

from app.repositories.user_role_repository import UserRoleRepository
from app.repositories.user_repository import UserRepository
from app.repositories.role_repository import RoleRepository
from app.models.auth_model import Role, UserRole, User

from app.exceptions.user_exception import (
    UserNotFound
)
from app.exceptions.role_exception import RoleNotFound, RoleAlreadyUsed


class AdminUserRoleService:

    def __init__(
            self,
            user_repository: UserRepository,
            role_repository: RoleRepository,
            user_role_repository: UserRoleRepository,
    ):
        self.user_repository = user_repository
        self.role_repository = role_repository
        self.user_role_repository = user_role_repository

    async def assign_roles(
            self,
            *,
            user_uid: UUID,
            role_uids: list[UUID],
    ) -> list[Role]:

        # 1. Verify user exists or not
        user = self.user_repository.get_by_uid(
            user_uid=user_uid,
        )

        if user is None:
            raise UserNotFound()

        # 2. Remove Duplicate role UIDs from request
        unique_role_uids = list(dict.fromkeys(role_uids))

        # 3. Verify requested roles exists
        roles = await self.role_repository.get_by_uids(
            role_uids=unique_role_uids,
        )

        if len(unique_role_uids) != len(roles):
            raise RoleNotFound()

        # 4. Get roles user already has
        existing_roles = (
            await self.user_role_repository.get_roles(
                user_uid=user_uid
            )
        )

        existing_role_uids = {
            user_role.role_uid
            for user_role in existing_roles
        }

        # 5. Determine roles that actually need assignment
        new_role_uids = [
            role_uid
            for role_uid in unique_role_uids
            if role_uid not in existing_role_uids
        ]

        # 6. Create relationships
        user_roles = [
            UserRole(
                user_uid=user_uid,
                role_uid=role_uid
            )
            for role_uid in new_role_uids
        ]

        if not user_roles:
            raise RoleAlreadyUsed()
        
        await self.user_role_repository.add_many(
            user_roles=user_roles
        )


        try:
            await self.user_role_repository.commit()

        except SQLAlchemyError:
            await self.user_repository.rollback()
            raise

        # 7. Return resulting roles
        return roles

    

    async def get_roles_by_uid(
            self,
            *,
            user_uid: UUID,
    ) -> list[Role]:
        
        return await self.user_role_repository.get_roles(
            user_uid=user_uid
        )