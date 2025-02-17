from dataclasses import dataclass

from app.exceptions import ApplicationException


@dataclass(frozen=True, eq=False)
class PasswordIsIncorrectException(ApplicationException):

    def message(self):
        return "You enter incorrect login password"
