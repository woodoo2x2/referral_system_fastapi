from dataclasses import dataclass

from app.exceptions import ApplicationException


@dataclass
class UserWithThisEmailAlreadyExistException(ApplicationException):
    email: str

    @property
    def message(self):
        return f"User with email:{self.email} already exist"


@dataclass
class UserWithThisEmailNotExistException(ApplicationException):
    email: str

    @property
    def message(self):
        return f"User with email:{self.email} not exist"
