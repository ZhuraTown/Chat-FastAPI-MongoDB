from dotenv import load_dotenv
from pydantic import field_validator, MongoDsn
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings

load_dotenv()


class InfrastructureSettings(BaseSettings):
    # MONGO CONFIG
    db_user: str
    db_password: str
    db_name: str
    db_host: str
    db_port: int
    mongo_dsn: MongoDsn | None = None

    @field_validator("mongo_dsn", mode="before")  # noqa
    @classmethod
    def get_mongo_dsn(cls, _, info: ValidationInfo):
        return MongoDsn.build(
            scheme="mongodb",
            username=info.data["db_user"],
            password=info.data["db_password"],
            host=info.data["db_host"],
            port=info.data["db_port"],
            path=info.data["db_name"],
        )



class Settings(BaseSettings):
    infrastructure: InfrastructureSettings = InfrastructureSettings()


settings = Settings()
