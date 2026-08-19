
# app/models/plant_species.py

from datetime import datetime, timezone
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import (
    Boolean,
    CheckConstraint,
    Column, 
    DateTime, 
    Field, 
    Float, 
    Integer,
    Relationship,
    SQLModel,
    String,
    Text,
    text,
    true,
)

from app.constants.plant_constant import SunlightRequirement
from app.models.plant_species_category import PlantSpeciesCategory

if TYPE_CHECKING:
    from app.models.plant_category import PlantCategory
    from app.models.plant_care_guide import PlantCareGuide


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class PlantSpecies(SQLModel, table=True):

    """
    Master/Catalog data describing a plant species
    """

    __tablename__ = "plant_species"

    __table_args__ = (
        CheckConstraint(
            "watering_frequency_days > 0",
            name="ck_plant_species_watering_frequency_positive",
        ),
        CheckConstraint(
            "ideal_humidity_min_percent IS NULL "
            "OR ideal_humidity_min_percent BETWEEN 0 AND 100",
            name="ck_plant_species_humidity_min_range",
        ),
        CheckConstraint(
            "ideal_humidity_max_percent IS NULL "
            "OR ideal_humidity_max_percent BETWEEN 0 AND 100",
            name="ck_plant_species_humidity_max_range",
        ),
        CheckConstraint(
            "ideal_soil_moisture_min_percent IS NULL "
            "OR ideal_soil_moisture_min_percent BETWEEN 0 AND 100",
            name="ck_plant_species_soil_moisture_min_range",
        ),
        CheckConstraint(
            "ideal_soil_moisture_max_percent IS NULL "
            "OR ideal_soil_moisture_max_percent BETWEEN 0 AND 100",
            name="ck_plant_species_soil_moisture_max_range",
        ),
        CheckConstraint(
            "ideal_temp_min_c IS NULL "
            "OR ideal_temp_max_c IS NULL "
            "OR ideal_temp_min_c <= ideal_temp_max_c",
            name="ck_plant_species_temperature_range",
        ),
        CheckConstraint(
            "ideal_humidity_min_percent IS NULL "
            "OR ideal_humidity_max_percent IS NULL "
            "OR ideal_humidity_min_percent <= ideal_humidity_max_percent",
            name="ck_plant_species_humidity_range",
        ),
        CheckConstraint(
            "ideal_soil_moisture_min_percent IS NULL "
            "OR ideal_soil_moisture_max_percent IS NULL "
            "OR ideal_soil_moisture_min_percent <= ideal_soil_moisture_max_percent",
            name="ck_plant_species_moisture_range",
        ),
        CheckConstraint(
            "sunlight_requirement IN "
            "('FULL_SUN', 'PARTIAL_SUN', 'PARTIAL_SHADE', 'FULL_SHADE')",
            name="ck_plant_species_sunlight_requirement",
        ),
    )


    plant_species_uid: UUID = Field(
        default_factory=uuid4,
        sa_column=Column(
            pg.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
            server_default=text("gen_random_uuid()"),
        ),
    )

    common_name: str = Field(
        max_length=100,
        sa_column=Column(
            String(100),
            nullable=False,
        ),
    )

    scientific_name: str = Field(
        max_length=150,
        sa_column=Column(
            String(150),
            nullable=False,
            unique=True,
        ),
    )

    description: str | None = Field(
        default=None,
        max_length=512,
        sa_column=Column(
            Text,
            nullable=True,
        ),
    )

    ideal_temp_min_c: float | None = Field(
        default=None,
        sa_column=Column(
            Float,
            nullable=True,
        ),
    )

    ideal_temp_max_c: float | None = Field(
        default=None,
        sa_column=Column(
            Float,
            nullable=True,
        ),
    )

    ideal_humidity_min_percent: float | None = Field(
        default=None,
        sa_column=Column(
            Float,
            nullable=True,
        ),
    )

    ideal_humidity_max_percent: float | None = Field(
        default=None,
        sa_column=Column(
            Float,
            nullable=True,
        ),
    )

    ideal_soil_moisture_min_percent: float | None = Field(
        default=None,
        sa_column=Column(
            Float,
            nullable=True,
        ),
    )

    ideal_soil_moisture_max_percent: float | None = Field(
        default=None,
        sa_column=Column(
            Float,
            nullable=True,
        ),
    )

    sunlight_requirement: SunlightRequirement = Field(
        max_length=32,
        sa_column=Column(
            String(32),
            nullable=False,
        ),
    )

    watering_frequency_days: int = Field(
        sa_column=Column(
            Integer,
            nullable=False,
        ),
    )

    image_url: str | None = Field(
        default=None,
        sa_column=Column(
            Text,
            nullable=True,
        ),
    )

    is_active: bool = Field(
        default=True,
        sa_column=Column(
            Boolean,
            nullable=False,
            server_default=true(),
        ),
    )

    created_at: datetime = Field(
        default_factory=utc_now,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        ),
    )
    
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            default=utc_now,
            onupdate=utc_now,
            server_default=text("CURRENT_TIMESTAMP"),
        ),
    )

    categories: list["PlantCategory"] = Relationship(
        back_populates="plant_species",
        link_model=PlantSpeciesCategory,
    )

    care_guide: "PlantCareGuide" = Relationship(
        back_populates="plant_species",
    )


    def __repr__(self) -> str:
        return (
            f"<PlantSpecies("
                f"plant_species_uid = {self.plant_species_uid!r}, "
                f"common_name = {self.common_name!r}, "
                f"scientific_name = {self.scientific_name!r}, "
                f"description = {self.description!r}"
            f")>"
        )