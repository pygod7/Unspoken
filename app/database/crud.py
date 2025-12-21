import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.models import User #$ DB Model
from app.database.schemas import UserCreate, UserUpdate #$ PYDANTIC
from app.database.helper import generate_password, generate_username, generate_uuid #$ helper func
from sqlalchemy import delete, update


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


async def delete_user(db: AsyncSession, user_id: str):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        return {"status": "error", "message": "User not found"}
    await db.execute(delete(User).where(User.id == user_id))
    await db.commit()
    return user


async def update_user(db: AsyncSession, user_id, user_data:UserUpdate):
    foo = user_data.model_dump(exclude_unset=True)
    if not foo:
        return{
            "status": "Error", "message": "No fields given for updating."
        }
    query = update(User).where(User.id==user_id).values(**foo).execution_options(synchronize_session="fetch") #we could use () for making breaking lines and do clearly but i like do do in same line :)
    await db.execute(query)
    await db.commit()
    updated_user = await db.get(User, user_id)
    return updated_user
    


    