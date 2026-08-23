# app/schemas/admin/plant_species_schema.py -> admin

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, model_validator, HttpUrl, field_validator

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
class PlantCareGuideCreateRequest(BaseModel):

    model_config = ConfigDict(extra="forbid")

    watering_guide: str = Field(
        min_length=1,
        max_length=5000,
    )
    fertilizer_guide: str | None = Field(
        default=None,
        max_length=5000,
    )
    pruning_guide: str | None = Field(
        default=None,
        max_length=5000,
    )
    common_problems: str | None = Field(
        default=None,
        max_length=5000,
    )

class AdminPlantSpeciesCreateRequest(BaseModel):

    """
    Request payload for creating a plant species
    """

    model_config = ConfigDict(extra="forbid")

    common_name: str = Field(
        min_length=3,
        max_length=100
    )

    scientific_name: str = Field(
        min_length=2,
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

    image_url: HttpUrl | None = None

    plant_category_uids: list[UUID] = Field(
        default_factory=list,
    )

    care_guide: PlantCareGuideCreateRequest | None = None

    @model_validator(mode="after")
    def validate_ranges(self):
        if (
            self.ideal_temp_min_c is not None
            and self.ideal_temp_max_c is not None
            and self.ideal_temp_min_c > self.ideal_temp_max_c
        ):
            raise ValueError(
                "ideal_temp_min_c must be less than or equal to "
                "ideal_temp_max_c"
            )

        if (
            self.ideal_humidity_min_percent is not None
            and self.ideal_humidity_max_percent is not None
            and self.ideal_humidity_min_percent > self.ideal_humidity_max_percent
        ):
            raise ValueError(
                "ideal_humidity_min_percent must be less than or equal to "
                "ideal_humidity_max_percent"
            )

        if (
            self.ideal_soil_moisture_min_percent is not None
            and self.ideal_soil_moisture_max_percent is not None
            and self.ideal_soil_moisture_min_percent > self.ideal_soil_moisture_max_percent
        ):
            raise ValueError(
                "ideal_soil_moisture_min_percent must be less than or equal to "
                "ideal_soil_moisture_max_percent"
            )

        return self

    @field_validator("plant_category_uids")
    @classmethod
    def validate_unique_category_uids(
        cls,
        value: list[UUID],
    ) -> list[UUID]:
        
        if len(value) != len(set(value)):
            raise ValueError(
                "plant_category_uids must contain unique values"
            )

        return value

# Update schemas

class PlantCareGuideUpdateRequest(BaseModel):

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    watering_guide: str | None = Field(
        default=None,
        min_length=1,
        max_length=5000,
    )
    fertilizer_guide: str | None = Field(
        default=None,
        max_length=5000,
    )
    pruning_guide: str | None = Field(
        default=None,
        max_length=5000,
    )
    common_problems: str | None = Field(
        default=None,
        max_length=5000,
    )
    is_active: bool | None = None

class AdminPlantSpeciesUpdateRequest(BaseModel):
    """
    Plant Species update request
    """
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    common_name: str | None = Field(
        default=None,
        min_length=3,
        max_length=100
    )
    scientific_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=150,
    )

    description: str | None = Field(
        default=None,
        max_length=512,
    )

    ideal_temp_min_c: float | None = Field(
        default=None,
        ge=-40,
        le=70,
    )
    ideal_temp_max_c: float | None = Field(
        default=None,
        ge=-40,
        le=70,
    )

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

    image_url: HttpUrl | None = None

    plant_category_uids: list[UUID] | None = None
    care_guide: PlantCareGuideUpdateRequest | None = None

    @model_validator(mode="after")
    def validate_ranges(self):
        if (
            self.ideal_temp_min_c is not None
            and self.ideal_temp_max_c is not None
            and self.ideal_temp_min_c > self.ideal_temp_max_c
        ):
            raise ValueError(
                "ideal_temp_min_c must be less than or equal to "
                "ideal_temp_max_c"
            )

        if (
            self.ideal_humidity_min_percent is not None
            and self.ideal_humidity_max_percent is not None
            and self.ideal_humidity_min_percent > self.ideal_humidity_max_percent
        ):
            raise ValueError(
                "ideal_humidity_min_percent must be less than or equal to "
                "ideal_humidity_max_percent"
            )

        if (
            self.ideal_soil_moisture_min_percent is not None
            and self.ideal_soil_moisture_max_percent is not None
            and self.ideal_soil_moisture_min_percent > self.ideal_soil_moisture_max_percent
        ):
            raise ValueError(
                "ideal_soil_moisture_min_percent must be less than or equal to "
                "ideal_soil_moisture_max_percent"
            )

        return self

    @field_validator("plant_category_uids")
    @classmethod
    def validate_unique_category_uids(
        cls,
        value: list[UUID],
    ) -> list[UUID]:
        
        if len(value) != len(set(value)):
            raise ValueError(
                "plant_category_uids must contain unique values"
            )

        return value




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