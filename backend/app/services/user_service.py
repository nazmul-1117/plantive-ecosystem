from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select, or_

from app.core.database import get_session
from app.schemas.auth_schema import UserCreate, UserRead
from app.models.auth_model import User, Role, UserRole
from app.core.security import generate_hash_password

from app.repositories.user_repository import UserRepository
from app.repositories.role_repository import RoleRepository
from app.repositories.user_role_repository import UserRoleRepository

from app.exceptions.user_exception import (
    UserNotFound,
    EmailAlreadyExists,
    UsernameAlreadyExists
)
from app.exceptions.auth_exception import InvalidLoginCredential
from app.exceptions.role_exception import RoleNotFound

user_repository = UserRepository()
role_repository = RoleRepository()
user_role_repository = UserRoleRepository()


# UserService

# get_by_id()
# update_profile()
# delete_account()
# change_password()

class UserService:
    """
    Don't raise HTTPException in the service—use custom domain exceptions and let the controller translate them into HTTP responses.
    """
    
    async def register_user(
            self,
            user_data: UserCreate,
            session: AsyncSession
    ) -> User:
        
        user = await user_repository.get_by_email(
            email=user_data.email,
            session=session
        )
        
        if user is not None:
            raise EmailAlreadyExists()

        user = await user_repository.get_by_username(
            username=user_data.username,
            session=session
        )

        if user is not None:
            raise UsernameAlreadyExists()
        
        # user_data.password = generate_hash_password(user_data.password)
        user = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            avatar_url=user_data.avatar_url,
            bio=user_data.bio,
            username=user_data.username,
            password_hash=generate_hash_password(user_data.password)
        )

        user_table = await user_repository.create(
            user=user,
            session=session
        )

        role_table = await role_repository.get_by_name(
            role_name="user",
            session=session
        )

        if role_table is None:
            raise RoleNotFound()

        await user_role_repository.assign_role(
            user_uid=user_table.user_uid,
            role_uid=role_table.role_uid,
            session=session
        )

        try:
            await session.commit()
            await session.refresh(user_table)

        except SQLAlchemyError:
            await session.rollback()
            raise

        return user_table
    
    async def get_by_uid(
            self,
            user_uid: str,
            session: AsyncSession
    ) -> User | None:
        
        return await user_repository.get_by_uid(
            user_uid=user_uid,
            session=session
        )

    async def update_profile():
        pass

    async def delete_account():
        pass

    async def change_password():
        pass