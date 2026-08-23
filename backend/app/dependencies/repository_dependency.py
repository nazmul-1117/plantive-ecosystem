
from typing import Annotated
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends

from app.repositories.user_repository import UserRepository
from app.repositories.role_repository import RoleRepository
from app.repositories.user_role_repository import UserRoleRepository
from app.repositories.verification_token_repository import VerificationTokenRepository
from app.repositories.password_reset_token_repository import PasswordResetTokenRepository

#plant repository
from app.repositories.plant_species_repository import PlantSpeciesRepository
from app.repositories.plant_care_guide_repository import PlantCareGuideRepository
from app.repositories.plant_category_repository import PlantCategoryRepository
from app.repositories.plant_species_category_repository import PlantSpeciesCategoryRepository

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

def get_verification_token_repository(
        session: SessionDeps
) -> VerificationTokenRepository:

    return VerificationTokenRepository(
        session = session
    )

def get_password_reset_token_repository(
        session: SessionDeps
) -> PasswordResetTokenRepository:

    return PasswordResetTokenRepository(
        session = session
    )

def get_plant_species_repository(
        session: SessionDeps
) -> PlantSpeciesRepository:

    return PlantSpeciesRepository(
        session=session
    )

def get_plant_care_guide_repository(
        session: SessionDeps
) -> PlantCareGuideRepository:

    return PlantCareGuideRepository(
        session=session
    )

def get_plant_category_repository(
        session: SessionDeps
) -> PlantCategoryRepository:

    return PlantCategoryRepository(
        session=session
    )

def get_plant_species_category_repository(
        session: SessionDeps
) -> PlantSpeciesCategoryRepository:

    return PlantSpeciesCategoryRepository(
        session=session
    )