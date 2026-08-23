
# app/service/plant_species_service.py

from uuid import UUID
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.repositories.plant_species_repository import PlantSpeciesRepository
from app.repositories.plant_category_repository import PlantCategoryRepository
from app.repositories.plant_species_category_repository import PlantSpeciesCategoryRepository
from app.repositories.plant_care_guide_repository import PlantCareGuideRepository

from app.schemas.admin.plant_species_schema import (
    AdminPlantSpeciesListParams,
    AdminPlantSpeciesResponse,
    AdminPlantSpeciesListResponse,

    AdminPlantSpeciesCreateRequest,
    PlantCareGuideCreateRequest,
    AdminPlantSpeciesUpdateRequest,
    PlantCareGuideUpdateRequest,
)

from app.models.plant_species import PlantSpecies
from app.models.plant_category  import PlantCategory
from app.models.plant_species_category  import PlantSpeciesCategory
from app.models.plant_care_guide  import PlantCareGuide

from app.exceptions.plant_species_exception import (
    PlantSpeciesNotFound,
    PlantSpeciesAlreadyExists,
    InvalidPlantSpeciesUpdate,
)
from app.exceptions.plant_care_guide import (
    PlantCareGuideNotFound,
    PlantCareGuideRequired,
)
from app.exceptions.plant_category_exception import PlantCategoryNotFound

from app.constants.plant_constant import SunlightRequirement

class AdminPlantSpeciesService:

    """
    1. list_plant_species()
    2. get_plant_species()
    3. create_plant_species()
    4. update_plant_species()
    5. delete_plant_species()
    6. activate_plant_species()
    7. deactivate_plant_species()
    """

    def __init__(
            self,
            plant_species_repository: PlantSpeciesRepository,
            plant_category_repository: PlantCategoryRepository,
            plant_species_category_repository: PlantSpeciesCategoryRepository,
            plant_care_guide_repository: PlantCareGuideRepository,
    ):
        self.plant_species_repository = plant_species_repository
        self.plant_category_repository = plant_category_repository
        self.plant_species_category_repository = plant_species_category_repository
        self.plant_care_guide_repository = plant_care_guide_repository

    async def list_plant_species(
            self,
            params: AdminPlantSpeciesListParams
    ) -> AdminPlantSpeciesListResponse:

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
            is_active=params.is_active,
            
            offset=offset,
            limit=params.page_size,
        )

        total_pages = (
            (total + params.page_size - 1)
            // params.page_size
            if total > 0
            else 0
        )

        return AdminPlantSpeciesListResponse(
            items=plant_species,
            page=params.page,
            page_size=params.page_size,
            total=total,
            total_pages=total_pages,
        )

    async def get_by_uid(
            self,
            plant_species_uid: UUID
    ) -> AdminPlantSpeciesResponse:

        plant_species = await self.plant_species_repository.get_by_uid(
            plant_species_uid=plant_species_uid
        )

        if plant_species is None:
            raise PlantSpeciesNotFound()

        return plant_species

    async def create_plant_species(
            self,
            request: AdminPlantSpeciesCreateRequest,
    ) -> PlantSpecies:
        
        existing_plant: PlantSpecies | None = await self.plant_species_repository.get_by_scientific_name(
            scientific_name=request.scientific_name,
        )

        if existing_plant is not None:
            raise PlantSpeciesAlreadyExists()

        categories = await self.plant_category_repository.get_by_uids(
            plant_category_uuids=request.plant_category_uids
        )

        if len(categories) != len(request.plant_category_uids):
            raise PlantCategoryNotFound()
        
        plant_species = self._build_plant_species(
            request=request
        )

        plant_species.categories = categories

        if request.care_guide is not None:
            plant_species.care_guide = self._build_plant_care_guide(
                care_guide=request.care_guide
            )

        plant_species = await self.plant_species_repository.create(
            plant_species=plant_species
        )

        try:
            await self.plant_species_repository.commit()
        except SQLAlchemyError:
            await self.plant_species_repository.rollback()
            raise

        await self.plant_species_repository.refresh(plant_species)

        created_plant = await self.plant_species_repository.get_by_uid(
            plant_species_uid=plant_species.plant_species_uid
        )

        return created_plant

    async def update_plant_species(
            self,
            *,
            plant_species_uid: UUID,
            request: AdminPlantSpeciesUpdateRequest,
    ) -> PlantSpecies:
        
        plant_species = await self.plant_species_repository.get_by_uid(
            plant_species_uid=plant_species_uid,
        )

        if plant_species is None:
            raise PlantSpeciesNotFound()

        update_data: dict = request.model_dump(exclude_unset=True)

        category_uids = update_data.pop(
            "plant_category_uids",
            None,
        )

        care_guide_updates = update_data.pop(
            "care_guide",
            None,
        )

        image_url = update_data.pop(
            "image_url",
            None,
        )

        if (
            not update_data
            and category_uids is None
            and care_guide_updates is None
            and image_url is None
        ):
            raise InvalidPlantSpeciesUpdate()

        if "scientific_name" in update_data:
            await self._validate_scientific_name(
                plant_species=plant_species,
                scientific_name=update_data["scientific_name"],
            )

        for field, value in update_data.items():
            setattr(
                plant_species,
                field,
                value,
            )

        if category_uids is not None:
            await self._replace_categories(
                plant_species_uid=plant_species_uid,
                category_uids=category_uids,
            )

        if care_guide_updates is not None:
            await self._update_care_guide(
                plant_species_uid=plant_species_uid,
                update_data=care_guide_updates,
            )

        if image_url is not None:
            plant_species.image_url = str(image_url)

        try:
            await self.plant_species_repository.commit()
        except IntegrityError:
            await self.plant_species_repository.rollback()
            raise PlantSpeciesAlreadyExists()

        await self.plant_species_repository.refresh(plant_species)

        # updated_plant_species = await self.plant_species_repository.get_by_uid(
        #     plant_species_uid=plant_species.plant_species_uid
        # )

        return plant_species



    def _build_plant_species(
            self,
            *,
            request: AdminPlantSpeciesCreateRequest
    ) -> PlantSpecies:

        return PlantSpecies(
            common_name=request.common_name,
            scientific_name=request.scientific_name,
            description=request.description,

            ideal_temp_min_c=request.ideal_temp_min_c,
            ideal_temp_max_c=request.ideal_temp_max_c,

            ideal_humidity_min_percent=request.ideal_humidity_min_percent,
            ideal_humidity_max_percent=request.ideal_humidity_max_percent,

            ideal_soil_moisture_min_percent=request.ideal_soil_moisture_min_percent,
            ideal_soil_moisture_max_percent=request.ideal_soil_moisture_max_percent,

            sunlight_requirement=request.sunlight_requirement,
            watering_frequency_days=request.watering_frequency_days,

            image_url=(
                str(request.image_url)
                if request.image_url is not None
                else None
            ),
        )
        
    def _build_plant_care_guide(
            self,
            *,
            care_guide: PlantCareGuideCreateRequest
    ) -> PlantCareGuide:

        return PlantCareGuide(
            watering_guide=care_guide.watering_guide,
            fertilizer_guide=care_guide.fertilizer_guide,
            pruning_guide=care_guide.pruning_guide,
            common_problems=care_guide.common_problems,
        )

    async def _replace_categories(
            self,
            *,
            plant_species_uid:UUID,
            category_uids: list[UUID],
    ) -> None:

        categories: list[PlantCategory] | None  = await self.plant_category_repository.get_by_uids(
            plant_category_uuids=category_uids
        )

        found_category_uids = {
            category.plant_category_uid
            for category in categories
        }

        missing_category_uids = set(category_uids) - found_category_uids

        if missing_category_uids:
            raise PlantCategoryNotFound()

        await self.plant_species_category_repository.replace_categories(
            plant_species_uid=plant_species_uid,
            category_uids=category_uids,
        )

    async def _update_care_guide(
            self,
            *,
            plant_species_uid:UUID,
            update_data: dict,
    ) -> None:

        # update_data: dict = care_guide_data.model_dump(exclude=True)

        care_guide = (
            await self.plant_care_guide_repository
            .get_by_plant_species_uid(
                plant_species_uid=plant_species_uid,
            )
        )

        if care_guide is None:

            watering_guide = update_data.get("watering_guide")

            if watering_guide is None:
                raise PlantCareGuideRequired()
            
            care_guide = PlantCareGuide(
                plant_species_uid=plant_species_uid,
                **update_data,
            )

            # for field, value in update_data.items():
            #     if field != "watering_guide":
            #         setattr(
            #             care_guide,
            #             field,
            #             value,
            #         )
            self.plant_care_guide_repository.add(
                care_uide=care_guide
            )

            return

        for field, value in update_data.items():
            setattr(
                care_guide,
                field,
                value,
            )

    async def _validate_scientific_name(
            self,
            *,
            plant_species: PlantSpecies,
            scientific_name: str,
    ) -> None:

        if scientific_name == plant_species.scientific_name:
            return

        existing = (
            await self.plant_species_repository.get_by_scientific_name(
                    scientific_name=scientific_name
                )
        )

        if existing is not None:
            raise PlantSpeciesAlreadyExists()

        

        
    # async def get_by_common_name():
    #     pass

    # async def get_by_scientific_name():
    #     pass

    # async def get_care_guide(
    #         self,
    #         *,
    #         plant_species_uid: UUID
    # ) -> PlantCareGuideResponse:
        
    #     plant_species = await self.plant_species_repository.get_by_uid_with_care_guide(
    #         plant_species_uid=plant_species_uid
    #     )

    #     if (
    #         plant_species is None
    #         or plant_species.care_guide is None
    #     ):
    #         raise PlantCareGuideNotFound()

    #     return PlantCareGuideResponse(
    #         plant_species=PlantSpeciesSummary.model_validate(plant_species),
    #         care_guide=PlantCareGuideData.model_validate(plant_species.care_guide),
    #     )

