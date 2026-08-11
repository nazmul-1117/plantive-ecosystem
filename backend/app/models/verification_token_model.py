from uuid import UUID, uuid4
from datetime import datetime, timezone, timedelta

from sqlmodel import SQLModel, Field, Column, DateTime, ForeignKey

class VerificationToken(SQLModel, table=True):
    __tablename__ = "verification_tokens"

    token_uid: UUID = Field(
        default_factory = uuid4,
        primary_key = True
    )

    user_uid: UUID = Field(
        sa_column=Column(
            ForeignKey(
                "users.user_uid",
                ondelete="CASCADE",
            ),
            nullable=False,
            index=True,
        ),
    )

    token_hash: str = Field(
        max_length = 64,
        unique = True,
        index = True,
        nullable = False
    )

    expires_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False
        )
    )

    created_at: datetime = Field(
        default_factory = lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False
        )
    )

    revoked_at: datetime | None = Field(
        default = None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=True
        ),
    )

    used_at: datetime | None = Field(
        default = None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=True
        ),
    )

    def __repr__(self) -> str:
        return (
            f"<VerificationToken("
            f"token_uid={self.token_uid}"
            f"user_uid={self.user_uid}"
            f"expires_at={self.expires_at}"
            f"created_at={self.created_at}"
            f"revoked_at={self.revoked_at}"
            f"used_at={self.used_at}"
            f")>"
        )


class PasswordResetToken(SQLModel, table=True):
    __tablename__ = "password_reset_tokens"

    password_reset_token_uid: UUID = Field(
        default_factory = uuid4,
        primary_key = True
    )

    user_uid: UUID = Field(
        sa_column=Column(
            ForeignKey(
                "users.user_uid",
                ondelete="CASCADE",
            ),
            nullable=False,
            index=True,
        ),
    )

    token_hash: str = Field(
        max_length = 64,
        unique = True,
        index = True,
        nullable = False
    )

    expires_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False
        )
    )

    created_at: datetime = Field(
        default_factory = lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False
        )
    )

    revoked_at: datetime | None = Field(
        default = None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=True
        ),
    )

    used_at: datetime | None = Field(
        default = None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=True
        ),
    )

    def __repr__(self) -> str:
        return (
            f"<PasswordResetToken("
            f"password_reset_token_uid={self.password_reset_token_uid}"
            f"user_uid={self.user_uid}"
            f"expires_at={self.expires_at}"
            f"created_at={self.created_at}"
            f"revoked_at={self.revoked_at}"
            f"used_at={self.used_at}"
            f")>"
        )