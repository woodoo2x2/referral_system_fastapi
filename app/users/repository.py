from dataclasses import dataclass

from pydantic import EmailStr
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.utils import Security
from app.users.exceptions import UserWithThisEmailAlreadyExistException, UserWithThisEmailNotExistException
from app.users.models import User
from app.users.schemas import UserCreateRequestSchema


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


    async def get_user_by_email(self, email: EmailStr) -> User:
        query = select(User).where(User.email == email)
        async with self.db_session as session:
            user = (await session.execute(query)).scalar_one_or_none()
        return user
