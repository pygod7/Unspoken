try:
    from fastapi import FastAPI
    from app.routes.login import router
    from starlette.middleware.sessions import SessionMiddleware

    app = FastAPI()

    @app.get("/")
    async def root():
        return {"message": "Hello from FastAPI on Vercel!"}

    app.include_router(router)
    app.add_middleware(SessionMiddleware, secret_key="nothing-here-lol-its-for-just-using-authlib-testing")

except Exception as e:
    print("Startup error:", e)
    raise e
