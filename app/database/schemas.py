 #$ this is for pydantic data validation stuff. pydantic is love man <3

from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email : EmailStr