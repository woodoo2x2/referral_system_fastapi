from dataclasses import dataclass


@dataclass
class ExternalApiException(Exception):
    @property
    def message(self):
        return "External api Error, please try again later"


@dataclass
class HunterApiResponseException(ExternalApiException):
    status_code: int

    @property
    def message(self):
        return f"Hunter api error, response code - {self.status_code}"


@dataclass
class EmailVerificationByHunterApiException(ExternalApiException):
    email: str

    @property
    def message(self):
        return f"{self.email} is not valid"
