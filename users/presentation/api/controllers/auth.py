from http import HTTPStatus
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from presentation.api.controllers.requests.auth import RefreshTokenRequest
from presentation.api.controllers.responses.auth import AuthResponse
from users.application.auth.jwt import create_access_token, decode_jwt
from users.application.services.interfaces.user import UserServiceI
from enums import TokenTypes
from users.presentation.api.deps.services import get_user_service

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post(
    "/",
    description="Аутентификация",
    response_model=AuthResponse,
    status_code=HTTPStatus.OK,
)
async def auth_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: Annotated[UserServiceI, Depends(get_user_service)],
):
    user = await service.authenticate(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="username or password invalid")

    return create_access_token({"sub": str(user.oid)})


@router.post(
    "/refresh",
    response_model=AuthResponse,
    status_code=HTTPStatus.OK,
)
async def refresh_token(
    form_data: RefreshTokenRequest,
    service: Annotated[UserServiceI, Depends(get_user_service)],
):
    token_data = decode_jwt(form_data.refresh_token)
    if not token_data or token_data.token_type != TokenTypes.REFRESH:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="not valid token")

    user = await service.get(token_data.user_oid)
    if not user:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="user not found")

    return create_access_token({"sub": str(user.oid)})


