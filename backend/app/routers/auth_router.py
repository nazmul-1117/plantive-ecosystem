from fastapi import APIRouter, status

from app.controllers.auth_controller import create_user

auth_router = APIRouter()

auth_router.post(
    path="/signup",
    status_code=status.HTTP_201_CREATED
)(create_user)