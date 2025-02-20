from dataclasses import dataclass

from app.exceptions import ApplicationException


class PasswordIsIncorrectException(ApplicationException):
    @property
    def message(self):
        return "You enter incorrect login password"


@dataclass
class AccessTokenExpiredException(ApplicationException):
    @property
    def message(self):
        return "Your access token is expired. Please repeat login."


@dataclass
class TokenNotFoundException(ApplicationException):
    @property
    def message(self):
        return "Token was not found"
