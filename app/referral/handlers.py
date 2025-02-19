from fastapi import APIRouter, Depends, HTTPException
from pydantic import EmailStr
from starlette import status

from app.dependency import get_referral_service, get_current_user_email
from app.exceptions import ApplicationException
from app.referral.schemas import ReferralCodeResponseSchema, CreateReferralCodeRequestSchema
from app.referral.service import ReferralService
from app.users.schemas import UserCreateReferralCodeResponseSchema, UserResponseSchema

router = APIRouter(prefix='/referral', tags=['referral'])


@router.post('/')
async def create_referral_code_for_me_handler(
        data: CreateReferralCodeRequestSchema,
        referral_service: ReferralService = Depends(get_referral_service),
        user_email: str = Depends(get_current_user_email),
) -> UserCreateReferralCodeResponseSchema:
    try:
        updated_user = await referral_service.create_referral_code(user_email, lifetime_minutes=data.lifetime_minutes)
        return UserCreateReferralCodeResponseSchema.from_user(updated_user)
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})


@router.get('/')
async def get_my_referral_code_handler(
        referral_service: ReferralService = Depends(get_referral_service),
        user_email: str = Depends(get_current_user_email),
) -> ReferralCodeResponseSchema:
    try:
        referral_code = await referral_service.get_referral_code(user_email)
        return ReferralCodeResponseSchema(referral_code=referral_code)
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})


@router.delete('/')
async def delete_my_referral_code_handler(
        referral_service: ReferralService = Depends(get_referral_service),
        user_email: str = Depends(get_current_user_email),
):
    try:
        referral_code = await referral_service.delete_referral_code(user_email)
        return {"message": f"{referral_code} was successfully deleted"}
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})


@router.get("/{email}")
async def get_referral_code_by_email(
        email: EmailStr,
        referral_service: ReferralService = Depends(get_referral_service),
        user_email: str = Depends(get_current_user_email),
) -> ReferralCodeResponseSchema:
    try:
        referral_code = await referral_service.get_referral_code(email)
        return ReferralCodeResponseSchema(referral_code=referral_code)
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})


@router.get("/all/{user_id}")
async def get_all_invited_users_by_referrer_id(
        user_id: int,
        referral_service: ReferralService = Depends(get_referral_service),
        user_email: str = Depends(get_current_user_email),
):
    try:
        users = await referral_service.get_all_invited_users_by_referral_id(user_id)
        return users
    except ApplicationException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})



