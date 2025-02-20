from fastapi import FastAPI, Depends
from pydantic import BaseModel, EmailStr
from starlette.middleware.sessions import SessionMiddleware

from app.api.service import HunterApiService
from app.auth.handlers import router as auth_router
from app.dependency import get_hunter_api_service
from app.referral.handlers import router as referral_router
from app.settings import Settings

app = FastAPI()
settings = Settings()
app.include_router(auth_router)
app.include_router(referral_router)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SESSION_SECRET_KEY,
    session_cookie="session",
)


class EmailCheckSchema(BaseModel):
    email: EmailStr


@app.post("/test_api")
async def check_api(
    data: EmailCheckSchema,
    hunter_api_service: HunterApiService = Depends(get_hunter_api_service),
):
    response = await hunter_api_service.verify_email(data.email)
    return response
