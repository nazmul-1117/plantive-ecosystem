# plant_router.py

from fastapi import APIRouter, status
from typing import List
from app.controllers.plant_controllers import add_plant, delete_plant, search_plant, get_all_plants, update_plant, get_plant
from app.schemas.plant_schema import PlantCreate, Plant
# from app.models.plant_model import Plants

router = APIRouter()

router.get(
    "/",
    status_code = status.HTTP_200_OK,
    response_model = List[Plant]
    )(get_all_plants)

router.get(
    "/{plant_uid}",
    status_code = status.HTTP_200_OK,
    response_model=Plant
    )(get_plant)

# create plant
router.post(
    "/",
    status_code = status. HTTP_201_CREATED
    )(add_plant)

router.delete(
    "/{plant_uid}",
    status_code = status.HTTP_204_NO_CONTENT
    )(delete_plant)

router.patch(
    "/{plant_uid}",
    status_code = status.HTTP_200_OK
    )(update_plant)

router.get(
    "/{plant_uid}",
    status_code = status.HTTP_200_OK
    )(search_plant)
