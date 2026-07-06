
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from app.config.database import get_session

from app.schemas.auth_schema import UserCreate, UserRead, UserUpdate, LoginRequest
from app.services.auth_service import UserService
from app.config.security import verity_hashed_password
from app.models.auth import User
from app.config.jwt import create_token, decode_token

user_service = UserService()

async def create_user(
        user_data: UserCreate,
        session: AsyncSession = Depends(get_session)
):
    exist_user: User | None = await user_service.get_by_email_or_username(
        session=session,
        email=user_data.email,
        username=user_data.username
    )

    if exist_user is None:
        user: User | None = await user_service.create_user(user_data, session)

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

async def login_user(
        login_data: LoginRequest,
        session: AsyncSession = Depends(get_session)
    ):
    
    user: User | None = await user_service.get_by_email_or_username(
        session=session,
        email="hey",
        username=login_data.username
    )

    if user is None or not verity_hashed_password(
        password=login_data.password,
        hashed_password=user.password_hashed
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    access_token = create_token(
        user_uid= str(user.user_uid)
    )

    refresh_token = create_token(
        user_uid= str(user.user_uid),
        token_type="refresh"
    )

    return JSONResponse(
        content={
            "message": "login successfull :)",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": {
                "user_uid": str(user.user_uid),
                "username": user.username,
                "email": user.email
            }
        }
    )
    