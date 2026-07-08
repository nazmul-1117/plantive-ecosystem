from pydantic import BaseModel
from datetime import datetime
import uuid
from sqlmodel import Field


class UserInDB(BaseModel):
    user_uid: uuid.UUID
    full_name: str
    email: str
    username: str
    password_hashed: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime


class UserCreate(BaseModel):
    full_name: str
    email: str
    username: str
    plain_password: str

class UserRead(BaseModel):
    user_uid: uuid.UUID
    full_name: str
    email: str
    username: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

class UserUpdate(UserCreate):
    pass


# auth
class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    pass

# class PayloadSchema(BaseModel):
#     sub

#         payload = {
#         "sub": user_uid,
#         "type": token_type,
#         "iat": now,
#         "exp": expire,
#         "jti": str(uuid.uuid4())
#     }
