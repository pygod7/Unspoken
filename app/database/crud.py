import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.models import User #$ DB Model
from app.database.schemas import UserCreate #$ PYDANTIC

#$ create user.

async def create_user(db: AsyncSession, user_data: UserCreate):
    