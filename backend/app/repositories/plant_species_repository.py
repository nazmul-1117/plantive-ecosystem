
# app/repositories/plant_species_repository.py


from uuid import UUID

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, exists, delete, or_, func
from sqlalchemy.orm import selectinload, joinedload

from app.models.plant_species import PlantSpecies
from app.models.plant_species_category import PlantSpeciesCategory
from app.models.plant_category import PlantCategory
from app.models.plant_care_guide import PlantCareGuide

from app.constants.plant_constant import SunlightRequirement, PlantSpeciesSort


class PlantSpeciesRepository:

    def __init__(
            self,
            session: AsyncSession
    ):
        self.session = session

    async def create(
            self,
    ):
        pass

    async def delete(
            self,
    ):
        pass

    async def update(
            self,
    ):
        pass

    async def get_by_uid(
            self,
            *,
            plant_species_uid: UUID
    ) -> PlantSpecies | None:
        
        statement = (
            select(PlantSpecies)
            .options(
                selectinload(PlantSpecies.categories)
            )
            .where(
                PlantSpecies.plant_species_uid == plant_species_uid
            )
        )

        result = await self.session.exec(statement)

        return result.first()

    async def get_plants(
            self,
            *,
            search: str | None = None,
            category: str | None = None,
            sunlight_requirement: SunlightRequirement | None = None,
            sort: PlantSpeciesSort = PlantSpeciesSort.COMMON_NAME,
            min_temp: float | None = None,
            max_temp: float | None = None,
            is_active: bool | None = None,

            offset: int = 0,
            limit: int = 20,
    ) -> tuple[list[PlantSpecies], int]:

        """
                    PlantSpecies
                         │
                         ▼
                    Base Query
                         │
                         ▼
                      Filters
                         │
             ┌───────────┴───────────┐
             │                       │
             ▼                       ▼
           COUNT                  SELECT
             │                       │
             │                    SORT
             │                       │
             │                 Eager Loading
             │                       │
             │                  OFFSET/LIMIT
             │                       │
             ▼                       ▼
           total                    plants
        """

        # 1. Build Base quesry
        statement = select(PlantSpecies)

        # 2. Apply Filters
        statement = await self._apply_filters(
            statement=statement,
            search=search,
            category=category,
            sunlight_requirement=sunlight_requirement,
            min_temp=min_temp,
            max_temp=max_temp,
            is_active=is_active,
        )

        # 3. Count filters
        count_statement = (
            select(func.count())
            .select_from(statement.subquery())
        )

        count_result = await self.session.exec(count_statement)
        total = count_result.one()

        # 4. Apply sorting
        statement = await self._apply_sorting(
            statement=statement,
            sort=sort,
        )

        # 5. Apply eager Loading
        statement = statement.options(
            selectinload(PlantSpecies.categories)
        )

        # 6. Apply changes
        statement = (
            statement
            .offset(offset)
            .limit(limit)
        )

        # 7. Execute final query

        result = await self.session.exec(statement)

        plants = result.all()


        return plants, total
        
    async def _apply_filters(
            self,
            statement,
            *,
            search: str | None,
            category: str | None,
            sunlight_requirement: SunlightRequirement | None,
            min_temp: float | None,
            max_temp: float | None,
            is_active: bool | None,
    ):

        if search:
            search = search.strip()

            search_pattern = f"%{search}%"

            statement = statement.where(
                or_(
                    PlantSpecies.common_name.ilike(search_pattern),
                    PlantSpecies.scientific_name.ilike(search_pattern),
                )
            )

        if category:
            category = category.strip().lower()

            category_exists = exists(
                select(1)
                .select_from(PlantSpeciesCategory)
                .join(
                    PlantCategory,
                    PlantCategory.plant_category_uid
                    == PlantSpeciesCategory.plant_category_uid,
                )
                .where(
                    PlantSpeciesCategory.plant_species_uid
                    == PlantSpecies.plant_species_uid,
                    PlantCategory.slug == category,
                )
            )

            statement = statement.where(category_exists)

        if sunlight_requirement:
            statement = statement.where(
                PlantSpecies.sunlight_requirement
                == sunlight_requirement
            )

        if is_active is not None:
            statement = statement.where(
                PlantSpecies.is_active == is_active
            )

        if min_temp is not None:
            statement = statement.where(
                PlantSpecies.ideal_temp_max_c >= min_temp
            )

        if max_temp is not None:
            statement = statement.where(
                PlantSpecies.ideal_temp_min_c <= max_temp
            )

        return statement

    async def _apply_sorting(
            self,
            statement,
            *,
            sort: PlantSpeciesSort
    ):

        if sort == PlantSpeciesSort.COMMON_NAME:
            return statement.order_by(
                PlantSpecies.common_name.asc(),
                PlantSpecies.plant_species_uid.asc(),
            )

        if sort == PlantSpeciesSort.SCIENTIFIC_NAME:
            return statement.order_by(
                PlantSpecies.scientific_name.asc(),
                PlantSpecies.plant_species_uid.asc(),
            )

        if sort == PlantSpeciesSort.NEWEST:
            return statement.order_by(
                PlantSpecies.created_at.desc(),
                PlantSpecies.plant_species_uid.desc(),
            )

        return statement.order_by(
            PlantSpecies.common_name.asc(),
            PlantSpecies.plant_species_uid.asc(),
        )

    async def get_by_uid_with_care_guide(
            self,
            *,
            plant_species_uid: UUID
    ) -> PlantSpecies | None:
        
        statement = (
            select(PlantSpecies)
            .options(
                joinedload(PlantSpecies.care_guide)
            )
            .where(
                PlantSpecies.plant_species_uid == plant_species_uid
            )
        )

        result = await self.session.exec(statement)

        return result.one_or_none()

    async def commit(self) -> None:
        await self.session.commit()
    
    async def rollback(self) -> None:
        await self.session.rollback()
    
    async def refresh(self, obj) -> None:
        await self.session.refresh(obj)




