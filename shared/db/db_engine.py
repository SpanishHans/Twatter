from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
import os

from shared.models.base import Base

DATABASE = os.getenv("DATABASE_URL",'postgresql+asyncpg://${DB_USER}:${DB_PASS}@db:5432/${DB_NAME}')

engine = create_async_engine(DATABASE, echo=True)

SessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
