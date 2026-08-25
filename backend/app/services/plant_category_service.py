

# ========================================================================================
#                  app/service/admin/plant_category_service.py -> ADMIN
# ========================================================================================

from uuid import UUID

from app.repositories.plant_species_repository import PlantSpeciesRepository
from app.repositories.plant_category_repository import PlantCategoryRepository

from app.models.plant_category import PlantCategory

from app.schemas.plant_category_schema import (
    PlantCategoryResponse,
    PlantCategoryListResponse,

    PlantCategoryListParams,
    PlantSpeciesListParams,
    PlantSpeciesListResponse,
)

from app.exceptions.plant_category_exception import (
    PlantCategoryNotFound,
    PlantCategoryAlreadyExists,

    PlantCategoryAlreadyInactive,
    PlantCategoryAlreadyActive,
)
from app.exceptions.plant_species_exception import PlantSpeciesNotFound

class PlantCategoryService:

    def __init__(
            self,
            plant_species_repository: PlantSpeciesRepository,
            plant_category_repository: PlantCategoryRepository,
    ):
        self.plant_species_repository = plant_species_repository
        self.plant_category_repository = plant_category_repository


    async def list_plant_categories(
            self,
            params: PlantCategoryListParams
    ) -> PlantCategoryListResponse:

        offset = (
            params.page - 1
        )*params.page_size

        plant_category, total = await self.plant_category_repository.list_categories(
            search=params.search,
            is_active=True,

            offset=offset,
            limit=params.page_size,
        )

        total_page = (
            (total + params.page_size - 1)
            // params.page_size
            if total > 0
            else 0
        )

        return PlantCategoryListResponse(
            page=params.page,
            page_size=params.page_size,
            total=total,
            total_pages=total_page,

            items=plant_category,
        )

    async def get_by_uid(
            self,
            plant_category_uid: UUID,
    ): 
        plant_caterory = await self.plant_category_repository.get_by_uid(
            plant_category_uid=plant_category_uid
        )

        if plant_caterory is None:
            raise PlantCategoryNotFound()

        if plant_caterory.is_active == False:
            raise PlantCategoryNotFound()

        return plant_caterory

    async def get_plant_species(
            self,
            *,
            plant_category_uid: UUID,
            params: PlantSpeciesListParams,
    ) -> PlantSpeciesListResponse:

        offset = (
            params.page - 1
        )*params.page_size

        plant_category = await self.plant_category_repository.get_by_uid(
            plant_category_uid=plant_category_uid
        )

        if plant_category is None:
            raise PlantCategoryNotFound()

        plant_species, total = await self.plant_species_repository.get_by_category_uid(
            plant_category_uid=plant_category_uid,
            search=params.search,
            sort=params.sort,
            is_active=True,

            offset=offset,
            limit=params.page_size,
        )

        total_page = (
            (total + params.page_size - 1)
            // params.page_size
            if total > 0
            else 0
        )


        return PlantSpeciesListResponse(
            page=params.page,
            page_size=params.page_size,
            total=total,
            total_pages=total_page,

            plant_category_uid=plant_category.plant_category_uid,
            name=plant_category.name,
            image_url=plant_category.image_url,

            items=plant_species,
        )
