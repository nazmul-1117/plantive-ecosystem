from collections.abc import AsyncGenerator
from sqlmodel import text, SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from .config import settings
from sqlmodel.ext.asyncio.session import AsyncSession


engine = create_async_engine(
    url=settings.DATABASE_URL
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# initialized database
async def init_db():
    async with engine.begin() as conn:
        from app.models.plant_model import Plants
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
