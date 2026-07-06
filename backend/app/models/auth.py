from sqlmodel import SQLModel, Field, Column, String, DateTime
import uuid
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime, timezone

class User(SQLModel, table=True):
    __tablename__ = "users"

    user_uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True),
            nullable=False,
            primary_key=True
        ),
        default_factory=uuid.uuid4
    )

    full_name: str = Field(max_length=255)
    email: str = Field(sa_column=Column(String, unique=True, nullable=False))
    username: str = Field(sa_column=Column(String, unique=True, nullable=False))
    password_hashed: str
    is_active: bool = Field (default=True)
    is_verified: bool = Field (default=False)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False)
        )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False)
        )
    
    
    def __repr__(self):
        return f"<User: {self.username}, Full_Name: {self.full_name}>"