from fastapi import status
from app.exceptions.base_exception import AppException

class PlantNotFound(AppException):
    """
    Raised when the requested plant does not exist
    """

    def __init__(self):
        super().__init__(
            message="Plant not found.",
            error_code="PLANT_NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND
        )