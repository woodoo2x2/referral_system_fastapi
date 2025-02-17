from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.auth.schemas import ErrorSchema
from app.dependency import get_user_repository
from app.exceptions import ApplicationException
from app.users.models import User
from app.users.repository import UserRepository
from app.users.schemas import UserCreateRequestSchema, UserResponseSchema

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
        user_repository: UserRepository = Depends(get_user_repository)
):
    try:
        await user_repository.check_if_user_already_uses_email(data.email)
        new_user: User = await user_repository.create_user(data)
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})
    return UserResponseSchema.from_database(new_user)


@router.post('/login')
def login_handler():
    pass
