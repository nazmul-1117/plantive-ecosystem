
# app/models/plant_care_guide.py

from datetime import datetime, timezone
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import (
    Boolean,
    Column, 
    DateTime, 
    Field, 
    ForeignKey,
    Relationship,
    SQLModel, 
    Text,
    text,
    true
)

if TYPE_CHECKING:
    from app.models.plant_species import PlantSpecies


def utc_now() -> datetime:
    return datetime.now(timezone.utc)

class PlantCareGuide(SQLModel, table=True):

    """
    Core and maintenance guidance for a plant species
    """

    __tablename__ = "plant_care_guides"

    plant_care_guide_uid: UUID = Field(
        default_factory=uuid4,
        sa_column=Column(
            pg.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
            server_default=text("gen_random_uuid()"),
        ),
    )

    plant_species_uid: UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True),
            ForeignKey(
                "plant_species.plant_species_uid",
                ondelete="CASCADE",
            ),
            unique=True,
            nullable=False,
        ),
    )

    watering_guide: str = Field(
        sa_column=Column(
            Text,
            nullable=False,
        ),
    )

    fertilizer_guide: str | None = Field(
        default=None,
        sa_column=Column(
            Text,
            nullable=True,
        ),
    )

    pruning_guide: str | None = Field(
        default=None,
        sa_column=Column(
            Text,
            nullable=True,
        ),
    )

    common_problems: str | None = Field(
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
        default_factory=utc_now,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            # default=utc_now,
            onupdate=utc_now,
            server_default=text("CURRENT_TIMESTAMP"),
        ),
    )

    plant_species: "PlantSpecies" = Relationship(
        back_populates="care_guide",
    )


    def __repr__(self) -> str:
        return (
            f"<PlantCareGuide("
            f"plant_care_guide_uid = {self.plant_care_guide_uid!r}, "
            f"plant_species_uid = {self.plant_species_uid!r}"
            f")>"
        )