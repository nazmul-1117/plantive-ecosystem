
# app/repositories/plant_care_guide_repository.py

from uuid import UUID
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.plant_care_guide import PlantCareGuide

class PlantCareGuideRepository:

    def __init__(
            self,
            session: AsyncSession
    ):
        self.session = session

    async def create(
            self,
    ):
        pass

    async def add(
            self,
            *,
            care_uide: PlantCareGuide,
    ) -> None:
        
        self.session.add(care_uide)

    async def delete(
            self,
    ):
        pass

    async def update(
            self,
    ):
        pass

    async def get_by_uid():
        pass

    async def get_by_plant_species_uid(
            self,
            *,
            plant_species_uid: UUID,
    ) -> PlantCareGuide | None:

        statement = (
            select(PlantCareGuide)
            .where(
                PlantCareGuide.plant_species_uid == plant_species_uid,
                PlantCareGuide.is_active.is_(True),
            )
        )

        result = await self.session.exec(statement)

        return result.first()
        

    async def commit(self) -> None:
        await self.session.commit()
    
    async def rollback(self) -> None:
        await self.session.rollback()
    
    async def refresh(self, obj) -> None:
        await self.session.refresh(obj)