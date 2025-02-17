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


class UserSuccessfullyAuthorizedResponseSchema(BaseModel):
    email: EmailStr
    access_token: str
