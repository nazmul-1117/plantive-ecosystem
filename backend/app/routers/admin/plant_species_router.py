# admin/plant_router.py - admin

from fastapi import APIRouter, status
from typing import List
from app.schemas.admin.plant_species_schema import (
    AdminPlantSpeciesResponse,
    AdminPlantSpeciesListResponse,
    AdminPlantSpeciesListItem,
)

from app.controllers.admin.plant_species_controller import (
    list_plant_species,
    get_plant_species,
    create_plant_species,
    update_plant_species,
    activate_plant_species,
    deactivate_plant_species,
)

admin_plant_species_router = APIRouter(
    prefix="/plant-species",
    tags=["Admin - Plant Species"],
)

admin_plant_species_router.get(
    path="",
    response_model = AdminPlantSpeciesListResponse,
    status_code = status.HTTP_200_OK,
    summary="List plant species"
)(list_plant_species)


admin_plant_species_router.get(
    path="/{plant_species_uid}",
    response_model = AdminPlantSpeciesResponse,
    status_code = status.HTTP_200_OK,
    summary="Get Plant species by UID"
)(get_plant_species)


admin_plant_species_router.post(
    path="",
    response_model = AdminPlantSpeciesResponse,
    status_code = status.HTTP_201_CREATED,
    summary="Create Plant Species"
)(create_plant_species)

admin_plant_species_router.patch(
    path="/{plant_species_uid}",
    response_model = AdminPlantSpeciesResponse,
    status_code = status.HTTP_200_OK,
    summary="Update Plant Species"
)(update_plant_species)

admin_plant_species_router.post(
    path="/{plant_species_uid}/activate",
    response_model = AdminPlantSpeciesListItem,
    status_code = status.HTTP_200_OK,
    summary="Activate Plant species"
)(activate_plant_species)

admin_plant_species_router.post(
    path="/{plant_species_uid}/deactivate",
    response_model = AdminPlantSpeciesListItem,
    status_code = status.HTTP_200_OK,
    summary="Deactivate Plant species"
)(deactivate_plant_species)
