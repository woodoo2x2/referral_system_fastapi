from dataclasses import dataclass
from datetime import datetime, timedelta

from jose import jwt
from pydantic import EmailStr

from auth.exceptions import PasswordIsIncorrectException
from auth.utils import Security
from settings import Settings
from users.exceptions import UserWithThisEmailNotExistException
from users.repository import UserRepository
from users.schemas import LoginUserRequestSchema


@dataclass
class AuthService:
    user_repository: UserRepository
    security: Security
    settings: Settings

    async def login(self, data: LoginUserRequestSchema):
        user = await self.user_repository.get_user_by_email(data.email)
        if not user:
            raise UserWithThisEmailNotExistException(data.email)
        if not self.security.verify_password(data.password, user.password):
            raise PasswordIsIncorrectException()
        access_token = self.generate_access_token(data.email)

    def generate_access_token(self,email: EmailStr) -> str:
        expire_time_unix = (datetime.utcnow() + timedelta(minutes=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp()
        token = jwt.encode(
            {"email": email, "expire": expire_time_unix},
            self.settings.JWT_SECRET_KEY,
            algorithm=self.settings.JWT_DECODE_ALGORITHM,
        )
        return token

