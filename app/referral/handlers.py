from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from starlette.requests import Request

from app.auth.service import AuthService
from app.dependency import get_auth_service, get_referral_service
from app.exceptions import ApplicationException
from app.referral.service import ReferralService
from app.users.schemas import UserCreateReferralCodeResponseSchema

router = APIRouter(prefix='/referral', tags=['referral'])


@router.post('/')
async def create_referral_code_for_me_handler(
        request: Request,
        auth_service: AuthService = Depends(get_auth_service),
        referral_service: ReferralService = Depends(get_referral_service)
) -> UserCreateReferralCodeResponseSchema:
    try:
        access_token = request.session['access_token']
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token was not found")
    try:
        user_email = await auth_service.get_current_user_email(access_token)
        updated_user = await referral_service.create_referral_code(user_email)
        return UserCreateReferralCodeResponseSchema.from_user(updated_user)
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message})
