 #$ this is for pydantic data validation stuff. pydantic is love man <3

from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email : EmailStr

class UserUpdate(BaseModel):
    email : EmailStr | None = None
    username : str | None = None
    password : str | None = None
