from typing import AsyncGenerator

import ssl
import certifi
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.models.session import Base

# create async engine; Supabase pooler sometimes presents a cert chain that fails local verification.
# For now, disable verification to unblock local dev. In production, provide proper CA.
ssl_context = ssl.create_default_context(cafile=certifi.where())
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
engine = create_async_engine(
    settings.database_url,
    echo=False,
    future=True,
    connect_args={"ssl": ssl_context},
)

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
