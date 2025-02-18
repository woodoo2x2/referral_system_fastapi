from pydantic import BaseModel


class ReferralCodeResponseSchema(BaseModel):
    referral_code: str
