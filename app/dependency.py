from fastapi import Depends, security, Security
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.exceptions import HTTPException

from app.auth.service import AuthService

from app.database.session import get_db_session
from app.exceptions import ApplicationException
from app.referral.service import ReferralService
from app.settings import Settings
from app.users.repository import UserRepository
from app.auth.utils import SecurityConfig

reusable_oauth2 = security.HTTPBearer()


def get_app_security() -> SecurityConfig:
    return SecurityConfig()


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


def get_referral_service(
        user_repository: UserRepository = Depends(get_user_repository),
):
    return ReferralService(user_repository=user_repository)


async def get_current_user_email(
        token: security.http.HTTPAuthorizationCredentials = Security(reusable_oauth2),
        # Получаем токен из заголовка Authorization
        auth_service: AuthService = Depends(get_auth_service)
) -> str:
    try:

        user_email = await auth_service.get_current_user_email(token.credentials)
        return user_email
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})