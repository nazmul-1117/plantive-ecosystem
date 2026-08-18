# service/admin/user_role_service.py

from uuid import UUID

from app.repositories.user_role_repository import UserRoleRepository
from app.models.auth_model import Role, UserRole


class AdminUserRoleService:

    def __init__(
            self,
            user_role_repository: UserRoleRepository
    ):
        self.user_role_repository = user_role_repository


    async def get_roles_by_uid(
            self,
            *,
            user_uid: UUID,
    ) -> list[Role]:
        
        return await self.user_role_repository.get_roles(
            user_uid=user_uid
        )