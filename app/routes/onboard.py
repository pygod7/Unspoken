from fastapi import FastAPI, APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter()

templates = Jinja2Templates(directory="app/templates") 

@router.get("/onboard", response_class=HTMLResponse)
async def onboarding_data(request: Request):
    return templates.TemplateResponse("onboard.html", {"request": request})
