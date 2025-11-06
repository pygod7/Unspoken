#$%

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.settings import Settings

config = Settings()

engine = create_async_engine(config.DATABASE_URL, echo=True)

async_session = sessionmaker(
    bind = engine,
    class_=AsyncSession,
    expire_on_commit=False #$ still stores data after user comits !!

)

#$ for fastapi easyness.

async def get_database():
    async with async_session as session:
        yield session
