from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.dependency import get_referral_service, get_current_user_email
from app.exceptions import ApplicationException
from app.referral.schemas import ReferralCodeResponseSchema, CreateReferralCodeRequestSchema, \
    GetReferralCodeByEmailRequestSchema
from app.referral.service import ReferralService
from app.users.schemas import UserCreateReferralCodeResponseSchema

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


@router.post("/get_referral_code_by_email")
async def get_referral_code_by_email(
        data: GetReferralCodeByEmailRequestSchema,
        referral_service: ReferralService = Depends(get_referral_service),
        user_email: str = Depends(get_current_user_email),
) -> ReferralCodeResponseSchema:
    try:
        referral_code = await referral_service.get_referral_code(data.email)
        return ReferralCodeResponseSchema(referral_code=referral_code)
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})

