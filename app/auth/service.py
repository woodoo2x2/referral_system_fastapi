from dataclasses import dataclass
from datetime import datetime, timedelta

from jose import jwt
from pydantic import EmailStr

from app.auth.exceptions import PasswordIsIncorrectException, AccessTokenExpiredException

from app.settings import Settings
from app.users.exceptions import UserWithThisEmailNotExistException, UserWithThisEmailAlreadyExistException
from app.users.models import User
from app.users.repository import UserRepository
from app.users.schemas import LoginUserRequestSchema, UserSuccessfullyAuthorizedSchema, UserCreateRequestSchema, \
    RegistrationAsReferralRequestSchema
from app.referral.exceptions import ReferralCodeNotExistException
from app.auth.utils import SecurityConfig


@dataclass
class AuthService:
    user_repository: UserRepository
    security: SecurityConfig
    settings: Settings

    async def registration(self, data: UserCreateRequestSchema):
        await self.check_user_already_exist_with_this_email(data.email)
        new_user: User = await self.user_repository.create_user(data)
        return new_user

    async def registration_as_referral(self, data: RegistrationAsReferralRequestSchema):
        await self.check_user_already_exist_with_this_email(data.email)
        user = await self.user_repository.get_user_by_referral_code(data.referral_code)
        if not user:
            raise ReferralCodeNotExistException()
        new_user: User = await self.user_repository.create_user_as_referral(data, user.id)
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

    async def check_user_already_exist_with_this_email(self, email: str) -> None:
        user_with_same_email: User = await self.user_repository.get_user_by_email(email)
        if user_with_same_email:
            raise UserWithThisEmailAlreadyExistException(email)

    def generate_access_token(self, email: EmailStr) -> str:
        expire_time_unix = (
                datetime.utcnow() + timedelta(minutes=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp()
        token = jwt.encode(
            {"email": email, "exp": expire_time_unix},
            self.settings.JWT_SECRET_KEY,
            algorithm=self.settings.JWT_DECODE_ALGORITHM,
        )
        return token

    def decode_jwt(self, token: str) -> dict | None:
        payload = jwt.decode(
            token,
            self.settings.JWT_SECRET_KEY,
            algorithms=[self.settings.JWT_DECODE_ALGORITHM],
            options={"verify_exp": False}
        )
        current_time = datetime.utcnow().timestamp()
        if payload['exp'] < current_time:
            raise AccessTokenExpiredException()
        return payload

    async def get_current_user_email(self, token: str) -> str:
        payload = self.decode_jwt(token)
        return payload['email']

