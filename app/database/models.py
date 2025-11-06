import uuid
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from datetime import datetime
from sqlalchemy import text
from sqlalchemy import func

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True),
                primary_key=True,
                default=uuid.uuid4,
                unique=True,
                nullable=False)
    email = Column(String,unique=True,index=True,nullable=False) #$ index = fast lookup
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    profile_pic = Column(String, nullable=True)
    is_active = Column(Boolean, server_default=text('true')) #$ this is db side so postgres neeeds 'true' not True as its not python boolean. so we are passing RAW sql. ##$
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())  
    role = Column(String, server_default="user")


    
