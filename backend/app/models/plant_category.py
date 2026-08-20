
# app/models/plant_category.py

from datetime import datetime, timezone
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import (
    Boolean,
    Column, 
    DateTime, 
    Field, 
    Relationship,
    SQLModel, 
    String,
    Text,
    text,
    true,
)

from app.models.plant_species_category import PlantSpeciesCategory
if TYPE_CHECKING:
    from app.models.plant_species import PlantSpecies


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class PlantCategory(SQLModel, table=True):

    __tablename__ = "plant_categories"

    plant_category_uid: UUID = Field(
        default_factory=uuid4,
        sa_column=Column(
            pg.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
            server_default=text("gen_random_uuid()"),
        ),
    )

    name: str = Field(
        max_length=50,
        sa_column=Column(
            String(50),
            nullable=False,
            unique=True,
        ),
    )

    slug: str = Field(
        max_length=50,
        sa_column=Column(
            String(50),
            nullable=False,
            unique=True,
            index=True,
        ),
    )

    description: str | None = Field(
        default=None,
        sa_column=Column(
            Text,
            nullable=True,
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

    plant_species: list["PlantSpecies"] = Relationship(
        back_populates="categories",
        link_model=PlantSpeciesCategory,
    )

    def __repr__(self) -> str:
        return (
            f"<PlantCategory("
            f"plant_category_uid = {self.plant_category_uid!r}, "
            f"name = {self.name!r}"
            f")>"
        )

