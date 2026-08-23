# app/schemas/admin/plant_category_schema.py -> admin

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, model_validator, HttpUrl, field_validator

from app.constants.plant_constant import SunlightRequirement, PlantSpeciesSort


# create
class AdminPlantCategoryCreateRequest(BaseModel):

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid"
    )

    name: str = Field(
        ge=3,
        le=50,
    )

    description: str | None = None
    image_url: HttpUrl | None = None

    @field_validator("name", mode="before")
    @classmethod
    def normalize_name(
        cls,
        value: str
    ) -> str:

        return value.strip()

    @field_validator("image_url", mode="after")
    @classmethod
    def normalize_name(
        cls,
        value: HttpUrl | None
    ) -> str:

        if isinstance(value, HttpUrl):
            return str(value)

        return value


#summary
class AdminPlantCategorySummary(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    plant_category_uid: UUID
    name: str
    image_url: str | None = None

    is_active: bool
    created_at: datetime
    updated_at: datetime

# read response
class AdminPlantCategoryResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    plant_category_uid: UUID
    name: str
    slug: str

    description: str | None = None
    image_url: str | None = None

    is_active: bool
    created_at: datetime
    updated_at: datetime

class AdminPlantCategoryListResponse(BaseModel):

    """
    Paginated plant categories response
    """

    page: int
    page_size: int

    total: int
    total_pages: int

    items: list[AdminPlantCategorySummary] = Field(
        default_factory=list,
    )

class AdminPlantCategoryListParams(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    search: str | None = None
    is_active: bool | None = None

    page: int = Field(
        default=1,
        ge=1,
    )

    page_size: int = Field(
        default=20,
        ge=1,
        le=100,
    )

