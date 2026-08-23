# routers/admin/plant_category_router.py -> admin

from fastapi import APIRouter, status

from app.schemas.admin.plant_category_schema import (
    AdminPlantCategoryResponse,
    AdminPlantCategoryListResponse,
)

from app.controllers.admin.plant_category_controller import (
    list_plant_categories
)


admin_plant_category_router = APIRouter(
    prefix="/plant-categories",
    tags=["Admin - Plant Categories"],
)


admin_plant_category_router.get(
    path="",
    response_model = AdminPlantCategoryListResponse,
    status_code = status.HTTP_200_OK,
    summary="List plant categories"
)(list_plant_categories)