from jose import jwt, JWTError
from datetime import datetime, timezone, timedelta

from enums import TokenTypes
from presentation.api.config import auth_settings
from transfer.auth import JWTTokenDTO, TokenData


def create_access_token(data: dict) -> JWTTokenDTO:
    access_data = data.copy()
    refresh_data = data.copy()
    access_data["token_type"] = TokenTypes.ACCESS
    refresh_data["token_type"] = TokenTypes.REFRESH
    access_data["exp"] = datetime.now(timezone.utc) + timedelta(seconds=auth_settings.ACCESS_TOKEN_TTL)
    refresh_data["exp"] = datetime.now(timezone.utc) + timedelta(seconds=auth_settings.REFRESH_TOKEN_TTL)

    access_token = jwt.encode(access_data, auth_settings.SECRET_KEY, algorithm=auth_settings.ALGORITHM)
    refresh_token = jwt.encode(refresh_data, auth_settings.SECRET_KEY, algorithm=auth_settings.ALGORITHM)
    return JWTTokenDTO(access_token=access_token, refresh_token=refresh_token)


def decode_jwt(token: str) -> TokenData | None:
    try:
        payload = jwt.decode(token, auth_settings.SECRET_KEY, algorithms=[auth_settings.ALGORITHM])
        user_oid: str = payload.get("sub")
        token_type: TokenTypes = payload.get("token_type")
        if user_oid is None or token_type is None:
            return None
        token_data = TokenData(user_oid=user_oid, token_type=token_type)
    except JWTError:
        return None
    return token_data

