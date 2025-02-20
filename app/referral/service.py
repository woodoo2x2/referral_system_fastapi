import random
import string
from dataclasses import dataclass
from datetime import datetime, timedelta

from app.referral.exceptions import (
    DeleteNotExistedReferralCodeException,
    UserWithThatIDNotExistException,
    ReferralCodeExpiresException,
    ReferralCodeNotExistException,
)
from app.users.models import User
from app.users.repository import UserRepository
from app.users.schemas import UserResponseSchema, AllUserReferralsResponseSchema
from app.cache.service import RedisService
from app.settings import Settings


@dataclass
class ReferralService:
    user_repository: UserRepository
    redis_service: RedisService
    settings: Settings

    @staticmethod
    def generate_referral_code() -> str:
        return "".join(random.choices(string.ascii_letters + string.digits, k=8))

    async def create_referral_code(
        self, user_email: str, lifetime_minutes: int
    ) -> User:
        expires_at = datetime.utcnow() + timedelta(minutes=lifetime_minutes)

        referral_code = self.generate_referral_code()
        user: User = await self.user_repository.create_referral_code_for_user(
            user_email, referral_code, expires_at
        )
        cache_key = f"referral_code:{user_email}"

        await self.redis_service.set(
            cache_key,
            {
                "referral_code": user.referral_code,
                "referral_code_expires_at": user.referral_code_expires_at.isoformat(),
            },
            expire=self.settings.REDIS_EXPIRE_CACHE_SECONDS,
        )

        return user

    async def get_referral_code(self, user_email: str) -> str:
        cache_key = f"referral_code:{user_email}"

        cached_data = await self.redis_service.get(cache_key)

        if cached_data:
            referral_code = cached_data["referral_code"]
            expires_at = cached_data["referral_code_expires_at"]

            if datetime.fromisoformat(expires_at) > datetime.utcnow():
                return referral_code
            else:
                await self.redis_service.delete(cache_key)
                raise ReferralCodeExpiresException(user_email)

        user: User = await self.user_repository.get_user_by_email(user_email)
        if not user.referral_code:
            raise ReferralCodeNotExistException(user_email)
        if (
            not user.referral_code_expires_at
            or user.referral_code_expires_at < datetime.utcnow()
        ):
            raise ReferralCodeExpiresException(user.email)

        await self.redis_service.set(
            cache_key,
            {
                "referral_code": user.referral_code,
                "referral_code_expires_at": user.referral_code_expires_at.isoformat(),
            },
            expire=self.settings.REDIS_EXPIRE_CACHE_SECONDS,
        )
        return user.referral_code

    async def delete_referral_code(self, user_email: str) -> str:
        referral_code = await self.user_repository.get_referral_code_by_user_email(
            user_email
        )

        if not referral_code:
            raise DeleteNotExistedReferralCodeException()
        await self.user_repository.delete_user_referral_code(user_email)

        cache_key = f"referral_code:{user_email}"
        await self.redis_service.delete(cache_key)

        return referral_code

    async def get_all_invited_users_by_referral_id(
        self, user_id: int
    ) -> AllUserReferralsResponseSchema:
        referral = await self.user_repository.get_user_by_user_id(user_id)
        if not referral:
            raise UserWithThatIDNotExistException(user_id)
        users = await self.user_repository.get_all_invited_users_by_referral_id(user_id)

        return AllUserReferralsResponseSchema(
            referrer_id=referral.id,
            referrer_email=referral.email,
            referred_users=[UserResponseSchema.from_user(user) for user in users],
        )
