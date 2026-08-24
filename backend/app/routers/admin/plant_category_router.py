# routers/admin/plant_category_router.py -> admin

from fastapi import APIRouter, status

from app.schemas.admin.plant_category_schema import (
    AdminPlantCategoryResponse,
    AdminPlantCategoryListResponse,
)

from app.controllers.admin.plant_category_controller import (
    list_plant_categories,
    get_plant_category,
    create_plant_category,
    update_plant_category,
    activate_plant_category,
    deactivate_plant_category
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


admin_plant_category_router.get(
    path="/{plant_category_uid}",
    response_model = AdminPlantCategoryResponse,
    status_code = status.HTTP_200_OK,
    summary="Get plant category"
)(get_plant_category)


admin_plant_category_router.post(
    path="",
    response_model = AdminPlantCategoryResponse,
    status_code = status.HTTP_201_CREATED,
    summary="Create plant category"
)(create_plant_category)


admin_plant_category_router.patch(
    path="/{plant_category_uid}",
    response_model = AdminPlantCategoryResponse,
    status_code = status.HTTP_200_OK,
    summary="Update plant category",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Plant category not found",
        },
        status.HTTP_409_CONFLICT: {
            "description": "Plant category already exists",
        },
    },
)(update_plant_category)


admin_plant_category_router.post(
    path="/{plant_category_uid}/activate",
    response_model = AdminPlantCategoryResponse,
    status_code = status.HTTP_200_OK,
    summary="Activate plant category",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Plant category not found",
        },
        status.HTTP_409_CONFLICT: {
            "description": "Plant category already exists",
        },
    },
)(activate_plant_category)


admin_plant_category_router.post(
    path="/{plant_category_uid}/deactivate",
    response_model = AdminPlantCategoryResponse,
    status_code = status.HTTP_200_OK,
    summary="Deactivate plant category",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Plant category not found",
        },
        status.HTTP_409_CONFLICT: {
            "description": "Plant category already exists",
        },
    },
)(deactivate_plant_category)