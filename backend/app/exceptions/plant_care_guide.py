from fastapi import status
from app.exceptions.base_exception import AppException

class PlantCareGuideNotFound(AppException):
    """
    Raised when the requested plant care guide does not exist
    """

    def __init__(self):
        super().__init__(
            message="Plant Care Guide not found.",
            error_code="PLANT_CARE_GUIDE_NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND
        )

class PlantCareGuideRequired(AppException):
    """
    Raised when the requested plant care guide are required
    """

    def __init__(self):
        super().__init__(
            message="Plant Care Guide Required.",
            error_code="PLANT_CARE_GUIDE_REQUIRED",
            status_code=status.HTTP_404_NOT_FOUND
        )