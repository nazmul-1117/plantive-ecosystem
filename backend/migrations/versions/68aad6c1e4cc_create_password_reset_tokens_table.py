"""create password_reset_tokens table

Revision ID: 68aad6c1e4cc
Revises: f8b11ea3e5a1
Create Date: 2026-08-11 11:43:07.648350

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.

revision: str = "68aad6c1e4cc"
down_revision: Union[str, Sequence[str], None] = "f8b11ea3e5a1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "password_reset_tokens",

        sa.Column(
            "password_reset_token_uid",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),

        sa.Column(
            "user_uid",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),

        sa.Column(
            "token_hash",
            sa.String(length=64),
            nullable=False,
        ),

        sa.Column(
            "expires_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),

        sa.Column(
            "revoked_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),

        sa.Column(
            "used_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),

        sa.ForeignKeyConstraint(
            ["user_uid"],
            ["users.user_uid"],
            ondelete="CASCADE",
        ),

        sa.PrimaryKeyConstraint(
            "password_reset_token_uid",
        ),
    )

    op.create_index(
        op.f("ix_password_reset_tokens_user_uid"),
        "password_reset_tokens",
        ["user_uid"],
        unique=False,
    )

    op.create_index(
        op.f("ix_password_reset_tokens_token_hash"),
        "password_reset_tokens",
        ["token_hash"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_password_reset_tokens_token_hash"),
        table_name="password_reset_tokens",
    )

    op.drop_index(
        op.f("ix_password_reset_tokens_user_uid"),
        table_name="password_reset_tokens",
    )

    op.drop_table("password_reset_tokens")