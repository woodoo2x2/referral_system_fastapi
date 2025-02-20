from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from app.api.exceptions import ExternalApiException
from app.auth.schemas import ErrorSchema
from app.auth.service import AuthService
from app.dependency import get_auth_service
from app.exceptions import ApplicationException
from app.users.schemas import (
    UserCreateRequestSchema,
    UserResponseSchema,
    LoginUserRequestSchema,
    UserSuccessfullyAuthorizedSchema,
    UserLoginResponse,
    RegistrationAsReferralRequestSchema,
    RegistrationAsReferralResponseSchema,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    description="Authorize to API",
    response_model=UserLoginResponse,
    responses={
        status.HTTP_200_OK: {"model": UserLoginResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def login_handler(
    data: LoginUserRequestSchema, auth_service: AuthService = Depends(get_auth_service)
):
    try:
        user_data: UserSuccessfullyAuthorizedSchema = await auth_service.login(data)
        return UserLoginResponse(email=user_data.email, token=user_data.access_token)
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"error": exception.message}
        )


@router.post(
    "/registration",
    status_code=status.HTTP_201_CREATED,
    description="Create user",
    responses={
        status.HTTP_201_CREATED: {"model": UserResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def registration_handler(
    data: UserCreateRequestSchema, auth_service: AuthService = Depends(get_auth_service)
):
    try:
        new_user = await auth_service.registration(data)
        return UserResponseSchema.from_user(new_user)
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"error": exception.message}
        )
    except ExternalApiException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"error": exception.message}
        )


@router.post("/registration_as_referral")
async def registration_as_referral_handler(
    data: RegistrationAsReferralRequestSchema,
    auth_service: AuthService = Depends(get_auth_service),
) -> RegistrationAsReferralResponseSchema:
    try:
        new_user = await auth_service.registration_as_referral(data)
        return RegistrationAsReferralResponseSchema.from_user(new_user)
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"error": exception.message}
        )

    except ExternalApiException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"error": exception.message}
        )
