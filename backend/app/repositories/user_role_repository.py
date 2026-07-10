from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, exists

from app.models.auth_model import Role, User, UserRole

class UserRoleRepository:
    
    async def assign_role(
            self,
            user_uid: str,
            role_uid: str,
            session: AsyncSession
    ):
        user_role_data = UserRole(
            user_uid=user_uid,
            role_uid=role_uid
        )

        session.add(user_role_data)

    async def get_roles(
            self,
            user_uid: str,
            session: AsyncSession
    ) -> list[UserRole]:
        
        statement = select(UserRole).where(UserRole.user_uid == user_uid)
        result = await session.exec(statement)

        return result.all()

    async def remove_role():
        pass

    async def has_role():
        pass


        