
# app/controllers/admin/plant_species_controller.py - admin

from uuid import UUID
from fastapi import Depends
from typing import Annotated

from app.models.auth_model import User
from app.models.plant_species import PlantSpecies

from app.services.admin.plant_species_service import AdminPlantSpeciesService
from app.services.plant_care_guide_service import PlantCareGuideService

from app.schemas.plant_care_guide_schema import PlantCareGuideResponse

from app.schemas.admin.plant_species_schema import (
    AdminPlantSpeciesListParams,
    AdminPlantSpeciesListResponse,
    AdminPlantSpeciesResponse,
    AdminPlantSpeciesListItem,

    AdminPlantSpeciesCreateRequest,
    AdminPlantSpeciesUpdateRequest,
)

from app.constants.roles_constant import RoleConstant

from app.dependencies.permission_dependency import require_roles
from app.dependencies.query_validation_dependency import strict_query_params
from app.dependencies.service_dependency import (
    get_admin_plant_species_service
)

async def list_plant_species(
        _: Annotated[
            None,
            Depends(strict_query_params(AdminPlantSpeciesListParams))
        ],

        params: Annotated[
            AdminPlantSpeciesListParams,
            Depends()
        ],

        admin_plant_species_service: Annotated[
            AdminPlantSpeciesService,
            Depends(get_admin_plant_species_service)
        ],
        
) -> AdminPlantSpeciesListResponse:

    return await admin_plant_species_service.list_plant_species(
        params=params
    )

async def get_plant_species(
        admin_plant_species_service: Annotated[
            AdminPlantSpeciesService,
            Depends(get_admin_plant_species_service)
        ],

        plant_species_uid: UUID
) -> AdminPlantSpeciesResponse:

    return await admin_plant_species_service.get_by_uid(
        plant_species_uid = plant_species_uid
    )

async def create_plant_species(

        request: AdminPlantSpeciesCreateRequest,

        admin_plant_species_service: Annotated[
            AdminPlantSpeciesService,
            Depends(get_admin_plant_species_service)
        ],

        # _: Annotated[
        #     User,
        #     Depends(require_roles(RoleConstant.ADMIN, RoleConstant.MODERATOR))
        # ],
) -> AdminPlantSpeciesResponse:

    return await admin_plant_species_service.create_plant_species(
        request=request
    )

async def update_plant_species(

        plant_species_uid: UUID,
        request: AdminPlantSpeciesUpdateRequest,

        service: Annotated[
            AdminPlantSpeciesService,
            Depends(get_admin_plant_species_service)
        ],

        # _: Annotated[
        #     User,
        #     Depends(require_roles(RoleConstant.ADMIN, RoleConstant.MODERATOR))
        # ],
) -> AdminPlantSpeciesResponse:

    return await service.update_plant_species(
        plant_species_uid=plant_species_uid,
        request=request
    )

async def activate_plant_species(
        
        plant_species_uid: UUID,

        service: Annotated[
            AdminPlantSpeciesService,
            Depends(get_admin_plant_species_service)
        ],

        # _: Annotated[
        #     User,
        #     Depends(require_roles(RoleConstant.ADMIN, RoleConstant.MODERATOR))
        # ],
) -> AdminPlantSpeciesListItem:

    return await service.set_plant_species_active(
        plant_species_uid=plant_species_uid,
        is_active=True,
    )


async def deactivate_plant_species(
        
        plant_species_uid: UUID,

        service: Annotated[
            AdminPlantSpeciesService,
            Depends(get_admin_plant_species_service)
        ],

        # _: Annotated[
        #     User,
        #     Depends(require_roles(RoleConstant.ADMIN, RoleConstant.MODERATOR))
        # ],
) -> AdminPlantSpeciesListItem:

    return await service.set_plant_species_active(
        plant_species_uid=plant_species_uid,
        is_active=False,
    )