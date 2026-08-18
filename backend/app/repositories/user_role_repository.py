from uuid import UUID

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.models.auth_model import UserRole, Role

class UserRoleRepository:

    def __init__(
            self,
            session: AsyncSession
    ):
        self.session = session
    
    async def assign_role(
            self,
            user_uid: UUID,
            role_uid: UUID,
    ):
        user_role_data = UserRole(
            user_uid=user_uid,
            role_uid=role_uid
        )

        self.session.add(user_role_data)

    async def get_roles(
            self,
            *,
            user_uid: UUID,
    ) -> list[Role]:
        
        statement = (
            select(Role)
            .join(
                UserRole,
                UserRole.role_uid == Role.role_uid,
            )
            .where(
                UserRole.user_uid == user_uid,
            )
            .order_by(Role.name)
        )
        result = await self.session.exec(statement)

        return result.all()

    async def remove_role():
        pass

    async def has_role():
        pass

    async def add_many(
            self,
            *,
            user_roles: list[UserRole]
    ) -> None:

        if not user_roles:
            return
        self.session.add_all(user_roles)

        await self.session.flush()



    async def commit(self) -> None:
        await self.session.commit()
    
    async def rollback(self) -> None:
        await self.session.rollback()
    
    async def refresh(self, obj) -> None:
        await self.session.refresh(obj)
