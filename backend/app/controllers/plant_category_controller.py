
# ========================================================================================
#                  app/controllers/plant_category_controller.py -> Public
# ========================================================================================


from uuid import UUID
from fastapi import Depends
from typing import Annotated

from app.services.plant_category_service import PlantCategoryService

from app.schemas.plant_category_schema import (
    PlantCategoryResponse,
    PlantCategoryListResponse,

    PlantCategoryListParams,
    PlantSpeciesListResponse,
    PlantSpeciesListParams
)

from app.dependencies.permission_dependency import require_roles
from app.dependencies.query_validation_dependency import strict_query_params
from app.dependencies.service_dependency import (
    get_plant_category_service
)

async def list_plant_categories(
        _: Annotated[
            None,
            Depends(strict_query_params(PlantCategoryListParams))
        ],

        params: Annotated[
            PlantCategoryListParams,
            Depends()
        ],

        service: Annotated[
            PlantCategoryService,
            Depends(get_plant_category_service)
        ],
        
) -> PlantCategoryListResponse:

    return await service.list_plant_categories(
        params=params
    )

async def get_plant_category(

        plant_category_uid: UUID,

        service: Annotated[
            PlantCategoryService,
            Depends(get_plant_category_service)
        ],
        
) -> PlantCategoryResponse:

    return await service.get_by_uid(
        plant_category_uid=plant_category_uid
    )

async def get_plant_species(
        _query_params: Annotated[
            None,
            Depends(strict_query_params(PlantSpeciesListParams))
        ],

        params: Annotated[
            PlantSpeciesListParams,
            Depends()
        ],

        plant_category_uid: UUID,

        service: Annotated[
            PlantCategoryService,
            Depends(get_plant_category_service)
        ],
        
) -> PlantSpeciesListResponse:

    return await service.get_plant_species(
        plant_category_uid=plant_category_uid,
        params=params
    )