from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.models.auth_model import UserRole

class UserRoleRepository:

    def __init__(
            self,
            session: AsyncSession
    ):
        session = session
    
    async def assign_role(
            self,
            user_uid: str,
            role_uid: str,
    ):
        user_role_data = UserRole(
            user_uid=user_uid,
            role_uid=role_uid
        )

        self.session.add(user_role_data)

    async def get_roles(
            self,
            user_uid: str,
    ) -> list[UserRole]:
        
        statement = select(UserRole).where(UserRole.user_uid == user_uid)
        result = await self.session.exec(statement)

        return result.all()

    async def remove_role():
        pass

    async def has_role():
        pass

