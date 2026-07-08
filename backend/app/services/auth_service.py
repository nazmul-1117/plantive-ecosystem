
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends
from app.core.database import get_session
from sqlmodel import select, or_

from app.schemas.auth_schema import UserCreate, UserRead
from app.models.auth_model import User
from app.core.security import generate_hash_password

class UserService:
    async def get_by_email_or_username(
            self,
            session: AsyncSession,
            email: str | None = "None",
            username: str | None = None
    ):
        statement = select(User).where(or_(User.email == email, User.username == username))
        result = await session.exec(statement)
        return result.first()
        
    async def create_user(
            self,
            user_data: UserCreate,
            session: AsyncSession
    ) -> User:
        
        password_hash: str = generate_hash_password(user_data.password)

        user = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            avatar_url=user_data.avatar_url,
            bio=user_data.bio,
            username=user_data.username,
            password_hash=password_hash
        )

        session.add(user)
        await session.commit()
        await session.refresh(user)

        return user
    
    async def get_by_uid(
            self,
            user_uid: str,
            session: AsyncSession,
    ) -> User | None:
        statement = select(User).where(User.user_uid == user_uid)
        result = await session.exec(statement)
        user: User = result.first()

        return user
