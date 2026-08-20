# app/schemas/admin/plant_species_schema.py -> admin

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.constants.plant_constant import SunlightRequirement, PlantSpeciesSort
from app.schemas.plant_species_schema import (
    PlantSpeciesListParams,

)

# schema naming vocabulary could be
"""
Data - embedded representation
Summary - lightweight embedded representation
Response - top-level API response
ListItem - item inside a list response
"""

# create schema
class AdminPlantSpeciesCreateRequest(BaseModel):

    """
    Plant species creation request
    """

    model_config = ConfigDict(extra="forbid")

    common_name: str = Field(
        min_length=3,
        max_length=100
    )

    scientific_name: str = Field(
        max_length=150
    )

    description: str | None = Field(
        default=None,
        max_length=512,
    )

    ideal_temp_min_c: float | None = None
    ideal_temp_max_c: float | None = None

    ideal_humidity_min_percent: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    ideal_humidity_max_percent: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    ideal_soil_moisture_min_percent: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    ideal_soil_moisture_max_percent: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    sunlight_requirement: SunlightRequirement

    watering_frequency_days: int = Field(
        ge=1,
    )

    image_url: str | None = None

    category_uids: list[UUID] = Field(
        default_factory=list
    )

# Update schemas
class AdminPlantSpeciesUpdateRequest(BaseModel):
    """
    Plant Species update request
    """
    model_config = ConfigDict(extra="forbid")

    common_name: str | None = Field(
        default=None,
        min_length=3,
        max_length=100
    )

    scientific_name: str | None = Field(
        default=None,
        max_length=150
    )

    description: str | None = Field(
        default=None,
        max_length=512,
    )

    ideal_temp_min_c: float | None = None
    ideal_temp_max_c: float | None = None

    ideal_humidity_min_percent: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    ideal_humidity_max_percent: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    ideal_soil_moisture_min_percent: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    ideal_soil_moisture_max_percent: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    sunlight_requirement: SunlightRequirement | None = None

    watering_frequency_days: int | None = Field(
        default=None,
        ge=1,
    )

    image_url: str | None = None



class AdminPlantCategorySummary(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    plant_category_uid: UUID
    name: str
    slug: str

    description: str | None = None
    image_url: str | None = None

    is_active: bool
    created_at: datetime
    updated_at: datetime

class AdminPlantCareGuideResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    plant_care_guide_uid: UUID
    plant_species_uid: UUID

    watering_guide: str
    fertilizer_guide: str | None = None
    pruning_guide: str | None = None
    common_problems: str | None = None

    is_active: bool
    created_at: datetime
    updated_at: datetime

class AdminPlantSpeciesListItem(BaseModel):
    
    """
    Plant species Read Response
    """

    model_config = ConfigDict(from_attributes=True)

    plant_species_uid: UUID
    common_name: str
    scientific_name: str

    sunlight_requirement: SunlightRequirement
    image_url: str | None = None

    is_active: bool
    created_at: datetime
    updated_at: datetime

    categories: list[AdminPlantCategorySummary] = Field(
        default_factory=list,
    )

class AdminPlantSpeciesResponse(BaseModel):
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

    is_active: bool
    created_at: datetime
    updated_at: datetime

    categories: list[AdminPlantCategorySummary] = Field(
        default_factory=list,
    )
    care_guide: AdminPlantCareGuideResponse | None = None

class AdminPlantSpeciesListResponse(BaseModel):

    """
    Paginated plant species response
    """

    page: int
    page_size: int

    total: int
    total_pages: int

    items: list[AdminPlantSpeciesListItem] = Field(
        default_factory=list,
    )


# parameters
class AdminPlantSpeciesListParams(PlantSpeciesListParams):
    is_active: bool | None = None