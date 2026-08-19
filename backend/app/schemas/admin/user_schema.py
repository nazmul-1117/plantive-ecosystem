
# schemas/admin/user_schema.py -> admin

from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator, SecretStr


# Role
class AdminRoleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    role_uid: UUID
    name: str
    description: str | None = None
    is_active: bool



# User
class AdminUserUpdateRequest(BaseModel):

    """
    Fields an administrator is allowed to modify directly through the general user-management endpoint
    """

    model_config = ConfigDict(extra="forbid")

    # Profile
    first_name: str | None = Field(
        default=None,
        min_length=3,
        max_length=50
    )

    last_name: str | None = Field(
        default=None,
        min_length=3,
        max_length=50
    )

    username: str | None = Field(
        default=None,
        min_length=6,
        max_length=32
    )

    email: EmailStr | None = None

    bio: str | None = Field(
        default=None,
        max_length=500
    )

    # Account management
    is_active: bool | None = None

    # Verification management
    is_verified: bool | None = None

class AdminUserPasswordResetRequest(BaseModel):

    model_config = ConfigDict(extra="forbid")

    new_password: SecretStr = Field(
        min_length=8,
        max_length=128,
    )

    confirm_new_password: SecretStr = Field(
        min_length=8,
        max_length=128,
    )

    @model_validator(mode="after")
    def passwords_match(self):
       if (
           self.new_password.get_secret_value()
           !=
           self.confirm_new_password.get_secret_value()
       ):
           raise ValueError("New passwords do not match")

       return self

class AdminUserReadResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    user_uid: UUID

    # profiles
    first_name: str
    last_name: str | None = None
    email: EmailStr
    username: str

    # authenticate
    auth_provider: str
    is_verified: bool

    # authorizations
    roles: list[AdminRoleResponse] = Field(default_factory=list)

    # account state
    is_active: bool

    # Profile information
    avatar_url: str | None = None
    bio: str | None = None

    # Audit
    created_at: datetime
    updated_at: datetime


class AdminUserPasswordResetResponse(BaseModel):
    status: bool
    details: str = "Password Reset Successfully"

# class AdminUserUpdateResponse(BaseModel):
#     message: str = Field(default="Profile updated successfully")
#     user: AdminUserReadResponse = Field(default_factory=list)

class AdminUserDeleteResponse(BaseModel):
    status: bool
    message: str = Field(default="User deleted successfully")


# List
class AdminUserListParams(BaseModel):

    search: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    is_active: bool | None = None
    is_verified: bool | None = None

    role: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
    )

    page: int = Field(
        default=1,
        ge=1,
    )

    page_size: int = Field(
        default=20,
        ge=1,
        le=100,
    )

class AdminUserListResponse(BaseModel):
    
    page: int
    page_size: int
    total: int
    total_page: int

    items: list[AdminUserReadResponse] = Field(default_factory=list)

# activate-deactivate
class AdminUserActivateResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    user_uid: UUID
    first_name: str
    email: EmailStr
    username: str
    is_active: bool

class AdminUserDeactivateResponse(AdminUserActivateResponse):
    pass