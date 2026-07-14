from fastapi import Depends
from typing import Annotated
from redis.asyncio import Redis
from sqlmodel.ext.asyncio.session import AsyncSession

from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.services.token_service import TokenService
from app.services.role_service import RoleService
from app.services.plant_service import PlantService

from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.repositories.user_role_repository import UserRoleRepository

from app.dependencies.repository_dependency import get_role_repository, get_user_repository, get_user_role_repository
from app.dependencies.redis_dependency import get_redis

from app.core.database import get_session


def get_user_service(
        role_repository: Annotated[RoleRepository , Depends(get_role_repository)],
        user_repository: Annotated[UserRepository , Depends(get_user_repository)],
        user_role_repository: Annotated[UserRoleRepository , Depends(get_user_role_repository)],
) -> UserService:
    
    return UserService(
        user_repository=user_repository,
        role_repository=role_repository,
        user_role_repository=user_role_repository,
    )

def get_token_service(
        redis: Annotated[Redis , Depends(get_redis)],
) -> TokenService:
    
    return TokenService(
        redis=redis
    )

def get_auth_service(
        token_service: Annotated[TokenService , Depends(get_token_service)],
        user_repository: Annotated[UserRepository , Depends(get_user_repository)],
) -> AuthService:
    
    return AuthService(
        token_service=token_service,
        user_repository=user_repository
    )

def get_role_service(
        role_repository: Annotated[RoleRepository , Depends(get_role_repository)],
) -> RoleService:
    
    return RoleService(
        role_repository=role_repository,
    )

def get_plant_service() -> PlantService:
    return PlantService()