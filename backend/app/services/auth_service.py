
import time
from sqlmodel.ext.asyncio.session import AsyncSession
from redis.asyncio import Redis

from app.schemas.auth_schema import LoginRequest, LoginResponse
from app.schemas.token_schema import AccessTokenResponse

from app.services.token_service import TokenService
from app.services.user_service import UserService

from app.repositories.user_repository import UserRepository

from app.models.auth_model import User
from app.schemas.token_schema import TokenPayload
from app.schemas.auth_schema import LogoutResponse

from app.core.jwt import create_token
from app.core.security import verity_hashed_password

from app.exceptions.user_exception import UserNotFound
from app.exceptions.auth_exception import InvalidLoginCredentials


"""
AuthService.register()

↓

user_repository.get_by_email()

↓

user_repository.get_by_username()

↓

hash password

↓

User(...)

↓

user_repository.create()

↓

role_repository.get_by_name()

↓

user_role_repository.assign()

↓

commit()

↓

return user
"""

# AuthService
    # register()
    # login()
    # logout()
    # refresh_token()

class AuthService:

    def __init__(
            self,
            token_service: TokenService,
            user_repository: UserRepository
    ):
        self.token_service = token_service
        self.user_repository = user_repository
    
    async def login(
            self,
            login_credentials: LoginRequest,
    ) -> LoginResponse:
        
        user: User | None = await self.user_repository.get_by_username(
            username=login_credentials.username,
        )

        if user is None or not verity_hashed_password(
            password=login_credentials.password,
            hashed_password=user.password_hash
        ):
            raise InvalidLoginCredentials()

        access_token: str = create_token(
            user_uid= str(user.user_uid)
        )

        refresh_token: str = create_token(
            user_uid= str(user.user_uid),
            token_type="refresh"
        )

        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer"
        )

    async def logout(
            self,
            token_payload: TokenPayload,
    ) -> LogoutResponse:
        
        jti: str = token_payload.jti
        ttl: int = max(1, token_payload.exp - int(time.time()))
        
        await self.token_service.revoke_token(
            jti=jti,
            ttl=ttl,
        )

        return LogoutResponse(
            success=True
        )

    async def refresh_access_token(
            self,
            token_payload: TokenPayload,
    ) -> AccessTokenResponse:
        
        user: User | None = await self.user_repository.get_by_uid(
            user_uid=token_payload.sub,
        )

        if user is None:
            raise UserNotFound()
        
        new_access_token: str = create_token(
            user_uid=str(user.user_uid)
        )

        return AccessTokenResponse(
            access_token=new_access_token
        )
