from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, exists

from app.models.auth_model import Role, UserRole

class RoleRepository:

    def __init__(
            self,
            session: AsyncSession
    ):
        self.session = session

    async def get_by_uid(
            self,
            role_uid: str,
    ) -> Role | None:
        
        statement = select(Role).where(Role.role_uid == role_uid)
        result = await self.session.exec(statement)

        return result.first()

    async def get_by_name(
            self,
            role_name: str,
    ) -> Role | None:
        
        statement = select(Role).where(Role.name == role_name)
        result = await self.session.exec(statement)
        
        return result.first()

    async def list_roles(
            self,
            role_uid: str,
    ):
        pass

    async def get_user_role_names(
            self,
            user_uid: str,
    ) -> list[str]:
        
        statement = (
            select(Role.name)
            .join(UserRole, UserRole.role_uid == Role.role_uid)
            .where(UserRole.user_uid == user_uid)
        )

        result = await self.session.exec(statement)
        
        return result.all()
    
    async def has_any_role(
            self,
            user_uid: str,
            required_roles: tuple[str],
    ) -> bool:
        
        statement = (
            select(UserRole)
            .join(Role, UserRole.role_uid == Role.role_uid)
            .where(UserRole.user_uid == user_uid)
            .where(Role.name.in_(required_roles))
            .limit(1)
        )

        result = await self.session.exec(statement)

        return result.first() is not None
    
