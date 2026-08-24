
# ========================================================================================
#                  app/repositories/plant_category_repository.py -> PUBLIC + ADMIN
# ========================================================================================

from uuid import UUID

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, or_, func

from app.models.plant_category import PlantCategory


class PlantCategoryRepository:

    def __init__(
            self,
            session: AsyncSession
    ):
        self.session = session

    async def create(
            self,
            *,
            plant_category: PlantCategory
    ) -> PlantCategory:

        self.session.add(plant_category)
        await self.session.flush()

        return plant_category

    async def update(
            self,
            plant_category: PlantCategory
    ) -> PlantCategory:
        
        # self.session.add(plant_category)
        await self.session.flush()

        return plant_category
        
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

    async def get_by_uid(
            self,
            *,
            plant_category_uid: UUID,
    ) -> PlantCategory | None:

        statement = (
            select(PlantCategory)
            .where(
                PlantCategory.plant_category_uid == plant_category_uid,
            )
        )

        result = await self.session.exec(statement)

        return result.one_or_none()

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

    async def get_by_name(
        self,
        *,
        name: str
    ) -> PlantCategory | None:

        statement = (
            select(PlantCategory)
            .where(
                func.lower(PlantCategory.name) == name.lower()
            )
        )

        result = await self.session.exec(statement)

        return result.one_or_none()

    async def get_by_conflicting_category(
        self,
        *,
        name: str,
        slug: str,
        exclude_uid: UUID,
    ) -> PlantCategory | None:

        statement = (
            select(PlantCategory)
            .where(
                PlantCategory.plant_category_uid != exclude_uid,
                or_(
                    func.lower(PlantCategory.name) == name.lower(),
                    func.lower(PlantCategory.slug) == slug,
                ),
            )
            .limit(1)
        )

        result = await self.session.exec(statement)

        return result.one_or_none()

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





    async def commit(self) -> None:
        await self.session.commit()
    
    async def rollback(self) -> None:
        await self.session.rollback()
    
    async def refresh(self, obj) -> None:
        await self.session.refresh(obj)