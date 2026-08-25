
# app/schemas/plant_species_schema.py

import re
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, model_validator, field_validator

from app.constants.plant_constant import SunlightRequirement, PlantSpeciesSort

class PlantCategorySummaryResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    plant_category_uid: UUID
    name: str
    slug: str

class PlantSpeciesReadResponse(BaseModel):
    
    """
    Plant species Read Response
    """
    model_config = ConfigDict(from_attributes=True)

    plant_species_uid: UUID

    common_name: str
    scientific_name: str
    description: str | None = None

    ideal_temp_min_c: float | None = None
    ideal_temp_max_c: float | None = None

    ideal_humidity_min_percent: float | None = None
    ideal_humidity_max_percent: float | None = None

    ideal_soil_moisture_min_percent: float | None = None
    ideal_soil_moisture_max_percent: float | None = None

    sunlight_requirement: SunlightRequirement
    watering_frequency_days: int

    image_url: str | None = None

    categories: list[PlantCategorySummaryResponse] = Field(
        default_factory=list,
    )

class PlantSpeciesListItem(BaseModel):

    """
    Simple Plant Summary
    """

    model_config = ConfigDict(from_attributes=True)

    plant_species_uid: UUID
    common_name: str
    scientific_name: str

    image_url: str | None = None

    categories: list[PlantCategorySummaryResponse] = Field(
        default_factory=list,
    )

class PlantSpeciesListParams(BaseModel):

    """
    Plant species list/filter parameters
    """

    model_config = ConfigDict(extra="forbid")

    search: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    category: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
    )

    sunlight_requirement: SunlightRequirement | None = None

    sort: PlantSpeciesSort = PlantSpeciesSort.COMMON_NAME

    min_temp: float | None = Field(
        default=None,
        ge=-50,
        le=70,
    )

    max_temp: float | None = Field(
        default=None,
        ge=-50,
        le=70,
    )

    page: int = Field(
        default=1,
        ge=1,
    )

    page_size: int = Field(
        default=20,
        ge=1,
        le=100,
    )


    @model_validator(mode="after")
    def validate_temparature_range(self):
        if (
            self.min_temp is not None
            and self.max_temp is not None
            and self.min_temp > self.max_temp
        ):
            raise ValueError(
                "min_temp must be less then or equal to max_temp"
            )

        return self

    @field_validator("category", mode="before")
    @classmethod
    def slugify(
        cls,
        value: str | None
    ) -> str | None:

        if value is None:
            return None

        value = value.strip().lower()
        value = re.sub(r"[^a-z0-9\s-]", "", value)
        value = re.sub(r"[\s-]+", "-", value)

        return value.strip("-") or None

class PlantSpeciesReadListResponse(BaseModel):

    """
    Paginated plant species response
    """

    page: int
    page_size: int

    total: int
    total_pages: int

    items: list[PlantSpeciesListItem] = Field(
        default_factory=list,
    )


# Plant care guide
class PlantSpeciesSummary(BaseModel):
    
    """
    Plant species Summary
    """
    model_config = ConfigDict(from_attributes=True)
    
    plant_species_uid: UUID
    common_name: str
    scientific_name: str

    image_url: str | None = None

class PlantCareGuideData(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    watering_guide: str
    fertilizer_guide: str | None = None
    pruning_guide: str | None = None
    common_problems: str | None = None

class PlantCareGuideResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)
    
    plant_species: PlantSpeciesSummary
    care_guide: PlantCareGuideData