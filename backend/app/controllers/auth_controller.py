
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends, HTTPException, status
from app.config.database import get_session

from app.schemas.auth_schema import UserCreate, UserRead, UserUpdate
from app.services.auth_service import UserService

user_service = UserService()

async def create_user(
        user_data: UserCreate,
        session: AsyncSession = Depends(get_session)
):
    exist_user = await user_service.get_by_email_or_username(
        session=session,
        email=user_data.email,
        username=user_data.username
    )

    if exist_user is None:
        user = await user_service.create_user(user_data, session)

        if user is not None:
            return {
                "status": status.HTTP_201_CREATED,
                "details": "User created successfully",
                "data": user
            }

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="username or email already exist"
    )