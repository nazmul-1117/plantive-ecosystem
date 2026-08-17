from uuid import UUID

from app.models.auth_model import Role
from app.repositories.role_repository import RoleRepository

from app.constants.roles_constant import RoleConstant

class RoleService:

    def __init__(
            self,
            role_repository: RoleRepository,
    ):
    
        self.role_repository = role_repository
        
        
    async def assign_role():
        pass

    async def remove_role():
        pass

    async def get_role(
            self,
            role_uid: UUID
    ) -> Role:
        
        return await self.role_repository.get_by_uid(
            role_uid=role_uid,
        )

    async def has_role(
            self,
            user_uid: UUID,
            required_roles: tuple[RoleConstant, ...],
    ) -> bool:
        
        """
        :return boolean: True if user has at least one of the required roles
        """

        user_roles: list[str] = await self.role_repository.get_user_role_names(
            user_uid=user_uid,
        )

        return bool(
            set(user_roles)
            .intersection(required_roles)
        )
    

    async def has_any_role(
            self,
            user_uid: UUID,
            required_roles: tuple[RoleConstant, ...],
    ) -> bool:
        
        """
        :return boolean: True if user has at least one of the required roles
        """

        return await self.role_repository.has_any_role(
            user_uid=user_uid,
            required_roles=required_roles,
        )

    
    async def get_user_role_names(
            self,
            user_uid: UUID,
    ) -> list[str]:
        
        return await self.role_repository.get_user_role_names(
            user_uid=user_uid,
        )
