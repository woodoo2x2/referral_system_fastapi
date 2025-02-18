from dataclasses import dataclass

from app.exceptions import ApplicationException


@dataclass(frozen=True, eq=False)
class ReferralCodeForThisUserAlreadyExist(ApplicationException):
    user_id: int

    @property
    def message(self):
        return f"Referral code for user with id - {self.user_id} already exist"


@dataclass(frozen=True, eq=False)
class DeleteNotExistedReferralCodeException(ApplicationException):

    @property
    def message(self):
        return f"This user not have referral code"
