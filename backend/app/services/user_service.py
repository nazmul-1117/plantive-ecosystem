
from uuid import UUID
from datetime import datetime, timezone, timedelta

from sqlalchemy.exc import SQLAlchemyError

from app.schemas.user_schema import UserCreateRequest, UserUpdateRequest, UserDeleteRequest, UserDeleteResponse
from app.schemas.password_schema import ChangePasswordRequest, ChangePasswordResponse

from app.models.auth_model import User
from app.models.verification_token_model import VerificationToken

from app.core.security import generate_hash_password, verify_hashed_password
from app.core.tokens import hash_token, generate_secret_token
from app.core.config import settings

from app.repositories.user_repository import UserRepository
from app.repositories.role_repository import RoleRepository
from app.repositories.user_role_repository import UserRoleRepository
from app.repositories.verification_token_repository import VerificationTokenRepository

from app.exceptions.user_exception import (
    EmailAlreadyExists,
    UsernameAlreadyExists,
    UserNotFound
)
from app.exceptions.role_exception import RoleNotFound
from app.exceptions.auth_exception import (
    InvalidVerificationTokenError,
    VerificationTokenExpiredError,
    VerificationTokenAlreadyUsedError,
    InvalidPasswordException
)

from app.constants.roles_constant import RoleConstant


class UserService:
    """
    Don't raise HTTPException in the service—use custom domain exceptions and let the controller translate them into HTTP responses.
    """

    def __init__(
            self,
            user_repository: UserRepository,
            role_repository: RoleRepository,
            user_role_repository: UserRoleRepository,
            verification_token_repository: VerificationTokenRepository,
    ):
        self.user_repository = user_repository
        self.role_repository = role_repository
        self.user_role_repository = user_role_repository
        self.verification_token_repository = verification_token_repository
    
    async def register_user(
            self,
            user_data: UserCreateRequest,
    ) -> tuple[User, str]:
        
        existing_user = await self.user_repository.get_by_email(
            email=user_data.email,
        )
        
        if existing_user is not None:
            raise EmailAlreadyExists()

        existing_user = await self.user_repository.get_by_username(
            username=user_data.username,
        )

        if existing_user is not None:
            raise UsernameAlreadyExists()
        
        # user_data.password = generate_hash_password(user_data.password)
        user = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            avatar_url=user_data.avatar_url,
            bio=user_data.bio,
            username=user_data.username,
            password_hash=generate_hash_password(user_data.password)
        )

        user_table = await self.user_repository.create(
            user=user,
        )

        role_table = await self.role_repository.get_by_name(
            role_name=RoleConstant.USER,
        )

        if role_table is None:
            raise RoleNotFound()

        await self.user_role_repository.assign_role(
            user_uid=user_table.user_uid,
            role_uid=role_table.role_uid,
        )

        # Generate row token
        raw_token, token_hash = generate_secret_token()

        verification_token = VerificationToken(
            user_uid = user_table.user_uid,
            token_hash = token_hash,
            expires_at = (
                datetime.now(timezone.utc)
                + timedelta(minutes=30)
            ),
        )

        await self.verification_token_repository.create_token(
            db_token=verification_token
        )

        try:
            await self.user_repository.commit()
            await self.user_repository.refresh(user_table)

        except SQLAlchemyError:
            await self.user_repository.rollback()
            raise

        verification_url = (
            f"{settings.FRONTEND_PUBLIC_URL}"
            f"/verify-email"
            f"?token={raw_token}"
        )

        return user_table, verification_url
    
    async def get_by_uid(
            self,
            user_uid: UUID,
    ) -> User:
        
        user: User | None = await self.user_repository.get_by_uid(
            user_uid=user_uid,
        )

        if user is None:
            raise UserNotFound()

        return user

    async def get_by_email(
            self,
            email: str
    ) -> User:

        user: User | None = await self.user_repository.get_by_email(email)

        if user is None:
            raise UserNotFound()

        return user

    async def get_by_username(
            self,
            username: str
    ) -> User | None:

        user: User | None = await self.user_repository.get_by_username(username)

        if user is None:
            raise UserNotFound()

        return user
        
    async def update_profile(
            self,
            user: User,
            update_data: UserUpdateRequest
    ) -> User:

        update_fields: dict = update_data.model_dump(exclude_unset=True)

        if not update_fields:
            return user

        if "username" in update_fields:
            username = update_fields["username"]

            if username != user.username:
                existing_user = await self.user_repository.get_by_username(username)

                if existing_user is not None:
                    raise UsernameAlreadyExists()

        for field, value in update_fields.items():
            setattr(user, field, value)

        user = await self.user_repository.update(user=user)

        try:
            await self.user_repository.commit()
            await self.user_repository.refresh(user)

        except SQLAlchemyError:
            await self.user_repository.rollback()
            raise

        return user

    async def delete_account(
            self,
            user: User,
            delete_data: UserDeleteRequest
    ) -> UserDeleteResponse:
        
        is_password_matches: bool = verify_hashed_password(
            password = delete_data.password.get_secret_value(),
            hashed_password = user.password_hash
        )

        if not is_password_matches:
            raise InvalidPasswordException()

        is_deleeted: bool = await self.user_repository.delete(
            user_uid=user.user_uid
        )

        if not is_deleeted:
            raise UserNotFound()

        try:
            await self.user_repository.commit()

        except SQLAlchemyError:
            await self.user_repository.rollback()
            raise

        return UserDeleteResponse(
            status = True
        )        

    async def change_password(
            self,
            password_data: ChangePasswordRequest,
            user_uid: UUID
    ):

        user: User = await self.get_by_uid(user_uid)

        is_password_matches: bool = verify_hashed_password(
            password = password_data.old_password,
            hashed_password = user.password_hash,
        )

        if not is_password_matches:
            raise InvalidPasswordException()

        hash_password: str = generate_hash_password(
            password = password_data.new_password
        )

        user.password_hash = hash_password

        user = await self.user_repository.update(user)
        
        try:
            await self.user_repository.commit()
            await self.user_repository.refresh(user)

        except SQLAlchemyError:
            await self.user_repository.rollback()
            raise

        return ChangePasswordResponse(
            status=True,
            details="Password changed successfully."
        )
    
    async def verify_email(
            self,
            raw_token: str
    ) -> User:

        """
        Verifies a user's email using provided raw token.
        Enforce single-use protection and expiration checks.
        """

        # 1. compute hash to query
        token_hash: str = hash_token(raw_token)
        db_token: VerificationToken | None = await self.verification_token_repository.get_by_hash(token_hash)

        # 2. check token exist or not
        if db_token is None:
            raise InvalidVerificationTokenError()

        # 3. check expiration
        now = datetime.now(timezone.utc)

        if db_token.revoked_at is not None:
            raise VerificationTokenExpiredError()

        if db_token.used_at is not None:
            raise VerificationTokenAlreadyUsedError()

        if db_token.expires_at <= now:
            raise VerificationTokenExpiredError()

        # 5. Fetch assosiate user
        user: User = await self.user_repository.get_by_uid(
            user_uid = db_token.user_uid
        )

        if not user:
            raise UserNotFound()

        # 5. ALready verified or not
        if user.is_verified:
            db_token.used_at = now

            await self.verification_token_repository.update(db_token)
            await self.verification_token_repository.commit()

            return user

        # 6. Update userstate
        user.is_verified = True
        db_token.used_at = now
        
        try: 
            await self.user_repository.update(user)
            await self.verification_token_repository.update(db_token)

            await self.user_repository.commit()
            await self.user_repository.refresh(user)

        except SQLAlchemyError:
            await self.user_repository.rollback()
            raise

        return user

