import asyncio
import os

import pytest
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core import db as db_module
from app.core.config import settings
from app.core.db import ssl_context as app_ssl_context
from app.models.session import Base
from main import app


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_engine():
    db_url = os.getenv("TEST_DATABASE_URL", settings.database_url)

    engine = create_async_engine(
        db_url,
        echo=False,
        future=True,
        pool_pre_ping=True,
        pool_recycle=1800,
        connect_args={"ssl": app_ssl_context, "statement_cache_size": 0},
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    await engine.dispose()


@pytest.fixture(scope="session")
async def SessionLocal(test_engine):
    return async_sessionmaker(test_engine, expire_on_commit=False)


@pytest.fixture()
async def db_session(SessionLocal):
    async with SessionLocal() as session:
        yield session
        await session.execute(text("TRUNCATE TABLE sessions"))
        await session.commit()


@pytest.fixture()
async def client(db_session):
    async def _get_test_db():
        yield db_session

    app.dependency_overrides[db_module.get_db_session] = _get_test_db

    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac

    app.dependency_overrides.clear()
