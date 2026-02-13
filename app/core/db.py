from typing import AsyncGenerator

import ssl
import certifi
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.models.session import Base


# Supabase pooler-friendly engine
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


# create async engine with SSL required using system CA bundle
engine = create_async_engine(
      settings.database_url,
      echo=False,
      future=True,
      pool_pre_ping=True,
      pool_recycle=1800,
      connect_args={"ssl": ssl_context, "statement_cache_size": 0},
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
