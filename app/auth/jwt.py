import jwt
import datetime

from datetime import datetime, timedelta, timezone
from app.settings import Settings
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request


config = Settings()
security = HTTPBearer()

def create_access_token(username:str, id:str):
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    stuff = {
        "sub": username,
        "id": id,
        "exp": expire
    }
    token = jwt.encode(stuff, config.JWT_SECRET, algorithm="HS256")
    return token


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, config.JWT_SECRET, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = decode_access_token(token)
    return payload

def get_user_from_session(request : Request):
    user = request.session.get('user')
    if not user:
        return HTTPException(status_code=401, detail="Not Authenticiated!")
    return user

