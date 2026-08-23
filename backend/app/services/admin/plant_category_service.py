
# app/service/admin/plant_category_service.py -> admin

from uuid import UUID
from sqlalchemy.exc import SQLAlchemyError

from app.repositories.plant_species_repository import PlantSpeciesRepository
from app.repositories.plant_category_repository import PlantCategoryRepository

from app.models.plant_category import PlantCategory

from app.schemas.admin.plant_category_schema import (
    AdminPlantCategoryListParams,

    AdminPlantCategoryListResponse
)

class AdminPlantCategoryService:

    def __init__(
            self,
            plant_species_repository: PlantSpeciesRepository,
            plant_category_repository: PlantCategoryRepository,
    ):
        self.plant_species_repository = plant_species_repository
        self.plant_category_repository = plant_category_repository


    async def list_plant_categories(
            self,
            params: AdminPlantCategoryListParams
    ) -> AdminPlantCategoryListResponse:

        offset = (
            params.page - 1
        )*params.page_size

        plant_category, total = await self.plant_category_repository.list_categories(
            search=params.search,
            is_active=params.is_active,

            offset=offset,
            limit=params.page_size,
        )

        total_page = (
            (total + params.page_size - 1)
            // params.page_size
            if total > 0
            else 0
        )

        return AdminPlantCategoryListResponse(
            page=params.page,
            page_size=params.page_size,
            total=total,
            total_pages=total_page,

            items=plant_category,
        )
