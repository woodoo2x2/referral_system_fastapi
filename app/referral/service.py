import random
import string
from dataclasses import dataclass
from datetime import datetime, timedelta

from app.referral.exceptions import DeleteNotExistedReferralCodeException
from app.users.models import User
from app.users.repository import UserRepository


@dataclass
class ReferralService:
    user_repository: UserRepository

    @staticmethod
    def generate_referral_code() -> str:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    async def create_referral_code(self, user_email: str, lifetime_minutes: int):
        expires_at = datetime.utcnow() + timedelta(minutes=lifetime_minutes)

        referral_code = self.generate_referral_code()
        user: User = await self.user_repository.create_referral_code_for_user(user_email, referral_code, expires_at)
        return user

    async def get_referral_code(self, user_email: str):
        return await self.user_repository.check_referral_code_expired(user_email)

    async def delete_referral_code(self, user_email: str):
        referral_code = await self.user_repository.get_referral_code_by_user_email(user_email)

        if not referral_code:
            raise DeleteNotExistedReferralCodeException()
        await self.user_repository.delete_user_referral_code(user_email)
        return referral_code
