from typing import Optional

from pydantic import BaseModel, Field, EmailStr

from app.settings import Settings

settings = Settings()


class ReferralCodeResponseSchema(BaseModel):
    referral_code: str | None


class CreateReferralCodeRequestSchema(BaseModel):
    lifetime_minutes: Optional[int] = Field(
        default=settings.REFERRAL_CODE_DEFAULT_LIFETIME_MINUTES,
        ge=1,
        description="Lifetime of referral code",
    )


class GetReferralCodeByEmailRequestSchema(BaseModel):
    email: EmailStr
