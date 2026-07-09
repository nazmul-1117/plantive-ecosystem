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

# RoleService

# assign_role()
# remove_role()
# get_roles()
# has_role()

class RoleService:
    async def assign_role():
        pass

    async def remove_role():
        pass

    async def get_role():
        pass

    async def has_role():
        pass