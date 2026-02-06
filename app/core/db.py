from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.models.session import Base

# create async engine
engine = create_async_engine(settings.database_url, echo=False, future=True)

# create async sessionmaker
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

# create database tables if they do not exist.
async def init_models() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# use sessionmaker to get session
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
