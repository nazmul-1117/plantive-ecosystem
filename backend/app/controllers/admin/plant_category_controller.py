# app/controllers/admin/plant_category_controller.py - admin

from uuid import UUID
from fastapi import Depends
from typing import Annotated

from app.services.admin.plant_category_service import AdminPlantCategoryService

from app.schemas.admin.plant_category_schema import (
    AdminPlantCategoryListParams,

    AdminPlantCategoryCreateRequest,
    AdminPlantCategoryUpdateRequest,

    AdminPlantCategoryResponse,
    AdminPlantCategoryListResponse,
)

from app.dependencies.permission_dependency import require_roles
from app.dependencies.query_validation_dependency import strict_query_params
from app.dependencies.service_dependency import (
    get_admin_plant_category_service
)

async def list_plant_categories(
        _: Annotated[
            None,
            Depends(strict_query_params(AdminPlantCategoryListParams))
        ],

        params: Annotated[
            AdminPlantCategoryListParams,
            Depends()
        ],

        service: Annotated[
            AdminPlantCategoryService,
            Depends(get_admin_plant_category_service)
        ],
        
) -> AdminPlantCategoryListResponse:

    return await service.list_plant_categories(
        params=params
    )

async def get_plant_category(

        plant_category_uid: UUID,

        service: Annotated[
            AdminPlantCategoryService,
            Depends(get_admin_plant_category_service)
        ],
        
) -> AdminPlantCategoryResponse:

    return await service.get_by_uid(
        plant_category_uid=plant_category_uid
    )

async def create_plant_category(
        request: AdminPlantCategoryCreateRequest,

        service: Annotated[
            AdminPlantCategoryService,
            Depends(get_admin_plant_category_service)
        ],
) -> AdminPlantCategoryResponse:

    return await service.create_plant_category(
        request=request,
    )

async def update_plant_category(
        
        plant_category_uid: UUID,
        request: AdminPlantCategoryUpdateRequest,

        service: Annotated[
            AdminPlantCategoryService,
            Depends(get_admin_plant_category_service)
        ],
) -> AdminPlantCategoryResponse:

    return await service.update_plant_category(
        plant_category_uid=plant_category_uid,
        request=request,
    )