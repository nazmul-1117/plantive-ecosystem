
# app/service/plant_species_service.py

from uuid import UUID
from sqlalchemy.exc import SQLAlchemyError

from app.repositories.plant_species_repository import PlantSpeciesRepository

from app.schemas.plant_species_schema import (
    PlantSpeciesListParams,
    PlantSpeciesReadListResponse,
    PlantSpeciesReadResponse,

    PlantCareGuideResponse,
    PlantSpeciesSummary,
    PlantCareGuideData,
)
from app.models.plant_species import PlantSpecies

from app.exceptions.plant_exception import PlantSpeciesNotFound
from app.exceptions.plant_care_guide import PlantCareGuideNotFound

class PlantSpeciesService:

    def __init__(
            self,
            plant_species_repository: PlantSpeciesRepository
    ):
        self.plant_species_repository = plant_species_repository

    async def list_plant_species(
            self,
            params: PlantSpeciesListParams
    ) -> PlantSpeciesReadListResponse:

        offset = (
            params.page - 1
        ) * params.page_size

        plant_species, total =  await self.plant_species_repository.list(
            search=params.search,
            category=params.category,
            sunlight_requirement=params.sunlight_requirement,
            min_temp=params.min_temp,
            max_temp=params.max_temp,
            sort=params.sort,
            is_active=True,
            
            offset=offset,
            limit=params.page_size,
        )

        total_pages = (
            (total + params.page_size - 1)
            // params.page_size
            if total > 0
            else 0
        )

        return PlantSpeciesReadListResponse(
            items=plant_species,
            page=params.page,
            page_size=params.page_size,
            total=total,
            total_pages=total_pages,
        )

    async def get_by_uid(
            self,
            plant_species_uid: UUID
    ) -> PlantSpeciesReadResponse:

        plant_species = await self.plant_species_repository.get_by_uid(
            plant_species_uid=plant_species_uid
        )

        if plant_species is None:
            raise PlantSpeciesNotFound()

        return plant_species

    async def get_by_common_name():
        pass

    async def get_by_scientific_name():
        pass

    async def get_care_guide(
            self,
            *,
            plant_species_uid: UUID
    ) -> PlantCareGuideResponse:
        
        plant_species = await self.plant_species_repository.get_by_uid_with_care_guide(
            plant_species_uid=plant_species_uid
        )

        if (
            plant_species is None
            or plant_species.care_guide is None
        ):
            raise PlantCareGuideNotFound()

        return PlantCareGuideResponse(
            plant_species=PlantSpeciesSummary.model_validate(plant_species),
            care_guide=PlantCareGuideData.model_validate(plant_species.care_guide),
        )

