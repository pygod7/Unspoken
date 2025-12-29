from fastapi import FastAPI, APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter()

templates = Jinja2Templates(directory="app/templates") 

@router.get("/onboard", response_class=HTMLResponse)
async def onboarding_data(request: Request):
    return templates.TemplateResponse("onboard.html", {"request": request})

@router.get("/", response_class=HTMLResponse)
async def index_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})