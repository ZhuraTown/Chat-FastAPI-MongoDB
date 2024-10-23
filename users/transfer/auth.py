from uuid import UUID

from pydantic import BaseModel

from enums import TokenTypes


class JWTTokenDTO(BaseModel):
    access_token: str
    refresh_token: str


class TokenData(BaseModel):
    user_oid: UUID
    token_type: TokenTypes
