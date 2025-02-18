import random
import string
from dataclasses import dataclass

from app.users.models import User
from app.users.repository import UserRepository


@dataclass
class ReferralService:
    user_repository: UserRepository

    def generate_referral_code(self) -> str:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    async def create_referral_code(self, user_email:str):
        referral_code = self.generate_referral_code()
        user = await self.user_repository.create_referral_code_for_user(user_email, referral_code)
        return user

    async def delete_referral_code(self, user: User):
        if not user.referral_code:
            raise ValueError("У вас нет активного реферального кода")

        user.referral_code = None
        await self.db.commit()
