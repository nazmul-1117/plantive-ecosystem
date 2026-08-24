from fastapi import status
from app.exceptions.base_exception import AppException

class PlantCategoryNotFound(AppException):
    """
    Raised when the requested plant category does not exist
    """

    def __init__(self):
        super().__init__(
            message="Plant Category found.",
            error_code="PLANT_CATEGORY_NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND
        )

class PlantCategoryAlreadyExists(AppException):
    """
    Raised when the created plant category Already Exists
    """

    def __init__(self):
        super().__init__(
            message="Plant Category Already Exists.",
            error_code="PLANT_CATEGORY_ALREADY_EXISTS",
            status_code=status.HTTP_409_CONFLICT
        )

class InvalidPlantCategoryUpdate(AppException):
    """
    Raised when the requested plant category update field is None
    """

    def __init__(self):
        super().__init__(
            message="Invalid Plant Catgory Update.",
            error_code="INVALID_PLANT_CATEGORY_UPDATE",
            status_code=status.HTTP_404_NOT_FOUND
        )