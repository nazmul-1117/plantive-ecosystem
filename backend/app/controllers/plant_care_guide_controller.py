
# app/controllers/plant_care_guide_controller.py

from uuid import UUID
from fastapi import Depends
from typing import Annotated

from app.models.auth_model import User
from app.models.plant_species import PlantSpecies
from app.services.plant_care_guide_service import PlantCareGuideService
from app.schemas.plant_care_guide_schema import PlantCareGuideResponse

from app.constants.roles_constant import RoleConstant

from app.dependencies.permission_dependency import require_roles
from app.dependencies.query_validation_dependency import strict_query_params
from app.dependencies.service_dependency import (
    get_plant_care_guide_service
)


async def get_care_guide(
        plant_care_guide_service: Annotated[PlantCareGuideService, Depends(get_plant_care_guide_service)],
        
        plant_species_uid: UUID,
) -> PlantCareGuideResponse:

    return await plant_care_guide_service.get_care_guide_by_plant_species_uid(
        plant_species_uid=plant_species_uid
    )