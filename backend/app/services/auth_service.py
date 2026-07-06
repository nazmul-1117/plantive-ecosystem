
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends
from app.config.database import get_session
from sqlmodel import select, or_

from app.schemas.auth_schema import UserCreate, UserRead
from app.models.auth import User
from app.config.security import generate_hash_password

class UserService:
    async def get_by_email_or_username(
            self,
            session: AsyncSession,
            email: str | None = None,
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
        
        password_hashed = generate_hash_password(user_data.plain_password)

        user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            username=user_data.username,
            password_hashed=password_hashed
        )

        session.add(user)
        await session.commit()
        await session.refresh(user)

        return user