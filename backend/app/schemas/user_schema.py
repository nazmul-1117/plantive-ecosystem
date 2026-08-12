from pydantic import BaseModel, ConfigDict, EmailStr, Field
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
    first_name: str
    last_name: str | None = None
    avatar_url: str | None = None
    bio: str | None = None
    email: EmailStr
    username: str = Field(min_length=3)
    password: str = Field(min_length=8)

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

class UserUpdateRequest(BaseModel):
    pass

class UserResponse(BaseModel):
    success: bool
    message: str
    data: UserReadResponse | None = None

