
# app/models/plant_species_category.py

from uuid import UUID
from datetime import datetime, timezone

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import (
    Column, 
    DateTime, 
    Field, 
    ForeignKey,
    SQLModel, 
    text,
)

class PlantSpeciesCategory(SQLModel, table=True):

    """
    Association between plant species and plant categories

    A species can belong to multiple categories, and a category can contain multiple plant species
    """

    __tablename__ = "plant_species_categories"

    plant_species_uid: UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True),
            ForeignKey(
                "plant_species.plant_species_uid",
                ondelete="CASCADE",
            ),
            primary_key=True,
            nullable=False,
        ),
    )

    plant_category_uid: UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True),
            ForeignKey(
                "plant_categories.plant_category_uid",
                ondelete="CASCADE",
            ),
            primary_key=True,
            nullable=False,
        ),
    )

    assigned_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        ),
    )

    def __repr__(self) -> str:
        return (
            f"<PlantSpeciesCategory("
            f"plant_species_uid = {self.plant_species_uid!r}, "
            f"plant_category_uid = {self.plant_category_uid!r}, "
            f"assigned_at = {self.assigned_at!r}"
            f")>"
        )

