from pydantic import BaseModel, EmailStr

from app.users.models import User


class UserCreateRequestSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponseSchema(BaseModel):
    id: int
    email: EmailStr

    @classmethod
    def from_database(cls, user: User) -> 'UserResponseSchema':
        return UserResponseSchema(id=user.id, email=user.email)


class LoginUserRequestSchema(BaseModel):
    email: EmailStr
    password: str


class UserSuccessfullyAuthorizedSchema(BaseModel):
    email: EmailStr
    access_token: str


class UserLoginResponse(BaseModel):
    your_email: EmailStr
    your_access_token: str


class UserCreateReferralCodeResponseSchema(BaseModel):
    your_id: int
    your_email: EmailStr
    your_referral_code: str

    @classmethod
    def from_user(cls, user: User):
        return cls(your_id=user.id,
                   your_email=user.email,
                   your_referral_code=user.referral_code)
