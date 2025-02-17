from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.utils import Security
from app.database.session import get_db_session
from app.users.repository import UserRepository


def get_app_security() -> Security:
    return Security()


def get_user_repository(session: AsyncSession = Depends(get_db_session),
                        security: Security = Depends(get_app_security)
                        ) -> UserRepository:
    return UserRepository(db_session=session, security=security)
