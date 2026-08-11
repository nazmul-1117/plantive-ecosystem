"""create password_reset_tokens table

Revision ID: c0529050b05c
Revises: 68aad6c1e4cc
Create Date: 2026-08-11 11:46:25.326796

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'c0529050b05c'
down_revision: Union[str, Sequence[str], None] = '68aad6c1e4cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
