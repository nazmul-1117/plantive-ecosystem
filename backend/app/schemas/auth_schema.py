from pydantic import BaseModel, ConfigDict, EmailStr, model_validator
from sqlmodel import Field

from app.schemas.user_schema import UserReadResponse

# auth
class LoginRequest(BaseModel):
    identifier: str = Field(min_length=3)
    password: str = Field(min_length=8)

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user: UserReadResponse | None = None

class LogoutResponse(BaseModel):
    success: bool
    message: str = "Logged out successfully."

# Original Auth Model
class EmailVerificationResponse(BaseModel):
    message: str
    email: EmailStr