
import time
from datetime import datetime, timedelta, timezone

from sqlalchemy.exc import SQLAlchemyError

from app.schemas.auth_schema import LoginRequest, LoginResponse, LogoutResponse
from app.schemas.token_schema import AccessTokenResponse, TokenPayload
from app.schemas.password_reset_schema import ForgotPasswordResponseSchema, ResetPasswordResponseSchema, ResetPasswordRequestSchema

from app.services.token_service import TokenService
from app.services.email_service import EmailService

from app.repositories.user_repository import UserRepository
from app.repositories.password_reset_token_repository import PasswordResetTokenRepository

from app.models.auth_model import User
from app.models.verification_token_model import PasswordResetToken

from app.core.jwt import create_token
from app.core.security import verity_hashed_password, generate_hash_password
from app.core.tokens import generate_secret_token, hash_token
from app.core.config import settings

from app.exceptions.user_exception import UserNotFound, UserInactive
from app.exceptions.auth_exception import (
    InvalidLoginCredentials,
    AccountNotVerified
)
from app.exceptions.password_reset_exception import (
    PasswordResetTokenAlreadyUsedError,
    PasswordResetTokenExpiredError,
    PasswordResetTokenRevokedError,
    InvalidPasswordResetTokenError
)

class AuthService:

    def __init__(
            self,
            token_service: TokenService,
            user_repository: UserRepository,
            password_reset_token_repository: PasswordResetTokenRepository,
            email_service: EmailService
    ):
        self.token_service = token_service
        self.user_repository = user_repository
        self.password_reset_token_repository = password_reset_token_repository
        self.email_service = email_service
    
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

    async def forgot_password(
            self,
            user: User,
    ) -> ForgotPasswordResponseSchema:
        
        if not user.is_active:
            raise UserInactive() 

        if not user.is_verified:
            raise AccountNotVerified()

        # Generate secret token
        raw_token, token_hash = generate_secret_token()

        reset_token = PasswordResetToken(
            user_uid=user.user_uid,
            token_hash=token_hash,
            expires_at = (
                datetime.now(timezone.utc)
                + timedelta(minutes=30)
            ),
        )

        reset_token = await self.password_reset_token_repository.create_token(reset_token)

        try:
            await self.password_reset_token_repository.commit()
            await self.password_reset_token_repository.refresh(reset_token)

        except SQLAlchemyError:
            await self.password_reset_token_repository.rollback()
            raise

        reset_url = (
            f"{settings.BACKEND_PUBLIC_URL}"
            f"/api/{settings.API_VERSION}/auth"
            f"/reset-password"
            f"?token={raw_token}"
        )

        await self.email_service.send_verification_email(
            email = user.email,
            verification_url = reset_url
        )

        return ForgotPasswordResponseSchema(
            status=True,
            details="Forgot Password verification link send to your email",
        )

    async def reset_password(
            self,
            reset_data: ResetPasswordRequestSchema,
            raw_token: str
    ) -> ResetPasswordResponseSchema:
        
        token_hash = hash_token(raw_token)

        reset_token: PasswordResetToken | None = await self.password_reset_token_repository.get_by_hash(token_hash)

        if reset_token is None:
            raise InvalidPasswordResetTokenError()

        now = datetime.now(timezone.utc)

        if reset_token.revoked_at is not None:
            raise PasswordResetTokenRevokedError()

        if reset_token.used_at is not None:
            raise PasswordResetTokenAlreadyUsedError()

        if reset_token.expires_at <= now:
            raise PasswordResetTokenExpiredError()

        user: User = await  self.user_repository.get_by_uid(
            user_uid = reset_token.user_uid
        )

        if user is None:
            raise UserNotFound()

        user.password_hash = generate_hash_password(reset_data.new_password)
        reset_token.used_at = now

        try:
            await self.user_repository.update(user)
            await self.password_reset_token_repository.update(reset_token)
            await self.user_repository.commit()

        except SQLAlchemyError:
            await self.user_repository.rollback()
            raise

        
        return ResetPasswordResponseSchema(
            status=True,
            details="Passwordd has been reset successfully",
        )     