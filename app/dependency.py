from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.utils import Security
from app.database.session import get_db_session
from app.users.repository import UserRepository
from app.auth.service import AuthService
from app.settings import Settings


def get_app_security() -> Security:
    return Security()


def get_user_repository(session: AsyncSession = Depends(get_db_session),
                        security: Security = Depends(get_app_security)
                        ) -> UserRepository:
    return UserRepository(db_session=session, security=security)


def get_auth_service(
        user_repository: UserRepository = Depends(get_user_repository),
        security: Security = Depends(get_app_security),
) -> AuthService:
    return AuthService(user_repository=user_repository,
                       security=security,
                       settings=Settings())
