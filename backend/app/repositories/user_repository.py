
from uuid import UUID

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, exists, delete, or_, func
from sqlalchemy.orm import selectinload

from app.models.auth_model import User, UserRole, Role

class UserRepository:

    def __init__(
            self,
            session: AsyncSession
    ):
        self.session = session
        
    async def create(
            self,
            user: User,
    ) -> User:
        
        self.session.add(user)
        await self.session.flush()

        return user

    async def delete(
            self,
            user_uid: UUID
    ) -> bool:
        
        statement = delete(User).where(User.user_uid == user_uid)
        result = await self.session.exec(statement)

        return result.rowcount > 0

    async def update(
            self,
            user: User
    ) -> User | None:
        
        self.session.add(user)
        await self.session.flush()

        return user
    
    async def get_by_uid(
            self,
            user_uid: UUID,
    ) -> User | None:
        
        statement = (
            select(User)
            .options(
                selectinload(User.roles)
            )
            .where(
                User.user_uid == user_uid
            )
        )
        result = await self.session.exec(statement)
        return result.first()

    async def get_by_email(
            self,
            email: str,
    ) -> User | None:
        
        statement = select(User).where(User.email == email)
        result = await self.session.exec(statement)
        return result.first()

    async def get_by_username(
            self,
            username: str,
    ) -> User | None:
        
        statement = select(User).where(User.username == username)
        result = await self.session.exec(statement)
        return result.first()

    async def exists_by_email(
            self,
            email: str,
    ) -> bool:
        
        statement = select(
            exists().
            where(User.email == email)
        )
        result = await self.session.exec(statement)

        return result.one()

    async def exists_by_username(
            self,
            username: str,
    ) -> bool:
        
        statement = select(
            exists().
            where(User.username == username)
        )
        
        result = await self.session.exec(statement)
        return result.one()

    async def get_by_email_username():
        pass

    async def get_users(
                self,
                *,
                search: str | None = None,
                is_active: bool | None = None,
                is_verified: bool | None = None,
                role: str | None = None,
                offset: int = 0,
                limit: int = 20,
    ) -> tuple[list[User], int]:

        filters = []

        if search:
            search_pattern = f"%{search}%"

            filters.append(
                or_(
                    User.first_name.ilike(search_pattern),
                    User.last_name.ilike(search_pattern),
                    User.username.ilike(search_pattern),
                    User.email.ilike(search_pattern),
                )
            )

        if is_active is not None:
            filters.append(
                User.is_active == is_active
            )

        if is_verified is not None:
            filters.append(
                User.is_verified == is_verified
            )

        if role:
            role_exists = exists(
                select(1)
                .select_from(UserRole)
                .join(
                    Role,
                    Role.role_uid == UserRole.role_uid,
                )
                .where(
                    UserRole.user_uid == User.user_uid,
                    Role.name == role,
                )
            )

            filters.append(role_exists)


        # count
        count_statement = (
            select(func.count(User.user_uid))
            .select_from(User)
            .where(*filters)
        )

        count_result = await self.session.exec(count_statement)

        total = count_result.one()

        # Users
        statement = (
            select(User)
            .options(
                selectinload(User.roles)
            )
            .where(*filters)
            .order_by(User.created_at.desc())
            .offset(offset)
            .limit(limit)
        )

        result = await self.session.exec(statement)

        users = result.all()

        return users, total

        
    async def commit(self) -> None:
        await self.session.commit()
    
    async def rollback(self) -> None:
        await self.session.rollback()
    
    async def refresh(self, obj) -> None:
        await self.session.refresh(obj)

