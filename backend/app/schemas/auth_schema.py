from pydantic import BaseModel, ConfigDict, EmailStr, model_validator
from datetime import datetime
import uuid
from sqlmodel import Field
from typing import Optional

# UserCreate
# UserLogin
# UserRead
# RegisterResponse
# LoginResponse
# LoginRequest, RegisterRequest, LoginResponse

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

    model_config = ConfigDict(from_attributes=True)

    user_uid: uuid.UUID

    first_name: str
    last_name: str | None = None

    email: str
    username: str
    auth_provider: str

    avatar_url: str | None = None
    bio: str | None = None

    is_active: bool
    is_verified: bool

    created_at: datetime
    updated_at: datetime

class UserUpdate(BaseModel):
    pass

class UserResponse(BaseModel):
    success: bool
    message: str
    data: UserRead | None = None



# auth
class LoginRequest(BaseModel):
    username: str
    email: str | None = None
    password: str

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user: UserRead | None = None

class LogoutResponse(BaseModel):
    success: bool
    message: str = "Logged out successfully."

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


# Original Auth Model
class EmailVerificationResponse(BaseModel):
    message: str
    email: EmailStr

class ChangePasswordRequest(BaseModel):
    old_password: str = Field(min_length=8)
    new_password: str = Field(min_length=8)
    confirm_new_password: str

    @model_validator(mode="after")
    def passwords_match(self):
       if self.new_password != self.confirm_new_password:
           raise ValueError("New passwords do not match")

       if self.old_password == self.new_password:
           raise ValueError(
               "New password must be different from the old password"
           )

       return self


class ChangePasswordResponse(BaseModel):
    status: bool
    details: str