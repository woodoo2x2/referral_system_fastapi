from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.auth.handlers import router as auth_router
from app.settings import Settings

app = FastAPI()
settings = Settings()
app.include_router(auth_router)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SESSION_SECRET_KEY,
    session_cookie="session",
)