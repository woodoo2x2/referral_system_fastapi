from dataclasses import dataclass

from app.exceptions import ApplicationException


@dataclass(frozen=True,eq=False)
class UserWithThisEmailAlreadyExistException(ApplicationException):
    email: str

    @property
    def message(self):
        return f"User with email:{self.email} already exist"


@dataclass(frozen=True,eq=False)
class UserWithThisEmailNotExistException(ApplicationException):
    email: str

    @property
    def message(self):
        return f"User with email:{self.email} not exist"
