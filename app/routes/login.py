import fastapi
import authlib
import httpx

from fastapi import FastAPI
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from authlib.integrations.starlette_client import OAuth
from app.settings import Settings
from authlib.integrations.base_client.errors import MismatchingStateError
from app.database.crud import create_user
from app.database.helper import get_user_by_email
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends,HTTPException
from app.database.conn import get_database
from app.database.schemas import UserCreate

config = Settings()
oauth = OAuth()

oauth.register(
    name='discord',
    client_id=config.DISCORD_CLIENT_ID,
    client_secret=config.DISCORD_CLIENT_SECRET,
    access_token_url='https://canary.discord.com/api/oauth2/token',      # token exchange URL
    authorize_url='https://discord.com/api/oauth2/authorize',             # where user logs in
    api_base_url='https://discord.com/api/',                               # base for API calls
    client_kwargs={'scope': 'identify email'}                              # requested permissions
)


oauth.register(
    name="github",
    client_id=config.GITHUB_CLIENT_ID,
    client_secret=config.GITHUB_CLIENT_SECRET,
    access_token_url="https://github.com/login/oauth/access_token",
    authorize_url="https://github.com/login/oauth/authorize",
    api_base_url="https://api.github.com/",
    client_kwargs={"scope": "public_repo user:email"},
)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)
templates = Jinja2Templates(directory="app/templates")


@router.get("/login/discord")
async def login_discord(request: Request):
    redirect_uri = request.url_for("discord_callback")  # Discord callback URL
    return await oauth.discord.authorize_redirect(request, redirect_uri)

@router.get("/login")
async def login_page(request : Request):
    return templates.TemplateResponse('login.html',{'request':request})

@router.get("/discord/callback", name="discord_callback")
async def login_via_discord(request: Request, db:AsyncSession=Depends(get_database)):
    try:    
        token = await oauth.discord.authorize_access_token(request)
        print(token)
        user = await oauth.discord.get("users/@me", token=token)
        user_info = user.json()
        email = user_info.get('email')
        existing_user = await get_user_by_email(db, email=email)
        if existing_user:
            return {
                "message": "User exists already!",
                "id": existing_user.id,
                "email": existing_user.email,
                "username": existing_user.username
            }
        
        #$ create new if doesnt exist.
        user_data = UserCreate(email=email)
        new_user = await create_user(db, user_data=user_data)
        return{
            "message" : "User created successfully!",
            "id" : new_user.id,
            "email": new_user.email,
            "username": new_user.username
        }
    except MismatchingStateError:
        return "CSRF Verification Failed! Please login using the web LoginViaDiscord Button!"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/login/github")
async def login_github(request: Request):
    redirect_uri = request.url_for("github_callback")  # Discord callback URL
    return await oauth.github.authorize_redirect(request, redirect_uri)


@router.get("/github/callback", name="github_callback")
async def github_callback(request: Request, db:AsyncSession=Depends(get_database)):
    try:
        token = await oauth.github.authorize_access_token(request)
        user = await oauth.github.get("user", token=token)
        user_info = user.json()
        email_response = await oauth.github.get("user/emails", token=token)
        emails = email_response.json()
        email = emails[0]['email']
        existing_user = await get_user_by_email(db, email=email)
        if existing_user:
            return {
                "message": "User exists already!",
                "id": existing_user.id,
                "email": existing_user.email,
                "username": existing_user.username
            }
        
        #$ create new if doesnt exist.
        user_data = UserCreate(email=email)
        new_user = await create_user(db, user_data=user_data)
        return{
            "message" : "User created successfully!",
            "id" : new_user.id,
            "email": new_user.email,
            "username": new_user.username
        }
    except MismatchingStateError:
        return "CSRF Verification Failed! Please login using the web LoginViaGithub Button!"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))