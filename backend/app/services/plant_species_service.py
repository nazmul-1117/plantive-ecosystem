
# app/service/plant_species_service.py

from uuid import UUID
from sqlalchemy.exc import SQLAlchemyError

from app.repositories.plant_species_repository import PlantSpeciesRepository

from app.schemas.plant_species_schema import (
    PlantSpeciesListParams,
    PlantSpeciesReadListResponse
)
from app.models.plant_species import PlantSpecies

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

        plant_species, total =  await self.plant_species_repository.get_plants(
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