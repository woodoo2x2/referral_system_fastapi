from dataclasses import dataclass

from app.exceptions import ApplicationException


@dataclass
class ReferralCodeNotExistException(ApplicationException):
    email: str

    @property
    def message(self):
        return f"Referral code for user with email - {self.email} not exists"


@dataclass
class ReferralCodeForThisUserAlreadyExist(ApplicationException):
    email: str

    @property
    def message(self):
        return f"Referral code for user with email - {self.email} already exist"


@dataclass
class DeleteNotExistedReferralCodeException(ApplicationException):
    @property
    def message(self):
        return f"This user not have referral code"


@dataclass
class ReferralCodeExpiresException(ApplicationException):
    user_email: str

    @property
    def message(self):
        return f"Referral code user with emai:{self.user_email} is expired"


@dataclass
class UserWithThatIDNotExistException(ApplicationException):
    user_id: int

    @property
    def message(self):
        return f"User with id {self.user_id} not registred"
