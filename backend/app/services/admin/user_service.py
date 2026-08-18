
# service/admin/user_service -> admin

from uuid import UUID
from sqlalchemy.exc import SQLAlchemyError

from app.models.auth_model import User
from app.repositories.user_repository import UserRepository
from app.schemas.admin.user_schema import (
    AdminUserUpdateRequest,
    AdminUserDeleteResponse,
    AdminUserListResponse,
    AdminUserListParams,
    AdminUserPasswordResetResponse,
    AdminUserPasswordResetRequest
)

from app.exceptions.user_exception import (
    UserNotFound,
    UsernameAlreadyExists,
    EmailAlreadyExists
)

from app.core.security import generate_hash_password


class AdminUserService:

    def __init__(
            self,
            user_repository: UserRepository,
    ):
        
        self.user_repository = user_repository


    async def list_users(
            self,
            params: AdminUserListParams
    ) -> AdminUserListResponse:

         offset = (
             params.page - 1
         ) * params.page_size
        
         users, total = await self.user_repository.get_users(
             search=params.search,
             is_active=params.is_active,
             is_verified=params.is_verified,
             role=params.role,
             offset=offset,
             limit=params.page_size,
         )

         total_pages = (
             (total + params.page_size - 1)
             // params.page_size
             if total > 0
             else 0
         )

         return AdminUserListResponse(
             items=users,
             page=params.page,
             page_size=params.page_size,
             total=total,
             total_page=total_pages,
         )

    async def get_user_by_uid(
            self,
            user_uid: UUID,
    ) -> User:
        
        user: User | None = await self.user_repository.get_by_uid(
            user_uid=user_uid,
        )

        if user is None:
            raise UserNotFound()

        return user

    async def update_user(
            self,
            user: User,
            update_data: AdminUserUpdateRequest
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

        if "email" in update_fields:
            email = update_fields["email"]

            if email != user.email:
                existing_user = (
                    await self.user_repository.get_by_email(
                        email = email
                    )
                )

                if existing_user is not None:
                    raise EmailAlreadyExists()

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

    async def delete_user(
            self,
            user: User
    ) -> AdminUserDeleteResponse:

        is_deleted: bool = await self.user_repository.delete(
            user_uid=user.user_uid
        )

        if not is_deleted:
            raise UserNotFound()

        try:
            await self.user_repository.commit()

        except SQLAlchemyError:
            await self.user_repository.rollback()
            raise

        return AdminUserDeleteResponse(
            status = True
        )  

    async def deactivate_user():
        pass

    async def deactivate_user():
        pass

    async def reset_user_password(
                self,
                *,
                password_data: AdminUserPasswordResetRequest,
                user_uid: UUID
    ) -> AdminUserPasswordResetResponse:
            
            user = await self.user_repository.get_by_uid(
                user_uid=user_uid
            )
    
            if user is None:
                raise UserNotFound()
    
            user.password_hash = generate_hash_password(
                password = password_data.new_password.get_secret_value()
            )
    
            # await self.user_repository.update(
            #     user=user
            # )
    
            try:
                await self.user_repository.commit()
    
            except SQLAlchemyError:
                await self.user_repository.rollback()
                raise
    
            # 7. Return resulting roles
            return AdminUserPasswordResetResponse(
                status=True,
            )

