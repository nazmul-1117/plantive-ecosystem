import uuid
from datetime import datetime, timezone
# from typing import Optional

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import SQLModel, Field, Column, String, DateTime, Relationship, text, ForeignKey


class UserRole(SQLModel, table=True):
    __tablename__ = "user_roles"

    user_uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True),
            ForeignKey(
                "users.user_uid",
                ondelete="CASCADE"
            ),
            primary_key=True,
            nullable=False,
        )
    )

    role_uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True),
            ForeignKey(
                "roles.role_uid",
                ondelete="CASCADE"
            ),
            primary_key=True,
            nullable=False,
        )
    )

    assigned_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
        ),
    )

    def __repr__(self) -> str:
        return f"""<UserRole(
            user_uid: {self.user_uid},
            role_uid: {self.role_uid}
        )>
        """

class User(SQLModel, table=True):
    __tablename__ = "users"

    user_uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True),
            nullable=False,
            primary_key=True,
            server_default=text("gen_random_uuid()")
        ),
        default_factory=uuid.uuid4
    )

    first_name: str = Field(
        sa_column=Column(
            pg.VARCHAR(50),
            nullable=False
        )
    )

    last_name: str | None = Field(
        default=None,
        sa_column=Column(
            pg.VARCHAR(50),
            nullable=True,
        ),
    )
    
    email: str = Field(
        sa_column=Column(
            String,
            unique=True,
            nullable=False,
            index=True,
        ),
    )
    
    username: str = Field(
        max_length=16,
        sa_column=Column(
            String,
            unique=True,
            nullable=False,
            index=True
        )
    )
    
    password_hash: str | None = Field(
        default=None,
        sa_column=Column(
            pg.TEXT,
            nullable=True
        )
    )

    auth_provider: str = Field(
        default="email",
        sa_column=Column(
            pg.VARCHAR(16),
            nullable=False
        )
    )

    avatar_url: str | None = Field(
        default=None,
        sa_column=Column(
            pg.VARCHAR(255),
            nullable=True
        )
    )
    
    bio: str | None = Field(
        default=None,
        sa_column=Column(
            pg.TEXT,
            nullable=True
        )
    )

    is_active: bool = Field (
        default=True
    )
    
    is_verified: bool = Field(
        default=False
    )
    
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
        ),
    )
    
    updated_at: datetime = Field(
        # default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            default=lambda: datetime.now(timezone.utc),
            onupdate=lambda: datetime.now(timezone.utc)
        )
    )
    

    roles: list["Role"] = Relationship(
        back_populates="users",
        link_model=UserRole
    )

    def __repr__(self) -> str:
        return f"""<User(
            user_uid: {self.user_uid}
            username: {self.username},
            full_name: {self.first_name},
        )>
        """
    
class Role(SQLModel, table=True):
    __tablename__ = "roles"

    role_uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True),
            nullable=False,
            primary_key=True,
            server_default=text("gen_random_uuid()")
        ),
        default_factory=uuid.uuid4
    )

    name: str = Field(
        max_length=16,
        unique=True,
        index=True,
        nullable=False
    )

    description: str | None = Field(
        default=None,
        sa_column=Column(
            pg.TEXT,
            nullable=True
        )
    )

    is_active: bool = Field (
        default=True
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False
        )
    )
    
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            default=lambda: datetime.now(timezone.utc),
            onupdate=lambda: datetime.now(timezone.utc)
        )
    )

    users: list["User"] = Relationship(
        back_populates="roles",
        link_model=UserRole
    )
    
    def __repr__(self) -> str:
        return f"""<Role(
            role_uid: {self.role_uid}
            role_name: {self.name},
            is_active: {self.is_active},
        )>
        """