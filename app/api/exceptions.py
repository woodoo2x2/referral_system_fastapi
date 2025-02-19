from dataclasses import dataclass


@dataclass(frozen=True, eq=False)
class ExternalApiException(Exception):

    @property
    def message(self):
        return "External api Error, please try again later"


@dataclass(frozen=True, eq=False)
class HunterApiResponseException(ExternalApiException):
    status_code: int

    @property
    def message(self):
        return f"Hunter api error, response code - {self.status_code}"


@dataclass(frozen=True, eq=False)
class EmailVerificationByHunterApiException(ExternalApiException):
    email: str

    @property
    def message(self):
        return f"{self.email} is not valid"
