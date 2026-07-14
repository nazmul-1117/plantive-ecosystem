from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, exists
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.auth_model import User

class UserRepository:

    def __init__(
            self,
            session: AsyncSession
    ):
        self.session = session
        
    async def create(
            self,
            user: User,
    ) -> User:
        
        self.session.add(user)
        await self.session.flush()

        return user

    async def delete():
        pass

    async def update():
        pass

    async def get_by_uid(
            self,
            user_uid: str,
    ) -> User | None:
        
        statement = select(User).where(User.user_uid == user_uid)
        result = await self.session.exec(statement)
        return result.first()

    async def get_by_email(
            self,
            email: str,
    ) -> User | None:
        
        statement = select(User).where(User.email == email)
        result = await self.session.exec(statement)
        return result.first()

    async def get_by_username(
            self,
            username: str,
    ) -> User | None:
        
        statement = select(User).where(User.username == username)
        result = await self.session.exec(statement)
        return result.first()

    async def exists_by_email(
            self,
            email: str,
    ) -> bool:
        statement = select(
            exists().
            where(User.email == email)
        )
        result = await self.session.exec(statement)

        return result.one()

    async def exists_by_username(
            self,
            username: str,
    ) -> bool:
        
        statement = select(
            exists().
            where(User.username == username)
        )
        
        result = await self.session.exec(statement)
        return result.one()

    async def get_by_email_username():
        pass
    
    async def commit(self) -> None:
        await self.session.commit()
    
    async def rollback(self) -> None:
        await self.session.rollback()
    
    async def refresh(self, obj) -> None:
        await self.session.refresh(obj)

