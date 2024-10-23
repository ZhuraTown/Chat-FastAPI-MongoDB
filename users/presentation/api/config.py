from typing import Sequence

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class ApiConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="API_")

    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = False
    WORKERS: int = 4
    ALLOWED_HOSTS: Sequence[str] = ["*"]


class AuthConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="AUTH_")
    SECRET_KEY: str = "secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_TTL: int = 30
    REFRESH_TOKEN_TTL: int = 4320


api_settings = ApiConfig()
auth_settings = AuthConfig()
