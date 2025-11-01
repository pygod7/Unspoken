#$ main entrypoint!

from fastapi import FastAPI
from app.routes.login import router

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI on Vercel!"}

app.include_router(router)
