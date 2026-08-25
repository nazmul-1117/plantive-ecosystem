
# ========================================================================================
#                  app/schemas/plant_category_schema.py  -> Public
# ========================================================================================

from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.constants.plant_constant import PlantSpeciesSort

#summary
class PlantCategorySummary(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    plant_category_uid: UUID
    name: str
    image_url: str | None = None


# read response
class PlantCategoryResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    plant_category_uid: UUID
    name: str
    slug: str

    description: str | None = None
    image_url: str | None = None

class PlantCategoryListResponse(BaseModel):

    """
    Paginated plant categories response
    """

    page: int
    page_size: int

    total: int
    total_pages: int

    items: list[PlantCategorySummary] = Field(
        default_factory=list,
    )

class PlantCategoryListParams(BaseModel):
    model_config = ConfigDict(extra="forbid")

    search: str | None = None

    page: int = Field(
        default=1,
        ge=1,
    )

    page_size: int = Field(
        default=20,
        ge=1,
        le=100,
    )


    @field_validator("search", mode="before")
    @classmethod
    def normalize_search(
        cls,
        value: str | None
    ) -> str | None:

        if value is None:
            return None

        return value.strip() or None



# plant species
class PlantSpeciesSummary(BaseModel):
    
    """
    Summary Representation of a Plant species
    """
    model_config = ConfigDict(from_attributes=True)
    
    plant_species_uid: UUID
    common_name: str
    scientific_name: str

    image_url: str | None = None

class PlantSpeciesListResponse(BaseModel):


    """
    Paginated plant species belonging to a plant category.
    """

    page: int
    page_size: int

    total: int
    total_pages: int

    plant_category_uid: UUID
    name: str
    image_url: str | None
    
    items: list[PlantSpeciesSummary] = Field(
        default_factory=list,
    )


class PlantSpeciesListParams(PlantCategoryListParams):

    sort: PlantSpeciesSort = Field(
        default=PlantSpeciesSort.SCIENTIFIC_NAME,
    )
