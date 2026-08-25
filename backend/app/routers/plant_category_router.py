
# ========================================================================================
#                  app/routers/plant_category_router.py -> Public
# ========================================================================================

from fastapi import APIRouter, status

from app.schemas.plant_category_schema import (
    PlantCategoryResponse,
    PlantCategoryListResponse,
    PlantSpeciesListResponse,
)

from app.controllers.plant_category_controller import (
    list_plant_categories,
    get_plant_category,
    get_plant_species,
)


plant_category_router = APIRouter(
    prefix="/plant-categories",
    tags=["User - Plant Categories"],
)


plant_category_router.get(
    path="",
    response_model = PlantCategoryListResponse,
    status_code = status.HTTP_200_OK,
    summary="List plant categories"
)(list_plant_categories)


plant_category_router.get(
    path="/{plant_category_uid}",
    response_model = PlantCategoryResponse,
    status_code = status.HTTP_200_OK,
    summary="Get plant category"
)(get_plant_category)


plant_category_router.get(
    path="/{plant_category_uid}/plant-species",
    response_model = PlantSpeciesListResponse,
    status_code = status.HTTP_200_OK,
    summary="Get plant Species by category"
)(get_plant_species)