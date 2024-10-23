from pydantic import BaseModel


class AuthEmailPasswordRequest(BaseModel):
    email: str
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str
