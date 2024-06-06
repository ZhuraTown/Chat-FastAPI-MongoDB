from typing import Optional
from pydantic import Field, EmailStr

from datetime import datetime
from uuid import UUID, uuid4

from beanie import Document, Indexed


class User(Document):
    id: UUID = Field(default_factory=uuid4)
    email: Indexed(EmailStr, unique=True)
    username: Indexed(str, unique=True)
    about_me: Optional[str] = Field(None)

    hash_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    deleted_at: Optional[datetime] = Field(None)
    # todo: make later
    # email_confirmed_at: datetime | None = None

    class Settings:
        name = "users"
        validate_on_save = True

    class Config:
        json_schema_extra = {
            "example": {
                "id": "88ec9ec7-27bf-415f-b740-1d87dcefdbcf",
                "email": "example@user.com",
                "username": "ExampleUser",
                "about_me": "Good boy!",
                "created_at": "2024-01-01 00:00:01",
            },
        }
