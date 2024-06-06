from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette import status

from users.application.auth.jwt import decode_jwt
from users.application.services.interfaces.user import UserServiceI
from enums import TokenTypes
from users.presentation.api.deps.services import get_user_service

security = HTTPBearer()


async def get_current_user(
        token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
        service: Annotated[UserServiceI, Depends(get_user_service)],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Bad credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = decode_jwt(token.credentials)
    if not token_data or token_data.token_type == TokenTypes.REFRESH:
        raise credentials_exception
    user = await service.get(token_data.user_oid)
    if user is None:
        raise credentials_exception
    return user
