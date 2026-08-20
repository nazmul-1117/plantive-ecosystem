# plant_router.py

from fastapi import APIRouter, status
from typing import List
from app.schemas.plant_species_schema import (
    PlantSpeciesReadListResponse,
    PlantSpeciesReadResponse,
    PlantCareGuideResponse,
)
# from app.schemas.plant_care_guide_schema import PlantCareGuideResponse

from app.controllers.plant_species_controller import (
    list_plant_species,
    get_plant_species,
    get_care_guide
)

# from app.controllers.plant_care_guide_controller import get_care_guide

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

router.get(
    path="/{plant_species_uid}",
    status_code = status.HTTP_200_OK,
    response_model = PlantSpeciesReadResponse,
    summary="get Plant species by UID"
)(get_plant_species)

router.get(
    path="/{plant_species_uid}/care-guide",
    response_model = PlantCareGuideResponse,
    status_code = status.HTTP_200_OK,
    summary="Get plant care guide by plant species UID"
)(get_care_guide)