import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.models import User #$ DB Model
from app.database.schemas import UserCreate #$ PYDANTIC
from app.database.helper import generate_password, generate_username, generate_uuid #$ helper func

#$ create user.

async def create_user(db: AsyncSession, user_data: UserCreate):
    email = user_data.email
    username = await generate_username(db)
    password = generate_password()
    user_id = generate_uuid()
    new_user = User(
        id = user_id,
        username=username,
        password=password,
        email = email
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

    