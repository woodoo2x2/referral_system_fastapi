from dataclasses import dataclass

from app.exceptions import ApplicationException


@dataclass(frozen=True, eq=False)
class ReferralCodeNotExistException(ApplicationException):
    email: str

    @property
    def message(self):
        return f"Referral code for user with email - {self.email} not exists"


@dataclass(frozen=True, eq=False)
class ReferralCodeForThisUserAlreadyExist(ApplicationException):
    email: str

    @property
    def message(self):
        return f"Referral code for user with email - {self.email} already exist"


@dataclass(frozen=True, eq=False)
class DeleteNotExistedReferralCodeException(ApplicationException):

    @property
    def message(self):
        return f"This user not have referral code"


@dataclass(frozen=True, eq=False)
class ReferralCodeExpiresException(ApplicationException):
    user_email: str

    @property
    def message(self):
        return f"Referral code user with emai:{self.user_email} is expired"
