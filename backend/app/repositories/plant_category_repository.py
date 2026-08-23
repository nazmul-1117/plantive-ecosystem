
# app/repositories/plant_category_repository.py


from uuid import UUID

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, exists, delete, or_, func
from sqlalchemy.orm import selectinload, joinedload

from app.models.plant_species import PlantSpecies
from app.models.plant_species_category import PlantSpeciesCategory
from app.models.plant_category import PlantCategory
from app.models.plant_care_guide import PlantCareGuide

from app.constants.plant_constant import SunlightRequirement, PlantSpeciesSort


class PlantCategoryRepository:

    def __init__(
            self,
            session: AsyncSession
    ):
        self.session = session

    async def get_by_uids(
            self,
            *,
            plant_category_uuids: list[UUID]
    ):
        if not plant_category_uuids:
            return []
        
        statement = (
            select(PlantCategory)
            .where(
                PlantCategory.plant_category_uid.in_(plant_category_uuids)
            )
        )

        result = await self.session.exec(statement)

        return result.all()