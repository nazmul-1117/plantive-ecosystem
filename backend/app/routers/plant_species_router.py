# plant_router.py

from fastapi import APIRouter, status
from typing import List
from app.schemas.plant_species_schema import (
    PlantSpeciesReadListResponse,
)
from app.controllers.plant_species_controller import (
    list_plant_species
)

router = APIRouter(
    prefix="/plant-species",
    tags=["Plant Species"],
)

router.get(
    path="/",
    status_code = status.HTTP_200_OK,
    response_model = PlantSpeciesReadListResponse,
    summary="List plant species"
)(list_plant_species)
