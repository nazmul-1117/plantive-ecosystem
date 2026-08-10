"""fix user role foreign key cascade

Revision ID: f8b11ea3e5a1
Revises: ff6457dacb6f
Create Date: 2026-08-10 20:34:55.526292
"""

from typing import Sequence, Union

from alembic import op


revision: str = "f8b11ea3e5a1"
down_revision: Union[str, Sequence[str], None] = "ff6457dacb6f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # users -> user_roles
    op.drop_constraint(
        "user_roles_user_uid_fkey",
        "user_roles",
        type_="foreignkey",
    )

    op.create_foreign_key(
        "user_roles_user_uid_fkey",
        "user_roles",
        "users",
        ["user_uid"],
        ["user_uid"],
        ondelete="CASCADE",
    )

    # roles -> user_roles
    op.drop_constraint(
        "user_roles_role_uid_fkey",
        "user_roles",
        type_="foreignkey",
    )

    op.create_foreign_key(
        "user_roles_role_uid_fkey",
        "user_roles",
        "roles",
        ["role_uid"],
        ["role_uid"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    # users -> user_roles
    op.drop_constraint(
        "user_roles_user_uid_fkey",
        "user_roles",
        type_="foreignkey",
    )

    op.create_foreign_key(
        "user_roles_user_uid_fkey",
        "user_roles",
        "users",
        ["user_uid"],
        ["user_uid"],
    )

    # roles -> user_roles
    op.drop_constraint(
        "user_roles_role_uid_fkey",
        "user_roles",
        type_="foreignkey",
    )

    op.create_foreign_key(
        "user_roles_role_uid_fkey",
        "user_roles",
        "roles",
        ["role_uid"],
        ["role_uid"],
    )