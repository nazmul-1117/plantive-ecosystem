from pydantic import BaseModel
from datetime import datetime
import uuid
from sqlmodel import Field
from typing import Optional


class UserInDB(BaseModel):
    user_uid: uuid.UUID
    
    first_name: str
    last_name: Optional[str] = None
    
    email: str
    username: str
    
    password_hash: Optional[str] = None
    auth_provider: str
    
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    
    is_active: bool
    is_verified: bool

    created_at: datetime
    updated_at: datetime


class UserCreate(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    email: str
    username: str
    password: str

class UserRead(BaseModel):
    user_uid: uuid.UUID

    ftrst_name: str
    last_name: Optional[str] = None

    email: str
    username: str
    auth_provider: str

    avatar_url: Optional[str] = None
    bio: Optional[str] = None

    is_active: bool
    is_verified: bool

    created_at: datetime
    updated_at: datetime

class UserUpdate(UserCreate):
    pass


# auth
class LoginRequest(BaseModel):
    username: str
    email: str | None = None
    password: str

class TokenResponse(BaseModel):
    pass



# Role
# | Column        | Type                      |
# | --------------| --------------------------|
# | role_uid      | UUID PK                   |
# | name          | VARCHAR(50) UNIQUE        |
# | description   | TEXT                      |
# | is_active     | BOOLEAN                   |
# | created_at    | TIMESTAMP DEFAULT TRUE    |
# | updated_at    | TIMESTAMP DEFAULT TRUE    |
class RoleInDB(BaseModel):
    role_uid: uuid.UUID
    name: str
    description: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True

class RoleRead(BaseModel):
    role_uid: uuid.UUID
    name: str
    description: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

class RoleUpdate(BaseModel):
    pass



# Role User

class UserRoleInDB(BaseModel):
    pass

class UserRoleCreate(BaseModel):
    pass

class UserRoleRead(BaseModel):
    pass

class UserRoleUpdate(BaseModel):
    pass
