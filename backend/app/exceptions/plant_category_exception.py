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