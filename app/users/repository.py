from dataclasses import dataclass
from datetime import datetime

from pydantic import EmailStr
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.utils import Security
from app.referral.exceptions import ReferralCodeForThisUserAlreadyExist, ReferralCodeNotExistException, \
    ReferralCodeExpiresException
from app.users.models import User
from app.users.schemas import UserCreateRequestSchema


@dataclass
class ReferralCodeAlreadyExistsException(Exception):
    referral_code: str


@dataclass
class UserRepository:
    db_session: AsyncSession
    security: Security

    async def create_user(self, data: UserCreateRequestSchema) -> User:
        query = insert(User).values(
            username=data.username,
            email=data.email,
            password=self.security.hash_password(data.password)
        ).returning(User)

        async with self.db_session as session:
            new_user = (await session.execute(query)).scalar()
            await session.commit()

        return new_user

    async def get_user_by_email(self, email: EmailStr | str) -> User:
        query = select(User).where(User.email == email)
        async with self.db_session as session:
            user = (await session.execute(query)).scalar_one_or_none()
        return user

    async def create_referral_code_for_user(self,
                                            user_email: str,
                                            referral_code: str,
                                            expires_at: datetime):
        user = await self.get_user_by_email(user_email)
        if user.referral_code:
            raise ReferralCodeForThisUserAlreadyExist(user_id=user.id)
        query = update(User).where(User.email == user_email).values(
            referral_code=referral_code,
            referral_code_expires_at=expires_at
        )
        async with self.db_session as session:
            await session.execute(query)
            await session.commit()

        updated_user = await self.db_session.execute(
            select(User).where(User.email == user_email)
        )
        return updated_user.scalar()

    async def get_user_referral_code(self, user_email: str):
        user: User = await self.get_user_by_email(user_email)

        if not user.referral_code:
            raise ReferralCodeNotExistException()

        if user.referral_code_expires_at < datetime.utcnow():
            raise ReferralCodeExpiresException(user.email)
        return user.referral_code

    async def delete_user_referral_code(self, user_email: str):
        query = update(User).where(User.email == user_email).values(
            referral_code=None,
            referral_code_expires_at = None
        )
        async with self.db_session as session:
            await session.execute(query)
            await session.commit()
