from uuid import UUID
from typing import Literal
from pydantic import BaseModel

class TokenPayload(BaseModel):
    sub: UUID
    jti: UUID
    type: Literal["access", "refresh"]
    exp: int
    iat: int
    iss: str | None = None # Issuer -> Who created (plantive-api)
    aud: str | None = None # Audience -> Who is allowed to use this token? (mobile-app, web-app, admin-panel)

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: Literal["Bearer"] = "Bearer"