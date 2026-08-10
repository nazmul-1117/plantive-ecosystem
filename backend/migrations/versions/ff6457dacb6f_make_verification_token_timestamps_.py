"""make verification token timestamps timezone aware

Revision ID: ff6457dacb6f
Revises: 12c4fe6cfe40
Create Date: 2026-08-10 15:01:57.688446

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'ff6457dacb6f'
down_revision: Union[str, Sequence[str], None] = '12c4fe6cfe40'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
