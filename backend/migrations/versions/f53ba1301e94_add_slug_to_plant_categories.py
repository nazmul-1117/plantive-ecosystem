"""add slug to plant categories

Revision ID: f53ba1301e94
Revises: 6b46d1bc9648
Create Date: 2026-08-19 21:10:15.137031

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = "f53ba1301e94"
down_revision: Union[str, Sequence[str], None] = "6b46d1bc9648"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "plant_categories",
        sa.Column(
            "slug",
            sa.String(length=50),
            nullable=False,
        ),
    )

    op.create_unique_constraint(
        "uq_plant_categories_slug",
        "plant_categories",
        ["slug"],
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint(
        "uq_plant_categories_slug",
        "plant_categories",
        type_="unique",
    )

    op.drop_column(
        "plant_categories",
        "slug",
    )