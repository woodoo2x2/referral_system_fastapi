from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from starlette.requests import Request

from app.auth.schemas import ErrorSchema
from app.dependency import get_user_repository, get_auth_service
from app.exceptions import ApplicationException
from app.users.models import User
from app.users.repository import UserRepository
from app.users.schemas import UserCreateRequestSchema, UserResponseSchema, LoginUserRequestSchema, \
    UserSuccessfullyAuthorizedSchema, UserLoginResponse
from app.auth.service import AuthService

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
