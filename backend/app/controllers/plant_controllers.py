# app/controllers/plant_controllers.py

import json
from fastapi import HTTPException, status, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas.plant import Plant, PlantUpdate, PlantCreate
from app.config.database import get_session
from app.services.plants import PlantService

plant_services = PlantService()


async def get_all_plants(session: AsyncSession = Depends(get_session)):
    result = await plant_services.get_all_plants(session)
    return result

async def get_plant(
        plant_uid: str,
        session: AsyncSession = Depends(get_session)
    ):

    plant: Plant = await plant_services.get_plant(
        plant_uid=plant_uid,
        session=session
        )
    
    if plant is not None:
        return plant
        
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="This Plant is not available right now"
    )

async def add_plant(
        plant_data: PlantCreate,
        session: AsyncSession = Depends(get_session)
        ):
    
    result = await plant_services.create_plant(plant_data, session)
    
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Plant not created"
        )
    
    return {
        "status": status.HTTP_201_CREATED,
        "message": "add plant successfully",
        "data": result
    }

async def delete_plant(
        plant_uid: str,
        session: AsyncSession = Depends(get_session)
        ):
    
    result = await plant_services.delete_plant(
        plant_uid=plant_uid,
        session=session
    )
    
    if result is not None:
        return result
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"This plant with {plant_id}, not found"
    )

async def update_plant(
        plant_uid: str,
        update_data: PlantUpdate,
        session: AsyncSession = Depends(get_session)
        ):
    
    result = await plant_services.update_plant(
        plant_uid=plant_uid,
        update_data=update_data,
        session=session
    )

    if result is not None:
         return {
            "status": status.HTTP_200_OK,
            "message": "plant successfully modified",
            "data": result
        }
    
    raise HTTPException(
        status_code=status.HTTP_304_NOT_MODIFIED,
        detail="data not modified"
    )

async def search_plant(
        plant_uid: str,
        session: AsyncSession = Depends(get_session)
):
    pass