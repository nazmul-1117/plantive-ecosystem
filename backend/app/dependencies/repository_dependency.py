
from typing import Annotated
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends

from app.repositories.user_repository import UserRepository
from app.repositories.role_repository import RoleRepository
from app.repositories.user_role_repository import UserRoleRepository

from app.core.database import get_session

SessionDeps = Annotated[AsyncSession, Depends(get_session)]

def get_user_repository(
        session: SessionDeps
) -> UserRepository:
    
    return UserRepository(
        session=session
    )

def get_role_repository(
        session: SessionDeps
) -> RoleRepository:
    
    return RoleRepository(
        session=session
    )

def get_user_role_repository(
        session: SessionDeps
) -> UserRoleRepository:
    
    return UserRoleRepository(
        session=session
    ) 