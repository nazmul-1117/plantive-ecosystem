
# app/service/plant_care_guide_service.py

from uuid import UUID
from sqlalchemy.exc import SQLAlchemyError

from app.repositories.plant_care_guide_repository import PlantCareGuideRepository
from app.models.plant_care_guide import PlantCareGuide
from app.exceptions.plant_care_guide import PlantCareGuideNotFound


class PlantCareGuideService:

    def __init__(
            self,
            plant_care_guide_repository: PlantCareGuideRepository
    ):
        self.plant_care_guide_repository = plant_care_guide_repository
