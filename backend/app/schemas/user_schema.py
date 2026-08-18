from pydantic import BaseModel, ConfigDict, EmailStr, Field, SecretStr
from datetime import datetime
import uuid

class UserInDB(BaseModel):
    user_uid: uuid.UUID
    
    first_name: str
    last_name: str | None = None
    
    email: EmailStr
    username: str
    
    
    password_hash: str | None= None
    auth_provider: str
    
    avatar_url: str | None = None
    bio: str | None = None
    
    is_active: bool
    is_verified: bool

    created_at: datetime
    updated_at: datetime


class UserCreateRequest(BaseModel):

    model_config = ConfigDict(extra="forbid")

    first_name: str = Field(
        default="anonymous",
        min_length=3,
        max_length=100
    )

    last_name: str | None = Field(
        default=None,
        min_length=3,
        max_length=100
    )

    username: str | None = Field(
        default=None,
        min_length=6,
        max_length=32
    )

    bio: str | None = Field(
        default=None,
        max_length=500
    )

    password: str = Field(
        min_length=8
    )

    avatar_url: str | None = None
    email: EmailStr

class UserReadResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    user_uid: uuid.UUID

    first_name: str
    last_name: str | None = None

    email: EmailStr
    username: str
    auth_provider: str

    avatar_url: str | None = None
    bio: str | None = None

    is_active: bool
    is_verified: bool

    created_at: datetime
    updated_at: datetime

class UserResponse(BaseModel):
    success: bool
    message: str
    data: UserReadResponse | None = None



class UserUpdateRequest(BaseModel):

    model_config = ConfigDict(extra="forbid")

    first_name: str | None = Field(
        default=None,
        min_length=3,
        max_length=100
    )

    last_name: str | None = Field(
        default=None,
        min_length=3,
        max_length=100
    )

    username: str | None = Field(
        default=None,
        min_length=6,
        max_length=32
    )

    bio: str | None = Field(
        default=None,
        max_length=500
    )

class UserUpdateResponse(BaseModel):
    message: str = Field(default="Profile updated successfully")
    user: UserReadResponse



class UserDeleteRequest(BaseModel):

    model_config = ConfigDict(extra="forbid")

    password: SecretStr = Field(min_length=8)
    feedback: str | None = Field(
        default=None,
        max_length=100
    )

class UserDeleteResponse(BaseModel):
    status: bool
    message: str = Field(default="User deleted successfully")