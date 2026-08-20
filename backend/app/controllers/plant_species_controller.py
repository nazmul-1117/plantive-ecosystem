
# app/controllers/plant_species_controller.py

from uuid import UUID
from fastapi import Depends
from typing import Annotated

from app.models.auth_model import User
from app.models.plant_species import PlantSpecies
from app.schemas.plant_species_schema import PlantSpeciesListParams, PlantSpeciesReadListResponse
from app.services.plant_species_service import PlantSpeciesService

from app.constants.roles_constant import RoleConstant

from app.dependencies.permission_dependency import require_roles
from app.dependencies.query_validation_dependency import strict_query_params
from app.dependencies.service_dependency import (
    get_plant_species_service
)

async def list_plant_species(
        _: Annotated[None, Depends(strict_query_params(PlantSpeciesListParams))],
        params: Annotated[PlantSpeciesListParams, Depends()],
        plant_species_service: Annotated[PlantSpeciesService, Depends(get_plant_species_service)],
        
) -> PlantSpeciesReadListResponse:
     
    return await plant_species_service.list_plant_species(
        params=params
    )