from dataclasses import dataclass
from datetime import datetime

from pydantic import EmailStr
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.utils import SecurityConfig
from app.referral.exceptions import ReferralCodeForThisUserAlreadyExist, ReferralCodeNotExistException, \
    ReferralCodeExpiresException
from app.users.models import User
from app.users.schemas import UserCreateRequestSchema, RegistrationAsReferralRequestSchema


@dataclass
class UserRepository:
    db_session: AsyncSession
    security: SecurityConfig

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
    async def get_user_by_user_id(self, user_id:int):
        query = select(User).where(User.id == user_id)
        async with self.db_session as session:
            user = (await session.execute(query)).scalar_one_or_none()
        return user
    async def create_referral_code_for_user(self,
                                            user_email: str,
                                            referral_code: str,
                                            expires_at: datetime):
        user = await self.get_user_by_email(user_email)
        if user.referral_code:
            raise ReferralCodeForThisUserAlreadyExist(user_email)
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

    async def check_referral_code_expired(self, user_email: str):
        user: User = await self.get_user_by_email(user_email)

        if not user.referral_code:
            raise ReferralCodeNotExistException(user.email)

        if not user.referral_code_expires_at or user.referral_code_expires_at < datetime.utcnow():
            raise ReferralCodeExpiresException(user.email)
        return user.referral_code

    async def get_referral_code_by_user_email(self, user_email: str):
        return await self.check_referral_code_expired(user_email)

    async def delete_user_referral_code(self, user_email: str):
        query = update(User).where(User.email == user_email).values(
            referral_code=None,
            referral_code_expires_at=None
        )
        async with self.db_session as session:
            await session.execute(query)
            await session.commit()

    async def get_user_by_referral_code(self, referral_code: str) -> User | None:
        query = select(User).where(User.referral_code == referral_code)
        async with self.db_session as session:
            user = (await session.execute(query)).scalar_one_or_none()
        return user

    async def create_user_as_referral(self, data: RegistrationAsReferralRequestSchema, inviter_user_id: int):
        query = insert(User).values(
            username=data.username,
            email=data.email,
            password=self.security.hash_password(data.password),
            inviter_id=inviter_user_id,
        ).returning(User)
        async with self.db_session as session:
            new_user = (await session.execute(query)).scalar()
            await session.commit()

        return new_user

    async def get_all_invited_users_by_referral_id(self, user_id: int):
        query = select(User).where(User.inviter_id == user_id)
        async with self.db_session as session:
            result = await session.execute(query)
            users = result.scalars().all()
        return users

