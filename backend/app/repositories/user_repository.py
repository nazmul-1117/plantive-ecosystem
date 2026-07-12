from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, exists

from app.models.auth_model import User

class UserRepository:
    async def create(
            self,
            user: User,
            session: AsyncSession
    ) -> User:
        
        session.add(user)
        await session.flush()

        return user


    async def delete():
        pass

    async def update():
        pass

    async def get_by_uid(
            self,
            user_uid: str,
            session: AsyncSession
    ) -> User | None:
        
        statement = select(User).where(User.user_uid == user_uid)
        result = await session.exec(statement)
        return result.first()

    async def get_by_email(
            self,
            email: str,
            session: AsyncSession
    ) -> User | None:
        
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        return result.first()

    async def get_by_username(
            self,
            username: str,
            session: AsyncSession
    ) -> User | None:
        
        statement = select(User).where(User.username == username)
        result = await session.exec(statement)
        return result.first()

    async def exists_by_email(
            self,
            email: str,
            session: AsyncSession
    ) -> bool:
        statement = select(
            exists().
            where(User.email == email)
        )
        result = await session.exec(statement)

        return result.one()


    async def exists_by_username(
            self,
            username: str,
            session: AsyncSession
    ) -> bool:
        
        statement = select(
            exists().
            where(User.username == username)
        )
        
        result = await session.exec(statement)
        return result.one()

    async def get_by_email_username():
        pass