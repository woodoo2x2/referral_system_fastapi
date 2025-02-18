from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from starlette.requests import Request

from app.auth.schemas import ErrorSchema
from app.auth.service import AuthService
from app.dependency import get_auth_service
from app.exceptions import ApplicationException
from app.users.schemas import UserCreateRequestSchema, UserResponseSchema, LoginUserRequestSchema, \
    UserSuccessfullyAuthorizedSchema, UserLoginResponse, RegistrationAsReferralRequestSchema, \
    RegistrationAsReferralResponseSchema

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/registration',
             status_code=status.HTTP_201_CREATED,
             description='Create user',
             responses={
                 status.HTTP_201_CREATED: {'model': UserResponseSchema},
                 status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
             })
async def registration_handler(
        data: UserCreateRequestSchema,
        auth_service: AuthService = Depends(get_auth_service)
):
    try:
        new_user = await auth_service.registration(data)
        return UserResponseSchema.from_database(new_user)
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})


@router.post('/login',
             status_code=status.HTTP_200_OK,
             description='Authorize to API',
             responses={
                 status.HTTP_200_OK: {'model': UserLoginResponse},
                 status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema},
             })
async def login_handler(
        request: Request,
        data: LoginUserRequestSchema,
        auth_service: AuthService = Depends(get_auth_service)):
    try:
        user_data: UserSuccessfullyAuthorizedSchema = await auth_service.login(data)
        request.session['access_token'] = user_data.access_token
        return UserLoginResponse(
            your_email=user_data.email,
            your_access_token=user_data.access_token
        )
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})


@router.post("/logout")
async def logout(request: Request):
    if "access_token" in request.session:
        request.session.pop("access_token")
        return {"message": "Logout successful"}
    else:
        return {"message": "No active session found"}


@router.post("/registration_as_referral")
async def registration_as_referral_handler(
        data: RegistrationAsReferralRequestSchema,
        auth_service: AuthService = Depends(get_auth_service),
) -> RegistrationAsReferralResponseSchema:
    try:
        new_user = await auth_service.registration_as_referral(data)
        return RegistrationAsReferralResponseSchema.from_user(new_user)
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})

