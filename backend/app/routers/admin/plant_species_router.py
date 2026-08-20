# admin/plant_router.py - admin

from fastapi import APIRouter, status
from typing import List
from app.schemas.admin.plant_species_schema import (
    AdminPlantSpeciesListItem,
    AdminPlantSpeciesListResponse,
)

from app.controllers.admin.plant_species_controller import (
    list_plant_species,
)

admin_plant_species_router = APIRouter(
    prefix="/plant-species",
    tags=["Admin - Plant Species"],
)

admin_plant_species_router.get(
    path="",
    status_code = status.HTTP_200_OK,
    response_model = AdminPlantSpeciesListResponse,
    summary="List plant species"
)(list_plant_species)

