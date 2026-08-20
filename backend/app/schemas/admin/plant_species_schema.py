# create schema
# class PlantSpeciesCreateRequest(BaseModel):

#     """
#     Plant species creation request
#     """

#     model_config = ConfigDict(extra="forbid")

#     common_name: str = Field(
#         min_length=3,
#         max_length=100
#     )

#     scientific_name: str = Field(
#         max_length=150
#     )

#     description: str | None = Field(
#         default=None,
#         max_length=512,
#     )

#     ideal_temp_min_c: float | None = None
#     ideal_temp_max_c: float | None = None

#     ideal_humidity_min_percent: float | None = Field(
#         default=None,
#         ge=0,
#         le=100,
#     )

#     ideal_humidity_max_percent: float | None = Field(
#         default=None,
#         ge=0,
#         le=100,
#     )

#     ideal_soil_moisture_min_percent: float | None = Field(
#         default=None,
#         ge=0,
#         le=100,
#     )

#     ideal_soil_moisture_max_percent: float | None = Field(
#         default=None,
#         ge=0,
#         le=100,
#     )

#     sunlight_requirement: SunlightRequirement

#     watering_frequency_days: int = Field(
#         ge=1,
#     )

#     image_url: str | None = None

#     category_uids: list[UUID] = Field(
#         default_factory=list
#     )

# Update schemas
# class PlantSpeciesUpdateRequest(BaseModel):
#     """
#     Plant Species update request
#     """
#     model_config = ConfigDict(extra="forbid")

#     common_name: str | None = Field(
#         default=None,
#         min_length=3,
#         max_length=100
#     )

#     scientific_name: str | None = Field(
#         default=None,
#         max_length=150
#     )

#     description: str | None = Field(
#         default=None,
#         max_length=512,
#     )

#     ideal_temp_min_c: float | None = None
#     ideal_temp_max_c: float | None = None

#     ideal_humidity_min_percent: float | None = Field(
#         default=None,
#         ge=0,
#         le=100,
#     )

#     ideal_humidity_max_percent: float | None = Field(
#         default=None,
#         ge=0,
#         le=100,
#     )

#     ideal_soil_moisture_min_percent: float | None = Field(
#         default=None,
#         ge=0,
#         le=100,
#     )

#     ideal_soil_moisture_max_percent: float | None = Field(
#         default=None,
#         ge=0,
#         le=100,
#     )

#     sunlight_requirement: SunlightRequirement | None = None

#     watering_frequency_days: int | None = Field(
#         default=None,
#         ge=1,
#     )

#     image_url: str | None = None

