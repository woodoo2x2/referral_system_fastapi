from dataclasses import dataclass

import httpx

from app.api.exceptions import HunterApiResponseException
from app.settings import Settings


@dataclass
class HunterApiService:
    settings: Settings

    async def verify_email(self, email: str) -> str:
        params = {"email": email, "api_key": self.settings.EMAIL_HUNTER_API_KEY}

        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.settings.EMAIL_HUNTER_BASE_URL, params=params
            )

        if response.status_code == 200:
            return response.json()

        else:
            raise HunterApiResponseException(response.status_code)
