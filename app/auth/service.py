from dataclasses import dataclass
from datetime import datetime, timedelta

from jose import jwt
from pydantic import EmailStr

from app.auth.exceptions import PasswordIsIncorrectException
from app.auth.utils import Security
from app.settings import Settings
from app.users.exceptions import UserWithThisEmailNotExistException, UserWithThisEmailAlreadyExistException
from app.users.models import User
from app.users.repository import UserRepository
from app.users.schemas import LoginUserRequestSchema, UserSuccessfullyAuthorizedSchema, UserCreateRequestSchema


@dataclass
class AuthService:
    user_repository: UserRepository
    security: Security
    settings: Settings

    async def registration(self, data: UserCreateRequestSchema):
        user_with_same_email: User = await self.user_repository.get_user_by_email(data.email)
        if user_with_same_email:
            raise UserWithThisEmailAlreadyExistException(data.email)
        new_user: User = await self.user_repository.create_user(data)
        return new_user

    async def login(self, data: LoginUserRequestSchema) -> UserSuccessfullyAuthorizedSchema:
        user: User | None = await self.user_repository.get_user_by_email(data.email)
        if not user:
            raise UserWithThisEmailNotExistException(data.email)
        if not self.security.verify_password(data.password, user.password):
            raise PasswordIsIncorrectException()
        access_token: str = self.generate_access_token(data.email)
        return UserSuccessfullyAuthorizedSchema(
            access_token=access_token,
            email=data.email,
        )

    def generate_access_token(self, email: EmailStr) -> str:
        expire_time_unix = (
                datetime.utcnow() + timedelta(minutes=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp()
        token = jwt.encode(
            {"email": email, "expire": expire_time_unix},
            self.settings.JWT_SECRET_KEY,
            algorithm=self.settings.JWT_DECODE_ALGORITHM,
        )
        return token
