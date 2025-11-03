import fastapi
import authlib
import httpx

from fastapi import FastAPI
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from authlib.integrations.starlette_client import OAuth
from app.settings import Settings
from authlib.integrations.base_client.errors import MismatchingStateError


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
    client_kwargs={"scope": "public_repo"},
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
async def login_via_discord(request: Request):
    try:    

        token = await oauth.discord.authorize_access_token(request)
        print(token)
        user = await oauth.discord.get("users/@me", token=token)
        user_info = user.json()
        return user_info
    except MismatchingStateError:
        return "CSRF Verification Failed! Please login using the web LoginViaDiscord Button!"


@router.get("/login/github")
async def login_github(request: Request):
    redirect_uri = request.url_for("github_callback")  # Discord callback URL
    return await oauth.github.authorize_redirect(request, redirect_uri)


@router.get("/github/callback", name="github_callback")
async def github_callback(request: Request):
    try:
        # exchange code for access token
        token = await oauth.github.authorize_access_token(request)

        # fetch user info
        user = await oauth.github.get("user", token=token)
        user_info = user.json()

        # store token and user info in session
        request.session["token"] = token
        request.session["user"] = {"login": user_info.get("login"), "id": user_info.get("id")}

        # --- Automatically star repo ---
        access_token = token.get("access_token")
        return user_info

    except MismatchingStateError:
        return "CSRF Verification Failed! Please login using the GitHub login button!"