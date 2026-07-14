
from app.models.auth_model import Role
from app.repositories.role_repository import RoleRepository

# RoleService
# assign_role()
# remove_role()
# get_roles()
# has_role()

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
            role_uid: str
    ) -> Role:
        
        return await self.role_repository.get_by_uid(
            role_uid=role_uid,
        )

    async def has_role(
            self,
            user_uid: str,
            required_roles: tuple[str],
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
            user_uid: str,
            required_roles: tuple[str],
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
            user_uid: str,
    ) -> list[str]:
        
        return await self.role_repository.get_user_role_names(
            user_uid=user_uid,
        )
