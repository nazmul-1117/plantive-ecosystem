from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends, HTTPException, status
from app.core.database import get_session
from sqlmodel import select, or_

from app.schemas.auth_schema import UserCreate, UserRead
from app.models.auth_model import User, Role, UserRole
from app.core.security import generate_hash_password
from app.repositories.user_repository import UserRepository
from app.repositories.role_repository import RoleRepository
from app.repositories.user_role_repository import UserRoleRepository

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