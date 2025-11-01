import fastapi

from fastapi import FastAPI
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates



router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)
templates = Jinja2Templates(directory="app/templates")


@router.get("/login")
async def login_page(request : Request):
    return templates.TemplateResponse('login.html',{'request':request})