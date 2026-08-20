from uuid import UUID
from pydantic import BaseModel, ConfigDict

class PlantCareGuideResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    plant_species_uid: UUID
    watering_guide: str
    fertilizer_guide: str | None = None
    pruning_guide: str | None = None
    common_problems: str | None = None
