from fastapi import Depends
from typing import Annotated
from redis.asyncio import Redis

from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.services.token_service import TokenService
from app.services.role_service import RoleService
from app.services.plant_service import PlantService
from app.services.email_service import EmailService

#plant service
from app.services.plant_species_service import PlantSpeciesService
from app.services.plant_care_guide_service import PlantCareGuideService

from app.services.admin.user_service import AdminUserService
from app.services.admin.user_role_service import AdminUserRoleService
from app.services.admin.plant_species_service import AdminPlantSpeciesService

from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.repositories.user_role_repository import UserRoleRepository
from app.repositories.verification_token_repository import VerificationTokenRepository
from app.repositories.password_reset_token_repository import PasswordResetTokenRepository

#plant repository
from app.repositories.plant_species_repository import PlantSpeciesRepository
from app.repositories.plant_care_guide_repository import PlantCareGuideRepository

from app.dependencies.repository_dependency import (
    get_role_repository, get_user_repository, get_user_role_repository,
    get_verification_token_repository, get_password_reset_token_repository,
    get_plant_species_repository, get_plant_care_guide_repository
)
from app.dependencies.redis_dependency import get_redis


def get_email_service() -> EmailService:
    return EmailService()

def get_user_service(
        role_repository: Annotated[RoleRepository , Depends(get_role_repository)],
        user_repository: Annotated[UserRepository , Depends(get_user_repository)],
        user_role_repository: Annotated[UserRoleRepository , Depends(get_user_role_repository)],
        verification_token_repository: Annotated[VerificationTokenRepository, Depends(get_verification_token_repository)]
) -> UserService:
    
    return UserService(
        user_repository = user_repository,
        role_repository = role_repository,
        user_role_repository = user_role_repository,
        verification_token_repository = verification_token_repository,
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
        password_reset_token_repository: Annotated[PasswordResetTokenRepository, Depends(get_password_reset_token_repository)],
) -> AuthService:
    
    return AuthService(
        token_service=token_service,
        user_repository=user_repository,
        password_reset_token_repository = password_reset_token_repository,
    )

def get_role_service(
        role_repository: Annotated[RoleRepository , Depends(get_role_repository)],
) -> RoleService:
    
    
    return RoleService(
        role_repository=role_repository,
    )

def get_plant_service() -> PlantService:
    return PlantService()



# user - admin
def get_admin_user_service(
        user_repository: Annotated[UserRepository , Depends(get_user_repository)],
) -> AdminUserService:

    return AdminUserService(
        user_repository = user_repository
    )

def get_admin_user_role_service(
        user_repository: Annotated[UserRepository , Depends(get_user_repository)],
        role_repository: Annotated[RoleRepository , Depends(get_role_repository)],
        user_role_repository: Annotated[UserRoleRepository , Depends(get_user_role_repository)],
) -> AdminUserRoleService:

    return AdminUserRoleService(
        user_repository=user_repository,
        role_repository=role_repository,
        user_role_repository=user_role_repository,
    )


# plant species - public
def get_plant_species_service(
    plant_species_repository: Annotated[PlantSpeciesRepository, Depends(get_plant_species_repository)],
) -> PlantSpeciesService:

    return PlantSpeciesService(
        plant_species_repository=plant_species_repository
    )

def get_plant_care_guide_service(
        plant_care_guide_repository: Annotated[PlantCareGuideRepository, Depends(get_plant_care_guide_repository)],
) -> PlantCareGuideService:

    return PlantCareGuideService(
        plant_care_guide_repository=plant_care_guide_repository
    )


# plant species admin
def get_admin_plant_species_service(
    plant_species_repository: Annotated[PlantSpeciesRepository, Depends(get_plant_species_repository)],
) -> AdminPlantSpeciesService:

    return AdminPlantSpeciesService(
        plant_species_repository=plant_species_repository
    )
