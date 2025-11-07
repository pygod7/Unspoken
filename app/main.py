import traceback

try:
    from fastapi import FastAPI
except Exception:
    print("Failed to import FastAPI")
    traceback.print_exc()
    raise

try:
    from starlette.middleware.sessions import SessionMiddleware
except Exception:
    print("Failed to import SessionMiddleware")
    traceback.print_exc()
    raise

try:
    from app.routes.login import router
except Exception:
    print("Failed to import router from login.py")
    traceback.print_exc()
    raise

app = FastAPI()

try:
    app.include_router(router)
except Exception:
    print("Failed to include router")
    traceback.print_exc()
    raise

try:
    app.add_middleware(SessionMiddleware, secret_key="testing-secret")
except Exception:
    print("Failed to add SessionMiddleware")
    traceback.print_exc()
    raise

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI on Vercel!"}
