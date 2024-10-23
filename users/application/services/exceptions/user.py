from dataclasses import dataclass
from uuid import UUID

from fastapi.exceptions import ValidationException


@dataclass
class UserNotExistError(ValidationException):
    oid: UUID

    @property
    def message(self) -> str:
        return f"User with id:{self.id} not exist!"


@dataclass
class UsernameAlreadyExistError(ValidationException):
    username: str

    @property
    def message(self) -> str:
        return f"User with username:{self.username} already exist!"


@dataclass
class EmailAlreadyExistError(ValidationException):
    email: str

    @property
    def message(self) -> str:
        return f"User with email:{self.email} already exist!"
