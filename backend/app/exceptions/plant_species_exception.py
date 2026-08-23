from fastapi import status
from app.exceptions.base_exception import AppException

class PlantSpeciesNotFound(AppException):
    """
    Raised when the requested plant does not exist
    """

    def __init__(self):
        super().__init__(
            message="Plant not found.",
            error_code="PLANT_NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND
        )

class PlantSpeciesAlreadyExists(AppException):
    """
    Raised when the requested plant already exists
    """

    def __init__(self):
        super().__init__(
            message="Plant already exists.",
            error_code="PLANT_ALREADY_EXISTS",
            status_code=status.HTTP_404_NOT_FOUND
        )

class InvalidPlantSpeciesUpdate(AppException):
    """
    Raised when the requested plant update field is None
    """

    def __init__(self):
        super().__init__(
            message="Invalid Plant Species Update.",
            error_code="INVALID_PLANT_UPDATE",
            status_code=status.HTTP_404_NOT_FOUND
        )