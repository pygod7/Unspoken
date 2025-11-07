from fastapi import APIRouter
from app.database.schemas import UserCreate
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.database.conn import get_database
from app.database.crud import create_user
router = APIRouter(prefix="/api/user", tags=["UserCRUD"])



@router.post("/create")
async def create_user(user_data = UserCreate, db: AsyncSession=Depends(get_database)):
    new_user = await create_user(db=db, user_data=user_data)
    return {
        "id" : new_user.id,
        "username": new_user.username,
        "email" : new_user.email
    }

    


        