
# routers/admin/user_routers.py -> admin router

from fastapi import APIRouter, status
from app.schemas.admin.user_schema import (
    AdminUserReadResponse,
    AdminUserListParams,
    AdminUserListResponse,
    AdminUserDeleteResponse,
    AdminRoleResponse
)
from app.schemas.admin.role_schema import AdminRoleReadResponse

from app.controllers.admin.user_controller import (
    get_users,
    get_user_by_uid,
    update_user,
    delete_user,
    get_user_roles,
    assign_user_roles,
    get_roles
)

router = APIRouter(
    prefix="/users",
    tags=["Admin Users"],
)

# temp roles
router.get(
    path="/roles",
    status_code=status.HTTP_200_OK,
    response_model=list[AdminRoleReadResponse],
    summary="Get all roles"
)(get_roles)


# User Management
router.get(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=AdminUserListResponse,
    summary="Get users list"
)(get_users)

router.get(
    path="/{user_uid}",
    status_code=status.HTTP_200_OK,
    response_model=AdminUserReadResponse,
    summary="Get user by UID"
)(get_user_by_uid)

router.patch(
    path="/{user_uid}",
    status_code=status.HTTP_200_OK,
    response_model=AdminUserReadResponse,
    summary="Update user"
)(update_user)

router.delete(
    path="/{user_uid}",
    status_code=status.HTTP_200_OK,
    response_model=AdminUserDeleteResponse,
    summary="Delete user"
)(delete_user)


# User Roles
router.get(
    path="/{user_uid}/roles",
    status_code=status.HTTP_200_OK,
    response_model=list[AdminRoleResponse],
    summary="Get user roles"
)(get_user_roles)

router.post(
    path="/{user_uid}/roles",
    status_code=status.HTTP_200_OK,
    response_model=list[AdminRoleResponse],
    summary="Assign user roles"
)(assign_user_roles)

# Authentication Management