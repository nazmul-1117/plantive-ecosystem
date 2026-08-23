
# app/repositories/plant_category_repository.py

from uuid import UUID

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, exists, delete, or_, func
from sqlalchemy.orm import selectinload, joinedload

from app.models.plant_category import PlantCategory


class PlantCategoryRepository:

    def __init__(
            self,
            session: AsyncSession
    ):
        self.session = session

    async def list_categories(
            self,
            *,
            search: str | None = None,
            is_active: bool | None = None,

            offset: int = 0,
            limit: int = 20,
    ) -> tuple[list[PlantCategory], int]:
        
        statement = select(PlantCategory)

        statement = self._apply_filters(
            statement=statement,
            search=search,
            is_active=is_active,
        )

        count_statement = (
            select(func.count())
            .select_from(statement.subquery())
        )

        count_result = await self.session.exec(count_statement)
        total = count_result.one()

        statement = (
            statement
            .order_by(
                PlantCategory.created_at.desc(),
                PlantCategory.plant_category_uid,
            )
            .offset(offset)
            .limit(limit)
        )

        result = await self.session.exec(statement)
        return result.all(), total

    async def get_by_uids(
            self,
            *,
            plant_category_uuids: list[UUID]
    ) -> list[PlantCategory]:
        
        if not plant_category_uuids:
            return []
        
        statement = (
            select(PlantCategory)
            .where(
                PlantCategory.plant_category_uid.in_(plant_category_uuids)
            )
        )

        result = await self.session.exec(statement)

        return result.all()


    def _apply_filters(
        self,
        statement,
        *,
        search: str | None,
        is_active: bool | None,
    ):
        if search:
            search = search.strip()
            
            search_pattern = f"%{search}%"

            statement = statement.where(
                or_(
                    PlantCategory.name.ilike(search_pattern),
                    PlantCategory.slug.ilike(search_pattern),
                )
            )

        if is_active is not None:
            statement = statement.where(
                PlantCategory.is_active == is_active
            )

        return statement