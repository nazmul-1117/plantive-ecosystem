from pydantic import BaseModel, ConfigDict, EmailStr, model_validator
from sqlmodel import Field
from datetime import datetime
from uuid import UUID

class RoleInDB(BaseModel):
    role_uid: UUID
    name: str
    description: str | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

class RoleCreate(BaseModel):
    name: str
    description: str | None = None
    is_active: str | None = True

class RoleRead(BaseModel):
    role_uid: UUID
    name: str
    description: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

class RoleUpdate(BaseModel):
    pass
