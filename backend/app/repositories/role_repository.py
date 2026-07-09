from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, exists

from app.models.auth_model import Role
from app.schemas.auth_schema import UserCreate

class RoleRepository:
    async def get_by_uid(
            self,
            role_uid: str,
            session: AsyncSession
    ):
        pass

    async def get_by_name(
            self,
            role_name: str,
            session: AsyncSession
    ) -> Role | None:
        
        statement = select(Role).where(Role.name == role_name)
        result = await session.exec(statement)
        
        return result.first()

    async def list_roles(
            self,
            role_uid: str,
            session: AsyncSession
    ):
        pass