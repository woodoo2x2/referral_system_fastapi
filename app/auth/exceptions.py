from dataclasses import dataclass

from app.exceptions import ApplicationException


@dataclass(frozen=True, eq=False)
class PasswordIsIncorrectException(ApplicationException):
    @property
    def message(self):
        return "You enter incorrect login password"


@dataclass(frozen=True, eq=False)
class AccessTokenIsInvalidException(ApplicationException):
    @property
    def message(self):
        return "Your token is invalid"


@dataclass(frozen=True, eq=False)
class AccessTokenExpiredException(ApplicationException):
    @property
    def message(self):
        return "Your token is expired. Please repeat login."


@dataclass(frozen=True, eq=False)
class TokenNotFoundException(ApplicationException):

    @property
    def message(self):
        return "Token was not found"
