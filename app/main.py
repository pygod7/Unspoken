try:
    from fastapi import FastAPI
except Exception as e:
    print("FastAPI import failed:", e)
    raise e

try:
    from app.routes.login import router
except Exception as e:
    print("Router import failed:", e)
    raise e

try:
    from starlette.middleware.sessions import SessionMiddleware
except Exception as e:
    print("SessionMiddleware import failed:", e)
    raise e

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI on Vercel!"}

try:
    app.include_router(router)
except Exception as e:
    print("Failed to include router:", e)
    raise e

try:
    app.add_middleware(SessionMiddleware, secret_key="testing-secret")
except Exception as e:
    print("Failed to add middleware:", e)
    raise e
#testing fail