
# app/service/admin/plant_category_service.py -> admin

import re
from uuid import UUID
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.repositories.plant_species_repository import PlantSpeciesRepository
from app.repositories.plant_category_repository import PlantCategoryRepository

from app.models.plant_category import PlantCategory

from app.schemas.admin.plant_category_schema import (
    AdminPlantCategoryListParams,
    AdminPlantCategoryCreateRequest,
    AdminPlantCategoryUpdateRequest,

    AdminPlantCategoryResponse,
    AdminPlantCategoryListResponse,
)

from app.exceptions.plant_category_exception import (
    PlantCategoryNotFound,
    PlantCategoryAlreadyExists,
    InvalidPlantCategoryUpdate,

    PlantCategoryAlreadyInactive,
    PlantCategoryAlreadyActive,
)

class AdminPlantCategoryService:

    def __init__(
            self,
            plant_species_repository: PlantSpeciesRepository,
            plant_category_repository: PlantCategoryRepository,
    ):
        self.plant_species_repository = plant_species_repository
        self.plant_category_repository = plant_category_repository

    async def create_plant_category(
            self,
            request: AdminPlantCategoryCreateRequest
    ) -> PlantCategory:

        
        plant_category = await self.plant_category_repository.get_by_name(
            name=request.name
        )

        if plant_category:
            raise PlantCategoryAlreadyExists()
        
        plant_category = self._build_plant_category(
            request=request
        )

        plant_category = await self.plant_category_repository.create(
            plant_category=plant_category
        )

        try:
            await self.plant_category_repository.commit()
        except SQLAlchemyError:
            await self.plant_category_repository.rollback()
            raise

        await self.plant_category_repository.refresh(plant_category)

        return plant_category

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

    async def get_by_uid(
            self,
            plant_category_uid: UUID,
    ): 
        plant_caterory = await self.plant_category_repository.get_by_uid(
            plant_category_uid=plant_category_uid
        )

        if plant_caterory is None:
            raise PlantCategoryNotFound()

        return plant_caterory
    
    async def update_plant_category(
            self,
            *,
            plant_category_uid: UUID,
            request: AdminPlantCategoryUpdateRequest,
    ) -> PlantCategory:

        plant_category = await self.plant_category_repository.get_by_uid(
            plant_category_uid=plant_category_uid,
        )

        if plant_category is None:
            raise PlantCategoryNotFound()


        update_data: dict = request.model_dump(exclude_unset=True)

        if not update_data:
            raise InvalidPlantCategoryUpdate()


        if "name" in update_data:
            name = update_data["name"]

            if name is not None:
                slug = self._make_slug(name=name)

                existing_category = await self.plant_category_repository.get_by_conflicting_category(
                    name=name,
                    slug=slug,
                    exclude_uid=plant_category_uid,
                )

                if existing_category is not None:
                    raise PlantCategoryAlreadyExists()

                plant_category.name = name
                plant_category.slug = slug

        if "description" in update_data:
            plant_category.description = update_data["description"]

        if "image_url" in update_data:
            image_url = update_data["image_url"]

            plant_category.image_url = (
                str(image_url)
                if image_url is not None
                else None
            )

        try:
            plant_category  =  await self.plant_category_repository.update(
                plant_category=plant_category,
            )
            await self.plant_category_repository.commit()
        
        except IntegrityError as exc:
            await self.plant_category_repository.rollback()
            raise PlantCategoryAlreadyExists() from exc

        # await self.plant_category_repository.refresh(plant_category)

        return plant_category

    async def set_plant_species_active(
            self,
            *,
            plant_category_uid: UUID,
            is_active: bool
    ) -> PlantCategory:

        plant_category = await self.plant_category_repository.get_by_uid(
            plant_category_uid=plant_category_uid
        )

        if plant_category is None:
            raise PlantCategoryNotFound()

        if plant_category.is_active == is_active:
            if is_active:
                raise PlantCategoryAlreadyActive()
            raise PlantCategoryAlreadyInactive()

        plant_category.is_active = is_active

        try:
            await self.plant_category_repository.commit()
        except SQLAlchemyError:
            await self.plant_category_repository.rollback()

        await self.plant_category_repository.refresh(plant_category)

        return plant_category
        

    def _build_plant_category(
            self,
            *,
            request: AdminPlantCategoryCreateRequest
    ) -> PlantCategory:

        return PlantCategory(
            name=request.name,
            slug=self._make_slug(name=request.name),
            description=request.description,
            image_url=(
                str(request.image_url)
                if request.image_url is not None
                else None
            ),
        )

    def _make_slug(
            self,
            *,
            name: str
    ) -> str:

        slug = name.strip().lower()
        slug = re.sub(r"[^a-z0-9]+", "-", slug)
        return slug.strip("-")
