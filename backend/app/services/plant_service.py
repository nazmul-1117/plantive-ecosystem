from fastapi import status, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, asc
from datetime import datetime
from app.schemas.plant_schema import PlantCreate, PlantUpdate
from app.models.plant_model import Plants

class PlantService:
    async def get_all_plants(self, session: AsyncSession):
        statement = select(Plants).order_by(asc(Plants.uid))
        results = await session.exec(statement=statement)
        
        return results.all()

    async def get_plant(self, plant_uid: str, session: AsyncSession):
        statement = select(Plants).where(Plants.uid == plant_uid)
        result = await session.exec(statement)
        plant = result.first()
        return plant if plant is not None else None

    async def create_plant(self, create_data: PlantCreate, session: AsyncSession):
        plant_data_dict = create_data.model_dump()
        new_data = Plants(**plant_data_dict)
        session.add(new_data)
        await session.commit()
        return new_data

    async def update_plant(self, plant_uid: str, update_data: PlantUpdate, session: AsyncSession):
        plant_to_update = await self.get_plant(plant_uid, session)
        if plant_to_update is None:
            return None
        
        plant_update_dict = update_data.model_dump()
        for k, v in plant_update_dict.items():
            setattr(plant_to_update, k, v)
        await session.commit()
        return plant_to_update

    async def delete_plant(self, plant_uid: str, session: AsyncSession):
        plant_to_delete = await self.get_plant(plant_uid, session)
        if plant_to_delete is None:
            return None
        await session.delete(plant_to_delete)
        await session.commit()
        return {
            "status": status.HTTP_200_OK,
            "message": f"Plant UID {plant_uid} deleted successfully"
        }

    async def search_plant(self, plant_uid: str, session: AsyncSession):
        pass