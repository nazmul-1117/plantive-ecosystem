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
