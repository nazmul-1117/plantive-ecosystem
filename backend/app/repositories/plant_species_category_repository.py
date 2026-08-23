
# app/repositories/plant_species_category_repository.py


from uuid import UUID

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, exists, delete, or_, func
from sqlalchemy.orm import selectinload, joinedload

from app.models.plant_species_category import PlantSpeciesCategory


class PlantSpeciesCategoryRepository:

    def __init__(
            self,
            session: AsyncSession
    ):
        self.session = session 


    async def replace_categories(
            self,
            *,
            plant_species_uid: UUID,
            category_uids: list[UUID],
    ) -> None:

        statement = (
            delete(PlantSpeciesCategory)
            .where(
                PlantSpeciesCategory.plant_species_uid == plant_species_uid
            )
        )

        await self.session.exec(statement)

        if not category_uids:
            return 

        associations = [
            PlantSpeciesCategory(
                plant_species_uid=plant_species_uid,
                plant_category_uid=plant_category_uid,
            )
            for plant_category_uid in category_uids
        ]

        self.session.add_all(associations)